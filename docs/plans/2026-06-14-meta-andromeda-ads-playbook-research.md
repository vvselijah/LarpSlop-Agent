# Meta Andromeda Ads Playbook — research + build/feasibility plan

**Date:** 2026-06-14
**Candidate id:** `meta-andromeda-ads-playbook`
**Source flag:** `obsidian/Elijah's vault/Research/YouTube summary about the best six things to know for the new Meta ads Andromeda.md` (a text summary of a Sabri Suby YouTube video; note opens "We need to do more research on all of these principles and expand on these practices"). Roadmap: STILL-TO-RESEARCH → Knowledge/strategy.
**Method:** WebSearch + WebFetch (exa/tavily/firecrawl keys dead). Pages fetched 2026-06-14. Validated Suby's claims against independent 2026 Andromeda data, then mapped to the hub's already-live `meta-ads` MCP.

---

## Verdict: ADD-LATER — build it as a **skill + grounded vault playbook note**, not a tool. Phase 0 is small and worth doing now; the full build waits until Elijah is actually spending on ads.

**Confidence: high** on the research and on the shape of the deliverable. **Medium** on the timing, because of one decisive fact: **the `AdSpend/` vault folder is empty and the connected ad account (`661339332628311`, the "Di$trobaby"/baby-reel side) has no ingested campaign history.** A playbook is a force-multiplier *on top of running campaigns*. Elijah's primary identity is an **organic IG creator** — paid ads are a secondary/emerging motion (Infinet/Artifacial/ClipWith product ads, per the `mass-ad-creative-generator` roadmap item). So this is high-value **when** the ad motion turns on, low-value as a standalone thing to build cold today.

**This is a knowledge-and-strategy item, not a tool install.** There is nothing to `pip install`, no repo to clone, no model to download. Zero Windows/OneDrive/dependency risk (no torch/cv2/cloud/paid anything). The entire build is: (1) one corrected, source-grounded vault note, and (2) optionally a thin `meta-ads-playbook` skill that wires the playbook to the read-only `meta-ads` MCP tools the hub already has. That makes it cheap — but cheapness is the argument for doing the small version now and deferring the rest, not for over-building it.

### The honest correction the playbook MUST carry
Suby's #1 hack — **"statics beat video, pump volume"** — is **half-right and half-stale for 2026 Andromeda.** Independent data (834M in spend across 3,014 advertisers; ScaleDon/Confect/JetFuel analyses) says:
- **Volume helps** (20+ fresh ads/mo → ~65% higher ROAS; top advertisers run ~395 live ads vs ~296), **AND**
- **Andromeda clusters near-identical creatives into ONE entity** via computer vision — so "50 near-identical statics" performs like ~10. Volume only counts if each ad is *genuinely visually different*. This directly contradicts the naive "crank out static variations" reading of the source note.
- For **e-commerce**, **Catalog Ads + video** now beat plain statics (Catalog: +23% ROAS, +37% CPA, 3.6× revenue/ad). For an **info/lead/creator offer**, statics-first is still defensible — but the volume must be *diverse*, not cloned.

A playbook that just parrots "statics-first, pump volume" would actively mislead. The value of building this is **correcting** the source note, not transcribing it.

---

## What it actually is

The source is a creator-marketer's (Sabri Suby, King Kong) 8-point YouTube summary on winning Meta Ads under **Andromeda** — Meta's rebuilt **ad-retrieval** engine (launched Dec 2024, fully global by Oct 2025). The 8 hacks:

1. **Statics-first** (cheap, fast → feed volume to beat fatigue) — *see correction above.*
2. **"One keyword" identity trigger** — put an identity word ("dental leads", "lawyer leads") in headline/body so the algorithm self-targets the niche.
3. **Winning-format clone + "zombie campaign"** — AI-vary winners; if a high-conviction ad gets no spend in its campaign, relaunch it in a separate ad set ("zombie campaign") to give it a fresh shot. *(This is Suby jargon, not a Meta feature; the real mechanism is just re-launching into a clean ad set so the auction re-evaluates it. Legitimate but minor.)*
4. **Don't make ads look like ads** — model creative on what performs organically in-niche (even via a burner research account).
5. **Broad targeting** — stop interest-stacking; give the algorithm context via creative + long copy, target broad (e.g., by country).
6. **Landing-page congruence** — LP headline/sub-headline must match the ad; split-test headlines (+15–20% conversion).
7. **Retarget with a *different* offer** — don't re-show the same ad; use objection-handling / testimonial carousels.
8. **Track blended ROAS + net free cash flow**, not per-ad ROAS noise.

**How Andromeda actually works (the part the playbook should anchor on):** two stages. **Retrieval (Andromeda)** scans tens of millions of live ads → ~1,000 candidates, scoring by *creative content* (CV + semantic analysis) rather than advertiser targeting. **Ranking/auction (Lattice/GEM)** picks winners + prices. The strategic consequence is the through-line behind hacks #1/#4/#5: **the creative IS the targeting now.** Most of Suby's list is downstream of that one fact, and the playbook should be organized around it rather than as 8 disconnected tips.

**Validation status of each hack (2026):** Broad targeting = **strongly confirmed** (independent data: +49% ROAS vs lookalikes). Creative-as-targeting / native-feel = **strongly confirmed**. Volume = **confirmed with the diversity caveat**. Statics-first = **partially superseded** (depends on offer type; diversity + Catalog/video matter more). Identity-keyword, zombie-campaign, LP-congruence, retarget-with-different-offer, blended-ROAS = **plausible, evergreen direct-response craft, not Andromeda-specific** — keep them, label them as fundamentals.

---

## Integration sketch — how it composes with the hub

The whole point of "playbook" (vs. a note that rots) is that it **runs against the live `meta-ads` MCP** and against Elijah's own results. It composes cleanly because every input already exists, all **read-only** (no write = no standing-rule risk):

| Playbook step | Hub mechanism (already live) | Data shape |
|---|---|---|
| Ground "what's working in-niche" (hack #4) | `meta-ads` MCP `ads_library_search` (Meta Ad Library, live-verified in hub) | competitor live-ad creatives, formats, longevity |
| Audit own account health vs. the rules | `ads_insights_*`, `ads_get_opportunity_score`, `ads_get_ad_entities` on acct `661339332628311` | live ad count, creative diversity, spend distribution |
| Benchmark vs. vertical | `ads_insights_industry_benchmark`, `ads_insights_performance_trend`, `ads_insights_anomaly_signal` | CPA/ROAS/CTR vs. industry; fatigue/anomaly flags |
| Blended-ROAS framing (hack #8) | pull spend/results via insights; reconcile against offer revenue | blended math, not per-ad noise |
| Feed creative production | the **`mass-ad-creative-generator`** roadmap item + Higgsfield Marketing Studio + `caption-engine` | N *diverse* statics/videos per concept |
| Persist results + learnings | vault `50-Business/AdSpend/` (`ad-campaign` template), `team/memory.md` | machine-refreshable metrics + dated learnings |

**This is the tightest "composes-with-the-hub" story of any current roadmap item**, because the `meta-ads` MCP is already connected and the playbook is *literally instructions for how to use it well*. It also directly **enables** `mass-ad-creative-generator` (the playbook tells that generator the diversity/format/volume targets to hit — they should ship as a pair) and reuses the same "rank winners → explain why → produce a better one" core the roadmap flagged as the recurring true ask.

**Crucial guardrail to bake in:** every Andromeda "rule" cited (volume thresholds, +49% broad, +23% Catalog) comes from **e-commerce/DTC** studies. Elijah's offers are info/lead/creator-product. The skill must **NOT** hardcode those numbers as truth for his account — it should treat them as priors and **always defer to his own `ads_insights` data + the IG-organic algorithm reality** (his real edge is organic; ads are support). Label the e-comm stats as "DTC priors, verify on your account."

---

## Phased build sketch

**Phase 0 (smallest safe thing — ~30–60 min, do now):** Rewrite the source vault note into a **corrected, source-grounded playbook note** in `70-Knowledge/Concepts/` (per the vault property contract — read `_templates/` first, do not invent properties; this is a `concept`/knowledge note, body is human-readable). Structure it around the one true principle ("creative is the targeting") with the 8 hacks reorganized as: *Andromeda-confirmed* (broad, native-feel, diverse volume) / *evergreen DR craft* (identity keyword, LP congruence, retarget-different-offer, blended ROAS) / *minor tactic* (zombie relaunch) / *corrected* (statics-first → diverse-creative-first). Cite the sources below. **Net result even if nothing else ships:** the misleading raw note is replaced by an accurate one. This is the 80/20.

**Phase 1 (when ad spend turns on):** Author a thin **`meta-ads-playbook` skill** (`.claude/skills/`, SKILL.md only — no code) that, on "audit my ads" / "plan an ad campaign" / "are my ads Andromeda-ready", runs the read-only `meta-ads` insights tools above, scores his account against the playbook checklist (creative count, diversity, broad vs. narrow, LP congruence, blended-ROAS framing), and drafts recommendations. **Read/report only; STOP before any `ads_create_*`/`ads_update_*`/budget write — confirm per-action (standing rule #2).**

**Phase 2 (optional, paired with `mass-ad-creative-generator`):** Close the loop — the playbook emits a concrete creative brief (N diverse concepts × required formats 1:1/4:5/9:16) that the mass-creative generator fulfills via Higgsfield, then a refresh ingests results into `50-Business/AdSpend/` and appends a dated learning to `team/memory.md`. This is where it becomes a real operating loop rather than a doc.

**Phase 3 (only if proven):** Wire a periodic "ad health" check into `Daily Agent Refresh.bat` (fatigue/anomaly flags via `ads_insights_anomaly_signal`). Skip unless he's running enough ads for daily monitoring to matter.

---

## Risks / compliance / ToS

- **No technical/dependency/OneDrive risk** — pure docs + already-connected MCP. No heavy deps.
- **Standing-rule risk (the real one):** the `meta-ads` MCP has **write** access. The playbook's Phase 1+ MUST be hard-walled to read/report and require explicit per-action confirmation before any create/edit/pause/budget change (CLAUDE.md rule #2, vault CLAUDE.md). Bake this into the SKILL.md as a stop-gate, not a footnote.
- **Stale-advice / wrong-niche risk:** the biggest content risk is treating Suby's video and DTC e-comm stats as gospel. Mitigated by Phase 0's explicit corrections + the "verify on your own data" guardrail. Andromeda is also fast-moving (rebuilt within ~18 months) — date-stamp the note and treat numbers as priors.
- **No ban/ToS risk in the playbook itself.** One yellow flag *in the source advice*: hack #4's "burner account to monitor trending content" — passive viewing is fine, but **don't** automate scraping/engagement from a burner (platform-ToS gray area). The hub already does competitor intel the clean way (official `business_discovery` / Ad Library), so the playbook should point at those, not a burner.
- **Opportunity cost:** building the full skill cold (before ad spend exists) is low-ROI. That's exactly why the verdict is add-LATER with only Phase 0 now.

**Rough effort:** Phase 0 ≈ 1 hr (write one corrected note). Phase 1 ≈ 2–3 hrs (SKILL.md + checklist + read-only MCP wiring). Phase 2 ≈ couples with `mass-ad-creative-generator`, don't cost separately. Total standalone for a usable v1 (Phase 0+1): **half a day**, dominated by writing, not engineering.

---

## Sources

- Confect — *Meta Andromeda: the ultimate guide to Meta Ads in 2026*: https://confect.io/tactics/meta-andromeda-2026
- ScaleDon — *Meta Andromeda Creatives: the data behind the biggest ad strategy shift in 2026*: https://scaledon.com/meta-andromeda-creatives-the-data-behind-the-biggest-ad-strategy-shift-in-2026/
- JetFuel Agency — *Meta's 2026 Algorithm Update: what Andromeda changed*: https://jetfuel.agency/meta-algorithm-changes-2026-andromeda/
- SuperScale — *What is Meta Andromeda? A 2026 guide for marketers*: https://superscale.ai/learn/what-is-meta-andromeda/
- Segwise — *Meta Andromeda Update: 2026 Creative Strategy Playbook*: https://segwise.ai/blog/meta-andromeda-update-creative-strategy-2026
- Sabri Suby strategy summary (Klind Parangoni): https://klindparangoni.com/best-meta-ads-strategies-from-sabri-suby/
- Sabri Suby Meta ad portfolio (AdScan): https://adscan.ai/meta/Sabri%20Suby
- TheOptimizer — *Why your Meta ads stopped working in 2026*: https://theoptimizer.io/blog/why-your-meta-ads-stopped-working-in-2026-and-what-to-do-about-it
- Source vault note: `obsidian/Elijah's vault/Research/YouTube summary about the best six things to know for the new Meta ads Andromeda.md`
- Hub context: `HANDOFF.md` (ad acct `661339332628311`), `docs/plans/2026-06-14-overnight-roadmap.md` (lines 78, 90), vault `CLAUDE.md` (Meta Ads MCP write-gate)
