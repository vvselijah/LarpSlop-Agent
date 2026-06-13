# Plan: audience-sim/ — pre-publish hook-ranker on OASIS (pairs with Higgsfield)

- **Date:** 2026-06-13
- **Branch:** `feat/audience-sim` (aspirational — hub not yet pushed; commit locally per CLAUDE.md "Honest scope")
- **Size estimate:** large (first hub engine with third-party deps; multi-phase, proof-first)
- **Status:** draft (awaiting Elijah's approval — NO code in this plan)

> Source of truth for the recommendation: `docs/plans/2026-06-13-simulation-composio-research.md`
> PART 1 (OASIS verdict). This plan operationalizes §1.3 of that doc.

---

## 1. Problem

Elijah has zero pre-publish *idea/hook* prediction in his stack. The IG dashboard
(`ig-dashboard/`, 300-post history) reads the **past**; the Higgsfield Virality
Predictor (`brain_activity`) scores the **rendered video's craft** (hook strength,
retention, distraction) on a clip that already exists. Nothing scores the
**message/angle itself — before a frame is shot.** When he's choosing between two
hook angles for a Money/Finance or AI/Tech reel, the only feedback loop is to
shoot both, post, and wait 7 days. The missing piece is an **audience-reaction
sandbox**: feed a candidate hook to a population of agents seeded from his *real*
@elijahaifl audience, and read back which angle lands, what objections surface,
and the head-to-head winner — for cents, in minutes, on his laptop.

The explicit value: a pre-publish **"audience reaction sandbox"** that **no other
tool in the stack provides**. It slots in upstream of Higgsfield to form a
two-gate funnel — **OASIS gates the IDEA/HOOK; Higgsfield gates the EDIT.**

## 2. Non-goals

This is the scope-creep fence. Read it before adding anything.

- **This change will NOT produce numeric IG forecasts** (predicted views/reach/saves).
  OASIS simulates X/Reddit, not Instagram, and the paper reports ~30% normalized
  RMSE — outputs are **qualitative** (which angle wins, what objections surface),
  never a calibrated number. (See Caveats, §3 row.)
- **This change will NOT replace the Higgsfield Virality Predictor.** They are
  complementary gates on different artifacts (angle vs. rendered edit). Both run.
- **This change will NOT ship a one-click persona-seeder from a vendor** — OASIS
  ships no real-audience→population generator. We build that bridge ourselves
  (`seed.py`), and that bridge is the actual work.
- **This change will NOT auto-publish, auto-post, or write to any platform.**
  Read-only against the IG Graph API + the local 300-post store; no IG/Meta writes.
- **This change will NOT be wired into `weekly-content-plan` until Phase 1's
  backtest passes.** No "simulate" step ships on an uncalibrated engine.
- **This change will NOT add a GPU/cluster dependency.** Runs on a laptop against
  an API (Claude) or a local model (vLLM/Ollama). Creator-scale only (~50–150 agents).
- **This change will NOT use Composio or any cloud token vault.** Secrets stay in
  Windows env vars (the existing `INSTAGRAM_ACCESS_TOKEN`; `ANTHROPIC_API_KEY` if Claude backend).

## 3. Honest caveats (up front — read before trusting any output)

These are non-negotiable framing for v1. They come straight from PART 1 §1.1 / §4.1.

| Caveat | What it means for us |
|---|---|
| **Platform mismatch** — OASIS simulates **X/Twitter + Reddit, NOT Instagram.** | Any IG signal is a **directional proxy**, not a calibrated forecast. v1 is qualitative by construction. |
| **No shipped persona-seeder.** The *paper* seeded ~196 real X users via the X API; the *repo* ships no real-audience→population generator. | **We build the CSV/JSON population ourselves** from his niches/segments (`seed.py`). This is the load-bearing effort, not the OASIS install. |
| **Accuracy ceiling ~30% normalized RMSE** (paper, arXiv 2411.11581); cascades run shallower than reality; synthetic respondents regress to the mean (low variance). | Trust **relative** outputs only: *hook A beats hook B*, *here are the top objections*. **Never** a predicted view count. Outputs are a confidence note, not a gate that blocks a post. |
| **Stable-signal floor unknown.** Emergent dynamics in the paper appear at thousands of agents; we run 50–150 for cost. | Phase 0 must check whether the affordable scale even yields **non-noisy** signal (run the same hook N times, measure variance). Open question for Elijah. |

The discipline these imply: **proof-first, backtest-before-trust** (§4 sequence).
Nothing wires into the content workflow until the calibration backtest correlates.

## 4. Approach

### Considered alternatives

| Approach | Effort | Key tradeoff |
|---|---|---|
| **A. Self-built `audience-sim/` on `camel-ai/OASIS` (Apache-2.0), seeded from his audience** | Medium-high (we own `seed.py` + calibration) | Best fit: license-clean, local, cents/run, grounded in *his* data (the 14–15pt accuracy lift from the Stanford result), runs on Claude (already wired) or local vLLM. Owns the persona bridge. **← chosen** |
| B. Buy a managed vendor (Ask Rally free tier / API) | Low (API call) | Fast, no persona engineering — but vendor persona pools are generic / LinkedIn-shaped, no own-audience grounding, and adds an external dependency + data-egress. **Kept on watchlist as fallback** if our persona layer proves too heavy. |
| C. MiroFish (polished OASIS wrapper) | Medium | **AGPL-3.0** (SaaS source-disclosure flag) + China-cloud deps (Qwen/Zep/GraphRAG) + thin English docs. It's literally a wrapper *on* OASIS — adopting OASIS directly gets the engine without the license/cloud baggage. **Rejected.** |
| D. BettaFish | — | China-platform public-opinion *analysis*, GPL-2.0, overlaps tools he owns; predicts macro trends not reel virality. **Rejected for content prediction.** |
| E. Do nothing (status quo: shoot both hooks, post, wait 7d) | Zero | No pre-shoot signal; every angle test costs a real post + a week. The gap this plan fills. |

### Chosen approach and why

**A — build a small self-hosted `audience-sim/` engine on OASIS, paired with (not
replacing) Higgsfield.** OASIS is the only one of the three candidates that is
(a) **Apache-2.0** (safe to embed in the hub), (b) **locally runnable for cents**
(~100 agents × 1 timestep ≈ 335k input + 17k output tokens), (c) runs on
**Claude via CAMEL's `ModelFactory`** (already wired) or a local **vLLM/Ollama**
model to zero out per-token cost, and (d) actually models virality *dynamics* (a
real recommender pushes a candidate post to agents). We pair it with Higgsfield to
form the two-gate funnel: **OASIS gates the idea/hook pre-shoot; Higgsfield gates
the rendered edit.** Critically, we do this **proof-first** — a spike, then a
backtest over the 300-post history — before trusting any output or wiring it into
the weekly plan.

## 5. Design

### Folder layout — new workspace-root `audience-sim/`, mirroring `ig-dashboard/` + `intel/`

```
audience-sim/
  README.md            # own README, like ig-dashboard/ and intel/ (house convention)
  requirements.txt     # NEW house convention — first hub engine with 3rd-party deps
  sim.py               # orchestrator / entry point  (BASE = Path(__file__).resolve().parent)
  seed.py              # persona-seeder: audience segments -> OASIS population JSON/CSV
  runner.py            # sim-runner: wraps camel-oasis via CAMEL ModelFactory
  backtest.py          # Phase-1 calibration harness over the 300-post history
  personas/            # generated population files (Reddit-JSON / CSV) — committed (no secrets)
  data/                # run outputs, raw OASIS state, logs (house convention: data/ dir)
    runs/<timestamp>/  # one dir per sim run: input hook(s), agent reactions, raw state
  report.md            # latest run summary, markdown (house convention: <engine>/report.md)
```

This mirrors the existing engines exactly: **BASE-anchored** paths
(`BASE = Path(__file__).resolve().parent`, `DATA = BASE / "data"`), a `data/`
directory for state, and a markdown report at the engine root — identical to
`ig-dashboard/refresh.py` (`data/store.json`, writes `team/stats.md`) and
`intel/competitor-radar.py` (`data/competitors.json`, writes `radar-report.md`).

### `requirements.txt` convention (new — propose for the hub)

This is the **first hub engine needing third-party deps** (`camel-oasis`, which
pulls `camel-ai`). Existing engines use only stdlib + `curl.exe`. Proposed convention:

- Each engine that needs deps gets its own `audience-sim/requirements.txt`
  (pinned, e.g. `camel-oasis==<verified>`), installed into a **local venv**
  (`audience-sim/.venv/`, git-ignored / not synced — venvs are large + machine-specific).
- A short note in `audience-sim/README.md`: *"create venv, `pip install -r requirements.txt`"*.
- Document the convention once in `AGENT-TEAM-BLUEPRINT.md` so future engines follow it.
- **Pin against the actually-installed version** — Premise table flags the API-drift risk
  (`generate_reddit_agent_graph` / `ActionType` may have moved between OASIS releases).

### Data flow (the two-gate funnel)

```
                 team/stats.md (niches, category mix, top hooks)
                 ig-dashboard/data/store.json (300 posts: caption, category,
                       views, saves, reach, follower/non-follower split,
                       demographics: age/gender/country)
                 team/memory.md (what this audience rewards/punishes)
                                  │
                                  ▼  seed.py
                 personas/elijah_population.json   (50–150 OASIS persona-agents:
                       realname/username/bio/persona/age/gender/mbti/country
                       + 24-dim hourly activity vector, distributions matched
                       to his real audience)
                                  │
              candidate hook(s)   ▼  runner.py  (camel-oasis + CAMEL ModelFactory;
              ──────────────────▶  backend = Claude OR local vLLM/Ollama)
                                  │   seed post = the hook; 1 timestep; recommender
                                  │   pushes it to agents; agents like/skip/comment
                                  ▼
   ┌──────────── GATE 1: OASIS (this engine) — qualitative ────────────┐
   │  • synthetic comment themes + top objections                       │
   │  • like/skip ratio (relative)                                      │
   │  • head-to-head: which of hook A / hook B wins on the same pop     │
   └────────────────────────────────────────────────────────────────────┘
                                  │  (hook survives → he shoots + edits it)
                                  ▼
   ┌──────────── GATE 2: Higgsfield Virality Predictor ────────────────┐
   │  scores the RENDERED clip's craft (hook/attention/retention)       │
   └────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼  (post; 7 days later)
   real 7-day performance  ──▶  logged beside sim-score + Higgsfield-score
        (ig-dashboard)            in data/runs/ + team/memory.md  → closes the loop
```

### Three layers (from research §1.3)

1. **Local engine (`runner.py` + `sim.py`):** wraps `camel-oasis`; backend chosen
   via CAMEL `ModelFactory` (Claude already wired, or local vLLM/Ollama to avoid
   per-token cost). Creator-scale: 50–150 agents × 1 timestep.
2. **Persona-seeding layer (`seed.py` — the work we own):** reads his real audience
   and emits the OASIS population. Sources:
   - **Local first (cheap, offline):** `ig-dashboard/data/store.json` already holds
     `demographics` (age/gender/country breakdowns), the category mix, and the
     300-post caption/performance history — `seed.py` reads this file directly
     (no API call needed for v1). `team/stats.md` gives the niche weighting
     (Money/Finance, AI/Tech, Motivation/Life, Founder/Business, Faith, etc.).
   - **Optional live:** `mcp__instagram get_account_insights` for fresh
     audience age/gender/country/interest distribution.
   - `team/memory.md` learnings → encode "what this audience punishes/rewards"
     into persona prompts.
   - (Later) real top/worst commenter voices scraped from his reels → calibrate tone.
3. **Pre-publish run (`sim.py`):** inject the candidate hook/caption as the seed
   post; capture (a) synthetic comment themes + top objections, (b) like/skip
   ratio, (c) head-to-head winner when A/B-ing two hooks.

### Existing helpers/modules to reuse (searched the tree — these exist, don't reinvent)

- **`ig-dashboard/refresh.py` `get_token()`** (env var → `winreg` HKCU fallback) —
  copy the pattern verbatim if `seed.py` ever needs a live IG call. Same pattern in
  `intel/competitor-radar.py`. **Do not invent a new token path.**
- **`ig-dashboard/refresh.py` `api()` / `curl.exe --config -` over stdin** — the
  house way to hit the Graph API on this host (PowerShell/urllib hang). Reuse if live-calling.
- **`ig-dashboard/refresh.py` `categorize()` + `CATEGORIES`** — the canonical
  caption→niche keyword map; `seed.py` should reuse it to bucket the 300 posts into
  the same niches the rest of the hub uses (don't fork a second category list).
- **`ig-dashboard/data/store.json`** — already has demographics + per-post
  performance; `seed.py` reads it instead of re-pulling from the API.
- **`log()` pattern** (timestamped line to stdout + `data/*.log`) from both engines.
- **House idioms:** `BASE = Path(__file__).resolve().parent`, `DATA = BASE/"data"`,
  `DATA.mkdir(exist_ok=True)`, markdown report at engine root.

## 6. Failure modes

| Scenario | Expected behavior |
|---|---|
| **Partial failure** (population seeded OK, OASIS run errors mid-sim) | Persist whatever agent reactions completed to `data/runs/<ts>/partial.json`; `report.md` marks the run **INCOMPLETE** with the error; never emit a "winner" from a partial run. |
| **camel-oasis not installed / wrong version (API drift)** | `sim.py` fails fast with a clear message pointing to `requirements.txt` + the pinned version; does not silently fall back to a stub that fabricates a result. |
| **Backend (Claude API) throttles / 429 / timeout** | Respect the hub research protocol's throttle-awareness: back off, cap concurrency, and if it can't complete, abort the run rather than produce a degraded population. Log token spend. |
| **Retry / duplicate run of the same hook** | Each run gets its own `data/runs/<timestamp>/` dir (idempotent by timestamp); re-running the same hook is expected (variance check) and never overwrites a prior run. |
| **Empty / malformed input** (no hook text; `store.json` missing or 0 posts) | `seed.py` refuses to emit a population it can't ground in real data; `sim.py` refuses to run with no hook. Both exit non-zero with a specific message. |
| **Oversized input** (caller asks for thousands of agents) | Cap at a configured max (e.g. 150 for v1) with a warning; document that cost/latency/stability above that is unverified. |
| **Concurrent access** | Single-user laptop tool; runs are serialized by the operator. No locking designed, but timestamped run dirs mean two runs can't clobber each other. |
| **Sim says "hook A wins" but reality later disagrees** | Expected and logged — that's the calibration loop's job. Phase 1 backtest must pass *before* anyone treats the winner as actionable; even then it's a confidence note, not a gate. |

## 7. UI states

No UI. (`report.md` is a static markdown artifact, like `intel/radar-report.md` and
`team/stats.md`. Section intentionally omitted per template.)

## 8. Test plan

| Case | Level | Covers failure mode # |
|---|---|---|
| `seed.py` reads `ig-dashboard/data/store.json` + `team/stats.md` and emits a valid OASIS population JSON (schema fields present, distributions sum sanely) | unit | empty/malformed input |
| `seed.py` reuses `refresh.py` `categorize()` and buckets 300 posts into the same niches | unit | (consistency) |
| `runner.py` runs ~10 agents × 1 timestep against a stub/local backend end-to-end (smoke) | integration | partial failure, install/version drift |
| Variance check: same hook run N times at the chosen agent count → measure spread of like/skip + objections | integration | stable-signal floor (open Q) |
| **Phase-0 spike:** ~100 agents on ONE real past reel's actual hook; compare synthetic reaction to what really happened | e2e (manual eyeball) | the whole premise |
| **Phase-1 backtest:** `backtest.py` over 10–20 (then 300) known posts; correlate predicted hook-rank vs actual saves/reach | e2e | accuracy / "does it correlate with IG" |
| Backend throttle: force a 429 path, confirm graceful abort + token-spend log | integration | throttle/timeout |
| Cost/latency measured: log real input/output tokens + wall-clock for a 100-agent run on Claude vs local | integration | cost open Q |

## 9. Steps — PHASED, PROOF-FIRST (each phase gates the next)

> The whole point is **not** to build the full engine on faith. We prove signal
> exists (Phase 0), prove it *correlates* (Phase 1), and only then wire it in (Phase 2).

### Phase 0 — SPIKE (2–3 hours; throwaway-OK; gate: "is there ANY signal?")
1. `pip install camel-oasis` into a throwaway venv; run the OASIS quickstart once
   to confirm it works on this Windows host (Premise 1/2 verification).
2. Hand-seed ~100 agents from his niches (distributions eyeballed from `stats.md` +
   `store.json` demographics) — quick-and-dirty, not the real `seed.py` yet.
3. Pick ONE real past reel with known outcome (e.g. the 3.9M-view Money/Finance one,
   or a known flop for contrast). Feed its **actual hook** as the seed post; run 1 timestep.
4. Eyeball: do the synthetic comment themes / like-skip ratio resemble what really
   happened? Run it 2–3× to gauge variance. **Log real token cost + latency.**
5. **Decision gate:** go/no-go on building the real persona layer. If no signal or
   wild variance at 100 agents → stop here, log the dated learning, reconsider Ask Rally.

### Phase 1 — CALIBRATION BACKTEST (gate: "does sim signal correlate with real performance?")
6. Scaffold the real `audience-sim/` (README, `requirements.txt` pinned, `seed.py`,
   `runner.py`, `sim.py`, `backtest.py`, `data/`, `personas/`). One commit per file-group.
7. Build `seed.py` for real: read `store.json` demographics + `categorize()` niches +
   `memory.md`; emit `personas/elijah_population.json`. Commit.
8. Build `backtest.py`: for 10–20 known past reels, run the sim on each historical hook,
   then **correlate predicted rank vs actual saves/reach** (Spearman). Expand to the full
   300 if 10–20 looks promising. Commit.
9. **Decision gate:** report the correlation in `report.md`. **If it does not correlate,
   the engine stays a qualitative objection-miner only** (still useful: surfaces angles +
   objections) and we do NOT advance to a ranking step. Log the dated learning to `memory.md`.

### Phase 2 — WIRE THE VALIDATED HOOK-RANKER IN (only if Phase 1 correlates)
10. Add an optional **"simulate" step** to the `weekly-content-plan` skill: before a
    planned hook hits the calendar, fire a ~100-agent run seeded from his audience and
    attach synthetic comment themes + like/skip ratio as a **confidence note** per post;
    A/B two competing hooks on the same population.
11. Pipe simulated persona objections into `carousel-builder` / `comment-triage` as
    pre-drafted rebuttals (objection-mining reuse).
12. Close the loop: log **sim-score + Higgsfield-score + actual 7-day performance**
    side-by-side (in `data/runs/` and `team/memory.md`) so the system keeps learning
    whether the sim earns its slot (the hub's evidence-before-"done" rule).

## 10. Cost / latency / backend

- **Per-run order of magnitude (research §1.1):** ~100 agents × 1 timestep ≈
  **335,600 input + ~16,750 output tokens** → **cents** on Claude; runs on a laptop
  against an API. A/B-ing two hooks ≈ 2× that. Phase 0 must measure the *real* number
  (Sonnet vs Opus pricing materially changes it — confirm against the `claude-api` skill
  before quoting a dollar figure to Elijah).
- **Backend choice (CAMEL `ModelFactory`):**
  - **Claude (already wired):** zero setup, cents/run, best persona quality. Default for v1.
  - **Local vLLM / Ollama:** zero per-token cost + fully offline (no data egress), at the
    price of local GPU/CPU + lower persona fidelity. Worth benchmarking in Phase 0 if
    Elijah plans frequent / large runs — open question below.
- **Latency:** dominated by the backend; ~100 agents × 1 timestep should be minutes,
  not hours, on an API — but **measure in Phase 0**, don't assume.

## 11. Standing rules (non-negotiable for this engine)

1. **Read-only.** Reads the IG Graph API (insights/demographics) and the local 300-post
   store; **never** writes to IG/Meta. No publish, post, comment, or DM — ever.
2. **NEVER auto-publish.** This engine produces a *confidence note* on a draft hook. The
   final post is always Elijah's explicit per-action click (CLAUDE.md standing rule #1).
3. **Secrets in env vars only.** Token via the existing `get_token()` pattern
   (`INSTAGRAM_ACCESS_TOKEN` from env / HKCU registry); `ANTHROPIC_API_KEY` for the Claude
   backend likewise from env. **No secret ever written into the OneDrive-synced tree.**
   No Composio / cloud token vault (research PART 2).
4. **Append one dated learning to `team/memory.md`** after the spike and after the
   backtest (CLAUDE.md standing rule #7).
5. **`.venv/` and `data/runs/` raw state are git-ignored / not synced** (large, machine-specific);
   `personas/*.json` are committed (no secrets, useful as seed artifacts).

## 12. Premises (verify against real code/library before building — mark ✅/❌)

The agent **must** verify each against the actual installed library + repo before
Phase 1, not from memory. These are checkable in Phase 0's spike.

| # | Premise | Verified |
|---|---|---|
| 1 | `pip install camel-oasis` installs cleanly on this Windows host (Python in the existing toolchain) and imports. | ⏳ (Phase 0 step 1) |
| 2 | OASIS v0.2.x exposes the quickstart API used to build a population + run a step (`generate_reddit_agent_graph` / `ActionType` or their current equivalents — **docs lag releases; verify the installed version**). | ⏳ (Phase 0 step 1) |
| 3 | CAMEL `ModelFactory` can target Claude with the already-wired `ANTHROPIC_API_KEY` (and, separately, a local vLLM/Ollama endpoint). | ⏳ (Phase 0) |
| 4 | `ig-dashboard/data/store.json` contains the `demographics` (age/gender/country) + per-post category/views/saves needed to seed personas **without a live API call**. | ✅ confirmed in `refresh.py` (`store["demographics"]`, `DEMO_BREAKDOWNS`, per-post `insights`) — verify the file is populated on disk. |
| 5 | `refresh.py` `categorize()` + `CATEGORIES` are importable/reusable as the canonical niche map. | ✅ present in `ig-dashboard/refresh.py`; confirm it imports cleanly from a sibling folder (or copy the constant). |
| 6 | `team/stats.md` carries the live niche weighting + top hooks to seed segment proportions. | ✅ confirmed (category mix + top-5 posts present in current `stats.md`). |
| 7 | ~100 agents × 1 timestep costs cents and runs in minutes on Claude (research estimate ~335k in / 17k out). | ⏳ measure in Phase 0; confirm $ via `claude-api` skill pricing. |
| 8 | The IG token (used only if `seed.py` makes a live insights call) is valid; expires 2026-08-11 (per `stats.md`). | ✅ token live; renewal in HANDOFF §4. |

## 13. Risks / gotchas

- **Over-trusting a directional tool.** The single biggest risk is treating the
  qualitative winner as a forecast. Mitigation: the §3 caveats are baked into
  `report.md`'s header on every run; no numeric prediction is ever emitted.
- **Persona-seeding is the real cost** (research §4.1) — there is no shipped tool.
  If `seed.py` proves too heavy, the watchlisted fallback is Ask Rally's free tier/API.
- **API drift (Premise 2).** OASIS docs lag releases; pin the version and verify the
  quickstart symbols against the *installed* build, not the README.
- **Stable-signal floor unknown** at 50–150 agents (the paper's dynamics appear at
  thousands). The variance check in Phase 0 is the early warning.
- **Synthetic-respondent regression to the mean** — agents under-produce extreme
  reactions, so the sim may under-call viral outliers. Keep it as a *relative* ranker.
- **Cross-pollination upside:** `audience-sim/` built here is directly reusable for
  `..\abc wrap\` (ClipWith.AI) — same skills/MCPs wired in both folders. Build once.

## 14. Open questions for Elijah (please answer before Phase 1)

1. **Does the OASIS persona/recommender combo produce ANY signal that correlates with
   real *Instagram* performance?** It's validated on X+Reddit, never IG. This is the
   gating question — **Phase 0 spike + Phase 1 backtest exist to answer it.** Are you
   OK greenlighting only the 2–3h spike first, before any build commitment?
2. **How heavy is the persona-seeding layer worth being?** No shipped tool converts real
   audience → population; we build `seed.py`. How much fidelity do you want (basic
   demographic match vs. real-commenter-voice calibration)? Or prefer we time-box it and
   fall back to Ask Rally if it balloons?
3. **What's the minimum agent count for stable signal?** We default to ~100 for cost;
   the paper's emergent dynamics show at thousands. If 100 is too noisy, are you OK
   paying for larger runs, or do we accept a coarser signal?
4. **Backend: Claude vs local vLLM/Ollama?** Claude = zero setup, cents/run, best
   quality, but per-token cost + data egress. Local = free per run + fully offline, but
   needs local compute and gives lower persona fidelity. Which do you want benchmarked
   in Phase 0, and is per-run cost or offline-privacy the priority?
5. **`requirements.txt` convention** — OK to introduce per-engine `requirements.txt` +
   local `.venv/` (git-ignored) as the hub's first third-party-dep pattern, documented
   in `AGENT-TEAM-BLUEPRINT.md`?

## 15. Retro (fill after shipping)

- Premises that turned out wrong:
- Missing from this plan:
- Context-file updates made:
