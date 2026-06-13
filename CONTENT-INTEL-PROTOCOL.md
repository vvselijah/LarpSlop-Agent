# CONTENT-INTEL-PROTOCOL — competitive intelligence + virality radar

*Synthesized 2026-06-12 from 3 deep-research runs (≈225 agents, ~9.7M tokens) +
live API tests on Elijah's own accounts. Every load-bearing claim was
independently verified (16/16 on the content-intel batch). Items flagged
**[verified]**, **[vendor-claim]**, or **[unverified]** accordingly.*

---

## The mental model: three layers, cheapest first

You almost never need scraping. Most of what you want is reachable through tools
you already own or free public APIs. Scraping is a thin top layer for a few
specific gaps. Build down this list and stop when the signal is covered.

```
LAYER 1  Official APIs you already have       → $0, zero risk, live today
LAYER 2  Free public data (no keys)           → $0, the virality radar
LAYER 3  Cheap scrapers for the few real gaps → ~$0–5/mo, vendor infra (safe)
LAYER 4  Premium (optional)                   → $59–75/mo, only if you outgrow 1–3
```

---

## Per-signal sourcing map (where each thing actually comes from)

| You want… | Source | Layer | Status |
|---|---|---|---|
| Competitor reels w/ **view counts**, per niche | `business_discovery` (official API) | 1 | ✅ **live** — `intel/competitor-radar.py` |
| Top **ad creatives** by niche/keyword | `meta-ads` MCP `ads_library_search` | 1 | ✅ **live** (active ads only — save on sight) |
| Your own performance ground truth | `ig-dashboard/` + `team/stats.md` | 1 | ✅ live |
| **Trend velocity** (what's breaking out) | Wikipedia + GDELT + Hacker News | 2 | ✅ **live** — `intel/trend-radar.py` |
| IG **hashtag / trending-audio** posts | Apify IG Hashtag Scraper | 3 | ⏳ needs free Apify account |
| **TikTok** trends / sounds / top videos | Apify TikTok Trends+Sound, or Bright Data MCP | 3 | ⏳ needs account |
| **YouTube/Shorts** stats at scale | Bright Data MCP `web_data_youtube_videos` | 3 | ⏳ needs account |
| Competitor **follower-growth history** | Social Blade Business API | 3 | ⏳ optional |
| **Video files** for frame analysis | yt-dlp (IG/TikTok), +PO-token plugin (YT) | 3 | ⏳ install when needed |
| 200M **ad swipe-file** w/ niche filters | Foreplay MCP | 4 | optional, $59/mo |

---

## LAYER 1 — already yours (live today)

- **`intel/competitor-radar.py`** [verified live] — pulls any public Business/Creator
  account's last 25 posts **with view counts** via `business_discovery`, flags
  breakouts (≥3× that account's median). Tonight's first run already surfaced
  real winners (e.g. babylist's baby-bath reel at **61.9× its median**). Edit
  `intel/watchlist.json` to choose who to track. Zero scraping, zero risk.
- **`ads_library_search`** [verified] — the Meta Ads MCP returns **all active US
  commercial ads** by keyword/page (a verifier proved it with a Philadelphia-only
  grocer: 24 US ads, 0 EU — so it's not limited to the EU-transparency path the
  public API is). **Caveat: active ads only, no archive** — when you spot a
  winning creative, save the snapshot URL immediately or it's gone on deactivation.

**The boundary [verified]:** the official API gives you others' **views, likes,
comments, captions** — but NOT their reach/saves/shares/watch-time (those need the
owner's token). For deeper competitor data you must go to Layer 3.

---

## LAYER 2 — the virality radar (free, no keys, live today)

**`intel/trend-radar.py`** — detects topics accelerating *before* they peak, using
three keyless sources, on your existing daily scheduler.

| Source | Endpoint | Signal | Cadence |
|---|---|---|---|
| Wikipedia Pageviews [verified] | `wikimedia.org/api/rest_v1/metrics/pageviews/per-article/...` | per-entity daily views (30-day baseline in one call) | daily |
| GDELT DOC 2.0 [verified reachable] | `api.gdeltproject.org/api/v2/doc/doc?mode=timelinevol` | news-mention volume timeline | daily (rate-limit 1 req/5s) |
| Hacker News [verified] | `hacker-news.firebaseio.com/v0/topstories.json` | software/AI front-page velocity | daily |

**The algorithm** (grounded in the burst-detection literature — Kleinberg, and
flu-trends lead-time studies — which warn that *bare fixed thresholds fragment real
trends into noise*):
- **Signal:** today's value vs a **rolling 28-day median** baseline (median+MAD, robust to spikes).
- **Threshold:** ratio ≥ **2.5×** baseline AND above a per-source noise floor.
- **Confirmation (the anti-blip rule):** an alert is **STRONG** only if it's
  *multi-source* (same entity fires on Wikipedia **and** GDELT) **or** *persistent*
  (rising 2+ consecutive days). Single-source one-day pops are labeled **watch**, not alerted.
- **Lead time, realistic [from evidence]:** days—weeks for durable topics (software,
  recurring events); **much shorter for fast pop-culture/news** — the radar's edge there
  is *hours*, which is exactly why it runs daily and why TikTok-sound trends (Layer 3)
  matter for the fastest-moving formats.

**Paid trend upgrades — only if you outgrow free:**
- **SerpApi** [verified] — free tier 250 searches/mo (~8 Google Trends calls/day);
  has *Google Trends* + *Trending Now* + *Autocomplete* endpoints. Paid $25/$75/mo.
  Trigger: when you want Google search-velocity per keyword. (Official Google Trends
  API exists but is **alpha, application-gated, daily-only, 2-day lag** [verified] — not worth chasing.)
- **Glimpse API** [verified] — enterprise/sales-gated, daily granularity → **skip** for a solo operator.

---

## LAYER 3 — scrapers for the real gaps (cheap, and safe)

**The risk question, answered [verified]:** using Apify/Bright Data creates **zero
risk to your Instagram token or account.** Their actors run on *their* infrastructure
with *no Instagram login* — the input schemas have no credential fields. Instagram's
own enforcement page penalizes the *account that scrapes or shares credentials*;
consuming public data a vendor scraped on separate infra is a different thing.
**Meta v. Bright Data (2024) was decided _against_ Meta** — logged-out scraping of
public data doesn't breach its terms. Stay on public data, never feed any scraper
your login, and you're clear. (One caution: privacy statutes still govern *personal*
data downstream — fine for public post metrics, don't build people-databases.)

**Winner — Bright Data MCP** [verified] — one MCP server, plugs into Claude Code,
**5,000 credits/mo FREE, no credit card.** `PRO_MODE=true` unlocks 60+ tools incl.
`web_data_instagram_posts`, `web_data_tiktok_posts`, `web_data_youtube_videos` —
covering TikTok, YouTube-at-scale, and non-business IG accounts in a single install.
Start here; it's the highest-leverage, lowest-friction add.

**Runner-up — Apify actors** (pay-per-result, ~free at your volume) [verified]:
- *Instagram Hashtag Scraper* — `$1.90/1k` (~free under the $5/mo credit at 4 niches × 50 posts).
  Returns likes, comments, plays, captions, **music/audio track**, +10 comments — the
  hashtag + trending-audio gap your official API can't reach.
- *TikTok Trends Scraper* `$1.70/1k` — pulls TikTok **Creative Center** trend data
  (hashtags, songs, creators) without touching logged-in TikTok.
- *TikTok Sound Scraper* `$2–4/1k` — trending-sound mining.

**Follower-growth history — Social Blade Business API** [verified] — credit model
(1 credit = 30 days history; **re-querying a profile is free for 30 days**), so
tracking a fixed competitor set costs ~1 credit/profile/month. Optional.

**Video files — yt-dlp** [verified]: reliable for **Instagram reels & TikTok**.
**YouTube is now hard** — needs Proof-of-Origin tokens per-video; install the
`bgutil-ytdlp-pot-provider` plugin, and even then it's not guaranteed. So: yt-dlp
for IG/TikTok downloads into the frame-by-frame analyzer; treat YouTube as best-effort.

---

## LAYER 4 — premium (only if you scale creative-testing)

- **Foreplay MCP** [verified] — $59/mo Basic, hosted MCP into Claude, 200M-ad
  library with niche/format/duration filters + your own swipe-file boards.
  Trigger: when ad-creative volume justifies a dedicated swipe tool over the free
  `ads_library_search`. Until then, skip.

---

## What NOT to install (already covered / dead ends)

- ❌ A custom **TikTok publisher** — unaudited API = private-only posts (policy wall).
- ❌ **Glimpse** for trends — enterprise-priced, daily-only; SerpApi free tier wins.
- ❌ Generic web-scraper MCPs (Firecrawl/Crawl4AI/Playwright) **for this** — your
  web-fetch + Chrome control already cover article/page reading; Bright Data covers
  the social-data gap. Don't stack redundant scrapers.
- ❌ Meta's **Widely Viewed Content Report** (the quarterly you remembered) — it's
  US-**Facebook-Feed only**, no Instagram, now semiannual. Not useful here.

---

## Recommended weekly cadence

| Cadence | Action | Tool |
|---|---|---|
| **Daily (7 AM, automated)** | own stats refresh + trend-radar sweep | `ig-dashboard` + `trend-radar.py` |
| **2–3×/week** | competitor breakout sweep | `competitor-radar.py` |
| **Weekly** | ad-creative scan per niche; save winners to vault swipe file | `ads_library_search` → `20-Content/Hooks/` |
| **Weekly** | content plan off the above | `weekly-content-plan` skill |
| **When a STRONG trend fires** | ship content *fast* — speed-to-trend is the whole edge | manual + generation stack |

---

## Cost summary for a solo operator

- **Layers 1–2: $0** (official APIs + free keyless data) — covers the majority.
- **Layer 3 starter: $0** (Bright Data 5k free credits + Apify $5 free credit) — covers
  TikTok/YouTube/hashtag gaps at your volume.
- **Optional:** SerpApi $0–25, Social Blade a few $, Foreplay $59 — add only on trigger.

The honest take: **Layers 1–2 are 80% of the value and cost nothing.** Build the habit
on those first; reach for Layer 3 the week you actually feel a specific gap.
