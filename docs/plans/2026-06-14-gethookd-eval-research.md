# gethookd.ai teardown + feasibility — what to replicate locally

**Date:** 2026-06-14
**Candidate id:** `gethookd-eval`
**Source flag:** `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md` (line 10: "checkout gethookd")
**Method:** WebSearch + WebFetch (exa/tavily/firecrawl keys are dead). Live pages fetched 2026-06-14.

---

## Verdict: SKIP the product. Borrow ONE small idea (a "performance score" + swipe-file note shape) into the hub we already have.

**Confidence: high.** GetHookd is a **paid-ads competitive-intelligence + ad-creative-generation SaaS for e-commerce/DTC brands** ($29–$129/mo). It is built around the **Meta + TikTok Ad Library** (paid ads), not organic Instagram. Elijah is an **organic IG creator** (@elijahaifl), and the hub **already replicates GetHookd's core mechanics for free, keyless, and tuned to organic content**:

| GetHookd feature | Hub equivalent (already live) |
|---|---|
| "Brand Spy" — track a competitor's ad activity (8 credits/brand) | `intel/competitor-radar.py` — tracks competitors' **organic reels with view counts**, flags breakouts at ≥3× their own median (official `business_discovery` API, keyless) |
| Ad Library access (23M ads, Meta/TikTok/Google) | `meta-ads` MCP `ads_library_search` — Meta Ad Library, **already live-verified** in this hub |
| "Swipe File" (bookmark winning creatives) | Vault `20-Content/Hooks/` notes (`hook` template) — the durable swipe file the Bases query |
| "Performance Score" (1–5 stars) | breakout flag (≥3× median views) in `competitor-radar.py` — **a better, organic-native signal** |
| AI script / hook / variation generation | the existing skill suite: `carousel-builder`, `viral-shortform-2026`, `caption-engine`, Higgsfield MCP |
| Trend signals | `intel/trend-radar.py` (Wikipedia + GDELT + HN velocity) — GetHookd has **no equivalent** |

So ~85% of GetHookd's value is already in the hub, and the missing 15% is the wrong shape for an organic creator. **Do not subscribe. Do not build a clone.** The only worthwhile takeaway is a tiny enhancement described below.

---

## What it actually is

GetHookd.ai (`gethookd.ai`) — marketed as "Facebook Ads Library on steroids" / "Your AI Ad-Scaling Weapon."

**Audience:** solopreneurs, **e-commerce/DTC brands**, marketing teams, agencies. Goal language is all paid-media: "stabilize ROAS," "reduce wasted ad spend," "faster creative testing."

**Data it works with:** **paid ads only**, sourced from the **Meta Ad Library + TikTok + Google** (23M+ ads). It does **not** touch organic IG/TikTok posts. This is the single most important mismatch with Elijah's workflow.

**Feature list (verified from the live site + help docs):**
- **Explore + Filters** — search millions of ads (free).
- **Brand Spy** — monitor a competitor's ad activity, winning creatives, landing pages, traffic sources (8 credits/brand, one-time).
- **Performance Score** — each ad gets a **1–5 star** rating from "multiple performance signals," chiefly **how long the ad has stayed live** (a longevity proxy for ROAS).
- **Swipe File** — bookmark ads from Explore or via a **Chrome extension** (free).
- **Video transcription** — extract ad copy from video creatives.
- **AI script / AI video script generation** — feed it an inspiration ad + your product → hooks/angles/scripts (5 credits).
- **Clone Ads** — generate image-ad variations of a creative (5 credits).
- **Static ad templates** (100+), **funnel/landing-page templates**.
- **Team seats** (1–10), **REST API + MCP server** (paid-plan feature flag).

**Pricing:** Starter $29/mo (50 credits, 1 seat) · Pro $49 (150, 3) · Team $79 (400, 5) · Agency $129 (800, 10). ~35% off annual. Credits gate the AI features.

**Hook scoring / hook library — the headline reason it was flagged — does NOT exist as a distinct feature.** The help docs explicitly have no "hook scoring" or "hook library." The closest thing is the per-**ad** "Performance Score," and that score is **ad-longevity-based**, which has **no organic analog** (an organic reel has no "still running = still profitable" signal). So the thing Elijah hoped to find here isn't actually there.

**It exposes an MCP server** (`https://app.gethookd.ai/api/mcp/v1`, Bearer token, paid-plan only): 7 tools — `search_ads`, `get_ad`, `get_brand`, `search_brands`, `list_brand_spies`, `get_brand_spy`, `get_top_ads`. Clean integration surface — but every tool returns **paid-ad** data the hub can already get from the `meta-ads` MCP for free.

**Reputation:** thin. A handful of Trustpilot reviews, a Toolify listing — early-stage tool, not an established standard. No open-source repo (it's closed SaaS), so there is no README to mine and nothing to self-host.

### Read the source note, not just the link
The vault note that flagged GetHookd lists Elijah's *actual* wants right above the link: (1) "a viral scraper that shows the top best-performing posts of any niche" and lets him iterate, (2) an always-on agent researching the highest-performing **carousels** and educational videos to replicate, (3) full longform build/edit/publish. **None of those are paid-ads use cases** — they're organic-content intelligence + production. The hub's `intel/` engines + `carousel-builder` + `auto-clip` + `weekly-content-plan` already aim at exactly that. GetHookd was a hopeful guess at a tool for those goals; it's the wrong category. The right move is to sharpen the organic engines, not bolt on a DTC ad-spy SaaS.

---

## OSS / approach comparison (2026)

There is **no OSS GetHookd** to adopt — it's closed SaaS. For the one borrowable idea (scoring + swipe-file shape), nothing needs installing:

| Need | Best 2026 approach | License / cost | Weight |
|---|---|---|---|
| Organic competitor "spy" | **Already built:** `competitor-radar.py` (official IG `business_discovery`) | hub code / free | zero new deps |
| Paid-ad library | **Already built:** `meta-ads` MCP `ads_library_search` | official Meta, free | zero |
| "Performance score" for a saved hook | Pure-Python heuristic on data already in hand (views ÷ account median, recency, multi-niche recurrence) | n/a | **stdlib only** |
| Swipe-file storage | Vault `Hooks/` notes (existing `hook` template) | n/a | zero |

No torch, no cv2, no cloud, no new packages. The enhancement is a few dozen lines of arithmetic over JSON the radar already writes.

---

## How the one good idea composes with the hub

GetHookd's genuinely useful concept = **"attach a single comparable score to each saved swipe-file item so you can rank them."** The hub captures breakouts but stores them as prose; it doesn't compute a portable 0–100 "hook strength" you can sort across niches. That's a small, honest upgrade.

**Where it lands:** `intel/competitor-radar.py` (compute) → vault `20-Content/Hooks/` (store) → `niche-intel` / `weekly-content-plan` skills (consume).

**Data shape — add a `hook_score` block to each flagged breakout the radar already emits:**
```jsonc
// per breakout in radar-report.md / data/competitors.json
{
  "permalink": "https://instagram.com/reel/...",
  "username": "competitor_handle",
  "niche": "money",
  "views": 412000,
  "account_median_views": 90000,
  "hook_score": 78,          // 0-100, see formula
  "score_factors": {
    "view_multiple": 4.6,    // views / account median  (dominant term)
    "recency_days": 5,       // newer = slightly hotter
    "cross_niche_recurrence": 1  // same hook pattern seen in N tracked accounts
  }
}
```
**Score formula (transparent, no ML):** normalize `view_multiple` (the radar's existing breakout signal) to 0–100 via a capped log curve, then small additive nudges for recency and for a hook angle recurring across multiple tracked accounts. Deliberately **NOT** GetHookd's ad-longevity score (no organic analog) — it's grounded in Elijah's own ground truth: views relative to the source account's median. This is honestly the *better* metric for his use case.

**Vault write:** when a breakout clears a threshold (e.g. `hook_score ≥ 70`), surface it in `niche-intel` for one-click save as a `Hooks/` note — add `hook_score` to the note body (not a new YAML property; the property contract forbids inventing property names without Elijah's OK). If he later wants it as a sortable Base column, that's a separate, explicit property-contract decision.

**Explicitly do NOT integrate GetHookd's MCP** — it would mean a $29+/mo subscription to fetch paid-ad data the `meta-ads` MCP already returns free, with no organic coverage. Net negative.

---

## Phased build sketch (only if Elijah wants the score; otherwise skip entirely)

- **Phase 0 — decision (5 min):** confirm Elijah wants a numeric hook score at all. If "the breakout flag is enough," **stop here** — no build.
- **Phase 1 — score function (~1–2 hrs):** add `compute_hook_score(breakout)` to `competitor-radar.py`, write `hook_score` + `score_factors` into `data/competitors.json` and `radar-report.md`. Pure stdlib. Follow `dev-workflow` (it's a Python-engine change): write a one-pager plan, verify against the real radar code, run it against the existing data, eyeball that the ranking matches intuition vs the 300-post ground truth.
- **Phase 2 — surface in skills (~1 hr):** have `niche-intel` sort its briefing by `hook_score` and offer top-N for vault save; `weekly-content-plan` reads the same field to prioritize ideas.
- **Phase 3 (optional) — backtest (~half-day):** score Elijah's OWN past reels with the same formula, correlate against actual views in `ig-dashboard` history. If the score doesn't correlate, it's vanity math — cut it. This is the honest gate.

**Rough total effort: 2–4 focused hours** for Phases 1–2; +half-day if backtested. Most of the value is in Phase 1.

---

## Risks / honest caveats

- **Category mismatch (the big one):** GetHookd is a paid-ads DTC tool; Elijah is an organic creator. Subscribing would pay for a Meta Ad Library wrapper the hub already has free, plus generation features the skill suite already covers. **Low value for him specifically.**
- **The flagged "hook scoring" doesn't exist** in GetHookd as imagined — only an ad-longevity "Performance Score" with no organic analog. The replicable idea is *inspired by*, not *copied from*, the product.
- **Score = vanity metric risk:** any single number can mislead. Phase 3 backtest against the 300-post history is the guard; if it doesn't predict, drop it. Don't ship a confident-looking number that isn't grounded.
- **Vault property contract:** do not add a `hook_score` YAML property without Elijah's explicit OK — put it in the note body until then (per `obsidian/Elijah's vault/CLAUDE.md`).
- **Scope creep:** the source note's bigger asks (auto-cloning account, always-on carousel research agent) are much larger projects and are **out of scope here** — this teardown is only about GetHookd. Flag separately if pursued.
- **OneDrive / Windows:** non-issue — stdlib arithmetic, no heavy deps, nothing to keep off the synced disk.

---

## Sources

- [GetHookd — main site ("AI Ad-Scaling Weapon")](https://www.gethookd.ai/main/)
- [GetHookd — "Facebook Ads Library On Steroids" landing](https://www.gethookd.ai/)
- [GetHookd — Features Explained (help docs)](https://gethookdai.crisp.help/en/category/features-explained-7xt942/)
- [GetHookd — MCP Server (7 tools, Bearer token, paid-plan)](https://www.gethookd.ai/mcp/)
- [GetHookd — REST API](https://www.gethookd.ai/api/)
- [GetHookd — for e-commerce brands](https://www.gethookd.ai/main/for-e-commerce-brands/)
- [GetHookd — for agencies](https://www.gethookd.ai/main/for-agencies/)
- [Toolify listing](https://www.toolify.ai/tool/gethookd)
- [Trustpilot reviews](https://www.trustpilot.com/review/www.gethookd.ai)
- Hub source flag: `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md`
- Hub existing capability: `intel/README.md` (`competitor-radar.py`, `trend-radar.py`, `meta-ads` `ads_library_search`)
