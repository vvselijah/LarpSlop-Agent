"""
metrics2026.py -- the canonical 2026 IG-algorithm scoring contract for @elijahaifl.

Turns the raw per-post fields the dashboard ALREADY stores (in
ig-dashboard/data/store.json) into the six 2026 priority RATES and one
composite score, and ranks posts by that score with skip-rate as a hard gate.

The 2026 priority order (Enrico Incarnati teardown + corroborating sources;
see docs/plans/2026-06-14-ig-2026-algorithm-metric-engine-research.md):

  1. skip_rate    -- % who skip in the first ~3s (hook failure). LOWER is better.
                     Used as a GATE, not a weight. >50% => IG throttles distro.
  2. share_rate   -- sends / reach   (strongest social proof)
  3. like_rate    -- likes / reach
  4. save_rate    -- saved / reach   (now SECONDARY, no longer #1)
  5. repost_rate  -- reposts / reach (low-conviction passive signal)
  6. comment_rate -- comments / reach (LOWEST priority; warns vs keyword-bait)

Share/like/save/repost/comment have no published absolute benchmark, so they're
graded RELATIVE to Elijah's own 300-post distribution (percentile rank), not an
absolute target. Skip rate has a published benchmark (<=40% healthy, >50%
throttled) so it's used as an absolute gate.

ADDITIVE + READ-ONLY: this module only reads store.json and computes arithmetic.
It does NOT modify refresh.py or any other engine. Pure stdlib (json, statistics).

FIELD REALITY (verified against the live store.json on 2026-06-14):
  - insights dict holds: views, reach, saved, shares, total_interactions,
    ig_reels_avg_watch_time, ig_reels_video_view_total_time
  - likes  = post-level "like_count"     (NOT inside insights)
  - comments = post-level "comments_count" (NOT inside insights)
  - reels_skip_rate / reposts are now ingested by refresh.py (2026-06-14).
    reels_skip_rate is stored as a 0..1 FRACTION (refresh.py normalizes it from
    the API's 0-100 percent at ingestion, so the thresholds below apply as-is);
    reposts is a raw count. Both land in insights[...] for reels refreshed since
    the change -- recent posts (<=14d) on any run, all 300 after `--full`. Any
    post still missing skip_rate keeps the gate NEUTRAL (not a win, not a penalty).
  - all 300 tracked posts are currently REELS.

Usage:
  python metrics2026.py            # top 15 posts by the 2026 score
  python metrics2026.py --n 25     # top 25
"""

import json
import statistics
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
STORE = BASE / "data" / "store.json"

# Priority weights from the 2026 model. Skip-rate is a GATE, not a weight, so
# it is deliberately absent here. Tunable in ONE place (the plan flags these as
# an ordinal model, not Meta-published gospel).
WEIGHTS = {"share": 0.40, "like": 0.25, "save": 0.20, "repost": 0.10, "comment": 0.05}

# Skip-rate benchmarks (inro.social, early 2026): <=40% healthy; >50% throttled.
SKIP_HEALTHY = 0.40   # <= this is good
SKIP_THROTTLE = 0.50  # > this and IG suppresses distribution

# The six rates, in priority order, for stable display.
RATE_KEYS = ["skip_rate", "share_rate", "like_rate", "save_rate", "repost_rate", "comment_rate"]


def log(msg):
    """cp1252-safe console line, mirroring the other engines' log() helper."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("cp1252", "replace").decode("cp1252"))


# --------------------------------------------------------------------------- #
# Per-post rate computation (pure, None-safe, zero-denominator-safe)
# --------------------------------------------------------------------------- #

def _num(post, *path):
    """Pull a numeric field from a post, trying each (location, key) in `path`.

    A path entry is either a bare key (looked up at post top-level) or a
    "insights:key" string (looked up inside post['insights']). First non-None
    numeric wins. Returns None if nothing usable is found.
    """
    ins = post.get("insights") or {}
    for entry in path:
        if entry.startswith("insights:"):
            v = ins.get(entry.split(":", 1)[1])
        else:
            v = post.get(entry)
        if isinstance(v, (int, float)):
            return v
    return None


def rates(post):
    """Raw IG fields -> the six per-reach rates for one post (all None-safe).

    Reads BOTH the insights sub-dict (shares, saved) AND the post top-level
    (like_count, comments_count) because that is how refresh.py actually stores
    them. skip_rate / reposts are read if present but are absent in the current
    store, so they come back None and are handled gracefully downstream.
    """
    reach = _num(post, "insights:reach")

    def per_reach(*path):
        v = _num(post, *path)
        if v is None or not reach:
            return None
        return v / reach

    # skip_rate is already a rate from the API (0..1). Accept either an
    # insights field or a post top-level field, whichever lands there.
    skip = _num(post, "insights:reels_skip_rate", "reels_skip_rate")

    return {
        "skip_rate":    skip,
        "share_rate":   per_reach("insights:shares"),
        "like_rate":    per_reach("like_count", "insights:likes"),
        "save_rate":    per_reach("insights:saved"),
        "repost_rate":  per_reach("insights:reposts", "reposts"),
        "comment_rate": per_reach("comments_count", "insights:comments"),
    }


def grade_skip(skip_rate):
    """Skip-rate band: 'healthy' | 'watch' | 'throttled' | 'n/a' (missing)."""
    if skip_rate is None:
        return "n/a"
    if skip_rate <= SKIP_HEALTHY:
        return "healthy"
    if skip_rate <= SKIP_THROTTLE:
        return "watch"
    return "throttled"


def skip_gate(skip_rate):
    """Multiplier applied to the weighted base score.

    Missing skip rate => NEUTRAL (1.0), per the plan's Risks section: a missing
    skip is NOT a win and NOT a penalty. Healthy => full credit; watch-zone =>
    half; throttled (>50%) => hard 0.2 penalty.
    """
    if skip_rate is None or skip_rate <= SKIP_HEALTHY:
        return 1.0
    if skip_rate <= SKIP_THROTTLE:
        return 0.5
    return 0.2


# --------------------------------------------------------------------------- #
# Distribution / percentile ranking (relative grading over Elijah's own posts)
# --------------------------------------------------------------------------- #

def build_distributions(posts):
    """For each weighted rate, collect the sorted list of non-None values across
    all posts. Used to percentile-rank an individual post relative to history."""
    dist = {}
    for k in WEIGHTS:
        vals = []
        for p in posts:
            v = rates(p)[f"{k}_rate"]
            if v is not None:
                vals.append(v)
        dist[k] = sorted(vals)
    return dist


def pct_rank(value, sorted_vals):
    """Percentile rank (0..1) of `value` within an already-sorted list.

    Fraction of the distribution at or below `value`. Returns 0.0 for a missing
    value or an empty distribution so a missing rate contributes nothing (rather
    than crashing or being treated as median).
    """
    if value is None or not sorted_vals:
        return 0.0
    # count of values <= value, via linear scan (lists are <=300 long).
    below = sum(1 for v in sorted_vals if v <= value)
    return below / len(sorted_vals)


def score_2026(post, distributions):
    """Composite 2026 score for one post in [0, 1].

    weighted sum of each rate's percentile rank (relative to Elijah's own
    distribution), multiplied by the skip-rate gate. Higher = better aligned to
    the 2026 priority (shares > likes > saves > reposts > comments, gated on a
    passing hook / skip rate).
    """
    rt = rates(post)
    base = sum(WEIGHTS[k] * pct_rank(rt[f"{k}_rate"], distributions.get(k, []))
               for k in WEIGHTS)
    return skip_gate(rt["skip_rate"]) * base


def rank_posts(posts, distributions=None):
    """Return posts sorted by score_2026 descending, each as a dict bundle:
    {post, score, rates, skip_grade}. distributions computed if not supplied."""
    if distributions is None:
        distributions = build_distributions(posts)
    bundles = []
    for p in posts:
        rt = rates(p)
        bundles.append({
            "post": p,
            "score": score_2026(p, distributions),
            "rates": rt,
            "skip_grade": grade_skip(rt["skip_rate"]),
        })
    bundles.sort(key=lambda b: b["score"], reverse=True)
    return bundles


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def load_posts():
    """Read store.json (read-only) and return the list of post dicts."""
    with open(STORE, encoding="utf-8") as f:
        store = json.load(f)
    return list(store.get("posts", {}).values())


def _fmt_pct(v):
    return f"{v * 100:5.2f}%" if v is not None else "   -- "


def _self_test():
    """Tiny inline sanity check (no test framework, matches hub style)."""
    fake = [
        {"insights": {"reach": 1000, "shares": 50, "saved": 30},
         "like_count": 200, "comments_count": 10},                       # strong
        {"insights": {"reach": 1000, "shares": 1, "saved": 2, "reels_skip_rate": 0.62},
         "like_count": 20, "comments_count": 1},                          # throttled hook
        {"insights": {"reach": 0, "shares": 0, "saved": 0},
         "like_count": 0, "comments_count": 0},                           # zero reach -> all None
    ]
    dist = build_distributions(fake)
    ranked = rank_posts(fake, dist)
    assert ranked[0]["post"] is fake[0], "strong post should rank first"
    assert grade_skip(0.62) == "throttled" and grade_skip(0.30) == "healthy"
    assert grade_skip(None) == "n/a"
    assert skip_gate(0.62) == 0.2 and skip_gate(None) == 1.0
    assert rates(fake[2])["share_rate"] is None, "zero reach must yield None, not div-by-zero"
    assert pct_rank(None, [0.1, 0.2]) == 0.0
    log("self-test OK")


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        _self_test()
        return

    n = 15
    if "--n" in argv:
        try:
            n = int(argv[argv.index("--n") + 1])
        except (IndexError, ValueError):
            log("WARN: --n needs an integer; defaulting to 15")

    if not STORE.exists():
        log(f"FATAL: store.json not found at {STORE}")
        sys.exit(1)

    posts = load_posts()
    dist = build_distributions(posts)
    ranked = rank_posts(posts, dist)

    have_skip = sum(1 for b in ranked if b["rates"]["skip_rate"] is not None)
    log(f"2026 scoring -- {len(posts)} posts | skip_rate present on {have_skip} "
        f"(skip gate = NEUTRAL where absent)")
    log("weights: " + ", ".join(f"{k} {int(v*100)}%" for k, v in WEIGHTS.items())
        + f" | skip gate: <={int(SKIP_HEALTHY*100)}% healthy, >{int(SKIP_THROTTLE*100)}% throttled")
    log("")
    header = (f"{'#':>3}  {'score':>6}  {'skip':>9}  {'share':>7}  {'like':>7}  "
             f"{'save':>7}  {'repost':>7}  {'comment':>7}  {'date':>10}  caption")
    log(header)
    log("-" * len(header))

    for i, b in enumerate(ranked[:n], 1):
        rt = b["rates"]
        p = b["post"]
        cap = (p.get("caption") or "").strip().replace("\n", " ")[:46]
        skip_cell = _fmt_pct(rt["skip_rate"]) if rt["skip_rate"] is not None else b["skip_grade"].rjust(6)
        log(f"{i:>3}  {b['score']:>6.3f}  {skip_cell:>9}  "
            f"{_fmt_pct(rt['share_rate'])}  {_fmt_pct(rt['like_rate'])}  "
            f"{_fmt_pct(rt['save_rate'])}  {_fmt_pct(rt['repost_rate'])}  "
            f"{_fmt_pct(rt['comment_rate'])}  {p.get('timestamp', '')[:10]:>10}  {cap}")


if __name__ == "__main__":
    main()
