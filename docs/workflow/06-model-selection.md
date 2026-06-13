# 06 — Model Selection

> **Claude Code only.** This entire document assumes Claude Code on
> Anthropic models. If you use Codex CLI, Cursor, a local model, or another
> stack, skip it — the workflow in docs 00–05 doesn't depend on anything
> here. The general principle still transfers: spend your most capable
> model on planning and review judgment, and cheaper models on mechanical
> execution. Consult your own tool's docs for how to switch.

Model lineups, versions, and prices change. This doc names Claude Code's
**aliases** (which track the current recommended model in each tier) rather
than version numbers. Run `/model` with no argument in a session to see
exactly what your account offers today, and check
https://code.claude.com/docs/en/model-config for current behavior.

## The tiers

Per the Claude Code model configuration docs:

| Alias | Tier | Use in this workflow |
|---|---|---|
| `fable` | Most capable model in Claude Code (Mythos class, above Opus) | Planning non-trivial work; architecture decisions; long, ambiguous multi-step tasks; the hardest debugging |
| `opus` | Most capable Opus model | Heavy implementation; complex review passes |
| `sonnet` | Balanced daily-driver | Routine implementation; most coding |
| `haiku` | Fast and efficient | Mechanical tasks: renames, formatting, exploration/search subagents |
| `opusplan` | Hybrid: Opus during plan mode, auto-switches to Sonnet on execution | The Plan→Implement phases of this workflow, automated |
| `best` | Resolves to the most capable model your account has access to | Set-and-forget top tier |
| `default` | Recommended model for your account type | Fine if you don't want to think about it |

Mapping to the loop:

- **Plan** (doc 02): `fable` — capability matters most where decisions are
  cheapest to change. To economize, `opusplan` gives Opus-grade planning
  while the implementation that follows runs on Sonnet.
- **Implement** (doc 03): `sonnet` for routine steps; `opus` when a step is
  genuinely hard. With `opusplan` this switch is automatic at the plan
  boundary.
- **Review** (doc 04): run review subagents on `opus` (or `fable` for
  high-stakes changes). Reviewing is judgment work; don't economize here.
- **QA** (doc 05): `sonnet` is typically sufficient; the methodology does
  the work.
- **Exploration subagents**: `haiku` — searching a codebase doesn't need a
  frontier model.

## How to switch

In order of precedence (per the model-config docs):

1. `/model <alias|name>` mid-session, or `/model` for the picker.
2. `claude --model <alias|name>` at launch.
3. `ANTHROPIC_MODEL` environment variable.
4. `model` field in your settings file.

**Gotcha:** in recent Claude Code versions, choosing a model in the
`/model` picker saves it as your default for *new* sessions. Press `s` in
the picker to use it for the current session only — otherwise one Fable
session quietly becomes your everyday default.

## Per-subagent models

Subagent markdown files (`.claude/agents/`) accept a `model` field in
frontmatter. This is how the routing above becomes durable instead of
manual: define an explore subagent pinned to `haiku` and a review subagent
pinned to `opus` once, and the right model runs every time without you
touching `/model`.

## Fable-specific notes (verify against current docs)

- Requires a recent Claude Code version; if `fable` doesn't appear in your
  picker, run `claude update`.
- Not available under zero-data-retention configurations.
- Fable runs with additional safety classifiers; a flagged request can
  cause Claude Code to re-run the session on Opus with a notice. `/model
  fable` switches back.
- It is the premium tier. Use it where capability compounds (planning,
  architecture, hard reviews), not for mechanical edits — that's the whole
  point of routing.

Next: [07 — Context hygiene](07-context-hygiene.md)
