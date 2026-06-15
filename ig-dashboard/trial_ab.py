"""
trial_ab.py -- the trial-reel A/B MEASURE half (Wave-3 build, id=trial-ab).

Closes the loop that metrics2026.py was built for: take the variant reels Elijah
already runs, GROUP them into A/B experiments, SCORE each variant on the correct
2026 signals (by importing metrics2026.rank_posts() UNCHANGED), and DECLARE a
winner -- but with an HONESTY GATE that refuses to crown a winner on a tiny
sample or a razor-thin margin (an over-confident "winner" is worse than none).

This is the MEASURE half only. Generating the overlay x image variant matrix and
publishing trial reels is the ADD-LATER, Elijah-gated half (Standing Rule 1).
See docs/plans/2026-06-14-trial-reel-ab-method-research.md.

GROUPING -- an "experiment" is a set of >=2 posts that vary ONE thing. Sources are
tried in priority order (most explicit first); the FIRST that yields groups wins,
so an intentional tag always beats a heuristic guess:

  1. Caption A/B tag   -- "#abx_<exp>" (or "#abx_<exp>_<variant>") in the caption.
                          The clean, intentional path: Elijah tags a grid himself.
  2. Sidecar file      -- ig-dashboard/experiments.json mapping an experiment id
                          to a list of post ids/shortcodes/permalinks. A durable,
                          hand- or skill-written record of "these N were one grid".
  3. Near-identical    -- posts whose base caption (lowercased, hashtags/urls/
     base caption        whitespace/emoji stripped) shares a long common prefix:
                          "same hook on different visuals" leaves a near-dup caption.
  4. Variant hashtag   -- posts sharing an unusual, low-frequency hashtag that
                          looks like an experiment marker (used by 2..6 posts).
  5. same-category +   -- the graceful fallback when NO explicit A/B exists: posts
     same-week           in the same content category posted in the same ISO week.
                          NOT a clean A/B (many things vary) -> always flagged and
                          its winners are held to a stricter margin.

HONESTY GATE (winner() refuses to declare unless ALL hold):
  - every compared variant clears MIN_REACH (trial/non-follower reach is small);
  - the experiment has >= MIN_VARIANTS variants with usable reach;
  - the top variant beats the runner-up's 2026 score by >= MIN_MARGIN
    (a stricter MIN_MARGIN_FALLBACK for the noisy same-category/week grouping).
Otherwise: "inconclusive -- keep running / collect more reach".

ADDITIVE + READ-ONLY: imports metrics2026 unchanged, reads store.json read-only,
and writes ONLY a report file (data/trial_ab-report.md by default, or --out).
Pure stdlib (json, re, statistics, datetime). Same engine shape as the hub's
other scripts: cp1252-safe log(), a --self-test, and a citation-friendly report.

Usage:
  python trial_ab.py                 # group + score + winner over store.json, write report
  python trial_ab.py --n 8           # cap variants shown per experiment
  python trial_ab.py --out foo.md    # custom report path
  python trial_ab.py --no-report     # console only, write nothing
  python trial_ab.py --self-test     # inline sanity checks, no I/O on the store
"""

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, date
from pathlib import Path

BASE = Path(__file__).resolve().parent
STORE = BASE / "data" / "store.json"
SIDECAR = BASE / "experiments.json"
DEFAULT_REPORT = BASE / "data" / "trial_ab-report.md"

# Import the 2026 contract UNCHANGED. metrics2026.py sits beside this file, so
# ensure its directory is importable regardless of the invoking cwd.
sys.path.insert(0, str(BASE))
import metrics2026 as m  # noqa: E402  (intentional: path set above)

# --------------------------------------------------------------------------- #
# Honesty-gate thresholds (tunable in ONE place; deliberately conservative).
# Trial / non-follower reach is structurally small + slow, so these are LOW
# floors -- but the margin check is what actually prevents crowning noise.
# --------------------------------------------------------------------------- #
MIN_REACH = 500          # a variant below this is "thin" -> not eligible to win
MIN_VARIANTS = 2         # need at least a head-to-head
MIN_MARGIN = 0.05        # top must beat #2's score by this (absolute, on a 0..1 scale)
MIN_MARGIN_FALLBACK = 0.10  # stricter margin for the noisy same-category/week grouping

# Grouping heuristic knobs.
ABX_TAG = re.compile(r"#abx[_-]([a-z0-9]+)", re.I)   # "#abx_hookA" -> exp id "hooka"
CAPTION_PREFIX_LEN = 45      # chars of normalized caption prefix that must match
CAPTION_MIN_PREFIX = 20      # ignore captions too short to be a meaningful match
HASHTAG_MIN_GROUP = 2        # a "variant hashtag" must tie together >=2 posts
HASHTAG_MAX_GROUP = 6        # ...and <=6 (a common hashtag isn't an experiment marker)


def log(msg):
    """cp1252-safe console line, mirroring the other engines' log() helper."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("cp1252", "replace").decode("cp1252"))


# --------------------------------------------------------------------------- #
# Post helpers
# --------------------------------------------------------------------------- #

def post_id(post):
    """A stable display/key handle for a post (shortcode > id > permalink tail)."""
    return (post.get("shortcode") or post.get("id")
            or (post.get("permalink") or "").rstrip("/").rsplit("/", 1)[-1] or "?")


def reach_of(post):
    """Reach for the honesty gate (None-safe; 0/None both fail the floor)."""
    ins = post.get("insights") or {}
    r = ins.get("reach")
    return r if isinstance(r, (int, float)) else None


def _norm_caption(caption):
    """Lowercase, strip hashtags/mentions/urls/emoji-ish/punct/whitespace.

    What's left is the 'base caption' -- the spoken hook text. Two reels that
    reuse the same proven hook over different visuals land on the same base.
    """
    c = (caption or "").lower()
    c = re.sub(r"https?://\S+", " ", c)
    c = re.sub(r"[#@]\w+", " ", c)
    c = re.sub(r"[^a-z0-9 ]+", " ", c)     # drop emoji/punct (keep ascii words)
    c = re.sub(r"\s+", " ", c).strip()
    return c


def _hashtags(caption):
    """Lowercased hashtag set for one caption."""
    return {h.lower() for h in re.findall(r"#(\w+)", caption or "")}


def _iso_week(timestamp):
    """ISO 'YYYY-Www' bucket for a post timestamp, or None if unparseable."""
    if not timestamp:
        return None
    ts = timestamp.strip().replace("Z", "+0000")
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            d = datetime.strptime(ts, fmt)
            iso = d.isocalendar()
            return f"{iso[0]}-W{iso[1]:02d}"
        except ValueError:
            continue
    # last resort: leading date
    try:
        d = date.fromisoformat(timestamp[:10])
        iso = d.isocalendar()
        return f"{iso[0]}-W{iso[1]:02d}"
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Grouping heuristics (each returns {exp_id: {"held": str, "posts": [post,...],
# "method": str, "clean": bool}}; only groups with >=2 posts are kept)
# --------------------------------------------------------------------------- #

def group_by_tag(posts):
    g = defaultdict(list)
    for p in posts:
        mt = ABX_TAG.search(p.get("caption") or "")
        if mt:
            g[mt.group(1).lower()].append(p)
    return {f"tag:{k}": {"held": "tagged", "posts": v, "method": "caption #abx_ tag",
                         "clean": True}
            for k, v in g.items() if len(v) >= 2}


def group_by_sidecar(posts, sidecar_path=SIDECAR):
    """Read an optional experiments.json. Two accepted shapes:
        {"exp_id": ["shortcodeA", "shortcodeB", ...]}                 # simple
        {"exp_id": {"held": "overlay", "variants": ["scA", "scB"]}}   # rich
    Each id in the list is matched against a post's shortcode / id / permalink.
    """
    if not sidecar_path.exists():
        return {}
    try:
        with open(sidecar_path, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        log(f"WARN: could not read {sidecar_path.name}: {e}")
        return {}

    index = {}
    for p in posts:
        for key in (p.get("shortcode"), p.get("id"), p.get("permalink")):
            if key:
                index[str(key).rstrip("/")] = p

    out = {}
    for exp_id, body in (spec or {}).items():
        if isinstance(body, dict):
            held = body.get("held", "manual")
            refs = body.get("variants") or body.get("posts") or []
        else:
            held, refs = "manual", body
        hits = []
        for ref in refs:
            key = str(ref).rstrip("/")
            p = index.get(key) or index.get(key.rsplit("/", 1)[-1])
            if p:
                hits.append(p)
        if len(hits) >= 2:
            out[f"sidecar:{exp_id}"] = {"held": held, "posts": hits,
                                        "method": "experiments.json", "clean": True}
    return out


def group_by_caption(posts):
    """Posts whose normalized base-caption prefix matches -> same hook, varied visual."""
    buckets = defaultdict(list)
    for p in posts:
        base = _norm_caption(p.get("caption"))
        if len(base) >= CAPTION_MIN_PREFIX:
            buckets[base[:CAPTION_PREFIX_LEN]].append(p)
    return {f"cap:{k[:18]}": {"held": "overlay/hook (caption shared)", "posts": v,
                             "method": "near-identical base caption", "clean": True}
            for k, v in buckets.items() if len(v) >= 2}


def group_by_hashtag(posts):
    """Posts sharing an UNUSUAL low-frequency hashtag (a plausible variant marker).

    A hashtag used by exactly HASHTAG_MIN_GROUP..HASHTAG_MAX_GROUP posts is the
    signature of an experiment marker; a hashtag on dozens of posts is just a
    normal brand tag, not an A/B grouping.
    """
    tag_to_posts = defaultdict(list)
    for p in posts:
        for h in _hashtags(p.get("caption")):
            tag_to_posts[h].append(p)
    out = {}
    for h, plist in tag_to_posts.items():
        if HASHTAG_MIN_GROUP <= len(plist) <= HASHTAG_MAX_GROUP:
            out[f"tag#{h}"] = {"held": f"#{h} variant tag", "posts": plist,
                              "method": "shared variant hashtag", "clean": True}
    return out


def group_by_category_week(posts):
    """GRACEFUL FALLBACK: same content category + same ISO week. NOT a clean A/B
    (audio/length/time/caption all vary) -> marked clean=False so winners are
    held to the stricter margin and the report says so honestly."""
    buckets = defaultdict(list)
    for p in posts:
        cat = p.get("category") or "Uncategorized"
        wk = _iso_week(p.get("timestamp"))
        if wk:
            buckets[(cat, wk)].append(p)
    return {f"catwk:{cat}|{wk}": {"held": "category+week (NOT a clean A/B)",
                                  "posts": v, "method": "same category, same week",
                                  "clean": False}
            for (cat, wk), v in buckets.items() if len(v) >= 2}


def find_experiments(posts):
    """Try grouping heuristics in priority order; return the first that yields
    groups, plus the name of the method actually used (for the report header)."""
    ladder = [
        ("caption #abx_ tag", group_by_tag),
        ("experiments.json sidecar", group_by_sidecar),
        ("near-identical base caption", group_by_caption),
        ("shared variant hashtag", group_by_hashtag),
        ("same-category same-week (fallback demo)", group_by_category_week),
    ]
    for name, fn in ladder:
        groups = fn(posts)
        if groups:
            return groups, name
    return {}, "none"


# --------------------------------------------------------------------------- #
# Scoring + winner declaration (the honesty gate)
# --------------------------------------------------------------------------- #

def score_experiment(group, distributions):
    """Rank ONE experiment's variants via metrics2026.rank_posts() (UNCHANGED),
    annotating each with reach + an eligibility flag for the honesty gate."""
    posts = group["posts"]
    ranked = m.rank_posts(posts, distributions)   # <-- metric engine, verbatim
    variants = []
    for b in ranked:
        r = reach_of(b["post"])
        variants.append({
            "id": post_id(b["post"]),
            "label": _variant_label(b["post"]),
            "score": b["score"],
            "rates": b["rates"],
            "skip_grade": b["skip_grade"],
            "reach": r,
            "eligible": bool(r and r >= MIN_REACH),
        })
    return variants


def _variant_label(post):
    """Short human label for a variant in the report."""
    cap = (post.get("caption") or "").strip().replace("\n", " ")
    return (cap[:38] + "...") if len(cap) > 38 else (cap or post_id(post))


def winner(variants, clean=True):
    """Declare a winner OR refuse. Returns
    {"status": "winner"|"inconclusive", "reason": str, "winner": variant|None,
     "margin": float|None}.

    Refusal conditions (any one triggers 'inconclusive'):
      - fewer than MIN_VARIANTS variants clear MIN_REACH;
      - top eligible variant doesn't beat #2's score by the margin threshold
        (MIN_MARGIN for a clean A/B, MIN_MARGIN_FALLBACK for the noisy grouping).
    """
    eligible = [v for v in variants if v["eligible"]]
    margin_floor = MIN_MARGIN if clean else MIN_MARGIN_FALLBACK

    if len(eligible) < MIN_VARIANTS:
        thin = len(variants) - len(eligible)
        return {"status": "inconclusive", "winner": None, "margin": None,
                "reason": (f"only {len(eligible)} variant(s) clear the reach floor "
                           f"(>={MIN_REACH}); {thin} too thin -> keep running.")}

    eligible.sort(key=lambda v: v["score"], reverse=True)
    top, second = eligible[0], eligible[1]
    margin = top["score"] - second["score"]
    if margin < margin_floor:
        return {"status": "inconclusive", "winner": None, "margin": margin,
                "reason": (f"top beats #2 by only {margin:.3f} (< {margin_floor:.2f} "
                           f"{'clean' if clean else 'fallback'} margin) -> too close "
                           f"to call, keep running.")}
    return {"status": "winner", "winner": top, "margin": margin,
            "reason": (f"clears reach floor and beats #2 by {margin:.3f} "
                       f"(>= {margin_floor:.2f}).")}


def evaluate(posts, distributions=None):
    """Full pipeline over a post list: find experiments, score, declare winners.
    Returns (results, method_used). distributions over the FULL post set so each
    variant is percentile-ranked against Elijah's whole history (not just its
    tiny experiment), exactly as metrics2026 intends."""
    if distributions is None:
        distributions = m.build_distributions(posts)
    groups, method = find_experiments(posts)
    results = []
    for exp_id, group in sorted(groups.items()):
        variants = score_experiment(group, distributions)
        # display sorted by score desc
        variants.sort(key=lambda v: v["score"], reverse=True)
        verdict = winner(variants, clean=group["clean"])
        results.append({
            "exp_id": exp_id,
            "held": group["held"],
            "method": group["method"],
            "clean": group["clean"],
            "n": len(variants),
            "variants": variants,
            "verdict": verdict,
        })
    # most decisive (a real winner, then biggest margin) first
    results.sort(key=lambda r: (r["verdict"]["status"] == "winner",
                                r["verdict"].get("margin") or -1), reverse=True)
    return results, method


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def _fmt_pct(v):
    return f"{v * 100:5.2f}%" if v is not None else "  -- "


def render_report(results, method, n_posts, cap=6):
    lines = []
    lines.append("# Trial-reel A/B -- 2026-correct winners (MEASURE half)")
    lines.append("")
    lines.append(f"_Generated by `ig-dashboard/trial_ab.py` over {n_posts} posts. "
                 f"Scoring imports `metrics2026.rank_posts()` UNCHANGED "
                 "(skip-gate -> share>like>save>repost>comment, percentile-ranked "
                 "vs the full post history)._")
    lines.append("")
    lines.append(f"**Grouping method used:** {method}. Experiments are surfaced by "
                 "the first heuristic that finds any: caption `#abx_` tag -> "
                 "`experiments.json` -> near-identical caption -> variant hashtag -> "
                 "same-category/week fallback.")
    lines.append("")
    lines.append(f"**Honesty gate:** a winner is declared ONLY when >= {MIN_VARIANTS} "
                 f"variants clear reach >= {MIN_REACH} AND the top beats #2's 2026 "
                 f"score by >= {MIN_MARGIN:.2f} (>= {MIN_MARGIN_FALLBACK:.2f} for the "
                 "noisy category+week fallback). Otherwise: inconclusive.")
    lines.append("")

    if not results:
        lines.append("_No groups of >=2 variants found by any heuristic. Run a real "
                     "A/B grid (tag the variants `#abx_<name>` or list them in "
                     "`experiments.json`) and re-run._")
        return "\n".join(lines) + "\n"

    decided = [r for r in results if r["verdict"]["status"] == "winner"]
    lines.append(f"**{len(decided)} of {len(results)} experiments produced a "
                 "declared winner; the rest are honestly inconclusive.**")
    lines.append("")

    for r in results:
        v = r["verdict"]
        flag = "" if r["clean"] else "  _(NOT a clean A/B -- fallback grouping; "
        flag += "" if r["clean"] else "many variables move)_"
        lines.append(f"## {r['exp_id']}  ({r['method']}){flag}")
        lines.append(f"- held / swept: **{r['held']}**, {r['n']} variants")
        if v["status"] == "winner":
            w = v["winner"]
            lines.append(f"- **WINNER: {w['label']}** (`{w['id']}`) -- "
                         f"score {w['score']:.3f}, reach {w['reach']}. {v['reason']}")
        else:
            lines.append(f"- **INCONCLUSIVE** -- {v['reason']}")
        lines.append("")
        # variant table
        lines.append("| # | score | skip | share | like | save | reach | variant |")
        lines.append("|--:|------:|-----:|------:|-----:|-----:|------:|---------|")
        for i, var in enumerate(r["variants"][:cap], 1):
            rt = var["rates"]
            skip_cell = (_fmt_pct(rt["skip_rate"]) if rt["skip_rate"] is not None
                         else var["skip_grade"])
            elig = "" if var["eligible"] else " *(thin)*"
            label = var["label"].replace("|", "/")
            lines.append(f"| {i} | {var['score']:.3f} | {skip_cell} | "
                         f"{_fmt_pct(rt['share_rate'])} | {_fmt_pct(rt['like_rate'])} | "
                         f"{_fmt_pct(rt['save_rate'])} | "
                         f"{var['reach'] if var['reach'] is not None else '--'}{elig} | "
                         f"{label} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def print_console(results, method, n_posts):
    log(f"trial_ab -- {n_posts} posts | grouping method: {method}")
    if not results:
        log("no >=2-variant groups found by any heuristic; "
            "tag a grid #abx_<name> or list it in experiments.json.")
        return
    decided = sum(1 for r in results if r["verdict"]["status"] == "winner")
    log(f"{len(results)} experiment(s); {decided} with a declared winner "
        f"(rest inconclusive by the honesty gate).")
    log("")
    for r in results:
        v = r["verdict"]
        tag = "" if r["clean"] else " [fallback: NOT clean A/B]"
        log(f"* {r['exp_id']} ({r['method']}, n={r['n']}){tag}")
        if v["status"] == "winner":
            w = v["winner"]
            log(f"    WINNER -> {w['label']} | score {w['score']:.3f} "
                f"reach {w['reach']} | {v['reason']}")
        else:
            log(f"    inconclusive -> {v['reason']}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def load_posts():
    """Read store.json (read-only) -> list of post dicts (same as metrics2026)."""
    with open(STORE, encoding="utf-8") as f:
        store = json.load(f)
    return list(store.get("posts", {}).values())


def _self_test():
    """Inline sanity checks (no test framework, matches hub style). Builds tiny
    synthetic experiments and asserts grouping + the honesty gate behave."""
    # --- grouping: caption tag beats everything ---
    tagged = [
        {"id": "a1", "caption": "best hook ever #abx_hookA", "category": "X",
         "timestamp": "2026-06-01T10:00:00+0000",
         "insights": {"reach": 1000, "shares": 50, "saved": 30}, "like_count": 200,
         "comments_count": 5},
        {"id": "a2", "caption": "best hook ever #abx_hookA", "category": "X",
         "timestamp": "2026-06-02T10:00:00+0000",
         "insights": {"reach": 1000, "shares": 5, "saved": 3}, "like_count": 20,
         "comments_count": 1},
    ]
    groups, method = find_experiments(tagged)
    assert method == "caption #abx_ tag", f"tag should win grouping, got {method}"
    assert "tag:hooka" in groups, groups.keys()

    # --- scoring + a CLEAR winner (variant 1 dominates, both clear reach floor) ---
    dist = m.build_distributions(tagged)
    res, _ = evaluate(tagged, dist)
    assert len(res) == 1
    v = res[0]["verdict"]
    assert v["status"] == "winner", f"expected a winner, got {v}"
    assert v["winner"]["id"] == "a1", v["winner"]

    # --- honesty gate: thin reach -> inconclusive ---
    thin = [
        {"id": "t1", "caption": "x #abx_thin", "insights": {"reach": 100, "shares": 5}},
        {"id": "t2", "caption": "x #abx_thin", "insights": {"reach": 120, "shares": 1}},
    ]
    vr = winner(score_experiment(
        {"posts": thin, "held": "h", "clean": True}, m.build_distributions(thin)),
        clean=True)
    assert vr["status"] == "inconclusive" and "reach floor" in vr["reason"], vr

    # --- honesty gate: thin MARGIN -> inconclusive (both pass reach, scores tie) ---
    tie = [
        {"id": "m1", "caption": "y #abx_tie",
         "insights": {"reach": 1000, "shares": 10, "saved": 5}, "like_count": 50,
         "comments_count": 2},
        {"id": "m2", "caption": "y #abx_tie",
         "insights": {"reach": 1000, "shares": 10, "saved": 5}, "like_count": 50,
         "comments_count": 2},
    ]
    vr2 = winner(score_experiment(
        {"posts": tie, "held": "h", "clean": True}, m.build_distributions(tie)),
        clean=True)
    assert vr2["status"] == "inconclusive" and "too close" in vr2["reason"], vr2

    # --- fallback grouping marks clean=False ---
    catwk = [
        {"id": "c1", "caption": "alpha", "category": "Money",
         "timestamp": "2026-06-01T10:00:00+0000", "insights": {"reach": 900}},
        {"id": "c2", "caption": "beta", "category": "Money",
         "timestamp": "2026-06-02T10:00:00+0000", "insights": {"reach": 900}},
    ]
    cg = group_by_category_week(catwk)
    assert cg and all(g["clean"] is False for g in cg.values()), cg

    # --- helpers ---
    assert _iso_week("2026-06-01T10:00:00+0000") == "2026-W23", _iso_week("2026-06-01T10:00:00+0000")
    assert _norm_caption("Best HOOK!! #ad http://x.co 🔥") == "best hook", \
        repr(_norm_caption("Best HOOK!! #ad http://x.co 🔥"))
    assert _hashtags("a #One #two") == {"one", "two"}

    log("self-test OK")


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        _self_test()
        return

    cap = 6
    if "--n" in argv:
        try:
            cap = int(argv[argv.index("--n") + 1])
        except (IndexError, ValueError):
            log("WARN: --n needs an integer; defaulting to 6")

    if not STORE.exists():
        log(f"FATAL: store.json not found at {STORE}")
        sys.exit(1)

    posts = load_posts()
    results, method = evaluate(posts)
    print_console(results, method, len(posts))

    if "--no-report" in argv:
        return
    out = DEFAULT_REPORT
    if "--out" in argv:
        try:
            out = Path(argv[argv.index("--out") + 1])
        except IndexError:
            log("WARN: --out needs a path; using default")
    report = render_report(results, method, len(posts), cap=cap)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(report)
    log("")
    log(f"report written -> {out}")


if __name__ == "__main__":
    main()
