"""
watchtime_ideator.py -- mine @elijahaifl's own 300 reels for the content
categories + specific reels that hold attention the LONGEST, and surface
concrete long-form / topic ideas the 2026 IG algorithm actually rewards.

WHY THIS EXISTS
---------------
The 2026 Reels ranking signal Mosseri/Meta call out as #1 is watch time /
retention / skip-rate -- above shares, saves, likes. Today team/stats.md and
the weekly-content-plan skill rank categories by VIEWS, which is a downstream
signal. This module ranks by WATCH TIME (the upstream lever) and reports which
categories hold attention consistently -> long-form / deeper-topic bets.

Per the plan (docs/plans/2026-06-14-watchtime-longform-ideator-research.md) it
computes, per the dashboard's own stored `category`:
  - avg watch seconds per category (ig_reels_avg_watch_time / 1000, averaged)
  - consistency: median + IQR spread (so a category isn't crowned on one fluke)
  - a watch-time-vs-views arbitrage gap (holds attention but under-posted = the
    bet; gets views but low hold = skip-rate risk)
  - the specific top-hold reels per winning category, as long-form seeds.

HONEST LIMITER (stated in the report header too): Meta exposes no per-post video
duration on the IG Media object, so this ranks RAW avg watch seconds + a
within-history relative score, NOT true % completion. A 17s hold on a 20s reel
is near-complete; a 17s hold on a 90s reel is a big drop-off. Treat the seconds
as a RELATIVE category signal, not absolute retention. True completion % is a
Phase 2 add via local ffprobe -- out of scope here.

ADDITIVE + READ-ONLY: reads ig-dashboard/data/store.json and computes
arithmetic. Imports metrics2026 to reuse its 2026 composite ranking for the
seed reels. Does NOT modify refresh.py / metrics2026.py / any engine, does NOT
touch the vault, never publishes. Pure stdlib (json, statistics, collections).

FIELD REALITY (verified against the live store.json on 2026-06-14):
  - all 300 posts have a non-null insights.ig_reels_avg_watch_time (ms) and
    insights.ig_reels_video_view_total_time (ms), insights.views, and a
    top-level `category` already assigned by refresh.py::categorize().
  - categories present: Motivation / Life (94), Other (61), Founder / Business
    (45), AI / Tech (34), Money / Finance (27), Child Safety / PSA (24),
    Faith (12), Jewelry (2), Real Estate (1). The plan's sample table omitted
    "Other"; this module reports it but never gives a small-n category a
    "direction" call (MIN_N gate).

Usage:
  python watchtime_ideator.py            # write report + print summary
  python watchtime_ideator.py --n 5      # top-N seed reels per winning category
  python watchtime_ideator.py --days 30  # restrict window (default: all history)
  python watchtime_ideator.py --self-test
"""

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Reuse the canonical 2026 ranker so seed reels carry the same composite score
# the rest of the hub uses. Import is best-effort: the report still works on
# pure watch-time if metrics2026 is unavailable for any reason.
try:
    import metrics2026  # sibling module in ig-dashboard/
    _HAVE_METRICS = True
except Exception:
    metrics2026 = None
    _HAVE_METRICS = False

BASE = Path(__file__).resolve().parent
STORE = BASE / "data" / "store.json"
REPORT = BASE / "data" / "watchtime-ideas.md"

# A category needs at least this many posts before it earns a "direction" call.
# Below it, the average is noise (Real Estate n=1, Jewelry n=2). From the plan's
# Risks section.
MIN_N = 5

# "Other" is the uncategorized bucket -- real posts, but no topic to act on, so
# it's shown for completeness but excluded from idea generation.
NOISE_CATEGORIES = {"Other"}


def log(msg):
    """cp1252-safe console line, mirroring the other engines' log() helper."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("cp1252", "replace").decode("cp1252"))


# --------------------------------------------------------------------------- #
# Per-post field access (None-safe, mirrors metrics2026 conventions)
# --------------------------------------------------------------------------- #

def _ins(post, key):
    return (post.get("insights") or {}).get(key)


def watch_s(post):
    """Average watch time in SECONDS for one reel, or None if missing.

    ig_reels_avg_watch_time is returned by the Graph API in milliseconds.
    """
    v = _ins(post, "ig_reels_avg_watch_time")
    return v / 1000.0 if isinstance(v, (int, float)) else None


def total_watch_s(post):
    """Total reel view time in SECONDS (ms / 1000), or None. A depth-of-attention
    proxy: avg-hold x viewers, so a high value = lots of cumulative attention."""
    v = _ins(post, "ig_reels_video_view_total_time")
    return v / 1000.0 if isinstance(v, (int, float)) else None


def views(post):
    v = _ins(post, "views")
    return v if isinstance(v, (int, float)) else 0


def category(post):
    c = post.get("category")
    return c if c else "Other"


def _ts(post):
    """Parse the post timestamp to an aware datetime, or None."""
    raw = post.get("timestamp")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("+0000", "+00:00"))
    except (ValueError, AttributeError):
        return None


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #

def _iqr(vals):
    """Interquartile range (spread) of a list; 0.0 if <2 points. The
    consistency signal -- a tight IQR means the category holds attention
    'every time', not on one fluke (the vault note's literal ask)."""
    if len(vals) < 2:
        return 0.0
    qs = statistics.quantiles(vals, n=4)  # [Q1, Q2(median), Q3]
    return qs[2] - qs[0]


def category_stats(posts):
    """Aggregate per-category watch-time + views into a list of dicts, sorted by
    mean watch seconds descending. Each dict:
        name, n, mean_watch, median_watch, iqr_watch, mean_views,
        total_watch_s, share_of_posts (None-filled where data missing).
    Posts with a missing avg_watch_time are skipped from the watch stats (graceful
    degradation per the plan's metric-deprecation mitigation).
    """
    by_cat = defaultdict(lambda: {"watch": [], "views": [], "total": 0.0, "n": 0})
    total_posts = 0
    for p in posts:
        w = watch_s(p)
        c = category(p)
        bucket = by_cat[c]
        bucket["n"] += 1
        total_posts += 1
        if w is not None:
            bucket["watch"].append(w)
        bucket["views"].append(views(p))
        tw = total_watch_s(p)
        if tw is not None:
            bucket["total"] += tw

    rows = []
    for name, b in by_cat.items():
        watch = b["watch"]
        rows.append({
            "name": name,
            "n": b["n"],
            "mean_watch": statistics.fmean(watch) if watch else None,
            "median_watch": statistics.median(watch) if watch else None,
            "iqr_watch": _iqr(watch),
            "mean_views": statistics.fmean(b["views"]) if b["views"] else 0.0,
            "total_watch_s": b["total"],
            "share_of_posts": b["n"] / total_posts if total_posts else 0.0,
        })
    # sort by hold; categories with no watch data sink to the bottom.
    rows.sort(key=lambda r: (r["mean_watch"] is not None, r["mean_watch"] or 0),
              reverse=True)
    return rows, total_posts


def arbitrage(rows):
    """Rank categories by a watch-vs-views *gap* to flag the two arbitrages the
    plan names:
      - UNDER-POSTED HOLD: high watch-rank but low post-share -> deepen / go
        long-form here (the algorithm rewards it and Elijah under-supplies it).
      - SKIP-RISK: high views-rank but low watch-rank -> rides reach, weak
        retention; a 2026 skip-rate liability.

    Returns (under_posted, skip_risk) lists of dicts, each with the category row
    plus its watch_rank, views_rank, post_share. Only categories meeting MIN_N
    and not in NOISE_CATEGORIES are considered.
    """
    eligible = [r for r in rows
                if r["n"] >= MIN_N
                and r["name"] not in NOISE_CATEGORIES
                and r["mean_watch"] is not None]
    if not eligible:
        return [], []

    n = len(eligible)
    # rank 1 = best. Build 0..1 normalized ranks so categories of any count compare.
    by_watch = sorted(eligible, key=lambda r: r["mean_watch"], reverse=True)
    by_views = sorted(eligible, key=lambda r: r["mean_views"], reverse=True)
    watch_rank = {r["name"]: i for i, r in enumerate(by_watch)}
    views_rank = {r["name"]: i for i, r in enumerate(by_views)}

    enriched = []
    for r in eligible:
        wr = watch_rank[r["name"]]
        vr = views_rank[r["name"]]
        enriched.append({
            **r,
            "watch_rank": wr + 1,
            "views_rank": vr + 1,
            "rank_gap": vr - wr,  # positive => holds better than it gets viewed
        })

    # Under-posted hold: holds well (top half on watch) but is a small share of
    # the posting mix -> room to lean in.
    median_share = statistics.median([r["share_of_posts"] for r in enriched])
    under_posted = sorted(
        [r for r in enriched
         if r["watch_rank"] <= max(1, n // 2) and r["share_of_posts"] <= median_share],
        key=lambda r: (r["watch_rank"], r["share_of_posts"]))

    # Skip-risk: gets views but holds worse than its view rank (rank_gap < 0).
    skip_risk = sorted([r for r in enriched if r["rank_gap"] < 0],
                       key=lambda r: r["rank_gap"])
    return under_posted, skip_risk


def top_hold_reels(posts, cat_name, n, score_lookup):
    """Return the top-n highest-avg-watch reels in a category, each as a dict with
    watch seconds, views, the 2026 composite score (if available), date, caption.
    These are the concrete long-form / deeper-topic SEEDS."""
    in_cat = [p for p in posts if category(p) == cat_name and watch_s(p) is not None]
    in_cat.sort(key=watch_s, reverse=True)
    seeds = []
    for p in in_cat[:n]:
        seeds.append({
            "watch_s": watch_s(p),
            "views": views(p),
            "score_2026": score_lookup.get(id(p)),
            "date": (p.get("timestamp") or "")[:10],
            "caption": (p.get("caption") or "").strip().replace("\n", " "),
            "permalink": p.get("permalink", ""),
        })
    return seeds


# --------------------------------------------------------------------------- #
# 2026 composite score lookup (reuse metrics2026)
# --------------------------------------------------------------------------- #

def build_score_lookup(posts):
    """Map id(post) -> metrics2026 composite score, reusing the canonical ranker
    so seeds carry the same number the rest of the hub uses. Empty if metrics2026
    is unavailable (report degrades to pure watch-time)."""
    if not _HAVE_METRICS:
        return {}
    try:
        dist = metrics2026.build_distributions(posts)
        return {id(p): metrics2026.score_2026(p, dist) for p in posts}
    except Exception as e:
        log(f"WARN: metrics2026 scoring unavailable ({e}); seeds show watch-time only")
        return {}


# --------------------------------------------------------------------------- #
# Report rendering
# --------------------------------------------------------------------------- #

def _fmt_s(v):
    return f"{v:.1f}s" if v is not None else "  -- "


def render_markdown(rows, total_posts, under_posted, skip_risk, posts,
                    score_lookup, top_n, window_label):
    now = datetime.now(timezone.utc)
    L = []
    L.append("# Watch-time content read — @elijahaifl")
    L.append("")
    L.append(f"_Generated {now.strftime('%Y-%m-%d %H:%M UTC')} by "
             "`ig-dashboard/watchtime_ideator.py` (read-only). Window: "
             f"{window_label}. {total_posts} reels._")
    L.append("")
    L.append("> **How to read this.** Ranks Elijah's own categories by how long "
             "people watch (`ig_reels_avg_watch_time`), the #1 signal the 2026 "
             "Reels algorithm rewards — the *upstream* lever, vs the views-ranked "
             "view in `stats.md`. **Caveat:** Meta exposes no per-post video "
             "duration, so these are RAW avg watch **seconds** + relative rank, "
             "NOT true % completion. A 17s hold on a 20s reel is near-complete; "
             "17s on a 90s reel is a big drop-off. Treat seconds as a *relative* "
             f"category signal. Categories with n<{MIN_N} get no direction call.")
    L.append("")

    # --- Category table ---
    L.append("## Category mix — by watch-time (avg hold seconds)")
    L.append("")
    L.append("| Category | n | avg watch | median | spread (IQR) | avg views |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for r in rows:
        flag = "" if (r["n"] >= MIN_N and r["name"] not in NOISE_CATEGORIES) else " ⚠ small-n / Other"
        L.append(f"| {r['name']}{flag} | {r['n']} | "
                 f"{_fmt_s(r['mean_watch'])} | {_fmt_s(r['median_watch'])} | "
                 f"{_fmt_s(r['iqr_watch'])} | {r['mean_views']:,.0f} |")
    L.append("")
    L.append("_Sorted by avg hold. **Tight IQR = consistent** (holds attention "
             "*every time*, not one fluke) — the categories worth committing "
             "long-form budget to._")
    L.append("")

    # --- Arbitrage ---
    L.append("## The arbitrage — where watch-time and views disagree")
    L.append("")
    if under_posted:
        L.append("### Long-form / deepen here (holds attention, under-posted)")
        L.append("")
        for r in under_posted:
            L.append(f"- **{r['name']}** — watch-rank #{r['watch_rank']}, "
                     f"views-rank #{r['views_rank']}, only "
                     f"{r['share_of_posts']*100:.0f}% of posts "
                     f"({r['n']}). Avg hold {_fmt_s(r['mean_watch'])}. "
                     "→ Strong retention but under-supplied. Best long-form bet.")
        L.append("")
    else:
        L.append("_No clearly under-posted high-hold category this window._")
        L.append("")
    if skip_risk:
        L.append("### Skip-rate risk (gets views, holds worse than it's viewed)")
        L.append("")
        for r in skip_risk:
            L.append(f"- **{r['name']}** — views-rank #{r['views_rank']} but "
                     f"watch-rank #{r['watch_rank']} (gap {r['rank_gap']:+d}). "
                     f"Avg views {r['mean_views']:,.0f}, avg hold "
                     f"{_fmt_s(r['mean_watch'])}. → Great hook / reach, weaker "
                     "depth; a 2026 skip-rate liability. Tighten the middle.")
        L.append("")
    else:
        L.append("_No category over-indexes on views vs hold this window._")
        L.append("")

    # --- Seed reels per winning (high-hold, eligible) category ---
    L.append(f"## Long-form seeds — top {top_n} highest-hold reels per winning category")
    L.append("")
    L.append("_Your own deepest-attention reels in each high-hold category. "
             "Each is a proven retention hit to expand into a longer / multi-part "
             "piece or a carousel. `2026` = the metrics2026 composite score._")
    L.append("")
    winners = [r for r in rows
               if r["n"] >= MIN_N and r["name"] not in NOISE_CATEGORIES
               and r["mean_watch"] is not None][:4]
    for r in winners:
        L.append(f"### {r['name']}  (avg hold {_fmt_s(r['mean_watch'])}, n={r['n']})")
        L.append("")
        seeds = top_hold_reels(posts, r["name"], top_n, score_lookup)
        for s in seeds:
            score_cell = (f" · 2026 {s['score_2026']:.3f}"
                          if s["score_2026"] is not None else "")
            cap = s["caption"][:120] or "(no caption)"
            L.append(f"- **{_fmt_s(s['watch_s'])} hold** · {s['views']:,} views"
                     f"{score_cell} · {s['date']}")
            L.append(f"  - {cap}")
        L.append("")

    # --- Closing direction ---
    L.append("## Bottom line")
    L.append("")
    if winners:
        lead = winners[0]
        L.append(f"- **Top-hold category: {lead['name']}** "
                 f"({_fmt_s(lead['mean_watch'])} avg). Your clearest long-form "
                 "/ deeper-topic lane.")
    if under_posted:
        names = ", ".join(r["name"] for r in under_posted)
        L.append(f"- **Lean in (under-posted but holds): {names}.**")
    if skip_risk:
        names = ", ".join(r["name"] for r in skip_risk)
        L.append(f"- **Watch the hook-vs-depth gap on: {names}** — they ride "
                 "reach, not retention.")
    L.append("- _Next step is Elijah's call: pick a seed above and expand it. "
             "This module stops at the report; no vault write, no publish._")
    L.append("")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def load_posts():
    """Read store.json (read-only) and return the list of post dicts."""
    with open(STORE, encoding="utf-8") as f:
        store = json.load(f)
    return list(store.get("posts", {}).values())


def filter_window(posts, days):
    """Keep posts within `days` of now (None => all history)."""
    if not days:
        return posts
    now = datetime.now(timezone.utc)
    out = []
    for p in posts:
        ts = _ts(p)
        if ts is not None and (now - ts).days <= days:
            out.append(p)
    return out


def _self_test():
    """Inline sanity check (no framework, matches hub style)."""
    fake = [
        # high-hold, under-posted-ish niche
        {"category": "AI / Tech", "timestamp": "2026-06-10T00:00:00+0000",
         "caption": "ai automation deep dive",
         "insights": {"ig_reels_avg_watch_time": 18000,
                      "ig_reels_video_view_total_time": 90000, "views": 5000, "reach": 4000,
                      "shares": 5, "saved": 10}},
        {"category": "AI / Tech", "timestamp": "2026-06-09T00:00:00+0000",
         "caption": "more ai",
         "insights": {"ig_reels_avg_watch_time": 16000,
                      "ig_reels_video_view_total_time": 80000, "views": 4000, "reach": 3500,
                      "shares": 3, "saved": 8}},
        # high-views, low-hold (skip risk)
        {"category": "Money / Finance", "timestamp": "2026-06-08T00:00:00+0000",
         "caption": "get rich quick money",
         "insights": {"ig_reels_avg_watch_time": 6000,
                      "ig_reels_video_view_total_time": 600000, "views": 200000, "reach": 150000,
                      "shares": 50, "saved": 100}},
        # missing watch-time -> must not crash, must be skipped from watch stats
        {"category": "Faith", "timestamp": "2026-06-07T00:00:00+0000",
         "caption": "faith post", "insights": {"views": 1000, "reach": 900}},
    ]
    rows, total = category_stats(fake)
    assert total == 4
    ai = next(r for r in rows if r["name"] == "AI / Tech")
    assert ai["n"] == 2 and abs(ai["mean_watch"] - 17.0) < 1e-6, "AI mean hold = 17s"
    faith = next(r for r in rows if r["name"] == "Faith")
    assert faith["mean_watch"] is None, "missing watch-time -> None, not crash"
    # AI should out-hold Money even though Money has way more views.
    assert rows[0]["name"] == "AI / Tech", "highest-hold category sorts first"
    # MIN_N gate: with n<5 nothing is eligible; just assert it doesn't crash.
    up, sr = arbitrage(rows)
    assert isinstance(up, list) and isinstance(sr, list)
    # seeds
    lookup = build_score_lookup(fake)
    seeds = top_hold_reels(fake, "AI / Tech", 5, lookup)
    assert seeds and seeds[0]["watch_s"] == 18.0, "top seed = highest hold"
    # window filter
    assert len(filter_window(fake, 30)) <= 4
    log("self-test OK")


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        _self_test()
        return

    top_n = 3
    if "--n" in argv:
        try:
            top_n = int(argv[argv.index("--n") + 1])
        except (IndexError, ValueError):
            log("WARN: --n needs an integer; defaulting to 3")

    days = None
    if "--days" in argv:
        try:
            days = int(argv[argv.index("--days") + 1])
        except (IndexError, ValueError):
            log("WARN: --days needs an integer; defaulting to all history")

    if not STORE.exists():
        log(f"FATAL: store.json not found at {STORE}")
        sys.exit(1)

    all_posts = load_posts()
    posts = filter_window(all_posts, days)
    window_label = f"last {days}d" if days else "all tracked history"
    if not posts:
        log("FATAL: no posts in window")
        sys.exit(1)

    score_lookup = build_score_lookup(posts)
    rows, total = category_stats(posts)
    under_posted, skip_risk = arbitrage(rows)

    md = render_markdown(rows, total, under_posted, skip_risk, posts,
                         score_lookup, top_n, window_label)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(md)

    # --- stdout summary ---
    log(f"watchtime-ideator — {total} reels | window: {window_label} | "
        f"2026 scoring: {'on' if score_lookup else 'off'}")
    log(f"report written: {REPORT}")
    log("")
    log("Category mix — by watch-time (avg hold seconds):")
    header = f"  {'category':<24} {'n':>3}  {'avg':>6}  {'median':>7}  {'avg views':>10}"
    log(header)
    log("  " + "-" * (len(header) - 2))
    for r in rows:
        flag = "" if (r["n"] >= MIN_N and r["name"] not in NOISE_CATEGORIES) else "  (small-n/Other)"
        log(f"  {r['name']:<24} {r['n']:>3}  {_fmt_s(r['mean_watch']):>6}  "
            f"{_fmt_s(r['median_watch']):>7}  {r['mean_views']:>10,.0f}{flag}")
    log("")
    if under_posted:
        log("Lean in (holds attention, under-posted): "
            + ", ".join(r["name"] for r in under_posted))
    if skip_risk:
        log("Skip-rate risk (views > hold): "
            + ", ".join(r["name"] for r in skip_risk))
    log("")
    log("Full ranked report + long-form seeds in: " + str(REPORT))


if __name__ == "__main__":
    main()
