---
name: self-improve
description: Close the predict->observe loop on the hub's own models. Use when Elijah says "self-improve", "close the loop", "grade the predictions", "what should we tune", "learn from the data", "is the model actually working", "did our scoring predict anything", or wants the agent team to audit and recalibrate ITSELF against realized outcomes. Runs the read-only grader (self-improve/grade.py), interprets the held-out correlations + skip-gate + weight search + category audit, then DRAFTS proposals (never auto-applies) across 5 content loops plus 2 recursive/meta loops, and logs one dated learning to team/memory.md. DRAFT/PROPOSE-ONLY by the hub's golden rule.
---

# self-improve — the recursive self-learning loop

This skill makes the agent team **grade its own predictions against reality and
propose its own recalibrations**. It is the activation of the dormant
predict→observe loop: every model the hub uses to decide content (the 2026
score, the skip-gate, the Higgsfield virality predictor, the categorizer, the
watch-time ideator) made an implicit prediction; store.json records what actually
happened; this skill measures the gap and drafts the fix.

**Claude is the brain.** `grade.py` is a dumb, deterministic, read-only
calculator — it produces correlations and candidates. YOU read its report,
decide what's signal vs noise, and write the proposals. The script proposes
arithmetic; you propose judgment.

## The one hard rule (read this twice)

**PROPOSE, NEVER AUTO-APPLY.** This hub's whole safety model is that Claude
drafts and Elijah clicks. You may NEVER edit a production engine
(`metrics2026.py`, `refresh.py`, `dashboard.html`, any `intel/*.py`). Every real
change is written as a `docs/plans/<date>-<slug>.md` proposal (use
`docs/templates/SELF-IMPROVE-PROPOSAL.md`) and routed through the **dev-workflow**
skill — Plan → Implement → Review → QA → Ship — with Elijah's explicit accept.

The ONLY safe auto-writes from this loop:
1. The append-only predictor-vs-actual **ledger** under `self-improve/data/`
   (gitignored generated output — `grade.py` writes it).
2. `category_override` **data fixes** in store.json (refresh.py:193 already
   supports this; it is data, not engine logic) — still surface them to Elijah
   first as a batch, don't silently rewrite his data.
3. One dated **learning** appended to `team/memory.md`.
4. **`intel/*.json` watchlist** suggestions (data, not code).

Anything else is a draft.

## Workflow

### Step 0 — run the grader
```powershell
python self-improve/grade.py --self-test   # must print "self-test OK"
python self-improve/grade.py               # writes data/grade-<date>.json + grade-report.md
```
Run via the **PowerShell tool** (python is not on the Bash PATH here). `grade.py`
is pure stdlib and read-only. Then READ `self-improve/data/grade-report.md`.

### Step 1 — interpret the report (this is the judgment part)
The report gives you four things. For each, decide signal vs noise BEFORE drafting:

- **Held-out Spearman(score, views) and (score, watch_time).** The held-out
  column (train older 70% / test newer 30%) is the honest one — in-sample is
  partly circular because the percentile distribution is built from the same
  posts. A held-out Spearman around +0.3–0.5 means the 2026 score has real
  predictive lift; near 0 or negative means the model is not earning its keep and
  you should say so plainly.
- **Skip-gate table.** Does the `healthy` band actually out-view / out-retain the
  `throttled` band? If yes, the gate is valid. If inverted, the gate may be
  suppressing the wrong posts — that's a finding, draft an L5 proposal.
- **Weight proposal.** `grade.py` already applied an honest-gate (a candidate
  must beat current weights by ≥0.02 held-out Spearman). Even when it fires,
  **sanity-check the proposed weights yourself** — a tiny delta or a weird jump
  (e.g. `repost` leaping when reposts exist on only ~94/300 posts) is likely
  overfitting to a small held-out set, NOT a real improvement. Be skeptical.
- **Category audit.** "Other" posts that hit a keyword, and captions straddling
  >1 category — `category_override` candidates.

### Step 2 — min-sample / confidence gates (mandatory)
- Skip-rate metrics exist on **~94/300 posts** — borderline. Any skip-gate or
  repost-driven conclusion is **directional, not proven**. Flag confidence
  explicitly in every proposal that leans on skip_rate or reposts.
- Held-out test sets under ~20 posts → LOW CONFIDENCE; `grade.py` flags this, you
  must carry the flag into the proposal.
- **Honest-gate:** if a proposed change does NOT beat baseline on HELD-OUT data,
  **ship nothing and say so.** "No change is warranted; the current model already
  generalizes" is a complete, valuable answer. Do not invent a tweak to look busy.

### Step 3 — draft proposals across the 5 content loops
For each loop where the report shows a real, held-out-validated signal, write ONE
`docs/plans/<date>-<loop>-<slug>.md` from `docs/templates/SELF-IMPROVE-PROPOSAL.md`.

- **L1 — metrics2026 recalibration.** WEIGHTS or skip-thresholds tuning, ONLY if
  `weight_search` beats baseline held-out AND the weights pass your sanity check.
  Target: `ig-dashboard/metrics2026.py:56` (WEIGHTS) / `:59-60` (skip bands).
- **L2 — Higgsfield-trust ledger.** Cross-reference past Higgsfield virality
  predictor scores (where logged in the vault / reel notes) against realized
  views. Build/append the predictor-vs-actual ledger in `self-improve/data/`. If
  the predictor doesn't correlate with outcomes, propose down-weighting its vote
  in pre-publish ranking. (Ledger append is a safe auto-write; the trust-weight
  change is a proposal.)
- **L3 — categorize keyword-drift.** From the category audit: propose
  `category_override` data fixes for the worst mislabels (batch them for Elijah),
  AND if a keyword list is systematically wrong, draft a refresh.py CATEGORIES
  edit (proposal, dev-workflow) — never edit the list directly.
- **L4 — watchtime backtest.** Did `watchtime_ideator.py`'s arbitrage picks
  actually earn more watch-time when posted? Backtest its logic against
  store.json's `ig_reels_avg_watch_time`; propose a tweak only if held-out lift
  exists.
- **L5 — threshold self-tune.** Skip-gate bands (`SKIP_HEALTHY` 0.40 /
  `SKIP_THROTTLE` 0.50). If the skip-gate table shows the published 40/50
  benchmark splits Elijah's own posts poorly, propose his personalized thresholds
  — flagged LOW CONFIDENCE at n≈94.

### Step 4 — log the learning
Append exactly ONE dated line to `team/memory.md` summarizing what the loop found
this run (e.g. "2026-06-15: m26 held-out Spearman +0.46 vs views — model
generalizes; weight-search delta only +0.02, rejected as overfit; skip-gate valid
(healthy 14.8k vs throttled 5.4k views)"). This is how the loop compounds.

### Step 5 — the recursive / meta tier
- **L6 — review past proposals.** Read prior `docs/plans/*self-improve*.md` and
  the dated `team/memory.md` learnings. Which proposals did Elijah accept? Did the
  accepted ones actually improve the next grade run's held-out numbers? Write a
  short "proposal acceptance + impact" note. This is the loop grading ITSELF —
  if your past proposals didn't help, propose tightening your own honest-gate.
- **L7 — propose edits to OTHER skills.** From outcome patterns, draft proposals
  to improve sibling skills (e.g. `content-intel-2026`, `weekly-content-plan`,
  `carousel-builder`) — "the data says saves-first carousels underperform
  shares-first, update the skill's optimization target." These are SKILL.md edit
  proposals routed through dev-workflow, never silent edits.

## Output contract
Each run produces: the refreshed `self-improve/data/` ledger (auto), 0–N proposal
docs in `docs/plans/` (drafts), one `team/memory.md` line (auto), and a short
spoken summary to Elijah leading with the held-out correlation and an explicit
confidence call. If nothing beat baseline: say so, log it, propose nothing.

## See also
- `self-improve/grade.py` — the read-only grader (run it first, every time)
- `self-improve/README.md` — the 5+2 loops one-liners + golden rule
- `docs/templates/SELF-IMPROVE-PROPOSAL.md` — the proposal schema
- `ig-dashboard/metrics2026.py` — the 2026 scoring contract under test
- **dev-workflow** skill — the required path for any accepted code change
