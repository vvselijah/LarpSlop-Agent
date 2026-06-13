# 04 — Review

Passing tests do not mean the branch is safe. Review exists for the class
of defect that survives CI: races, trust-boundary mistakes, N+1 queries,
silently unhandled failure paths, and code that does more than the plan
said.

## The mechanism (read this part even if you skip the checklists)

A review pass works because of three properties, none of which is a
persona:

1. **Fresh context.** The reviewer must not share the implementer's
   context. An agent that just wrote the code will defend it; the same
   agent in a new session (or a subagent with its own context window) will
   find problems in it. Cheapest implementation: open a new session, give
   it the diff and the plan, nothing else.
2. **One lens at a time.** "Review this" produces shallow, scattered
   comments. A pass scoped to a single defect class goes deep. Run the
   lenses below as separate prompts, not one mega-prompt.
3. **Read-only.** The review pass produces a report; it does not fix
   things. Fixes happen back in the implementation phase, as normal
   commits, so they get re-reviewed. (Exception: pure mechanical fixes —
   dead code, stale comments — can be batched if each is its own commit.)

## The three lenses

Full checklists live in
[templates/REVIEW-CHECKLIST.md](../templates/REVIEW-CHECKLIST.md). Summary:

### Lens 1 — Correctness & robustness

What breaks in production that didn't break in tests: race conditions and
concurrent writes; partial-failure handling (the upload succeeded, the
enrichment failed — what's persisted?); retry logic and idempotency; N+1
queries and missing indexes; new enum/status values traced through every
switch and allowlist, not just changed files; resource leaks; and **test
integrity** — assertions weakened, tests skipped, or outputs hardcoded to
get green (see [08 — Failure modes](08-failure-modes.md)).

### Lens 2 — Security & trust boundaries

Every place external input crosses into the system: validation of actual
content vs. client-supplied metadata; injection (SQL, command, and prompt
injection wherever model output or fetched web content feeds another
operation); authz checks on every new route, not just the happy-path one;
secrets in diffs, logs, and error messages.

### Lens 3 — Plan conformance & completeness

The diff against the plan, both directions: everything in the plan present
(or explicitly deferred, with the plan updated); nothing in the diff absent
from the plan; the stated non-goals still untouched; new helpers that
duplicate existing code; docs and context file updated if behavior they
describe changed. (Test coverage of the plan's failure modes is a Lens 1
item.)

## Cross-tool second opinions

If you have access to a second, unrelated agent (e.g. Claude Code and Codex
CLI), running Lens 1 in both and diffing the findings is cheap and
occasionally catches what either alone misses. Treat it as optional — a
disciplined single-agent review with fresh context covers most of the
value.

## Output

Each lens produces a short written report: finding, file:line, severity,
and a one-sentence exploit/failure scenario for anything marked high. A
finding without a concrete scenario is a style opinion; downgrade it.

You — the human — read the reports. That reading is the gate. Agents
reviewing agents with no human in the loop is how confidently wrong code
ships.

**Closing the loop.** The return path needs the same discipline as the
review itself. An implementing agent handed a findings list will agree
with every item — including the false positives review agents also produce
— and "fix" correct code (see
[08 — Failure modes](08-failure-modes.md)). So: for each finding, the
implementing session first reproduces or independently confirms the defect
(file:line plus the failing scenario) before changing anything. Findings it
can't confirm get answered with evidence and returned to you to arbitrate.
Blanket acceptance of all findings is itself a red flag.

Next: [05 — QA](05-qa.md)
