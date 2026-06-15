"""
grade.py -- the dormant predict->observe loop, ACTIVATED.

This is the deterministic, READ-ONLY scorer that closes the feedback loop on the
hub's 2026 content model. It asks the only honest question a self-improving
system can ask: *do our predictions actually correlate with what happened?*

It reads `ig-dashboard/data/store.json` (the realized outcomes -- views,
watch-time, skip-rate) and `ig-dashboard/metrics2026.py` (the model under test),
then grades the model against reality:

  1. grade_score_vs_outcome -- Spearman(m26 score, realized views) and
     Spearman(m26 score, avg_watch_time), IN-SAMPLE *and* HELD-OUT (train on the
     older 70% of posts by timestamp, test on the newer 30%). Held-out is the
     number that matters: in-sample correlation is partly circular because the
     percentile distribution is built from the same posts being scored.
  2. grade_skip_gate -- the skip-gate validity check. Among the ~94 posts that
     now carry reels_skip_rate, do "healthy"-band posts actually out-view and
     out-retain "throttled"-band posts? If not, the gate is noise.
  3. weight_search -- a coarse grid search over alternative WEIGHTS dicts to find
     which maximizes HELD-OUT Spearman(score, views). Reported as a PROPOSAL
     ONLY -- this script NEVER edits metrics2026.py.
  4. category_audit -- deterministic flagging of mislabeled posts ("Other" +
     captions hitting >1 category keyword set) as `category_override` candidates.

GOLDEN RULE OF THE HUB: propose, never auto-apply. This file writes ONLY to
`self-improve/data/` (gitignored generated output). It does not touch any
production engine, store.json, or the vault.

Pure stdlib (json, statistics, math, sys, datetime, pathlib, itertools). No
third-party imports. metrics2026 is imported as the model contract.

Usage:
  python self-improve/grade.py             # live grade on store.json -> data/
  python self-improve/grade.py --self-test # tiny synthetic asserts (no I/O)
"""

import json
import math
import statistics
import sys
from datetime import date
from itertools import product
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / "ig-dashboard"))
import metrics2026 as m26  # noqa: E402  (path inserted above)

STORE = BASE.parent / "ig-dashboard" / "data" / "store.json"
OUT_DIR = BASE / "data"

# Minimum-sample gates -- below these, report a number but flag it LOW CONFIDENCE.
MIN_PAIRS = 5            # Spearman is meaningless below this
MIN_SKIP_BAND = 8        # per-band count for the skip-gate comparison to mean much
MIN_HELDOUT = 20         # held-out test set below this -> low confidence


def log(msg):
    """cp1252-safe console line, mirroring the other engines' log() helper."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("cp1252", "replace").decode("cp1252"))


# --------------------------------------------------------------------------- #
# Spearman rank correlation (pure stdlib, average-rank ties -> Pearson on ranks)
# --------------------------------------------------------------------------- #

def _average_ranks(xs):
    """Return the rank of each element in xs, with ties sharing the average rank.

    Ranks are 1-based. For [10, 30, 30, 20] -> [1, 3.5, 3.5, 2]: the two 30s
    occupy positions 3 and 4, so both get (3+4)/2 = 3.5.
    """
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    n = len(xs)
    while i < n:
        j = i
        # extend j over the run of equal values
        while j + 1 < n and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        # positions i..j (0-based) -> ranks (i+1)..(j+1); average them
        avg = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    """Spearman rank correlation: Pearson correlation on average-ranked data.

    Returns a float in [-1, 1], or None if fewer than MIN_PAIRS usable pairs or
    if either ranked series has zero variance (correlation undefined).
    """
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < MIN_PAIRS:
        return None
    rx = _average_ranks([p[0] for p in pairs])
    ry = _average_ranks([p[1] for p in pairs])
    n = len(rx)
    mx = sum(rx) / n
    my = sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0 or vy == 0:
        return None
    return cov / math.sqrt(vx * vy)


# --------------------------------------------------------------------------- #
# Helpers shared across graders
# --------------------------------------------------------------------------- #

def _views(post):
    v = (post.get("insights") or {}).get("views")
    return v if isinstance(v, (int, float)) else None


def _watch(post):
    v = (post.get("insights") or {}).get("ig_reels_avg_watch_time")
    return v if isinstance(v, (int, float)) else None


def _skip(post):
    return m26.rates(post)["skip_rate"]


def _ts(post):
    return post.get("timestamp") or ""


def _split_70_30(posts):
    """Chronological split: oldest 70% TRAIN, newest 30% TEST.

    Splitting by time (not randomly) is the honest test -- it mimics using the
    history we had to predict posts we hadn't seen yet.
    """
    ordered = sorted(posts, key=_ts)
    cut = int(len(ordered) * 0.70)
    return ordered[:cut], ordered[cut:]


def _scored_pairs(test_posts, distributions, outcome_fn):
    """(m26 score, realized outcome) pairs over test_posts, dropping None outcomes."""
    xs, ys = [], []
    for p in test_posts:
        out = outcome_fn(p)
        if out is None:
            continue
        xs.append(m26.score_2026(p, distributions))
        ys.append(out)
    return xs, ys


# --------------------------------------------------------------------------- #
# LOOP-adjacent graders
# --------------------------------------------------------------------------- #

def grade_score_vs_outcome(posts):
    """Does the m26 score predict realized views / watch-time?

    In-sample: distributions built from ALL posts, scored on ALL posts (partly
    circular). Held-out: distributions built from TRAIN (older 70%), scored on
    TEST (newer 30%) -- the number that actually tells us if the model generalizes.
    """
    dist_all = m26.build_distributions(posts)

    # in-sample
    xs_v, ys_v = _scored_pairs(posts, dist_all, _views)
    xs_w, ys_w = _scored_pairs(posts, dist_all, _watch)
    in_sample = {
        "views": {"spearman": spearman(xs_v, ys_v), "n": len(xs_v)},
        "watch_time": {"spearman": spearman(xs_w, ys_w), "n": len(xs_w)},
    }

    # held-out (train older / test newer)
    train, test = _split_70_30(posts)
    dist_train = m26.build_distributions(train)
    hxs_v, hys_v = _scored_pairs(test, dist_train, _views)
    hxs_w, hys_w = _scored_pairs(test, dist_train, _watch)
    held_out = {
        "train_n": len(train),
        "test_n": len(test),
        "views": {"spearman": spearman(hxs_v, hys_v), "n": len(hxs_v)},
        "watch_time": {"spearman": spearman(hxs_w, hys_w), "n": len(hxs_w)},
        "low_confidence": len(test) < MIN_HELDOUT,
    }
    return {"in_sample": in_sample, "held_out": held_out}


def grade_skip_gate(posts):
    """Skip-gate validity: do 'healthy'-band posts outperform 'throttled' ones?

    Buckets the posts that carry reels_skip_rate by m26.grade_skip band and
    reports count + mean/median views + mean avg_watch_time per band. If healthy
    does NOT out-view/out-retain throttled, the gate is suppressing the wrong
    posts and is flagged as such.
    """
    bands = {"healthy": [], "watch": [], "throttled": []}
    for p in posts:
        sk = _skip(p)
        if sk is None:
            continue
        band = m26.grade_skip(sk)
        if band in bands:
            bands[band].append(p)

    def summarize(group):
        vs = [_views(p) for p in group if _views(p) is not None]
        ws = [_watch(p) for p in group if _watch(p) is not None]
        return {
            "count": len(group),
            "mean_views": round(statistics.mean(vs), 1) if vs else None,
            "median_views": round(statistics.median(vs), 1) if vs else None,
            "mean_watch_time": round(statistics.mean(ws), 2) if ws else None,
        }

    summary = {band: summarize(group) for band, group in bands.items()}

    # validity verdict: healthy mean_views vs throttled mean_views
    h = summary["healthy"]["mean_views"]
    t = summary["throttled"]["mean_views"]
    enough = (summary["healthy"]["count"] >= MIN_SKIP_BAND
              and summary["throttled"]["count"] >= MIN_SKIP_BAND)
    if h is None or t is None or not enough:
        verdict = "INSUFFICIENT DATA -- too few posts in healthy and/or throttled band"
        gate_holds = None
    elif h > t:
        verdict = f"GATE HOLDS -- healthy out-views throttled ({h:.0f} vs {t:.0f})"
        gate_holds = True
    else:
        verdict = (f"GATE INVERTED -- throttled out-views healthy ({t:.0f} vs {h:.0f}); "
                   f"skip-gate may be suppressing the wrong posts")
        gate_holds = False

    total_with_skip = sum(s["count"] for s in summary.values())
    return {
        "bands": summary,
        "verdict": verdict,
        "gate_holds": gate_holds,
        "n_with_skip": total_with_skip,
        "low_confidence": total_with_skip < 2 * MIN_SKIP_BAND,
    }


def _normalized_grid():
    """A coarse set of candidate WEIGHTS dicts, each normalized to sum 1.

    We vary the five weights over a small per-key level set, keep only
    combinations that are non-degenerate, and cap the total at ~80 to stay fast.
    The current production weights are guaranteed to be in the candidate set so
    the comparison is apples-to-apples.
    """
    keys = ["share", "like", "save", "repost", "comment"]
    levels = [0.10, 0.25, 0.40, 0.55]
    candidates = []
    seen = set()

    def add(raw):
        s = sum(raw.values())
        if s <= 0:
            return
        norm = {k: round(raw[k] / s, 4) for k in keys}
        sig = tuple(norm[k] for k in keys)
        if sig in seen:
            return
        seen.add(sig)
        candidates.append(norm)

    # always include the current production weights first
    add(dict(m26.WEIGHTS))

    # full grid would be 4**5 = 1024; sample it deterministically and cap.
    for combo in product(levels, repeat=len(keys)):
        raw = dict(zip(keys, combo))
        # require share to be among the top signals (2026 model keeps it dominant)
        if raw["share"] < max(raw["like"], raw["save"], raw["repost"], raw["comment"]):
            continue
        add(raw)
        if len(candidates) >= 80:
            break
    return candidates


def _score_with_weights(post, distributions, weights):
    """Re-implement m26.score_2026 with an alternative weights dict (read-only)."""
    rt = m26.rates(post)
    base = sum(weights[k] * m26.pct_rank(rt[f"{k}_rate"], distributions.get(k, []))
               for k in weights)
    return m26.skip_gate(rt["skip_rate"]) * base


def weight_search(posts):
    """Coarse search for the WEIGHTS dict that maximizes HELD-OUT Spearman(score,
    views). Reported as a PROPOSAL only -- never applied.

    Both the current and candidate weights are evaluated on the SAME held-out
    split (train older / test newer) so the comparison is fair. A candidate only
    "wins" if it beats the current weights on the held-out set by a margin.
    """
    train, test = _split_70_30(posts)
    dist_train = m26.build_distributions(train)
    test_views = [(p, _views(p)) for p in test if _views(p) is not None]

    def heldout_corr(weights):
        xs = [_score_with_weights(p, dist_train, weights) for p, _ in test_views]
        ys = [v for _, v in test_views]
        return spearman(xs, ys)

    current = dict(m26.WEIGHTS)
    current_corr = heldout_corr(current)

    best_w, best_corr = current, current_corr
    evaluated = 0
    for w in _normalized_grid():
        c = heldout_corr(w)
        evaluated += 1
        if c is not None and (best_corr is None or c > best_corr):
            best_w, best_corr = w, c

    # only call it a real proposal if it beats baseline by a meaningful margin
    MARGIN = 0.02
    if (current_corr is not None and best_corr is not None
            and best_w != current and best_corr - current_corr >= MARGIN):
        proposal = {
            "recommend_change": True,
            "old_weights": current,
            "new_weights": best_w,
            "old_corr": round(current_corr, 4),
            "new_corr": round(best_corr, 4),
            "delta": round(best_corr - current_corr, 4),
        }
    else:
        proposal = {
            "recommend_change": False,
            "reason": ("no candidate beat current weights by >= "
                       f"{MARGIN} held-out Spearman -- keep current (honest-gate)"),
            "old_weights": current,
            "old_corr": round(current_corr, 4) if current_corr is not None else None,
            "best_seen_corr": round(best_corr, 4) if best_corr is not None else None,
        }
    proposal["candidates_evaluated"] = evaluated
    proposal["test_n"] = len(test_views)
    proposal["low_confidence"] = len(test_views) < MIN_HELDOUT
    return proposal


# Lowercased keyword sets mirrored from refresh.py CATEGORIES (read-only copy;
# refresh.py is the source of truth, this is a deterministic audit lens).
_CATEGORY_KEYWORDS = [
    ("Child Safety / PSA", ["safety", "psa", "parent", "child", "kids", "predator", "blur your"]),
    ("Founder / Business", ["founder", "cofounder", "co-founder", "business", "entrepreneur",
                            "ceo", "startup", "company", "clients"]),
    ("AI / Tech",          ["ai ", " ai", "artificial intelligence", "software", "tech ",
                            "automation", "coding", "developer"]),
    ("Real Estate",        ["real estate", "property", "realtor", "housing", "development deal"]),
    ("Money / Finance",    ["money", "financ", "invest", "wealth", "broke", "rich", "income"]),
    ("Jewelry",            ["jewel", "diamond", "vvs", "gold chain", "custom piece"]),
    ("Faith",              ["jesus", "god ", "faith", "pray", "bible", "church", "scripture"]),
    ("Motivation / Life",  ["motivat", "lock in", "grind", "mindset", "discipline", "success",
                            "dream", "goal", "lazy", "potential", "yourself"]),
]


def _matched_categories(caption):
    """Return the list of category names whose keyword set the caption hits."""
    c = (caption or "").lower()
    hits = []
    for name, kws in _CATEGORY_KEYWORDS:
        if any(kw in c for kw in kws):
            hits.append(name)
    return hits


def category_audit(posts):
    """Count posts per category and flag override candidates, deterministically.

    Two flag types:
      - "other": caption was labeled 'Other' but in fact hits a known category's
        keywords (would have categorized had keyword order differed) OR is a real
        Other with no hits (listed so Elijah can eyeball them).
      - "ambiguous": caption hits >1 category keyword set, so the first-match-wins
        rule in refresh.categorize() may have picked the wrong one.

    Output is a list of {id, category, snippet, matched, kind} -- pure data for a
    `category_override` proposal. NOTHING is applied here.
    """
    counts = {}
    for p in posts:
        cat = p.get("category", "Other")
        counts[cat] = counts.get(cat, 0) + 1

    candidates = []
    for p in posts:
        cat = p.get("category", "Other")
        cap = (p.get("caption") or "").strip().replace("\n", " ")
        snippet = cap[:80]
        matched = _matched_categories(cap)

        kind = None
        if cat == "Other" and matched:
            kind = "other-but-keyword-hit"
        elif len(matched) > 1:
            # only interesting if the assigned category isn't the unique best;
            # flag when the caption straddles multiple sets
            kind = "ambiguous-multi-category"

        if kind:
            candidates.append({
                "id": p.get("id"),
                "category": cat,
                "snippet": snippet,
                "matched": matched,
                "kind": kind,
            })

    # deterministic order: kind, then category, then id
    candidates.sort(key=lambda d: (d["kind"], d["category"], str(d["id"])))
    return {"counts": counts, "candidates": candidates, "n_candidates": len(candidates)}


# --------------------------------------------------------------------------- #
# Report rendering
# --------------------------------------------------------------------------- #

def _fmt_corr(c):
    return f"{c:+.3f}" if isinstance(c, (int, float)) else "  n/a"


def render_report(grade):
    """Human-readable Markdown summary of the grade dict."""
    L = []
    L.append(f"# Self-Improve Grade Report -- {grade['date']}")
    L.append("")
    L.append(f"_Generated by `self-improve/grade.py` (read-only) over "
             f"{grade['n_posts']} posts in store.json._")
    L.append("")
    L.append("**This is the predict->observe loop.** It grades the 2026 model "
             "(`metrics2026.py`) against realized outcomes. Held-out numbers "
             "(train older 70% / test newer 30%) are the ones that matter; "
             "in-sample is partly circular.")
    L.append("")

    # --- 1. score vs outcome ---
    sv = grade["score_vs_outcome"]
    L.append("## 1. Does the m26 score predict reality? (Spearman rank corr)")
    L.append("")
    L.append("| series | in-sample (n) | held-out (n) |")
    L.append("|---|---|---|")
    for key, label in [("views", "score vs realized VIEWS"),
                       ("watch_time", "score vs AVG WATCH TIME")]:
        ins = sv["in_sample"][key]
        ho = sv["held_out"][key]
        L.append(f"| {label} | {_fmt_corr(ins['spearman'])} ({ins['n']}) "
                 f"| {_fmt_corr(ho['spearman'])} ({ho['n']}) |")
    L.append("")
    ho = sv["held_out"]
    L.append(f"Held-out split: train n={ho['train_n']} (older) / test n={ho['test_n']} (newer)."
             + ("  **LOW CONFIDENCE: small held-out set.**" if ho["low_confidence"] else ""))
    L.append("")

    # --- 2. skip gate ---
    sg = grade["skip_gate"]
    L.append("## 2. Skip-gate validity (does 'healthy' actually outperform 'throttled'?)")
    L.append("")
    L.append(f"Posts carrying `reels_skip_rate`: **{sg['n_with_skip']}**"
             + ("  _(borderline sample -- treat bands as directional)_"
                if sg["low_confidence"] else ""))
    L.append("")
    L.append("| band | count | mean views | median views | mean watch time |")
    L.append("|---|---|---|---|---|")
    for band in ["healthy", "watch", "throttled"]:
        b = sg["bands"][band]
        L.append(f"| {band} | {b['count']} | {b['mean_views']} "
                 f"| {b['median_views']} | {b['mean_watch_time']} |")
    L.append("")
    L.append(f"**Verdict:** {sg['verdict']}")
    L.append("")

    # --- 3. weight proposal ---
    ws = grade["weight_search"]
    L.append("## 3. Weight-tuning proposal (held-out Spearman vs views) -- PROPOSAL ONLY")
    L.append("")
    L.append(f"Candidates evaluated: {ws['candidates_evaluated']} | held-out test n={ws['test_n']}"
             + ("  **LOW CONFIDENCE.**" if ws["low_confidence"] else ""))
    L.append("")
    if ws["recommend_change"]:
        L.append(f"**PROPOSE** changing `metrics2026.WEIGHTS` (honest-gate passed, "
                 f"delta {ws['delta']:+.3f} held-out Spearman):")
        L.append("")
        L.append(f"- OLD: `{ws['old_weights']}` (corr {ws['old_corr']:+.3f})")
        L.append(f"- NEW: `{ws['new_weights']}` (corr {ws['new_corr']:+.3f})")
        L.append("")
        L.append("Route via dev-workflow as a one-line WEIGHTS edit to "
                 "`ig-dashboard/metrics2026.py:56`. Do NOT auto-apply.")
    else:
        L.append(f"**NO CHANGE PROPOSED** (honest-gate): {ws['reason']}")
        L.append("")
        L.append(f"- current WEIGHTS corr: {_fmt_corr(ws['old_corr'])} | "
                 f"best candidate seen: {_fmt_corr(ws['best_seen_corr'])}")
    L.append("")

    # --- 4. category audit ---
    ca = grade["category_audit"]
    L.append("## 4. Category audit -- `category_override` candidates (data-only fix)")
    L.append("")
    L.append("Category counts:")
    L.append("")
    for cat, n in sorted(ca["counts"].items(), key=lambda kv: -kv[1]):
        L.append(f"- {cat}: {n}")
    L.append("")
    L.append(f"Override candidates flagged: **{ca['n_candidates']}** "
             "(captions labeled 'Other' that hit a category keyword, or captions "
             "straddling >1 category). These are safe data-only fixes via "
             "`category_override` (refresh.py:193).")
    L.append("")
    if ca["candidates"]:
        L.append("| id | current | matched categories | caption snippet |")
        L.append("|---|---|---|---|")
        for c in ca["candidates"][:30]:
            matched = ", ".join(c["matched"]) or "(none)"
            snip = c["snippet"].replace("|", "\\|")
            L.append(f"| `{c['id']}` | {c['category']} | {matched} | {snip} |")
        if ca["n_candidates"] > 30:
            L.append("")
            L.append(f"_({ca['n_candidates'] - 30} more in the JSON sidecar.)_")
    L.append("")

    L.append("---")
    L.append("")
    L.append("**Golden rule:** this report PROPOSES. Nothing here is applied. Real "
             "changes go through `docs/templates/SELF-IMPROVE-PROPOSAL.md` -> "
             "dev-workflow. The only safe auto-writes are the append-only ledger "
             "in `self-improve/data/`, `category_override` data fixes, "
             "`team/memory.md` learnings, and `intel/*.json` watchlist suggestions.")
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def grade_all(posts):
    """Run every grader and bundle the machine-readable result."""
    return {
        "date": date.today().isoformat(),
        "n_posts": len(posts),
        "score_vs_outcome": grade_score_vs_outcome(posts),
        "skip_gate": grade_skip_gate(posts),
        "weight_search": weight_search(posts),
        "category_audit": category_audit(posts),
    }


def load_posts():
    with open(STORE, encoding="utf-8") as f:
        store = json.load(f)
    return list(store.get("posts", {}).values())


# --------------------------------------------------------------------------- #
# Self-test (no I/O; tiny synthetic asserts)
# --------------------------------------------------------------------------- #

def _self_test():
    # spearman: perfectly monotonic increasing -> +1
    assert spearman([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]) == 1.0, "monotonic up -> +1"
    # spearman: perfectly monotonic decreasing -> -1
    assert spearman([1, 2, 3, 4, 5], [50, 40, 30, 20, 10]) == -1.0, "monotonic down -> -1"
    # spearman: monotonic but non-linear still -> +1 (rank-based)
    assert spearman([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]) == 1.0, "rank-monotonic -> +1"
    # too few pairs -> None
    assert spearman([1, 2, 3], [1, 2, 3]) is None, "<5 pairs -> None"
    # zero variance -> None
    assert spearman([1, 1, 1, 1, 1], [1, 2, 3, 4, 5]) is None, "flat x -> None"

    # average ranks with ties
    r = _average_ranks([10, 30, 30, 20])
    assert r == [1.0, 3.5, 3.5, 2.0], f"tie-averaged ranks wrong: {r}"

    # 70/30 chronological split keeps order and proportion
    pp = [{"timestamp": f"2026-01-{d:02d}T00:00:00+0000"} for d in range(1, 11)]
    train, test = _split_70_30(pp)
    assert len(train) == 7 and len(test) == 3, f"split sizes {len(train)}/{len(test)}"
    assert train[0]["timestamp"] < test[0]["timestamp"], "train must be older than test"

    # skip-gate bucketing via m26 grade_skip
    fake = [
        {"insights": {"reach": 1000, "views": 9000, "ig_reels_avg_watch_time": 5.0,
                      "reels_skip_rate": 0.30, "shares": 50, "saved": 30},
         "like_count": 200, "comments_count": 10, "timestamp": "2026-01-01T00:00:00+0000"},
        {"insights": {"reach": 1000, "views": 100, "ig_reels_avg_watch_time": 1.0,
                      "reels_skip_rate": 0.62, "shares": 1, "saved": 1},
         "like_count": 5, "comments_count": 1, "timestamp": "2026-01-02T00:00:00+0000"},
    ]
    sg = grade_skip_gate(fake)
    assert sg["bands"]["healthy"]["count"] == 1, "one healthy post expected"
    assert sg["bands"]["throttled"]["count"] == 1, "one throttled post expected"
    assert sg["bands"]["healthy"]["mean_views"] == 9000.0, "healthy mean views wrong"

    # weight grid: current weights always present, all normalized to sum 1
    grid = _normalized_grid()
    assert any(abs(sum(w.values()) - 1.0) < 1e-6 for w in grid), "weights must sum to 1"
    cur = {k: round(v, 4) for k, v in m26.WEIGHTS.items()}
    norm_cur = {k: round(cur[k] / sum(cur.values()), 4) for k in cur}
    assert any(w == norm_cur for w in grid), "current weights must be a candidate"

    # category audit flags an Other post that hits a keyword
    posts = [
        {"id": "x1", "category": "Other", "caption": "the best automation software for your business"},
        {"id": "x2", "category": "Faith", "caption": "just a normal caption with no keywords here zzz"},
    ]
    ca = category_audit(posts)
    flagged_ids = {c["id"] for c in ca["candidates"]}
    assert "x1" in flagged_ids, "Other-but-keyword-hit post must be flagged"
    assert ca["counts"]["Other"] == 1, "category count wrong"

    log("self-test OK")


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        _self_test()
        return

    if not STORE.exists():
        log(f"FATAL: store.json not found at {STORE}")
        sys.exit(1)

    posts = load_posts()
    log(f"grading {len(posts)} posts against metrics2026 ...")
    grade = grade_all(posts)

    OUT_DIR.mkdir(exist_ok=True)
    json_path = OUT_DIR / f"grade-{grade['date']}.json"
    md_path = OUT_DIR / "grade-report.md"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(grade, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_report(grade))

    # console summary
    sv = grade["score_vs_outcome"]["held_out"]
    log(f"held-out Spearman(score, views) = {_fmt_corr(sv['views']['spearman'])} "
        f"(test n={sv['test_n']})")
    log(f"skip-gate: {grade['skip_gate']['verdict']}")
    log(f"weight proposal: {'CHANGE' if grade['weight_search']['recommend_change'] else 'no change'}")
    log(f"category override candidates: {grade['category_audit']['n_candidates']}")
    log(f"wrote {json_path.name} + grade-report.md to {OUT_DIR}")


if __name__ == "__main__":
    main()
