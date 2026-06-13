# 02 — Planning

Code is the most expensive place to discover a scope mistake. Planning moves
that discovery into a document, where fixing it costs a sentence.

## When to plan

Not everything needs a plan. Use this split:

- **Trivial** (typo, copy change, dependency bump): no plan. Just do it.
- **Small** (single-file bugfix, isolated function): a one-paragraph plan in
  the prompt is enough — what changes, what proves it worked.
- **Non-trivial** (touches multiple files, changes behavior, adds a
  feature, migrates data): full plan document. Use
  [templates/PLAN.md](../templates/PLAN.md).

If you're unsure which bucket a task is in, that uncertainty is itself the
signal: plan it.

## What a plan must pin down

The template covers these; the reasoning behind each section:

1. **Problem statement and non-goals.** Agents over-deliver by default.
   Writing "this change will NOT add caching / refactor the auth module /
   touch the schema" prevents the most common form of scope creep.
2. **Premises.** Falsifiable claims the plan depends on ("the API already
   returns `updated_at`," "sessions are stored server-side"). Have the
   agent verify each premise against the code before implementation —
   wrong premises are the top cause of plans that fall apart mid-build.
   If the plan leans on a fast-moving library, make the library's API a
   premise too, verified against its current docs — agents answer from
   training-time memory by default (see
   [08 — Failure modes](08-failure-modes.md)).
3. **Approach with alternatives.** Two or three candidate approaches with
   honest tradeoffs, and a stated reason for the pick. If the agent can
   only produce one approach, it hasn't explored the space.
4. **Failure modes.** What happens on partial failure, retry, concurrent
   access, empty/oversized input. Asking for a data-flow or state diagram
   here is effective: diagrams force hidden assumptions into the open.
5. **Test plan.** What will be tested, at which level (unit/integration/
   end-to-end), and which cases prove the failure modes are handled.
6. **UI states** (if the change has a UI): empty, loading, error, success,
   and narrow-viewport behavior. Unspecified states get implemented as
   whatever is easiest, which is usually nothing.

## The planning conversation

Don't accept the first plan. The cheap, high-value move is one round of
adversarial questioning before approving:

- "What's the strongest argument this is the wrong approach?"
- "Which premise, if false, breaks this plan?"
- "What's the smallest version of this that's still useful?"

That last question replaces what role-based systems call a "CEO review."
You don't need a persona to ask it.

## Claude Code specifics (skip if using another tool)

- **Plan mode** puts Claude Code in a read-only research state: it can read
  files, search, and propose, but not edit, until you approve the plan.
  Cycle modes with Shift+Tab, or start a session with plan mode active.
  This is the right default for the planning phase — it makes "no code
  until the plan is approved" mechanical instead of honor-system.
- **Model choice matters most here.** Planning is where the most capable
  model pays for itself; implementation often doesn't need it. Routing
  details: [06 — Model selection](06-model-selection.md).
- Save approved plans into the repo (e.g. `docs/plans/<date>-<slug>.md`).
  A committed plan survives context compaction and session restarts, and
  the retro (below) needs it.

## Retro: closing the loop

After shipping, spend five minutes comparing the plan to what actually
happened: which premises were wrong, what wasn't in the plan but should
have been, what the agent repeatedly misunderstood. Each finding lands in
one of two places:

- A correction to the **context file** (recurring misunderstandings), or
- A new line in your **plan template** (recurring blind spots).

This is the entire retro practice. It's small, and it compounds.

Next: [03 — Implementation](03-implementation.md)
