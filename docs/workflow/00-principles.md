# 00 — Principles: Structure Beats Roles

## Why no personas

Popular agent setups assign job titles: the agent is a "CEO" when reviewing
scope, a "staff engineer" when reviewing code, a "QA lead" when testing.
It's memorable, but the title isn't the mechanism. Research on persona
prompting has repeatedly found that telling a model it is some expert has
negligible — sometimes negative — effect on task accuracy. What the
well-known role-based setups actually rely on is hiding underneath the
costume:

1. **Scoped rubrics.** Each pass looks for a specific class of problem
   (scope creep is a different search than race conditions).
2. **Separate passes.** Review happens in a different pass — ideally a
   different context — than implementation, so the reviewer isn't anchored
   on the implementer's reasoning.
3. **Constrained actions.** A review pass that can only read and comment
   behaves differently from one that can rewrite the code.

This repo keeps those three mechanisms and states them directly. Every
"role" becomes a named **lens**: a checklist, a scope, and a rule about what
the pass may modify.

## Why a fixed loop

An agent given "build feature X" makes dozens of silent decisions: scope,
architecture, error handling, what to test. The failure mode isn't that the
agent can't do these — it's that the decisions are made implicitly, in the
middle of writing code, where you can't see or veto them.

The loop forces decisions to the surface at the cheapest moment to change
them:

- Scope decisions surface in **planning**, before any code exists.
- Architecture and failure-mode decisions surface in the **plan document**,
  where editing them costs a sentence, not a refactor.
- Correctness problems surface in **review**, before merge.
- "Works on the happy path but the UI is broken" surfaces in **QA**, with a
  screenshot, before a user sees it.

## Why small scope (1–3 repos)

Parallel multi-agent setups are real, but they solve a problem most
developers don't have, and they import problems most developers don't want:
merge coordination, context fragmentation, and reviewing more code than you
can read. On 1–3 repos, the bottleneck is not agent throughput — it's your
review bandwidth. The loop is designed around that constraint: every phase
produces a short artifact (a plan, a review report, a QA report) sized to be
actually read by a human.

## The contract

Every phase in this workflow follows the same contract:

- **Input:** a written artifact from the previous phase.
- **Output:** a written artifact for the next phase.
- **Gate:** a human reads the artifact before the next phase starts.

If a phase has no artifact, it didn't happen. "I reviewed it" with nothing
written down is not a review.

Next: [01 — Context files](01-context.md)
