# Always-on content research agent — build/feasibility research

**Candidate id:** `always-on-content-research-agent`
**Date:** 2026-06-14
**Source:** `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md` (the "always on agent... constant research on the highest performing carousels and non-personal videos to automatically replicate... and using the agent to make the video/script/editing better" item). The note links [gethookd.ai](https://www.gethookd.ai/).

---

## Verdict: ADD-LATER (build the thin orchestration layer; do NOT buy a tool or build a scraper)

**Confidence: high.** This is **not a new tool** — it is a scheduled wrapper around engines the hub already owns. ~80% of the candidate already exists as separate, tested parts: `intel/competitor-radar.py` (the data feed), the `niche-intel` skill (intel→ideas), and the `carousel-builder` skill (idea/proven-reel→draft). The genuinely missing 20% is (a) a **scheduled, autonomous** run that chains those three and writes drafts to the vault unattended, and (b) closing one **data gap** (image carousels are largely invisible to the official API for *other* accounts).

It is **add-later not add-now** for one honest reason: the "carousel" half of the request has a hard ceiling on the free/official data path (see Risk 1), and the existing on-demand `niche-intel` skill already delivers 90% of the daily value with zero new code. Build the scheduled loop only once Elijah confirms he'll actually consume a daily auto-draft (otherwise it just generates vault clutter he ignores).

**Do NOT** adopt GetHookd or any scraper SaaS for this — see "What it is" and Risk 1.

---

## What it actually is / does

Elijah's ask, decomposed:

1. **Continuously surface** the highest-performing carousels + educational/non-personal videos per niche (Money/Finance, AI/Tech are his proven winners).
2. **Auto-draft a better iteration** — script + slide deck + edit plan — that keeps the winning structure but improves on it.
3. Run it **on a schedule** ("always-on"), not on demand.

This is a classic **intel → idea → draft loop**. The "always-on agent" framing is the only new requirement; the loop itself is content-intel work the hub already does.

### The linked tool (gethookd.ai) is the wrong target
GetHookd is a **paid e-commerce *ad* intelligence SaaS** ($29–$129/mo): 23M+ Facebook/TikTok/Google **ads**, "Brand Spy" on competitor ad creatives, AI ad-script generation, "Clone Ads." It is closed-source, ad-focused (not organic carousels/educational reels), and overlaps with capability the hub **already has free** via the `meta-ads` MCP `ads_library_search`. It is not a fit and not adoptable (no API/OSS). Skip it.

### The OSS / 2026 landscape (for reference, also skip)
The market has shifted to all-in-one SaaS "autonomous content agents" (Virale, ReelMind, PostEverywhere) that research a niche then draft+schedule. None are OSS in a way that helps here, all are cloud-paid, and all would *replace* the hub's own (free, official-API, vault-integrated) stack rather than compose with it. The one genuinely relevant 2026 primitive is **Claude Code's own scheduling**: as of June 2026 Claude Code supports **Routines / scheduled cloud agents** and **headless `-p` mode**, so "an agent on a cron" is now a native capability, not something to buy. ([Anthropic managed-agent cron beta](https://www.techtimes.com/articles/318163/20260610/claude-managed-agents-add-cron-schedules-credential-vaultsanthropic-beta-puts-agents-autopilot.htm), [Claude Code scheduled tasks guide](https://claudefa.st/blog/guide/development/scheduled-tasks))

**Bottom line:** the correct build is *internal glue*, not a procurement.

---

## Windows + OneDrive feasibility + dependency weight

**Excellent — zero new heavy deps.** Everything this needs is already proven on Elijah's machine:

- `intel/competitor-radar.py` and `trend-radar.py` are **pure stdlib + `curl.exe`** (no torch/cv2/cloud). Already run on the OneDrive disk fine.
- The draft step is **Claude reasoning + vault file writes** — no model download, no GPU.
- Scheduling reuses the **existing Windows Task Scheduler** entry (`Daily Agent Refresh.bat`, 7 AM) that already chains the three radars. The new step is one more line in that `.bat` (or a headless `claude -p` call).
- No new secrets: reuses `INSTAGRAM_ACCESS_TOKEN` (already an env var). Honors the OneDrive/secrets rules unchanged.

The **only** weight risk is if "find top carousels" pushes toward a scraper (Apify/Bright Data IG scrapers) to get carousel save/reach data the official API won't give — that's a paid cloud dep and an account-trust/ToS risk. The plan below explicitly *avoids* that for v1.

---

## How it composes with the hub (integration sketch)

The loop reuses existing engines end to end. Nothing here is new infrastructure — it's a chain.

```
[Windows Task Scheduler 7AM]  →  Daily Agent Refresh.bat
        │  (existing chain: dashboard + competitor-radar + trend-radar)
        ▼
  intel/radar-report.md     ← breakouts: per-niche reels ≥3× account median, ≥25k views
  intel/trend-report.md     ← STRONG/watch trend velocity
  team/stats.md             ← Elijah's own ground truth (which niches reward him)
        │
        ▼  NEW STEP: headless `claude -p` (or a niche-intel scheduled variant)
  ┌─────────────────────────────────────────────────────────────┐
  │ research-agent run:                                          │
  │  1. read the 3 reports above (no new fetching needed)        │
  │  2. rank breakouts × trend-match × his-niche-fit            │
  │  3. for the top 1–3 winners, call the DRAFT path:           │
  │       - reel winner   → auto-clip plan / script rewrite      │
  │       - carousel/edu  → carousel-builder draft (slides+caption)│
  │  4. write drafts as vault `idea` notes (idea.md contract)    │
  │  5. append 1 learning to team/memory.md                      │
  └─────────────────────────────────────────────────────────────┘
        │
        ▼
  obsidian/Elijah's vault/20-Content/Ideas/*.md   ← Elijah reviews; nothing auto-posts
```

**Engines/skills it wires together (all already built):**

| Step | Reuses | Data shape |
|---|---|---|
| Discover winners | `intel/competitor-radar.py` → `radar-report.md` | per-post: `view_count, like_count, comments_count, caption, permalink, timestamp` |
| Trend overlay | `intel/trend-radar.py` → `trend-report.md` | STRONG/watch alerts per niche |
| Own-data filter | `team/stats.md` | category mix + top posts |
| Rank + synthesize | `niche-intel` skill logic | 5–10 ranked ideas w/ source signal |
| Draft a carousel | `carousel-builder` skill | vault `idea` note (`type: idea, domain: content, stage: raw, status: open`) |
| Draft a clip/script | `auto-clip` skill (if a long video is the source) | `out/` clips + script |
| Schedule | `Daily Agent Refresh.bat` + Task Scheduler / Claude Routines | one extra step |

**Critical design constraint — it stops at drafts.** Standing rule 1 (never publish without per-action confirmation) means the "automatically replicate **and post**" part of Elijah's ask is **off the table**. The agent produces vault `idea`/`hook` notes and clip files only; Elijah does the publish click. This must be stated up front so the feature isn't mis-scoped as an autoposter.

---

## Phased build sketch

**Phase 0 — decide it's wanted (no code).** Run the existing `niche-intel` skill on demand for a week. If Elijah actually acts on its ideas, proceed. If he ignores the output, an *always-on* version just makes more ignored output — stop here. (This is the cheap gate that justifies add-*later*.)

**Phase 1 — the scheduled loop (the actual build, ~half-day).**
- Add a `content-research-agent` skill (or a `--scheduled` mode of `niche-intel`) that reads the three already-generated reports, ranks, and writes the **top 1–3** ideas as vault `idea` notes via the `carousel-builder` draft path. No new fetching — it consumes the radars' output.
- Wire one line into `Daily Agent Refresh.bat` *after* the radars, as a headless `claude -p "run content-research-agent"` step (or a Claude Routine on the cloud per the June 2026 beta).
- Dedupe: skip a topic if a matching `idea` note already exists (use the source permalink as the key, mirroring how `competitor-radar` tracks `posts` by id).
- Output cap: max 1–3 drafts/day to avoid vault clutter.

**Phase 2 — close the carousel data gap (only if Phase 1 proves valuable, ~half-day + a decision).**
- The official API gives competitors' reel `view_count` but **not** carousel saves/reach. Options, cheapest first:
  - (a) Accept the limit: rank competitor *carousels* by likes+comments only (available via `business_discovery`), and lean on his *own* saved-rate data for format quality. **Free, recommended.**
  - (b) Add the `meta-ads` `ads_library_search` signal for any niche where competitors run paid static/carousel ads (already wired, free).
  - (c) Only if (a)+(b) prove insufficient: a free-tier Apify "IG Hashtag/Profile Scraper" pass (already flagged as ⏳ in `CONTENT-INTEL-PROTOCOL.md` / `intel/README.md`). Paid/ToS risk — Elijah-gated.

**Phase 3 — "make the edit better" loop (optional, later).** For a chosen winner that's a video, chain `auto-clip` (already live) + `caption-engine` to produce the improved edit, not just the script. This is the most speculative half and should wait until the draft loop earns its keep.

---

## Risks / honest assessment

1. **The carousel half has a hard data ceiling (biggest issue).** `business_discovery` exposes other accounts' reel `view_count`, but **saves and reach — the metrics that actually define a winning carousel — are owner-only** and not returned for competitors. So "continuously find the top *carousels*" can only rank by likes/comments on the free path, which is a weak proxy for save-driven carousel success. The *reel/educational-video* half works great (view counts are real); the *carousel* half is structurally limited unless he pays for a scraper. Be upfront: v1 nails reels, approximates carousels.
2. **"Automatically replicate and post" is blocked by design.** Standing rule 1. This is a *draft* generator, full stop. If the underlying desire is true hands-off autoposting, the answer is "no, and that's deliberate."
3. **Clutter / value risk.** An always-on drafter that writes notes he never opens is negative value. Phase 0 gate exists precisely to avoid this. The on-demand `niche-intel` skill may simply be the right altitude — "always-on" might be a solution looking for a problem.
4. **Replication = sameness risk.** Auto-iterating on competitor winners trends toward derivative "larp slop" (cf. the project name). The draft must run through `team/profile.md` voice + add a genuine angle, not just reskin the source. Quality is on the prompt, not the pipeline.
5. **GetHookd / SaaS temptation.** Buying a tool here would duplicate free hub capability, add a subscription, and pull data *out* of the vault-integrated workflow. Net-negative; documented so it isn't re-litigated.

**Rough effort:** Phase 1 (the real value) is **~half a day** of glue + one `.bat` line, because every dependency already exists and is tested. Phases 2–3 are optional follow-ups, each ~half a day, gated on Phase 1 proving useful.

---

## Sources

- Candidate source note: `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md`
- [GetHookd.ai](https://www.gethookd.ai/) — the tool linked in the note (paid e-commerce ad-intel SaaS; not a fit)
- [Instagram Graph API developer guide 2026 (Elfsight)](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/) — business_discovery + insights scope
- [Meta new IG API analytics features (Social Samosa)](https://www.socialsamosa.com/news-2/meta-instagram-api-features-branded-content-analytics-11760299) — saved/shares now on owner Media endpoint
- [Anthropic managed-agent cron + headless beta (TechTimes, Jun 2026)](https://www.techtimes.com/articles/318163/20260610/claude-managed-agents-add-cron-schedules-credential-vaultsanthropic-beta-puts-agents-autopilot.htm) — native scheduling primitive
- [Claude Code scheduled tasks guide (claudefa.st)](https://claudefa.st/blog/guide/development/scheduled-tasks) — `-p` headless + cron pattern
- [Jotform: best Instagram AI tools 2026](https://www.jotform.com/ai/agents/instagram-ai-tools/) and [PostEverywhere: 35 AI tools for IG](https://posteverywhere.ai/blog/35-best-ai-tools-for-instagram) — the autonomous-content-agent SaaS landscape (all cloud-paid, non-composing)
- Existing hub parts this reuses: `intel/competitor-radar.py`, `intel/trend-radar.py`, `intel/README.md`, `.claude/skills/niche-intel/SKILL.md`, `.claude/skills/carousel-builder/SKILL.md`, `Daily Agent Refresh.bat`, `CONTENT-INTEL-PROTOCOL.md`
