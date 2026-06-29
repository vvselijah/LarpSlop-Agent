"""
Viral teardown — Claude-as-analyst "why it works" breakdown of viral-radar's winners.

Consumes the output of viral-radar.py (DOES NOT edit or re-run it) and turns the
ranked top-post leaderboard into a structured teardown card per post: hook type,
format, retention lever, and a replicable angle Elijah can actually shoot. Where
viral-radar answers "WHAT is winning", this answers "WHY it works + how to steal it".

DATA SOURCE (read-only, in priority order):
  1. intel/viral-report.md  — the rich per-post leaderboard viral-radar writes
     (views, eng-rate, median-ratio, account, date, media_type, caption, permalink).
     This is a primary source: viral.json only stores per-ACCOUNT median history,
     not per-POST detail, so the markdown report is where the per-post signal lives.
  1b. intel/niche-report.md — the DISCOVERY leaderboard niche-radar writes (scraped
     hashtag winners, same line format). Read alongside viral-report.md when present;
     posts are merged and de-duped by permalink, so the teardown covers both the
     tracked-account winners AND the freshly-discovered ones.
  2. intel/data/viral.json  — optional cross-reference for an account's follower
     count + median views (adds "punching above weight" context to each card).

It performs a deterministic, keyless FIRST-PASS classification from the caption text
+ media_type + the views/eng/ratio signals (a transparent rubric, see HOOK_RULES /
RETENTION_RULES below). That first pass is meant to be REVIEWED and sharpened by
Claude-as-analyst — every card carries the raw evidence so the call is auditable.

READ-ONLY & SAFE: no API calls, no network, no secrets, stdlib only. It reads the two
files above and writes exactly ONE new file (intel/viral-teardown.md). It never writes
viral.json, viral-report.md, or any other engine's data.

Usage:
  python viral_teardown.py            # parse viral-report.md + niche-report.md -> teardown
  python viral_teardown.py --top 6    # cap the number of posts torn down (default 8)
  python viral_teardown.py --stdout    # also echo the teardown to stdout
  python viral_teardown.py --self-test # run built-in tests, write nothing, exit
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPORT = BASE / "viral-report.md"
NICHE_REPORT = BASE / "niche-report.md"
STORE = BASE / "data" / "viral.json"
OUT = BASE / "viral-teardown.md"

DEFAULT_TOP = 8

# A post line from viral-report.md, e.g.:
#   - [new-parent] **1,466,282 views** (eng 6.2%, 62.6x @babylist's median) | @babylist | 2026-05-21 | REELS | caption text | https://...
# The optional "[niche] " prefix only appears in the cross-niche board; the
# per-niche boards omit it. Both are handled.
POST_RE = re.compile(
    r"^- (?:\[(?P<niche>[^\]]+)\] )?"
    r"\*\*(?P<views>[\d,]+) views\*\* "
    r"\(eng (?P<eng>[\d.]+)%, (?P<ratio>[\d.]+)[x×] @(?P<user2>[^']+)'s median\) \| "
    r"@(?P<user>[^|]+?) \| "
    r"(?P<date>[\d-]+) \| "
    r"(?P<mtype>[^|]+?) \| "
    r"(?P<caption>.*?) \| "
    r"(?P<url>\S+)\s*$"
)


def log(msg):
    """cp1252-safe stdout (OneDrive console is cp1252; emojis in captions blow up print)."""
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    enc = sys.stdout.encoding or "utf-8"
    sys.stdout.write(line.encode(enc, "replace").decode(enc, "replace") + "\n")


# ---- classification rubric (transparent, keyless first pass) ----

# Hook type: matched against the lowered caption, first rule that hits wins.
# Order matters — more specific patterns first.
HOOK_RULES = [
    ("Curiosity gap / reveal",
     r"\b(you won'?t believe|nobody tells you|secret|truth about|here'?s why|"
     r"the real reason|what (?:no one|nobody)|reacts to|sold everything)\b"),
    ("Listicle / number promise",
     r"\b(\d+\s+(?:ways|things|tips|signs|reasons|steps|habits|mistakes|rules)|"
     r"average\s+\w+\s+by age|net worth by age)\b"),
    ("Question hook",
     r"^\W*(?:are you|do you|did you|what if|why do|how to|which|who did you|ever\b)"),
    ("Contrarian / myth-bust",
     r"\b(stop|don'?t|never|myth|wrong|nobody|isn'?t|won'?t|doesn'?t|"
     r"unpopular|actually)\b"),
    ("Comment-bait / CTA gate",
     r"\b(comment|drop a|type \w+|dm me|link in bio|tag (?:a|someone)|"
     r"save this|share this)\b"),
    ("Emotional / relatable resonance",
     r"\b(grief|healing|loss|love|struggling|peace|fear|alone|"
     r"you'?re changing the world|nothing|memories|am i doing this right)\b"),
    ("Authority / proof-of-results",
     r"\b(millionaire|i made|i built|\$\d|how i|after \d+ years|net worth|"
     r"this played out)\b"),
]

# Retention lever: why people keep watching to the end.
RETENTION_RULES = [
    ("Open loop the caption sets up (payoff withheld)",
     r"\b(here'?s why|the real reason|what (?:no one|nobody)|you won'?t believe|"
     r"secret|wait for it|until the end)\b"),
    ("Step-by-step / how-to payoff (watch to learn the move)",
     r"\b(how to|step|way to|the way you|make a (?:big )?difference|tips?|"
     r"ideas? for|fill\w* your)\b"),
    ("Numbered list keeps a running tally (count-down tension)",
     r"\b\d+\s+(?:ways|things|tips|signs|reasons|steps|habits|mistakes|rules)\b"),
    ("Emotional build / catharsis (stay for the feeling)",
     r"\b(grief|healing|loss|love|fight for|believe you can|changing the world)\b"),
    ("Reaction / stakes escalate (watch the number/outcome land)",
     r"\b(reacts to|bank account|net worth|taxes|sold everything|played out)\b"),
]

# Format inferred from media_type + caption shape.
def classify_format(mtype, caption):
    m = (mtype or "").strip().upper()
    c = caption.lower()
    base = "Reel (short-form video)" if "REEL" in m else (
        "Carousel / image post" if m in ("CAROUSEL_ALBUM", "IMAGE") else (m.title() or "Unknown"))
    tags = []
    if re.search(r"\b(reacts to|reaction)\b", c):
        tags.append("reaction-format")
    if re.search(r"\b\d+\s+(?:ways|things|tips|signs|reasons|steps)\b", c):
        tags.append("list-format")
    if re.search(r"\b(how to|step|tutorial|the way you)\b", c):
        tags.append("how-to / educational")
    if re.search(r"\b(quote|grief|healing|peace)\b", c):
        tags.append("quote / text-over-emotion")
    if re.search(r"\b(comment|link in bio|dm|tag)\b", c):
        tags.append("CTA-gated")
    return base + (f" ({', '.join(tags)})" if tags else "")


def first_match(rules, text, default):
    low = text.lower()
    for label, pat in rules:
        if re.search(pat, low):
            return label
    return default


def replicable_angle(post):
    """A concrete 'how Elijah steals this' line — niche-translated to his AI/founder lane."""
    niche = post["niche"] or "this niche"
    hook = post["hook"]
    # Translate the borrowed structure into Elijah's lane without copying the topic.
    return (f"Borrow the *{hook.lower()}* structure, not the topic: re-skin it for AI / "
            f"solo-founder content (keep the same hook shape that worked in {niche}). "
            f"Reference: {post['url']}")


# ---- parsing ----

def parse_report(text):
    """Pull the ranked posts out of viral-report.md, de-duped by permalink, views-desc."""
    posts = []
    seen = set()
    for line in text.splitlines():
        mo = POST_RE.match(line)
        if not mo:
            continue
        d = mo.groupdict()
        url = d["url"].strip()
        if url in seen:
            continue
        seen.add(url)
        try:
            views = int(d["views"].replace(",", ""))
        except ValueError:
            continue
        posts.append({
            "niche": (d["niche"] or "").strip(),
            "views": views,
            "eng": float(d["eng"]),
            "ratio": float(d["ratio"]),
            "user": d["user"].strip(),
            "date": d["date"].strip(),
            "mtype": d["mtype"].strip(),
            "caption": d["caption"].strip(),
            "url": url,
        })
    posts.sort(key=lambda p: p["views"], reverse=True)
    return posts


def enrich(post, store):
    """Attach hook/retention/format/angle + optional account context from viral.json."""
    cap = post["caption"]
    post["hook"] = first_match(HOOK_RULES, cap, "Direct statement / pattern interrupt")
    post["retention"] = first_match(
        RETENTION_RULES, cap, "Tight pacing + payoff density (no single dominant lever)")
    post["format"] = classify_format(post["mtype"], cap)
    post["angle"] = replicable_angle(post)
    # cross-ref account context (followers / median) if present
    acct = (store.get("accounts", {}) or {}).get(post["user"])
    if acct and acct.get("history"):
        latest = sorted(acct["history"].items())[-1][1]
        post["followers"] = latest.get("followers")
        post["acct_median"] = latest.get("median_views")
    return post


# ---- rendering ----

def render(posts, generated):
    out = [
        "# Viral teardown — Claude-as-analyst 'why it works' board",
        f"_Generated {generated} from `intel/viral-report.md` + `intel/niche-report.md` "
        "(read-only). viral-radar/niche-radar found WHAT wins; this is WHY + how to steal it._",
        "",
        "Each card is a transparent FIRST PASS: the hook/retention/format calls come from "
        "a keyless caption-text rubric and should be **reviewed and sharpened by Claude** "
        "against the actual video at the permalink. The raw evidence (views, eng-rate, "
        "median-ratio) is shown so every call is auditable.",
        "",
        "**How to read the signals:** high `median-ratio` = this post beat the account's "
        "own baseline (a true breakout, not just a big account); high `eng%` with lower "
        "views = it over-indexed on saves/comments (a different, save-driven win).",
        "",
        "---",
        "",
    ]
    for i, p in enumerate(posts, 1):
        ctx = ""
        if p.get("followers"):
            ctx = (f" — account: {p['followers']:,} followers, "
                   f"median {int(p.get('acct_median') or 0):,} views")
        out += [
            f"## {i}. @{p['user']} — {p['views']:,} views  ·  {p['niche'] or 'n/a'}",
            f"- **Evidence:** {p['eng']:.1f}% eng · {p['ratio']:.1f}x the account's median "
            f"· {p['date']} · {p['mtype']}{ctx}",
            f"- **Caption (truncated by radar):** {p['caption'] or '(none captured)'}",
            f"- **Hook type:** {p['hook']}",
            f"- **Format:** {p['format']}",
            f"- **Retention lever:** {p['retention']}",
            f"- **Replicable angle (for Elijah):** {p['angle']}",
            f"- **Watch it:** {p['url']}",
            "",
            "> _Analyst note:_ confirm the on-screen hook and the first-3s visual at the "
            "link — the caption is only a proxy; the actual cold-open may differ.",
            "",
            "---",
            "",
        ]
    out += [
        "## Cross-cutting patterns to test next",
        "_(Claude fills this in after reviewing the cards above: which hook type / format "
        "repeats across the winners, and the single highest-leverage thing for Elijah to "
        "shoot this week.)_",
        "",
        "_Read-only teardown — no API calls, no posting. Source of truth is "
        "`viral-report.md`; re-run viral-radar.py to refresh the underlying winners._",
        "",
    ]
    return "\n".join(out)


# ---- self-test ----

def _self_test():
    # NOTE: uses the real Unicode "×" (U+00D7) the live report emits, plus an emoji
    # header — both must survive parsing/logging. ASCII "x" is also accepted.
    sample = (
        "# Viral radar — 2026-06-14\n"
        "## \U0001f3c6 Biggest hits across all niches (by views)\n"
        "- [new-parent] **1,466,282 views** (eng 6.2%, 62.6× @babylist's median) | @babylist | 2026-05-21 | REELS | Baby's first bath is a big deal, am I doing this right? Especially the um | https://www.instagram.com/reel/DYnXT-dAa86/\n"
        "- [money-finance] **818,144 views** (eng 2.0%, 4.4× @gpstephan's median) | @gpstephan | 2026-05-18 | REELS | Millionaire Reacts To Togi's Bank Account | https://www.instagram.com/reel/DYfGhArgHDm/\n"
        "- [money-finance] **775,448 views** (eng 2.2%, 4.1x @gpstephan's median) | @gpstephan | 2026-05-16 | REELS | Average net worth by age! | https://www.instagram.com/reel/DYZ80EfAT3U/\n"
        "## money-finance\n"
        "- **818,144 views** (eng 2.0%, 4.4× @gpstephan's median) | @gpstephan | 2026-05-18 | REELS | Millionaire Reacts To Togi's Bank Account | https://www.instagram.com/reel/DYfGhArgHDm/\n"
    )
    posts = parse_report(sample)
    # 3 unique permalinks despite 4 matching lines (one dup across boards)
    assert len(posts) == 3, f"expected 3 de-duped posts, got {len(posts)}"
    assert posts[0]["views"] == 1466282, posts[0]["views"]
    assert posts[0]["user"] == "babylist", posts[0]["user"]
    assert posts[0]["niche"] == "new-parent", posts[0]["niche"]
    # views-desc ordering
    assert [p["views"] for p in posts] == sorted((p["views"] for p in posts), reverse=True)

    store = {"accounts": {"gpstephan": {"history": {"2026-06-14": {"followers": 489715, "median_views": 186879}}}}}
    e = [enrich(p, store) for p in posts]
    # listicle caption -> listicle hook
    nw = next(p for p in e if "net worth" in p["caption"].lower())
    assert "Listicle" in nw["hook"], nw["hook"]
    # reaction caption -> reaction format tag + reaction retention
    rx = next(p for p in e if "reacts to" in p["caption"].lower())
    assert "reaction" in rx["format"].lower(), rx["format"]
    # account cross-ref attached for gpstephan
    assert rx.get("followers") == 489715, rx.get("followers")
    # emotional/relatable caption
    bath = next(p for p in e if "babylist" == p["user"])
    assert bath["hook"], "hook must be non-empty"
    # render must produce a non-trivial markdown doc with all cards
    md = render(e, "2026-06-15T00:00:00Z")
    assert md.count("## ") >= 4, "expected >=3 post cards + patterns section"
    assert "Replicable angle" in md
    assert "https://www.instagram.com/reel/DYfGhArgHDm/" in md
    # emoji in caption must not crash cp1252 log()
    log("self-test caption with emoji: \U0001f4b0 ok")
    print("SELF-TEST PASS: parsed 3/4 lines (1 dup), classified hook/format/retention, "
          "cross-ref + render OK")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description="Claude-as-analyst teardown of viral-radar winners.")
    ap.add_argument("--top", type=int, default=DEFAULT_TOP, help="max posts to tear down")
    ap.add_argument("--stdout", action="store_true", help="echo the teardown to stdout too")
    ap.add_argument("--self-test", action="store_true", help="run built-in tests, write nothing")
    args = ap.parse_args(argv)

    if args.self_test:
        return 0 if _self_test() else 1

    sources = [p for p in (REPORT, NICHE_REPORT) if p.exists()]
    if not sources:
        log(f"FATAL: neither {REPORT.name} nor {NICHE_REPORT.name} found — "
            "run viral-radar.py and/or niche-radar.py first to produce a leaderboard.")
        return 2

    # Merge both leaderboards; parse_report de-dupes by permalink across the
    # combined text, so a post that appears in both reports is torn down once.
    text = "\n".join(p.read_text(encoding="utf-8") for p in sources)
    posts = parse_report(text)
    if not posts:
        log(f"No parseable post lines in {', '.join(p.name for p in sources)} "
            "(was the last pull empty / over the floor?).")
        return 3
    log(f"parsed {len(posts)} unique post(s) from: {', '.join(p.name for p in sources)}")

    store = {}
    if STORE.exists():
        try:
            store = json.loads(STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            store = {}

    posts = posts[: max(1, args.top)]
    posts = [enrich(p, store) for p in posts]

    generated = datetime.now(timezone.utc).isoformat()[:19] + "Z"
    md = render(posts, generated)
    OUT.write_text(md, encoding="utf-8")
    log(f"teardown written: {OUT}  ({len(posts)} post(s) torn down)")
    if args.stdout:
        sys.stdout.write("\n" + md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
