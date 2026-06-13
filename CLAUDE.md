# CLAUDE.md — Elijah's AI Agent Team hub (workspace root)

This folder is the single hub that consolidates Elijah's content, analytics, ads,
and business ops into Claude Code. Read this first; it routes you everywhere else.

## Read-first map

| When you're doing… | Read / use |
|---|---|
| Anything (session start) | This file. Ops state + history: `HANDOFF.md` |
| Content or business planning | `team/profile.md` (who he is) + `team/stats.md` (live numbers, auto-fed daily) + `team/memory.md` (accumulated learnings) |
| Vault note work | `obsidian/Elijah's vault/CLAUDE.md` — the property contract is law |
| Adding tools/MCPs/automations | `AGENT-TEAM-BLUEPRINT.md` — researched tier list, don't re-litigate |
| IG performance questions | `reel-analytics` skill or `ig-dashboard/` (refresh via `Open Dashboard.bat`) |
| Competitor / trend research | `intel/` (`competitor-radar.py`, `trend-radar.py`) + `CONTENT-INTEL-PROTOCOL.md` |
| Building/changing a Python engine, or any long session | `docs/` — working method (`dev-workflow` + `context-checkpoint` skills); see "Working method" below |
| ANY research task | `docs/RESEARCH-PROTOCOL.md` — try direct WebFetch/API first; use `research-lean` workflow (not the throttle-prone `deep-research`) for surveys; one workflow at a time |

## Standing rules (non-negotiable)

1. **Never publish, post, comment, or DM on any platform without explicit per-action confirmation from Elijah.** Drafts and container-creation are fine; the final publish click is his.
2. **Meta Ads:** read/report freely; confirm before ANY write (create, edit, pause, budget).
3. **Secrets:** only in Windows user env vars via `setx` — never in files; this whole tree syncs to OneDrive. (Current vars: `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_ACCOUNT_ID`.)
4. **IG API publishing:** voice-only / original-audio reels only (API-published reels can't use licensed/trending audio). Pre-flight with `get_content_publishing_limit` before bulk publishing.
5. **Vault:** follow its property contract exactly; never invent property names; templates in `_templates/` are the schema.
6. **`here/`** is a personal space with its own charter (`here/about.md`) — read it on visits, never tidy it.
7. After a planning run or experiment, append one dated learning to `team/memory.md`.

## Working method (Tanner's `tworkflow`, applied where valid)

Adapted from https://github.com/clarity-digital-development/tworkflow → lives in `docs/`
(skills in `.claude/skills/`). **Apply it where it fits this hub; don't over-apply it.**

- **Context hygiene — the 40% rule (applies to EVERY session here).** This hub's sessions run long
  and heavy, and its whole continuity is session handoffs. When context passes ~40%, reset deliberately
  at the next clean boundary (a finished step / delivered report) — don't wait for auto-compact. The
  `context-checkpoint` skill measures real usage and walks the compact-vs-clear call; a hook in
  `.claude/settings.json` auto-nudges at 40%. **Before any `/clear` or `/compact`, write the baton note**
  (`docs/templates/SESSION-HANDOFF.md`) — that's separate from, and feeds, the master `HANDOFF.md`.
- **`dev-workflow` (Plan→Implement→Review→QA→Ship→Retro) — for CODE changes only.** Use the full loop
  when changing the Python engines (`ig-dashboard/refresh.py`, `intel/*.py`) or `dashboard.html`:
  write a `docs/plans/<date>-<slug>.md` from the PLAN template, verify premises against the real code,
  then the three review lenses + QA. **Lighter touch for docs / content / vault edits** — those are
  not the dev loop's target; a one-line plan inline is enough.
- **Honest scope:** this hub isn't under git yet, so the loop's commit/branch/PR mechanics are
  aspirational — the discipline (written plan, separate review passes, evidence-before-"done",
  handoff-before-reset) applies regardless. Full rationale + caveats: `docs/README.md`.

## Capability quick-map (all already installed — don't re-add)

- **IG data + publishing:** `instagram` MCP (insights, comments, publish, DMs) + `ig-dashboard/` (300 posts, daily history)
- **Ads:** `meta-ads` MCP (official, OAuth-managed)
- **Video editing:** Remotion/HyperFrames skill suite (`edit-video`, `caption-engine`, `broll-inserter`, `platform-exporter`, `robthebank-style`, …)
- **Generation:** Higgsfield MCP (image/video/ads/virality-predictor), ElevenLabs MCP (TTS/voice/music)
- **Video understanding:** `video-intake` (TwelveLabs), `video-analyzer`, `gemini-video`, `frame-by-frame-video`
- **Research:** `deep-research` skill; **Docs:** docx/pdf/pptx/xlsx skills
- **Desktop/web control:** computer-use MCP, Claude-in-Chrome (never DOM-tools on developers.facebook.com — it hangs)
- **Scheduling:** Windows Task Scheduler ("IG Dashboard Daily Refresh", 7:00 AM, now chained via `Daily Agent Refresh.bat`) + cron/scheduled-task tools
- **Content ops (new 2026-06-13):** `carousel-builder` skill (idea/proven-reel → saveable carousel + thread, drafts to vault) · `comment-triage` skill (draft→approve→reply on IG comments, never auto-sends)
- **Queued PLANs (awaiting Elijah approval):** `auto-clip` long-video→shorts engine (`docs/plans/2026-06-13-auto-clip-pipeline.md`) · `audience-sim` OASIS pre-publish hook-ranker (`docs/plans/2026-06-13-audience-sim-pipeline.md`)

## Folder map

- `team/` — the context system: profile / stats (auto-generated) / memory
- `ig-dashboard/` — analytics engine + local dashboard (`README.md` inside)
- `intel/` — competitive intelligence: competitor watchlist radar (official API, view counts on others' reels) — `README.md` inside
- `obsidian/Elijah's vault/` — structured second brain (own CLAUDE.md)
- `here/` — Claude's personal space (own charter)
- `docs/` — working method (Tanner's tworkflow): `workflow/` reference + `templates/` (PLAN, REVIEW, QA, SESSION-HANDOFF)
- `AGENT-TEAM-BLUEPRINT.md` — tool roadmap; `CONTENT-INTEL-PROTOCOL.md` — intel strategy; `HANDOFF.md` — ops state + token renewal (§4)
- `Daily Agent Refresh.bat` — runs all three engines (dashboard + competitor + trend) for the scheduled task
- `fromtheinside/`, `frames/`, `tiktok-analysis.md`, etc. — archive material
- **Sibling repo:** `..\abc wrap\` — ClipWith.AI video R&D (Remotion edits, baby reel, Derwin Scott
  podcast edit). Before any video work, read its `SESSION-COMPACT-2026-06-12.md` + `CLAUDE.md`.
  Same skills/MCPs are wired in both folders; work on it from either environment.
