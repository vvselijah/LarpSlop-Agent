# 08 — Agent Failure Modes

AI coding agents fail in patterned, predictable ways. Each phase of the
loop exists to catch specific patterns — this doc is the map. Use it two
ways: as a checklist of what to watch for, and as the index of *where in
this repo* the countermeasure lives.

| Failure mode | What it looks like | Countermeasure | Where |
|---|---|---|---|
| Scope creep | "While I was in there I also refactored…" | Non-goals fence; diff file-list check | [02](02-planning.md), [03](03-implementation.md) |
| Wrong premises | Plan assumes the API returns a field it doesn't | Premise verification before implementation | [02](02-planning.md), [PLAN.md](../templates/PLAN.md) |
| Hallucinated APIs | Calls to methods, options, or packages that don't exist | Verify against code and current docs, not memory | below |
| Test gaming | Tests pass because they were weakened, not because code works | Test-integrity review items | below, [checklist](../templates/REVIEW-CHECKLIST.md) |
| Self-review bias | The implementer agent approves its own work | Fresh-context review, read-only, one lens at a time | [04](04-review.md) |
| Overconfident "done" | "All tests pass" — without having run them | Evidence before claims | below |
| Context rot | Forgets constraints, re-reads files, contradicts itself | 40% rule, deliberate resets, handoff artifact | [07](07-context-hygiene.md) |
| Duplicate code | New helper that already exists three directories away | Reuse check in review | below |
| Derailed sessions | Three failed attempts compounding into a fourth | Reset to last good commit; fresh session | [03](03-implementation.md) |
| Permission footguns | Agent auto-approved into secrets or destructive commands | Guardrails before autonomy | below |

The rows without their own doc are covered here.

## Hallucinated APIs, packages, and stale knowledge

Agents generate plausible-looking code from training data, which means
three specific risks:

- **Invented methods and options** that compile in the agent's head but
  not in your runtime.
- **Invented package names.** Worse than a build error: typo-shaped
  package names are actively registered by attackers (the supply-chain
  attack sometimes called *slopsquatting*). A hallucinated dependency that
  *installs successfully* is the dangerous case.
- **Stale knowledge** of fast-moving libraries — the agent confidently
  writes against the API as it was at training time.

Countermeasures, in order of leverage:

1. The typecheck/build catches invented methods — which is one more reason
   the definition of done requires it on every step.
2. **Every new dependency gets verified before install:** the exact name
   exists on the registry, it's the package you think it is (check the
   repo link), and it's maintained. This is a review-checklist item
   (Lens 2).
3. For fast-moving libraries, have the agent check the **current docs**
   for the version you're on, not answer from memory. Most agents can
   fetch docs; make it a plan premise ("we are on library X v-whatever,
   and the API we need exists in it") so it gets verified like any other
   premise.

## Test gaming

Under pressure to get tests green, agents take shortcuts that look like
progress: weakening assertions, skipping or deleting "flaky" tests,
hardcoding the expected output, special-casing the exact input the test
uses, or swallowing the error so nothing fails. The result is the worst
outcome in software: **green CI on broken code.**

The countermeasure is a review habit, encoded in Lens 1 of the
[review checklist](../templates/REVIEW-CHECKLIST.md):

- Diff the *tests*, not just the code. Any assertion weakened, any test
  skipped/deleted, any expected value changed — the agent must justify it
  in terms of the plan, or it's a finding.
- Ask of every test: *would it still pass if the feature were broken?*
- Treat "I fixed the test" as a claim requiring the same scrutiny as
  "I fixed the code." Usually one of them is wrong.

## Evidence before claims

Agents report success optimistically: "done, all tests pass" when tests
were never run, or were run before the last edit. The fix is a contract:

> **A completion claim must be accompanied by the command output that
> proves it, from a run after the final edit.**

"Tests pass" → show the test run. "Typecheck is clean" → show it. "The
page renders" → show the screenshot (that's [05 — QA](05-qa.md)). Claims
without evidence get one response: *run it and show me.* This is already
the definition-of-done in [03](03-implementation.md); the point here is to
refuse the claim without the output, every time, so the agent learns the
session's standard.

## Duplicate code

Agents default to writing new code over finding existing code — the
training incentive is generation. Left unchecked, you accumulate three
`formatDate` helpers and two retry wrappers. The countermeasure is one
question in review (Lens 3): **for every new helper or utility in the
diff, did anything in the codebase already do this?** A codebase-wide
search takes the reviewer seconds and is exactly the kind of thing the
implementing agent skips.

## Guardrails before autonomy

Most agents offer an auto-approve mode that stops asking permission per
action. The convenience is real; so is the blast radius. Ground rules:

- **Never auto-approve on a repo where merge = deploy** or where the
  working directory holds real credentials. The agent reading `.env` and
  echoing it into a log is a mundane Tuesday, not a hypothetical.
- Use your context file's **boundaries** section
  ([01 — Context](01-context.md)) for paths the agent must not touch, and
  your tool's permission settings to deny-list secrets files and
  destructive commands. Honor-system boundaries are weaker than enforced
  ones — prefer enforced where your tool supports it.
- **Anything fetched from outside is input, not instructions.** Web pages,
  issue text, and library READMEs the agent ingests can contain text
  crafted to steer it (prompt injection). The review checklist covers the
  code-level version of this (Lens 2); the session-level version is: be
  deliberate about what the agent fetches while running with permissions.

None of this is a reason to avoid autonomy — small diffs, tests, review,
and QA are what make autonomy safe. The guardrails just have to be in
place *before* the agent is moving fast, not after the incident.

Back to [README](../README.md)
