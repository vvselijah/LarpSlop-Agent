---
name: weekly-content-plan
description: Build Elijah's weekly Instagram content plan from live performance data. Use when he asks to "plan my content", "plan this week", "what should I post", or wants a content calendar/strategy refresh. Reads team/profile.md + team/stats.md + team/memory.md + vault ideas, produces a 7-day plan as a vault note, and logs learnings back to memory.
---

# Weekly content plan

Produce a 7-day posting plan grounded in what's actually working, not vibes.

## Steps

1. **Load context** (all paths relative to the workspace root `C:\Users\elija\OneDrive\Desktop\ai agent team`):
   - `team/profile.md` — voice, niches, standing rules
   - `team/stats.md` — live numbers (auto-fed daily by the dashboard)
   - `team/memory.md` — prior learnings; do not repeat failed experiments
   - Idea backlog: `obsidian/Elijah's vault/Fable ideas.md`, `obsidian/Elijah's vault/20-Content/Ideas/`, `obsidian/Elijah's vault/00-Inbox/`
2. **Pull fresh data if stats.md is older than 24h:** run `python ig-dashboard/refresh.py`, or query the `instagram` MCP directly (`get_media_insights` on recent posts). For deeper analysis, the `reel-analytics` skill is available.
3. **Find the arbitrage:** compare posts-per-category vs views-per-post (stats.md "Category mix"). Allocate the week's slots toward undersupplied winners; cap oversupplied weak categories. Check the dashboard's best day/hour heatmap if timing questions matter.
4. **Draft the plan — 7 days**, each slot: category, hook (in Elijah's voice per profile.md), format (talking-head / b-roll edit / AI-generated via Higgsfield), CTA, and which venture it feeds (if any). Flag which slots are API-publishable (voice-only/original audio) vs need manual posting (trend audio).
5. **Write it to the vault** as `obsidian/Elijah's vault/20-Content/Ideas/Week of YYYY-MM-DD.md` using the `idea` template's property block (`type: idea`, `domain: content`, `status: open`, `date_captured: today`). Follow the vault CLAUDE.md property contract exactly.
6. **Log one learning** to `team/memory.md` (dated, newest-first): what the data said this week that changed the plan.
7. **Never schedule or publish anything** — the plan is a deliverable for Elijah to approve. Publishing requires his explicit per-action confirmation (workspace CLAUDE.md rule 1).
