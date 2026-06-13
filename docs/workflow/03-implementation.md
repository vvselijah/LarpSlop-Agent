# 03 — Implementation

The plan is approved. The implementation phase has one governing rule:
**keep the diff reviewable.** Every practice below serves it.

## Work in plan-sized steps

Implement the plan's steps in order, one step per checkpoint. After each
step: run the tests, commit. Small commits are not bureaucracy — they are
what makes the review phase possible and `git bisect` useful when something
breaks later.

Commit messages should reference the plan step they implement. If the agent
proposes work that isn't in the plan, that's a plan amendment, not a
freebie: update the plan document first (one line), then implement.

One hard rule inside every step: **the agent never modifies an existing
test to make it pass without flagging it for your approval.** When told to
"make the tests green," editing the test is often the shortest path — and
the most commonly gamed gate there is (see
[08 — Failure modes](08-failure-modes.md)).

## Branch hygiene

- One plan, one branch. Never let the agent implement on `main`.
- Start each work session by syncing the branch with `main` so review and
  QA happen against reality.
- If the agent has produced three failed attempts at the same step, stop.
  Reset to the last good commit and re-prompt with what you learned —
  accumulated failed attempts in context degrade every subsequent attempt.
  This applies to every agent, not just Claude Code.

## Scope guards

Agents drift. Practical guards, in increasing order of strictness:

1. State boundaries in the prompt: "only modify files under `src/billing/`."
2. Put hard boundaries in the context file (see
   [01 — Context](01-context.md)): directories that are never to be edited.
3. Review the diff file list before reading the diff itself. A file you
   didn't expect in the list is the fastest scope-creep detector there is.

## Claude Code specifics (skip if using another tool)

- **Subagents** are markdown-defined workers in `.claude/agents/` (project)
  or `~/.claude/agents/` (personal), each with its own context window,
  optional `tools` restriction, and optional `model` override in YAML
  frontmatter. Manage them with the `/agents` command. Two uses fit this
  workflow:
  - **Exploration** during implementation ("find every caller of X") in a
    subagent keeps your main context clean for the actual work.
  - **Review** in a subagent gives you the fresh-context reviewer that
    [04 — Review](04-review.md) calls for, without opening a new terminal.
  Docs: https://code.claude.com/docs (subagents section).
- **Skills** in `.claude/skills/<name>/SKILL.md` encode repeatable
  procedures (this repo ships one — see
  [skills/dev-workflow](../skills/dev-workflow/SKILL.md)). Skills load
  their full instructions only when invoked, so they don't tax the context
  window the way a long CLAUDE.md does. Docs:
  https://code.claude.com/docs/en/skills
- **Long sessions degrade.** When a session has accumulated corrections
  and dead ends, prefer a fresh session seeded with the committed plan
  over pushing through. The plan document is your save file. Don't wait
  for the tool to force a summary — reset deliberately at a clean
  boundary once context usage passes ~40%. Full guidance, and the
  installable `context-checkpoint` skill that automates the check:
  [07 — Context hygiene](07-context-hygiene.md).

## Definition of done for this phase

Before moving to review:

- [ ] All plan steps implemented or explicitly deferred (plan updated).
- [ ] Tests from the plan's test section written and passing.
- [ ] Lint and typecheck clean.
- [ ] Diff file list contains no surprises.
- [ ] Context file still accurate (or updated in this branch).
- [ ] Every box above backed by command output from a run *after* the
      final edit — claims without evidence don't count (see
      [08 — Failure modes](08-failure-modes.md)).

Next: [04 — Review](04-review.md)
