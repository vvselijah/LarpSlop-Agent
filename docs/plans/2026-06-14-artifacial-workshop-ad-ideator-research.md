---
type: research
domain: content-ops
status: open
date_captured: 2026-06-14
candidate_id: artifacial-workshop-ad-ideator
verdict: add-now
build_effort: S (Phase 0 ~30 min; usable v1 P0+P1 ~½ day)
tags: [ad-ideation, artifacial, analytics-grounded, agent-as-brain, vault-idea-note]
---

# Research — artifacial-workshop-ad-ideator

**Candidate:** Per-tool viral ad-concept generator for the artifacial.io workshop, grounded in Elijah's own niche analytics.
**Title:** Artifacial workshop ad-ideator — per-tool viral ad concepts grounded in his analytics
**Source:** vault `Brainstorming/In the moment ideas.md` → "artifacial ad idea creation for workshop" (his exact ask: *"Use Claude code to Check out all the different new tools that Tanner added into the workshop of artifacial.io And think of unique and viral video ideas that we could create for each tool that would advertise the software in a natural and unique manner, while referencing all of our past analytics and statistics in different content based in that niche to help create the idea and pacing"*). Roadmap STILL-TO-RESEARCH → Content-ops (line 109).
**Method:** WebSearch + WebFetch (exa/tavily/firecrawl keys dead). Fetched artifacial.io + /pricing (live tool surface), surveyed the 2026 AI-ad-ideation/creative-brief landscape, and grounded the integration against the live hub (`auto-clip/highlight.py` `--provider agent` pattern, `carousel-builder`/`niche-intel` skills, `team/stats.md`, and tonight's `metrics2026` + `watchtime-longform-ideator` outputs). Pages fetched 2026-06-14.

---

## Headline verdict: ADD-NOW (Phase 0 ~30 min; usable v1 ~½ day) — build the **`artifacial-ad-ideator` skill** (agent-as-brain → vault idea-notes), NOT a new engine

This is one of the cleanest ADD-NOW candidates in the roadmap, for three reasons:

1. **Bounded, enumerable input.** The artifacial.io "workshop" is a *finite, named* tool list — verified live: **Character Swap, Face Swap, Lip Sync, Upscale, End-Frame Control, Motion Templates, Prompt Enhancer (+ "more each week")**. "Generate an ad idea per tool" is therefore a small fan-out over a known set, not an open-ended problem. Tanner adds tools weekly, so a re-runnable per-tool ideator has standing value.
2. **The only hard part — analytics-grounded ideation — is exactly what the hub is uniquely set up to do, and what NO off-the-shelf tool does.** The 2026 market (Pollo, InVideo, Synthesia, Higgsfield, even the GitHub `claude-ads` skill) does *generation* and *variation testing*; the analytics-driven brief generators that exist all read a **paid Meta Ads account's** performance. **None ingests a creator's own organic retention/watch-time analytics by niche as the ideation input.** That intersection — *his* watch-time-by-niche data × a specific product feature → a paced ad concept — is the differentiator, and it's the hub's home turf.
3. **Zero new dependencies, OneDrive-safe, stops at vault idea-notes.** It's a SKILL.md + the `--provider agent` brain (no key, no model, no install), reading files already on disk and writing template-conformant `idea` notes. Same exact shape as the already-live `carousel-builder` and `niche-intel` skills. Nothing to install, nothing heavy, no publish path.

**One honest scoping correction (the thing that makes the verdict ADD-NOW not ADD-LATER):** the candidate description says it *"composes with mass-ad-creative-generator (this writes the brief, that fulfills it)."* True — but `mass-ad-creative-generator` is **ADD-LATER, gated on ad spend turning on** (its `AdSpend/` folder is empty; Elijah is primarily organic). **This ideator does NOT inherit that gate.** It stops at an *idea note* — a creative concept + pacing Elijah (or the existing Higgsfield/edit-video suite) can act on by hand, today, with zero ad spend. So decouple them: **build the ideator now as a standalone brainstorm tool**; let it *optionally* emit a brief into the mass-generator later, when that lane comes online. Coupling its verdict to the spend-gated executor would wrongly delay an independently-useful, dependency-free skill.

---

## What it actually is / does

A **skill**, not an engine. On invocation it:

1. **Reads the workshop tool list** — primary path: a small `intel/artifacial-tools.json` Elijah/Claude maintains (one row per tool: `name`, `what_it_does`, `hero_use_case`). Optional refresh path: WebFetch `https://artifacial.io/` and diff the "Inside the studio" tool names against the JSON, flagging any new tool Tanner shipped (the "tools added weekly" reality — verified that section is publicly readable). Keep the JSON canonical so a fetch failure never blocks ideation.
2. **Pulls his analytics priors** — reads `team/stats.md` (the auto-fed "Category mix" blocks) and, once tonight's builds land, the **watch-time-by-category** block from `watchtime-longform-ideator` and the **2026 priority rates** from `metrics2026.py` (skip-rate / share-rate / save-rate). These answer *which niche framing holds attention* and *what pacing the algorithm rewards* — the "reference our past analytics to help create the idea and pacing" half of his ask.
3. **Maps each tool → its best-fit niche → a concrete, on-brand ad concept.** Claude (`--provider agent`) writes, per tool: a scroll-stopping **hook line** (in Elijah's voice), the **format** (talking-head / AI-generated demo / screen-record), the **angle** (why this tool, framed for the audience that already rewards that niche), a **beat-by-beat pacing outline** grounded in his watch-time data (e.g. "AI/Tech holds 17.5s avg → open on the payoff, 3-beat demo, hard CTA"), and the **source signal** it rode (which niche stat / competitor reel). "Natural and unique" = each concept is a genuinely different creative angle, not a feature-list readout.
4. **Saves keepers as vault `idea` notes** under `20-Content/Ideas/` (one note per tool, or one rollup note with a section per tool), copying the `_templates/idea.md` property block exactly. **Stops there.** Never generates media, never publishes.

It is the **ideator/brief-writer** that sits *upstream* of the generation suite — the natural complement to `mass-ad-creative-generator` (executor) and a sibling of `niche-intel` (which already does "intel → on-brand idea" but for organic content, not per-product-feature ads).

---

## Best 2026 approach + tooling (and licenses)

**The right answer is "no new tool — Claude IS the brain," and that is the finding.** The landscape survey is decisive:

| Layer | Pick | Why / license / cost |
|---|---|---|
| **Ideation brain** | **Claude via `--provider agent`** (the hub's own `auto-clip/highlight.py` idiom) | No API key, no Ollama, no model download. Claude is the concept-writer. This is the hub's proven "thin skill, Claude is the brain" pattern (auto-clip, carousel-builder, niche-intel all use it). Our own code/prompt — no license issue. |
| **Workshop tool surface** | **`intel/artifacial-tools.json`** (canonical) + optional **WebFetch** refresh of `artifacial.io` | Verified the "Inside the studio" tool list is publicly readable via WebFetch (no auth). Keep a local JSON so ideation never depends on a live fetch. Stdlib only. |
| **Analytics priors** | **`team/stats.md`** + **`watchtime-longform-ideator`** block + **`metrics2026.py`** rates (tonight's builds) | Already on disk / being built tonight. Zero new fetch. This is the *grounding* that makes the candidate non-generic. |
| **Output store** | **vault `idea` notes** (`_templates/idea.md`) | Same target as carousel-builder/niche-intel. Template-conformant; no new property invented. |
| **Optional downstream** | **`mass-ad-creative-generator`** (ADD-LATER) brief hand-off | The ideator can emit a `creative-slate`-shaped brief into the executor *when that lane is live* — but does not depend on it. |

**Off-the-shelf alternatives surveyed and rejected (all worse fit):**
- **AI ad-video generators** (Pollo, InVideo, Synthesia, Higgsfield Marketing Studio): these *generate the asset*, they don't *ideate from your analytics*. The hub already has Higgsfield for the generation step; the gap is the analytics-grounded *idea*, which they don't do.
- **Claude-Code creative-brief generators** (get-ryze, Stormy AI, `AgriciDaniel/claude-ads` on GitHub — comprehensive paid-ads audit skill, MIT-ish OSS): genuinely the closest prior art, and they confirm the *pattern* (Claude reads performance data → writes briefs → scores). **But every one reads a paid Meta Ads account.** This candidate's twist — *organic* watch-time-by-niche × a *specific product feature* — is not what they do. Worth a glance at `claude-ads` for prompt-structure ideas; not worth adopting (it's built around ad-account audit, not organic-creator analytics).

**Net new dependencies: zero.** No torch, no cv2, no cloud SaaS, no paid scraper, no API key, no model download. Optional `curl.exe`/WebFetch for the tool-list refresh is already available.

---

## Windows + OneDrive feasibility / dependency weight

**GREEN across the board — the lightest possible profile.**
- **No heavy imports.** The OneDrive-hang risk (torch/cv2/big-model loads) is entirely absent — this skill imports nothing; the "compute" is Claude reasoning over text already on disk.
- **Reads local files** (`team/stats.md`, the watch-time block, `intel/artifacial-tools.json`) — Phase 0 needs no network call at all. The optional `artifacial.io` refresh is one short WebFetch, no auth.
- **No secrets touched.** It never sees the IG token; it consumes data `refresh.py` already wrote.
- **Outputs are small markdown** vault notes — no large media in `out/`, no binary state, nothing that stresses OneDrive sync.

Dependency-weight flags requested by the brief: **torch — none. cv2 — none. heavy — none. cloud — none. paid — none.**

---

## Integration sketch — how it composes with the hub

```
                team/stats.md  ─┐
   watchtime-longform-ideator  ─┤  (analytics priors: which niche holds attention, what pacing)
        metrics2026.py rates   ─┘
                                 │
   intel/artifacial-tools.json ──┤  (the enumerable workshop tool surface;
     (optional artifacial.io ────┘   optional WebFetch refresh diffs for NEW tools)
        WebFetch refresh)
                                 ▼
                ┌──────────────────────────────────┐
                │  artifacial-ad-ideator SKILL      │
                │  brain: Claude via --provider     │
                │         agent (auto-clip idiom)   │
                │  per tool → {hook, format, angle, │
                │   pacing(grounded in watch-time), │
                │   source_signal}                  │
                └──────────────────────────────────┘
                                 │
                                 ▼
   vault 20-Content/Ideas/  ◀── one `idea` note per tool (or a rollup w/ a section per tool)
   (_templates/idea.md exact)     STOP. Never generates media. Never publishes.
                                 │
                                 ▼ (OPTIONAL, only when its lane is live)
   mass-ad-creative-generator ◀── emit the concept as a creative-slate brief
   (ADD-LATER, ad-spend-gated)     ── playbook writes brief → ideator feeds concept → executor renders
```

**Which existing pieces it reuses (nothing new built that already exists):**
- **Brain:** `auto-clip/highlight.py`'s `--provider agent` two-step (no key/model) — the same idiom carousel-builder/niche-intel rely on.
- **Voice / niche grounding:** `team/profile.md` (voice rules, ranked niches), `team/stats.md` (Category-mix blocks).
- **Pacing grounding (the differentiator):** the **watch-time-by-category** block from `watchtime-longform-ideator` (Money/Finance prints views but holds worst; AI/Tech + Child Safety hold longest → drives both *which niche to frame a tool in* and *how to pace the cut*). This is a clean, real dependency on a tonight ADD-NOW build.
- **2026 algorithm rates:** `metrics2026.py` (skip-rate as the pacing North-Star — front-load the payoff).
- **Output contract:** the vault `idea` template + the `niche-intel`/`carousel-builder` "write keepers to the vault, log a learning" flow, copied almost verbatim.

**Data shapes:** input = `artifacial-tools.json` rows + `stats.md` text + watch-time block. Output = one `idea` note per tool (YAML from `_templates/idea.md`; the concept/pacing live in the note BODY — **do not invent an `ad_concept` or `pacing` property**). Optional downstream = a `creative-slate`-shaped brief object handed to the (later) mass-generator.

---

## Phased build sketch

**Phase 0 — smallest safe thing (~30 min, ship now, zero deps, zero spend).**
Create `intel/artifacial-tools.json` (the 7 verified tools + their one-line use cases) and a thin `SKILL.md` (`artifacial-ad-ideator`) that: reads that JSON + `team/stats.md`, and for ONE tool (start with Face Swap — the flagship) writes ONE on-brand ad concept (hook + format + angle + a pacing outline grounded in the niche it's framed for) as a vault `idea` note. **DoD:** running the skill produces one template-conformant idea note Elijah can eyeball. Proves the only hard part (analytics-grounded, on-voice ideation over a real tool) end-to-end. Mirrors how auto-clip shipped its highlight brain first.

**Phase 1 — full fan-out + watch-time grounding (~2–3 hr, after tonight's watch-time block lands).**
Fan out over ALL tools in the JSON; wire in the **watch-time-by-category** block so pacing/niche-framing is data-driven (not generic ad lore), and the `metrics2026` skip-rate North-Star ("front-load the payoff"). Emit either one note per tool or a single rollup note with a section per tool (Elijah's preference). Add the optional `artifacial.io` WebFetch refresh that flags NEW tools since the JSON. **DoD:** one invocation yields a complete, distinct, analytics-grounded ad concept for every current workshop tool, each citing the niche stat it rode.

**Phase 2 — multi-product + executor hand-off (optional, demand-gated).**
Generalize the tool-list source so the same skill ideates per-feature ads for **Infinet** and **ClipWith** too (same shape, different `tools.json`). Add an optional `--brief` mode that emits the concept as a `creative-slate`-shaped object for `mass-ad-creative-generator` — **only meaningful once that lane is live (ad spend on).** Keep the AI-disclosure reminder (see Risks) attached to any brief destined for paid launch.

**Phase 3 — close the loop (nice-to-have, only with ad spend).**
Once concepts have actually run, feed which *angles* won back into the ideator as priors, and append a dated learning to `team/memory.md` each run. Skip until there's launched-ad performance to learn from.

---

## Risks / compliance / ToS

- **Standing Rule 1 (the hard wall):** the skill **stops at vault idea-notes** — it never generates media, never calls `publish_*` / `ads_create_*` / `send_dm`. Drafting concepts is fine unattended; any downstream generation (Higgsfield) or launch is a separate, Elijah-confirmed step. Bake the stop-gate into the SKILL.md as a rule, same posture as carousel-builder/niche-intel.
- **Don't let the verdict get coupled to the spend-gated executor.** The candidate text pairs it with `mass-ad-creative-generator`; that executor is ADD-LATER (empty `AdSpend/`). The ideator is independently useful *now* (idea note → manual creation via the existing Higgsfield/edit-video suite). Ship it decoupled; make the executor hand-off optional/Phase-2.
- **Meta AI-disclosure rule (inherited, real, citable — effective Mar 2026):** any concept that becomes a *paid* ad where AI generated/modified the visual subject (i.e. Higgsfield/Artifacial output) must carry an "AI-generated" label at launch (~14% of ad rejections are undisclosed AI). The ideator only writes *ideas*, so this is not a build blocker — but a concept destined for a paid ad should carry a one-line "disclose as AI on launch" reminder in the note, so it propagates to the (later) generator/launch step. Organic posting of his own AI content is governed by IG's normal labeling, not the ads rule.
- **artifacial.io fetch is read-only and low-risk** — it's Tanner's own product page; the optional refresh just reads the public "Inside the studio" list. Keep the JSON canonical so a fetch failure/redesign never blocks ideation (the page returned cleanly today but product sites churn).
- **Don't over-trust thin niche data for pacing.** Watch-time-by-category requires n≥5 before crowning a category (the watchtime-ideator research flags this). For a tool whose best-fit niche is small-n, frame the concept on a stronger niche or label the pacing as a prior, not a rule.
- **"Natural and unique" is a quality bar, not a guarantee.** The failure mode is generic "here's a tool, here's a demo" concepts. Mitigation: force each concept to cite a *specific* niche stat or competitor signal and a distinct creative angle — the same anti-clone discipline `mass-ad-creative-generator` enforces at the slate layer, applied here at the idea layer.
- **No scraper/ban risk:** no automation against IG, no burner accounts, no paid scraper. Reads his own already-authorized analytics + a public product page.

---

## Rough effort

- **Phase 0** (tools.json + skill + one concept): ~30 min. Zero new deps. Independently useful today.
- **Phase 1** (full fan-out + watch-time grounding + new-tool diff): ~2–3 hr. Depends only on tonight's `watchtime-longform-ideator` block (itself ADD-NOW).
- **Phase 2** (multi-product + optional executor hand-off): ~½ day, demand-gated on ad spend.
- **Phase 3** (performance loop): couples with the mass-generator's Phase-3; don't cost separately.
- **Usable v1 (Phase 0+1): ~½ day**, dominated by the brain prompt + the vault-note wiring, not engineering.

**Bottom line:** genuinely useful, unusually cheap, and a clean fit for the hub's recurring **intel → idea** core ask. It's the *ideator* the roadmap keeps circling (niche-intel for organic, this for per-product ads), it's grounded in analytics no off-the-shelf tool touches, and it carries zero new dependencies and no publish path. The one trap to avoid is inheriting `mass-ad-creative-generator`'s ad-spend gate — this stops at an idea note and is buildable today. **ADD-NOW: ship the Phase-0 skill + `artifacial-tools.json` now; light up the watch-time grounding (Phase 1) right after tonight's `watchtime-longform-ideator` block lands; keep the paid-executor hand-off optional and later.**

---

## Sources

- Artifacial — homepage "Inside the studio" tool list (verified live: Character Swap, Face Swap, Lip Sync, Upscale, End-Frame Control, Motion Templates, Prompt Enhancer, "+more each week"): https://artifacial.io/
- Artifacial — pricing page (confirms "3 generations free · no card"; no public per-tool URL structure): https://artifacial.io/pricing
- Buffer — 14 AI Tools for Social Media Content Creation in 2026 (generation/variation tooling, no analytics-grounded ideation): https://buffer.com/resources/ai-social-media-content-creation/
- Synthesia — 18 Best AI Video Generators 2026 (generation, not ideation-from-analytics): https://www.synthesia.io/post/best-ai-video-generators
- Digen — AI Video Generator for Social Media Ads 2026 (the "10–20 variations of one concept, test, keep the winner" pattern): https://resource.digen.ai/ai-video-generator-social-media-ads-2026/
- get-ryze — Automated Ad Creative Brief Generator with Claude (closest prior art; reads a *paid* ad account, not organic analytics): https://www.get-ryze.ai/blog/automated-ad-creative-brief-claude
- Stormy AI — Claude Code to automate Meta Ads creative strategy (Claude-Code-+-MCP brief pattern, paid-ads framing): https://stormy.ai/blog/maximizing-creative-velocity-claude-code-meta-ads
- GitHub — AgriciDaniel/claude-ads (Claude Code paid-ads audit + AI creative-generation skill; adjacent prior art, ad-account-centric): https://github.com/AgriciDaniel/claude-ads
- Sibling research: `docs/plans/2026-06-14-mass-ad-creative-generator-research.md` (the spend-gated EXECUTOR this ideator optionally feeds), `docs/plans/2026-06-14-watchtime-longform-ideator-research.md` (the watch-time grounding it consumes), `docs/plans/2026-06-14-ig-2026-algorithm-metric-engine-research.md` (the skip-rate pacing North-Star)
- Hub context: `docs/plans/2026-06-14-overnight-roadmap.md` (line 109), vault `Brainstorming/In the moment ideas.md` ("artifacial ad idea creation for workshop"), `auto-clip/highlight.py` (`--provider agent` brain pattern), `.claude/skills/niche-intel/SKILL.md` + `.claude/skills/carousel-builder/SKILL.md` (the intel→idea→vault-note precedent), `team/profile.md` + `team/stats.md` (voice + niche analytics), vault `CLAUDE.md` + `_templates/idea.md` (the property contract)
