# Research: meta-stats-opensource-app — productize/OSS the ig-dashboard

**Candidate:** `meta-stats-opensource-app` — turn the hub's most mature asset (`ig-dashboard/` + the brand-new `ig-dashboard/metrics2026.py`) into a sellable/open-source Meta-stats tracker with an Obsidian-linked dashboard.
**Source:** `docs/plans/2026-06-14-overnight-roadmap.md` (STILL-TO-RESEARCH → Infra); vault `Brainstorming/In the moment ideas.md` line 18 ("create some type of possibly opensource app to fully track meta stats / Obsidian link / Full refresh analytics / Content breakdown / Dashboard").
**Date:** 2026-06-14 · **Researcher:** overnight roadmap, Wave (this pass)

---

## Headline verdict: ADD-LATER (lean OSS template) / SKIP the SaaS

**Build effort: the *useful* slice is S–M (~1 day). The *ambitious* slice is weeks + ongoing compliance.**

Split the candidate cleanly, because it's really three different products wearing one name:

| Sub-product | Verdict | Why |
|---|---|---|
| **A. OSS single-user template** (genuinely de-personalize the existing engine → public repo anyone runs on *their own* account) | **ADD-LATER** ⭐ | The real, achievable version. ~80% built. **No Meta App Review needed** (own-account = Development mode). Content/credibility angle is real. Gate = ~1 day of de-hardcoding + a clean README, and Elijah actually *wanting* to maintain a public repo. |
| **B. Obsidian-linked dashboard** ("Obsidian link" line) | **ADD-LATER** (cheap P0) | Partly stubbable today: the vault already has a `dashboard` note `type`, and the Obsidian ecosystem (Charts View / Dataview / Activity Dashboard) renders frontmatter into charts. A nightly export of `metrics2026` output into a templated `dashboard` note is a ~half-day add. Low value vs. the existing HTML dashboard, but it's the literal ask. |
| **C. Multi-account / sellable SaaS** ("sellable" framing) | **SKIP for now** | The expensive trap. Multi-tenant = Meta **App Review + Business Verification + OAuth login flow + per-user token refresh + 200-req/hr/user budgeting + ongoing compliance/webhooks**. That's a 4–6 week build *before* product-market fit, for a market already crowded by paid tools — and it's a SaaS business, not a hub feature. Don't start it as part of the hub. |

**Bottom line:** the high-leverage, honest move is **ship A as a stripped, MIT-licensed public repo of what already works** (a credibility/content artifact and a genuinely-better-than-the-OSS-field tool because it uses the *official consented API*, not scrapers), optionally bolt on **B** as a vault export. **Do not** chase **C** as a hub project — it's a separate company with a real go-to-market cost, and the dependency that kills the "easy 80% done" framing isn't code, it's Meta's review/compliance treadmill.

---

## What it actually is / does

The idea note is four lines: *opensource app · Obsidian link · full refresh analytics · content breakdown · dashboard.* Decoded against what's on disk, every one of those already exists in the hub:

- **`ig-dashboard/refresh.py`** (415 lines, pure stdlib + `curl.exe`) — syncs 300 posts + per-post insights with velocity history, daily account metrics with follower/non-follower view split, audience-online hours, and follower demographics from the **official** Instagram Graph API v22.0. Writes `data/store.json` + `data/data.js`. Runs daily at 7AM via Task Scheduler. "Full refresh analytics" = done.
- **`ig-dashboard/dashboard.html`** (28KB, single-file) — Overview / Posts / Strategy / Compare tabs. "Dashboard" + "content breakdown" (category mix, posts-vs-results bubbles, best day/hour) = done.
- **`ig-dashboard/metrics2026.py`** (created 2026-06-14, today) — the canonical 2026 scoring contract: six priority rates (skip/share/like/save/repost/comment) with skip-rate as a hard gate, percentile-ranked against Elijah's own 300-post distribution. Pure stdlib. This is the "fresh metrics2026.py" the candidate wants to ship.
- **Vault** already defines a `dashboard` note `type` (see `obsidian/Elijah's vault/CLAUDE.md` property contract) — the "Obsidian link" hook is half-wired.

So the candidate is **NOT a build-from-zero**. It's: (1) de-personalize the engine so a stranger can run it (today it hardcodes `ACCOUNT_ID = 17841400159953101` and reads `INSTAGRAM_ACCESS_TOKEN`), (2) write setup docs, (3) optionally pipe output into the vault as a `dashboard` note, (4) decide OSS-vs-paid + license. **Research scope = productization, exactly as the candidate states.**

### The OSS landscape it would join (and why the hub's engine is already better)

I checked the live GitHub field for "Instagram analytics dashboard." The decisive finding: **the popular ones are NOT official-API and NOT free.**

- `reachvivek/Instagram-Analytics-with-Growth-Dashboard` and `aslyadneva/Instagram-Analytics-Dashboard` (the two highest-profile "IG analytics dashboard" React repos) both run on the **IGBlade API** — a *paid third-party* service, no Meta consent flow, ToS-gray. Not self-hostable without buying a key. ([reachvivek repo](https://github.com/reachvivek/Instagram-Analytics-with-Growth-Dashboard))
- The genuinely-private-API tools (`subzeroid/instagrapi`, `misiektoja/instagram_monitor`, `XD-MHLOO/Osintgraph`) are **scrapers / unofficial API** — explicitly ToS-violating and ban-risky. The hub's standing rules forbid this path. ([instagrapi](https://github.com/subzeroid/instagrapi), [instagram_monitor](https://github.com/misiektoja/instagram_monitor))
- The closest *official-Graph-API* OSS analytics tool, `nielsuit227/SocialMediaAnalytics`, is **4 stars, last touched 2023** — i.e. the legitimate niche is wide open but also has ~zero proven demand. ([GitHub instagram-graph-api topic](https://github.com/topics/instagram-graph-api))

**Implication for the verdict:** the hub's engine is *differentiated* (official consented API, no scraper, no paid key, runs locally) — a real reason an OSS release could stand out. But the same emptiness of the legitimate niche is a demand red flag: the people who want IG analytics mostly reach for paid SaaS or scrapers, not a self-hosted Python repo they have to wire a Meta app into. **Differentiation is real; market pull is weak.** That's exactly an ADD-LATER (build the cheap version, don't bet on it) — not an ADD-NOW.

---

## Best 2026 approach + license

**Approach: keep the existing stack. Do NOT rewrite into a framework.** The engine's whole virtue is that it's stdlib + `curl.exe` + one HTML file — zero install, OneDrive-safe, no torch/cv2/cloud/paid. A "productized" rewrite into React/Next + a server + a DB would *destroy* the property that makes it shippable here and would cross into SaaS territory (sub-product C). The right OSS form is "clone, set two env vars, run `python refresh.py`, open the HTML."

**License: MIT.** Permissive, expected for a small dev tool, lets it be a credibility artifact without GPL friction. (None of the comparable repos publish a clear license — shipping a clean MIT one is itself a small differentiator. Confirm no GPL-licensed code gets vendored in `ig-dashboard/vendor/` before publishing.)

**Obsidian side (sub-product B):** don't build a custom plugin. Reuse the existing community plugins — **Charts View** (Dataview-driven bar/pie/radar) or **Dataview** + **Activity Dashboard** — which already render note frontmatter into charts. The hub's job is only to *write a well-formed `dashboard` note* with the metrics as frontmatter; the plugins draw it. ([Obsidian Charts View](https://www.obsidianstats.com/plugins/obsidian-chartsview-plugin), [Obsidian dashboard plugins](https://www.obsidianstats.com/tags/dashboard))

---

## Windows + OneDrive feasibility + dependency weight

**GREEN across the board — for sub-products A and B.** This is the candidate's genuine strength:

- **Zero heavy deps.** `refresh.py` and `metrics2026.py` are pure stdlib (`json`, `subprocess`, `statistics`, `datetime`). No torch, no cv2, no numpy, no cloud SDK, no paid key. Nothing to hang on the OneDrive disk.
- **Official API, read-only, existing token** — `INSTAGRAM_ACCESS_TOKEN` already lives in a Windows env var (never in the synced tree), exactly per the hub's secret rule. The OSS template inherits this pattern (env var, never a committed file).
- **The `vendor/` folder + `data/` need scrubbing before publishing.** `data/store.json` contains Elijah's real account data and must be `.gitignore`d / excluded from any public repo. This is the one concrete pre-publish chore.
- **Sub-product C is where the weight appears — and it's not dependency weight, it's *compliance* weight:** OAuth login UI, secure multi-user token storage, automated 50–55-day token refresh per user, 200-req/hr/user rate-limit budgeting, webhooks, and Meta App Review + Business Verification. None of that is OneDrive-unsafe, but all of it is real engineering + legal/process load, and it turns a local tool into a hosted service. Flag: **SaaS = a server + a DB + a review process, none of which belong in a OneDrive-synced single-user hub.**

---

## How it composes with the hub (integration sketch)

The composition is unusual for this roadmap: **most candidates ADD a tool to the hub; this one EXTRACTS an existing tool *out* of the hub** (as a public repo) and optionally **threads it back** through the vault. Two concrete wires:

### Wire 1 — OSS extraction (sub-product A)
```
ig-dashboard/ (hub copy, stays personalized)
      │  de-hardcode: ACCOUNT_ID + token → env/config, scrub data/
      ▼
new public repo  meta-stats-tracker/   (MIT)
   refresh.py        ← config.example: IG_ACCOUNT_ID + IG_ACCESS_TOKEN env
   metrics2026.py    ← the 2026 scoring contract, generalized
   dashboard.html    ← unchanged single-file viewer
   README.md         ← "make a Meta app, get a token, set 2 env vars, run"
   .gitignore        ← data/, *.log, vendor third-party if license-incompatible
```
- **Data shape unchanged:** `store.json` → `data.js` (`window.DASHBOARD_DATA = {posts, daily, demographics, ...}`) → HTML. A stranger's repo produces the identical shape for their own account.
- **No new hub plumbing.** The hub keeps its personalized copy; the public repo is a *fork-point*, maintained in parallel. (Honest cost: now there are two copies to keep in sync — a maintenance tax that argues for keeping the public repo *minimal* and not back-porting hub-specific features.)

### Wire 2 — Obsidian link (sub-product B)
```
metrics2026.rank_posts(store)  →  top-N + category rollup (JSON)
      │   (new ~40-line writer, fork of refresh.py::write_stats_md)
      ▼
obsidian/Elijah's vault/ … /IG Dashboard.md     type: dashboard   (frontmatter = metrics)
      ▼   rendered by Charts View / Dataview plugin (already installable)
   in-vault chart of skip-grade / share-rate / category mix
```
- **Composes with:** `ig-dashboard/refresh.py::write_stats_md()` (the existing `team/stats.md` writer is the exact pattern to clone — it already crosses from the engine into a markdown file the rest of the hub reads). Downstream: `weekly-content-plan`, `reel-analytics`, `niche-intel` already read `team/stats.md`; a `dashboard` vault note gives Elijah the same numbers *inside Obsidian* with charts.
- **HARD CONSTRAINT:** obey the vault property contract (`obsidian/Elijah's vault/CLAUDE.md`). Use the existing `dashboard` `type`; **do NOT invent new property names**; copy the `_templates/` block exactly. Never overwrite a human-written body — write only frontmatter, mirroring the existing ingestion rule.

---

## Phased build sketch

**Phase 0 — smallest safe thing (~30 min, zero risk): the vault `dashboard` note export.**
Add a `write_dashboard_note()` (a near-clone of `write_stats_md()` in `refresh.py`) that emits one `type: dashboard` note into the vault with `metrics2026` top-line numbers as frontmatter, using the exact `_templates/dashboard` property block. Delivers the literal "Obsidian link + content breakdown + dashboard" ask *today*, no new repo, no Meta work, no dependency. **This is the only piece worth doing immediately.**

**Phase 1 — OSS-template extraction (~1 day, gated on Elijah wanting a public repo).**
- De-hardcode `ACCOUNT_ID` → `IG_ACCOUNT_ID` env/config; keep `INSTAGRAM_ACCESS_TOKEN` env pattern.
- Add `config.example`, `.gitignore` (exclude `data/`, logs), strip Elijah-specific category keywords into a sample config.
- Audit `vendor/` for license compatibility; add `LICENSE` (MIT) + a README walking a stranger from "create a Meta Business app" → "long-lived token" → "set 2 env vars" → "run."
- Publish as a separate public repo. **No App Review needed — each user runs it on their own account in their app's Development mode.**

**Phase 2 — polish for external users (~1–2 days, demand-gated).**
- Token-refresh helper script (the 50–55-day refresh the README must explain), better error messages, a `--demo` mode with synthetic data so people can see the dashboard before wiring a token. Only do this if the repo gets real traction.

**Phase 3 — multi-account / SaaS: DO NOT BUILD as a hub project.**
If Elijah ever genuinely wants to sell it, that's a standalone company: OAuth, hosted server, DB, per-user token vault, Meta App Review + Business Verification, rate-limit budgeting, billing. Out of scope for the hub; re-scope as its own product with its own plan.

---

## Risks / ToS / ban

- **App Review is the real gate — and it only bites the SaaS version.** A single-user tool on your *own* account, app kept in Development mode, needs **no App Review** ("for a single solo project that only needs Instagram, building direct is reasonable"). The moment it accesses data for *external users*, App Review + Business Verification kick in (4–6 weeks, ongoing). This is the precise line between ADD-LATER (A/B) and SKIP-for-now (C). ([elfsight 2026 guide](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/), [getphyllo rate-limit guide](https://www.getphyllo.com/post/instagram-api-rate-limits-explained----and-how-to-scale-beyond-them-2026/))
- **Token treadmill.** Long-lived tokens last ~60 days and don't auto-renew; refresh every 50–55 days. The OSS README must teach this or every user's tool silently dies in two months. (The hub already tracks this via `HANDOFF.md §4`.)
- **Rate limits: 200 req/hr per Instagram account.** Fine for one creator's daily refresh; a budgeting concern only for the multi-account SaaS path.
- **Don't ship a scraper to "compete" with IGBlade-based repos.** The temptation in the OSS field is to add unofficial-API features for parity. That would violate Meta ToS and the hub's standing rules, and risk account bans. The whole point of differentiation here is staying *official-API-only*. Hold that line.
- **Pre-publish data hygiene.** `data/store.json` and `data/refresh.log` contain Elijah's real metrics — must be excluded from any public repo. One-time scrub + `.gitignore`.
- **Metric-availability caveat (inherited from the 2026 metric-engine research).** `reels_skip_rate` / `reposts` are newly machine-readable (Dec-2025) but field availability is still uneven and not in all docs — `metrics2026.py` already degrades the skip-gate to NEUTRAL when absent, which is the right behavior for a tool other people run on accounts that may not surface those fields yet. ([elfsight metrics list](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/))
- **Maintenance tax of two copies.** Forking the hub's engine into a public repo means every future hub improvement has to be consciously back-ported (or not). Keep the public repo deliberately minimal to limit this.

---

## Honest read

This is the roadmap's classic "80% done!" mirage. The 80% that exists (the engine) is real and good — genuinely better than most of the OSS field because it's official-API, not a scraper. But the **20% that's left is not 20% of the *value*** — it's the productization, and productization splits into a trivial part (publish what works, MIT, ~1 day) and an enormous part (multi-tenant SaaS with Meta's review/compliance machinery). The candidate's framing ("research only needs to scope productization") quietly assumes the hard 20% is light. It isn't, for the sellable version.

So: **ship the cheap, honest version** — a Phase-0 vault `dashboard` note now, and a Phase-1 MIT OSS template when Elijah wants a public artifact (it doubles as a content/credibility piece and aligns with his SaaS interest *as a portfolio piece*, not as a revenue line). **Refuse the SaaS framing** until there's a real demand signal, because that path is a company, not a hub feature, and its blocker is Meta's process, not the code.

---

## Sources

- [GitHub topic: instagram-graph-api](https://github.com/topics/instagram-graph-api) — the legitimate official-API OSS field (thin; `SocialMediaAnalytics` 4★, 2023).
- [GitHub topic: instagram-analytics](https://github.com/topics/instagram-analytics)
- [reachvivek/Instagram-Analytics-with-Growth-Dashboard](https://github.com/reachvivek/Instagram-Analytics-with-Growth-Dashboard) — confirmed IGBlade-API (paid third-party), not official Graph API.
- [subzeroid/instagrapi](https://github.com/subzeroid/instagrapi), [misiektoja/instagram_monitor](https://github.com/misiektoja/instagram_monitor) — private-API scrapers (ToS-violating; out of bounds for the hub).
- [Elfsight — Instagram Graph API Complete Developer Guide for 2026](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/) — 2026 metrics list, 60-day token, App Review, 200 req/hr.
- [Phyllo — Instagram API rate limits & scaling 2026](https://www.getphyllo.com/post/instagram-api-rate-limits-explained----and-how-to-scale-beyond-them-2026/) — per-account 200/hr, multi-account limits, app review timeline.
- [DiviPeople — Instagram's API in 2026: what changed](https://divipeople.com/instagram-api-2026/) — Basic Display EOL, Professional-account requirement, single-solo-project guidance.
- [Obsidian Charts View plugin](https://www.obsidianstats.com/plugins/obsidian-chartsview-plugin) and [Obsidian dashboard plugins](https://www.obsidianstats.com/tags/dashboard) — render vault frontmatter into charts (the "Obsidian link" path).
- Local: `ig-dashboard/refresh.py`, `ig-dashboard/metrics2026.py`, `ig-dashboard/README.md`, `obsidian/Elijah's vault/CLAUDE.md` (property contract), `docs/plans/2026-06-14-overnight-roadmap.md`, vault `Brainstorming/In the moment ideas.md` (source idea).
