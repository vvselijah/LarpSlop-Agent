# Mass Ad-Creative Generator — research + build/feasibility plan

**Date:** 2026-06-14
**Candidate id:** `mass-ad-creative-generator`
**Title:** Mass-generate ad creatives (incl. high-performing statics) for Infinet / Artifacial / ClipWith
**Source flags:** `docs/plans/2026-06-14-overnight-roadmap.md` (STILL-TO-RESEARCH → Video, line 101); vault `Brainstorming/In the moment ideas.md` ("generate mass creatives for ads on infinet and artifacial and clipwith" — that single line is Elijah's entire stated ask).
**Pairs with:** `docs/plans/2026-06-14-meta-andromeda-ads-playbook-research.md` (its researched, corrected sibling — the playbook is the *brief-writer*, this is the *executor*).
**Method:** WebSearch + WebFetch (exa/tavily/firecrawl keys dead). Pages fetched 2026-06-14. Verified the Higgsfield Marketing Studio / CLI surface, an already-published Claude-Code-+-Higgsfield ad pipeline, Meta's 2026 AI-disclosure rule, and an OSS static-templating fallback. Grounded the integration against the live hub (Higgsfield MCP + ElevenLabs MCP + meta-ads MCP + the auto-clip `--provider agent` pattern in `auto-clip/highlight.py`).

---

## Verdict: ADD-LATER — build the **`mass-ad-creative` skill + thin diversity-aware "creative-slate" brain**, gated on the same trigger as its sibling: real ad spend turning on. Phase 0 (the slate brain) is small, no new deps, and worth doing now as a dry-run; the full generation loop waits.

**Confidence: high** on what to build and how it composes; **medium** on timing, for the same decisive reason the Andromeda-playbook research landed on: **the `AdSpend/` vault folder is empty and Elijah is primarily an organic creator.** A mass-creative *factory* is a force-multiplier on top of a running ad motion. Building the full render loop cold — before there's a campaign, a budget, or a winning concept to vary — is premature. But the *brain* (the part that turns one concept into N genuinely-different briefs) is cheap, dependency-free, and independently useful, so Phase 0 ships now.

**This is not a "new tool to install."** Every generation primitive already exists in the hub: Higgsfield Marketing Studio (URL→ad, 40+ avatars, hooks, UGC/CGI/cinematic, 9:16 / 1:1 / 16:9), Higgsfield image models (GPT Image 2 / Nano Banana Pro / Flux) for statics, ElevenLabs for VO/music, and the `virality_predictor` (`brain_activity`) for a pre-spend score — all wired via the `higgsfield-*` skills and the `mcp__e46b6dc5…` + `elevenlabs` MCPs. The missing piece is **orchestration**: a controlled, diversity-aware slate generator that produces *many genuinely distinct concepts* (not 50 near-clones), tracks them, scores them, and stops at `out/` for review. That is a thin Python harness + a SKILL.md, not a dependency.

### The one correction that makes this candidate worth scoping (inherited from the Andromeda research)
The candidate title says "incl. high-performing statics" — echoing Sabri Suby's "statics beat video, pump volume." That is **half-stale for 2026 Andromeda.** Independent data (834M in spend; ScaleDon/Confect/Segwise) is blunt: **Andromeda's retrieval stage clusters near-identical creatives into ONE entity via computer vision.** Ten variations of the same image with a recolored headline = "ten ads, one retrieval ticket." Volume only counts when each ad is **genuinely visually/conceptually different** — the 2026 rule of thumb is **8–12 conceptually distinct concepts per campaign** (different hooks, formats, emotional triggers, visual treatments), not 50 cloned statics. **This single fact is the entire reason a *controlled, diversity-aware* generator is the missing executor** rather than a dumb batch loop. A naive "crank out 50 statics" script would actively hurt under Andromeda. The generator's job is **forced diversity**, and that is exactly what makes it a non-trivial, valuable thing to build well.

---

## What it actually is / does

A pipeline that takes **one product (Infinet / Artifacial / ClipWith) + one core concept** and fans it out into **N genuinely-distinct ad creatives** — a mix of statics and short video — ready for Elijah to review and (manually) launch. Concretely:

1. **Slate brain (the real value):** Claude reads the product + the Andromeda-playbook diversity targets + Elijah's own niche analytics, and writes a *creative slate* — N rows, each a deliberately different concept (distinct hook × format × emotional angle × visual treatment), with a per-row generation brief. This is the anti-clone guard: diversity is enforced at the planning layer, before a single credit is spent.
2. **Generation:** each row is rendered via Higgsfield — statics through the image models (GPT Image 2 / Nano Banana Pro / Flux), video/UGC through Marketing Studio (URL→ad, avatars, hooks). VO/music via ElevenLabs where needed.
3. **Score gate:** video concepts pass through Higgsfield's `virality_predictor` (`brain_activity`) for a hook/retention/creative score; weak concepts are flagged before they ever reach a feed.
4. **Track + stop:** a tracking store (sheet or JSON) holds row → status → job_id → result URL → score, so re-runs don't duplicate. The pipeline **stops at `out/`** — never launches an ad (Standing Rule 2).

**Prior art (this exact pattern is already published):** MindStudio documented a Claude-Code-+-Higgsfield ad pipeline that does precisely this — Claude reads brand/research docs, writes a 50-row "creative slate" in a sheet (different value props/headlines/avatars/styles), calls the **Higgsfield CLI** in a loop, and writes back result URLs + job IDs, with a `.claude/skills/` markdown skill holding the hard rules (aspect ratio, style) and slash-command triggers. We don't need to invent the architecture — we adapt it to the hub's conventions (vault note instead of a Google Sheet; `--provider agent` brain instead of a cloud routine; stop-at-`out/`).

---

## Best 2026 approach + tooling (and licenses)

| Layer | Pick | Why / license / cost |
|---|---|---|
| **Video / UGC / URL→ad** | **Higgsfield Marketing Studio** (already installed) | Paste URL → finished ad; 40+ avatars (Soul 2.0), AI hook briefs, UGC + CGI + cinematic, 9:16/1:1/16:9. Best-in-class for this and already paid for (~1.9k credits per memory). Proprietary SaaS, credit-metered. |
| **Statics (AI)** | **Higgsfield image models** (GPT Image 2 / Nano Banana Pro / Flux, already installed) | Same account/credits; the documented pipeline uses exactly these for "product photos, Instagram ads." Proprietary. |
| **Statics (deterministic, free fallback)** | **Pillow** (`pip install pillow`, **PIL/MIT-style permissive license**, current 12.2.0) | For *templated* statics — same layout, swapped headline/colour/proof — where you want pixel-control and zero credits. Pure-Python, lightweight, **OneDrive-safe (no torch/cv2)**. Use for the boring "10 headline variants of one card" lane; use Higgsfield for the *distinct-concept* lane. |
| **Agent ↔ Higgsfield transport** | **Higgsfield CLI** `@higgsfield/cli` (`npm i -g`) **or** the already-wired Higgsfield MCP | CLI is the documented fast path for agent loops (no API key — browser login once, `hf login`/`hf status`/`hf generate`), "faster, cheaper, better for loops" than MCP. The hub already has the **MCP** path live, so **no new install is strictly required** — CLI is an optional speed upgrade if loops get token-heavy. Unofficial community CLI also exists (`clawdybotty/higgsfield-cli`, Python) but the official `@higgsfield/cli` is preferred. |
| **VO / music** | **ElevenLabs MCP** (already installed) | TTS/voice/SFX/music for video concepts. Proprietary, metered. |
| **Pre-spend score** | **Higgsfield `virality_predictor`** (already installed) | `brain_activity` returns hook/attention/retention/creative scores — the cheap gate before a concept reaches a budget. |
| **Brain / orchestration** | **Claude via `--provider agent`** (the hub's own auto-clip pattern, `auto-clip/highlight.py`) | No API key, no Ollama, no model download. Claude *is* the slate-writer. This is the hub's proven "thin Python harness, Claude is the brain" idiom. |

**Net new dependencies: effectively zero for Phase 0–1.** Optional later: `pip install pillow` (light, safe) for the deterministic-statics lane, and `npm i -g @higgsfield/cli` (optional speed) — neither is torch/cv2/cloud-heavy, neither touches the OneDrive-hang risk. **No paid scraper, no new SaaS subscription.** Everything heavy (Higgsfield/ElevenLabs renders) already runs server-side off Elijah's machine.

---

## Windows + OneDrive feasibility / dependency weight

**GREEN.** The candidate's whole appeal is that the compute lives in already-paid SaaS, so the local footprint is tiny:

- **No torch / no cv2 / no local model download.** All rendering is Higgsfield/ElevenLabs server-side via MCP (or CLI). This is the cleanest possible profile for the OneDrive-synced tree — nothing heavy imports, nothing hangs.
- **The only local code** is a thin orchestration script (stdlib + maybe Pillow) + a SKILL.md. Pillow is the single optional `pip` and it's small and pure-Python.
- **Secrets:** Higgsfield CLI uses browser login (no key in files); MCP is already authed; ElevenLabs key already in env. Nothing new to store, no env-var violations.
- **Outputs** land in a local `out/` dir (large media) — consistent with auto-clip. One OneDrive note: rendered MP4s/PNGs in `out/` will sync; keep `out/` git-ignored and consider it scratch (same posture auto-clip already takes).

---

## Integration sketch — how it composes with the hub

This is a **direct sibling of the Andromeda playbook and they ship as a pair**: the playbook writes the *brief* (how many concepts, which formats, the diversity/volume targets, the "creative is the targeting" framing); this generator *fulfills* it. Data flow:

```
meta-andromeda-ads-playbook  ──(creative brief: N concepts × formats × diversity rules)──▶
        │
        ▼
[ mass-ad-creative skill ]
  1. SLATE BRAIN  (Claude via --provider agent, like auto-clip/highlight.py)
       inputs:  product (Infinet/Artifacial/ClipWith) + brief + team/stats.md niche analytics
       output:  creative-slate.json / vault note — N rows, each a DISTINCT concept
                {id, product, hook, format(9:16|1:1|16:9), angle, visual_treatment, gen_brief, status:"blank"}
  2. GENERATE per row (status:"blank" only → no dupes)
       statics →  Higgsfield image MCP (GPT Image 2 / Nano Banana Pro)  OR  Pillow (templated)
       video/UGC → Higgsfield Marketing Studio MCP (show_marketing_studio / generate_video, URL→ad, avatars)
       VO/music →  ElevenLabs MCP
  3. SCORE  video rows → Higgsfield virality_predictor (brain_activity) → write score back to row
  4. WRITE  results to out/<product>/<concept-id>.{png,mp4}  +  update store(status, job_id, url, score)
        │
        ▼
  STOP at out/ + a review note.  NEVER ads_create_* / publish_*.  Elijah reviews → manually launches.
```

**Which existing pieces it reuses (nothing new built that already exists):**
- **Brain:** `auto-clip/highlight.py`'s `--provider agent` idiom (no key/model) → copy for the slate-writer.
- **Render:** Higgsfield MCP (`generate_image`, `generate_video`, `show_marketing_studio`, `media_import_url`, `virality_predictor`) + the `higgsfield-generate` / `higgsfield-marketing-studio` / `higgsfield-product-photoshoot` skills already in the catalog.
- **Audio:** ElevenLabs MCP.
- **Analytics input:** `team/stats.md` (and the upcoming `ig-2026-algorithm-metric-engine` contract) so concepts are grounded in what actually retains attention in his niches, not generic ad lore.
- **Tracking store:** a vault note or local JSON (NOT a Google Sheet — keep it in-hub). If it becomes a vault note, it is an `idea`-type note under `20-Content/Ideas/` per the property contract (read `_templates/idea.md` first; do not invent a "creative_slate" property — the slate rows live in the note BODY/an attached JSON, not as YAML).
- **Persistence of ad results:** once spend is on, ingest performance into `50-Business/AdSpend/` via the `ad-campaign` template (read-only meta-ads insights), closing the loop the playbook describes.

**Data shapes:** one `creative-slate` record per concept (the row above); one `out/` artifact per generated asset; one optional score per video row. All JSON/markdown — no binary state, no DB.

---

## Phased build sketch

**Phase 0 — the slate brain only (~½ day, do-able now, zero render spend, zero new deps).**
Build the diversity-aware **creative-slate writer**: a thin script (or just the SKILL.md + `--provider agent` prompt) that takes a product + a concept and emits an N-row slate of *genuinely distinct* concepts (enforcing the 8–12-distinct-concepts Andromeda rule, pulling angles from `team/stats.md`). **No image/video is generated yet.** Deliverable: a `creative-slate.json` (or vault idea note) Elijah can eyeball. This is the 80/20 — it proves the only hard part (forced diversity grounded in his data) and is independently useful as an ad-brainstorm tool even before any spend. Mirrors how auto-clip shipped its highlight brain first.

**Phase 1 — wire generation for ONE product, ONE lane (~½–1 day, gated on ad spend being imminent).**
Pick the cheapest lane (statics) for ONE product (say Infinet), wire the slate → Higgsfield image MCP (or Pillow for templated cards) → `out/` → tracking store with dedupe-by-status. Render a small real batch (e.g. 8 distinct statics), hand to Elijah. Add the `virality_predictor` score gate when the video lane comes online. **Stop-at-`out/` hard-coded; no launch path exists in the code.**

**Phase 2 — full skill: multi-lane, multi-product, video + UGC (couples with the playbook).**
Add the Marketing Studio video/UGC lane and ElevenLabs VO; accept a brief *from* the `meta-ads-playbook` skill (formats + diversity targets) and emit results back; add the `--provider agent` virality score to every video row. This is where it becomes the "executor" the roadmap describes.

**Phase 3 — loop + persistence (only if ads are actually running).**
Ingest launched-ad performance into `50-Business/AdSpend/` (read-only meta-ads insights), append a dated learning to `team/memory.md`, and let the next slate learn from which *concepts* won (not which images) — the diversity-aware feedback loop. Skip entirely until there's spend to learn from.

---

## Risks / compliance / ToS

- **Standing Rule 2 (the hard wall):** the pipeline must **stop at `out/`** and never call `ads_create_*` / `ads_update_*` / `publish_*` / `send_dm`. Generation and slate-writing are fine unattended; the launch click is Elijah's, per-action. Bake the stop-gate into the SKILL.md as a rule, not a footnote — same posture as auto-clip and carousel-builder.
- **Meta AI-disclosure rule (NEW, real, citable — effective March 2026):** ad creative where AI *generated/substantially modified the visual subject* (a person, product render, scene — i.e. exactly what Higgsfield produces) **must carry an "AI-generated" label**, and "undisclosed AI content" is now ~14% of ad rejections (3rd-largest category). The generator must (a) **tag every Higgsfield-rendered asset as AI-generated in its tracking store**, and (b) surface a "disclose this as AI on launch" reminder in the review note. Exemptions: AI used only for color/crop/headline-optimization doesn't need disclosure (so a Pillow-templated card with a real product photo may not), and Meta's own Advantage+ Creative is auto-labeled by Meta. **This is a launch-time obligation, not a build blocker — but the skill should not let Elijah forget it.**
- **Andromeda anti-clone reality (the core design constraint, not a risk to mitigate later):** if the generator emits near-duplicates it *defeats its own purpose* — Andromeda collapses them to one entity. Diversity must be enforced at the slate layer (Phase 0). Don't ship a dumb batch loop.
- **Don't treat DTC e-com stats as gospel for his offers.** The volume/format numbers (8–12 concepts, statics-vs-video, +23% Catalog) are from e-commerce studies; Elijah's offers are info/SaaS/creator-product. Treat them as priors; defer to his own `ads_insights` + organic-niche reality. (Same guardrail the playbook research flagged.)
- **Credit burn:** mass video generation spends Higgsfield credits fast. The score gate (`virality_predictor`) and the "generate only `status:blank` rows" dedupe exist partly to avoid wasting credits on weak/duplicate concepts. Phase 1 should cap batch size and confirm with Elijah before any large render run.
- **No ban/scraper ToS risk in the generator itself** — it produces *his own* creatives via paid first-party tools. (Contrast the source advice's "burner research account" idea — passive viewing only; never automate burner scraping. The hub already does competitor/ad intel the clean way via `ads_library_search`.)
- **Opportunity cost:** building the full render loop before any ad spend exists is low-ROI — which is exactly why the verdict is ADD-LATER with only the (independently-useful) Phase-0 slate brain now.

---

## Rough effort

- **Phase 0** (slate brain, no render): ~½ day. No new deps. Independently useful today.
- **Phase 1** (one product, statics lane, tracking + dedupe): ~½–1 day. Optional `pip install pillow`.
- **Phase 2** (full multi-lane skill + video/UGC + score gate, paired with playbook): ~1–2 days.
- **Phase 3** (performance loop into AdSpend): couples with the playbook's Phase-3; don't cost separately.
- **Usable v1 (Phase 0+1): ~1 day**, dominated by the brain prompt + tracking glue, not engineering. Heavy lifting is server-side SaaS the hub already pays for.

**Bottom line:** genuinely useful and unusually cheap (no new deps, reuses the full generation suite + the proven `--provider agent` brain), and it's the natural executor for the already-researched Andromeda playbook — but its value is **conditional on ad spend turning on**, and the `AdSpend/` folder is still empty. So: **ADD-LATER**, build the diversity-aware **slate brain (Phase 0) now** as a dry-run + standalone ad-brainstorm tool, and gate the render loop on the same trigger as its sibling playbook. Ship the two as a pair.

---

## Sources

- Higgsfield — *AI Ad Generator (URL→ad, formats, aspect ratios)*: https://higgsfield.ai/ai-ad-generator
- Higgsfield — *Marketing Studio intro (UGC/CGI/cinematic, avatars, hooks)*: https://higgsfield.ai/marketing-studio-intro
- Higgsfield — *Marketing Automation for Creative (40+ avatars, Soul 2.0, batch variations)*: https://higgsfield.ai/marketing-automation
- Higgsfield — *CLI (agent-friendly, browser login, no API key)*: https://higgsfield.ai/cli
- MindStudio — *Ad Creative Generation with Claude Code and Higgsfield (the exact pattern: slate → CLI loop → tracking)*: https://www.mindstudio.ai/blog/build-brand-ad-creative-claude-code-higgsfield-5-minutes
- MindStudio — *Higgsfield CLI with Claude Code for scalable content automation*: https://www.mindstudio.ai/blog/higgsfield-cli-claude-code-content-automation
- `@higgsfield/cli` (official) install + commands: https://higgsfield.ai/cli ; unofficial community CLI: https://github.com/clawdybotty/higgsfield-cli
- ScaleDon — *Meta Andromeda Creatives: the data behind the 2026 shift (clustering near-identical creatives, diversity rule)*: https://scaledon.com/meta-andromeda-creatives-the-data-behind-the-biggest-ad-strategy-shift-in-2026/
- To The Max — *Executive Guide to Creative Diversification on Meta (8–12 distinct concepts)*: https://marketingtothemax.com/creative-diversification/
- Confect — *Meta Andromeda: the ultimate guide to Meta Ads in 2026*: https://confect.io/tactics/meta-andromeda-2026
- TechJack Solutions — *Meta now requires advertisers to disclose AI-generated content*: https://techjacksolutions.com/ai-brief/meta-now-requires-advertisers-to-disclose-ai-generated-conte/
- AuditSocials — *Meta AI Content Label Policy 2026: detection & disclosure*: https://www.auditsocials.com/blog/meta-ai-generated-content-label-policy-2026
- Pillow (PIL fork) — programmatic/batch image generation, PyPI 12.2.0: https://pypi.org/project/pillow/
- Sibling research: `docs/plans/2026-06-14-meta-andromeda-ads-playbook-research.md`
- Hub context: `docs/plans/2026-06-14-overnight-roadmap.md` (line 101), vault `Brainstorming/In the moment ideas.md`, `auto-clip/highlight.py` (`--provider agent` pattern), vault `CLAUDE.md` (meta-ads write-gate), `HANDOFF.md` (ad acct `661339332628311`)
