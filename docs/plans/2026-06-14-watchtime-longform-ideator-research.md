---
type: research
domain: content-ops
status: open
date_captured: 2026-06-14
candidate_id: watchtime-longform-ideator
verdict: add-now
build_effort: S (half a day, Phase 0 ~30 min)
tags: [reel-analytics, watch-time, 2026-algorithm, content-plan]
---

# Research — watchtime-longform-ideator

**Candidate:** Mine which content categories earn the longest watch time -> long-form / topic ideas (reel-analytics extension)
**Source:** vault `Brainstorming/In the moment ideas.md` ("use my contact analysis system for Long form ideas"); roadmap STILL-TO-RESEARCH (Content-ops)

---

## Headline verdict: ADD NOW (Phase 0 is ~30 min, pure local Python, zero new deps)

This is the rare candidate where **the hard part is already done**. The data this feature needs —
`ig_reels_avg_watch_time` and `ig_reels_video_view_total_time` — is **already pulled and stored for
all 300 reels** in `ig-dashboard/data/store.json` (verified: 300/300 reels have a non-null
`ig_reels_avg_watch_time`). There is no tool to install, no model to download, no API key, no scraper.
The build is a small pure-Python ranker plus one paragraph of wiring into existing skills.

It is also the single best-aligned candidate to the 2026 algorithm: Mosseri and Meta's own "What
impacts your views" breakdown put **watch time / completion / skip-rate as the #1 Reels ranking
signal** — above shares, saves, likes (sources below). Today `team/stats.md` and the
`weekly-content-plan` skill rank categories by **views**, which is a *downstream* signal. Ranking by
watch-time gives Elijah the *upstream* lever the algorithm actually rewards.

**Honest caveat (don't oversell it):** a *true* completion rate ("% of the video watched") needs the
video's duration, and **Meta does NOT expose `video_duration` on the IG media object** (confirmed
against the official IG Media reference — no `duration`/`length`/`video_duration` field exists, and
there is no clean per-post completion-rate metric in the organic Graph API). So Phase 0 ranks on raw
**avg watch seconds** and a **within-category relative score**, not true % completion. That is still
genuinely actionable. True completion % is a clean Phase 2 add via local `ffprobe` on the
downloadable `media_url` — cheap, but optional. Don't block Phase 0 on it.

---

## What it actually is / does

A reporting layer, not a new engine. It answers: **"Which categories of content hold attention the
longest, consistently — and what long-form / topic directions does that imply?"**

Concretely it computes, per the dashboard's existing `CATEGORIES` taxonomy:
- **avg watch seconds** per category (`ig_reels_avg_watch_time` / 1000, averaged)
- **consistency** — median + spread (so a category isn't crowned on one fluke); the vault note
  literally asks for "watched the longest *every time*", i.e. consistency, not a single peak
- **a watch-time-vs-views gap** — categories that hold attention well but are *under-posted* are the
  arbitrage; categories that get views but low hold are skip-rate risks
- a short ranked list of the **specific top-hold reels** per winning category, as seeds for long-form
  expansion (the "Long form ideas" ask)

I already ran the core computation against live `store.json` to prove it works and is meaningful
(numbers are live as of this research pass):

| Category | n | avg views | avg watch (s) |
|---|---:|---:|---:|
| AI / Tech | 34 | 43,454 | **17.5** |
| Child Safety / PSA | 24 | 48,941 | **14.9** |
| Faith | 12 | 18,467 | 14.6 |
| Founder / Business | 45 | 15,423 | 12.3 |
| Money / Finance | 27 | **168,586** | 11.7 |
| Motivation / Life | 94 | 8,939 | **8.3** |

The read jumps out immediately and is **non-obvious from the views-only view**:
- **AI/Tech and Child Safety hold attention longest** — these are the long-form / deeper-topic bets.
- **Money/Finance prints views but holds worst of the top tier** — great hook, weaker retention; it
  rides reach, not depth. (Matches the known niche: Money/Finance + AI/Tech are his best niches.)
- **Motivation/Life is 94 posts (his most-posted) but dead last on watch-time** — classic
  oversupplied-weak-category. The watch-time lens flags it harder than the views lens does.

That is exactly the "actionable category-level direction" the candidate promises, and it falls out of
data already on disk.

---

## Best 2026 tool / approach + license

**No external tool is the right answer here — and that IS the finding.** I checked the OSS / product
landscape; everything in the "reels analytics" space is either (a) a paid SaaS dashboard
(Socialinsider, Databox, Phyllo, Sociality.io, Metricool) that re-sells the same Graph API numbers the
hub already pulls for free, or (b) a thin Graph-API wrapper. None of them adds signal the hub doesn't
already have. Pulling in any of them would violate the hub's "prefer local scripts + official MCPs
over paid scrapers" rule for zero benefit.

The right approach is **~80 lines of stdlib Python** reading `store.json` (the dashboard's own format)
and emitting Markdown. License: it's our own code. Dependency weight: **zero new deps** (Phase 0 uses
only `json`/`statistics`/`collections` from stdlib). Optional Phase 2 completion-% uses **`ffprobe`**,
which is **already on this machine** (the `auto-clip` / FFmpeg toolchain depends on it) — still no
torch, no cv2, no cloud, no paid anything.

---

## Windows + OneDrive feasibility + dependency weight

**Green across the board.**
- **No heavy imports.** The OneDrive-hang risk in this hub comes from `torch`/`cv2`/big-model loads.
  This feature imports nothing heavier than `statistics`. Safe to run inline, safe under the daily
  scheduled task.
- **Reads local JSON already on the synced disk** — no network call in Phase 0 at all (the data is
  already fetched by `refresh.py`). So it's instant and works offline.
- **No secrets touched.** It consumes data `refresh.py` already wrote; it never sees the token.
- **Optional Phase 2** (`ffprobe` on `media_url` to get duration) does one short-lived subprocess per
  post and a tiny HTTP range read — light, and it's the same subprocess pattern the hub already uses
  for ffmpeg. Cache duration in `store.json` so it's computed once per post, not every run.

Dependency-weight flags requested by the brief: **torch — none. cv2 — none. heavy — none. cloud —
none. paid — none.** This is the lightest possible candidate.

---

## How it composes with the hub (integration sketch)

The hub already has the exact seam for this. Two clean attach points, in priority order:

**1. `team/stats.md` (the auto-fed context file).** `refresh.py::write_stats_md()` already emits a
"Category mix — last 30 days (posts / total views)" block. Add a sibling block
**"Category mix — by watch-time (avg hold seconds, last 30d)"** right below it. This is the
highest-leverage wiring: every skill that reads `stats.md` (`weekly-content-plan`, `niche-intel`, any
session start per CLAUDE.md) instantly gets the watch-time lens for free, with no new invocation.
- Data shape consumed: `store["posts"][*]["insights"]["ig_reels_avg_watch_time"]` (ms),
  `["ig_reels_video_view_total_time"]` (ms), `["views"]`, `["reach"]`, and `["category"]`.
- ~15 lines added inside the existing `write_stats_md` function. No schema change to `store.json`.

**2. The `weekly-content-plan` skill (`.claude/skills/weekly-content-plan/SKILL.md`).** Its Step 3
"Find the arbitrage" currently says *"compare posts-per-category vs views-per-post."* Extend it to also
compare **posts-per-category vs watch-seconds-per-category**, and to treat the watch-time leader as the
long-form / deeper-topic bet. One-line edit to Step 3 plus a sentence in Step 4 about long-form seeds.
No code — the skill just reads the new `stats.md` block.

**Note on the `reel-analytics` skill:** CLAUDE.md and `weekly-content-plan` both *reference* a
`reel-analytics` skill, but **it does not exist on disk** — `.claude/skills/` contains
auto-clip, carousel-builder, comment-triage, context-checkpoint, dev-workflow, niche-intel, research,
weekly-content-plan, and nothing named reel-analytics. So "extend reel-analytics" can't literally mean
editing that skill. Recommended resolution: ship this as a small **`intel/`-style standalone script**
(`ig-dashboard/watchtime_report.py`, matching the `intel/*.py` convention) + the `stats.md` block, and
optionally create the missing `reel-analytics` skill later as a thin wrapper that calls it. **Flag this
gap to Elijah** — a referenced-but-missing skill is its own small bug worth noting.

**Optional deliverable: a vault note.** For a richer one-off, write a dated `type: idea` note to
`obsidian/Elijah's vault/20-Content/Ideas/` ("Watch-time category read — YYYY-MM-DD") with the ranked
table + 3-5 long-form seeds, following the vault property contract (copy the `idea` template block
exactly; `domain: content`, `status: open`). This makes it a saveable artifact `weekly-content-plan`
can wikilink.

---

## Phased build sketch

**Phase 0 — smallest safe thing (~30 min, ship this first).**
Add the "Category mix — by watch-time" block to `write_stats_md()` in `ig-dashboard/refresh.py`:
avg watch seconds + post count per category, sorted by hold, last-30d window (reuse the existing
`recent` list and `views()` helper; add a `watch_s()` helper). Pure stdlib, runs inside the existing
daily refresh. **Definition of done:** next `python ig-dashboard/refresh.py` writes the new block and
the table matches a hand-check against `store.json`. No new files, no new deps, fully reversible.

**Phase 1 — the standalone ranker + skill wiring (~2-3 hr).**
`ig-dashboard/watchtime_report.py`: per-category avg + **median + IQR** (the "consistently" signal),
the watch-vs-views arbitrage gap, and a top-N "highest-hold reels per winning category" list to seed
long-form. Emit Markdown to stdout (and optionally the vault note). Edit `weekly-content-plan` Step 3/4
to consume it. **DoD:** running the script produces a ranked, consistency-aware report;
`weekly-content-plan` references watch-time in its arbitrage step.

**Phase 2 — true completion % (optional, only if Phase 1 proves valuable, ~2-3 hr).**
Since Meta exposes no duration field, derive it locally: `ffprobe` the `media_url` once per post,
cache `duration_s` into `store.json`, then compute `completion ≈ avg_watch_s / duration_s` (clamp
0-1) and a category-level completion rate. This is the metric most tightly coupled to the 2026
skip-rate signal. Gate it on Phase 1 actually changing decisions, and on `media_url`s still being
live (they expire — fetch duration during the same refresh that fetches the post).

**Phase 3 — close the loop (nice-to-have).** Feed the watch-time leaders into the `auto-clip` highlight
brain as a category prior ("favor long-form on AI/Tech / Child Safety"), and surface a watch-time
column in `dashboard.html`. Only if Elijah asks.

---

## Risks / compliance / ToS

- **ToS / ban risk: none.** Uses only official Graph API data the hub is already authorized to pull
  (`get_media_insights`); no scraping, no automation against the IG app, no publishing. It is a
  read-and-report layer that stops at a Markdown table / vault note — fully inside the standing rules
  (no publish/post/DM).
- **Metric-deprecation risk (real, low-effort to absorb):** Meta is migrating "Watch Time / Average
  Watch Time" toward "Minutes Viewed / Average Minutes Viewed" (rounds to the nearest minute) and the
  April-2025 insights deprecation already churned several reel metrics. So `ig_reels_avg_watch_time`
  could be renamed/retired. Mitigation: the feature already reads from `refresh.py`'s cached store, so
  if Meta renames the metric, the fix is one constant in `REEL_EXTRAS` — same place it's pulled today.
  Keep the report defensive (skip posts where the field is null) so a metric change degrades gracefully
  instead of crashing the daily refresh.
- **Small-n categories mislead:** Real Estate (n=1) and Jewelry (n=2) will produce noisy averages.
  Mitigation: require a minimum n (e.g. >=5) before a category gets a "direction" call; show the rest
  as "insufficient data." This is the main *analysis* pitfall, not a technical one.
- **Watch-time != quality of fit for long-form:** a 17s avg hold on a 20s reel is near-complete; a 17s
  hold on a 90s reel is a big drop-off. Without Phase 2 duration, treat Phase 0/1 numbers as *relative*
  category signal, not absolute retention. Say this plainly in the report header so Elijah doesn't
  over-read raw seconds.

---

## Bottom line

Add now. Phase 0 is a ~30-minute, zero-dependency edit to a file the hub already runs daily, and it
upgrades the whole context system from a views-ranked worldview to the watch-time-ranked worldview the
2026 algorithm actually rewards. The data is already on disk; this is almost pure leverage. The only
honest limiter is that true completion % needs a local `ffprobe` pass (Phase 2) because Meta hides
video duration — but the category-level "what holds attention" question, which is what the vault note
actually asked, is answerable today.

---

## Sources

- Meta for Developers — IG Media reference (confirmed: no `video_duration`/duration field):
  https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/
- Databox metric library — Reel Average Watch Time / Total Reel View Time (definitions, returned in ms):
  https://databox.com/metric-library/metrics/instagram-business/reel-average-watch-time-by-reel ·
  https://databox.com/metric-library/metrics/instagram-business/total-reel-view-time-by-reel
- Phyllo — Real-Time Reels Analytics (avg watch time, completion rate = % reaching 95-100% of duration):
  https://www.getphyllo.com/post/real-time-reels-analytics-using-instagram-reels-api-iv
- Emplifi — Instagram Insights Metrics Deprecation (Apr 21 2025) + Views integration / metric churn:
  https://docs.emplifi.io/platform/latest/home/instagram-insights-metrics-deprecation-april-2025
- Dataslayer — Instagram Algorithm 2026, Mosseri's confirmed ranking signals (watch time, sends/reach):
  https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers
- Sprout Social — How the Instagram Algorithm Works [2026] (watch time / completion weighting):
  https://sproutsocial.com/insights/instagram-algorithm/
- Crescitaly — Instagram Reels KPI playbook 2026 (watch / replay metrics, skip-rate framing):
  https://blog.crescitaly.com/instagram-reels-kpi-playbook-2026/
