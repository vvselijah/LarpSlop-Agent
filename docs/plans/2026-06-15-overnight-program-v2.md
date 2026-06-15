# OVERNIGHT PROGRAM v2 — 2026-06-15 (Self-Learning + Vault Mine + Build-Out)

> **What this is.** The plan for the next autonomous overnight run, modeled on the proven
> `2026-06-14-overnight-program.md` structure. Three headline mandates from Elijah:
> **(1)** build a *self-improving, recursive self-learning* skill for these repos;
> **(2)** an entire section that mines the Obsidian vault — every idea + every saved repo —
> for feasibility, repo-matches, and add/not verdicts; **(3)** general research for anything
> that helps the work or the repos. Plus: actually **execute** the already-researched
> ADD-NOW build queue so the night ships code, not just plans.
>
> **Status legend:** ✅ done · 🟡 built/unreviewed · ⚑ needs Elijah · 🤖 autonomous-safe.
> **Today:** 2026-06-15. **Prior baton:** `SESSION-COMPACT-2026-06-14.md`.

---

## 0. OPERATING RULES (autonomous — do not violate)

Carried verbatim from the 2026-06-14 program (held clean all night, never throttled):

- **Throttle safety:** ONE Workflow at a time, **≤5 concurrent agents** (`docs/RESEARCH-PROTOCOL.md`).
  exa/tavily/firecrawl keys are dead in-process → agents use **WebSearch/WebFetch**. If agents start
  returning null (load-shed), back off — widen the gap between waves, don't relaunch the fan-out.
- **Build only SAFE, reversible, LOCAL things** (scripts / skills / plan docs / data configs).
  Verified builds → local commits. **Do NOT push** unless Elijah says so.
- **Never:** publish/post/DM, spend money, install multi-GB deps (GPU/torch-cu128, big models),
  put secrets in files, make irreversible vault edits, or **auto-edit a production engine**.
  Production-engine changes are PROPOSED as `docs/plans/*.md` diffs for dev-workflow review.
- **Vault is READ-ONLY tonight** (Standing Rule 6 + "never tidy"). Mining = read + inventory +
  feasibility notes written to `docs/plans/`, never edits inside `obsidian/`.
- Each researched item → a plan doc `docs/plans/2026-06-15-<id>-*.md`. Roadmap + morning
  briefing generated at the end (Wave 5).
- **Environment:** run python/ffmpeg via **PowerShell** (not Bash); keep heavy models OFF the
  OneDrive tree; graph.facebook.com calls via `curl.exe --config -` (token off argv).

## 0b. ALREADY DONE — do NOT re-research / re-build

The 2026-06-14 run already tiered **30 candidates** (ADD-NOW/LATER/SKIP, web-cited) and **built 6
modules**. Treat those verdicts as settled (re-open only if priorities changed):

- **Built + committed (now PUSHED through `800058e`):** `metrics2026.py`, `watchtime_ideator.py`,
  `auto-clip/library.py`, `intel/viral-radar.py`, `intel/news-radar.py`, `content-intel-2026` skill
  (+ the full auto-clip pipeline: highlight/caption/facetrack/tighten).
- **Production tweak shipped today (`1c8743b`):** `refresh.py` now ingests `reels_skip_rate`+`reposts`
  (normalized ÷100) → **metrics2026 skip-gate is LIVE** (94/300 posts have skip data; `--full` backfills the rest).
- **SKIP'd (do not revisit unless asked):** gethookd.ai, literal auto-clone account, FinceptTerminal,
  dropship-character store, github/spec-kit, addyosmani/agent-skills install, self-built community site.
- The pending **ADD-NOW build queue** from that run is Wave 3 below (we execute it, not re-plan it).

---

## WAVE 1 — 🤖 THE SELF-LEARNING SKILL  *(headline build)*

**Goal:** make the hub measurably smarter every day by closing prediction→outcome loops and
**proposing** (never auto-applying) improvements to its own heuristics, skills, and strategy.
"Recursive" = it also grades and improves *itself* and the *other* skills.

### 1.1 Why this is buildable now (not aspirational)
The recon found the hub is already a predict→observe substrate — it just never closed the loop:
- **Predictions** are made by deterministic engines with hardcoded tunables (metrics2026 score+weights,
  skip-gate, watchtime arbitrage, trend/competitor/viral fires, news score, `categorize()`, Higgsfield
  virality, auto-clip highlight rubric).
- **Outcomes** are already stored: `ig-dashboard/data/store.json` (300 posts + per-post `history[]`
  velocity snapshots + daily follower/non-follower split + `follower_snapshots`), plus accruing intel
  histories (`competitors.json`, `viral.json`, `trend-history.json`, `news.json`).
- **The loop was literally designed and abandoned:** `abc wrap/analysis/predictor-vs-actual.md` exists
  with a header schema and a "≥5 rows → start trusting/distrusting" rule — but is **empty (`_none yet_`)**.

So this skill *activates dormant infrastructure* rather than inventing it.

### 1.2 The five closed loops (ranked by leverage ÷ risk)

| # | Loop | Reads | Proposes (gated) | Write-safety | Min-sample gate |
|---|------|-------|------------------|--------------|-----------------|
| **L1** | **metrics2026 weight + skip-threshold recalibration** *(highest leverage)* | store.json rates+history+daily split; `metrics2026.py:56-60` | new `WEIGHTS` dict + `SKIP_*` thresholds that best rank-correlate score↔realized reach/retention | `docs/plans/*-metrics2026-recalibration.md` diff only — **never edits the .py** | held-out split; flag that skip-n=94 is borderline |
| **L2** | **Higgsfield-predictor trust** *(feed the empty ledger)* | `predictor-vs-actual.md`, `ig-performance-baseline-*.md`, store insights, Higgsfield logs | append 1 row/published reel; after ≥5 rows, a trust-weight ("discount creative score by X when hook-type=Y") | **append-only ledger** (safe auto-write) + 1 memory learning | ≥5 published-reel rows before any verdict |
| **L3** | **`categorize()` keyword-drift** *(cleanest mechanical loop)* | store.json captions + assigned `category`; `refresh.py:52-64` | keyword add/remove list; per-post `category_override` for clear mislabels (e.g. DoorDash→Faith) | `category_override` is **data, not code** → safe auto-write; keyword edits → plan diff | sample audit; only override unambiguous cases |
| **L4** | **watchtime-arbitrage backtest** | `data/watchtime-ideas.md`, store history for newly-posted reels, `team/memory.md` | confirm/retract each "post more X / less Y" call against realized hold | memory learning only (directional, never a guarantee) | ≥3 in-category posts (mirror `MIN_N=5`) |
| **L5** | **trend/competitor/viral threshold self-tune** *(lowest priority — partly self-correcting)* | `trend-history.json`, `competitors.json`, `viral.json` | nudge `RATIO_THRESH`/`BREAKOUT_X`/`OVERPERFORM_X`; promote viral-radar's auto-emitted watchlist adds into a tracked accept/reject set | plan diff + `intel/*.json` watchlist (data) | false-positive rate over ≥14 days history |

### 1.3 The recursive / meta tier  *(this is the "recursive self-learning" part)*
- **L6 — self-review:** the skill reads its OWN past proposals (`docs/plans/*-self-improve-*.md`) →
  were they accepted? did accepted changes actually improve rank-correlation on the next window? →
  tune its own grading rubric and confidence calibration. Logs what it changed *about itself*.
- **L7 — cross-skill improvement:** from outcome patterns, propose edits to *other* skills' guidance
  (e.g. "save-heavy winners share trait Z → carousel-builder should lead with Z"; "AI/Tech holds
  17.5s vs Motivation 8.3s → weekly-content-plan should reweight the mix"). Proposals only.

### 1.4 What gets built (Wave-1 deliverables)
- 🤖 `self-improve/grade.py` — deterministic, **read-only**, pure-stdlib grader. Computes: Spearman
  rank-correlation(metrics2026 score, realized reach & avg-watch-time) over a held-out split; skip-gate
  calibration; category-audit candidates; arbitrage hit-rate. Emits `self-improve/data/grade-<date>.json`
  + a human-readable `grade-report.md`. CLI + `--self-test` (match hub engine style).
- 🤖 `.claude/skills/self-improve/SKILL.md` — the **Claude-is-the-brain** orchestrator: run grader →
  interpret → draft proposal docs → append memory learnings → run L6/L7 self/cross review. Trigger
  phrases: "self-improve", "close the loop", "grade the predictions", "what should we tune", "learn from the data".
- 🤖 `docs/templates/SELF-IMPROVE-PROPOSAL.md` — proposal schema (old→new value, evidence, held-out
  delta, confidence, accept/reject checkbox for Elijah).
- 🤖 Seed `predictor-vs-actual.md` with the first real rows from the 94 skip-rate posts (back-fill L2).
- ⚑ **Proposed (dev-workflow gated):** append a nightly read-only grader pass to `Daily Agent Refresh.bat`
  so the loop runs at the 7 AM cadence and stages a proposal — left as a plan diff for Elijah (touches the
  scheduled-task chain).

### 1.5 Golden constraint (non-negotiable)
**Propose, don't apply.** The only auto-writes allowed: the append-only `predictor-vs-actual` ledger,
`category_override` data fixes, `team/memory.md` learnings, and `intel/*.json` watchlist suggestions.
**Every production-engine code change is a `docs/plans/*.md` diff routed through dev-workflow + Elijah.**
Honest-gate: if a proposed change doesn't beat baseline on held-out data, **ship nothing and say so.**

---

## WAVE 2 — 🤖 VAULT DEEP-MINE + FEASIBILITY  *(Elijah's big section)*

**Goal:** go through *every* idea and *every* saved repo in the Obsidian vault and answer, per item:
**can we build/do it? what repos/tools would help? should we add them?** Output:
`docs/plans/2026-06-15-vault-feasibility.md` (read-only; nothing written inside `obsidian/`).

### 2.1 Feasibility rubric (applied to each of ~50 vault ideas)
For each idea record: **Verdict** ∈ {Build-now 🤖 / Phase-0 spike / Needs-Elijah ⚑ / Venture-scale /
Content-only / Skip} · **Effort** · **What it needs** (data/API/dep/decision) · **Helpful repo or tool**
(from the saved list or new) · **Add the repo? Y/N + why** · **Composes with** (existing hub engine/skill).
Carry forward the prior run's lessons: *a vault note's framing is a hypothesis, not the scope — find the
cheapest slice; split at the measure/generate seam; verify the API exposes a named metric before promising it.*

### 2.2 First-cut triage of the vault inventory  *(grounding — the run does the deep per-item pass)*
The recon catalogued ~50 ideas across `Brainstorming/`, `Research/`, `To do general/`,
`me and tanner cooking/`, `40-Projects/{LarpSlop,Labeltrust,Artifacial,Infinet,Archetype-Index}/`,
`20-Content/Ideas/`. Pre-bucketed (the overnight run validates + details each):

- **Build-now / Phase-0 (hub-shaped, autonomous-safe):** personal-name SEO/authority engine (idea #3) ·
  content-analysis→longform feeder (#14, overlaps watchtime_ideator — extend it) · unbiased AI-news→vault
  (#13, already shipped as `news-radar.py` → wire its output into vault idea-notes) · trial-reel A/B (#34 = Wave-3 build) ·
  Labeltrust "social-ad analyzer" (#26) + "speculation meter" (#29) as standalone analyzer skills ·
  reverse-engineer omnipresent ads (#12, read-only ad-spy = a prior ADD-LATER Phase-0).
- **Needs-Elijah ⚑ (decision/credential/creative gate):** Kajabi-replacement / community platform (#6 — prior verdict: BUY Whop/Skool, don't self-build) ·
  ManyChat-alt DM responder (#11 — ~30min app-config Phase-0 unblocks it) · clipping-campaign rollout (#43 — agency contacts) ·
  music re-upload (#44) · Champagne Lance / Derwin collabs (#45, #21) · in-person events + "Meet Your Cofounder" (#16/#17) · live project-grading stream (#18 = Wave-3 rubric skill).
- **Venture-scale (out of hub center-of-gravity — slice only):** "SaaS for AI agents" (#5 — content series ✅, product ⚑) ·
  dropship w/ Lexi (#8) · proprietary virality ML (#10 — prior verdict: tiny sklearn spike that likely ships nothing) ·
  full Labeltrust redesign (#22-#33 — that's its own repo `C:\Users\elija\dev\labeltrust`, evaluate which features the hub can *assist*, not own).
- **Content-only (feed carousel-builder / weekly-content-plan):** ideas #35-#42, #49, #50 (the 2026 IG-algo + Meta-Andromeda research notes are intel, already partly absorbed by metrics2026).
- **Skip / joke:** "Zombie GPT" misinformation swarm (#42 — flagged "dumb shit").

### 2.3 Saved-repo evaluation  *(the "cool repos to checkout" note + others)*
Prior run already SKIP'd FinceptTerminal, addyosmani/agent-skills, github/spec-kit. **New repos to evaluate
this run** (feasibility + "add to the hub? Y/N"):

| Repo | Why it's interesting | Eval focus |
|------|----------------------|-----------|
| **EvoMap / evolver** (`github.com/EvoMap/evolver`, evomap.ai) | Elijah tagged it "agentic recursive learning?" | **Directly relevant to Wave 1** — does its approach improve our self-improve skill design? Adopt patterns or skip. |
| **opendataloader-pdf** | ~100 pg/sec CPU PDF→Markdown+OCR, Apache-2.0 | Useful for Labeltrust research vaults + any doc ingestion; light dep → likely ADD. |
| **OpenWA** (self-hosted WhatsApp API) | unlimited msgs, Docker, MIT | Ties to DM/ManyChat-alt thesis — but Docker/OneDrive friction; eval as ⚑. |
| **train-llm-from-scratch** | consumer-HW GPT training | Feeds the "proprietary ML model" idea — prior verdict says sklearn-not-LLM; likely educational-only. |
| **motion / motion.dev** | animation lib | "3D motion-graphic vids w/ Claude" — overlaps HyperFrames/Remotion already installed; eval for redundancy. |
| **codecrafters build-your-own-x**, **ASCILINE**, **Telegram-Drive**, **CloakHQ/cloakbrowser** | misc | quick triage: relevance to content/agency/infra vs novelty; most likely "interesting, not now." |

Deliver a single table: repo · what it does · would it help (which hub goal) · **ADD / LATER / SKIP** + reason.

---

## WAVE 3 — 🤖 EXECUTE THE PENDING ADD-NOW BUILD QUEUE

These were researched + tiered ADD-NOW last run but not built. All autonomous-safe, draft/read-only,
zero-dep. Build + test + local-commit each (don't push):

1. 🤖 **`ig-dashboard/trial_ab.py`** — trial-reel A/B *measure* half: group A/B variants, score on 2026
   signals via `metrics2026.rank_posts()` (import unchanged), declare a winner with an honesty gate.
2. 🤖 **`artifacial-workshop-ad-ideator` skill** — `intel/artifacial-tools.json` + SKILL.md; fans over
   artifacial.io tools → one analytics-grounded ad concept per tool as vault idea-notes (zero ad spend).
3. 🤖 **`live-software-review` skill** — scoring rubric (Quality 25 / Looks 20 / Virality 20 /
   Pro-fix 20 / Performance 15) + show-prep SKILL for the recurring "grade my software" live w/ Tanner.
4. 🤖 **`saas-for-agents` content-series note** — one vault idea-note w/ verified 2026 agent-economy rails.
5. 🤖 **viral-radar Phase-2** — wire a Claude-as-analyst "why it works" teardown into `niche-intel`.
6. 🤖 **`ai-article-broll-creator` Phase-0 planner** — `broll-plan.json` (auto-assemble OFF).
7. 🤖 **`meta-stats-opensource-app` slices A+B** — MIT OSS template + Obsidian dashboard note (gitignore
   real account data first — it's already covered by `ig-dashboard/data/`).

*(Each ships only if it passes its own test on live data; otherwise it's logged as a plan, not a build.)*

---

## WAVE 4 — 🤖 GENERAL / NEW RESEARCH  *(net-new territory)*

Not the old 30. New questions that help the work or the repos (≤5 agents, WebSearch/WebFetch, cited):

- **Agentic self-improvement state of the art (2026):** EvoMap/evolver + comparable "self-improving agent"
  / agent-memory / reflexion frameworks — what's worth grafting into the Wave-1 skill? (feeds L6/L7.)
- **New/changed MCPs & Claude-Code skills since 2026-06-14** worth adding (the prior run pinned Metricool
  Tier-A pending Elijah; check for anything new in scheduling/analytics/agent-memory).
- **IG 2026 algorithm deltas** since the Incarnati teardown — any new public signal/metric Meta exposed
  (we just found `total_views/total_likes/total_comments/link_clicks` in v22.0 — research if any are
  worth ingesting next, like the skip-rate win).
- **Idea-feeding research for the top Build-now vault items** (e.g., name-SEO authority tactics;
  social-ad-analyzer heuristics for Labeltrust; what data a virality model would actually need).
- **One "what would most help these repos" sweep** — the prior run's recurring lesson is *intel→idea,
  not new tools*; pressure-test whether that still holds or a genuinely new capability gap exists.

---

## WAVE 5 — SYNTHESIS (generated at end of run)

Match the proven 5-artifact output:
1. **Roadmap** `docs/plans/2026-06-15-overnight-roadmap-v2.md` — tiered tables (ADD-NOW/LATER/SKIP) for the
   vault ideas + new repos + new research, with a "Suggested BUILD ORDER" and dependency prose.
2. **Morning briefing** `docs/plans/2026-06-15-MORNING-BRIEFING.md` — 2-min wake-up: what shipped (table),
   3 data-grounded findings to act on, the self-improve skill's first proposals, "one thing only you can do".
3. **Per-item docs** `docs/plans/2026-06-15-<id>-*.md` for each researched item.
4. **Session compact** update at repo root.
5. **`team/memory.md`** — one dated learning (Rule 7).

---

## EXECUTION MODEL & MORNING DELIVERABLES

- **How it runs:** sequential Waves; within a wave use a single Workflow with ≤5 concurrent agents
  (pipeline where stages are independent). Wave 1 (self-improve build) and Wave 3 (queue builds) are
  build-then-test-then-commit; Waves 2/4 are research→synthesis. One workflow at a time.
- **Estimated scope:** comparable to the ~6h 2026-06-14 run; cost is not a constraint (Elijah's stance).
- **By morning Elijah gets:** the self-improve skill (built+tested), its first batch of *proposals*
  (metrics2026 recalibration, category fixes, predictor-ledger seed), the full vault-feasibility doc with
  per-idea verdicts + repo add/skip table, the executed ADD-NOW builds (local commits), new-research docs,
  and the roadmap + briefing.
- **⚑ Needs-Elijah after the run:** approve/reject the self-improve proposals (dev-workflow); decide which
  Wave-3 builds to push; the credential/creative-gated vault items (DM app-config, Kajabi buy-decision,
  collab outreach, milestone reel). Nothing publishes, spends, or edits a production engine without him.

### Open question for Elijah before kickoff
- **Push policy:** push each verified build as it lands, or hold all for one review like last time?
- **Scheduled-task wiring:** OK to *propose* (not apply) adding the nightly grader to `Daily Agent Refresh.bat`?
- **Scope dial:** run the full 5 waves, or self-improve skill + vault mine first and defer Waves 3-4?
