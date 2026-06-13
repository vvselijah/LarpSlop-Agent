# 01 — Context Files

The single highest-leverage artifact in agentic work is the project context
file the agent reads at session start. It is also the most commonly botched:
too long, stale, or full of instructions the agent can't act on.

## Which file

- **Claude Code** reads `CLAUDE.md` (repo root, parent directories, and
  `~/.claude/CLAUDE.md` for personal preferences). Official docs:
  https://code.claude.com/docs
- **Most other agents** (Codex CLI, Cursor, and a growing list) read
  `AGENTS.md`, an open convention documented at https://agents.md
- If your team mixes tools, maintain `AGENTS.md` as the source of truth and
  make `CLAUDE.md` point to it (a one-line `See AGENTS.md` plus any
  Claude-Code-specific notes works; some teams symlink instead). Check your
  tool's docs for current precedence behavior.

## What goes in it

Aim for under a page. Every line costs context window on every single
request, so each line must earn its place. Include only what the agent
cannot discover quickly and is likely to get wrong without:

1. **Commands** — how to run tests, lint, typecheck, build, start dev
   server. Exact commands, not descriptions.
2. **Non-obvious conventions** — "migrations are never edited after merge,"
   "all API routes go through `src/api/router.ts`," "we use pnpm, not npm."
3. **Boundaries** — directories or files the agent should not touch
   (generated code, vendored deps, infra configs that deploy on merge).
4. **Definition of done** — what must pass before a change is considered
   complete (tests green, typecheck clean, docs updated).

## What to leave out

- Anything the agent can read from the code in seconds (framework, folder
  layout, dependency list).
- Aspirational style essays. If a rule isn't enforced by a linter or a
  review checklist, the context file is the wrong place to legislate it.
- Persona instructions ("act as a meticulous senior engineer"). See
  [00 — Principles](00-principles.md).
- Stale facts. A wrong line in the context file is worse than a missing
  one, because the agent trusts it over the code.

## Keeping it current

Treat the context file as code: it changes in the same PR as the behavior
it describes. Add a line to your review checklist (see
[04 — Review](04-review.md)): *"Does this change invalidate anything in
CLAUDE.md / AGENTS.md?"*

A useful retro habit: when the agent makes the same mistake twice, the fix
is usually one new line in the context file — not a longer prompt next time.

Starters: [templates/CLAUDE.md.example](../templates/CLAUDE.md.example),
[templates/AGENTS.md.example](../templates/AGENTS.md.example)

Next: [02 — Planning](02-planning.md)
