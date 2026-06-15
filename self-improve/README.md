# self-improve/ — the predict→observe loop

This folder closes the feedback loop on the hub's own models. Every time the
agent team uses a model to decide content — the 2026 score (`metrics2026.py`),
the skip-gate, the categorizer, the Higgsfield virality predictor — it makes an
implicit **prediction**. `ig-dashboard/data/store.json` records what actually
**happened**. This loop measures the gap and **proposes** recalibrations.

It is the activation of a previously dormant capability: the hub had a scoring
model but never graded it against reality. Now it does, on live data, every run.

## How to run

Run via the **PowerShell tool** (python is not on the Bash PATH on this host).
`grade.py` is pure stdlib and strictly read-only — it never touches store.json or
any production engine.

```powershell
python self-improve/grade.py --self-test   # tiny synthetic asserts -> "self-test OK"
python self-improve/grade.py               # live grade over store.json
```

The live run writes two files into `self-improve/data/`:
- `grade-<YYYY-MM-DD>.json` — the full machine-readable grade (the ledger entry).
- `grade-report.md` — the human summary: held-out correlations, the skip-gate
  validity table, the weight-tuning proposal, and the category-override candidates.

Then invoke the **`self-improve` skill** (say "self-improve" / "grade the
predictions" / "close the loop") — Claude reads the report, decides signal vs
noise, and drafts proposals.

## What it grades

- **Score vs outcome** — Spearman rank correlation between the 2026 score and
  realized views / avg watch-time, both in-sample AND held-out (train on the older
  70% of posts, test on the newer 30%). Held-out is the number that matters.
- **Skip-gate validity** — do `healthy`-band posts actually out-view/out-retain
  `throttled` ones? If not, the gate is suppressing the wrong posts.
- **Weight search** — a coarse grid over alternative WEIGHTS dicts, scored on the
  same held-out split, with an honest-gate (must beat current by ≥0.02). Proposal
  only — `grade.py` NEVER edits `metrics2026.py`.
- **Category audit** — deterministic flagging of mislabeled posts ("Other" + a
  keyword hit, or captions straddling >1 category) as `category_override`
  candidates.

## The loops (5 content + 2 recursive)

- **L1 — metrics2026 recalibration** — tune WEIGHTS / skip-thresholds, only if held-out beats baseline.
- **L2 — Higgsfield-trust ledger** — grade past virality-predictor scores vs realized views; down-weight if uncorrelated.
- **L3 — categorize keyword-drift** — propose `category_override` fixes + CATEGORIES keyword edits.
- **L4 — watchtime backtest** — did `watchtime_ideator.py`'s arbitrage picks actually earn watch-time?
- **L5 — threshold self-tune** — personalize the skip-gate bands to Elijah's own distribution (LOW CONFIDENCE at n≈94).
- **L6 — review past proposals** — which prior proposals were accepted, and did they actually improve the next grade? The loop grading itself.
- **L7 — propose edits to other skills** — turn outcome patterns into SKILL.md improvement proposals for sibling skills.

## The golden rule

**Propose, never auto-apply.** This loop NEVER edits a production engine
(`metrics2026.py`, `refresh.py`, `dashboard.html`, `intel/*.py`). Every real
change is a `docs/plans/*.md` draft (from `docs/templates/SELF-IMPROVE-PROPOSAL.md`)
routed through the **dev-workflow** skill with Elijah's explicit accept.

The only safe auto-writes:
1. The append-only ledger in `self-improve/data/` (what `grade.py` writes).
2. `category_override` data fixes in store.json (data, not engine logic).
3. One dated learning appended to `team/memory.md`.
4. `intel/*.json` watchlist suggestions.

**Honest-gate:** if a proposed change doesn't beat baseline on held-out data,
ship nothing and say so. "No change is warranted" is a complete answer.

## Note on `self-improve/data/`

`self-improve/data/` is **gitignored generated output** — the grade ledger is
regenerable from store.json by re-running `grade.py`. Do not commit it. (The
`.gitignore` entry mirrors `ig-dashboard/data/` and `intel/data/`.)
