# intel/ — competitive content intelligence + virality radar

The outward-facing twin of `ig-dashboard/` (which tracks Elijah's own account).
Two independent engines, both free and keyless. Full strategy: `../CONTENT-INTEL-PROTOCOL.md`.

## A. Competitor radar — who's winning, and with what

- **`watchlist.json`** — niches → Instagram usernames to track. **Elijah edits this freely.**
  Accounts must be public Business/Creator accounts; bad usernames are flagged in the
  report, not fatal.
- **`competitor-radar.py`** — pulls each watched account via the official
  `business_discovery` API (same token as the dashboard, zero scraping): followers,
  last 25 posts with **view counts**, likes, comments. Flags **breakouts** (≥3× the
  account's own median views and ≥25k views), accrues follower/post history in
  `data/competitors.json`, writes `radar-report.md` grouped by niche.
  Run: `python competitor-radar.py` (~2s per account; trivial vs rate limits).
- **`radar-report.md`** — the latest sweep. Breakouts = formats/topics proven to
  out-perform for that audience — the swipe-file feed.

## B. Trend radar — what's breaking out, before it peaks

- **`trend-watchlist.json`** — per niche: Wikipedia article titles, GDELT news phrases,
  Hacker News keywords. **Elijah edits this freely.** (Wikipedia titles must be EXACT.)
- **`trend-radar.py`** — three keyless sources: Wikipedia daily pageviews (per-entity
  velocity), GDELT news-mention volume, Hacker News front-page velocity. Compares each
  signal to its **28-day rolling median** and fires at ≥2.5× (or z≥3). An alert is
  **STRONG** only if multi-source (Wikipedia + GDELT agree) or persistent (rising 2+
  days) — single-day pops are flagged **watch**, not alerted, so blips don't cry wolf.
  Accrues `data/trend-history.json` (persistence needs ≥2 days). Run: `python trend-radar.py`
  (~3 min; GDELT self-rate-limits to 1 req/5s).
- **`trend-report.md`** — STRONG / watch / Hacker-News sections. When a STRONG trend
  fires in a niche, **ship content fast** — speed-to-trend is the whole edge.

Both are safe to add to the daily 7 AM scheduled task (alongside `ig-dashboard`).

## C. Viral pipeline — what wins, WHY, and who to track next

Three engines that answer "show me the top posts in my niche and how to replicate
them." Run together (in this order) by `Weekly Agent Refresh.bat`:

1. **`niche-radar.py` (DISCOVERY)** — finds top posts in a *niche you don't track
   yet* by scraping hashtags. The official Graph API hashtag endpoints
   (`ig_hashtag_search`/`top_media`) are **App-Review-gated for this app**
   (live-probed 2026-06-29 → `OAuthException #10`), so this is the one engine that
   uses a **scraper** (Apify `instagram-hashtag-scraper`) — which returns **true
   view counts** on arbitrary posts. Config: **`niche-hashtags.json`** (niche →
   bare hashtags + `min_views`; **Elijah edits freely**). Reads `APIFY_TOKEN` from a
   Windows env var (`setx APIFY_TOKEN "…"`); fed to curl over stdin, never on argv.
   Writes `niche-report.md` + `data/niche.json`. **Costs Apify credit** (free tier
   ≈ $5/mo, ~$0.08 per 30-post hashtag) — see the `_budget` block in the config.
   `python niche-radar.py --dry-run` shows the cost with **no API call**; if
   `APIFY_TOKEN` is unset it skips itself cleanly so the rest of the chain still runs.
2. **`viral-radar.py` (TRACKING)** — ranks the winners among the accounts you
   *already* name in `watchlist.json` via the official `business_discovery` (true
   views, no scraper). Writes `viral-report.md` + `data/viral.json`.
3. **`viral_teardown.py` (WHY)** — reads **both** leaderboards above and writes a
   keyless "why it works" teardown card per top post (hook / format / retention /
   replicable angle) to `viral-teardown.md`. `--self-test` runs offline.

**The hybrid loop:** niche-radar discovers winning *new authors* and lists them
under "Suggested watchlist additions"; add the good ones to `watchlist.json` and the
official radars then track them with true numbers next run. All three are read-only
w.r.t. Instagram and never publish.

## How this fits the bigger protocol

| Signal | Source | Status |
|---|---|---|
| Competitor reels w/ view counts, per niche | `competitor-radar.py` (official API) | ✅ live |
| Top ad creatives per niche/keyword | `meta-ads` MCP `ads_library_search` (live-verified) | ✅ live |
| Own-account ground truth | `ig-dashboard/` + `team/stats.md` | ✅ live |
| Trend velocity (what's breaking out) | `trend-radar.py` (Wikipedia + GDELT + HN, keyless) | ✅ live |
| IG hashtag top posts (true views) | `niche-radar.py` (Apify IG Hashtag Scraper) | ✅ built — ⏳ needs `APIFY_TOKEN` |
| TikTok trends/sounds, YouTube-at-scale | Bright Data MCP (5k free credits) or Apify | ⏳ needs account |

Standout breakouts worth keeping should be saved to the vault as hook notes
(`obsidian/Elijah's vault/20-Content/Hooks/`, `hook` template property block) with
the permalink + why it worked — that's the durable swipe file the bases query.
