# Cross-niche viral scraper / top-performer radar — build & feasibility research

- **Candidate id:** `viral-scraper-niche-radar`
- **Date:** 2026-06-14
- **Source of the ask:** `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md` (line 2, his #1 recurring ask) + the gethookd.ai reference (line 10)

---

## Verdict: ADD-LATER (build the cheap 80% now as a competitor-radar extension; do NOT build a real scraper)

**One-line:** The valuable, ToS-clean 80% of this — "rank the top organic posts per niche and explain *why* they win" — is a ~half-day extension of the existing `intel/competitor-radar.py` using the official Graph API (`top_media` per hashtag + `business_discovery`) plus Claude-as-analyst for the "why." The remaining 20% he literally wrote ("extract as much real-life data as possible," true view counts on *arbitrary* viral posts) requires a real scraper or a paid API and is **not worth the maintenance/ToS/OneDrive cost** for a single-creator hub. **Build the official-API niche radar; skip the scraper.**

Why not ADD-NOW: it's genuinely useful but not blocking anything, and the existing competitor radar already covers his named competitors. This is an enhancement, not a gap. Slot it after the current auto-clip / caption-engine wiring is finished.

Why not SKIP: it's his stated #1 ask, the cheap version reuses infra that already exists and is already scheduled daily, and it directly feeds the carousel-builder and weekly-content-plan skills. High leverage for low effort.

**Rough effort:** Phase 1 ~half-day (the part worth doing). Phases 2-3 optional, ~1 day each, lower ROI.

---

## What it actually is / what he's asking for

Reading the source note literally, the ask is four stacked things, in descending order of value-per-effort:

1. **"See the top best-performing posts of any specific niche"** — a per-category ranked board of winning posts. (High value, cheap.)
2. **"Why it's succeeding... how to replicate those effects"** — a structured "why it works" teardown (hook, format, length, topic, structure). (High value; this is the part Claude is uniquely good at and no off-the-shelf tool does well.)
3. **"Extract as much real-life data as possible"** — true view/engagement numbers on *arbitrary* viral posts, not just his watchlist. (This is the expensive, ToS-risky 20%.)
4. **"Always-on agent that auto-clones and re-posts"** — out of scope here and against the hub's standing rules (never auto-publish; #1 non-negotiable). The clone-and-iterate creative loop is already served by `carousel-builder` + `auto-clip` + the editing skills, gated on his approval. **Do not build the auto-poster.**

So the buildable candidate = items 1 + 2. Item 3 is the scraper question (answered below). Item 4 is a non-goal.

### The gethookd.ai reference is a red herring for the core ask
gethookd.ai (the YouTube link in his note) is an **ads** intelligence tool: a 23M+ **ad** library (Meta/TikTok/Google ad creatives) with brand-spy, AI script-clone, and swipe files, $29–129/mo. It is about *paid ad creatives*, not organic top posts. The hub **already has the official, free equivalent**: the `meta-ads` MCP exposes `ads_library_search` (the Meta Ad Library) — so the "spy on competitor ads" slice is already covered without paying gethookd. His core recurring ask (organic top posts + why) is a *different* thing that gethookd does not do.

---

## Feasibility: the one finding that decides the design

**The official Instagram Graph API gives you ranking signal for free, but NOT view counts on arbitrary posts.**

| Endpoint | What it returns | Use for this candidate |
|---|---|---|
| `GET {hashtag-id}/top_media` | `id, caption, media_type, like_count, comments_count, permalink, timestamp` — engagement-ranked. **No `view_count` / `plays`.** Cap: **30 unique hashtags / 7 days / account.** | The niche "top posts" board, ranked by likes+comments. ToS-clean, keyless beyond the existing token. |
| `business_discovery.username(...)` | `view_count, like_count, comments_count, caption, permalink, ...` on **known public Business/Creator accounts** | Already used by `competitor-radar.py`. This is the ONLY official way to get real view counts — but only for accounts you name. |
| `{hashtag-id}/recent_media` | same fields, last 24h only | trend freshness, not "top." |

Implications, and they're clean:
- **For his named competitors** → `business_discovery` already gives true views. The radar already does this. ✅
- **For "any niche" discovery** → `top_media` finds the winning posts but ranks by **likes+comments only** (no views). That's an acceptable proxy — high-like/comment posts are the winners — and it's free and ToS-safe.
- **For true view counts on *arbitrary* discovered posts** → not possible officially. Requires a scraper (Apify ~$ per run, or OSS like `instaloader`/TikTok-Api that break often and risk the account) — and the hub's exa/tavily/firecrawl keys are already dead, which is a preview of how brittle scraper dependencies are here. **Recommend: don't.** Use the likes+comments proxy from `top_media` and the real views from `business_discovery` on the auto-promoted accounts.

**The smart hybrid:** use `top_media` to *discover* which accounts keep producing niche winners, auto-suggest the strongest new authors into `watchlist.json`, then let the existing `business_discovery` path pull true views on them next run. Discovery (cheap proxy) feeds tracking (true numbers). No scraper needed.

### Windows + OneDrive + dependency weight
**Trivially safe.** This piggybacks on the exact pattern `competitor-radar.py` already uses: `curl.exe` + stdlib `json`/`statistics`, token from env, writes a markdown report + a small JSON store. **Zero new dependencies. No torch, no cv2, no cloud, no heavy models, no large files on the synced disk.** It runs in the same daily scheduled task. This is the lightest possible addition.

---

## Integration sketch — how it composes with the hub

Extend the existing **`intel/`** engine; do not create a new top-level system.

**New file: `intel/niche-radar.py`** (sibling of competitor-radar.py, same idioms)
- **Input:** a new `intel/niche-hashtags.json`:
  ```json
  {
    "money-finance": { "hashtags": ["personalfinance","sidehustle","investingtips"], "min_engagement": 5000 },
    "ai-tech":       { "hashtags": ["aitools","chatgpttips","aiautomation"],         "min_engagement": 5000 }
  }
  ```
  Budget-aware: total unique hashtags across all niches must stay **≤ 30 / week** (the hard API cap). With a daily run, rotate ~4 hashtags/day or run weekly. Document this in the file's `_readme`, mirroring `watchlist.json`.
- **Step 1 — resolve + rank:** for each hashtag, `GET /ig_hashtag_search` → id, then `top_media` (fields: caption, like_count, comments_count, permalink, timestamp, media_type). Rank within niche by `like_count + W*comments_count` (comments weighted, they're scarcer signal). Emit top N per niche.
- **Step 2 — author promotion (the hybrid):** collect the authoring usernames of the top posts; any account appearing across ≥2 winning posts and not already in `watchlist.json` → write to a `suggested_accounts` block in the report for Elijah to one-click add. This auto-grows the competitor radar's true-view tracking.
- **Step 3 — the "why it works" teardown (the differentiator):** this is **Claude-as-analyst, like auto-clip's `--provider agent`** — no API key, no model. The skill (below) reads the ranked board + captions and produces a structured teardown per top post:
  - `hook` (first line / on-image text intent), `format` (carousel / reel / single), `length_proxy`, `topic`, `structure` (list / story / contrarian / tutorial), `why_it_won` (1-2 sentences), `how_elijah_adapts_it` (tied to his @elijahaifl money/AI niches and his actual `team/stats.md` top performers).
- **Output:** `intel/niche-report.md` (ranked board + teardowns + suggested accounts) and `intel/data/niche.json` (history, so you can later flag *which winners keep winning*). Same write pattern as the other two radars.

**Wiring:**
- Add to **`Daily Agent Refresh.bat`** as the 4th engine (after dashboard + competitor + trend), or run weekly to respect the 30-hashtag cap.
- Surface through a **skill**: extend the existing **`niche-intel`** skill (it already runs competitor + trend + ad-library and synthesizes hooks) to also run niche-radar and fold the teardowns into its briefing. No new skill needed — this slots into the one that already exists for exactly this purpose.
- Downstream consumers already exist: **`carousel-builder`** (turn a proven winner into a carousel) and **`weekly-content-plan`** (reads intel to plan the week). The teardown's `how_elijah_adapts_it` field is the bridge.

**Data shapes** mirror the existing radars (a `{niche: {...}}` config in, a markdown report + JSON history out), so it inherits the same hygiene and the same scheduled-task slot.

---

## Phased build sketch

**Phase 1 — Niche top-posts board + author promotion (~half-day). THE PART WORTH DOING.**
- `intel/niche-hashtags.json` seeded with his real money-finance + ai-tech hashtags, ≤30 unique total.
- `intel/niche-radar.py`: hashtag-search → top_media → rank by weighted engagement → `niche-report.md`.
- Author-promotion block (suggest new accounts into watchlist).
- Reuse competitor-radar's `api()` / token / report idioms verbatim. **Done = a real ranked board for 2 niches with zero new deps.**

**Phase 2 — "Why it works" teardowns (~half-day to a day). THE DIFFERENTIATOR.**
- Add the Claude-as-analyst teardown pass (agent provider pattern from auto-clip).
- Wire into the `niche-intel` skill so the briefing includes per-post teardowns + adaptation ideas grounded in `team/stats.md`.
- **Done = the report explains the wins and proposes Elijah-specific adaptations.**

**Phase 3 (OPTIONAL, lower ROI) — true-view enrichment.**
- ONLY via the existing `business_discovery` on promoted accounts (the hybrid). **Do not add a scraper.**
- If he insists on view counts for arbitrary posts, the honest answer is a paid Apify actor billed per run — evaluate cost-per-value then, don't build it speculatively.

**Non-goal (do NOT build):** the always-on auto-clone-and-repost agent. It violates the hub's #1 standing rule (never publish without per-action confirmation) and the creative-iteration half is already served by carousel-builder / auto-clip under human approval.

---

## Risks & honest caveats

- **No views on hashtag results.** The board ranks by likes+comments. This is a proxy, not ground truth; a high-view/low-like post can be missed. Mitigated by the author-promotion hybrid (true views follow on the next competitor-radar run). Be transparent in the report that hashtag ranks are engagement-proxied.
- **30-hashtag/week cap is real and per-account.** It's the binding constraint on coverage. Rotate hashtags or run weekly; don't let a daily loop burn the budget in 8 days. The existing token is shared with the dashboard + competitor radar — they don't touch hashtag search, so no contention there, but document the budget.
- **`top_media` content quality varies** — it returns globally-popular posts for a hashtag, not necessarily Elijah-sized creators. Filter by a `min_engagement` floor and optionally by account-size band (needs a `business_discovery` follow-up per author = more calls; keep optional).
- **Scraper path is a trap here.** OSS scrapers (instaloader, TikTok-Api, omkarcloud) break on every Meta/TikTok change, risk the account/token, and add brittle deps to a OneDrive-synced tree — the same class of fragility that already killed the exa/tavily/firecrawl keys. The maintenance tax outweighs the value for one creator.
- **Don't pay for gethookd.** Its organic-content value is low for this use case, and its ad-spy value is already covered free by the `meta-ads` MCP's `ads_library_search`.

---

## Sources

- gethookd.ai product (ads-library tool, pricing): https://www.gethookd.ai/
- IG Graph API hashtag `top_media` fields + 30-hashtag/week cap (2026): https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/ , https://zernio.com/blog/instagram-graph-api
- Graph API does NOT expose view counts on third-party / hashtag media (Reels view-count limitation): https://medium.com/@python-javascript-php-html-css/how-to-use-the-graph-api-to-get-instagram-reel-view-counts-f236a7baf9d3 , https://www.getphyllo.com/post/a-complete-guide-to-the-instagram-reels-api
- IG hashtag recent_media edge (official ref): https://developers.facebook.com/docs/instagram-api/reference/hashtag/recent-media
- OSS scraper landscape (fragility context): https://github.com/davidteather/TikTok-Api , https://github.com/omkarcloud/tiktok-scraper , https://github.com/Q-Bukold/TikTok-Content-Scraper
- IG API change/alternative context 2026: https://elfsight.com/blog/instagram-graph-api-changes/ , https://www.netrows.com/blog/best-instagram-data-apis-2026
- Hub infra this extends: `intel/competitor-radar.py` (business_discovery + report pattern), `intel/trend-radar.py`, `intel/watchlist.json`, `niche-intel` skill, `carousel-builder` skill.
