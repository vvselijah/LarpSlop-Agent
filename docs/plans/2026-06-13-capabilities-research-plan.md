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
6. **Audience-reaction simulation & predictive modeling (NEW — Elijah req 2026-06-13)** — can an agent-based
   social simulation predict how HIS audience reacts to a candidate post/hook BEFORE publishing (feed it
   team/stats.md + reel history + niches)? Compare and pick the best single tool, one of them, or a mix:
   - **camel-ai/OASIS** — https://github.com/camel-ai/oasis — CAMEL's large-scale social-media simulation
     (reportedly up to ~1M persona agents on X/Reddit-like platforms). Strongest a-priori fit for "simulate
     audience reaction to the next post." Q: can personas be seeded from his follower data/niches? compute/cost?
   - **666ghj/BettaFish** — https://github.com/666ghj/BettaFish/blob/main/README-EN.md — (VERIFY) appears to be a
     multi-agent social-media / public-opinion analysis & prediction system. Q: what exactly it predicts, English
     support, deps, maturity, license.
   - **666ghj/MiroFish** — https://github.com/666ghj/MiroFish — (VERIFY) related "Fish" project; how it differs
     from BettaFish and whether it adds anything OASIS/BettaFish don't.
   - Cross-cut: how are OTHERS using these (real use cases + results); how to iterate on their use case for what
     Elijah + Tanner build — pre-publish hook A/B prediction, ad-creative pre-screen ALONGSIDE Higgsfield Virality
     Predictor, audience-segment modeling. OUTPUT: add-now/later/skip per repo + an integration sketch (local
     engine vs MCP; what data feeds it; how it plugs into the dashboard/weekly-content-plan loop).
7. **Composio — agent tool-integration layer (NEW — Elijah req 2026-06-13)** — https://composio.dev /
   https://github.com/composiohq/composio / https://docs.composio.dev/toolkits/github — managed multi-app toolkit
   (250+ apps, managed OAuth) for AI agents. Validity + concrete use case HERE: does it add value OVER the existing
   MCP stack (instagram/meta-ads/elevenlabs/higgsfield/etc.)? Which integrations would actually help (CRM,
   email/newsletter, scheduling, GitHub, Notion, Stripe)? Q: how does its auth/secret model square with the hub's
   secrets-in-env-vars-only + OneDrive-sync constraint? self-host vs cloud? overlap/conflict with current MCPs?
   Was suggested by people Elijah showed the dashboard to. OUTPUT: add-now/later/skip + why + a wiring sketch.
8. **Playwright MCP — browser automation for the AGENT (NEW — Elijah req 2026-06-13, brainstorm)** —
   https://github.com/microsoft/playwright-mcp / https://playwright.dev/docs/getting-started-mcp — lets the agent
   drive a real Chromium via the accessibility tree (navigate/click/read DOM/screenshot). NOT for Elijah's content
   directly; the question is whether it helps the AGENT with research/scraping where no API exists: e.g. checking
   where a competitor's link-in-bio actually redirects, reading public posts/pages behind JS. KEY EVAL: does it add
   value OVER the already-wired Claude-in-Chrome MCP + firecrawl (likely heavy overlap)? And the RISK line —
   browser-scraping LOGGED-IN Instagram/TikTok is against ToS and an account-ban vector (the competitor-intel
   deep-dive already flagged browser automation as banned/risky), so scope any use to PUBLIC, non-logged-in pages
   only (link-destination checks, public web). OUTPUT: add-now/later/skip + the safe-use envelope. Fold into the
   next research pass (post-restart), one workflow at a time.

## Build pattern
For each confirmed winner: write a PLAN (docs/plans/), build it as a local script or wire the MCP,
test live, document in CLAUDE.md + the blueprint. Prefer local scripts + official MCPs; gate scrapers
behind real need; never auto-publish/DM without per-action confirmation.

## Also parked
- **GitHub repo** — framework committed locally (`f364ef4`, 52 files, clean). Pending: Elijah pastes the
  empty-private-repo URL → push → add Tanner. See the chat / git log.

---

# DEEP-DIVE RESULTS — Workflow 1 (`wf_646cdd8c-80a`, 2026-06-13, clean run, 6 agents/520k tok)

Throttle-safe run (max ~6 concurrent, 3 web). Three recon + three research agents. This section is the
**build spec** the next session implements. Confidence on all three research deep-dives: **high**.

## ⚠️ Infra flag found mid-run — research stack keys not loaded (simple fix)
Exa/Tavily/Firecrawl all **401'd** (agents fell back to WebFetch and delivered anyway). Diagnosed:
the three keys ARE set at User level with valid prefixes (`EXA=2f18…` len36, `TAVILY=tvly…` len57,
`FIRECRAWL=fc-8…` len35) but are **absent from the running Claude process** (Process len=0), while the
INSTAGRAM vars ARE in-process. → This session launched before those keys were in the env → MCP servers
got empty keys → 401. **FIX: full quit + relaunch Claude Code** (NOT `/clear` — that keeps the same
process). Classic "env vars load only on full restart" landmine. Keys themselves look valid; do not rotate.

## Build A — comment-triage skill (`.claude/skills/comment-triage/`)
- **Works TODAY** on owned account / app-role testers: read + reply + hide + delete comments via the
  `instagram` MCP (`get_comments`/`reply_to_comment`/`hide_comment`/`delete_comment`). Perm:
  `instagram_business_manage_comments`. Limits are generous (750 private-replies/hr).
- **Architecture:** inbound → classify (FAQ/lead/spam/needs-human) → KB auto-draft → **review queue
  (status=draft)** → Elijah one-click → API send. **Nothing leaves draft without his click** (CLAUDE.md rule 1).
  Prefer **hide (reversible)** over delete (irreversible) for spam.
- **DM caveat:** `send_dm` only works inside the **24h reactive window** the user opens; outside it fails.
  Acting on **real followers** (non-app-role) at scale needs **Advanced Access via Meta App Review** — error
  `#3` = the app is on Standard Access. Build comment-only v1 now; DM + App Review is a separate track.
- **OPEN (Elijah/verify):** does @elijahaifl's Meta app already hold Advanced or only Standard access?
  (App Dashboard → App Review → Permissions & Features.) Is the MCP on IG-Login or FB-Login scopes?

## Build B — carousel/thread builder skill (`.claude/skills/carousel-builder/`)
- **Highest-leverage now:** he runs **zero carousels** today = untested upside; carousels/saves are the gap.
- **Optimize for SAVES first, shares second.** His live save-rate peaks (~3.6%) on **AI/Tech utility**;
  **Money/Finance** is his runaway view-leader (~207k views/post, ~25× Motivation). Repurpose a proven
  Money/Finance or AI/Tech reel → multi-slide save-able reference; strong hook on slide 1.
- Read `team/profile.md` (voice) + `team/stats.md`; output as a vault note using the exact `_templates/`
  property block (vault property contract is law); **never auto-publish** (`publish_carousel` gated on his OK).

## Build C — auto-clipping pipeline (`auto-clip/` engine + `.claude/skills/auto-clip/`) — write a PLAN first
**~70% already exists** across the hub + sibling `..\abc wrap\`. **Reuse, don't rebuild.** Build ONLY 3 new pieces:
1. **Local-transcribe wrapper** — `faster-whisper` (1.2.1 already installed) `word_timestamps=True` → flat
   `[{text,start,end}]` JSON (matches existing comps). Generalize the existing hub-root `transcribe.py`.
2. **Highlight/moment selector (the true missing brain)** — LLM pass over the transcript → ranked
   `{start,end,title,hook,score,reason}`; pre-filter with the sibling's proven `build_cutlist.js` boundary logic.
3. **Face/subject-aware 9:16 auto-reframe** — OpenCV/MediaPipe face track → smoothed crop track → feed the
   EXISTING `PodcastEdit.tsx` transform (1.35× softness cap + black-edge clamp). v2: KazKozDev YOLOv11+ByteTrack.
- **Reuse:** local Whisper, `build_cutlist.js` (editorial brain), `PodcastEdit.tsx` (crop comp), caption-engine,
  broll-inserter, platform-exporter, FFmpeg 8.1 MCP (NVENC/CUDA/`--enable-whisper`) for probe+audio.
- **9:16 crop must be a direct FFmpeg CLI filtergraph** (`crop=/scale=/pad=`) — the MCP `resize-video` is
  fixed-preset and CANNOT reframe. Prefer a **pure-FFmpeg render path** to avoid Remotion's ~10GB/bundle disk
  blowup (documented in the sibling's INTERVIEW-HANDOFF). Engine **stops at files in `out/`** — never publishes.
- **GPU FIX (highest-leverage):** RTX 5070 (Blackwell sm_120) present but torch is the **+cpu** build →
  faster-whisper is CPU-only. Reinstall `torch --index-url https://download.pytorch.org/whl/cu128` + cuDNN9/CUDA12
  DLLs on PATH → near-instant transcribe + `h264_nvenc` encodes. (Needs a multi-GB download — confirm with Elijah.)
- **First engine to need third-party deps** (every existing engine is stdlib-only) → call out a `requirements.txt`
  convention in the PLAN. Engine folder mirrors `ig-dashboard/`/`intel/` (entry `.py` + `data/` + `README.md`),
  chained later into `Daily Agent Refresh.bat` (on-demand first).

## Research — competitor/engagement intelligence (two-layer; ADD NOW)
- **Layer 1 (FREE, zero token risk):** official IG Graph **`business_discovery`** — already wired
  (`mcp__instagram__business_discovery`). Returns competitor follower_count, media_count, per-post
  like/comment/**view** counts on HIS existing token. Limits: public Business/Creator targets only;
  **counts not comment TEXT**; no competitor demographics; 4,800×impressions/24h (huge headroom).
- **Layer 2 (cheap, NEVER touches his token):** **Apify pay-per-result** actors (scrape via their own
  proxies). IG `$1.50/1k` posts, `$2.30/1k` comments; TikTok `$0.30–1.70/1k`; YouTube comments `$0.90/1k`.
  Fills the comment-TEXT + TikTok/YT gaps. **Bright Data = SKIP** ($250 min / $499/mo — enterprise overkill).
- **Sentiment/themes:** no scraper does it well — pull raw comments cheap, cluster + score **in-house with Claude**.
- **OPEN (Elijah):** comment TEXT (→Apify) or just engagement COUNTS (→business_discovery, $0)? Recurring
  volume (accounts × posts/comments per week) to size Apify spend? Wire an IG competitor pull into `intel/`?

## Research — repurposing / auto-clipping toolchain (verdicts)
- **add-now:** `faster-whisper` (best Windows transcriber, word ts), **SamurAIGPT local mode** (MIT reference
  pipeline — route ranking to Claude/Ollama, ignore paid MuAPI), **OpenCV+MediaPipe** crop (reframe v1).
- **add-later:** `WhisperX` (diarization for 2-speaker podcasts; GPU+HF token), **KazKozDev** auto-vertical-reframe
  (AutoFlip successor, YOLOv11+ByteTrack — Windows untested), `ClipsAI` (boundaries only, needs LLM scorer),
  `Ollama-Clip-Anything` (fully-local multi-agent — mine for prompts).
- **skip:** `OpenShorts` (Docker + mandatory cloud keys), `ClippedAI` (CC BY-NC non-commercial), `whisper.cpp`
  as primary (Windows friction — keep only as zero-Python fallback).

## Research — DM/comment compliance (the rules that gate scale)
- **Comments:** read/reply/hide work today (perm above). **DMs:** 24h reactive window only; **200
  business-initiated msgs/hr**, 2 calls/sec (Meta cut from 5,000 in Oct 2024) — fine reactive, no blasting.
- **Error #3 = Standard Access.** Production on real followers needs **Advanced Access via App Review**:
  Business Verification + per-permission screencasts + privacy policy + data-deletion + **webhook handler for
  message-deletion** + opt-out; ~2–4 weeks. Start Business Verification early (it's the slow gate).
- **HUMAN_AGENT tag (7-day window) = SKIP for automation** — must be human-applied or Meta revokes API access.
- **Triage = webhook-driven** (`comments`/`live_comments`/`messages` fields), not polling (saves the ~200 reads/hr).
- **OPEN (Elijah):** hosted HTTPS webhook endpoint for v1, or polling to start? Business Verification done yet?

## Build order (locked by content mix: short-form-dominant, ramping long-form)
1. **carousel-builder** (leverage now) · 2. **comment-triage** (works today, comment-only v1) ·
3. **auto-clip PLAN + scaffold** (strategic for the long-form/podcast push; GPU fix gates speed).
Then: add-now intel layer (`business_discovery` recurring + optional Apify), housekeeping (repoint task), save-back.
