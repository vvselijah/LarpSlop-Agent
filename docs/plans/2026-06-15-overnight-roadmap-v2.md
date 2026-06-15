# Overnight master roadmap v2 — 2026-06-15 (Wave 5 synthesis)

Single prioritized roadmap for the 2026-06-15 autonomous run (the *self-learning + vault-mine +
build-out* night). Synthesizes tonight's deliverables — the **self-improve grader** (Wave 1), the
**50-idea + 13-repo vault feasibility mine** (Wave 2), the executed **ADD-NOW build queue** (Wave 3),
and the **5-thread new-research** + **content-series** + **OSS-template** docs (Wave 4) — into one
tiered table + a build order. Honest read throughout: items are tiered on *value-to-Elijah*, not on
research novelty.

**Program baton:** `docs/plans/2026-06-15-overnight-program-v2.md`
**Prior roadmap (still authoritative for its 30 candidates):** `docs/plans/2026-06-14-overnight-roadmap.md`
**This run's headline:** the hub stopped only *scoring* and started *grading itself*. `self-improve/grade.py`
closed the predict→observe loop on `metrics2026.py` and produced the first held-out evidence that the
2026 score actually predicts reality (Spearman **+0.455** vs views, **+0.476** vs watch-time, held-out)
and that the skip-gate is **valid** (healthy 14.8k vs throttled 5.4k mean views). Everything else this
run hangs off that: the vault mine found the cheapest slice of all 50 ideas, the build queue shipped 6
new safe-additive artifacts, and the new-research wave found the *single highest-leverage* next move —
**close self-improve L2** by logging Higgsfield's pre-publish prediction so it can finally be graded.

---

## How to read this

- **ADD-NOW** — clear value, low/known effort, composes with something already live, no Elijah decision
  needed to *start*. Build is always a NEW file/skill/proposal-doc, never a production-engine edit.
- **ADD-LATER** — genuinely useful but an *enhancement* of an already-~covered gap, OR gated on a real
  blocker (a paid plan, a published-reel sample, a credential, a creative/ops decision). Plan stays warm.
- **SKIP** — low value for *this* creator, redundant with what the hub already has, or conflicts with the
  OneDrive / secrets / no-publish / official-API rails. Do not build; do not subscribe.

Hard constraint on everything: Windows + OneDrive-synced tree (no torch/cv2/heavy models on the synced
disk), secrets only in env vars, official APIs over paid scrapers, production engines are **PROPOSED as
`docs/plans/*.md` diffs, never edited in place**, and **Standing Rule 1 — never publish/post/DM without
per-action confirmation.** Many items here are *draft generators that stop before the publish click* —
that is by design, not a limitation to "fix".

---

## TIERED TABLE

Each row: **Tier | Item | Effort | Deps | Key gate / note | Source-doc.** "Composes-with" is folded into
the gate column to keep rows scannable. Built-tonight artifacts are marked **🔨 BUILT**.

### ADD-NOW — built tonight (Wave 3 build queue executed)

| Tier | Item | Effort | Deps | Key gate / note | Source-doc |
|---|---|---|---|---|---|
| **ADD-NOW** ⭐⭐ 🔨 BUILT | **self-improve grader** (`self-improve/grade.py` + README + `self-improve` skill) — the predict→observe loop: grades `metrics2026` against realized views/watch-time (held-out), validates the skip-gate, weight-searches with an honest-gate, audits categories | DONE (P0 shipped); follow-ons below | GREEN — pure stdlib, strictly read-only vs `store.json`/engines, `--self-test` passes, cp1252 `log()` | **The headline build.** First-ever grade of the hub's own model: held-out Spearman +0.455 (views) / +0.476 (watch-time); skip-gate HOLDS (healthy 14.8k > throttled 5.4k views). PROPOSE-only by golden rule — every change routes through `docs/templates/SELF-IMPROVE-PROPOSAL.md` → dev-workflow. Its proposals (weight-tune, 121 category-overrides) are *review items*, not auto-applied. | `self-improve/README.md` + `self-improve/data/grade-report.md` |
| **ADD-NOW** ⭐ 🔨 BUILT | **trial-reel A/B measure** (`ig-dashboard/trial_ab.py`) — groups variants, scores each on 2026 North-Stars via `metrics2026.rank_posts()`, declares a winner behind an honesty gate | DONE (measure half); generate+publish half = ADD-LATER | GREEN — stdlib over `store.json`, imports `metrics2026` UNCHANGED, read-only | Degraded correctly to the near-identical-caption heuristic (no `#abx_` tags/sidecar yet) → 46 fallback groups, `clean=False`, stricter **0.10 margin** flags borderline as inconclusive; produced **6 real winners** with both honesty-gate branches (reach floor + margin) firing on real data. | `2026-06-14-trial-reel-ab-method-research.md` |
| **ADD-NOW** ⭐ 🔨 BUILT | **artifacial-ad-ideator** (`.claude/skills/artifacial-ad-ideator/` + `intel/artifacial-tools.json`) — one analytics-grounded ad CONCEPT per Artifacial tool, drafted as a vault `idea` note | DONE | GREEN — agent-as-brain, zero deps, ZERO ad spend, draft-only | Catalog of **9 LIVE tools** (Face Swap, Image-to-Video, Motion Transfer, Character Swap, Lip Sync, Upscale, End-Frame Control, Motion Templates, Prompt Enhancer), all `verified:true` off the live site. Decoupled from the spend-gated executor — useful today. Mar-2026 "AI-generated" label reminder baked in. | `intel/artifacial-tools.json` + vault-feasibility #9 |
| **ADD-NOW** 🔨 BUILT | **live-software-review** (`.claude/skills/live-software-review/`) — show-prep skill for the recurring "grade my software live with Tanner" segment; scored rubric card + segment script + 60-sec recap | DONE | GREEN — agent-as-brain, zero deps, draft-only | Rubric weights sum to 100 (Quality 25 / Looks 20 / Virality 20 / Pro-fix 20 / Performance 15); valid YAML frontmatter, skill is selectable. Honesty gate: grade the work not the person, opinion-frame the subjective, every low score carries a fix. Stops at show-prep notes — never publishes. | `2026-06-14-live-software-review-format-research.md` + vault #18 |
| **ADD-NOW** 🔨 BUILT | **viral-teardown** (`intel/viral_teardown.py`) — consumes `intel/viral-report.md`, produces per-post teardown cards + a patterns section ("WHY they win") | DONE | GREEN — stdlib, read-only, `--self-test`, cp1252 `log()`; does NOT touch `viral-radar.py` | The "WHY they win" half of vault #20 (viral scraper), built as a downstream reader of the already-shipped `viral-radar` output — no scraper, no production-engine edit. 6 teardown cards + patterns generated. | `intel/viral-teardown.md` + vault #20 |
| **ADD-NOW** 🔨 BUILT | **broll-planner** (`auto-clip/broll_planner.py`) — article/paragraph → ordered visual-beat plan (`out/<stem>.broll-plan.json`), each beat `{beat, on_screen_text, suggested_visual, seconds}` | DONE (Phase-0 planner) | GREEN — stdlib, `--provider agent` two-step, mirrors `highlight.py`; no fetch/assemble (that's v2) | The Phase-0 planner half of the `ai-article-broll-creator` candidate — the storyboard brain only; per-beat stock-fetch (Pixabay/Pexels) + FFmpeg assemble stay deferred (auto-assembled stock slideshows are an anti-pattern in 2026; bias to Higgsfield/face-cam). | `2026-06-14-ai-article-broll-creator-research.md` + vault #22 |

### ADD-NOW — researched tonight, not yet built (the next safe queue)

| Tier | Item | Effort | Deps | Key gate / note | Source-doc |
|---|---|---|---|---|---|
| **ADD-NOW** ⭐⭐ | **Higgsfield trust-ledger** — close self-improve **L2**: append-only `self-improve/data/higgsfield-ledger.jsonl` draft-time logger + a stdlib grade-join sibling that reports `Spearman(hold_rate→realized avg_watch_time)` + `Spearman(hook_score→3s-retention proxy)`, emitting a trust-weight PROPOSAL | P0 ~½-day | GREEN — pure stdlib, read-only vs production, no spend/publish; one of the 4 permitted auto-writes (append-only ledger) | **The single highest-leverage new item this run.** The hub gates real editing on Higgsfield's Virality Predictor but never grades it — pre-publish hook quality is the **5–10× distribution lever** m26's post-hoc rates structurally can't see (today's grade tops at +0.455). Ground truth already in `store.json`. | `2026-06-15-new-research.md` (ADD ⭐⭐) |
| **ADD-NOW** ⭐ | **self-improve `ledger.py` sidecar + 3 SOTA grafts** — committed append-only `events.jsonl` (one line/grade run) + `capsules.json` (accepted-and-it-helped cases) → operationalizes the toothless **L6**; + anti-reward-hacking gate (beat baseline on a *majority* of k≥5 splits, not one); + two-stage adversarial review + explicit rollback contract | P0 ~½-day | GREEN — new file, stdlib, `--self-test`, cp1252 `log()`; **never touches `grade.py`** | Grafts EvoMap's validated mechanics (versioned assets + validate-before-apply) + Reflexion/CoALA memory + the 2026 reward-hacking literature. Do NOT graft evolver's autonomous Hub/network/leaderboard layer (offline-only posture). | `2026-06-15-new-research.md` (ADD ⭐) |
| **ADD-NOW** ⭐ | **category_override data-fix pass** — apply the grader's **121 flagged** mislabels (captions tagged "Other" that hit a category keyword, or straddling >1 category) via `category_override` in `store.json` | P0 ~1–2h | GREEN — data-only fix (`refresh.py:193` override mechanism), NOT engine logic; one of the 4 permitted auto-writes | Improves every downstream that reads category (watchtime arbitrage, content-intel, viral). Review the flagged list first (a few are genuine multi-category, not errors). Pairs with a CATEGORIES keyword-edit PROPOSAL for the recurring "Other" drift. | `self-improve/data/grade-report.md` §4 |
| **ADD-NOW** | **Labeltrust 3-detector classifier (Phase-0)** — additive explainable classifier (dropship / affiliate / baseless-claim) mirroring metrics2026 style: 3 sub-scores, each a weighted-boolean sum, output = label + triggered-signals-as-rationale | P0 ~½-day | GREEN — runs on metadata + OCR/transcript the app already has; reverse-image is v2 | Weight the baseless-claim detector hardest for baby/kids. **Verify-before-ship:** pull the full FTC **TruHeight** (Apr 2026) order + Health Products Compliance Guidance to enumerate exact prohibited phrasings before shipping the claim-bank. Labeltrust is its OWN repo (`C:\Users\elija\dev\labeltrust`) — the hub *assists*, doesn't own. | `2026-06-15-new-research.md` (ADD ⭐) |
| **ADD-NOW** | **name-SEO / entity-authority checklist** — per-person ("Elijah Sullivan" / "Tanner Carlson") setup checklist: own-domain + `Person` schema → Wikidata/LinkedIn/Crunchbase/GBP identical-NAP → `sameAs` wiring → cornerstone bio page | P0 ~½-day | GREEN — a `docs/plans/` doc, no spend, no publish | 2026 shift: establish an *entity* Google can categorize (Knowledge-Graph-trained Gemini/AI Mode), not "rank for a name". SERP push-down is a byproduct. Vault is read-only tonight → write to `docs/plans/`, Elijah places it. | `2026-06-15-new-research.md` (ADD ⭐) + vault #19 |
| **ADD-NOW** | **Basic Memory MCP adoption note** — local-first agent memory (no key/account/cloud, Markdown + `[[wiki-links]]` Obsidian reads natively, offline semantic search) | P0 ~2h (note + verify) | GREEN — privacy-correct for a OneDrive-synced, vault-running hub | **Verify the offline-search claim against the repo before wiring**, then a short `docs/plans/` adoption note. Aligns with secrets-in-env + vault-as-second-brain. Could back `team/memory.md`-style continuity. | `2026-06-15-new-research.md` (ADD) |

### ADD-NOW — content / vault items (zero-dep, draft-only)

| Tier | Item | Effort | Deps | Key gate / note | Source-doc |
|---|---|---|---|---|---|
| **ADD-NOW** ⭐ DEADLINE | **#35 social-followers-IRL milestone reel** — 10→100k crowd scale-reveal for the ~100k milestone, pure WebGL via the `three` skill in HyperFrames | P0 ~1–2h / P1 ~½-day | GREEN — no torch/cv2/keys; `InstancedMesh` = 100k figures in one draw call | **The only item whose value DECAYS** — worthless a week after the milestone. Ship the smallest postable version BEFORE 100k, then resume the metric cluster. Stops at a file in `out/`. | vault-feasibility #35 |
| **ADD-NOW** ⭐ | **saas-for-agents content series** — 5-part AI/Tech mini-series on the agent economy (DONE as a content plan tonight; execution = scripting each part) | XS — plan shipped; per-part scripting ~XS each | GREEN — content-ops, existing skills only | 5 parts each with HOOK+PAYOFF in his voice, per-part CTA/niche/format, "verified facts used" line. HARD anchors verified 2026-06-15 ($285B Feb-2026 selloff, Intercom $0.99/HubSpot $0.50, AP2, x402 ~165M tx); SOFT figures ("more agents than humans", $2T) deliberately NOT stated as fact. Route Parts 2&3 through `carousel-builder` (untapped saves). | `2026-06-15-saas-for-agents-content-series.md` |
| **ADD-NOW** | **EvoMap graft into self-improve L6** — give accepted proposals a stable versioned ID ("Gene"-like) so L6 can track which were accepted and whether they improved the next grade | XS — a SKILL.md bookkeeping convention | GREEN — zero EvoMap code; pattern only (GPL-3 + obfuscated core makes code reuse a non-starter) | Near-zero effort, sharpens the headline Wave-1 build. Folds into the `ledger.py` sidecar above. | vault-feasibility repos table (EvoMap row) |

### ADD-LATER

| Tier | Item | Effort | Deps | Key gate / note | Source-doc |
|---|---|---|---|---|---|
| **ADD-LATER** ⭐⭐ | **ingest real watch-time fields → `refresh.py` PROPOSAL** — `ig_reels_avg_watch_time` (ms→s) + `ig_reels_video_view_total_time` + per-reel `follows`/`profile_visits`; pair the new completion score with the existing skip-rate as a combined retention gate | PROPOSAL ~½-day to write | GREEN to plan; the EDIT is Elijah-gated | Watch-time is the **#1 2026 ranking signal** — currently only *inferred*. **Write `docs/plans/2026-06-15-ingest-watchtime-fields.md`; NEVER edit `refresh.py` in place.** The next skip-rate-tier win after tonight. | `2026-06-15-new-research.md` (ADD ⭐⭐) |
| **ADD-LATER** ⭐ | **weight-tune PROPOSAL** — adopt the grader's proposed `metrics2026.WEIGHTS` (held-out delta **+0.023** Spearman) | S — a one-line WEIGHTS edit via dev-workflow | gated on the anti-reward-hacking gate (don't trust one lucky split) | Grader PROPOSES share 0.40→0.286, repost 0.10→0.286, save 0.20→0.071 (corr +0.455→+0.478). Honest-gate passed but delta is small and from a single split → **route through the majority-of-k-splits stability check first** (see `ledger.py` graft). Do NOT auto-apply. | `self-improve/data/grade-report.md` §3 |
| **ADD-LATER** | **meta-stats OSS template** (`meta-stats-tracker/`) — de-personalize the 3 engines + viewer into an MIT public repo a stranger runs on their own IG account | A ~1 day / B ~30min / C SKIP | GREEN for A/B (stdlib, official read-only API) | **Plan complete tonight; gated on Elijah wanting a public repo.** The data scrub (A.3) + vendor license audit (A.4) are the blocking pre-publish chores; **fresh `git init`** is the safe way to guarantee no real account data (username/follower count/captions/media-ids all live in `data/`) enters history. SKIP the multi-tenant SaaS framing (C). | `2026-06-15-meta-stats-oss-template.md` |
| **ADD-LATER** | **vault dashboard note** (slice B) — nightly-refreshed `20-Content/IG Dashboard.md` mirroring `write_stats_md()` | ~30min once unblocked | gated on an Elijah vault-schema decision | **Blocking finding:** `dashboard` is a listed `type` but there is **no `_templates/dashboard.md`** → emitting metric *properties* would invent property names (contract-forbidden). Safe default = body-only metrics with `type/status/tags` frontmatter (zero-permission path). Elijah's call whether to create the template. | `2026-06-15-meta-stats-oss-template.md` (slice B) |
| **ADD-LATER** | **Metricool MCP** — official, write-capable, env-var auth; multi-platform scheduling + analytics + competitor data | wire-up S once gated | gated on a paid **Advanced** plan + Standing Rule 1 | The biggest tool-gap filler found, but distribution is a *downstream multiplier after you know what wins*, not the thing that tells you what wins. Write a `docs/plans/` proposal; verify current pricing first. Do NOT wire tonight. | `2026-06-15-new-research.md` (LATER ⭐) |
| **ADD-LATER** | **OASIS audience-sim pre-publish hook-ranker** (vault #7) — already an approved Phase-0 spike | P0 spike per the approved plan | UNPROVEN for IG until backtested vs the 300-post history | Clarify the unidentified "betta/miro fish repo" with Elijah. Pairs with metrics2026 + carousel-builder. | `docs/plans/2026-06-13-audience-sim-pipeline.md` + vault #7 |
| **ADD-LATER** | **DM Phase-0 unblock** (vault #11) — enable messaging product + `messages` webhook on the `mybrain` app, do ONE live human-approved send | ~30min (Elijah-actioned) | GREEN code-wise; the live send is Elijah's | DMing his OWN account is Standard Access (no App Review). Unblocks the `comment-triage`-pattern DM responder + DM-routing (#45). NEVER cold-outbound (2026 ban surface). | vault #11/#45 |
| **ADD-LATER** | **`link_clicks` reel field** — defer ingestion | XS when relevant | gated on Elijah running link/CTA reels | Near-zero signal for a voice-only / DM-share-driven account today. | `2026-06-15-new-research.md` (LATER) |

### SKIP

| Tier | Item | Effort | Deps | Key gate / note | Source-doc |
|---|---|---|---|---|---|
| **SKIP** | **EvoMap/evolver (as code)** | — | — | GPL-3 + **obfuscated core engine** = unauditable + license-contaminating for a private repo; Node network/leaderboard play. **Graft the pattern, install nothing** (see ADD-NOW EvoMap-graft row). | vault repos table |
| **SKIP** | **Mem0 MCP** | — | requires `MEM0_API_KEY`, sends data off-machine | Best memory benchmarks but cloud-hosted → conflicts with the secrets/OneDrive posture. WATCH only if a confirmed self-hosted config exists; Basic Memory is the privacy-correct pick. | `2026-06-15-new-research.md` (WATCH) |
| **SKIP** | **`total_views`/`total_likes`/`total_comments`** v22 aliases | — | — | Redundant — hub already ingests `views`/`likes`/`comments`; likes-per-reach already computable. | `2026-06-15-new-research.md` (SKIP) |
| **SKIP** | **Ayrshare MCP** | — | unofficial + $149/mo | Redundant with Metricool for a single-brand creator. | `2026-06-15-new-research.md` (SKIP) |
| **SKIP** | **OpenClaudia / social-media-analyzer skills** | — | — | Hub's IG-data-grounded equivalents (content-intel-2026, niche-intel, weekly-content-plan) are stronger. Mine for technique, don't bulk-install. | `2026-06-15-new-research.md` (SKIP) |
| **SKIP** | **Browser-session IG MCPs** (duhlink, engagement-mcp) | — | fragile Chrome session persistence | The official Graph-API `instagram` MCP is strictly better. | `2026-06-15-new-research.md` (SKIP) |
| **SKIP** | **a second virality ML model** | — | — | Don't build a second predictor before grading the first (the Higgsfield ledger). n=300 too small; the GBT-vs-Claude bake-off most likely ships nothing. | `docs/plans/2026-06-14-proprietary-virality-ml-model-research.md` |
| **SKIP** | **opendataloader-pdf** | — | needs a JRE (Java CLI) | Best-in-class Apache-2.0 PDF→MD, but defer until a concrete PDF-ingestion need (Labeltrust corpus #28); `research-lean`+WebFetch cover today. (LATER, not now.) | vault repos table |
| **SKIP** | **OpenWA / Telegram-Drive / cloakbrowser / ASCILINE / motion.dev / train-llm-from-scratch / build-your-own-x** | — | various | Wrong platform / ToS-gray storage / anti-detect / cv2+ad-block-evasion / redundant-with-HyperFrames / wrong-tool-at-n=300+torch / link-list. Full reasons in the vault repos table. | `2026-06-15-vault-feasibility.md` (repos table) |
| **SKIP** | **vault Venture-scale items** — Labeltrust product UX/bug/UI backlog (#28,30,31,32), kajabi self-build (#1), automated clone account (#21), zombie-GPT (#42) | — | — | Belong to product repos or are venture-scale / ToS-hostile. Hub assists with research/copy only. | `2026-06-15-vault-feasibility.md` |

---

## Suggested BUILD ORDER

The dependency spine: **grade → log the un-graded prediction → harden the loop → apply the cheap data
fixes → ship the time-boxed content → then enhancements.** In words:

1. **Higgsfield trust-ledger first (close L2).** It's the highest-leverage new item *and* it has no
   prerequisites — the ground truth (`store.json` watch-time) and the predictor (Higgsfield, already
   gating edits) both exist today; the only missing piece is the draft-time log. Build the append-only
   `higgsfield-ledger.jsonl` logger + the stdlib grade-join sibling. This unblocks the one expensive
   judgment the hub makes but never measures, and it sharpens the headline Wave-1 self-improve loop.

2. **self-improve `ledger.py` sidecar + the EvoMap-graft (do them together).** Both operationalize L6
   (track which proposals were accepted and whether they improved the next grade) and both are pure
   additive stdlib files that never touch `grade.py`. The anti-reward-hacking gate inside the sidecar
   (majority-of-k≥5-splits) is a *prerequisite for trusting the weight-tune PROPOSAL* — so build the
   gate before acting on §3's +0.023 weight delta. Order: ledger.py → graft → then the weight PROPOSAL
   becomes safe to evaluate.

3. **category_override data-fix pass.** Independent of 1–2, pure data fix (not engine logic), improves
   every category-reading downstream. Review the 121 flagged rows first (some are genuine multi-category).
   Quick, high-fan-out. Can run in parallel with 1–2.

4. **The #35 milestone reel — out of dependency order because of the CLOCK.** It depends on nothing in
   this list, but its value decays past ~100k followers. If the milestone is near, it *jumps the queue*
   to #1. Ship the smallest postable version, then return to the loop work.

5. **Watch-time ingest PROPOSAL doc.** Writing the proposal has no dependency; *applying* it is
   Elijah-gated (it edits `refresh.py`). Write it now so it's queued for his review — it's the
   next skip-rate-tier win and the field the Higgsfield ledger should ultimately be graded against.

6. **The remaining ADD-NOW research items in any order:** Labeltrust 3-detector classifier (pull the FTC
   TruHeight order first), name-SEO checklist, Basic Memory adoption note. None block each other.

7. **Content scripting + ADD-LATER enhancements last:** script the saas-for-agents 5 parts as desired;
   the OSS template / vault dashboard note / Metricool / DM Phase-0 all wait on an Elijah decision.

**Why this order:** it front-loads the one move that raises the *ceiling* on every prediction (grading
the pre-publish hook signal, which post-hoc rates structurally can't see), hardens the self-grader
against fooling itself *before* acting on its first weight proposal, applies the free data fixes that
need no review, and respects the single hard deadline (the milestone reel). Enhancements that merely
*widen* an already-covered gap come last.

---

## Elijah-gated (needs your decision/action — nothing here was done autonomously)

- **Apply the weight-tune PROPOSAL** (`metrics2026.WEIGHTS`, +0.023 held-out) — route via dev-workflow;
  evaluate against the stability gate first. Accept/reject is yours.
- **Apply the watch-time ingest PROPOSAL** to `refresh.py` (production-engine edit) once the doc exists.
- **Create `_templates/dashboard.md`** (or accept the body-only path) so the vault dashboard note can ship
  without inventing property names.
- **DM Phase-0 (~30min):** enable the messaging product + `messages` webhook on the `mybrain` app and do
  ONE live human-approved send → unblocks the DM responder + DM-routing.
- **Decide on the meta-stats OSS public repo** (and run the data-scrub + vendor-license gates).
- **Metricool Advanced plan** decision (gates the scheduling MCP).
- **Push to GitHub** — `main` is ahead of `origin` with all of tonight's commits.
- **The 121 category-override rows** — eyeball before applying (a few are legitimate multi-category posts).
- **Labeltrust classifier** lives in `C:\Users\elija\dev\labeltrust` — the hub drafts heuristics; you wire them.

---

## Cross-cutting observations

1. **The frontier moved INSIDE the loop.** Five prior nights chased *more intel* and *more tools*; this
   night's clearest finding is the opposite — the hub already scores on the right 2026 signal *and* now
   grades that score against reality, so the genuinely-new gap is neither intel nor a tool. It is the
   **un-closed expensive half of a loop the hub already runs**: every Higgsfield-gated edit is a
   pre-publish prediction that has never been graded. Close that (item #1) before buying anything.

2. **The grader earned the right to be trusted — modestly.** Held-out Spearman +0.455/+0.476 is a *real,
   positive, out-of-sample* signal (not circular in-sample), and the skip-gate validation (healthy
   14.8k > throttled 5.4k views) is the first hard proof that gate suppresses the *right* posts. But the
   weight-tune delta is small (+0.023) and from a single split → the honest move is to *harden the grader
   against fooling itself* (the reward-hacking gate) before acting on its first proposal. Self-improvement
   that can't be gamed is worth more than one lucky weight dict.

3. **Propose-never-apply held all night, and it's load-bearing, not ceremonial.** Every tonight artifact
   is additive (new file/skill/doc) or read-only; the grader writes only its append-only ledger; the
   weight-tune and watch-time ingest are *PROPOSAL docs*, not edits. This is exactly what let an
   autonomous run touch the hub's own scoring model without risk — the discipline IS the safety mechanism.

4. **The vault mine confirmed the recurring lesson a sixth time:** a vault note's framing is a hypothesis,
   not the scope. Of 50 ideas, the clean ADD-NOWs were all the *cheapest measure/draft slice* of a
   bigger idea; the over-scoped halves (self-build platform, automated clone, venture dropship) stay
   SKIP/Venture-scale. Split at the measure/generate seam; measuring composes cheaply, generating/
   publishing collides with Standing Rule 1 and waits.

5. **Six artifacts shipped clean again (6/6).** Subagents continue to excel at safe additive builds
   (stdlib/agent-as-brain, read-only, `--self-test`, local-commit) and degrade *correctly* when inputs are
   absent (trial_ab fell back to the caption heuristic; broll-planner is planner-only). Delegate builds to
   keep the orchestrator's context lean; keep them additive.

6. **One honest non-finding:** a 31st intel source or a second virality model would be diminishing returns.
   The only real *tool* candidates this wave were one paid LATER (Metricool, gated on plan + the publish
   wall) and one low-risk memory ADD (Basic Memory). Don't buy more tools — close the loop.
