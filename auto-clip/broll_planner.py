"""
auto-clip/broll_planner.py -- turn an article / paragraph of text into an ordered VISUAL-BEAT plan.

Phase-0 of the "AI-article -> b-roll" pipeline. This is the PLANNER ONLY: it reads prose
(an article, a script paragraph, a news-radar story) and emits a broll-plan.json -- an ordered
list of visual beats, each:
    {beat, on_screen_text, suggested_visual, seconds, source_sentence, keywords}
plus a header (title, totals, est_runtime_s) and a `next_steps` block that documents the two
DOWNSTREAM stages that are intentionally OFF in Phase-0:
    - FETCH    (pull/generate the actual footage for each beat) -- STUBBED, clearly labeled.
    - ASSEMBLE (lay the beats onto a timeline / render)         -- STUBBED, clearly labeled.
Both stubs print exactly what they WOULD do and refuse to do anything real (no network, no
files fetched, no render). Turning them on is a separate, gated build.

How beats get chosen (two "brains", same deterministic time-mapping in Python):
  heuristic (default) -- NO key, NO install. Splits prose into sentences, scores each for
                         "show-worthiness" (concrete nouns, numbers, named entities, contrast
                         words), keeps the ordered top-N, derives a short on_screen_text + a
                         suggested_visual category + a per-beat duration from word count.
  agent               -- the Claude Code agent IS the planner (mirrors highlight.py's --provider
                         agent two-step). Run once to emit data/<stem>.broll-prompt.json and stop;
                         the agent writes data/<stem>.broll-picks.json; re-run --from-picks to
                         validate + map to the final plan. No API key / no Ollama needed.

This is additive + read-only: it reads text (from --file or --text or a tiny built-in sample),
writes ONLY a plan JSON (and, for --provider agent, a prompt/picks scratch file). It never
fetches media, never renders, never publishes.

Usage:
  python broll_planner.py --text "Your paragraph here."
  python broll_planner.py --file article.txt --title "My Article" --target-seconds 45
  python broll_planner.py --file article.txt --provider agent           # step 1: emit prompt
  python broll_planner.py --file article.txt --provider agent --from-picks data/<stem>.broll-picks.json
  python broll_planner.py --self-test                                   # offline sanity check

Writes:
  out/<stem>.broll-plan.json      ordered beat plan (the deliverable)
  data/<stem>.broll-prompt.json   (--provider agent step 1 only)
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "out"
DATA = BASE / "data"

# --- pacing knobs (deterministic, tweakable) --------------------------------
WORDS_PER_SECOND = 2.6     # ~157 wpm VO -> seconds a line of on-screen text wants to breathe
MIN_BEAT_S = 2.0           # floor: even a tiny beat needs to register
MAX_BEAT_S = 7.0           # ceiling: one b-roll shot shouldn't overstay
DEFAULT_TARGET_S = 40.0    # default total runtime we plan toward
ON_SCREEN_MAX_WORDS = 9    # short-form on-screen text stays skimmable

SAMPLE = (
    "OpenAI released a new model this week that scores 30 percent higher on coding "
    "benchmarks than the previous version. Developers can now generate an entire app "
    "from a single prompt. But critics warn the tool still hallucinates dependencies "
    "that do not exist. Meanwhile, startups are racing to build on top of it, and "
    "investors poured two billion dollars into the space last quarter."
)


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:  # Windows cp1252 console chokes on emoji/smart-quotes/arrows
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


# ---- text helpers ---------------------------------------------------------

_WS_RE = re.compile(r"\s+")
# sentence split: end punctuation followed by space + capital/quote/number, keeps it simple + offline
_SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[\"'(\[A-Z0-9])")
_NUM_RE = re.compile(r"\b\d[\d,\.]*\s?(?:%|percent|billion|million|thousand|x|k|m|b)?\b", re.I)
_CAP_RE = re.compile(r"\b[A-Z][a-zA-Z0-9]+\b")  # crude proper-noun / named-entity proxy

CONTRAST_WORDS = {"but", "however", "yet", "meanwhile", "instead", "although",
                  "despite", "while", "whereas", "still", "critics", "warn"}
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "that", "this", "it", "is", "are", "was", "were", "be", "been", "being", "as",
    "at", "by", "from", "into", "than", "then", "so", "if", "can", "now", "new",
    "they", "you", "your", "their", "its", "his", "her", "our", "we", "i", "he",
    "she", "not", "no", "do", "does", "did", "will", "would", "could", "should",
    "have", "has", "had", "up", "out", "about", "over", "more", "most", "some",
    "all", "one", "two", "still", "also", "just", "like", "what", "which", "who",
    "how", "when", "where", "why", "them", "these", "those", "there", "here",
}


def clean(text):
    return _WS_RE.sub(" ", (text or "")).strip()


def split_sentences(text):
    text = clean(text)
    if not text:
        return []
    parts = _SENT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def keywords_of(sentence, k=4):
    """Top content words (longest non-stopword tokens), order-preserving + deduped."""
    toks = re.findall(r"[A-Za-z][A-Za-z0-9\-']+", sentence)
    seen, out = set(), []
    for t in toks:
        low = t.lower()
        if low in STOPWORDS or len(low) < 3:
            continue
        if low in seen:
            continue
        seen.add(low)
        out.append(t)
    # prefer numbers / capitalized terms first, then by length
    out.sort(key=lambda w: (0 if (w[0].isupper() or w[0].isdigit()) else 1, -len(w)))
    return out[:k]


def show_worthiness(sentence):
    """Heuristic 0..1: how much this sentence WANTS a visual (concrete > abstract)."""
    s = sentence.lower()
    nums = len(_NUM_RE.findall(sentence))
    caps = len(_CAP_RE.findall(sentence))
    contrast = sum(1 for w in CONTRAST_WORDS if w in s.split())
    words = max(len(sentence.split()), 1)
    # concrete signals reward; very long sentences slightly penalized (harder to show)
    score = (0.34 * min(nums, 3) / 3.0
             + 0.30 * min(caps, 4) / 4.0
             + 0.18 * min(contrast, 2) / 2.0
             + 0.18 * (1.0 if 6 <= words <= 26 else 0.4))
    return round(min(score, 1.0), 4)


def on_screen_text(sentence):
    """Compress a sentence to a short, skimmable on-screen line (<= ON_SCREEN_MAX_WORDS)."""
    words = re.findall(r"[\w%$\-']+|[.,!?]", sentence)
    # drop a leading connective so the line starts with substance
    while words and words[0].lower() in {"but", "however", "meanwhile", "and", "so", "yet"}:
        words = words[1:]
    line = []
    count = 0
    for w in words:
        if w in {".", ",", "!", "?"}:
            continue
        line.append(w)
        count += 1
        if count >= ON_SCREEN_MAX_WORDS:
            break
    text = " ".join(line).strip().rstrip(",")
    return text or clean(sentence)[:60]


def suggested_visual(sentence, kws):
    """Map a sentence to a coarse b-roll CATEGORY + a concrete shot suggestion.
    Deterministic + offline; the FETCH stage (when built) turns this into real footage."""
    s = sentence.lower()
    kw_phrase = ", ".join(kws[:3]) if kws else "the key subject"
    if _NUM_RE.search(sentence):
        return {"category": "data-stat",
                "shot": f"Animated stat / number callout for: {kw_phrase}"}
    if any(w in s.split() for w in CONTRAST_WORDS):
        return {"category": "contrast",
                "shot": f"Split-screen or before/after illustrating the tension around {kw_phrase}"}
    if _CAP_RE.search(sentence):
        return {"category": "entity",
                "shot": f"Logo / product / location B-roll of {kw_phrase}"}
    if any(w in s for w in ("build", "create", "make", "generate", "code", "develop", "launch")):
        return {"category": "process",
                "shot": f"Screen-recording / hands-on B-roll showing {kw_phrase} in action"}
    return {"category": "concept",
            "shot": f"Abstract / metaphor B-roll evoking {kw_phrase}"}


def beat_seconds(on_text, scale=1.0):
    """Per-beat duration from on-screen word count, clamped to [MIN,MAX]."""
    words = max(len(on_text.split()), 1)
    raw = (words / WORDS_PER_SECOND) * scale
    return round(min(max(raw, MIN_BEAT_S), MAX_BEAT_S), 1)


# ---- plan assembly (the actual planner) -----------------------------------

def plan_from_sentences(sentences, target_seconds, max_beats):
    """Score sentences, keep an ordered subset that fits target_seconds, build beats."""
    scored = []
    for i, sent in enumerate(sentences):
        scored.append({"idx": i, "sentence": sent, "score": show_worthiness(sent)})

    # rank by show-worthiness, but KEEP ORIGINAL ORDER in the final plan (narrative flow)
    ranked = sorted(scored, key=lambda x: (-x["score"], x["idx"]))
    chosen, total = [], 0.0
    for item in ranked:
        if len(chosen) >= max_beats:
            break
        on_text = on_screen_text(item["sentence"])
        secs = beat_seconds(on_text)
        if total + secs > target_seconds and chosen:
            continue  # skip beats that would blow the target (keep at least one)
        item["_on_text"] = on_text
        item["_secs"] = secs
        chosen.append(item)
        total += secs

    chosen.sort(key=lambda x: x["idx"])  # restore narrative order
    beats = []
    for n, item in enumerate(chosen, 1):
        kws = keywords_of(item["sentence"])
        vis = suggested_visual(item["sentence"], kws)
        beats.append({
            "beat": n,
            "on_screen_text": item["_on_text"],
            "suggested_visual": vis["shot"],
            "visual_category": vis["category"],
            "seconds": item["_secs"],
            "source_sentence": item["sentence"],
            "keywords": kws,
            "show_score": item["score"],
        })
    return beats


def renumber_and_total(beats):
    for n, b in enumerate(beats, 1):
        b["beat"] = n
    return round(sum(b["seconds"] for b in beats), 1)


def build_plan(title, stem, beats, provider, source_chars):
    est = renumber_and_total(beats)
    return {
        "schema": "broll-plan/1",
        "title": title,
        "stem": stem,
        "provider": provider,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_chars": source_chars,
        "beat_count": len(beats),
        "est_runtime_s": est,
        "beats": beats,
        "next_steps": {
            "fetch": "STUB (OFF in Phase-0): would pull/generate footage per beat "
                     "(stock / Higgsfield / screen-rec). Run broll_planner.py --stub-fetch to see.",
            "assemble": "STUB (OFF in Phase-0): would lay beats on a timeline + render. "
                        "Run broll_planner.py --stub-assemble to see.",
        },
    }


# ---- agent provider (Claude IS the planner) -------------------------------

AGENT_SYSTEM = (
    "You are a short-form video editor planning B-ROLL for narrated text. Given an article/"
    "paragraph, return an ordered list of visual beats. Each beat covers a span of the text and "
    "names: a SHORT on-screen text line (<=9 words), a concrete SUGGESTED VISUAL (one shot), and "
    "the source sentence it illustrates. Keep narrative order. Return STRICT JSON only, no prose."
)
AGENT_PICK_SCHEMA = (
    '[{"on_screen_text": <str <=9 words>, "suggested_visual": <one concrete shot>, '
    '"source_sentence": <the sentence it illustrates>, "seconds": <2-7>}]'
)


def emit_agent_prompt(stem, title, sentences):
    DATA.mkdir(exist_ok=True)
    payload = {
        "system": AGENT_SYSTEM,
        "schema": AGENT_PICK_SCHEMA,
        "title": title,
        "instructions": (
            "Read the numbered sentences. Choose an ORDERED set of beats (typically one per "
            "show-worthy sentence). For each beat emit the schema object. Write your answer as a "
            f"JSON array to data/{stem}.broll-picks.json, then re-run broll_planner.py with "
            "--provider agent --from-picks that file."
        ),
        "sentences": [{"idx": i, "text": s} for i, s in enumerate(sentences)],
    }
    path = DATA / f"{stem}.broll-prompt.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def beats_from_picks(picks):
    """Validate agent picks -> normalized beats (same shape as the heuristic planner)."""
    beats = []
    for n, p in enumerate(picks, 1):
        if not isinstance(p, dict):
            continue
        on_text = clean(str(p.get("on_screen_text", "")))[:120]
        shot = clean(str(p.get("suggested_visual", "")))
        src = clean(str(p.get("source_sentence", "")))
        if not (on_text and shot):
            continue
        try:
            secs = float(p.get("seconds", 0)) or beat_seconds(on_text)
        except (TypeError, ValueError):
            secs = beat_seconds(on_text)
        secs = round(min(max(secs, MIN_BEAT_S), MAX_BEAT_S), 1)
        kws = keywords_of(src or on_text)
        beats.append({
            "beat": n,
            "on_screen_text": on_text,
            "suggested_visual": shot,
            "visual_category": suggested_visual(src or on_text, kws)["category"],
            "seconds": secs,
            "source_sentence": src,
            "keywords": kws,
            "show_score": None,  # agent-chosen, no heuristic score
        })
    return beats


# ---- downstream STUBS (intentionally OFF in Phase-0) ----------------------

def stub_fetch(plan):
    """STUB -- does NOT fetch anything. Prints what a real FETCH stage WOULD do per beat."""
    log("=== FETCH STAGE: STUB (OFF in Phase-0) -- no network, no media pulled ===")
    for b in plan["beats"]:
        log(f"  [stub-fetch] beat {b['beat']} ({b['visual_category']}, {b['seconds']}s): "
            f"WOULD source -> {b['suggested_visual']}")
    log("  FETCH is intentionally disabled. Enabling it (stock API / Higgsfield / screen-rec) "
        "is a separate, gated build -- this planner stops at the plan.")


def stub_assemble(plan):
    """STUB -- does NOT render. Prints the timeline a real ASSEMBLE stage WOULD build."""
    log("=== ASSEMBLE STAGE: STUB (OFF in Phase-0) -- no timeline built, nothing rendered ===")
    t = 0.0
    for b in plan["beats"]:
        log(f"  [stub-assemble] {t:6.1f}s -> {t + b['seconds']:6.1f}s  "
            f"text='{b['on_screen_text']}'  visual='{b['suggested_visual']}'")
        t += b["seconds"]
    log(f"  Total timeline: {t:.1f}s across {len(plan['beats'])} beats. "
        "ASSEMBLE/render is intentionally disabled (separate, gated build).")


# ---- self-test ------------------------------------------------------------

def self_test():
    log("SELF-TEST: planning the built-in sample paragraph (offline, heuristic)...")
    sents = split_sentences(SAMPLE)
    assert len(sents) >= 4, f"sentence split failed: got {len(sents)}"
    beats = plan_from_sentences(sents, DEFAULT_TARGET_S, max_beats=12)
    assert beats, "no beats produced"
    plan = build_plan("Self-test", "selftest", beats, "heuristic", len(SAMPLE))

    # structural assertions
    assert plan["schema"] == "broll-plan/1"
    for b in plan["beats"]:
        for key in ("beat", "on_screen_text", "suggested_visual", "seconds",
                    "source_sentence", "keywords"):
            assert key in b, f"beat missing key: {key}"
        assert MIN_BEAT_S <= b["seconds"] <= MAX_BEAT_S, f"bad duration: {b['seconds']}"
        assert len(b["on_screen_text"].split()) <= ON_SCREEN_MAX_WORDS + 1, "on-screen text too long"
    assert [b["beat"] for b in plan["beats"]] == list(range(1, len(plan["beats"]) + 1)), \
        "beats not 1..N"
    # the stat sentence (30 percent / two billion) should be tagged data-stat somewhere
    cats = {b["visual_category"] for b in plan["beats"]}
    assert "data-stat" in cats, f"expected a data-stat beat; got {cats}"
    assert plan["est_runtime_s"] <= DEFAULT_TARGET_S + MAX_BEAT_S, "runtime overshot target"

    # stubs must be callable and side-effect-free (no files / network)
    stub_fetch(plan)
    stub_assemble(plan)

    log(f"SELF-TEST PASS: {plan['beat_count']} beats, est {plan['est_runtime_s']}s, "
        f"categories={sorted(cats)}")
    log("Sample plan (first 2 beats):")
    for b in plan["beats"][:2]:
        log(f"  beat {b['beat']} [{b['visual_category']}] {b['seconds']}s | "
            f"'{b['on_screen_text']}' -> {b['suggested_visual']}")
    return 0


# ---- main -----------------------------------------------------------------

def read_source(args):
    if args.text:
        return clean(args.text), (args.title or "Untitled paragraph"), (args.stem or "paragraph")
    if args.file:
        p = Path(args.file)
        p = p if p.is_absolute() else (BASE / p)
        if not p.exists():
            log(f"FATAL: --file not found: {p}")
            sys.exit(1)
        text = clean(p.read_text(encoding="utf-8", errors="replace"))
        return text, (args.title or p.stem), (args.stem or p.stem)
    # fall back to the built-in sample so a bare run still demonstrates the tool
    log("no --text/--file given -> using built-in SAMPLE paragraph (demo mode).")
    return clean(SAMPLE), (args.title or "Sample article"), (args.stem or "sample")


def main():
    ap = argparse.ArgumentParser(
        description="Plan ordered b-roll visual beats from an article/paragraph (Phase-0; "
                    "FETCH + ASSEMBLE are stubbed OFF).")
    ap.add_argument("--text", help="paragraph/article text inline")
    ap.add_argument("--file", help="path to a .txt/.md article (UTF-8)")
    ap.add_argument("--title", help="title for the plan (default: filename / 'Sample article')")
    ap.add_argument("--stem", help="output stem (default: from filename)")
    ap.add_argument("--target-seconds", type=float, default=DEFAULT_TARGET_S,
                    help=f"target total runtime to plan toward (default {DEFAULT_TARGET_S})")
    ap.add_argument("--max-beats", type=int, default=12, help="cap number of beats (default 12)")
    ap.add_argument("--provider", choices=["heuristic", "agent"], default="heuristic",
                    help="heuristic (offline, default) or agent (Claude Code two-step)")
    ap.add_argument("--from-picks", help="(agent step 2) path to data/<stem>.broll-picks.json")
    ap.add_argument("--stub-fetch", action="store_true",
                    help="run the FETCH stub on the produced plan (prints, fetches NOTHING)")
    ap.add_argument("--stub-assemble", action="store_true",
                    help="run the ASSEMBLE stub on the produced plan (prints, renders NOTHING)")
    ap.add_argument("--self-test", action="store_true", help="offline sanity check; writes nothing")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    text, title, stem = read_source(args)
    if not text:
        log("FATAL: empty source text.")
        sys.exit(1)
    sentences = split_sentences(text)
    if not sentences:
        log("FATAL: no sentences parsed from source.")
        sys.exit(1)
    log(f"source: '{title}' (stem={stem}) -- {len(text)} chars, {len(sentences)} sentences, "
        f"provider={args.provider}")

    # ---- agent provider: two-step (emit prompt -> ... -> from-picks) ----
    if args.provider == "agent" and not args.from_picks:
        path = emit_agent_prompt(stem, title, sentences)
        log(f"AGENT STEP 1: wrote {path}")
        log(f"  Next: the agent reads it, writes data/{stem}.broll-picks.json (array per schema), "
            f"then re-run:")
        log(f"  python broll_planner.py --file/--text ... --provider agent "
            f"--from-picks data/{stem}.broll-picks.json")
        return

    if args.from_picks:
        pp = Path(args.from_picks)
        pp = pp if pp.is_absolute() else (BASE / pp)
        if not pp.exists():
            log(f"FATAL: --from-picks not found: {pp}")
            sys.exit(1)
        try:
            picks = json.loads(pp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            log(f"FATAL: picks file is not valid JSON: {e}")
            sys.exit(1)
        if not isinstance(picks, list):
            log("FATAL: picks file must be a JSON array of beat objects.")
            sys.exit(1)
        beats = beats_from_picks(picks)
        if not beats:
            log("FATAL: no valid beats in picks file.")
            sys.exit(1)
        provider_label = "agent"
    else:
        beats = plan_from_sentences(sentences, args.target_seconds, args.max_beats)
        provider_label = "heuristic"
        if not beats:
            log("FATAL: heuristic planner produced no beats.")
            sys.exit(1)

    plan = build_plan(title, stem, beats, provider_label, len(text))

    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"{stem}.broll-plan.json"
    out_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"PLAN WRITTEN: {out_path}  ({plan['beat_count']} beats, est {plan['est_runtime_s']}s)")
    for b in plan["beats"]:
        log(f"  beat {b['beat']} [{b['visual_category']}] {b['seconds']}s | "
            f"'{b['on_screen_text']}' -> {b['suggested_visual']}")

    if args.stub_fetch:
        stub_fetch(plan)
    if args.stub_assemble:
        stub_assemble(plan)
    if not (args.stub_fetch or args.stub_assemble):
        log("FETCH + ASSEMBLE are STUBBED OFF (Phase-0). Add --stub-fetch / --stub-assemble "
            "to preview what those stages WOULD do. This engine stops at the plan JSON.")


if __name__ == "__main__":
    main()
