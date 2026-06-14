# Ad-Omnipresence Reverse-Engineer — research + build/feasibility plan

**Date:** 2026-06-14
**Candidate id:** `ad-omnipresence-reverse-engineer`
**Title:** Find "everywhere" winning campaigns via Meta Ad Library and replicate for his own products.
**Source flag:** vault `Brainstorming/In the moment ideas.md`, heading **"reverse engineering top tier marketing ad strategies"**. Elijah's exact words: *"whenever I notice an ad or company that keeps coming in front of me on my feed in every app… that's an indicator that whoever is running this ad campaign knows what they're doing… figure out either who that ad company is or the strategies they used… so I can do that myself with our softwares in different niches… Figure out how to do that with our products."* Roadmap: STILL-TO-RESEARCH → Intel (line 103).
**Pairs with:** `docs/plans/2026-06-14-meta-andromeda-ads-playbook-research.md` (the playbook brain) and `docs/plans/2026-06-14-mass-ad-creative-generator-research.md` (the executor). **This candidate is the *discovery front-end* that feeds both.**
**Method:** WebSearch + WebFetch (exa/tavily/firecrawl keys dead). Pages fetched 2026-06-14. Verified what the public commercial Ad Library and the connected `ads_library_search` MCP actually expose vs. what Elijah's idea assumes, then mapped to the live hub.

---

## Verdict: ADD-LATER — build a thin **`ad-spy` skill** over the already-connected `ads_library_search` MCP. Phase 0 (a manual-driven "reverse-engineer this advertiser" skill) is small, dependency-free, and worth doing now; the automated radar waits on ad spend turning on.

**Confidence: high** on the research, the data limits, and the shape of the deliverable. **Medium** on timing — same gate as both siblings: **the `AdSpend/` vault folder is empty and Elijah is primarily an *organic* creator.** A competitor-ad spy tool is a force-multiplier *on the paid motion*; building the full automated radar cold (before there's a campaign to inform) is premature. But the discovery skill itself is cheap and independently useful as a **creative-research tool** even before spend — so Phase 0 ships now.

**This is NOT a tool to install.** Zero `pip install`, no repo, no model, no scraper. The capability is **already live**: `mcp__meta-ads__ads_library_search` is connected and verified in the hub. The entire build is (1) a `SKILL.md` that wraps the right query patterns + a scoring heuristic, and (2) optional later automation into the intel radar. Pure docs + an already-connected MCP. **Zero Windows/OneDrive/dependency risk** (no torch/cv2/cloud/paid).

### The honest correction this candidate MUST carry (the data wall)

Elijah's premise — *"an ad I see in every app = a campaign that knows what it's doing, so identify it and copy the strategy"* — is **directionally smart but rests on one thing the Ad Library cannot give him.** The "omnipresence" he's noticing is **user-side frequency** (how many times *he personally* was shown that ad across Instagram/Facebook/Audience Network). **No Meta API — including the connected MCP — exposes that.** The public commercial Ad Library returns NO impressions, NO reach, NO spend, NO frequency for normal US commercial ads. Those transparency fields exist **only** for political/issue/housing/employment/credit ads, plus reach/targeting for EU-delivered ads under the DSA. So the literal feature ("detect the omnipresent ad → look up its spend/reach") **is not buildable from the API.**

**What IS buildable — and is actually the more useful version:** you reverse-engineer *winning advertisers and their creative playbooks* from the signals the Ad Library **does** expose, which the connected MCP returns: ad creative (image/video/copy/headline/CTA), the page, **start date + active status**, platform breadth (FB/IG/Messenger/Audience Network), landing-page URL, and **how many near-identical variations are live**. The proxy for "this campaign knows what it's doing" is **not** frequency-to-Elijah — it's:

- **Longevity** — an ad still live after 60+ days is almost certainly profitable; independent tracking finds **only ~11% of ads survive past 60 days** (advertisers kill losers fast). This is the single strongest public signal.
- **Variation survival** — many similar ads where some persist and others vanished reveals which creative angle won.
- **Library density** — 3–5 live ads = "found it, scaling"; 50+ = "still testing." Reading the count tells you their stage.
- **Cross-competitor convergence** — when independent brands in a niche all converge on the same hook/format, that format is category-validated.

So the skill's framing is a **correction of the idea, not a transcription**: *we can't measure how often an ad chased you across apps, but we can find the proven winners in your niches and decode their playbook — which gets Elijah to the same destination (copy what works) by a route the API actually supports.* The "saw it everywhere" instinct still works as **a human-sourced lead** — Elijah names the brand he keeps seeing, the skill looks it up and decodes it.

---

## What it actually is / does

A discovery + decode skill that turns either **(a) a brand Elijah keeps seeing** or **(b) a niche keyword** into a ranked, decoded read on the winning advertisers and creative patterns worth copying for Infinet / Artifacial / ClipWith / his content. Flow:

1. **Seed** — either a page name ("this brand is everywhere"), a `page_id`, or a niche keyword ("AI video editor", "uncensored AI", "faceless content").
2. **Pull** — `ads_library_search` (search_terms / page_ids / countries) returns the live ad set per page/keyword.
3. **Score "knows-what-they're-doing"** — rank by the proxy signals: **longevity** (days since start, still active), **variation survival** (how many near-clones live + which persisted), **library density** (stage: testing vs scaling), **platform breadth**. No spend/impression needed — these are all in the response.
4. **Decode** — Claude reads the top-scored ads and extracts the *playbook*: hook (first line), offer structure, visual format/treatment, CTA, landing-page pattern, and the cross-ad framework that repeats.
5. **Translate** — emit a "steal-this-for-Infinet/Artifacial/ClipWith" brief: which winning angle maps to which of his products, in his niches (Money/Finance, AI/Tech). **This brief is the input the `meta-andromeda-ads-playbook` skill turns into diversity targets, which the `mass-ad-creative-generator` then fulfills.**
6. **Persist** — write the decoded read as a vault note (knowledge/idea type, property contract enforced).

It is the **discovery front-end of the ads trio**: spy (this) → playbook (brief→targets) → generator (targets→creatives). It answers "what should we even make?" before the other two answer "how do we make it well / make a lot of it."

---

## Best 2026 approach + tooling (and licenses)

| Layer | Pick | Why / license / cost |
|---|---|---|
| **Ad data source** | **`mcp__meta-ads__ads_library_search`** (already connected, verified) | Official Meta Ad Library via the connected MCP. Read-only, no spend, no scraper. Returns creative/page/start-date/active-status/snapshot-url/variations. Note: the tool itself requires the caller to have ≥1 active ad account (the hub has acct `661339332628311`), so it works today. Free. |
| **Scoring + decode brain** | **Claude via `--provider agent`** (the hub's auto-clip idiom, `auto-clip/highlight.py`) | No API key, no model download. Claude ranks by the longevity/variation heuristic and extracts the creative playbook. The hub's proven "thin harness, Claude is the brain" pattern. |
| **Persistence** | vault note (`70-Knowledge/Concepts/` for a niche-playbook writeup, or `20-Content/Ideas/` for a "steal-this" brief) + optionally `team/memory.md` learning | Property contract enforced; read `_templates/` first, do NOT invent properties. |
| **Optional automation** | wire a recurring keyword sweep into the **intel radar** (`intel/`, alongside `competitor-radar.py` / `trend-radar.py`) and `Daily Agent Refresh.bat` | Only once the paid motion is live and a watchlist exists. Reuses the existing radar pattern. |
| **NOT needed** | third-party ad-spy SaaS (Minea, AdSpy, BrandSearch, PowerAdSpy), Meta Content Library/CASD researcher access | These *do* surface more (e.g. EU reach, cross-brand search UX), but they're **paid** or **researcher-gated**, and the hub's rule is prefer local scripts + official MCPs over paid scrapers. The free `ads_library_search` covers the 80%. Flag as "only if a real budget + need appears." |

**Net new dependencies: ZERO.** No `pip`, no `npm`, no model. The only build artifact is a `SKILL.md` (and later a small intel-radar Python script reusing the existing radar scaffolding).

---

## Windows + OneDrive feasibility / dependency weight

**GREEN — the cleanest profile of any roadmap item.** Nothing imports, nothing renders, nothing downloads.

- **No torch / no cv2 / no local model / no heavy import** — all data comes from the connected MCP server-side. No OneDrive-hang risk whatsoever.
- **The only local artifact** is a markdown `SKILL.md`; the optional Phase-2 radar is a thin stdlib Python script (HTTP-via-MCP, JSON out) cloning the existing `intel/*.py` shape.
- **Secrets:** none new — the `meta-ads` MCP is already authed (OAuth-managed). No env-var work, no file-secret risk.
- **Outputs** are small markdown/JSON (decoded reads, watchlists) — git-friendly, no large media, no `out/` scratch needed.

---

## Integration sketch — how it composes with the hub

This is the **missing front-end of the already-researched ads trio**, and it slots in with zero new infrastructure:

```
  HUMAN LEAD: "I keep seeing <brand> everywhere"   OR   NICHE KEYWORD: "AI video editor"
        │
        ▼
[ ad-spy skill ]  (SKILL.md + --provider agent brain)
  1. PULL    mcp__meta-ads__ads_library_search(search_terms|page_ids, countries=["US"], ad_active_status="ACTIVE")
  2. SCORE   rank by proxy signals already in the response:
               longevity(start_date→now, still active) · variation_survival(#near-clones live)
               · library_density(stage: 3-5 scaling vs 50+ testing) · platform_breadth
             (NO impressions/reach/spend exist for US commercial ads — do NOT promise them)
  3. DECODE  Claude reads top ads → {hook, offer, visual_format, cta, lp_pattern, repeating_framework}
  4. TRANSLATE → "steal-this" brief mapped to Infinet / Artifacial / ClipWith × his niches
        │
        ├──▶  meta-andromeda-ads-playbook skill   (brief → diversity/format/volume targets)
        │            │
        │            ▼
        └──────▶  mass-ad-creative-generator skill (targets → N distinct creatives → out/)
                     │
                     ▼
              STOP at out/ + vault brief.  NEVER ads_create_* / publish_*.  Elijah reviews → manually launches.
```

**Which existing pieces it reuses (nothing new that already exists):**
- **Data:** `mcp__meta-ads__ads_library_search` — already connected, verified, read-only.
- **Brain:** the `--provider agent` idiom from `auto-clip/highlight.py` (no key/model) for scoring + decode.
- **Intel home (Phase 2):** the existing `intel/` radar pattern (`competitor-radar.py`, `trend-radar.py`, `CONTENT-INTEL-PROTOCOL.md`) and `Daily Agent Refresh.bat` for an optional recurring niche sweep. Note `intel/` already does the *organic* side via IG `business_discovery`; this adds the *paid-ad* side via the Ad Library — a natural sibling, surfaced through the existing `niche-intel` skill (which the roadmap notes already "runs the competitor radar + trend radar + Meta ad-library scan").
- **Analytics grounding:** `team/stats.md` / `team/profile.md` so the "which winning angle maps to which product" translation is grounded in his actual niches (Money/Finance, AI/Tech), not generic.
- **Persistence:** vault notes per the property contract; dated learning to `team/memory.md`.

**Data shapes:** one `ads_library_search` response per seed (array of ad objects: page, creative, start_date, active_status, snapshot_url, variations); one scored+decoded "advertiser read" record per page; one "steal-this" brief per product mapping. All JSON/markdown — no binary, no DB.

**Composition note — it's the cheapest add of the three precisely because the MCP is live and the brain idiom is proven.** It also makes the trio coherent: without it, the playbook and generator start from a blank concept; with it, they start from a *decoded proven winner in his niche.*

---

## Phased build sketch

**Phase 0 — the manual-driven `ad-spy` skill (~½ day, do-able now, zero spend, zero new deps).**
Write a `SKILL.md` (`.claude/skills/ad-spy/`) that triggers on "this brand is everywhere", "reverse-engineer this ad/advertiser", "spy on competitor ads", "what ads is <brand> running", "decode the winning ads in <niche>". It: (1) calls `ads_library_search` with the seed; (2) applies the longevity/variation/density scoring heuristic; (3) has Claude decode the top ads into a playbook; (4) emits a "steal-this-for-Infinet/Artifacial/ClipWith" brief; (5) **explicitly states the data limit in its output** ("ranked by longevity/variation, NOT by spend/impressions — those aren't public for US commercial ads"). **Deliverable:** a skill Elijah can fire today against any brand he keeps seeing. This is the 80/20 — it delivers the real, buildable version of his idea and is independently useful as creative research before any ad spend. Mirrors how auto-clip shipped its brain skill first.

**Phase 1 — niche-keyword sweep + vault persistence (~½ day, gated on the paid motion being imminent).**
Extend the skill to run keyword sweeps across his niches (not just a single named brand), de-dup advertisers, rank cross-niche, and persist the top reads as vault notes (knowledge/idea type, contract-compliant) + a dated `team/memory.md` learning. Output a small "winning-ad watchlist" of advertiser page_ids worth tracking.

**Phase 2 — automate into the intel radar (only once spend is live + a watchlist exists).**
Add a thin `intel/ad-radar.py` (stdlib, clones `competitor-radar.py`) that re-pulls the watchlist page_ids on a schedule via the MCP, flags **new** long-running ads (longevity threshold crossed) and **newly killed** ones (signal a loser), and writes a digest. Wire into `Daily Agent Refresh.bat` and surface via the existing `niche-intel` skill. Skip entirely until there's a paid motion to inform.

**Phase 3 — close the loop (only if ads actually run).**
Feed the decoded winning-angle briefs straight into the `meta-andromeda-ads-playbook` → `mass-ad-creative-generator` pair, and after Elijah launches, ingest performance into `50-Business/AdSpend/` (read-only insights) so the next sweep learns which *decoded angle* actually won for him. This is where the trio becomes a real operating loop.

---

## Risks / compliance / ToS

- **The data-wall risk (the big one — design constraint, not a footnote):** the literal "detect the omnipresent ad and read its spend/reach" feature is **not buildable** — no impressions/reach/spend for US commercial ads in any API; "omnipresence" is user-side frequency that no endpoint exposes. The skill must be honest about this in its own output and deliver the *proxy-signal* version (longevity/variation/density). If it silently implied it was measuring reach, it would mislead Elijah into trusting a number that doesn't exist. **Mitigation: bake the data-limit disclaimer into the SKILL.md output, not just the docs.**
- **Standing Rule 2 (write-gate):** the `meta-ads` MCP has **write** access. This skill uses **only** the read-only `ads_library_search`; it must never touch `ads_create_*` / `ads_update_*` / budget. It stops at a decoded brief / vault note. Bake the stop-gate into the SKILL.md as a rule.
- **Tool precondition:** `ads_library_search` requires the caller to have ≥1 active ad account; the hub has `661339332628311`, so it works today — but if that account is ever closed, the tool errors. Note it; not a blocker now.
- **No ban/ToS/scraper risk:** this is the *clean* way to do ad intel — official Meta Ad Library via the connected MCP, read-only, no scraping, no burner accounts. (Contrast the source-note's broader "reverse engineer top-tier strategies" instinct, which in other items flirted with burner-account scraping — this candidate explicitly avoids that by using the official surface, same posture as `intel/`'s `business_discovery`.)
- **Geography limit:** richer reach/targeting transparency exists for **EU-delivered** ads (DSA: `eu_total_reach`, `delivery_by_region`, beneficiary/payer) and for political/issue ads — so for EU-targeting advertisers there's *more* signal. For Elijah's US-centric niches, expect the leaner US field set; the proxy-signal method is the right default. Don't over-promise EU-grade data for US ads.
- **"Copying" risk (creative, not legal-serious):** "replicate the strategy" should mean **decode the framework** (hook structure, offer, format), not clone a competitor's literal creative/assets (trademark/copyright). The translate step must produce *his own* angle for *his own* products, not a pixel copy. Cheap to enforce in the prompt; worth stating.
- **Opportunity cost / timing:** building the automated radar (Phase 2) cold — before any ad spend — is low-ROI. That's exactly why the verdict is ADD-LATER with only the (independently-useful) Phase-0 skill now. As a *creative-research* tool it has standalone value today even for his organic content (decoding what hooks/formats win in Money/Finance + AI/Tech), which is the strongest reason to build Phase 0 now rather than wait.

---

## Rough effort

- **Phase 0** (manual `ad-spy` skill, no automation): **~½ day.** No new deps. Independently useful today (creative research even pre-spend).
- **Phase 1** (niche keyword sweep + vault persistence): **~½ day.**
- **Phase 2** (automated `intel/ad-radar.py` + `Daily Agent Refresh.bat` wiring): **~½–1 day.** Stdlib only; clones existing radar. Gated on paid motion.
- **Phase 3** (loop into the playbook/generator + AdSpend ingest): couples with the siblings' Phase-3; don't cost separately.
- **Usable v1 (Phase 0): ~½ day**, dominated by writing the SKILL.md + the scoring heuristic prompt, not engineering. The data source and brain idiom already exist.

**Bottom line:** the cheapest and most-composable of the ads trio — **zero new dependencies**, reuses a **live connected MCP** + the proven `--provider agent` brain, and it's the natural *discovery front-end* that feeds the already-researched playbook + generator. But (1) the literal "omnipresence/spend" framing is **not API-buildable** — ship the honest proxy-signal version instead, and (2) its full value is **conditional on the paid motion turning on**, and `AdSpend/` is still empty. So: **ADD-LATER**, build the standalone **`ad-spy` skill (Phase 0) now** — it's a genuinely useful creative-research tool even for his organic content today — and gate the automated radar on the same trigger as its two siblings. Ship the three as one coherent pipeline (spy → playbook → generator).

---

## Sources

- DeepSolv — *How to Use the Meta Ad Library to Find and Analyze Competitor Ads in 2026* (commercial fields available; no CTR/ROAS/spend; longevity + variation framework): https://deepsolv.ai/blog/how-to-use-the-meta-ad-library-to-find-and-analyze-competitor-ads-in-2026
- Shopify — *How to Use the Meta Ad Library in 2026: 9 Ways*: https://www.shopify.com/ae/blog/ad-library-facebook
- AdManage.ai — *Facebook Ads Library API: Pull Any Competitor's Ads* (API scoped to political/issue; commercial limits): https://admanage.ai/blog/facebook-ads-library-api
- Admapix — *Meta Ads Library API for Developers (Graph API v20.0, impressions/spend as ranges, political-only)*: https://www.admapix.com/blog/ad-intelligence/meta-ads-library-api-developers
- Primores — *Meta Ad Library API: Programmatic Competitor Research Guide*: https://primores.org/blog/meta-ad-library-api/
- Minea — *Facebook Ads Library (2026): Find Winning Ads & Competitor Insights* (longevity = strongest signal; ~11% survive 60 days): https://www.minea.com/competitor-analysis/competitor-spy-tools/facebook-ads-library
- Brandsearch — *What Winning Meta Ads Have in Common in 2026 (patterns from 500+ creatives)*: https://brandsearch.co/blog/winning-meta-ad-patterns-2026
- Simplified — *Meta Ad Library: How to Use It to Spy on Competitors in 2026* (3–5 ads = scaling vs 50+ = testing): https://simplified.com/blog/ai-social-media/meta-ad-library
- Kevel — *Meta's new beneficiary and payer requirements* (EU DSA disclosure fields): https://www.kevel.com/blog/metas-new-beneficiary-and-payer-requirements-an-overview
- Social Media Today — *Meta Implements New Updates for EU Advertisers (DSA)*: https://www.socialmediatoday.com/news/meta-implements-new-updates-eu-advertisers-evolving-requirements/653046/
- Connected tool: `mcp__meta-ads__ads_library_search` (Meta Ad Library via the hub's meta-ads MCP; read-only; requires ≥1 active ad account)
- Sibling research: `docs/plans/2026-06-14-meta-andromeda-ads-playbook-research.md`, `docs/plans/2026-06-14-mass-ad-creative-generator-research.md`
- Hub context: vault `Brainstorming/In the moment ideas.md` (heading "reverse engineering top tier marketing ad strategies"), `docs/plans/2026-06-14-overnight-roadmap.md` (line 103), `intel/` radar + `CONTENT-INTEL-PROTOCOL.md`, `.claude/skills/niche-intel/SKILL.md`, `auto-clip/highlight.py` (`--provider agent`), vault `CLAUDE.md` (meta-ads write-gate), `HANDOFF.md` (ad acct `661339332628311`)
