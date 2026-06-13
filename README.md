# AI Agent Team

A single **Claude Code** hub that consolidates a creator-founder's content, analytics, ads,
competitive intelligence, and business ops — built on the official Meta/Instagram MCPs plus a
set of local Python engines, skills, and a disciplined working method.

> This is the **framework** extracted from a live hub (engines, skills, docs, working method).
> Personal data — the owner's Obsidian vault, private analytics, and media — is intentionally
> excluded via `.gitignore`. Configure it with your own credentials (see Setup).

## What's inside

| Area | What it is |
|---|---|
| **`ig-dashboard/`** | Self-updating Instagram analytics engine (`refresh.py`) over your last 300 posts + a self-contained local dashboard (`dashboard.html`). Daily history accrues past Meta's 30-day window; token expiry auto-detected. |
| **`intel/`** | Competitive + trend intelligence. `competitor-radar.py` pulls competitors' reels **with view counts** via the official `business_discovery` API (no scraping). `trend-radar.py` is a virality early-warning radar over free, keyless sources (Wikipedia pageviews + GDELT + Hacker News). |
| **`team/`** | The file-based context system — `profile.md` (who the operator is) + `memory.md` (accumulated learnings). `stats.md` is auto-generated from the dashboard (gitignored). |
| **`.claude/skills/`** | `weekly-content-plan`, `niche-intel` (content/intel skills) + `dev-workflow` & `context-checkpoint` (the working method). |
| **`.claude/workflows/`** | `research-lean.js` — a throttle-safe deep-research workflow (batched verification; see `docs/RESEARCH-PROTOCOL.md`). |
| **`docs/`** | The working method (adapted from [tworkflow](https://github.com/clarity-digital-development/tworkflow)) + research protocol + product/strategy docs + reusable templates. |
| **Root docs** | `CLAUDE.md` (the hub's operating contract, auto-loaded each session), `HANDOFF.md` (ops state), `AGENT-TEAM-BLUEPRINT.md` & `CONTENT-INTEL-PROTOCOL.md` (researched tool roadmaps). |

## Setup

1. **Prereqs:** Python 3.12+, Node 20+ (`npx`), `uv` (`uvx`), git, Claude Code (desktop/CLI).
2. **Secrets via env vars (never in files):**
   ```
   setx INSTAGRAM_ACCESS_TOKEN "<your 60-day IG Graph token>"
   setx INSTAGRAM_ACCOUNT_ID  "<your IG business account id>"
   ```
   Optional (for the research/media stack): `EXA_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`,
   `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `FAL_KEY`.
3. **MCP servers** load from `.mcp.json` (env-var placeholders only — no secrets committed). Restart
   Claude Code after setting env vars. The Meta Ads connector is added via the app's browser-OAuth.
4. **Run the engines:** `python ig-dashboard/refresh.py` · `python intel/competitor-radar.py` ·
   `python intel/trend-radar.py` (or `Daily Agent Refresh.bat` for all three). A daily scheduled task
   keeps history accruing.

## Design principles

- **Official APIs first, scraping last** — most competitive data is reachable via `business_discovery`
  and the Ad Library with zero scraping risk. See `CONTENT-INTEL-PROTOCOL.md`.
- **Secrets only in OS env vars** — this tree was cloud-synced; nothing sensitive touches disk.
- **Context hygiene** — long sessions reset deliberately at ~40% (the `context-checkpoint` skill + a hook).
- **Written artifacts over conversation** — plans, handoffs, and memory files carry state across sessions.

## Credits

Working method adapted from Tanner Carlson's [tworkflow](https://github.com/clarity-digital-development/tworkflow) (MIT).
Built collaboratively in Claude Code.
