# Research: Proprietary virality / behavior-prediction ML model on Elijah's own content data

- **Date:** 2026-06-14
- **Candidate id:** `proprietary-virality-ml-model`
- **Source of the ask:** vault `Brainstorming/In the moment ideas.md` — "build my OWN behavior/virality-prediction model on my content-analysis data via local LLM-training repos, distinct from the agent-based audience-sim."
- **Status:** research only (no code). Decisive verdict below.

---

## Headline verdict: ADD-LATER (small, sklearn baseline) — and explicitly SKIP the "local LLM-training repo" framing of the ask

**Build a tiny scikit-learn baseline ranker, not a trained deep/LLM model. And not now — after `metrics2026.py` and the audience-sim Phase-0 spike, because all three feed the same scoring line and a model is only worth it once the 2026 label contract is proven against real saved/skip data.**

The honest read, point by point:

1. **The literal ask ("local LLM-training repos") is the wrong tool for this data and should be declined.** Fine-tuning a local LLM to predict a virality score needs ~**1,000 examples minimum per task** as an absolute floor; below that the model **memorizes/regurgitates** training rows instead of learning ([Dialzara](https://dialzara.com/blog/fine-tuning-llms-with-small-data-guide), [Latitude](https://latitude.so/blog/dataset-size-impacts-llm-fine-tuning)). Elijah has **n=300**. An LLM fine-tune here would be slow, torch-heavy (the OneDrive hang risk), commercially licensable-or-not depending on the base model, and **worse** than a 30-line sklearn baseline. Multiple sources land on the same conclusion: *for small-dataset regression, standard sklearn with thoughtful feature engineering is more practical than an LLM fine-tune* ([Google ML crash course](https://developers.google.com/machine-learning/crash-course/llm/tuning)).

2. **For n=300 tabular data, gradient-boosted trees / a tabular foundation model beat deep learning — this is settled 2024-2026 consensus.** GBDTs (XGBoost/LightGBM/CatBoost and sklearn's `HistGradientBoosting`) "frequently exceed the performance of deep learning models" on small tabular data; deep nets "need oceans of data" and overfit ([Towards AI](https://towardsai.net/p/l/tabular-learning-gradient-boosting-vs-deep-learning-critical-review), [ScienceDirect — "Deep learning is not all you need"](https://www.sciencedirect.com/science/article/abs/pii/S1566253521002360)).

3. **n=300 is a hard ceiling on model complexity, and the viral class is even smaller.** The standard rule of thumb is **~10 positive events per predictor** to avoid overfit ([PMC sample-size review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8905023/)). 300 rows caps usable features at ~30 *if* the target were balanced — but "viral" reels are a small minority of the 300, so the effective positive count is far lower. k-fold CV on small n produces **strongly optimistic, biased** accuracy estimates unless done carefully (nested CV) ([PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224365)). Any reported accuracy must be treated with suspicion until it survives a held-out / nested-CV check.

4. **The honest baseline question — does a trained model even beat the thing you already built?** `metrics2026.py` is already a hand-weighted ranker (share 40 / like 25 / save 20 / repost 10 / comment 5, skip-rate gate) over percentile ranks. That **is** the no-ML baseline. A trained model only earns its slot if it beats that ordinal baseline (and beats "Claude-reads-the-caption-and-scores-it") on a held-out split. On 300 rows that is **not a given** — quite plausibly it does not, and the right answer is to keep `metrics2026.py` + Claude-as-evaluator and not ship a model at all. The plan below is structured to **kill the idea cheaply in Phase 0** if the model can't beat the baseline.

So: this is a *worth-a-2-hour-spike* idea, not a *go-build-it* idea, and it is the **sklearn line of the scoring story**, not a second LLM project.

---

## What it actually is (and is not)

**The ask, restated honestly:** a supervised model that learns, from Elijah's 300 past reels, a function `caption/metadata features -> predicted 2026 score (or "will this beat my median")`, so a draft hook can be scored *before* posting.

**Distinct from audience-sim** (`docs/plans/2026-06-13-audience-sim-pipeline.md`): audience-sim is a generative LLM *simulation* — spin up persona-agents, read qualitative reactions/objections, no numbers. This candidate is the *quantitative* counterpart — one trained regressor/classifier emitting a scalar from his real labels. They are complementary points on the **same scoring line**: `metrics2026.py` (past, no ML) -> this model (cheap learned prior) -> audience-sim (qualitative pre-publish) -> Higgsfield (rendered-clip craft). Do **not** re-litigate audience-sim here; this is the lightweight numeric sibling.

**Training data on disk (verified 2026-06-14):** `ig-dashboard/data/store.json`, 300 posts (all `media_type=VIDEO`/reels, all have captions). Per-post fields present: `caption`, `category`, `like_count`, `comments_count`, `timestamp`, and `insights{reach, saved, shares, views, total_interactions, ig_reels_avg_watch_time, ig_reels_video_view_total_time}`. **Label/target contract** = `metrics2026.py`'s `score_2026()` (skip > share > save), so the labels already exist — that's exactly why "now" is timely. **Caveat baked into the contract itself:** `reels_skip_rate` and `reposts` are **not yet in the store** (metrics2026 degrades the skip gate to neutral), so the headline 2026 signal — skip-rate — is currently a constant the model cannot learn from. That is a real limiter (see Risks).

**Best 2026 OSS approaches, ranked for THIS host:**

| Tool | Fit for n=300 | Deps on this host | License | Verdict |
|---|---|---|---|---|
| **sklearn `HistGradientBoostingRegressor/Classifier`** | Excellent — research-consensus winner on small tabular; numba/pure-Python, parallel, native missing-value + categorical support ([sklearn docs](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html)) | **Already installed** (sklearn 1.9.0, numpy 2.4.4, scipy 1.17.1, joblib 1.5.3). **No torch.** | BSD-3 | **CHOSEN baseline** |
| XGBoost / LightGBM / CatBoost | Also excellent; marginally better tuned | New C++/wheel dep (not installed); adds weight for ~zero gain at n=300 | Apache-2 / MIT | Skip for v1 — sklearn already wins, don't add a dep |
| **TabPFN v2.5/2.6/3** (tabular foundation model) | Best-in-class on <10k rows, beats GBDT on small data ([Nature](https://www.nature.com/articles/s41586-024-08328-6), [Wikipedia](https://en.wikipedia.org/wiki/TabPFN)) | **Pulls torch**; CPU only ≲1000 rows (fine for 300) but the OneDrive torch-hang risk applies; needs license-token acceptance | **Default models are NON-COMMERCIAL** (TabPFN-3/2.6/2.5). Only the older v2 is Apache-2; v2.5+ requires a `TABPFN_TOKEN` + accepting a per-version license ([PriorLabs/TabPFN](https://github.com/PriorLabs/TabPFN), [Medium v2.5](https://rehoyt.medium.com/tabpfn-v2-5-an-even-better-algorithm-68b72c6be5d5)) | **SKIP** — non-commercial license is a hard blocker for a paid creator's pipeline; torch dep + token gate add friction for a marginal lift. Watchlist only if v2-Apache is ever enough. |
| Local LLM fine-tune (the literal ask) | **Poor** — needs ~1k+ examples, memorizes at n=300 | torch + multi-GB model off-disk | base-model dependent | **DECLINE** — wrong tool, see verdict #1 |

**On caption text features:** the captions are the richest signal, but turning them into embeddings normally pulls `sentence-transformers` (**not installed** — would add a torch-backed heavy dep). For v1, **do not** embed: reuse `ig-dashboard/refresh.py`'s existing `categorize()` + `CATEGORIES` (confirmed at lines 48 / 115) for the niche one-hot, plus cheap stdlib text stats (length, has-number, has-question, emoji/hook-word flags, hour-of-day, day-of-week). That keeps v1 **zero new dependencies**. Embeddings are a Phase-2-only experiment, gated on the baseline proving worthwhile.

---

## Integration sketch (how it composes with the hub)

**Lives as:** a new `predict.py` **inside `ig-dashboard/`** (NOT a new top-level engine). It is the read-side sibling of `metrics2026.py` and shares its target. House idioms: `BASE = Path(__file__).resolve().parent`, reads `data/store.json` read-only, writes a model artifact to `ig-dashboard/data/`, `log()` helper, stdlib-first.

```
ig-dashboard/data/store.json  (300 posts: caption, category, insights{reach,saved,shares,views,watch_time})
        │
        ▼  featurize()  — reuse refresh.py categorize()/CATEGORIES + stdlib text/time stats (NO embeddings v1)
   X = [niche one-hot, caption_len, has_number, has_question, emoji_ct, hook_word_flag, hour, weekday, ...]
   y = metrics2026.score_2026(post)   ← label contract ALREADY defined; import it, don't fork it
        │
        ▼  train  (sklearn HistGradientBoostingRegressor, nested/held-out CV)
        │
        ▼  EVALUATE vs baselines  ── Spearman(model_rank, true_2026_rank) on held-out split
        │     baseline A: metrics2026 itself (the hand-weighted ranker)
        │     baseline B: Claude-as-evaluator scoring the caption cold
        │   GATE: model must beat BOTH on held-out data or it does not ship.
        ▼
   data/virality_model.joblib  +  report (top feature importances = "what your audience rewards")
        │
        ▼  (only if it beats baselines)
   score_draft(caption, niche) -> predicted 2026 percentile
        → optional confidence note in weekly-content-plan / carousel-builder, beside audience-sim + Higgsfield
```

**Reuses (searched the tree — exist, don't reinvent):** `metrics2026.score_2026()` / `rates()` / `build_distributions()` for labels; `refresh.py` `categorize()` + `CATEGORIES` for niche features; `log()` pattern; `data/` dir convention. **Highest-value *non-prediction* output:** even if the predictor never beats baseline, **feature importances** ("number-in-hook and Money/Finance niche correlate with high 2026 score; long captions hurt") are a genuinely useful, honest, explainable read of his own history — arguably the real deliverable.

---

## Phased build sketch (proof-first; each phase can kill it cheaply)

**Phase 0 — SPIKE (~2h, throwaway, gate: "does a model beat `metrics2026` + Claude on held-out data?")**
1. Throwaway script: load `store.json`, `featurize()` with stdlib + `categorize()` only (no new deps), `y = score_2026(post)`.
2. Train `HistGradientBoostingRegressor`; evaluate with a held-out split (and nested CV given small n) — report Spearman vs the true 2026 rank.
3. Compare against **baseline A** (`metrics2026` ranking) and **baseline B** (Claude scoring 20 held-out captions cold).
4. **Decision gate:** if the model does **not** clearly beat both → **STOP, log the dated learning, ship nothing.** Keep `metrics2026` + Claude-as-evaluator. (This is the most likely outcome and that's fine.) Print feature importances regardless — they may be the only keeper.

**Phase 1 — PRODUCTIONIZE (only if Phase 0 beats baselines)**
5. Scaffold `ig-dashboard/predict.py` properly: `featurize()`, `train()`, `evaluate()`, `score_draft()`; persist `data/virality_model.joblib`; write a markdown importances report. Pure sklearn, zero new deps. One commit per function-group (dev-workflow).
6. Retrain hook: re-fit after the daily `refresh.py` run only when the store grows by N posts (avoid daily-noise refits on a near-static dataset).

**Phase 2 — ENRICH (optional, gated, each its own go/no-go)**
7. **First fix the label, not the model:** add `reels_skip_rate` + `reposts` to `refresh.py` so the model can actually learn the #1 2026 signal (today skip-rate is a constant). This is higher ROI than any model upgrade.
8. Only then consider caption embeddings (adds `sentence-transformers`/torch — weigh the OneDrive hang risk) and, if ever, the Apache-2 TabPFN-v2 as a benchmark. Each gated on a measured lift over the sklearn baseline.

---

## Risks / gotchas (honest)

- **Most likely outcome: the model does not beat the baseline, and that's the correct finding.** n=300 with a rare positive class is genuinely small; the hand-weighted `metrics2026` + Claude-as-evaluator may simply win. Phase 0 is designed to surface this in 2 hours, not after a build.
- **The headline 2026 signal isn't in the training data yet.** `reels_skip_rate`/`reposts` are absent from the store (metrics2026 neutralizes the skip gate), so v1 trains on share/like/save/comment only — it cannot learn the skip-rate driver that the 2026 algorithm prioritizes most. Fixing `refresh.py` ingestion (Phase 2 step 7) is the real unlock and should arguably precede any model.
- **Optimistic-accuracy trap.** Small-n k-fold over-reports accuracy ([PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224365)); use a held-out test set / nested CV and never quote in-sample numbers.
- **Reflexivity / leakage.** `views/reach/saves` are *outcomes*; only **pre-publish-knowable** features (caption, niche, planned post-time) may be inputs, or the model "predicts" by peeking at the answer. Featurize must exclude all post-hoc insight fields from X.
- **torch on the OneDrive disk.** A one-shot `import torch` succeeded here (2.11.0+cpu) but MEMORY.md warns heavy torch/cv2 imports hang on the synced disk — the sklearn path deliberately avoids torch entirely; keep it that way for v1.
- **Don't add a new top-level engine.** This is a `predict.py` inside `ig-dashboard/`, sharing `metrics2026`'s contract — not a fourth root engine.
- **Compliance / ToS / ban risk: essentially none.** Pure local training on data Elijah already owns via the official Graph API; read-only; never publishes. No scraping, no paid scraper, no new account risk. The only license trap is **TabPFN's non-commercial default models** — avoided by choosing sklearn (BSD-3).

---

## Sources

- [Tabular Learning — Gradient Boosting vs Deep Learning (Towards AI)](https://towardsai.net/p/l/tabular-learning-gradient-boosting-vs-deep-learning-critical-review)
- [Tabular data: Deep learning is not all you need (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S1566253521002360)
- [Accurate predictions on small data with a tabular foundation model — TabPFN (Nature)](https://www.nature.com/articles/s41586-024-08328-6)
- [PriorLabs/TabPFN (GitHub) — install, license, CPU/size limits](https://github.com/PriorLabs/TabPFN)
- [TabPFN v2.5 license/token notes (Medium)](https://rehoyt.medium.com/tabpfn-v2-5-an-even-better-algorithm-68b72c6be5d5)
- [TabPFN (Wikipedia)](https://en.wikipedia.org/wiki/TabPFN)
- [sklearn HistGradientBoostingRegressor docs](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html)
- [Histogram-Based Gradient Boosting in Python (MachineLearningMastery)](https://machinelearningmastery.com/histogram-based-gradient-boosting-ensembles/)
- [Fine-tuning LLMs with small data — pitfalls (Dialzara)](https://dialzara.com/blog/fine-tuning-llms-with-small-data-guide)
- [How dataset size impacts LLM fine-tuning (Latitude)](https://latitude.so/blog/dataset-size-impacts-llm-fine-tuning)
- [LLM tuning vs alternatives (Google ML Crash Course)](https://developers.google.com/machine-learning/crash-course/llm/tuning)
- [Machine learning models and over-fitting considerations (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8905023/)
- [ML algorithm validation with limited sample size (PLOS One)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224365)
- [Predicting Post Virality with Temporal Cross-Attention (arXiv)](https://arxiv.org/abs/2605.02358)
- [ViralBERT: BERT-based virality prediction (arXiv)](https://arxiv.org/pdf/2206.10298)

---

*Adjacent plans (do not re-litigate): `docs/plans/2026-06-13-audience-sim-pipeline.md` (qualitative LLM sim), `docs/plans/2026-06-14-ig-2026-algorithm-metric-engine-research.md` (the label contract). This candidate is the lightweight numeric sibling on the same scoring line.*
