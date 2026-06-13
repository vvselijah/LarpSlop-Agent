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

## How this fits the bigger protocol

| Signal | Source | Status |
|---|---|---|
| Competitor reels w/ view counts, per niche | `competitor-radar.py` (official API) | ✅ live |
| Top ad creatives per niche/keyword | `meta-ads` MCP `ads_library_search` (live-verified) | ✅ live |
| Own-account ground truth | `ig-dashboard/` + `team/stats.md` | ✅ live |
| Trend velocity (what's breaking out) | `trend-radar.py` (Wikipedia + GDELT + HN, keyless) | ✅ live |
| IG hashtag/trending-audio surfaces | Apify IG Hashtag Scraper (free tier) | ⏳ needs Apify account |
| TikTok trends/sounds, YouTube-at-scale | Bright Data MCP (5k free credits) or Apify | ⏳ needs account |

Standout breakouts worth keeping should be saved to the vault as hook notes
(`obsidian/Elijah's vault/20-Content/Hooks/`, `hook` template property block) with
the permalink + why it worked — that's the durable swipe file the bases query.
