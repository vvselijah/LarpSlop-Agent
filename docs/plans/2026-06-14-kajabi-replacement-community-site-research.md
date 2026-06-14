# Research + Feasibility Plan — Self-built course/community site (Kajabi replacement) on Archetype Index

**Candidate id:** `kajabi-replacement-community-site`
**Date:** 2026-06-14
**Source:** roadmap STILL-TO-RESEARCH → Infra (`docs/plans/2026-06-14-overnight-roadmap.md` line 154) + vault `To do general/Full self built community website.md`.
**Why he wants it:** the vault note: *"convert everything that used to be on kajabi into the archetype index assessment website — Full community, Gamification, Guided Courses/Classes, Downloadable content, Funnel tracking and creation, Proprietary Tools and resources for users."* The driver is real and stated plainly: *"DMs are blowing up now that we're at 100k followers… up thousands every month and we can't provide proper answers and help to anyone."* He wants a home to send those people that isn't Kajabi.

---

## HEADLINE VERDICT: SKIP the self-built site; ADD-LATER the *cheap slice* (a thin landing/funnel page + the decision itself). Confidence: high. Build effort: full self-build = XL (venture-scale, OneDrive-hostile); the cheap slice = S.

**The honest core, in one breath:** a full self-built course + community + gamification + funnel platform is **its own startup**, not a hub automation. Every credible 2026 OSS option (LearnHouse, ClassroomIO) is an **AGPL-3.0, multi-service Docker + PostgreSQL + Node-22 stack** — precisely the heavy, always-on, OneDrive-synced infrastructure this hub is architected to avoid, and it cannot live on Elijah's machine anyway (a course site needs 24/7 public hosting, which a Windows + OneDrive laptop is not). The hub's own business-ops research **already resolved this exact migration in favor of Whop** (`docs/plans/2026-06-13-business-ops-productivity-research.md` Part 3) and explicitly **SKIPPED self-built / WordPress+LearnDash** as "highest build + maintenance burden, no agent surface, contradicts never-build-ahead-of-need." Nothing found here overturns that — it reinforces it.

**But there is real, cheap value in the slice the prior research didn't name:** the agent team can (1) be the **decision-support layer** that picks the platform and de-risks the migration, and (2) **build the thin landing/funnel asset** — a single static "send-your-DMs-here" page / link-in-bio funnel — using tools the hub **already owns** (Higgsfield/HyperFrames for the creative, the vault for copy, Meta pixel via `meta-ads` MCP for funnel tracking, the planned `dm-routing` layer to feed it). That slice is `S` effort, OneDrive-safe, and attacks the actual pain (a place to send DMs) *today* — without committing to the venture-scale build.

**One sharp correction to the prior pick:** the business-ops research picked **Whop**, but the vault note lists **"Gamification" as a top-line requirement** — and re-verified 2026 sources are unanimous that **Whop has no gamification at all** (no points, no leaderboard, no levels, no progression; communities "work like a chat group — active during launches, quiet otherwise"). If gamification is genuinely load-bearing for the Archetype Index community, the hosted pick should be re-opened as **Skool** (purpose-built gamification, structured classroom + drip) — at the cost of Skool's lack of any agent MCP. That is the real open decision, and it is a **buy-vs-buy** decision, not buy-vs-build. (See "The decision the hub should actually make.")

---

## WHAT IT IS / WHAT IT DOES

The vault note asks for six things to replace Kajabi for the **Archetype Index** (a personality classifier with an automated PDF-report pipeline — a *product you sell + a community around it*, per the vault project list):

1. **Full community** — feed/forums/chat among members.
2. **Gamification** — points, levels, leaderboards to drive engagement.
3. **Guided courses/classes** — modules, lessons, drip scheduling.
4. **Downloadable content** — gated files/resources.
5. **Funnel tracking and creation** — landing pages → checkout → conversion analytics.
6. **Proprietary tools/resources for users** — i.e. the Archetype Index assessment itself, embedded.

That is the **full Kajabi feature set** plus a custom embedded app (#6). Building all six yourself is a SaaS product. The question this candidate poses — *should the hub build it from open source rather than buy it* — has a clear answer below: **no**, with one buy-vs-buy nuance and one cheap-slice yes.

---

## BEST 2026 OSS TOOL(S) / APPROACH + LICENSE

Three real options survive a 2026 scan. All are genuinely capable — and all are **the wrong shape for this hub**.

| Option | License | Stack / weight | What it gives | Verdict for THIS hub |
|---|---|---|---|---|
| **LearnHouse** (`github.com/learnhouse/learnhouse`, 1.7k★, v1.2.6 **Jun 13 2026** — actively maintained) | **AGPL-3.0** (Enterprise license for SSO/multi-org) | **Heavy**: Next.js + **FastAPI/Python** + **PostgreSQL** + **Redis** + **S3** + Yjs/Hocuspocus realtime, all via **Docker Compose**. AI = Google Gemini + LlamaIndex. | Block-based course editor, Stripe payments (Enterprise), community discussions, certificates, analytics, white-label, REST API + CLI. **Gamification not a first-class feature.** | **SKIP for self-host.** Best-built OSS option, but it's a 5-service Docker stack needing a 24/7 public host — not a thing that runs on a OneDrive-synced Windows laptop. AGPL means any hosted/network use obligates source disclosure of modifications. |
| **ClassroomIO** (`github.com/classroomio/classroomio`) | **AGPL-3.0** | **Heavy**: SvelteKit + **Supabase (Postgres)** + a separate **api** service (PDF/video/email) + **Docker** + **Node ≥22** + custom SMTP. Mono-repo of 3 apps. | "Alternative to Moodle/Teachable/Skool" — courses, dashboards, student forums, AI lesson planning, auto video transcription. | **SKIP for self-host.** Same class of problem: Supabase + a second backend + SMTP + Docker. Cloud-hosted version exists, at which point you're buying SaaS anyway. |
| **WordPress + LearnDash** (or Moodle) | GPL plugin / GPL | WordPress + MySQL + LMS plugin + membership + community plugins (BuddyBoss) + a host | The classic build-your-own LMS. Endless plugins, full control. | **SKIP** — already rejected by prior research; highest *ongoing* maintenance + security-patching burden, no agent surface, plugin-sprawl. |

**License takeaway:** the two purpose-built modern options are **AGPL-3.0**. AGPL's network-use clause means if you host a modified version for your users, you must offer them your source. For a vanilla self-host that's a non-issue; it only bites if Elijah wanted to fork-and-close it. Not a blocker — but it's a real obligation worth knowing, and it removes any "secret sauce moat" argument for self-hosting.

**Approach takeaway:** there is **no lightweight, single-file, local-first OSS** that does community + gamification + courses + funnels. The category is inherently a multi-service web app with a database and a public host. That is the structural reason this is buy-not-build for Elijah — same conclusion the OSS-CRM survey reached in the `dm-routing` research ("no good JSON/DB-free single-user option → use the vault / buy hosted").

**The honest build-vs-buy math:** a hosted platform (Whop 2.7%+$0.30 no-monthly, or Skool $99/mo) costs ~$0–100/mo and zero ops. A self-host costs a VPS (~$10–40/mo for the RAM these stacks want) **plus** Elijah-or-Tanner owning uptime, security patches, backups, AGPL compliance, and the embedding of the Archetype assessment — indefinitely. The "savings" are negative once a human's maintenance time is priced in. Build only buys you control/white-label, which the Archetype Index doesn't currently need.

---

## WINDOWS + ONEDRIVE FEASIBILITY + DEPENDENCY WEIGHT

**Red. This is the decisive constraint, and it kills the self-host on-machine outright.**

- **A course/community site must be publicly reachable 24/7.** Elijah's machine is a personal Windows laptop on OneDrive — not a server. Members can't hit `localhost`. So even ignoring everything else, self-hosting *on the hub box* is a category error; it would have to live on a VPS/cloud, at which point it's no longer "local-first" and the hub's posture stops applying.
- **The stacks are exactly what the hub avoids.** LearnHouse = Next.js + FastAPI + Postgres + Redis + S3 + Docker. ClassroomIO = SvelteKit + Supabase + a Python/Node api + SMTP + Docker. These are **multi-container, always-on, database-backed** apps — the heaviest possible dependency profile.
- **OneDrive actively breaks this.** Known-bad interactions confirmed in research: OneDrive's file locking corrupts `node_modules` operations and Postgres data files; Docker volume mounts onto synced folders cause performance/corruption issues. The hub's own memory note already flags that *heavy torch/cv2 imports hang on the OneDrive disk* — a Postgres data directory + `node_modules` for a Next.js app is the same hazard, worse. **Any such project would have to live entirely off the synced disk**, which the hub already mandates for big models.
- **Dependency flags:** no torch/cv2, but **heavy** (Docker, Postgres/Supabase, Redis, Node 22, FastAPI), **cloud/host-required** (must be publicly hosted), and **effectively paid** (VPS + Stripe fees + possibly AGPL-Enterprise tier for SSO). Every flag the brief asked me to raise is raised.

**The cheap slice, by contrast, is green:** a single **static landing/funnel page** (HTML/CSS, or generated via the hub's existing Higgsfield/HyperFrames + vault copy) has **zero** runtime, **zero** database, deploys to any static host (or a link-in-bio tool) in minutes, and the source markdown/HTML sits harmlessly in the vault/repo. That is the only piece of this candidate that belongs near the hub.

---

## THE DECISION THE HUB SHOULD ACTUALLY MAKE (decision-support, the real value)

The candidate's true value is **resolving the platform choice**, which is *buy-vs-buy* (Whop vs Skool), not buy-vs-build. The agent team should drive this decision, not build a server:

- **Prior pick = Whop**, chosen for its **first-party MCP** (`mcp.whop.com/sse`, agent-controllable: list/create resources, memberships, checkout) and **no monthly fee** (2.7%+$0.30). Confirmed live: Whop has official MCP servers and native Courses/Chat/Forums apps.
- **The gap the prior research under-weighted:** the vault note makes **gamification a top-line requirement**, and **Whop has none** (verified 2026: no points/levels/leaderboards; "active during launches, quiet otherwise"). **Skool** is the purpose-built gamification + structured-classroom + drip option — but has **no MCP/API** for the agent team and costs **$99/mo + 2.9%**.
- **So the real tie-breaker (open question O3 from the prior research, still unresolved):** is the Archetype Index community's value its **gamified engagement** (→ Skool, give up agent control) or a **product/course the agent team operates** (→ Whop, give up gamification)? A hybrid is viable: **Skool for the gamified community/courses + Stripe (official MCP, restricted key) for the agent-operated payments/invoicing**, accepting that Skool itself stays hand-driven.
- **Either way: the agent does NOT build the platform.** Its job is to (a) make this recommendation with the gamification correction surfaced, (b) prep the **Kajabi → [chosen platform] migration** (CSV member export, video/file inventory, mapping the Archetype assessment embed), and (c) build the funnel asset below to feed it.

---

## HOW THE CHEAP SLICE COMPOSES WITH THE HUB (integration sketch)

The one buildable, hub-appropriate deliverable is a **thin landing/funnel asset + its tracking**, using only owned tools. This is the "place to send the DMs" the pain demands, deliverable now, independent of the platform decision.

```
Archetype Index offer (vault: 40-Projects/Archetype-Index)
        │  copy + positioning (team/profile.md voice)
        ▼
[landing/funnel page]  ← built with Higgsfield (hero/creative) + HyperFrames/static HTML
        │                 (NO server, NO db — static deploy or link-in-bio)
        │
        ├─► Meta Pixel / dataset event  ──► meta-ads MCP (ads_pixel_event_*, ads_get_dataset_stats)
        │        (funnel tracking #5 — READ freely; any write/create = confirm)
        │
        ├─► checkout link  ──► Whop (MCP) OR Skool OR Stripe payment-link (restricted-key MCP)
        │
        └─► fed by inbound DMs  ──► the planned `dm-routing` layer drafts an in-thread reply
                 (human-approved) that routes the lead to THIS page — never a cold outbound
```

- **Engine/skill:** no new engine. Creative via `higgsfield-generate` / `higgsfield-product-photoshoot`; page assembly via HyperFrames or hand-written static HTML living in the repo/vault; copy from `team/profile.md` + the Archetype offer KB.
- **Funnel tracking (#5):** use the **`meta-ads` MCP** — it already exposes `ads_pixel_event_*`, `ads_pixel_parameter_*`, `ads_get_dataset_stats/quality`, `ads_get_customconversions`. So "funnel tracking and creation" is *already an owned capability* against a Meta pixel on the static page — no self-built analytics needed. (Read freely; any pixel/event **write** is a per-action confirm per Standing Rule 2.)
- **Lead feed:** the planned **`dm-routing-va-or-agent`** layer (`docs/plans/2026-06-14-dm-routing-va-or-agent-research.md`) is the natural front door — it qualifies a DM lead and drafts an **in-thread** reply routing them to this page (inbound-only, human-approved; **never** a cold DM).
- **Payments/checkout:** the chosen hosted platform's link, or a **Stripe payment-link** via the official Stripe MCP (restricted key in a Windows env var) — already specced in the prior research.
- **Data shapes:** static page = HTML + assets (in repo, not OneDrive-thrashing). Funnel events = Meta pixel events `{event_name, value, currency, custom_data}` read back via `ads_get_dataset_stats`. Lead → page handoff reuses the `dm-routing` in-session record (`{conversation_id, igsid, next_action: route, draft_reply}`).
- **Vault:** the offer copy, funnel variants, and the platform-decision write-up live as **property-contract-conformant** notes (reuse `idea`/`decision`/`task` templates from `_templates/`; do **not** invent properties — vault CLAUDE.md is law).

---

## PHASED BUILD SKETCH

### Phase 0 — DECISION + landing page (smallest safe thing) — **S, no new deps, no server**
- **Resolve the platform** (decision-support, not a build): present Whop-vs-Skool with the **gamification correction** front and center, and the hybrid (Skool community + Stripe-MCP payments) option. Get Elijah's call. Log to `team/memory.md` + a vault `decision` note.
- **Build the static landing/funnel page**: Higgsfield hero + HyperFrames/static HTML, copy from the vault offer KB, a Meta pixel snippet, and a single CTA → the chosen checkout link. Deploys to a static host or link-in-bio; **nothing runs on the hub box**.
- **Exit:** there is a real URL to send DMs to, with a pixel firing into the `meta-ads` dataset, independent of any heavy infra.

### Phase 1 — Wire the funnel loop — **S**
- Point the (planned) `dm-routing` layer's `route` next-action at the new page; confirm pixel events land via `ads_get_dataset_stats` (read-only).
- Prep the **Kajabi → chosen-platform migration kit**: member CSV export, a video/downloadable inventory, and the mapping for embedding the Archetype assessment (#6) into the chosen platform.
- **Exit:** inbound DM → human-approved in-thread route → page → tracked event, and the migration is a checklist away.

### Phase 2 — Execute the hosted migration (Elijah/Tanner-led, agent-assisted) — **M, still buy-not-build**
- Import members + content into Whop/Skool; embed the Archetype assessment; set up courses/community/gamification *in the hosted product's UI*.
- If Whop: wire its MCP for agent-operated memberships/checkout. If Skool: accept hand-driving + Stripe-MCP for payments.
- **Exit:** Kajabi is retired onto a hosted platform; the agent operates whatever surface that platform exposes.

### Phase 3 — ONLY-IF-EVER: self-host (explicitly deferred, likely never)
- Revisit a self-hosted LearnHouse/ClassroomIO on a **proper VPS (off the OneDrive box)** *only* if a hosted platform's fees become genuinely punitive at high MRR **and** Elijah/Tanner want white-label control worth owning the ops. This is a standalone venture-scale project with its own plan, its own host, and a named ops owner — not a hub task. AGPL compliance applies.

---

## RISKS / ToS / BAN RISK

- **Maintenance/ops debt (the headline risk of the self-build path):** a self-hosted multi-service web app is a permanent liability — security patches, DB backups, uptime, dependency churn — with no owner currently assigned. This is exactly the "never build ahead of need" trap the hub's CLAUDE.md warns against. *Mitigation: don't self-host; buy hosted.*
- **OneDrive/Windows data corruption:** running Postgres/`node_modules`/Docker volumes on the synced disk risks corruption + sync thrash (confirmed pattern; mirrors the hub's torch/cv2-hang note). *Mitigation: the cheap slice is static (no runtime); any real app must live off-machine on a VPS.*
- **AGPL-3.0 obligation:** hosting a *modified* LearnHouse/ClassroomIO for users triggers source-disclosure of changes. Not a blocker for vanilla self-host, but kills any "proprietary moat" rationale. *Mitigation: known + documented; irrelevant if buying hosted.*
- **Cold-DM ban risk (inherited from the lead feed):** routing DMs to the funnel page must be an **in-thread reply to someone who messaged first**, inside the 24h window — never a cold outbound sales link. Sending the first message / pushing promo to a non-engager is a bannable Meta integrity violation (per the `dm-routing` research). *Mitigation: the funnel is fed only by the human-approved, inbound-only `dm-routing` rails.*
- **Meta Ads write-gate:** any pixel/event/dataset **creation** via `meta-ads` MCP is a write → Standing Rule 2 per-action confirm. Reads (funnel stats) are free. *Mitigation: default to read; confirm any pixel write.*
- **Vault property contract:** decision/offer/funnel notes must reuse `_templates/` verbatim — no invented properties. *Mitigation: obey vault CLAUDE.md.*
- **Platform-fee / lock-in risk (the buy path):** Whop's % with no monthly is low-risk at low MRR; Skool's $99/mo is a fixed floor; both create some lock-in (export is CSV + manual video download). *Mitigation: it's the same migration-import work whichever way, and far cheaper than owning a server.*
- **No scraper/ToS-gray risk** in the cheap slice: static page + official Meta pixel + official MCPs only.

---

## HONEST BOTTOM LINE

The vault note describes a **second startup** (course + community + gamification + funnels + an embedded custom app), and the only credible 2026 OSS to build it (LearnHouse, ClassroomIO) are **AGPL-3.0, Docker + Postgres + Node multi-service stacks** that need a 24/7 public host and are actively hostile to a OneDrive-synced Windows laptop. The hub already correctly resolved this migration as **buy, not build** — and this pass reinforces that, while surfacing one real correction: **the prior Whop pick conflicts with the note's explicit gamification requirement** (Whop has none; that points back toward **Skool**, or a Skool-community + Stripe-MCP-payments hybrid). So **SKIP the self-built site** — it's venture-scale, OneDrive-hostile, and a permanent ops liability with no owner.

The **ADD-LATER, S-effort value** is the slice the prior research never named: **(1) make the platform decision** (with the gamification correction), and **(2) build the thin static landing/funnel page** — the actual "somewhere to send the exploding DMs" the pain demands — using tools the hub **already owns** (Higgsfield/HyperFrames creative, vault copy, **`meta-ads` MCP pixel for the funnel tracking he listed**, the planned `dm-routing` layer as the inbound-only feed). That asset ships now, runs on zero infrastructure, and de-risks the eventual hosted migration — which is the right way to honor the goal without building a startup inside a laptop.

---

## SOURCES

- [4 Best Open Source Kajabi Alternatives in 2026 — OpenAlternative](https://openalternative.co/alternatives/kajabi) (ClassroomIO, LearnHouse, CourseLit; LearnHouse = AGPLv3)
- [LearnHouse on GitHub](https://github.com/learnhouse/learnhouse) (AGPL-3.0; Next.js + FastAPI + Postgres + Redis + S3 + Yjs; 1.7k★, v1.2.6 Jun 13 2026; Docker + CLI)
- [LearnHouse community-edition (Docker Compose)](https://github.com/learnhouse/community-edition) · [Self-hosting docs](https://docs.learnhouse.app/self-hosting)
- [ClassroomIO on GitHub](https://github.com/classroomio/classroomio) (AGPL-3.0; SvelteKit + Supabase + separate api service + Docker + Node ≥22 + SMTP)
- [Best Online Course & Community Platforms 2026 — Heights](https://www.heightsplatform.com/blog/best-online-course-and-community-platforms)
- [Skool vs Whop (2026) — LearningRevolution](https://www.learningrevolution.net/skool-vs-whop/) (Skool = gamified community + classroom/drip; Whop = modular storefront)
- [Whop vs Skool: Which Has Better Courses (2026) — TopWhops](https://topwhops.com/whop-vs-skool/) (Whop has no points/leaderboard/levels/progression; "active during launches, quiet otherwise"; Skool = chapters + drip)
- [Whop vs. Skool — BloggingX (2026)](https://bloggingx.com/whop-vs-skool/) (gamification +40% engagement; Whop community ≈ Discord/chat group)
- [Whop AI & MCP developer docs](https://docs.whop.com/developer/guides/ai_and_mcp) (official `mcp.whop.com/sse` + docs MCP; agents list/create resources)
- [Top 10 Self-Hosted LMS 2026 — HostStage](https://www.host-stage.net/case-study/top-self-hosted-lms/) (self-hosted LMS want a VPS, ~8GB RAM min for production)
- Internal: `docs/plans/2026-06-13-business-ops-productivity-research.md` Part 3 (prior Whop pick + self-built SKIP + open question O3); `docs/plans/2026-06-14-dm-routing-va-or-agent-research.md` (the inbound-only, human-approved DM lead feed; OSS-CRM-is-OneDrive-hostile finding); `docs/plans/2026-06-14-overnight-roadmap.md` line 154 (candidate framing); `obsidian/Elijah's vault/To do general/Full self built community website.md` (the six requirements + the DM-volume driver); `obsidian/Elijah's vault/CLAUDE.md` (property contract); `CLAUDE.md` (never-build-ahead-of-need; OneDrive/secrets constraints)
