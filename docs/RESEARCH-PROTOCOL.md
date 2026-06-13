# RESEARCH-PROTOCOL — how to research efficiently in this hub (from 2026-06-13)

Written after three `deep-research` runs (~6.5M tokens) each returned ~7 claims instead of a
full report. This doc is the fix + the standing method. **Read before launching any research.**

## Root cause (diagnosed from the actual workflow script, not guessed)

The built-in `deep-research` workflow's **Verify phase bursts ~75 agents at once**
(`MAX_VERIFY_CLAIMS=25 × VOTES_PER_CLAIM=3`), and **each verifier runs its own WebSearch.**
That sustained request rate trips Anthropic's transient server-side throttle —
`"Server is temporarily limiting requests (not your usage limit)"` — which is an
**overload/529-style load-shed, NOT your account quota.** The script has **no backoff**, so
throttled agents return null → counted as **abstentions** → ≥2 abstentions breaks the 2/3 quorum
→ claims can't survive → "all refuted / synthesis skipped."

Evidence: every failure was a `[v0/v1/v2:…]` verifier (search/fetch completed fine); and a
*single* solo run still throttled. So it's **per-workflow verify concurrency**, made worse by
running two workflows at once. More budget does NOT help — the ceiling is the throttle, not quota.

## The method ladder — pick the lightest tool that answers the question

| Question shape | Method | Why |
|---|---|---|
| A specific fact / does X work / a value | **Direct: main-loop WebFetch or a live API/curl call** | Near-zero cost, no fan-out, no throttle, fastest. *This is what gave the DECISIVE answers today* (DM error #3, comments work, token health) — while the 4.6M-token fan-outs mostly re-confirmed them. |
| A few known sources to read | **Main-loop: 3–5 targeted WebFetches, then I synthesize** | No agents, no throttle, fully reliable. |
| Broad survey needing many sources + light skepticism | **`.claude/workflows/research-lean.js`** (low-concurrency, batched verify, top-claims-only) | Stays under the throttle by design. |
| Genuinely adversarial / high-stakes claims | The full `deep-research` fan-out — but **run it SOLO and accept the verify may be partial under load** | Reserve for when 3-vote rigor truly matters. |

**Rule of thumb: always try the direct/cheap method FIRST; escalate to a workflow only for what
direct methods can't reach.** Today's lesson: the live API tests (~free) answered the load-bearing
questions; the fan-outs were largely redundant confirmation.

## Depth layer — recommended tools (improves reach + per-read efficiency)

`WebFetch` = one page, surface-level, lossy, dies on JS. To research *deep* (whole sites/sections,
structured multi-page, behind JS/anti-bot) and *cheaper per read*, add — when ready:
- **Exa** (official MCP) — semantic search + full-content/deep mode; ~90% token reduction per read. Replaces keyword WebSearch as the *find* layer. Free trial; needs `EXA_API_KEY`.
- **Firecrawl** (official MCP) — `/crawl` + `/map` (whole sites, not one page), `/extract` (schema-based multi-page), renders JS. Replaces WebFetch as the *read* layer. 1,000 free pages/mo; needs `FIRECRAWL_API_KEY`.
- **Bright Data** (MCP, 5k free credits) — heaviest: anti-bot + deep pagination + social-data feeds (TikTok/YouTube/IG). Already in AGENT-TEAM-BLUEPRINT for the content-intel gaps.

**Install procedure (do NOT pre-write configs from memory):** when committing, fetch each tool's
*current* official MCP config, add to workspace `.mcp.json` with `${EXA_API_KEY}` / `${FIRECRAWL_API_KEY}`
placeholders (set via `setx`), then wire `research-lean.js` agent prompts to PREFER Exa-search +
Firecrawl-fetch *if available*, falling back to WebSearch/WebFetch so it never hard-breaks. Test live before trusting.

## Operational rules (the "from now on")

1. **Never run two research workflows concurrently.** One at a time — concurrent workflows stack their bursts.
2. **Prefer `research-lean.js` over the built-in `deep-research`** for most surveys (it's tuned to not throttle: ≤6 concurrent verify agents vs 75).
3. **Don't launch a heavy fan-out from a deeply bloated session** — reset context first; a fresh session's bursts are cleaner and the synthesis is sharper.
4. **If a run comes back "synthesis skipped / all abstained,"** that's the throttle — do NOT relaunch the same fan-out (it'll throttle again). Instead, I synthesize the partial claims myself + fill gaps with targeted WebFetches.
5. **Spend freely on what converts to output** (per Elijah: cost isn't the constraint) — but "converts to output" means reliable methods, not re-running a throttle-capped tool.

## `research-lean.js` — the tuned workflow

Lives at `.claude/workflows/research-lean.js`. Differences from the built-in deep-research:
- **8 verify claims, not 25; 2 votes, not 3** → 16 verify agents max instead of 75.
- **Batched verify** (3 claims/batch, ≤6 concurrent) so the burst never spikes.
- **Retry-once** safety net on agent nulls.
- Invoke: `Workflow({ scriptPath: ".../.claude/workflows/research-lean.js", args: "<question>" })`.
  (Built from the diagnosis above; validate on first real use and tune batch size if needed.)
