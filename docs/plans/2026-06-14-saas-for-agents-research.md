# SaaS for AI Agents — Research & Feasibility Plan

- **Date:** 2026-06-14
- **Candidate id:** `saas-for-agents`
- **Source:** vault `Brainstorming/In the moment ideas.md` → "## build something that sells to agents" (lines 63–66)
- **Researcher:** Claude (hub research pass, WebSearch + WebFetch; exa/tavily/firecrawl keys dead)

---

## Headline verdict

**Split the candidate in two, because it is two different things wearing one title:**

| Sub-candidate | Verdict | Effort |
|---|---|---|
| **A. Content/positioning angle** — "Selling to agents / the agent economy" as an AI/Tech content series (his #2 niche) | **ADD-NOW** | XS (one grounded vault note + 3–5 hook drafts) |
| **B. Literal business direction** — Elijah actually *builds* an agent-native SaaS product | **ADD-LATER / mostly SKIP** | XL (venture-scale; not a vault item) |

The *trend is real and verifiable* — there is hard 2026 infrastructure behind it (Stripe ACP, Visa Trusted Agent Protocol, Mastercard Agent Pay, AP2, Coinbase x402, MCP for discovery). That makes it **excellent, defensible content**. But the original vault framing over-promises in two specific ways (see "Rescope" below), and the "go build it yourself" reading is a multi-month engineering venture with no obvious tie to his creator business. **Build the content note now; flag the venture as a separate, unproven bet.**

This matches how prior "Knowledge/strategy" items were handled: cheap, source-grounded vault note; zero engineering; honest rescope of hype.

---

## What it actually is

The idea (verbatim intent from the vault note): *"Everything's marketed toward humans nowadays when there's already more AI agents on the internet than humans… We need to find a way to sell SaaS to agents… Most companies will rebuild themselves but there's a vast majority of niches where the first to act will win… the human customer wants persuasion. The agent customer wants structure, capability, permission, trust and data."*

That last sentence is the genuinely sharp insight and it is **correct and well-supported**. The broader claims need grounding:

**What's real (2026, cited):**
- **Agents are becoming buyers, not just tools.** Payment rails for agent-initiated purchases shipped in 2025–2026: Stripe's **Agentic Commerce Protocol (ACP)** + **Machine Payments Protocol (MPP)** (ACP co-developed with OpenAI; supports cards, stablecoins, BNPL), **Visa Trusted Agent Protocol** (unveiled 2025-10-14, broader rollout early 2026), **Mastercard Agent Pay** (developer preview Oct 2025), the shared **AP2** mandate layer (Intent / Cart / Payment mandates), and **Coinbase x402** onchain payments (May 2025). [Stripe, MindStudio, Opascope]
- **Discovery/permission layer is standardizing.** MCP (tool discovery), A2A (agent-to-agent), UCP (checkout) are the emerging stack agents use to *find and authorize* software — which is exactly the "structure / permission / trust" Elijah named. [search synthesis]
- **The market is moving capital.** Agentic AI market ~$8.5B (2026) → ~$45B (2030) at ~53% CAGR; IDC: >1B deployed agents by 2029. AI-native app spend +108% YoY (large enterprises +393%). 40% of enterprise apps to include task-specific agents by end of 2026 (up from <5% in 2025). >60% of YC W26 cohort building agent-native workflows. [BetterCloud, SaaS Mag, Zylo via SaaS Mag, Belitsoft, search synthesis]
- **The disruption has teeth, not just decks.** ~$2T software market cap reportedly evaporated Jan–Feb 2026; Atlassian −35%, Salesforce −28% cited as agents automate their core workflows (task tracking, data entry, CRM logging). [DigitalApplied, PANews, BuiltIn]

**The honest counter-signal (this is the rescope):**
- The most-quoted "SaaSpocalypse" article (DigitalApplied) is, on fetch, **speculative futurism presented as analysis** — it does *not* substantiate the "more agents than humans" claim, names no concrete agent-native winners with evidence, and doesn't mention MCP/payment protocols. Treat its $2T/−35% figures as directional, not gospel.
- The sober take that actually holds up (PANews / BuiltIn): **"SaaS isn't dead — the easy UI moat is dead."** If your data, APIs, and semantics are clean, agents generate their own interface on top of you. The winners are clean-data/clean-API backends, not "pretty UI."

---

## Rescope (flag the over-promised framing — same as prior strategy items)

1. **"More AI agents on the internet than humans."** Could not verify with a credible primary source in this pass. IDC projects >1B agents by **2029** (future), and bot-vs-human-traffic stats are a *different* metric than "agent customers." **Do not state this as fact in content.** Reframe to the defensible version: *"By 2029 there will be over a billion deployed AI agents — and they're starting to buy software, not just use it."*
2. **"Rebuild every SaaS category for agents; first to act wins."** Partly true, partly already-happening (YC W26, Stripe/Visa/MC moving first). The "vast un-served niches" land-grab is a **VC thesis, not a solo-creator move.** For Elijah personally this is over-promised — he is not positioned to out-build Stripe/Salesforce on agent infra. The *content* about this thesis is the leverage, not the build.

---

## How it composes with the hub

### Sub-candidate A (content — the actual recommendation)

Pure **content-ops**, no new engine. Reuses existing pieces:

- **Vault:** one new `idea`-type note in `20-Content/Ideas/` (follow `_templates/` property contract exactly — `type: idea`, `domain: business`/`content`, `status: open`). Body = the grounded thesis + the cited rails + 3–5 hook angles. This *is* the deliverable.
- **`carousel-builder` skill:** the thesis is a natural **saves-optimized carousel** ("The 5 payment rails that let AI agents buy software in 2026" / "Why your favorite SaaS just lost $2T"). He runs zero carousels today — high-leverage untapped format.
- **`niche-intel` / `reel-analytics`:** before scripting, pull his historical AI/Tech reel performance to pick the framing that has worked (skip-rate/reach first per 2026 algo, not likes).
- **`weekly-content-plan`:** slot a 3–5 part "agent economy" mini-series into a week once the note exists.
- **Data shapes:** none new. Vault note frontmatter + plain markdown body. No API, no payload schema.

### Sub-candidate B (build — only if he insists)

If Elijah ever wants a *real* agent-facing product, the cheapest non-venture toehold that touches the hub: **expose one of his existing assets as an MCP server / clean API** (e.g., a read-only "Elijah content-intel" MCP, or the Archetype Index classifier as an agent-callable tool). That's the "clean data + API, let agents build the UI" survivor strategy — but it's a *project*, not a vault note, and belongs in `40-Projects/`, not here. **Out of scope for this candidate.**

---

## Phased build sketch

**Phase 0 (smallest safe thing — do this):** Write the single grounded vault note in `20-Content/Ideas/` with (a) the rescoped thesis, (b) the cited 2026 rails, (c) the two over-promise flags, (d) 3–5 hook drafts. ~30 min, zero engineering, zero risk. **This closes the candidate.**

**Phase 1 (content series):** Run it through `carousel-builder` → one saves-carousel + thread draft. Pull AI/Tech historicals via `reel-analytics` first. Elijah reviews; nothing publishes without his per-action OK.

**Phase 2 (optional, weeks out):** If a reel/carousel from the series over-performs, expand into a recurring "agent economy watch" angle and fold the trend-tracking into the existing `intel/trend-radar.py` keyword set (agent-commerce, MCP, ACP) — minor config, no new engine.

**Phase 3 (separate venture track — NOT this candidate):** Only if he wants skin in the game: ship one existing asset as an MCP/clean-API endpoint. Spin out as a `40-Projects/` entry with its own plan.

---

## Windows + OneDrive feasibility & dependency weight

**Trivial / green across the board.** Sub-candidate A is markdown + existing skills — **no Python, no torch/cv2, no models, no cloud cost, nothing that hangs on the synced disk.** This is the lightest possible class of addition (a corrected, source-grounded note). The only "dependency" is web access for citation freshness, already available. Sub-candidate B would carry real engineering weight but is explicitly deferred.

---

## Risks / ToS / ban

- **Content/factual risk (main one):** stating the unverified "more agents than humans" claim, or the soft $2T/−35% figures, as hard fact. **Mitigation:** use the rescoped phrasings above; cite the real rails (Stripe/Visa/MC), which are verifiable and impressive on their own.
- **Recency decay:** this space moves weekly. Re-verify rails/figures before any post; don't let the note go stale silently.
- **Platform/ToS:** none. This is original AI/Tech commentary — fits IG, no scraping, no automation against any platform. Standard hub rule still applies: **nothing publishes without Elijah's per-action confirmation.**
- **Opportunity-cost risk on Sub-candidate B:** the biggest real risk is *misreading this as a build directive* and sinking weeks into an agent-SaaS product with no tie to his creator business. The research explicitly flags that as a venture bet, not a hub task.

---

## Sources

- [How SaaS Companies Are Monetizing AI Agents in 2026 — SaaS Mag](https://www.saasmag.com/how-saas-companies-monetizing-ai-agents/)
- [AI and the SaaS industry in 2026 — BetterCloud](https://www.bettercloud.com/monitor/saas-industry/)
- [The SaaSpocalypse: AI Agents Disrupting Software Industry — DigitalApplied](https://www.digitalapplied.com/blog/saaspocalypse-ai-agents-software-industry-analysis) (flagged: speculative futurism)
- [It's not AI that's killing SaaS, it's the agent — PANews](https://www.panewslab.com/en/articles/09ef78ca-d87a-4ef9-8295-32acfa5d85e8)
- [AI Agents Are Disrupting SaaS — What It Means for Enterprise — Built In](https://builtin.com/articles/ai-agents-enterprise-saas-disruption)
- [Stripe Agentic Commerce Suite](https://stripe.com/blog/agentic-commerce-suite) · [Stripe Agentic Commerce use-case](https://stripe.com/use-cases/agentic-commerce) · [Stripe agentic commerce docs](https://docs.stripe.com/agentic-commerce)
- [Stripe's Agentic Commerce Suite: 5 New Primitives — MindStudio](https://www.mindstudio.ai/blog/stripe-agentic-commerce-suite-5-new-primitives-ai-agents-buy-pay)
- [AI Shopping Assistant Guide 2026: Agentic Commerce Protocols — Opascope](https://opascope.com/insights/ai-shopping-assistant-guide-2026-agentic-commerce-protocols/)
- [Belitsoft AI agent development forecast 2026 (40% of enterprise apps) — Barchart](https://www.barchart.com/story/news/1204699/belitsoft-releases-ai-agent-development-forecast-2026-40-of-enterprise-applications-to-include-task-specific-agents-by-year-end)
- [B2B SaaS and Agentic AI Pricing Predictions for 2026 — Ibbaka](https://www.ibbaka.com/ibbaka-market-blog/b2b-saas-and-agentic-ai-pricing-predictions-for-2026)
