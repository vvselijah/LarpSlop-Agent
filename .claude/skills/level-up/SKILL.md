---
name: level-up
description: >-
  Recurring project-wide improvement engine — research the external frontier and
  make the WHOLE hub better. Use when Elijah says "level up", "level up the
  project", "make everything better", "what new things/strategies/tools should we
  do", "what's new in viral/content/business", "research improvements", "frontier
  scan", "how do we improve the project", "compound the project", or wants a fresh
  research-driven upgrade pass. Pulls the latest viral/content/business strategies
  + new tools/apps/MCPs/repos/agent practices, re-evaluates the value of everything
  already built (and how to extract more from it), grades our own models, then
  outputs ONE dated, prioritized DRAFT improvement plan. Runs as a BACKGROUND
  workflow (context-rot-safe). DRAFT/PROPOSE-ONLY — never edits a production
  engine, never publishes, never spends. Distinct from `self-improve` (which only
  grades our prediction models vs realized outcomes); level-up is the broad,
  outward-looking "what should we do next" pass that USES self-improve as one input.
---

# level-up — the recurring "make the whole project better" pass

Elijah runs this often and wants it to stay valuable every time with fresh, updated
information — **without rotting the session it's invoked from**. So the entire job is
delegated to a background workflow; this session only kicks it off and reports the summary.

## What it does
A single pass that compounds the project: **(1) Recall** what's already decided (so it never
repeats), **(2) Frontier research** — 5 parallel sweeps of what's genuinely NEW since the last
pass (short-form viral strategy, content formats, business/monetization, new tools/MCPs/repos,
agent-engineering practices), **(3) Asset re-eval** — re-score every engine/skill already built
for value + how to extract more + what's underused, grounded in live model data, **(4) Synthesize**
— one dated DRAFT plan: *new things to try* + *better use of what we have* + *new tools to add* +
*architecture upgrades*, each tiered (Do-now / Later / Skip) with the cheapest first slice.

## How to run it (the ONLY step in this session)
1. Launch the background workflow — **do not do the research inline** (that's the anti-rot rule). It
   **self-dates** via PowerShell (`Get-Date`), so you don't need to pass the date; `focus` is optional:
   ```
   Workflow({ name: 'level-up' })                                  // full pass
   Workflow({ name: 'level-up', args: { focus: 'monetization' } }) // narrowed
   ```
2. The workflow runs ~5 agents at a time, writes everything to disk, and notifies on completion.
3. When it completes, **verify before reporting**: `git status` + confirm no production engine was
   modified (the workflow is propose-only; it should only have created `docs/plans/<date>-level-up.md`,
   updated `docs/LEVEL-UP-LOG.md`, and prepended one `team/memory.md` learning). Then commit + push those
   additive docs and relay the TL;DR + the suggested-order list to Elijah.

## Output (always written to disk — never left only in chat)
- `docs/plans/<date>-level-up.md` — the prioritized DRAFT improvement plan (the deliverable).
- `docs/LEVEL-UP-LOG.md` — running one-line dated index so each pass builds on the last.
- one dated learning prepended to `team/memory.md`.

## Golden rules (non-negotiable — same as the rest of the hub)
- **Propose, never apply.** Every engine change is a plan-doc diff routed through dev-workflow + Elijah.
  Never edit `ig-dashboard/*.py`, `intel/*.py`, or any production engine directly.
- **Never** publish/post/DM, spend money, install multi-GB deps, put secrets in files, or write to the
  Obsidian vault (read-only).
- **Cite everything** with a URL + date; separate genuinely-new from evergreen; don't re-propose items in
  the recall's do-not-repeat list (mark them "still pending" instead).
- **Anti-rot by construction:** the heavy work lives in the background workflow's subagents → disk; this
  session stays lean. If asked to "just do it here," still launch the workflow — that's the whole point.

## Relationship to neighbors
- **`self-improve`** — narrow: grades metrics2026 vs realized outcomes, drafts recalibration. level-up
  RUNS it as one input (live data state) but is the broad outward-looking pass.
- **`content-intel-2026` / `niche-intel`** — produce the next *post/content* plan; level-up improves the
  *whole project* (tools, skills, architecture, strategy), not just the next post.
