---
name: research
description: Run any research/investigation efficiently in this hub. Use when asked to "research", "look into", "find out about", "compare", "what's the best", "survey", or gather multi-source info. Enforces the hub's hard-won protocol (docs/RESEARCH-PROTOCOL.md) so sessions don't repeat the throttle/cost mistakes.
---

# Research (efficiently)

Full rationale: `docs/RESEARCH-PROTOCOL.md`. The method ladder — **pick the lightest tool that answers the question:**

1. **A specific fact / does-X-work / a value** → DIRECT: a `WebFetch`, an `exa`/`tavily`/`firecrawl`
   MCP call, or a live API/`curl` check. Near-zero cost, no fan-out, no throttle. **This gave every
   decisive answer last session for ~free** — always try it FIRST.
2. **A few known sources to read** → main-loop: 3–5 targeted `firecrawl`/`WebFetch` fetches, then synthesize. No workflow.
3. **A broad survey needing many sources** → the throttle-safe **`research-lean`** workflow:
   `Workflow({ scriptPath: ".../.claude/workflows/research-lean.js", args: "<question>" })`.
4. **Genuinely adversarial / high-stakes claims** → the built-in `deep-research` — but run it SOLO and
   expect its verify phase may partial-fail under load.

## Hard rules (these are the expensive lessons)
- **NEVER run two research workflows at once.** Concurrent fan-out trips Anthropic's transient
  rate-limit ("temporarily limiting requests — not your usage limit") and wastes the run. One at a time.
- **Prefer `research-lean` over built-in `deep-research`.** deep-research bursts ~75 verify agents and
  reliably throttles into "synthesis skipped"; research-lean batches to ≤6 concurrent and runs clean.
- **If a run comes back "abstained / synthesis skipped,"** do NOT relaunch the same fan-out — synthesize
  the partial claims yourself + fill gaps with direct fetches.
- **The deep tools are wired:** `exa`/`tavily` (search), `firecrawl` (deep crawl/JS), free Jina via
  `WebFetch https://r.jina.ai/<url>`. Use them over plain WebSearch/WebFetch for depth.
- Cost is not the constraint here (Elijah's stance) — **reliable output-per-effort is.** Spend freely on
  what converts to a finished answer; don't burn it re-running a throttle-capped tool.

## After researching
Synthesize into a clear answer; for tool/capability research, append the verdict to the relevant doc
(`AGENT-TEAM-BLUEPRINT.md`, `CONTENT-INTEL-PROTOCOL.md`, or the active plan in `docs/plans/`).
