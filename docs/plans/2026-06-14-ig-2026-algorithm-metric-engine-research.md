# 2026 IG algorithm metric-priority engine — build & feasibility research

- **Candidate id:** `ig-2026-algorithm-metric-engine`
- **Date:** 2026-06-14
- **Source of the ask:** `obsidian/Elijah's vault/Research/YouTube summary in the new way to win with Instagram in 2026 content algorithm.md` (Enrico Incarnati teardown) + roadmap STILL-TO-RESEARCH (Knowledge/strategy) + program jump-queue (Priority #1 / cross-cutting force-multiplier).

---

## Verdict: ADD-NOW — but it's a small shared library + one new metric pull, NOT a new engine

**One-line:** Define one canonical `metrics2026` scoring module (≈100 lines, stdlib only) that turns the raw fields the dashboard *already stores* (`views, reach, saved, shares, total_interactions, likes, comments` + the newly-API-exposed `reels_skip_rate`) into the six 2026 priority rates, and have every scoring surface import it instead of hand-rolling a sort. This is the cheapest high-leverage change on the whole roadmap: it's mostly *wiring + a definition*, the data is already on disk, and a December-2025 Meta API change made the #1 metric (skip rate) machine-readable for the first time. **Build Phase 0 + Phase 1 now.**

**Two corrections to the candidate's framing (be honest with Elijah):**

1. **The premise "every surface currently sorts on LIKES" is mostly wrong.** I read the actual code. `ig-dashboard/refresh.py` already sorts top posts by **views** (`refresh.py` line 342-345, `def views(p)` → `sorted(..., key=views, ...)`). `intel/competitor-radar.py` already ranks breakouts by **views** vs the account's median (lines 79, 138-141). `intel/trend-radar.py` ranks by velocity of Wikipedia/Reddit signal, not likes at all. So the problem isn't "sorts on likes" — it's that **nobody computes the 2026 *rates* (skip-rate, share-rate, save-rate) at all**, even though every raw field needed is already captured per-post (and even snapshotted over time in `post["history"]`). The fix is "add the rate layer + a canonical sort," not "stop sorting on likes."

2. **`viral-scraper` hook_score and `audience-sim` are NOT BUILT yet** (they're research plans: `docs/plans/2026-06-14-viral-scraper-niche-radar-research.md`, `docs/plans/2026-06-13-audience-sim-pipeline.md`). So "wire the metric model into them" is forward-looking — you can't refactor code that doesn't exist. The win you can bank *today* is the dashboard + the markdown-driven skills (`reel-analytics`, `weekly-content-plan`, `niche-intel`). The shared module then becomes the contract those future engines import on day one.

**Why ADD-NOW and not later:** (a) zero new dependencies, zero new model, zero OneDrive/torch/cv2 risk — pure stdlib over data already on disk; (b) it's a genuine correctness gap — the hub's own `stats.md` and every skill currently reason about "top posts" with no notion of skip-rate, the literal #1 2026 signal; (c) it's a force-multiplier: defining the canonical model *once* means every future surface (viral-scraper, audience-sim, carousel-builder) inherits the right target instead of re-litigating it; (d) the enabling API change (skip rate in the API) is brand-new (Dec 2025) and nothing in the hub uses it yet.

**Rough effort:** Phase 0 ≈ 1-2 hrs (the module + unit math). Phase 1 ≈ half-day (add the `reels_skip_rate`/`reposts` pull to `refresh.py`, surface rates in `stats.md`/dashboard, point `reel-analytics` + `weekly-content-plan` at the module). Phase 2 (competitor proxy + future-engine contract) ≈ half-day, optional.

---

## What it actually is / what it does

It is **a definition, not a scraper or a model.** The Enrico Incarnati video (the vault source) and independent 2026 sources agree on Instagram's stated order-of-operations for what drives Reels views:

| # | Metric | What it measures | Source field(s) |
|---|---|---|---|
| 1 | **Skip rate** | % who skip in the first 3s (hook failure). *Lower is better.* | `reels_skip_rate` (NEW, Dec 2025 API) |
| 2 | **Share rate** | sends ÷ reach — strongest social proof | `shares / reach` |
| 3 | **Like rate** | likes ÷ reach, earned across the video | `likes / reach` |
| 4 | **Save rate** | saves ÷ reach — now *secondary* | `saved / reach` |
| 5 | **Repost rate** | reposts ÷ reach — low-conviction passive signal | `reposts / reach` (NEW, Dec 2025 API) |
| 6 | **Comment rate** | comments ÷ reach — *lowest* priority; warns against keyword-bait | `comments / reach` |

The candidate is to make this table the **single source of truth** the hub computes and ranks on, replacing ad-hoc "sort by views/likes" with a principled composite that respects the 2026 weighting (and, critically, treats **skip rate as the gate** — a great-share post with a 60% skip rate is a hook failure, not a winner).

### The decisive feasibility finding (this is what flips it to ADD-NOW)

**As of December 2025, Meta added `reels_skip_rate` and repost counts to the Instagram Insights API.** Before this, skip rate was UI-only (you could see it in the app but not pull it), which would have made the #1 metric unautomatable. Now it's a field on the `/{ig-media-id}/insights` endpoint for professional/creator accounts. Independently corroborated by Social Media Today, Storrito, and Global Dating Insights (see Sources). The four new metrics: **`reels_skip_rate`**, **repost counts (media-level)**, **repost counts (account-level)**, **profile visits (ads)**, plus a crossposted-views update.

Concrete benchmarks found (use these as the gate thresholds): **skip rate 30-40% is healthy; >50% and Instagram treats the Reel as low-quality and throttles distribution** (inro.social, early 2026). Average watch time is length-dependent (≈12s is excellent on a 15s reel). No official numeric benchmark exists for share/save rate — so rank those *relative to Elijah's own 300-post distribution* (percentile within his history), not against an absolute.

---

## Windows + OneDrive feasibility + dependency weight

**Lightest possible addition — green across the board.**

- **Dependencies:** none. Pure Python stdlib (arithmetic + `statistics` for percentiles). No torch, no cv2, no cloud, no paid API, no model download, no large files. It operates on JSON already in `ig-dashboard/store.json`.
- **OneDrive:** safe — no heavy imports that hang on the synced disk (the known failure mode); it's a small module other scripts `import`.
- **Secrets:** none new. Uses the existing `INSTAGRAM_ACCESS_TOKEN`. The one API call added (`reels_skip_rate` in the existing `REEL_EXTRAS` metric string) rides the token + rate-limit budget the dashboard already manages (`CALL_SLEEP`, re-fetch logic).
- **Scheduled task:** no new task — it's inside the existing daily `refresh.py` run.

---

## Integration sketch — how it composes with the hub

**Create one shared module, then point existing surfaces at it. Do NOT create a new top-level engine.**

### New file: `ig-dashboard/metrics2026.py` (the canonical contract)

Pure functions, no I/O, fully unit-testable:

```python
# Priority order + weights from the 2026 model (skip-rate is a GATE, not a weight)
WEIGHTS = {"share": 0.40, "like": 0.25, "save": 0.20, "repost": 0.10, "comment": 0.05}
SKIP_HEALTHY = 0.40   # <= this is good
SKIP_THROTTLE = 0.50  # > this and IG suppresses distribution

def rates(post_insights: dict) -> dict:
    """Raw IG fields -> the six per-reach rates (None-safe)."""
    reach = post_insights.get("reach") or 0
    def r(field): 
        v = post_insights.get(field)
        return (v / reach) if (v is not None and reach) else None
    return {
        "skip_rate":    post_insights.get("reels_skip_rate"),  # already a rate from API
        "share_rate":   r("shares"),
        "like_rate":    r("likes"),
        "save_rate":    r("saved"),
        "repost_rate":  r("reposts"),
        "comment_rate": r("comments"),
    }

def score_2026(post_insights, percentiles) -> float:
    """Composite aligned to 2026 priority. percentiles = Elijah's own distribution
    per rate, so share/save are graded relative to his history, not an absolute."""
    rt = rates(post_insights)
    # skip-rate gate: hard penalty above the throttle line
    skip = rt["skip_rate"]
    gate = 1.0 if (skip is None or skip <= SKIP_HEALTHY) else \
           (0.5 if skip <= SKIP_THROTTLE else 0.2)
    base = sum(WEIGHTS[k] * pct_rank(rt[f"{k}_rate"], percentiles[k])
               for k in WEIGHTS)
    return gate * base

def grade_skip(skip_rate) -> str:   # "healthy" | "watch" | "throttled"
    ...
```

**Data shapes:** input is the exact `post["insights"]` dict `refresh.py` already builds (`{views, reach, saved, shares, likes, comments, total_interactions, ...}`). Output is a flat `{rate_name: float}` + a single composite + a skip grade. No schema migration — it reads what's already stored.

### Wiring (smallest blast radius first)

1. **`ig-dashboard/refresh.py`** — add `reels_skip_rate,reposts` to the `REEL_EXTRAS` metric string (line ~207, the existing reels-only insights call) so the new fields land in `post["insights"]` and `post["history"]` on the next run. Then in `write_stats()` (the `stats.md` generator, ~line 331-367): add a **"2026 signal"** block — top posts by `score_2026`, and an explicit skip-rate column / flag on the existing "Top posts by views" list so a high-view post with a throttle-level skip rate is visibly marked. This single change makes the right model visible to *every* skill, because they all read `team/stats.md`.
2. **`reel-analytics` skill** (referenced in CLAUDE.md; the skill that pulls IG perf and closes the Higgsfield loop) — instruct it to compute and report the six rates + skip grade via `metrics2026`, and to frame "what worked" in 2026 terms (hook/skip first) instead of raw likes/views.
3. **`weekly-content-plan` skill** — its "find the arbitrage" step (currently views-per-category) gains a skip-rate lens: prefer categories/formats with low skip + high share rate, not just high views. One added bullet in `SKILL.md` step 3, grounded in the new `stats.md` block.
4. **`dashboard.html`** — add a skip-rate / share-rate column and a "2026 score" sort option (HTML/JS only, reads the same store).

### Future engines inherit the contract for free
- **`viral-scraper` hook_score (not built):** when built, its `hook_score` = the `skip_rate`/share-rate component of `metrics2026` for *own* posts; for discovered/competitor posts it falls back to the views proxy (see Risks — skip rate is own-media only).
- **`audience-sim` (not built):** its qualitative "which hook wins" output should be labeled against the same priority vocabulary (does angle A lower predicted skip / raise predicted shares), so the two-gate funnel speaks one language.
- **`carousel-builder`** already optimizes for SAVES; the module makes explicit that saves are now *priority #4*, so the skill should keep save-optimization but not at the expense of share/skip (matches the source video's exact warning).

---

## Phased build sketch

**Phase 0 — the canonical module (≈1-2 hrs). THE FORCE-MULTIPLIER.**
- Write `ig-dashboard/metrics2026.py`: `rates()`, `score_2026()`, `grade_skip()`, `pct_rank()`, the `WEIGHTS`/threshold constants, a short module docstring citing the source.
- A tiny `if __name__ == "__main__"` self-test over a couple of hand-made dicts (no test framework needed; matches hub style).
- **Done = one importable definition of "good in 2026," unit-checked, zero deps.** Even if nothing else ships, this is the artifact that ends the "what do we sort on" question.

**Phase 1 — pull the new field + surface it (≈half-day). THE VISIBLE WIN.**
- Add `reels_skip_rate,reposts` to `REEL_EXTRAS` in `refresh.py`; confirm one live run populates the fields (skip rate present only on reels with enough plays — handle `None`).
- Add the "2026 signal" block + skip-rate flag to `stats.md` (and the dashboard column).
- Point `reel-analytics` + `weekly-content-plan` skills at the module/`stats.md` block.
- **Done = `stats.md` and the two daily skills reason in 2026 terms, and a high-skip post is visibly flagged even if it has high views.**

**Phase 2 (OPTIONAL) — competitor proxy + future-engine contract (≈half-day).**
- `competitor-radar.py`: keep its views-based breakout rule (skip rate is unavailable for other accounts — see Risks), but add a documented note that competitor ranking is a *reach/views proxy*, not the full 2026 model, so the asymmetry is explicit.
- Document the module as the official `hook_score`/scoring contract in the viral-scraper + audience-sim plans, so they're built against it.
- **Done = one scoring vocabulary across the whole hub, with the own-media vs competitor asymmetry stated honestly.**

**Non-goal:** do not invent a predicted-views *forecast* from these rates. The model ranks *observed* posts and grades hooks; it is not a predictor. (Prediction is the separate, unproven audience-sim track.)

---

## Risks & honest caveats

- **Skip rate is OWN-MEDIA ONLY.** `reels_skip_rate` is on *your* insights endpoint; `business_discovery` returns only `like_count`, `comments_count`, and (for tracked accounts) `view_count` — **no skip/share/save** for other accounts. So the full 2026 model applies to Elijah's posts; competitor-radar must stay on the views proxy. Don't pretend otherwise in the report — label competitor ranks as reach-proxied.
- **`reels_skip_rate` availability is new and not universal.** It populates only on Reels with enough plays, and only for professional/creator accounts; expect `None` on photos, carousels, and very fresh/low-play reels. The module must be None-safe and the gate must degrade gracefully (treat missing skip as neutral, not as a win).
- **The weights are a model, not gospel.** The 0.40/0.25/0.20/0.10/0.05 split encodes the *ordinal* priority from the video; the exact numbers are a reasonable default, not Meta-published. Keep them in one constant so they're tunable, and (ideal) backtest the composite's ranking against Elijah's actual top-by-views posts in the 300-post store before trusting it as a sort — if the composite badly disagrees with what actually went viral, retune before promoting it over views.
- **Don't double-count vs Higgsfield.** Higgsfield's Virality Predictor scores the *rendered edit's* craft (hook strength/retention) pre-publish; this module scores *observed post-publish* signals. They're different artifacts on different sides of publish — keep them distinct, don't merge their scores.
- **ToS / ban risk: none.** This is read-only over the official API with the existing token, computing arithmetic on data the account owns. No scraping, no writes, no new permissions. The new metrics are an official, documented Meta API addition.
- **Low-value scenario to be honest about:** if Elijah never looks at `stats.md`/the dashboard and drives purely off the app's native Insights screen (which already shows skip rate + the retention chart in-app since Aug 2025), the *visibility* value drops. The durable value is then the **contract** for future engines, not the dashboard cosmetics — still worth Phase 0, maybe defer Phase 1's dashboard polish.

---

## Sources

- Vault source (the priority order): `obsidian/Elijah's vault/Research/YouTube summary in the new way to win with Instagram in 2026 content algorithm.md` (Enrico Incarnati).
- **Dec 2025 API change adding `reels_skip_rate` + repost counts (decisive feasibility fact):** https://www.socialmediatoday.com/news/meta-announces-updates-for-the-instagram-marketing-api/807083/ · https://storrito.com/resources/how-instagram-marketing-api-metrics-work/ · https://www.globaldatinginsights.com/featured/meta-expands-instagram-marketing-api-with-big-reels-focus/
- Skip-rate definition + retention chart (Aug 2025 rollout): https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/ · https://metricool.com/instagram-reel-analytics/
- Skip-rate benchmarks (30-40% healthy, >50% throttled; priority order corroborated): https://www.inro.social/blog/instagram-reels-insights
- 2026 algorithm priority (watch time / sends-per-reach / likes-per-reach as top Mosseri-confirmed signals): https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers · https://later.com/blog/how-instagram-algorithm-works/ · https://sproutsocial.com/insights/instagram-algorithm/
- Reels insights API field names (`ig_reels_avg_watch_time`, plays/reach/saves/shares/completion): https://www.getphyllo.com/post/real-time-reels-analytics-using-instagram-reels-api-iv
- `business_discovery` field limits (no skip/save/share for third-party accounts): https://developers.facebook.com/docs/instagram-api/business-discovery · https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/
- Hub code this extends: `ig-dashboard/refresh.py` (already stores views/reach/saved/shares/likes/comments per-post + history; sorts top posts by views), `intel/competitor-radar.py` (views-based breakouts), `intel/trend-radar.py`, `team/stats.md`, `weekly-content-plan` skill, `reel-analytics` skill. Related plans: `docs/plans/2026-06-14-viral-scraper-niche-radar-research.md`, `docs/plans/2026-06-13-audience-sim-pipeline.md`.
