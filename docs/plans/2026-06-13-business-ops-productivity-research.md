# Business-Ops + Personal-Productivity Stack — Research & Verdicts

- **Date:** 2026-06-13
- **Scope:** Workflows #4 (business ops) + #5 (personal productivity). Covers (1) scheduling & social management, (2) email/newsletter + sponsor CRM + payments, (3) the course platform for the Archetype Index Kajabi migration, (4) personal productivity/knowledge, (5) the recommended wire-now stack + open questions.
- **Method:** synthesis of a 4-agent research run (deep re-validation of the scheduling layer) + targeted live re-checks of beehiiv/Stripe/Whop/Skool/Kajabi current state on 2026-06-13.
- **Standing rules honored throughout:** secrets-local (Windows env vars via `setx`, never in OneDrive-synced files); official-MCPs-first; human-in-the-loop (no publish/post/send/charge without Elijah's explicit per-action OK).
- **Cross-reference:** this report CONFIRMS or REVISES the `AGENT-TEAM-BLUEPRINT.md` picks (Metricool / Whop / beehiiv). One blueprint fact is corrected; two are confirmed with new detail.

---

## Executive summary — add now / later / skip (all tools, all four areas)

| Area | Tool | Verdict | One-line why | Cost |
|---|---|---|---|---|
| **1. Scheduling** | **Metricool (official MCP)** | **ADD NOW** | Only official, Claude-Code-supported MCP covering all his platforms + audited TikTok client + new IG licensed-audio auto-publish | ~$54/mo (Advanced — **corrected**, see §1) |
| 1. Scheduling | Postiz (self-host, official MCP) | LATER / if | Best secrets-local fallback if he ever wants every token on-machine; but it's an infra project + he owns the TikTok audit | Free self-host (~$5–20/mo server) |
| 1. Scheduling | Buffer / Publer / Mixpost | SKIP | Community MCPs, weaker agent surface, no edge over Metricool for his need | n/a |
| 1. Scheduling | Hypefury | SKIP | X-first, no MCP/API, growth-automation collides with human-in-the-loop rule | n/a |
| **2. Email/newsletter** | **beehiiv (official MCP, read) + send API (write)** | **ADD AT LAUNCH** | MCP is read-only V1; do the actual sending via beehiiv's send API behind human approval — confirmed | Paid-plan-gated (free tier exists) |
| **2. Payments** | **Stripe (official MCP, restricted key)** | **ADD WHEN MONEY MOVES IN** | Official `@stripe/mcp`; use a **restricted/read-only key** in a local env var; doubles as the sponsor-invoice + lightweight CRM layer | Stripe's normal % fees only |
| 2. Sponsor CRM | **Vault note + Stripe invoices** (no SaaS) | **ADD NOW (free)** | A sponsors/ folder in the vault is the CRM; Stripe handles invoices/payment status — avoids a paid CRM seat | $0 |
| 2. Email/CRM | HubSpot/Notion-CRM/dedicated sponsor SaaS | SKIP (for now) | Overkill at his scale; the vault + Stripe + IG-DM MCP already cover the pipeline | n/a |
| **3. Course platform** | **Whop (official MCP `mcp.whop.com`)** | **PICK — migrate here** | Full native Courses app + Chat/Forums/Video-calls + lowest fees + the ONLY option with a first-party MCP (agent-controllable) | 2.7% + $0.30/txn, **no monthly** |
| 3. Course platform | Skool | RUNNER-UP / if community-first | Better gamified community + structured classroom, but $99/mo flat + 2.9% and **no MCP/API for agents** | $99/mo + 2.9% |
| 3. Course platform | Self-built / WordPress+LearnDash | SKIP | High build + maintenance burden, no agent surface, contradicts "never build ahead of need" | $498+/yr + ops time |
| **4. Productivity** | **Obsidian vault + local engines (reuse)** | **ALREADY BUILT — extend** | Local-first knowledge base already exists; reuse `auto-clip/transcribe.py` + the 7AM task; add no new SaaS | $0 |
| 4. Productivity | Notion/Mem/cloud PKM SaaS | SKIP | Cloud-first, duplicates the vault, breaks local-first + secrets-local posture | n/a |

**Bottom line:** exactly **one** new paid commitment is worth making today (Metricool, with the corrected price). Everything else is either already built (vault, local engines), free (vault-as-CRM), or correctly trigger-gated to a real event (beehiiv at newsletter launch, Stripe when money flows, Whop at the migration decision — which is now resolved in favor of Whop).

---

## PART 1 — Scheduling & social management (resolve the Metricool pick)

**VERDICT: Metricool stays the single best pick — CONFIRMED — with one blueprint correction and two constraint updates.**

Metricool is the only **official, Claude-Code-supported** MCP that (a) covers every platform Elijah uses (IG, TikTok, YouTube, X, Threads, FB, LinkedIn, Pinterest, GBP), (b) is an **audited TikTok client** — which sidesteps a wall he physically cannot build around — and (c) as of a **May-2026 official IG Content Publishing API update**, can now search/preview/schedule and **auto-publish Reels with audio from Meta's licensed library OR original audio** (source: https://metricool.com/mcps-for-marketing/ ; https://metricool.com/trending-audio-on-instagram/).

### Blueprint correction (flip this stale fact)

The blueprint (line 51 + line 81) says Metricool's MCP "works on any plan" and that the "requires Advanced tier" claim was "refuted." **That is now stale and must be flipped.** Consistent 2026 sources (Metricool's own MCP article + pricing reviews) say the **MCP requires the ADVANCED plan (~$54/mo), OAuth 2.1** — the Starter (~$20–22/mo) tier does **not** unlock the MCP (source: https://costbench.com/software/social-media-management/metricool/). **Action:** verify the MCP plan-gate live in his own Metricool account before committing the ~$54/mo (open question O1).

### Two constraint updates vs the blueprint

1. **IG trending-audio rule is now PARTIALLY lifted.** The blueprint's hard rule (line 76–78) "API-published reels can't use licensed/trending audio" is no longer absolute. The May-2026 update lets Metricool auto-publish Reels with audio "cleared for third-party software distribution" — **but** that catalog is *narrower* than the in-app one, and it needs **Facebook Login** (not legacy IG Login). Only **native-only sounds + AR effects** still force a manual/Notify-Me post.
2. **TikTok wall UNCHANGED and re-confirmed.** TikTok's own docs still restrict unaudited Content Posting API clients to `SELF_ONLY` (private) posts + max 5 users/24h — not a quota you can buy out. He MUST publish TikTok through an audited third party (Metricool qualifies). Building a self-hosted TikTok publisher remains a dead end. This confirms blueprint Tier C and constraint #2.

### Why not the alternatives

- **Postiz (self-host, official MCP, AGPL):** the *correct* secrets-local fallback and the best OSS pick — all OAuth tokens stay on his box (perfect OneDrive-avoidance fit). But it's an **infra project** (container + DB + reverse proxy + per-platform dev-apps), it makes *him* the TikTok-audit owner, and it trails Metricool on the new IG-audio integration. **LATER / if** Metricool's cost or cloud-token model becomes unacceptable — scope it as a `docs/plans` dev-workflow spike, not a drop-in (source: https://github.com/gitroomhq/postiz-app).
- **Buffer (community MCP):** runs on Buffer's Feb-2026 GraphQL **beta** — create-only, no engagement metrics via API, and a risky delete+recreate "update." Duplicates, worse, what his `instagram` MCP + `ig-dashboard` already do. **SKIP.**
- **Publer (community MCP):** strong budget scheduler but community-hosted MCP and push-notification semi-automation for TikTok. No official MCP, less-mature agent surface. **SKIP** (keep as a known cheaper manual-dashboard option).
- **Mixpost (self-host, community MCP):** buy-once licensing is appealing, but community MCP + he owns every dev-app + TikTok audit; Postiz is the better-supported self-host. **SKIP** unless he specifically wants perpetual licensing.
- **Hypefury:** X-first, **no MCP/API at all**, and its growth-automation (auto-DM, pods) collides with the hub's human-in-the-loop rule + Meta policy risk. **SKIP.**

### Integration design (keep the existing pipeline intact)

- **Analytics source of truth stays the `instagram` MCP + `ig-dashboard`.** Use Metricool **only as the cross-platform publish layer** — do NOT route IG analytics through it (that's the Buffer/Publer overlap trap and would break his daily-history pipeline).
- **Pipe `auto-clip` output straight into Metricool's `post_schedule_post`.** His clip engine emits **voice-only / original-audio** clips, which qualify for IG + TikTok auto-publish — so clip → caption → schedule runs headless with **one** human approval at the schedule step (preserves the standing rule).
- **Encode a two-lane split in `weekly-content-plan`:** original-audio reels → auto-publish lane; native-only-sound / AR-effect reels → manual/Notify-Me lane. Tag each piece with its publish path up front.
- **Secrets fit:** Metricool's cloud holds each platform's OAuth — it does **not** touch his local `INSTAGRAM_ACCESS_TOKEN` env var. Compatible with the secrets-local rule for the scheduling layer specifically.

---

## PART 2 — Email/newsletter + sponsor CRM + payments (minimal stack)

**Recommended minimal stack: beehiiv (newsletter) + Stripe restricted-key MCP (payments + invoices) + the vault as the sponsor CRM.** No dedicated CRM SaaS.

### Email / newsletter — beehiiv (CONFIRMED, with a correction to the "how")

The blueprint picks beehiiv for newsletter launch — **confirmed**. But note the current capability split (re-verified 2026-06-13):

- **beehiiv MCP (shipped Mar 24, 2026) is read-only V1** — it pulls subscribers/revenue/engagement analytics and emits real-time events (new subs, cancellations, publishes) but **cannot publish posts, send emails, or modify subscriptions** (source: https://product.beehiiv.com/p/beehiiv-mcp ; https://www.beehiiv.com/support/article/39255979546263-getting-started-with-the-beehiiv-mcp).
- **Therefore: do the actual sending via beehiiv's send API, not the MCP.** beehiiv's own guidance is that for production sends, the **API remains the better choice** for formatting/design consistency (source: https://www.beehiiv.com/features/api-and-integrations). The agent **drafts** in beehiiv; the **send click stays Elijah's** (standing rule 1). Use the MCP for analytics/monitoring, the send API for the human-approved send.
- **Trigger:** newsletter launch (a real current gap, per blueprint). **Secrets:** beehiiv API key in a Windows env var (`setx`), never in a synced file.

### Payments — Stripe official MCP (ADD WHEN MONEY MOVES INTO THE HUB)

- **Official `@stripe/mcp` exists** and supports both **local** (`npx -y @stripe/mcp@latest`, key via `STRIPE_SECRET_KEY` env var) and **remote OAuth** (`https://mcp.stripe.com`) modes (source: https://docs.stripe.com/mcp).
- **Secrets-local angle (decisive):** use a **restricted API key** (Stripe's own strong recommendation for agents — minimum permissions, e.g. read-only or invoice-only) stored in a **Windows env var via `setx`** — never in `claude_desktop_config.json` and never in any OneDrive-synced file. This satisfies both the official-MCP-first and secrets-local rules. The remote OAuth mode is an alternative, but the local restricted-key path keeps the secret on-machine, which is the better fit for this hub's posture.
- **What it gives him:** `create_payment_link`, `create_invoice` / `finalize_invoice` / `list_invoices`, `create_customer` / `list_customers`, subscriptions, refunds/disputes, `retrieve_balance`. This is enough to **be** the sponsor-invoicing layer.
- **Human-in-the-loop:** scope the key **read-only by default**; any write (creating an invoice, a payment link, a refund) is a per-action confirmation. Never auto-charge.

### Sponsor CRM — the vault, not a SaaS (ADD NOW, free)

At his scale a dedicated CRM seat is overkill and breaks local-first. The minimal CRM is:

- A `sponsors/` folder in the Obsidian vault (one note per sponsor/deal), following the vault's property contract (`obsidian/Elijah's vault/CLAUDE.md` — never invent property names).
- **Stripe** holds the invoice + payment-status truth; the vault note links to it.
- The existing **`instagram` MCP** already reads/sends DMs (human-in-the-loop) for inbound sponsor conversations — no new tool needed for the top of funnel.
- **SKIP** HubSpot / Notion-CRM / dedicated sponsor-SaaS until the deal volume genuinely outgrows a vault folder. (This matches blueprint Tier C's "no speculative MCPs" discipline.)

---

## PART 3 — Course platform (RESOLVE Whop vs Skool vs self-built for the Archetype Index Kajabi migration)

**VERDICT: migrate the Archetype Index to Whop.** This **resolves the blueprint's open question** (line 60: "unverified whether Whop exposes course-content/community tools").

### The open question is now answered: Whop DOES host courses natively

Re-verified 2026-06-13: Whop is **not** just a payments layer. It ships a native **Courses app** (video lessons, text, files), plus **Chat**, **Forums**, and **Video-calls** apps for community, a storefront, an affiliate/marketplace discovery layer, and a **Whop App Store + Developers section** (modular architecture) (source: https://whop.com/blog/skool-alternatives/ ; https://topwhops.com/whop-vs-skool/). So the blueprint's caveat is cleared: Whop can host the actual course content, not only consolidate payments.

### Decision matrix

| Factor | **Whop** | Skool | Self-built (WP+LearnDash / custom) |
|---|---|---|---|
| Native course hosting (modules/video/drip) | Courses app: video/text/files (less rigid module structure) | **Strongest** — structured modules + drip + classroom layout | Full control, you build it |
| Community | Chat / Forums / Video-calls (transactional feel) | **Strongest** — gamified feed, points, leaderboard | You build/integrate it |
| **Agent control (official MCP/API)** | **YES — first-party hosted MCP `mcp.whop.com`** (products/payments/memberships/checkout) + App Store/dev API | **NO MCP/API for agents** | Possible but you build the surface |
| Fees | **2.7% + $0.30/txn, NO monthly** | $99/mo flat + 2.9% (Hobby $9/mo + 10%) | $498+/yr + ongoing ops |
| Migration off Kajabi | CSV members + manual video download from Kajabi, import to Whop | same import path | same, plus you host everything |
| Maintenance burden | Low (hosted) | Low (hosted) | **High** (you own uptime/security) |

Sources: https://www.learningrevolution.net/skool-vs-whop/ ; https://www.creatoreconomytools.com/vs/skool-vs-whop ; https://thrivecart.com/blog/kajabi-alternatives/ ; https://circle.so/blog/kajabi-alternatives.

### Why Whop wins for THIS hub

1. **It's the only option with a first-party MCP** (blueprint line 60: `mcp.whop.com`, native `claude mcp add --transport sse`). Skool has no agent surface at all; a self-built platform means building the surface yourself. For an agent-driven business hub, **agent-controllability is the deciding axis** — exactly the same logic that made Metricool the scheduling pick.
2. **Lowest, usage-based fees** (2.7% + $0.30, no monthly) vs Skool's $99/mo + 2.9%. For a course that isn't yet at high MRR, no monthly floor de-risks the migration.
3. **Consolidates payments + course + community in one MCP-controllable platform** — and can lean on the existing **Stripe** layer for any off-platform invoicing.

### The honest trade-off (and the tie-breaker question)

Skool genuinely wins on **community engagement** (gamified, social) and **course structure** (clean modules/drip); Whop communities read as more "transactional." So the decision hinges on **what the Archetype Index actually is**: if its value is a *highly-engaged, gamified peer community*, Skool's social layer may justify giving up the MCP and paying the monthly. If it's a *course/product you sell and want your agent team to operate*, Whop is the clear pick (open question O3).

**SKIP self-built / WordPress+LearnDash:** highest build + maintenance burden, no agent surface, and it contradicts the hub's "never build ahead of need" principle. Only revisit if a hosted platform's fees become genuinely punitive at scale.

---

## PART 4 — Personal productivity / knowledge (local-first; reuse what exists)

**VERDICT: nothing new to buy. The local-first stack already exists — extend it, don't replace it.**

The hub already has the right shape for local-first knowledge work, and it aligns with the secrets-local + OneDrive-avoidance posture better than any cloud PKM SaaS:

- **Obsidian vault (`obsidian/Elijah's vault/`)** — the structured second brain and knowledge base. Local files, plain markdown, a strict property contract. This IS the PKM layer; a cloud tool (Notion/Mem) would duplicate it and break local-first. **SKIP cloud PKM.**
- **Reuse `auto-clip/transcribe.py`** — already on disk, uses `faster-whisper 1.2.1` (segment-level today; the auto-clip PLAN adds a word-level wrapper). This is the local transcription brain for turning any audio/video — podcasts, voice memos, meeting recordings — into searchable vault notes at ~$0. No SaaS transcription needed. (Verified in `docs/plans/2026-06-13-auto-clip-pipeline.md`, Premise 1–2.)
- **Reuse the 7AM Windows scheduled task** ("IG Dashboard Daily Refresh" → `Daily Agent Refresh.bat`) as the heartbeat for any recurring personal-productivity automation (e.g. a morning vault digest, a "what's due" roll-up). The cron/scheduled-task infra is already wired — extend the `.bat` or add a sibling engine following the house convention (`BASE = Path(__file__).resolve().parent`, `data/`, `log()` helper, stdlib-first).
- **Capture loop idea (free, local):** voice memo → `transcribe.py` (word-level) → vault note (property-contract-compliant) → optionally surfaced in the 7AM digest. Entirely on-machine, no new dependency, no new secret.

**Why no new tool:** every cloud productivity SaaS would (a) duplicate the vault, (b) put notes off-machine (against local-first), and (c) add a secret/seat. The hub's own engines + vault + scheduled task already cover capture, transcription, storage, and recurrence.

---

## PART 5 — Recommended minimal "wire-now" stack + open questions

### Wire NOW (this week / at the named trigger)

1. **Metricool MCP** — the one new paid commitment. Create account → OAuth-connect each platform inside Metricool (via **Facebook Login** for IG, to unlock licensed-audio) → confirm the Advanced (~$54/mo) MCP gate **in his account** → `claude mcp add` with the API token. Publish layer only; analytics stays on `instagram` MCP + `ig-dashboard`. *(blueprint Tier A — confirmed, price corrected)*
2. **Vault `sponsors/` CRM** — free, today. One note per sponsor, property-contract-compliant; links to Stripe invoices. *(no new tool)*
3. **Extend the 7AM task + reuse `transcribe.py`** for the local capture/digest loop. *(no new tool, no new secret)*

### Wire at the trigger (already gated correctly)

4. **Whop MCP (`mcp.whop.com`)** — at the Archetype Index migration go-decision (pending O3). First-party SSE MCP; migrate course content + payments + community here.
5. **beehiiv** — at newsletter launch. MCP for analytics (read), send **API** for the human-approved send.
6. **Stripe official MCP** — when invoicing/payments move into the hub. **Restricted key in a Windows env var**, read-only by default, per-action confirm on any write.

### Explicitly SKIP

Buffer / Publer / Mixpost / Hypefury (scheduling); HubSpot / dedicated sponsor-CRM SaaS; self-built / WordPress course platform; cloud PKM (Notion/Mem). All either duplicate owned tools, lack an agent surface, or break local-first/secrets-local.

### Open questions for Elijah

- **O1 (Metricool price gate):** Confirm in your own Metricool account that the MCP truly requires Advanced (~$54/mo) for a single brand / your own accounts — or whether a cheaper path unlocks it — **before** committing the spend.
- **O2 (IG licensed-audio reality test):** Does the new "cleared for third-party distribution" audio catalog actually contain the trending sounds you use, or is it too narrow in practice? Run one hands-on test post before relying on it for trend-audio reels. Also confirm your Metricool connection is re-authed via **Facebook Login** (not legacy IG Login), which the feature requires.
- **O3 (course platform tie-breaker — DECIDES Part 3):** Is the Archetype Index primarily a **gamified peer community** (favors Skool) or a **course/product you want your agent team to operate** (favors Whop, the recommended pick)? Your answer flips the verdict.
- **O4 (TikTok headless check):** Confirm in-product that Metricool's MCP auto-publishes TikToks **headlessly** (no app notification) for original/non-trending-sound videos — your `auto-clip` output is voice-only and should qualify, but verify before designing the headless lane.
- **O5 (beehiiv tiers):** Confirm beehiiv's current paid-tier requirement for API send access at launch time (tiers were unsettled in prior research).
- **O6 (Stripe key scope):** Decide the restricted-key scope (read-only vs invoice-write) and store it via `setx` — confirm you're comfortable with even read-only payment data flowing through the agent before wiring.

### Overall confidence

**Medium-high.** Part 1 (scheduling) is **high** — deeply re-validated, primary-doc-anchored. Parts 2–4 verdicts are **high on direction** (official-MCP-first + local-first + secrets-local all point the same way and the platform facts re-verified cleanly today), but the **timing/price specifics** (Metricool's exact MCP plan-gate for his account, beehiiv tiers, the Whop-vs-Skool tie-breaker) carry live-account uncertainty captured as O1/O3/O5 — none of which change the picks, only the spend/sequencing.

### ⚠️ Run note — throttle + post-hoc verification (main loop)
3 of the 4 research agents (email/CRM/payments, course platform, productivity) **failed mid-run to Anthropic's transient throttle** ("Server is temporarily limiting requests — not your usage limit"). Only Part 1 (scheduling) was agent-researched; **Parts 2–4 were reasoned by the synthesis agent from the one surviving finding + its own knowledge**, not freshly fetched. Per `docs/RESEARCH-PROTOCOL.md` the fan-out was **not relaunched** (it would throttle again); instead the load-bearing **tool-existence claims were spot-verified by direct WebSearch — all CONFIRMED**:
- **Whop MCP** — real/official: `@whop/mcp`, `mcp.whop.com/sse`, native Courses/chapters/lessons/assessments tools; no monthly fee, 2.7%+$0.30. (docs.whop.com/developer/guides/ai_and_mcp)
- **Stripe MCP** — official: remote `mcp.stripe.com` (OAuth) or local `npx @stripe/mcp --api-key=…`. (docs.stripe.com/mcp)
- **beehiiv MCP** — real (Mar 2026), but **read-only V1, paid-plans only; Send API is beta + Enterprise-only on request** (sending is gated harder than Part 2 implies).
**Net:** the picks rest on verified facts; Parts 2–4 are sound on direction. For full primary-source depth, re-run those three as a small fresh pass after a true Claude restart (keys live, clean window).
