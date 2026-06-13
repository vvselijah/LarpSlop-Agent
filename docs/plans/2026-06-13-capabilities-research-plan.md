# Capabilities research program — what to add to Elijah's local agent hub

*Started 2026-06-13. Goal: research + build the "ultimate local agent team environment" for Elijah
(personal use, not a sellable app). Run focused research ONE workflow at a time (throttle rule —
docs/RESEARCH-PROTOCOL.md), synthesize, then build the winners.*

## Running now
- **Broad capabilities survey** — `research-lean` run **`wf_84437966-a54`** (task `w3bc8kh7f`).
  Surfaces the top 8–12 additions across all 6 areas below. When it lands: synthesize into a tiered
  "add now / add later / skip" list (append to `AGENT-TEAM-BLUEPRINT.md`), then deep-dive the winners.

## ✅ Broad survey RESULTS (wf_84437966-a54, 2026-06-13 — clean run, 6 confirmed findings)

The winners are **local scripts/skills** (highest leverage, ~$0, no platform risk):

1. **Auto-clipping + repurposing pipeline** (LOCAL, TOP PICK) — Faster-Whisper transcript → LLM
   highlight pass → FFmpeg/OpenCV face-track reframe → vertical shorts. MIT bases (SamurAIGPT
   AI-Youtube-Shorts-Generator, OpenShorts, KazKozDev). ~half a day, ~$0 (just an LLM key). Turns
   his podcast/talking-head into daily reels. Plugs into the existing Remotion/HyperFrames suite.
2. **Carousel + thread builder skill** (LOCAL skill) — idea/transcript → hook + body slides +
   caption + thread. Fills the static-format gap. Adapt itchernetski/threads-carousel-claude-skill. ~1–3 hrs.
3. **Local transcription engine** (Faster-Whisper + WhisperX) — podcast/meeting/voice-note →
   diarized, time-coded notes; feeds a daily-briefing on the 7 AM slot. ~1–2 hrs, $0, fully offline.
4. **Comment-mining + sentiment** — Apify "Social Media Sentiment" actor (IG/FB/TikTok comments,
   ~$0.004/comment, vendor infra = zero token risk) + the draft-and-approve **comment-triage skill**
   (works on the instagram MCP today) + official **Notion/Stripe MCPs** for a sponsor/deal pipeline.
- **SKIP (gimmicks):** auto-DM closers, marketplace plugin packs, redundant scrapers, unaudited
  TikTok publisher. Area 3 (ad-creative *generation*) had no new winner beyond existing Higgsfield/Foreplay.

**Open questions (need Elijah) before building:** (a) enough long-form/podcast to justify auto-clipping
first, or mostly short reels (→ carousel skill first)? (b) is speaker diarization (WhisperX) needed or is
single-speaker Faster-Whisper enough? (c) brand-deal volume enough for the Notion MCP, or local CSV for now?

## Queued deep-dives (fire one at a time, fresh session, via `research-lean`)
Each is a focused follow-up once the broad survey names the winners in that area:

1. **Competitor/engagement intelligence + scraping** (Elijah's recurring priority) — exact 2026 toolchain
   to pull OTHER accounts' analytics/engagement/comments at scale: Apify actors vs Bright Data vs
   official `business_discovery`; per-1k costs; comment-sentiment/theme mining; cross-account benchmarking;
   risk to his own token. (Builds on CONTENT-INTEL-PROTOCOL.)
2. **Content repurposing pipeline** — best 2026 local/MCP toolchain for one-long-video → many shorts +
   carousels + threads + captions; auto-clipping (which tools find the viral moments); how it plugs into
   his existing Remotion/HyperFrames suite.
3. **DM/comment management** — the compliant build for his 3–5k DMs/mo: comment-triage skill (works TODAY),
   the Meta App Review path for DMs, knowledge-base auto-draft architecture. (Builds on PRODUCT-VISION.)
4. **Business ops automation** — which of CRM / email-newsletter / scheduling / invoicing / course-platform
   actually have good MCPs or local options worth wiring (re-validate AGENT-TEAM-BLUEPRINT's Metricool/Whop/beehiiv picks).
5. **Personal productivity / knowledge** — meeting+podcast transcription→notes, daily briefing generator,
   capture→vault automation, task automation. Local-first (Whisper, etc.).

## Build pattern
For each confirmed winner: write a PLAN (docs/plans/), build it as a local script or wire the MCP,
test live, document in CLAUDE.md + the blueprint. Prefer local scripts + official MCPs; gate scrapers
behind real need; never auto-publish/DM without per-action confirmation.

## Also parked
- **GitHub repo** — framework committed locally (`f364ef4`, 52 files, clean). Pending: Elijah pastes the
  empty-private-repo URL → push → add Tanner. See the chat / git log.
