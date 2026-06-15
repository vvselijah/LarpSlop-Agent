# Self-Improve Proposal: <short title>

> One proposal = one change. The self-improve loop DRAFTS this; Elijah accepts or
> rejects; accepted changes are implemented via the **dev-workflow** skill.
> Nothing in this doc is applied until the accept box below is checked.

- **Date:**
- **Loop:** L1 metrics2026-recalibration / L2 higgsfield-trust / L3 categorize-drift / L4 watchtime-backtest / L5 threshold-self-tune / L6 meta-review-past-proposals / L7 sibling-skill-edit
- **Generated from:** `self-improve/data/grade-<date>.json` (run id / date)
- **Status:** draft / accepted / rejected / shipped

## 1. The prediction that was graded

What model made a prediction, and against what realized outcome was it graded?
(e.g. "metrics2026 score vs realized views, held-out 70/30 chronological split".)
One paragraph.

## 2. Target

- **File:line:** e.g. `ig-dashboard/metrics2026.py:56`
- **OLD value:**
  ```
  ```
- **NEW value (proposed):**
  ```
  ```

## 3. Evidence (held-out, not in-sample)

The honest-gate: a change only earns a proposal if it beats baseline on HELD-OUT
data. Fill this from the grade report — do not hand-wave.

| Metric | Baseline (current) | Proposed | Delta |
|---|---|---|---|
| Held-out Spearman (vs views) | | | |
| Held-out Spearman (vs watch_time) | | | |
| Other relevant outcome | | | |

- **Sample size (held-out test n):**
- **Total posts the signal rests on:**
- **Honest-gate passed?** yes / no — if no, this proposal should not exist.

## 4. Confidence

- **Level:** high / medium / LOW
- **Why:** sample size, fraction of posts carrying the field (skip_rate/reposts
  exist on only ~94/300 — anything leaning on them is borderline), risk of
  overfitting a small held-out set, stability across runs.
- **Would I bet on this generalizing to the NEXT 30 posts?** yes / no / unsure

## 5. Risk

| Scenario | Effect if this change is wrong |
|---|---|
| The held-out gain was noise | |
| The field this relies on is sparse | |
| Downstream skill / dashboard assumption breaks | |

- **Reversible?** yes / no — how to roll back.
- **Blast radius:** which engines/skills/reports consume this value.

## 6. Decision

- [ ] **ACCEPT** — Elijah approves implementing this change.
- [ ] **REJECT** — keep current behavior (note why below).

**Notes / reason:**

---

**Apply via dev-workflow.** If accepted, do NOT edit the production engine from
the self-improve loop. Open a `docs/plans/<date>-<slug>.md` from `PLAN.md`, verify
the premises in §3 against the live code, run the three review lenses + QA, and
ship one commit. The self-improve loop's job ended at this draft.
