# 07 — Context Hygiene

Every agent works inside a context window, and everything in the session
spends it: files read, command output, your corrections, the agent's own
dead ends. The window filling up is not the problem. The problem is that
**quality degrades long before the window is full** — the agent starts
forgetting constraints stated an hour ago, re-reading files it already
read, and contradicting decisions it already made. There is no error
message for this. It just gets quietly worse.

This doc is tool-agnostic except where marked. It is the reason this repo
ships a second skill,
[skills/context-checkpoint](../skills/context-checkpoint/SKILL.md).

## Treat context as a budget

The mindset shift: the context window is not a transcript, it's a budget.
A 5,000-line log paste, an unscoped "read the whole repo," or three failed
attempts left in the conversation are all withdrawals. A session that
spends carelessly runs out of quality in the middle of the task.

Spend less in the first place:

- **Exploration goes in subagents** (or a separate session). "Find every
  caller of X" can burn ten files' worth of context; only the one-line
  answer needs to come back.
- **Read scoped, not whole.** Point the agent at the function, not the file;
  the file, not the directory.
- **Don't paste what you can reference.** Big logs and stack traces go in a
  file the agent reads selectively.
- **Failed attempts are toxic residue.** After a reset-and-retry (see
  [03 — Implementation](03-implementation.md)), the failed attempts are
  still in context, degrading the next attempt. That's a signal to reset
  the session, not just the branch.

## The 40% rule

Most tools force a summarization ("compaction") only when the window is
nearly full. That is the worst possible timing: it fires mid-task, you
don't control what survives the summary, and you've already been working
with a degraded agent for the last stretch.

The rule this workflow uses: **when context usage passes about 40%, reset
deliberately at the next clean boundary** — end of a plan step, end of a
phase, after a commit. Don't wait for the tool to force it.

Why 40% and not higher:

1. Degradation starts well before the limit. At 40% you're acting while
   the agent is still sharp.
2. A clean reset needs headroom: enough budget left to finish the current
   step, write down state, and summarize well. At 90% you have none.
3. Boundaries are cheap, interruptions are expensive. Acting early is what
   lets you pick the boundary instead of having one picked for you.

Treat 40% as a default, not dogma — long single tasks may justify
stretching toward 50–60%. Past that you are gambling with quality.

## Compact or clear?

Two different resets, for two different situations:

| | Compact (summarize in place) | Clear / fresh session |
|---|---|---|
| **When** | Mid-task; the working state isn't written down anywhere yet | Between tasks or phases; or after dead ends and wrong turns polluted the session |
| **What survives** | A summary the tool writes (lossy, partly out of your control) | Only what's in your artifacts — plan doc, handoff note, commits |
| **Risk** | Summary silently drops a constraint or decision | You forgot to write something down before clearing |

The rule of thumb: **if the plan document and a handoff note capture
everything worth keeping, clear — a fresh session seeded from artifacts
beats a compacted one.** Compaction is for when they don't yet.

Before either, write the state down: fill in
[templates/SESSION-HANDOFF.md](../templates/SESSION-HANDOFF.md) (thirty
seconds: current step, decisions made, next action, open questions). This
is the same artifact contract as every other phase — if the state isn't
written down, it doesn't survive the reset.

## Watch for rot regardless of the number

Percentages are a proxy. Reset at *any* usage level when you see the
symptoms:

- The agent re-reads files it already read this session.
- It re-asks questions you answered.
- It contradicts a decision recorded earlier in the same session.
- It "forgets" a constraint from the context file or plan.
- Its plan for the next step has quietly drifted from the plan document.

Two of these in short order means the session is done. Write the handoff,
clear, reseed.

## Claude Code specifics (skip if using another tool)

Verified against https://code.claude.com/docs (commands, context-window,
statusline, env-vars pages) at time of writing; these change — check them.

- **`/context`** shows current usage as a breakdown (system prompt, tools,
  memory files, messages). This is the ground-truth number for the 40%
  rule.
- **`/compact`** summarizes the conversation in place, and accepts optional
  focus instructions — use them: `/compact preserve the plan decisions,
  the current step, and the failing test output`. A persistent
  `# Compact instructions` section in CLAUDE.md applies to every
  compaction, including automatic ones. Know what survives: the
  project-root CLAUDE.md is re-read from disk, but details from early
  conversation can be dropped by the summary — which is why the plan
  document, not the conversation, holds the decisions.
- **`/clear`** starts fresh — and is non-destructive: the old conversation
  stays available under `/resume`. Reseed the new session by pointing it
  at the committed plan and the handoff note.
- **Auto-compact** fires at roughly 95% of capacity by default — by the
  40% rule, if you see it fire, the deliberate reset is long overdue. The
  threshold is tunable via the `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`
  environment variable (e.g. `50` to compact earlier).
- A **custom status line** can display live usage: the status line input
  includes a `context_window.used_percentage` field, and the official docs
  ship examples that render it as a colored bar. Setup:
  https://code.claude.com/docs/en/statusline
- **The context-checkpoint skill** in this repo
  ([skills/context-checkpoint](../skills/context-checkpoint/SKILL.md))
  measures usage when invoked and walks the compact-or-clear decision
  above. Its optional companion hook (`scripts/context_hook.py` in the
  skill folder, setup in the file header) injects an automatic nudge the
  first time usage crosses 40% — skill for judgment, hook for the trigger,
  status line for always-on visibility.

Next: [08 — Agent failure modes](08-failure-modes.md)
