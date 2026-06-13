# docs/ — working method (adapted from Tanner's `tworkflow`)

Source: **https://github.com/clarity-digital-development/tworkflow** (Tanner Carlson, MIT).
Brought into this hub 2026-06-12. This is Tanner's AI-agent development workflow, applied
**where it's valid for this hub** (a content/ops/analytics workspace, not a typical code repo —
see the scoping in the workspace `CLAUDE.md` § "Working method").

## What's here

- `workflow/00`–`08` — the reference docs (principles, context, planning, implementation,
  review, QA, model-selection, **context-hygiene**, **failure-modes**). Internally cross-linked.
- `templates/` — the canonical copy-paste artifacts the skills look for FIRST:
  - `PLAN.md` — scope a change before building (problem / non-goals / premises / failure modes / steps)
  - `REVIEW-CHECKLIST.md` — three fresh-context review lenses (correctness / security / plan-conformance)
  - `QA-REPORT.md` — functional + visual QA record
  - `SESSION-HANDOFF.md` — the 30-second baton note written **before any /clear or /compact**
- `plans/` — created on demand; filled plans land here as `YYYY-MM-DD-<slug>.md`.

## The two installed skills (`.claude/skills/`)

- **`context-checkpoint`** — measures real context usage from the session transcript and walks
  the compact-or-clear decision at the 40% rule. The companion hook (`scripts/context_hook.py`,
  wired in `.claude/settings.json`) auto-nudges the first time usage crosses 40%.
- **`dev-workflow`** — the Plan → Implement → Review → QA → Ship → Retro loop. **Scope here:**
  use the full loop for changes to the **Python engines** (`ig-dashboard/refresh.py`,
  `intel/*.py`) and `dashboard.html`; lighter touch for docs/content/vault edits; visual-QA
  screenshots (`scripts/qa-screenshots.js`) need `npm i -D playwright` and apply only to `dashboard.html`.

## Honest caveats for this hub

- **Not under git (yet).** The loop's commit/branch/PR mechanics (Implement "one commit per step",
  Ship "open a PR") are aspirational until this hub is version-controlled. The *discipline* —
  written plan, separate review passes, QA with evidence, handoff before reset — applies regardless.
- The **40% context rule is the highest-value import** for this hub specifically: its sessions run
  long and heavy (big research workflows), and its whole continuity model is session handoffs.
