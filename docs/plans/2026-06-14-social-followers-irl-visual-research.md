# Social Followers IRL-Scale Reel — Research & Build Plan

**Candidate id:** `social-followers-irl-visual`
**Date:** 2026-06-14
**Source:** vault `20-Content/Ideas/Different cool video ideas.md` (line 2 — the only un-researched Video roadmap item)
**Researcher pass:** focused timebox, WebSearch + WebFetch (exa/tavily/firecrawl keys dead).

---

## Headline verdict: **ADD-NOW (build-this-week)** — small, high-confidence, time-boxed

**Effort: ~0.5–1 day for a postable v1.** Confidence: **high.**

This is the rare candidate with a real clock: it is tied to Elijah hitting **~100k followers in the next couple of days** (his words in the idea note). Its value is near-zero once the milestone passes, and it's the *only* un-researched Video item — so it's worth jumping the queue. It is also genuinely cheap and low-risk: it composes directly with the hub's existing **HyperFrames `three` skill** (deterministic Three.js → MP4), needs **no new heavy dependencies** (no torch/cv2/cloud/paid), and the core technique — a GPU-instanced crowd that counts up 10 → 100 → 1k → 10k → 100k — is a solved, well-documented Three.js pattern that runs at 100k characters / 240fps in **one draw call**.

The honest caveat: this is a **one-shot content asset, not reusable infrastructure.** Don't over-build it into a parameterized "engine." Build the smallest thing that renders one great 9:16 reel, ship it before the milestone, and stop. A thin reusable scaffold is a nice-to-have, not the goal.

---

## What it actually is

A short-form "scale reveal" reel in the proven **"what does X people actually look like"** trend format. On-screen, the follower count ticks up in stages — **10 → 100 → 1,000 → 10,000 → 100,000** — and at each stage a crowd of *exactly that many* little people materializes around a central figure (Elijah / an avatar / a dot), with the camera pulling back so the viewer *feels* the scale jump from "a handful" to "a stadium." The emotional payoff: 100k followers is not an abstract number, it's a literal sea of humans. Timed to his actual milestone, it doubles as a celebration / thank-you post.

This is a live, performing trend, not a hypothesis:

- **TikTok discover pages** exist for "What Does 10 Thousand People Look Like", "What A Crowd of 100 Actually Looks Like", "What Does 100 People Look Like" — i.e. the format already has search demand and a recognizable shape.
- **visualizecrowds.com** (by Eric Otten) is a **Three.js** web tool that takes a number and renders *an actual 3D crowd of individuals* — built explicitly to help creators feel the real-world weight of their follower/like counts. This is the closest existing reference to exactly what Elijah wants (but it's a closed website with no export, so we rebuild the idea, not reuse the site).
- **crowdscale** (davkap92.github.io/crowdscale) visualizes big numbers as *stadium units* (each stadium = 100k) — a useful "100k = one full stadium" framing device, but it renders abstract stadiums, **not** individual people, so it's a weaker reference.
- A three.js-forum showcase, **"One Draw Call, Massive Crowd"**, renders **100,000 animated characters at 240 FPS, sub-2ms GPU**, via a single `InstancedMesh` with per-instance IDs and shader-driven detail/LOD — proof the heavy stage is trivially within budget.

**Niche fit:** this is a personal-brand / milestone post, not a Money or AI/Tech educational reel (his two strongest niches by views/saves). So judge it as a one-time **brand moment**, not as recurring niche content — its job is celebration + reach on the milestone, and the format's novelty is the hook.

---

## Best 2026 approach + tooling (and licenses)

There are two viable build paths. **They are complementary, not competing — the recommended v1 is Path A; Path B is an optional flourish.**

### Path A (RECOMMENDED) — Deterministic Three.js crowd in HyperFrames

Build the count-up crowd as a **HyperFrames composition** using the hub's **`three` skill** (seek-driven, deterministic Three.js that renders to MP4 via Chrome's `beginFrame`). This is the right tool because:

- **Exact, controllable counts.** A crowd of *precisely* 10 / 100 / 1,000 / 10,000 / 100,000 is the entire point. An `InstancedMesh` lets you place exactly N figures and animate the count + camera deterministically. AI video generators (Path B) **cannot** hit an exact count or do a clean progressive reveal — they hallucinate "a big crowd."
- **Render-safe scale.** 100k static/billboarded figures in one draw call is comfortably within the documented Three.js budget (the forum demo hits 100k *animated* at 240fps). For a reel we don't even need skinned animation — **billboarded sprites or low-poly capsules with a subtle idle wobble** read perfectly at this scale and keep it dead-simple and deterministic.
- **Already wired.** HyperFrames is HeyGen's open-source HTML→MP4 renderer (`github.com/heygen-com/hyperframes`), the `three` skill exists at the SDK level, and the `platform-exporter` skill finishes to exact IG Reels specs. Zero new infra.

**Tools / licenses:**
- **Three.js** — MIT. The crowd renderer (`InstancedMesh`, one draw call).
- **HyperFrames** — open source (HeyGen), the deterministic HTML→MP4 harness. Hub `three` / `hyperframes` / `hyperframes-cli` skills drive it.
- **`platform-exporter` skill** — IG Reels 1080×1920 finishing.
- Optional **ElevenLabs MCP** (already wired) — a one-line VO ("this is what 100,000 of you looks like") and/or `text_to_sound_effects` for a crowd "whoosh." Caption via `caption-engine` or `viral-shortform-2026` house style.

### Path B (OPTIONAL flourish) — Higgsfield/Seedance hero shot

Higgsfield is already wired (`higgsfield-generate`, Seedance 2.0 / Kling 3.0, ~1.9k credits). The **viral "Korean baseball stadium" AI trend** shows these models do hyper-real stadium-crowd *broadcast* shots beautifully. But the research is clear on the limits: best at **3–8s clips**, optimized for one continuous shot, and they **cannot do an exact-count progressive count-up** or guarantee crowd consistency across a 10→100k sweep.

So Path B's correct role is a **single hero/payoff shot** — e.g. a photoreal "Elijah standing at center field as the stadium fills to 100k" beauty frame to *end* on, cut after the Three.js count-up does the actual scale storytelling. Use it to garnish, not to carry the reel.

**Verdict on tooling:** Path A is the engine; Path B is optional seasoning. Build A first; only add B if there's time before the milestone.

---

## Windows + OneDrive feasibility & dependency weight

**Green across the board — this is one of the lightest candidates researched.**

- **No heavy Python.** No torch, no cv2, no faster-whisper, no model downloads. The whole thing is browser-side JS (Three.js) rendered by the HyperFrames harness. None of the OneDrive "heavy-import-hangs-on-synced-disk" failure modes apply.
- **No new MCP / API keys.** Higgsfield + ElevenLabs are already wired; everything else is the existing HyperFrames toolchain. Nothing depends on the dead exa/tavily/firecrawl keys.
- **No secrets to manage.** No new env vars; respects rule 3 (OneDrive-synced tree).
- **OneDrive note:** keep the working composition folder small (the HyperFrames `remotion-longform`/public-dir hygiene habit isn't needed here — there's no big source media; the crowd is generated, not ingested). Render output is one short MP4.
- **GPU:** Three.js uses the browser's WebGL — no CUDA/torch-cu128 gate. 100k instances render fine on integrated graphics for a short clip; worst case, drop to billboarded sprites.

---

## How it composes with the hub (integration sketch)

This slots cleanly into the existing generation suite — **no new engine, a new composition + a thin optional skill.**

```
                 ┌─────────────────────────────────────────────┐
  follower       │  HyperFrames composition (the `three` skill) │
  milestone  ──► │  • InstancedMesh crowd, exact N per stage    │ ──► out/100k-irl.mp4
  (100,000)      │  • count-up label + camera pull-back         │     (1080×1920)
                 │  • stages: 10→100→1k→10k→100k, deterministic │
                 └─────────────────────────────────────────────┘
                        │                         │
        (optional VO)   ▼          (optional)     ▼
   ElevenLabs MCP ──► audio track          caption-engine / viral-shortform-2026
                                                  │
                                                  ▼
                                          platform-exporter (IG Reels spec)
                                                  │
                                                  ▼
                                   Elijah reviews in out/ → his click to post
                                   (CLAUDE.md rule 1 — never auto-publish)
```

- **Which engine/skill:** primarily the SDK-level **`three`** + **`hyperframes` / `hyperframes-cli`** skills; finish with **`platform-exporter`**; optional **`caption-engine`**/**`viral-shortform-2026`** and **`higgsfield-generate`** (Path B) + **ElevenLabs MCP** (VO/SFX).
- **Data shapes (tiny, all local):** a config object — `stages: [{count: 10, label: "10"}, … {count: 100000, label: "100K"}]`, `secondsPerStage`, `cameraPath`, optional `voPath`. No JSON pipeline, no transcript, no model artifacts.
- **Output contract:** like auto-clip, **stops at a review file in `out/`** and reports the path — never publishes. His click is the publish action (rules 1 & 4: if ever IG-API-published, must be voice-only/original-audio with a `get_content_publishing_limit` pre-flight).
- **Where it lives:** a one-off composition folder now; *if* it proves worth keeping, promote to a thin `milestone-reel` skill later (low priority — see Phase 2). Don't build the skill first.

---

## Phased build sketch

**Phase 0 — smallest safe thing (≈1–2 hrs): static proof of scale.**
One HyperFrames `three` composition that renders **five still frames** — a crowd of exactly 10, then 100, 1k, 10k, 100k — using `InstancedMesh` billboarded sprites, with the count label and a fixed wide camera. No animation, no audio. Goal: confirm 100k instances render correctly and *read* well at 9:16, and that the scale jump lands visually. This de-risks everything heavy in the cheapest possible way.

**Phase 1 — the postable reel (≈half a day): the count-up.**
Add the deterministic **count-up animation** (label ticks 10→100→1k→10k→100k) + **camera pull-back** synced to each stage, a central hero figure (Elijah avatar / dot), and a tasteful idle wobble on the instances. Add the **hook gate** (first 1s must stop the scroll — start mid-jump, e.g. snap from 1k to 10k). Burn captions (`viral-shortform-2026` house style) + a one-line ElevenLabs VO and a crowd-swell SFX. Export via `platform-exporter` to 1080×1920. **Deliver to `out/` for his review — this is the shippable artifact before the milestone.**

**Phase 2 — optional, only if time / only if reused later:**
- Path B Higgsfield photoreal stadium hero shot to end on.
- Promote the composition to a thin **`milestone-reel`** skill (parameterized count + label) so any future milestone (200k, 1M, or *likes/views* on a specific reel — visualizecrowds' original framing) is a one-command reel. **Defer unless Phase 1 proves the format performs** — log the result to `team/memory.md` first (rule 7).

---

## Risks / compliance / ToS

**Low risk overall.**
- **Platform ToS / ban risk: none.** It's original generated content; no scraping, no automation against IG, no licensed-audio issue (use original-audio/VO per rule 4). Nothing touches developers.facebook.com.
- **Publish risk: controlled by the standing rule.** Engine stops at `out/`; Elijah's explicit click is the only publish action (rule 1).
- **Likeness:** if a recognizable Elijah avatar is used, it's his own likeness — fine. If Path B Higgsfield is used with his face, route through `higgsfield-soul-id` for identity fidelity (already the documented pattern).
- **The real risk is the clock, not compliance.** Value decays the moment he passes 100k. If it can't ship clean within ~2 days, the honest call is to either rush a Phase-0/Phase-1-lite version or skip it (don't post a milestone reel a week late). Build small, ship fast.
- **Over-engineering risk:** the temptation is to build a polished reusable "crowd engine." Resist it — this is a dated content asset. Phase 0 + 1 only; Phase 2 is explicitly conditional.

---

## Sources

- visualizecrowds.com — Three.js 3D crowd-from-a-number tool (closest reference): https://www.visualizecrowds.com/
- crowdscale stadium visualizer (100k = one stadium framing): https://davkap92.github.io/crowdscale/
- three.js forum — "One Draw Call, Massive Crowd" (100k chars @ 240fps, one InstancedMesh): https://discourse.threejs.org/t/one-draw-call-massive-crowd-performance-engineering-in-three-js/89928
- Three.js InstancedMesh docs: https://threejs.org/docs/pages/InstancedMesh.html
- Codrops — Three.js instances rendering (2025): https://tympanus.net/codrops/2025/07/10/three-js-instances-rendering-multiple-objects-simultaneously/
- HyperFrames (HeyGen open-source HTML→MP4, Three.js adapter, deterministic beginFrame): https://github.com/heygen-com/hyperframes
- HyperFrames deep dive (Three.js/Lottie/GSAP adapters, determinism): https://blog.nidhin.dev/video-as-code-a-deep-dive-into-heygen-s-hyperframes
- Khaleej Times — viral AI stadium video trend (Path B realism + limits): https://www.khaleejtimes.com/business/tech/go-viral-how-to-create-your-own-ai-stadium-video-like-the-korean-trend
- Seedance 2.0 stadium broadcast template (Path B, ~15s hero shots): https://seedance2.so/templates/stadium
- "Visualizing Crowd Sizes" (50 → 100k reference imagery): https://blog.lime.link/visualizing-crowd-sizes/
- TikTok trend discover page — "What Does 10 Thousand People Look Like": https://www.tiktok.com/discover/what-does-10-thousand-people-look-like
