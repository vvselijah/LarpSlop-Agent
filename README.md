# AI Agent Team

A single **Claude Code** hub that runs a creator-founder's entire operation — content, Instagram
analytics, paid ads, competitive intelligence, video repurposing, and business ops — on the official
Meta/Instagram MCPs plus a set of local Python engines, custom skills, and a disciplined session workflow.

> **This is the framework**, extracted from a live hub: the engines, skills, docs, and working method.
> Personal data — the owner's Obsidian vault, private analytics, rendered media, and all secrets — is
> intentionally excluded via `.gitignore`. Bring your own credentials (see [Setup](#setup)).

## What it does

- **Knows the numbers.** A self-updating Instagram analytics engine tracks the last 300 posts with
  daily history that outlives Meta's 30-day window, feeding a local dashboard and an auto-generated
  stats file the agent reads before any planning.
- **Watches the field.** Competitive + trend radars pull competitors' reels *with view counts* via the
  official `business_discovery` API (no scraping) and flag rising topics from free, keyless sources.
- **Makes the content.** Skills draft carousels/threads and triage comments (draft → approve → reply,
  never auto-send); a local **auto-clip** engine turns one long video into ranked vertical shorts
  (transcribe → highlight → reframe), feeding a Remotion/HyperFrames editing suite.
- **Plans and remembers.** A file-based context system (profile + memory) and a written-artifact
  discipline (plans, handoffs) carry state across sessions; a context-hygiene rule keeps long sessions sharp.

## What's inside

| Area | What it is |
|---|---|
| **`ig-dashboard/`** | Self-updating IG analytics engine (`refresh.py`) over your last 300 posts + a self-contained local dashboard (`dashboard.html`). Daily history accrues past Meta's 30-day window; token expiry auto-detected. |
| **`intel/`** | Competitive + trend intelligence. `competitor-radar.py` pulls competitors' reels **with view counts** via the official `business_discovery` API (no scraping). `trend-radar.py` is a virality early-warning radar over free, keyless sources (Wikipedia pageviews + GDELT + Hacker News). |
| **`auto-clip/`** | Local long-video → vertical-shorts engine: `transcribe.py` (word-level faster-whisper) → `highlight.py` (LLM moment selector) → `reframe.py` (9:16 cut + encode via FFmpeg). Reuses the editing suite; stops at files and **never auto-publishes**. |
| **`team/`** | The file-based context system — `profile.md` (who the operator is) + `memory.md` (accumulated learnings). `stats.md` is auto-generated from the dashboard (gitignored). |
| **`.claude/skills/`** | Custom skills (below) plus `dev-workflow` & `context-checkpoint` — the working method. |
| **`.claude/workflows/`** | `research-lean.js` — a throttle-safe deep-research workflow (batched verification; see `docs/RESEARCH-PROTOCOL.md`). |
| **`docs/`** | The working method (adapted from [tworkflow](https://github.com/clarity-digital-development/tworkflow)) + research protocol + product/strategy docs + dated capability research + reusable plan/review/QA templates. |
| **Root docs** | `CLAUDE.md` (the hub's operating contract, auto-loaded each session), `HANDOFF.md` (ops state), `AGENT-TEAM-BLUEPRINT.md` & `CONTENT-INTEL-PROTOCOL.md` (researched tool roadmaps). |

## Custom skills

- **`carousel-builder`** — an idea or a proven reel → a saveable IG carousel (+ optional thread), drafted as a vault note. Optimizes for *saves*.
- **`comment-triage`** — triage incoming comments and draft on-brand replies (+ reversible hides) for one-click approval. **Never auto-sends.**
- **`weekly-content-plan`** — a 7-day content plan built from live performance data.
- **`niche-intel`** — a competitor + trend sweep turned into on-brand content ideas.
- **`research`** — routes any research request through the hub's throttle-safe protocol.
- **`dev-workflow` / `context-checkpoint`** — the plan → build → review → QA loop, and the deliberate context-reset discipline.

## Connected capabilities (MCPs)

Wired via `.mcp.json` using env-var placeholders only — **no secrets committed**:

- **Instagram Graph** — insights, comments, media, demographics, publishing *(publishing requires explicit per-action confirmation)*.
- **Meta Ads** — campaigns / ad sets / ads / audiences / insights *(read freely; any write is confirmed first)*.
- **Research** — Exa + Tavily (search) + Firecrawl (deep crawl / JS render).
- **Media & generation** — Higgsfield (image/video/ads + virality predictor), ElevenLabs (TTS/voice), FFmpeg, video analyzers.
- **Control** — Claude-in-Chrome + computer-use, used sparingly and only on public pages.

## Setup

1. **Prereqs:** Python 3.12+, Node 20+ (`npx`), `uv`/`uvx`, git, Claude Code (desktop or CLI), FFmpeg on PATH.
2. **Secrets via OS env vars (never in files):**
   ```
   setx INSTAGRAM_ACCESS_TOKEN "<your IG Graph token>"
   setx INSTAGRAM_ACCOUNT_ID   "<your IG business account id>"
   ```
   Optional (research / media / auto-clip): `EXA_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`,
   `ANTHROPIC_API_KEY` (for `auto-clip/highlight.py`, or run a local Ollama), `ELEVENLABS_API_KEY`, `GEMINI_API_KEY`.
3. **MCP servers** load from `.mcp.json` (env-var placeholders). **Fully quit and relaunch** Claude Code
   after setting env vars — they load only on a fresh process. The Meta Ads connector is added via browser OAuth.
4. **Run the engines:** `python ig-dashboard/refresh.py` · `python intel/competitor-radar.py` ·
   `python intel/trend-radar.py` (or `Daily Agent Refresh.bat` for all three). A daily scheduled task keeps history accruing.
5. **Auto-clip (optional):** `python auto-clip/transcribe.py <video>` → `python auto-clip/highlight.py data/<stem>.transcript.json`
   → `python auto-clip/reframe.py <video> data/<stem>.highlights.json`. Outputs land in `auto-clip/out/`.

## Design principles

- **Official APIs first, scraping last** — most competitive data is reachable via `business_discovery`
  and the Ad Library with zero scraping risk. See `CONTENT-INTEL-PROTOCOL.md`.
- **Human-in-the-loop publishing** — agents draft, create containers, and queue actions; the operator
  makes every final publish/reply/DM click.
- **Secrets only in OS env vars** — this tree is cloud-synced; nothing sensitive touches disk.
- **Context hygiene** — long sessions reset deliberately around 40% (the `context-checkpoint` skill + a hook).
- **Written artifacts over conversation** — plans, handoffs, and memory files carry state across sessions.

## Project status

- **Built & working:** the IG dashboard, the intel radars, the file-based context system, the content/intel
  skills, the throttle-safe research stack, and the **auto-clip foundation** (transcribe → highlight → reframe,
  validated end-to-end on real footage).
- **In progress / R&D:** auto-clip enhancements (face-tracking reframe, fully-automated highlight selection,
  burned-in captions, optional GPU acceleration) and an **audience-sim** experiment — an OASIS-based pre-publish
  reaction predictor that is deliberately proof-first and unproven for Instagram until a backtest validates it.

## Credits

Working method adapted from Tanner Carlson's [tworkflow](https://github.com/clarity-digital-development/tworkflow) (MIT).
Built collaboratively in Claude Code.
