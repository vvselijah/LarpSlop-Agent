# Audience-Reaction Simulation + Composio — Research Verdict

**Date:** 2026-06-13
**Author:** Synthesis agent (from 5 parallel research agents)
**Scope:** (1) Pre-publish audience-reaction simulation — OASIS vs BettaFish vs MiroFish (and the commercial field); (2) Composio as an agent tool/integration layer; (3) how Elijah + Tanner can iterate on real use cases; (4) open questions + next steps.

---

## Executive summary — the verdicts up top

- **Audience-reaction simulation is a REAL, novel gap-filler — but only as a QUALITATIVE, hook-ranking tool, never an absolute view forecast.** Nothing in Elijah's current stack does pre-publish *idea/hook* prediction: the IG dashboard reads the past, and the Higgsfield Virality Predictor scores the *rendered video craft*. A simulator scores the *message/angle* before a frame is shot.
- **RECOMMENDED simulation choice: a small, self-built `audience-sim/` engine on `camel-ai/OASIS` (Apache-2.0), seeded from his real @elijahaifl audience data — paired, not replaced, with the Higgsfield Virality Predictor.** OASIS is the only open, license-clean, locally-runnable, virality-dynamics simulator of the three. ([github.com/camel-ai/oasis](https://github.com/camel-ai/oasis))
- **BettaFish → SKIP for content prediction.** It is China-platform public-opinion *analysis*, not reel virality, GPL-2.0, and overlaps tooling Elijah already owns. ([github.com/666ghj/BettaFish](https://github.com/666ghj/BettaFish))
- **MiroFish → INVESTIGATE LATER as a crowd-sim toy only.** It is a polished OASIS wrapper but China-cloud oriented (Qwen/Zep/GraphRAG), **AGPL-3.0** (a commercial/SaaS source-disclosure flag), and predicts event/opinion outcomes, not IG reel retention. ([github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish))
- **Composio → INVESTIGATE / ADD-LATER, scoped and selective — never for IG or Meta tokens.** It is a powerful 500–1000+ toolkit MCP gateway that drops into Claude Code in one line, but its **default model stores OAuth tokens/API keys in Composio's cloud**, with no real local/self-host option below the Enterprise tier. That conflicts with the *spirit* of the hub's secrets-in-env-vars-only rule (it does not literally write secrets into the OneDrive tree). ([composio.dev](https://composio.dev), [docs.composio.dev/docs/mcp-overview](https://docs.composio.dev/docs/mcp-overview))
- **The honest caveat across all of it:** every validated simulation tool was proven on **text** (surveys, X/Reddit cascades, LinkedIn copy) — **none on short-form Instagram video.** Treat all of this as directional until backtested against Elijah's 300-post history. Research was also limited where vendor keys returned 401s and where MiroFish's English docs are thin (its `README-EN.md` 404s).

---

# PART 1 — Audience-reaction SIMULATION

## 1.1 The three candidates, head-to-head

| | **OASIS** (camel-ai/oasis) | **BettaFish** (666ghj) | **MiroFish** (666ghj) |
|---|---|---|---|
| **What it does** | LLM-agent social-media *simulator*: a population of persona-agents like/comment/repost/follow/post in a simulated X or Reddit with a real recommender (TwHIN-BERT / hot-score). | Public-opinion *analysis* system: crawls 30+ (mostly China) platforms, runs sentiment/insight, generates reports via 5 agents + a ForumEngine debate. | *Prediction via simulation*: thousands of persona-agents on OASIS/CAMEL forecast how an event/opinion unfolds; adds seed-extraction, GraphRAG, Zep memory, report agent, web UI. |
| **What it predicts** | Emergent reaction: comment sentiment, like/skip, which objections surface, which of two hooks wins head-to-head. | Macro opinion *trends* — NOT individual post virality. | Event/scenario *outcomes* via crowd dynamics — NOT reel retention. |
| **English-ready** | Yes (English docs/quickstart). | Partial — has `README-EN.md`; examples China-oriented. | README English by default, but `README-EN.md` 404s and `README-ZH.md` is Chinese; community China-oriented. |
| **License** | **Apache-2.0** (permissive — safe to fork/embed/build on). | GPL-2.0. | **AGPL-3.0** (networked/SaaS use can trigger source disclosure). |
| **Maturity** | Active: 4.8k★, ~941 commits, v0.2.5 (2025-12-04), NeurIPS-era paper (arXiv 2411.11581), on the well-maintained CAMEL framework. | 41,361★, created Jul 2024, active, more proven — but China-oriented. | 66,285★ but created **Nov 2025** (hype-driven, Shanda-incubated), active. |
| **Platforms simulated** | X/Twitter + Reddit (NOT Instagram). | China platforms first (Weibo, Xiaohongshu, Douyin, Kuaishou). | Dual-platform sim, China seed data. |
| **Windows** | pip install, runs against an API on a laptop. | Docker; Python 3.9+, Postgres/MySQL, Playwright — fiddly natively. | Docker only on Windows; Node 18+ & Python 3.11–3.12, uv, cloud keys. |
| **VERDICT** | ✅ **INVESTIGATE → build a small local engine** | ❌ **SKIP for content prediction** | ⚠️ **INVESTIGATE LATER (toy only); AGPL flag** |

### Why OASIS wins as the base
It is the **only one of the three** that (a) is permissively licensed (Apache-2.0, safe to embed in the hub), (b) runs locally/cheaply at creator scale (100 agents × 1 timestep ≈ 335,600 input + 16,750 output tokens — cents per run), (c) runs on **Claude (already wired)** or a local vLLM/Ollama model via CAMEL's `ModelFactory`, and (d) actually models virality *dynamics* (a real recommender pushes a candidate post to agents). MiroFish is literally a wrapper *on top of* OASIS — so adopting OASIS directly gets the engine without the China-cloud dependencies (Qwen/Zep/GraphRAG) or the AGPL-3.0 license. ([github.com/camel-ai/oasis](https://github.com/camel-ai/oasis), [docs.oasis.camel-ai.org/quickstart](https://docs.oasis.camel-ai.org/quickstart))

### The three honest gaps before OASIS earns a permanent slot
1. **Platform mismatch:** OASIS simulates X/Reddit, **not Instagram.** Any IG signal is a directional proxy, not a calibrated forecast.
2. **No persona-seeding tool ships:** the *paper* seeded ~196 real X users via the X API, but the *repo* gives no automated "real-audience → population" generator. Elijah owns that bridge. ([arxiv.org/abs/2411.11581](https://arxiv.org/abs/2411.11581))
3. **Accuracy ceiling:** the paper reports **~30% normalized RMSE** vs real propagation and shallower cascades — explicitly a qualitative/directional tool. Trust *relative* outputs (hook A beats hook B; here are the top objections), not numbers.

## 1.2 The wider field (context for the decision)

The validated academic ceiling is real and encouraging: Stanford's generative agents reproduced 1,052 real people's survey answers at **85% of human test-retest reliability**, and **real-data grounding beat generic personas by 14–15 points** ([arxiv.org/pdf/2411.10109](https://arxiv.org/pdf/2411.10109)). Commercial options exist — **Ask Rally** (persona twins from real interviews, API, free tier — the most automatable vendor; [askrally.com](https://askrally.com)) and **Artificial Societies Reach** ($40/mo, claims 83% *LinkedIn* engagement accuracy — cheapest validated entry but LinkedIn-specific; [societies.io](https://societies.io)). Enterprise/agency players (**Aaru, Electric Twin, Simile, Dentsu**) are wrong-scale for a solo creator — **skip** ([adweek.com](https://www.adweek.com)). The universal caveat: **all validated tools target text, none short-form video**, and synthetic respondents regress to the mean (low variance, directional only). ([cambridge.org — Perils of LLMs, *Political Analysis* 2024](https://www.cambridge.org))

**Decision:** Build DIY on OASIS rather than buy. A grounded DIY panel captures the 14–15pt accuracy lift from his *own* audience data, runs for cents, stays license-clean and local (consistent with the hub's posture), and avoids LinkedIn-shaped vendor pools. Keep **Ask Rally** on the watchlist as a fast managed fallback if the DIY persona layer proves too heavy.

## 1.3 CONCRETE integration plan — pre-publish audience-reaction prediction

Build a `audience-sim/` engine in the hub, mirroring the `intel/` and `ig-dashboard/` pattern (own `README.md`, own refresh script, no GPU cluster).

**Architecture — three layers:**

1. **Local engine (`audience-sim/sim.py`):** wraps `camel-oasis`; runs on Claude or a local vLLM/Ollama model. Creator-scale = 50–150 agents × a few timesteps = cents/run.

2. **Persona-seeding layer (the real work Elijah/Tanner own — `audience-sim/seed.py`):** reads his real audience and emits the OASIS Reddit-JSON population (`realname / username / bio / persona / age / gender / mbti / country` + the 24-dim hourly activity vector). Source data:
   - `mcp__instagram get_account_insights` → audience age/gender/country/interest distribution.
   - `ig-dashboard/` 300-post history → which audience archetypes/segments to instantiate and what they reward.
   - `team/memory.md` learnings → encode "what this audience punishes/rewards" into persona prompts.
   - Real top/worst commenter voices (scraped from his reels) → calibrate the agent tone.

3. **Pre-publish run:** inject the candidate hook/caption as the seed post; capture (a) synthetic comment themes + top objections, (b) like/skip ratio, (c) head-to-head winner when A/B-ing two hooks.

**How it plugs into the three existing systems:**

- **→ IG dashboard / `reel-analytics`:** add a three-stage funnel and a feedback loop. **Stage 1** sim-rank hooks *pre-shoot*; **Stage 2** Higgsfield scores the *rendered video*; **Stage 3** Instagram **Trial Reels** gives real *non-follower* ground truth. Log **sim-score + Higgsfield-score + actual 7-day performance** side-by-side in the dashboard / `team/memory.md` so the system learns whether the sim is worth keeping (the hub's evidence-before-"done" rule).

- **→ `weekly-content-plan` skill:** add an optional **"simulate" step** — before a planned hook hits the calendar, fire a 100-agent OASIS run seeded from his audience and attach the synthetic comment themes + like/skip ratio as a *confidence note* on each planned post. A/B two competing hooks against the same population.

- **→ Higgsfield Virality Predictor (complementary, NOT redundant):** Higgsfield scores **video craft** (hook strength, retention, distraction) frame-by-frame on a *rendered* clip; OASIS scores **audience response to the message/angle** *before shooting*. Run both: **OASIS gates the idea/hook, Higgsfield gates the edit.** Pipe simulated persona objections into `carousel-builder` and `comment-triage` as pre-drafted rebuttals (objection-mining, not just scoring).

**Calibration discipline (non-negotiable for v1):** because OASIS is X/Reddit not IG, treat v1 output as **qualitative** — surface objections, sentiment skew, and the head-to-head winner, NOT a predicted view count. **Backtest against 10–20 known past reels first** (a calibration harness over the 300-post history correlating predicted rank vs actual saves/reach); only trust numeric outputs if the backtest correlates.

**Recommended first move:** a **2–3 hour spike** on ONE real past reel — seed ~100 agents from his niches, feed the actual hook, compare the synthetic reaction to what really happened — *before* committing to build the full persona-seeding layer.

---

# PART 2 — Composio

## 2.1 What it is
Composio is a **managed tool/integration ("skill") layer** that lets AI agents call external SaaS APIs through a unified gateway — it owns the hard plumbing: a catalog of **500–1000+ toolkits** (GitHub alone = 867 tools + 20 triggers), managed OAuth, automatic token refresh, and per-user credential isolation. Consumed via Python/TS SDKs, native adapters (OpenAI, Anthropic, LangChain/LangGraph, CrewAI, Vercel AI SDK, etc.), and a hosted MCP server ("Rube", 500+ apps). It drops into Claude Code in **one line** (~10–20 min setup). SDK is **MIT**; the platform/service is proprietary SaaS. ([github.com/composiohq/composio README](https://raw.githubusercontent.com/composiohq/composio/master/README.md), [docs.composio.dev/toolkits/introduction](https://docs.composio.dev/toolkits/introduction))

## 2.2 Honest auth/secret-model assessment vs the hub's rules

**The load-bearing fact:** by default Composio is **cloud-hosted and STORES YOUR OAUTH TOKENS / API KEYS on Composio's infrastructure** — the "Connected Account" abstraction holds the actual credentials and auto-refreshes them server-side. Even bring-your-own-OAuth uses a Composio redirect and Composio still stores/refreshes tokens server-side. ([docs.composio.dev/docs/authentication](https://docs.composio.dev/docs/authentication))

**Against the hub's two relevant rules:**
- **Literal OneDrive-sync rule** ("secrets only in Windows env vars, never in files that sync to OneDrive"): Composio does **NOT** violate it — nothing secret is written into the synced tree.
- **Spirit of the rule** (keep credentials local and under Elijah's control): Composio **conflicts** — it relocates credentials from Elijah's Windows env vars to a third-party cloud. The trust boundary shifts from "Elijah's machine" to "Composio's cloud," and a **vendor breach** (not a OneDrive leak) becomes the new exposure path. This is the central thing to flag.

**Mitigations exist but are gated:** bring-your-own-OAuth + minimum scopes reduces blast radius; **fully self-hosted / VPC / on-prem** (the only deployment that truly satisfies "keep it local") is **Enterprise-tier only** (custom quote) — i.e., the version that fits the hub's philosophy is the expensive one. There is **no local/air-gapped credential mode on free/cheap tiers** (confirmed via the SDK-vs-backend distinction in HN thread #45583676 + open issue #291). Vendor claims SOC 2 Type II + ISO 27001:2022, encryption in transit/at rest, zero-day log retention — verify independently before trusting anything high-privilege. ([composio.dev/enterprise](https://composio.dev/enterprise), [news.ycombinator.com/item?id=45583676](https://news.ycombinator.com/item?id=45583676))

**Pricing (usage-based):** Free $0 / 20K tool calls per month (ample for a solo creator, no card); $29/mo / 200K; $229/mo / 2M; Enterprise custom (adds VPC/self-host). ([composio.dev/pricing](https://composio.dev/pricing))

## 2.3 Add-now / later / skip

| Integration | Call | Why |
|---|---|---|
| **Notion** | **ADD-NOW** | Highest-leverage, lowest-sensitivity gap. No structured planning DB wired to Claude beyond the vault; lets the agent build content-calendar databases on a dedicated workspace. Low risk. |
| **Google Calendar + Sheets** | **ADD-NOW** | Concrete gaps: scheduling (he uses Task Scheduler today) + metrics export from the IG dashboard for sharing/charting. Low-stakes Google auth on a dedicated content account. |
| **Composio gateway (general)** | **ADD-LATER, scoped** | Fills CRM/Notion/Stripe/Calendar/Sheets with near-zero overlap on his media/ads stack — but the cloud token vault conflicts with secrets-local, so adopt selectively per-need. |
| **HubSpot / CRM** | **ADD-LATER** | Genuine gap (no CRM today); useful once sponsor/lead tracking is formalized. Defer until a real pipeline exists. |
| **Stripe** | **INVESTIGATE** | Real gap but **highest sensitivity** — a payments token in a third-party vault. Only with a restricted/limited key, or prefer a first-party Stripe MCP if one exists. |
| **Rube universal MCP** | **INVESTIGATE** | Fastest eval (one-liner, ~7 meta-tools, dynamic discovery) but broad surface + ~2× latency make it worse than per-toolkit servers for steady use. Good for trial only. |
| **GitHub** | **SKIP** | Redundant — Claude Code already has `gh` CLI + native git. |
| **beehiiv (newsletter)** | **SKIP (via Composio)** | beehiiv ships its **own first-party native MCP** — wire that directly so the newsletter token stays first-party. ([beehiiv.com/features/api-and-integrations](https://www.beehiiv.com/features/api-and-integrations)) |
| **Instagram / Meta Ads** | **NEVER via Composio** | Already wired as dedicated **local MCPs with tokens in Windows env vars** — the preferred model. A vendor breach on these high-privilege tokens would be catastrophic. |

**Overlap summary:** Composio's *highest-value* integrations for most users (IG, Meta Ads) are exactly the ones Elijah **already covers locally** — so its marginal value is *breadth* for apps he doesn't yet use (Notion, Calendar, Sheets, CRM), at the cost of relocating those (lower-stakes) credentials to a vendor cloud. ([composio.dev/toolkits](https://composio.dev/toolkits))

**Hard rule if ever adopted:** restrict to **low-stakes, read-mostly** toolkits; prefer **bring-your-own-OAuth + minimum scopes**; and document explicitly in `AGENT-TEAM-BLUEPRINT.md` that adopting Composio (below Enterprise self-host) means **accepting third-party cloud custody of those specific credentials** — a deliberate, scoped exception to the local-secrets philosophy.

---

# PART 3 — How Elijah + Tanner can iterate on others' real use cases

The whole field is "validated on text, unproven on IG video" — which makes *their own backtest* the most valuable asset they can build. Concretely:

1. **Run the OASIS spike together, publicly to themselves.** A 2–3 hour spike on one past reel is the fastest way to convert "interesting paper" into "does this correlate with *my* numbers." This is exactly the kind of grounded, real-data iteration the Stanford result rewards (own-audience grounding beats generic personas by 14–15pts).
2. **Build the calibration harness as a shared artifact.** Backtest sims against the 300-post `ig-dashboard` history; correlate predicted hook-rank vs actual saves/reach. This harness *is* the iteration loop — every new reel adds a labeled data point and recalibrates trust in the sim.
3. **Cross-pollinate with `..\abc wrap\` (ClipWith.AI).** Same skills/MCPs are wired in both folders; an `audience-sim/` engine built here is directly reusable for ClipWith.AI's video R&D. Build once, run from either environment.
4. **Cherry-pick patterns, not whole stacks, from others' tools.** BettaFish's **ForumEngine** (agents debate to avoid groupthink) is a lightweight, license-free *idea* worth lifting into the `niche-intel` skill — without importing the crawler/DB/China-language stack.
5. **Watch the managed vendors as a sanity check, not a dependency.** Ask Rally's free tier + API is cheap to A/B against the DIY panel on the same hooks — if the DIY persona layer underperforms a $0 vendor run, that's a signal to buy rather than build.
6. **Log every evaluation as a dated learning** in `team/memory.md` (the hub's standing rule #7), so the next session inherits "OASIS = qualitative, X/Reddit not IG, backtest first; BettaFish skipped; MiroFish AGPL toy; Composio scoped-cloud-exception" without re-litigating.

---

# PART 4 — Open questions + recommended next steps

## 4.1 Open questions for Elijah

**Simulation:**
- Does the OASIS persona/recommender combo produce ANY signal that correlates with **real Instagram** performance? It's built/validated on X+Reddit, never IG — **needs a backtest against known past reels before any trust.**
- How heavy is the persona-seeding layer in practice? No shipped tool converts real audience data into the population — Elijah/Tanner build that bridge.
- Does a 50–150 agent run (the affordable scale) produce **stable, non-noisy** signal, or do the paper's emergent dynamics only appear at thousands of agents?
- Real per-run cost/latency on Claude vs a local vLLM model for ~100 agents — fast enough for a pre-publish workflow?
- Has v0.2.5's API drifted from the quickstart (`generate_reddit_agent_graph` / `ActionType`)? Docs lag releases.

**Composio:**
- Is there genuinely **no** air-gapped/local credential mode below Enterprise? Evidence says Enterprise-only — re-check live docs before relying on it.
- Is there a **first-party Stripe MCP** that avoids routing a payments token through Composio?
- Does Elijah have a *present* need for Notion / Calendar / CRM / newsletter, or are these speculative? (Adopt only on real need.)
- **Unconfirmed:** one search result alluded to a Composio OAuth/token security incident — could not verify a dated breach from a primary source. Treat as unconfirmed; ask Composio directly before high-privilege use.

## 4.2 Recommended next steps (in order)

1. **Simulation spike (this/next session):** `pip install camel-oasis`; run ~100 agents on ONE past reel's real hook via Claude; eyeball synthetic reaction vs reality. Decide go/no-go on the persona layer.
2. **If go:** scaffold `audience-sim/` (own README, `seed.py` + `sim.py`), wire the IG-insights → persona generator, and build the calibration harness over the 300-post history. Add the optional "simulate" step to `weekly-content-plan`.
3. **Composio (low-risk, parallel):** trial the **free tier** with **Notion + Google Calendar/Sheets only**, on a **dedicated content Google/Notion account**, BYO-OAuth + minimum scopes. **Never** route IG/Meta tokens through it. Document the scoped cloud-custody exception in `AGENT-TEAM-BLUEPRINT.md`.
4. **Wire beehiiv (if/when a newsletter exists) via its own native MCP**, not Composio.
5. **Log the dated learning** to `team/memory.md`.

## 4.3 Where research was limited
- **Thin English docs:** MiroFish's `README-EN.md` 404s and its community/examples are China-oriented; whether MindSpider supports Western platforms (IG/YT/X/Reddit) is **unverified**, and whether it can credibly simulate a Western IG audience without Chinese seed data is **unproven**.
- **401 / unverifiable keys:** vendor accuracy claims (Artificial Societies' 83%, Composio's SOC-2/ISO posture) and the alleged Composio security incident could not be independently confirmed from primary sources — flagged as vendor-claimed/unconfirmed throughout.
- **No IG-video validation anywhere:** every quantified accuracy figure in this report comes from text (surveys, X/Reddit, LinkedIn). The hub's own backtest is the only way to close that gap.

---

*Sources cited inline. Primary: [github.com/camel-ai/oasis](https://github.com/camel-ai/oasis), [arxiv.org/abs/2411.11581](https://arxiv.org/abs/2411.11581), [arxiv.org/pdf/2411.10109](https://arxiv.org/pdf/2411.10109), [github.com/666ghj/BettaFish](https://github.com/666ghj/BettaFish), [github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish), [composio.dev](https://composio.dev), [docs.composio.dev/docs/mcp-overview](https://docs.composio.dev/docs/mcp-overview), [askrally.com](https://askrally.com), [societies.io](https://societies.io).*
