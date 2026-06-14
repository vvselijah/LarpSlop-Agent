# Overnight research + build program — 2026-06-14 (autonomous, ~6h)

Elijah is asleep ~6h and asked me to research + plan + (safely) build as many additions to the
**LarpSlop-Agent** hub as possible. **This doc is the resume baton** — if context compacts, continue from
the Wave log + the roadmap doc.

## Operating rules (autonomous — do not violate)
- **Throttle safety:** ONE Workflow at a time, **≤5 concurrent agents** (per `docs/RESEARCH-PROTOCOL.md`).
  exa/tavily/firecrawl keys are DEAD → agents use **WebSearch/WebFetch**. If agents start returning null
  (load-shed), back off — don't relaunch the fan-out; widen the gap between waves.
- **Build only SAFE, reversible, local things** (scripts / skills / plan docs). Verified builds → local
  commits (do NOT push). Everything else stays a PLAN for Elijah.
- **Never:** publish/post/DM, spend money, install multi-GB deps (GPU/torch-cu128, big models), put secrets
  in files, make irreversible vault edits, or anything needing Elijah's decision. Flag those in plans instead.
- Each researched item → a plan doc `docs/plans/2026-06-14-<id>-*.md`. The master roadmap lives at
  `docs/plans/2026-06-14-overnight-roadmap.md` (written/updated by each wave).

## Already covered (don't re-research; deepen only if a wave says so)
- Pocket / voice-capture device → `docs/plans/2026-06-13-pocket-heypocket-research.md`
- 4 vault repos (opendataloader-pdf, ASCILINE, Telegram-Drive, train-llm-from-scratch) → `docs/plans/2026-06-13-vault-repos-research.md`
- auto-clip interview enhancements (LR-ASD, etc.) → `docs/plans/2026-06-14-interview-clip-enhancements-research.md`
- audience-sim (OASIS) → `docs/plans/2026-06-13-audience-sim-pipeline.md`
- Capabilities survey + business-ops/productivity → `docs/plans/2026-06-13-capabilities-research-plan.md`, `...business-ops-productivity-research.md`

## Reusable workflows (re-invoke via Workflow({scriptPath}) — no re-sending)
- **research-batch** (auto-picks next ≤5 un-researched from the roadmap → plan docs → updates roadmap):
  `…\2abf6408-f40c-45f7-b6a6-a1b1e70fb987\workflows\scripts\overnight-research-batch-wf_0443964d-2d1.js`
  Run sequentially (ONE at a time) until the Pick phase returns an empty batch (queue drained).

## Wave log (newest appended by each wave)
- **Wave 1 DONE** (`wf_92db22ab-737`): 45 candidates discovered; 5 researched → viral-scraper-niche-radar,
  always-on-content-research-agent, auto-clone-account, gethookd-eval, longform-builder-pipeline. Roadmap →
  `docs/plans/2026-06-14-overnight-roadmap.md`. Verdicts: NO unconditional add-now; **BUILD-FIRST =
  viral-scraper-niche-radar Phase 1** (rank competitors by VIEWS, not likes); **SKIP** gethookd.ai + literal
  auto-clone. Jump-queued: **ig-2026-algorithm-metric-engine** (current rankings sort on likes = wrong 2026
  signal: skip-rate>share>like>save) + **manychat-alt-dm-responder** (his #1 pain at 100k).
- **BUILD QUEUE:** viral-scraper-niche-radar Phase 1 — do as an ADDITIVE new `intel/` script (don't destabilize
  competitor-radar.py), rank by VIEWS, test live read-only, commit locally. Schedule between research waves.
- **Wave 2 DONE** (`wf_0443964d-2d1`): 5 researched (ig-2026-algorithm-metric-engine, manychat-alt-dm-responder,
  meta-andromeda-ads-playbook, news-update-system, watchtime-longform-ideator). 3 ADD-NOW (ig-metric-engine
  [build-first], watchtime-longform-ideator, news-update-system), 2 ADD-LATER. Correction: refresh.py already
  sorts by views — gap = nobody computes the 2026 RATES. Roadmap updated.
- **BUILD 1 DONE** (`514e7a9`, local, NOT pushed): `ig-dashboard/metrics2026.py` (+292, stdlib, read-only,
  additive). Six 2026 rates/post (share/like/save/repost/comment = metric/reach + skip-rate gate),
  percentile-graded vs his own 300-post distribution, weighted score (share .40/like .25/save .20/repost
  .10/comment .05), CLI `python metrics2026.py [--n]` + `--self-test` (passes). Field reality: likes/comments
  are post top-level (not insights); **skip_rate + reposts are ABSENT from store.json today** → gate degrades
  to neutral. **FOLLOW-UP (Elijah-gated, touches production refresh.py → leave for review):** add
  `reels_skip_rate` + `reposts` to refresh.py so the skip gate + repost_rate activate (Phase 1 of the plan).
- **Wave 3 DONE** (`wf_1205dfb2-ab1`): 5 researched (trial-reel-ab-method [ADD-NOW measure-half],
  dm-routing-va-or-agent, mass-ad-creative-generator, meta-stats-opensource-app, ai-article-broll-creator).
  Mostly ADD-LATER (gated on DMs / ad-spend). Roadmap build order now ~9 items.
- **BUILD 2 DONE** (`9f6a2f4`, local): `ig-dashboard/watchtime_ideator.py` — mines 300 reels for watch-time
  patterns; per-category hold table (median+IQR), arbitrage (lean-in vs skip-risk), long-form seeds reusing
  metrics2026. Report → `ig-dashboard/data/watchtime-ideas.md` (gitignored). Findings: AI/Tech best hold (17.5s),
  Motivation worst (8.3s) despite most-posted; Child Safety+Faith = lean-in; Money/Finance = skip-risk. Noted:
  refresh.py `categorize()` has some mis-tags (future fix; not touched tonight).
- **Wave 4 DONE** (`wf_774b7e8b-957`): 5 researched (clipping-campaign-folder [ADD-NOW ⭐ build #2],
  clipping-agency-research [ADD-NOW decision-doc, no build], artifacial-workshop-ad-ideator [ADD-NOW ⭐ skill],
  proprietary-virality-ml-model [ADD-LATER, honest gate → likely ships nothing], ad-omnipresence-reverse-engineer
  [ADD-LATER, literal idea NOT buildable — no API exposes ad spend]). Roadmap build order ~12 items.
- **BUILD 3 DONE** (`600fe0f`, local): `auto-clip/library.py` (+363) — packaging layer: reads out/ manifests
  (+merges highlights on rank), COPIES clips (originals untouched) into niche-split library + CSV/MD index +
  agency README + idempotent library.manifest.json. `--dest` defaults to outside-OneDrive `C:\Users\elija\clip-library`
  (NOT created tonight). Tested on 6 clips in a throwaway dir (cleaned). README enforces full-res-via-Dropbox, never-chat-media.
- **Wave 5 DONE** (`wf_d939d0fc-697`): 5 researched (live-software-review-format [ADD-NOW skill], saas-for-agents
  [ADD-NOW content-note], abc-wrap-hub-integration [ADD-LATER; finding: skill/MCP suite already shared across both
  repos], fincept-terminal-eval [SKIP — C++/Qt GUI, wrong shape], addyosmani-agent-skills-eval [SKIP — duplicates
  hub dev skills]). ⚠️ **SECURITY (task_6a0761fe):** sibling repo `..\abc wrap\.mcp.json` has a HARDCODED plaintext
  `GEMINI_API_KEY` → Elijah: rotate it + move to env var. Diminishing returns (2 skips).
- **BUILD 4 DONE** (`4ea516d`, local): `intel/viral-radar.py` — competitor viral-post radar over watchlist.json
  via business_discovery (read-only, curl, token off argv). Ranks by VIEWS (eng-rate tiebreak), cross-niche +
  per-niche leaderboards, ×-vs-median, over-performer suggestions. Writes `intel/viral-report.md` + `intel/data/viral.json`.
  **LIVE-TESTED:** 7/8 accounts, 134 posts; top @babylist 1.47M, flagged @gpstephan ~10-25× over-performer. (Built
  the business_discovery path over the plan's hashtag-top_media — more reliable views.)
- **Wave 6 DONE** (`wf_c803187d-5ff`): 5 researched (social-followers-irl-visual [ADD-NOW ⭐ DEADLINE = 100k
  milestone reel, Three.js/HyperFrames — but he's ALREADY ~100k so value decaying + it's creative content needing
  his input → leave as plan], meet-your-cofounder-event-series [ADD-LATER], dropship-ai-character-store [SKIP
  venture], github-spec-kit-eval [SKIP dup of dev-workflow], kajabi-replacement-community-site [SKIP self-built]).
  **RESEARCH ~DRAINED** (3 skips; Content-ops/Video/Infra fully researched). 6 waves = 30 candidates + roadmap.
- **BUILD 5** (launched, subagent): `content-intel-2026` SKILL — ties metrics2026 + watchtime_ideator + viral-radar
  into ONE 2026 content-intelligence briefing (draft-only). Makes the night's 4 engines cohere into a usable workflow.
- **BUILD 5 DONE** (`fd451b8`, local): `.claude/skills/content-intel-2026/SKILL.md` — ties metrics2026 +
  watchtime_ideator + viral-radar into ONE 2026 content briefing (draft-only). All 3 engines smoke-tested OK;
  skill live in the registry.
- **CONSOLIDATING:** research drained (6 waves / 30 candidates), **5 builds shipped + committed**. Wrote
  **`docs/plans/2026-06-14-MORNING-BRIEFING.md`** (the 2-min wake-up summary — START THERE). Next: housekeeping
  commit of all docs; then optional deeper plans / 1 more safe build if time remains.
- **BUILD QUEUE remaining (safe/ADD-NOW):** trial-reel measure-half, viral-scraper-niche-radar, meta-stats OSS
  template. (news-update-system + artifacial-ideator write vault notes → defer to report-output or post-review.)
