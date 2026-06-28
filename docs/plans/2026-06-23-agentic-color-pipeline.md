# PLAN — Agentic color pipeline (auto-correction + stylized grading, images + video)

**Date:** 2026-06-23 · **Status:** ✅ BUILT + VERIFIED end-to-end on real footage (stills · single-clip · multi-scene video with auto shot-detect + per-shot constant correction + shot-match). Live tracker: `auto-clip/COLOR-BUILD-STATUS.md` · engine: `auto-clip/color.py` + `auto-clip/colorkit/`. DRAFT — uncommitted, stops at `out/`, never publishes.
**Origin:** Elijah is stuck learning DaVinci grading; wants a fast preset process now AND a higher
ceiling later. Research run: `agentic-color-grading-research` workflow (28 agents, ~1.8M tokens, 7 lanes,
9/10 load-bearing claims survived 2-vote adversarial verify). Tool verdict logged to `AGENT-TEAM-BLUEPRINT.md`
(2026-06-23 entry). Engine premises grounded against the real `auto-clip/` code on 2026-06-23.

---

## 0. The one-paragraph answer

Build our own **two-tier, fully-headless Python + FFmpeg color engine — no DaVinci Studio dependency.**
**Pixel-math measures and corrects** (OpenCV+NumPy for per-pixel ground truth, FFmpeg `signalstats` for cheap
whole-clip triage, `colour-science` for perceptually-correct targets); **semantic AI decides the look**
(Gemini / TwelveLabs Pegasus pick mood/intent — they do NOT and cannot measure pixels). It runs the canonical
pro order — **1) correct each shot to neutral → 2) match shots → 3) stylize on top** — and obeys one
non-negotiable video rule: **never correct per-frame-independently; derive ONE correction per shot and apply it
as a constant transform, or you get flicker/pumping.** Everything is pip/winget-installable, PowerShell-run, no
GPU or API key on the default path, and it bolts onto the existing `auto-clip` engine as a new `color.py` stage.

## 0.5 Does this already exist? (prior-art verdict — second workflow, 25 agents)

**PARTIALLY — and the precise gap is our build.** The *idea* (auto-correct WB/exposure/contrast + apply a
cinematic grade, even with AI shot-matching) is fully mainstream and shipping — consumer one-tap (Google Photos
Enhance, CapCut AI Color Correction) and pro tools (Colourlab AI, fylm.ai, DaVinci Auto Balance + AI Color Match).
So "nobody's done this" is wrong at the concept level. **But the specific architecture — one HEADLESS/programmable
engine that ingests a flat multi-scene file, measures pixels, auto-segments into shots with a CONSTANT per-shot
correction (anti-flicker), matches shots, stacks a STYLIZED grade, and uses an LLM to DECIDE the look — is NOT
shipped as a product or complete open repo.** That exact box is empty in both markets.

Verified closest matches (adversarially checked, not taken at face value):
- **`perbhat/agentic-color-grader`** (MIT, GitHub) — **closest runnable prior art.** LLM-agent-over-FFmpeg,
  headless: measures (scopes) → corrects to neutral → groups scenes → matches shots → AI-iterates. **But** (from
  inspecting its code) it has **NO creative/stylized grade** (only a technical S-Log→Rec709 LUT) and works
  **clip-by-clip, not true single-file shot segmentation.** 2★, single author, Sony-S-Log toy. Covers ~4 of our 6
  stages — missing exactly the two that make ours ours.
- **`isaacrowntree/color-grade-ai`** (MIT) — clean pattern for an LLM emitting a real `.cube` LUT (corrective +
  creative). Frame-scoped; pair with a segmentation front-end.
- **LumiVideo** (arXiv 2604.02409, Apr 2026) — best published design for the *decision layer* (VLM + LLM + RAG +
  Tree-of-Thoughts → ASC-CDL + 3D LUT). **No code released**, applies ONE global LUT from a single anchor frame
  (explicitly disclaims shot segmentation), GUI/DaVinci-oriented.
- **Colourlab AI / fylm.ai** — closest commercial *quality*, but **GUI-locked, no public API** (can't be wrapped).
- **AutoFinish.ai (Otto)** — genuinely headless API, autonomous grade — **but no single-file shot segmentation or
  shot matching** (skips our hardest stages).
- **DaVinci Resolve** — all the pieces in one app, but the **AI engines are NOT exposed to the scripting API** (can
  only round-trip pre-built grades), and needs Studio + an open GUI.

**Our defensible novelty = execution + packaging, not the concept:** the *combination* of headless + true
single-file per-shot anti-flicker segmentation + measured-neutral correction + creative stylize-on-neutral +
agentic look-choice, delivered as a CLI/API. Don't externally overclaim inventing auto-grading.

**Build-vs-adopt verdict: FORK-AND-EXTEND, don't build from zero and don't wrap a closed tool.** Study
`perbhat`'s agent loop as the blueprint, borrow `color-grade-ai`'s LUT-emit pattern, use LumiVideo as the
decision-layer design — then ADD the two genuinely-missing pieces (PySceneDetect single-file segmentation with
per-shot constant correction; a creative stylize stage on the neutral base under agent control). Every other brick
(OpenCV, ffmpeg, PySceneDetect, .cube/ASC-CDL) is mature — integration is the work, not reinvention.

## 1. The headline question, answered: who gives the most per-pixel color data?

**OpenCV + NumPy** — and the key realization is it's a *pixel-math stack, not a provider/service.*
`cv2.imread()` / `cv2.VideoCapture.read()` hand back the decoded frame as a raw `H×W×3` NumPy array — the
actual numeric color of **every** pixel in BGR — and `cv2.cvtColor` losslessly re-expresses it into
LAB / HSV / YCrCb / XYZ. This is load-bearing because **the full per-pixel array is a strict superset of every
aggregate**: you can always compute histograms, gray-world means, percentiles, or `signalstats` numbers *from*
the array, but never recover the array *from* the aggregates.

The ranking that matters for us:
- **Per-pixel ground truth → OpenCV + NumPy.** Richest possible; everything else sits on top of these arrays.
- **Perceptual correctness targets → `colour-science`.** CIE XYZ/Lab/Oklab, ΔE 2000, CCT in Kelvin — defines
  what "correct" *means*, not just raw code values.
- **Cheap whole-clip-per-frame triage → FFmpeg `signalstats`.** ~30 numeric values/frame (5-point Y/U/V/SAT
  distribution + hue + temporal diffs), exported as JSON via `ffprobe ... -of json`. Aggregate, not per-pixel
  → it's the "where is it wrong" map that tells you *which* frames deserve the heavy per-pixel pass.
- **Deepest bit-depth (RAW stills only) → `rawpy`** (pre-demosaic sensor data + camera WB). Only relevant if
  Elijah shoots RAW stills; his documented camera output is 10-bit H.265 MP4.
- **Semantic services → effectively none for measurement.** Confirmed: TwelveLabs Pegasus = descriptive text
  only; Google **Gemini documents NO numeric color output** (boxes/masks only). The *one* semantic service that
  returns measured pixel data is **Google Cloud Vision `image_properties`** (dominant colors as RGB +
  pixelFraction) — useful for palette/look context, not per-pixel correction. (Note: the verifiers refuted the
  absolute claim "Marengo embeddings carry zero color" — embeddings *implicitly* encode visual features
  including color, but they are not extractable as numeric color values, so still useless as a measurement.)

## 2. Decision layer vs measurement layer (the architecture's spine)

| | MEASUREMENT (pixel-math) | DECISION (semantic AI) |
|---|---|---|
| Tools | OpenCV+NumPy, FFmpeg signalstats, colour-science, scikit-image | Gemini-video, TwelveLabs Pegasus, (Marengo = retrieval) |
| Answers | "where/how is the color wrong, what's the correct target" | "what is this footage, what look should it have" |
| Cost | deterministic, free, no GPU/key | tokens/API |
| Output | gains, curves, LUTs, ΔE, CCT | "warm indoor interview → clean neutral skin" / "moody night → lean teal-orange" |

**Rule:** the semantic layer *chooses intent*; the pixel layer *measures and corrects*. Never let semantic AI
set numeric gains; never let pixel-math decide creative intent.

## 3. Image vs video — the real difference

- **A still is one-shot:** analyze frame → one correction → apply. (Stage 1 + Stage 3 only.)
- **Video breaks this three ways:** (1) one clip = many shots with different lighting → must **segment into
  shots** and correct shot-by-shot, never one-correction-for-the-file; (2) **temporal consistency** is the
  load-bearing failure mode — per-frame-independent auto-correction wobbles → visible **flicker/pumping** (the
  single most-cited problem in the literature: Bonneel 2015, Lai 2018, Lei 2020); (3) **shot matching** across
  cuts for continuity, which stills never need.
- **Temporal-consistency rule (non-negotiable):** analyze **one representative frame per shot → one constant
  correction → apply to every frame of the shot.** Constant params = structurally no flicker. Only escalate to
  per-frame when a shot has strong intra-shot lighting change (pan shade→sun); then smooth params over N frames.
  Backstops: FFmpeg `deflicker`/`normalize=smoothing`; Deep Video Prior only for un-reducible per-frame AI ops.

## 4. The pipeline architecture

| Stage | Does | Tool |
|---|---|---|
| **0 — Router** | image → single shot of length 1 (skip 0b + 2); video → full pipeline | Python file-type check |
| **0b — Shot segmentation** (video) | cut detection → per-shot `(start,end)` timecodes | PySceneDetect `AdaptiveDetector` |
| **1 — Triage** | one cheap whole-clip pass; flag flat/cast/oversaturated frames | FFmpeg `signalstats` → ffprobe JSON |
| **1b — Per-pixel measure** | decode representative frame → arrays; LAB/HSV stats, gray-world, percentiles | OpenCV+NumPy (+ colour-science targets) |
| **1c — CORRECT** | emit params (channel gains, eq, curves) from the rep frame; apply **constant** across the shot | OpenCV `xphoto` WB + scikit-image → FFmpeg `colorbalance`/`colortemperature`/`eq`/`curves` |
| **2 — MATCH shots** (video) | match each shot's LAB mean+std to a hero shot; constant per-shot transform | Reinhard LAB transfer (cv2+numpy) |
| **3 — STYLIZE** | the look, last, uniform across all shots | FFmpeg `lut3d=interp=tetrahedral` (.cube) + `colorbalance`/`colorchannelmixer`/`vibrance` |
| **3b — Temporal safety net** (video) | residual luminance pumping | FFmpeg `deflicker`/`normalize`; DVP (escalation, GPU) |
| **4 — Render** | concat or single filtergraph; encode once; **stop at `out/`** | FFmpeg |

## 5. Tool stack (all pip/winget, free, headless)

**Core (default path, no GPU/key):**
`pip install opencv-contrib-python numpy scikit-image colour-science scenedetect[opencv]`
+ FFmpeg (`winget install Gyan.FFmpeg`).

- **OpenCV-contrib + NumPy** — per-pixel arrays; `xphoto` auto WB (`createGrayworldWB`/`createLearningBasedWB` →
  `applyChannelGains`), CLAHE, HSV/LAB masks. *Apache-2.0.*
- **scikit-image** — `exposure` (histogram, `is_low_contrast`, `match_histograms`, `equalize_adapthist`,
  `adjust_gamma`); `color` (rgb2lab/hsv, ΔE). *BSD-3.*
- **colour-science** — perceptual targets (ΔE2000, CCT) + 3D-LUT apply. *BSD-3.*
- **PySceneDetect** — shot segmentation (`AdaptiveDetector`). *BSD-3.* (Already on auto-clip's roadmap.)
- **FFmpeg** — the deterministic apply + triage layer (`signalstats`, `colorbalance`, `colortemperature`, `eq`,
  `curves`, `lut3d`, `vibrance`, `selectivecolor`, `deflicker`, `normalize`). *LGPL/GPL.*

**Optional / situational:**
- `color-matcher` (reference-still transfer, **GPL-3.0** → fine for personal use, flag if ever commercial),
  `lut-estimator` (before/after → .cube), `colorgram.py`/`colorthief` (palettes), `rawpy` (RAW stills),
  OpenColorIO (cross-scene management), Deep Video Prior (AI flicker removal — torch/GPU, gate behind a flag).

## 6. Advanced techniques → code primitives (the "stylize" vocabulary)

| Technique | Primitive | How (tier) |
|---|---|---|
| S-curve / contrast | per-channel tone curve | FFmpeg `curves=preset=...` (T1, automate freely) |
| Split-toning (teal shadows/orange highs) | per-range RGB lift | FFmpeg `colorbalance` (pl=1) (T1) |
| Teal-and-orange | 3×3 channel mixer | FFmpeg `colorchannelmixer`+`colorbalance` or bake to LUT (T1) |
| Film/analog "house look" | 3D-LUT bake | FFmpeg `lut3d=interp=tetrahedral` (.cube) (T1) |
| Vibrance / selective sat | weighted sat boost (protects skin) | FFmpeg `vibrance` (T1) |
| Portable primary grade | ASC-CDL slope/offset/power | OCIO `CDLTransform` (T1, serializable) |
| HSL secondaries / color isolation | HSV/LAB threshold mask | `selectivecolor`/`huesaturation` first; OpenCV `inRange`+feather only if a true mask is needed (T2, guardrails) |
| Skin-tone protection | skin-range mask, grade chroma not luma | OpenCV HSV/LAB + feather (T2) |
| Reference-still matching | global distribution transfer | `color-matcher` — **never 100%, blend with alpha, gate to review** (T3, high-risk) |
| Sky/region grade on video | learned soft matte | SkyAR / ADE20K seg — **brittle at night/edges, flickers** (T3, hardest) |

## 7. Integration with the hub (grounded against real code)

- **Home = `auto-clip/`.** Verified: it's a chain of standalone Python CLI stages (`transcribe → highlight →
  reframe/facetrack → tighten → caption`), orchestrated by the `auto-clip` skill, already on **ffmpeg + OpenCV**,
  already runs headless from PowerShell, already **stops at `out/`** and never publishes. **PySceneDetect shot
  cuts are already on its roadmap** — our Stage-0 reuses that exact planned dependency.
- **Drop point:** add `color.py` as a new stage **after `tighten.py`, before `caption.py`** (grade the clean cut,
  then burn captions on top of the graded image). Same CLI-module shape as its siblings; add deps to
  `auto-clip/requirements.txt`.
- **FFmpeg MCP + local binaries** (wired in this hub and `abc wrap`) cover the entire apply + triage layer — no
  new install for that part.
- **`color-grade-system` skill** (in `abc wrap`, CSS-filter/Remotion render-time) = the **look library / preset
  vocabulary**, NOT the correction engine. This new engine is its headless FFmpeg-native counterpart and can
  export the same looks as `.cube` LUTs so both stay in sync.
- **`gemini-video` MCP + TwelveLabs `video-intake`** = the optional DECISION call (pick the look), numeric
  correction always stays in pixel-math.
- **Env gotchas honored:** run Python/ffmpeg via PowerShell (not Bash); `pip show` not `python -c import` for
  heavy cv2/torch on the OneDrive disk; DVP/torch gated behind a flag, never the default path.

## 8. Realistic quality ceiling (honest)

- **Very high for CORRECTION and DETERMINISTIC STYLIZED looks** — gray-world/learning-based WB, exposure/contrast
  normalization, S-curves, split-toning, teal-orange, and tetrahedral .cube film LUTs are pixel-identical to what
  a colorist would script, and constant-per-shot application is genuinely flicker-free. **~70% of pro color work
  is fully scriptable today at near-pro quality.**
- **The ceiling is hit in exactly two places** (quality, not capability gaps): (a) **automatic AI shot-matching** —
  Colourlab.Ai and DaVinci Color Match are best-in-class but **both are GUI/OFX-only with NO public CLI/API**
  (Resolve's Python API explicitly does not expose Color Match/Neural-Engine, and needs Studio anyway); our
  headless equivalent is Reinhard-to-hero-frame matching — good, not as smart. (b) **hard semantic masks** (sky,
  fine skin secondaries) where learned segmentation is brittle and flicker-prone. Both bridgeable only by human
  review or computer-use UI automation of a GUI tool.

## 9. Phased build (thin proof first)

0. **Study the blueprints (~30 min, before code).** Read `perbhat/agentic-color-grader`'s agent loop +
   scope-measurement design and `isaacrowntree/color-grade-ai`'s LUT-emit pattern. Don't fork wholesale — lift the
   patterns, build fresh on permissive bricks.
1. **Spike — still auto-correct + stylize (Stage 1+3 only).** OpenCV load → `createGrayworldWB` WB +
   CLAHE/contrast normalize + `is_low_contrast` check → emit params → apply one .cube stylize → before/after to
   `out/`. Proves the `analyze→params→apply` core + look library on the lowest-risk input, zero temporal
   complexity. (~1 evening.)
2. **The video leap — wrap the SAME core in PySceneDetect.** Treat each shot as "a still of length 1," derive
   one constant correction per shot, apply via FFmpeg. **This is where flicker appears or doesn't** — verify on a
   real multi-shot clip (the Elijah/Derwin interview already in auto-clip is the test case).
3. **Shot-matching (Stage 2) + temporal backstops.** Reinhard-to-hero, then `deflicker`/`normalize` safety net.
4. **Wire into the auto-clip chain** as `color.py` (after tighten, before caption), with image-vs-video routing
   and the constant-per-shot rule enforced.
5. **Look library** — build/port a small `.cube` set (neutral-correct, warm-interview, teal-orange, film); sync
   with `abc wrap`'s `color-grade-system`.
6. **(Optional) Decision layer** — Gemini/Pegasus selects the look; all numeric correction stays in pixel-math.

## 10. Risks / caveats

- **Flicker** is the whole reason the architecture exists — enforce constant-per-shot; never per-frame-independent.
- **Reference-still matching over/undershoots** — blend with alpha, similar-content reference, gate to review.
- **Hard HSV/LAB masks fringe** without feather — always erode/dilate + blur + clamp strength; prefer
  `selectivecolor`/`huesaturation` when a per-family nudge suffices.
- **Semantic sky/skin secondaries** are a quality risk, not a solved capability.
- **FFmpeg 8.1 native `ocio` filter** needs an OCIO-enabled build; `ociobakelut → lut3d` is the portable path.
- **Licenses:** core stack is Apache/BSD/MIT (clean). `color-matcher` is GPL-3.0; Afifi Deep White-Balance and
  NeuralPreset are research/non-commercial — fine for personal single-operator use, flag if ever distributed.
- **No DaVinci dependency** by design — the best AI matchers have no API and Resolve needs Studio for scripting.

## 11. Open decisions (Elijah's call)

1. **Default behavior:** correction auto-on, stylize opt-in (recommended) · both opt-in · both auto-on?
2. **v1 look-decision:** hard-code a small look library and skip API cost until the pixel core is proven
   (recommended) · wire Gemini/Pegasus look-picking from the start?
3. **Look library source:** port the existing `abc wrap` `color-grade-system` CSS presets to .cube · author
   fresh cinematic film looks (Kodak 2383 / Fuji emulation) · both?
4. **Shot-match ambition:** headless Reinhard-to-hero good enough · is the gap to Resolve Color Match worth a
   computer-use GUI-automation path for hero projects?
5. **RAW branch:** does he shoot RAW stills often enough to justify a `rawpy` pre-demosaic path, or is 10-bit
   H.265 MP4 the only real input?
6. **GPU posture:** stand up torch cu128 now (enables DVP + learning-based WB at scale) or stay CPU-only until a
   per-frame AI op forces it?

## 12. Fork-and-extend map (verified prior art → our build)

Treat the closest repos as **reference designs, not dependencies** (they're 2–8★, expect to rewrite). Stay on
permissive licenses for a possible future product — **avoid GPL `color-matcher` in shipped code**; swap for an
OpenCV/colour-science transfer.

| Repo | License | Take from it | What it lacks (= our work) |
|---|---|---|---|
| **perbhat/agentic-color-grader** | MIT | the headless LLM-agent-over-FFmpeg loop (measure→correct→detect→match→iterate) | NO creative stylize; clip-by-clip, not single-file shot segmentation |
| **isaacrowntree/color-grade-ai** | MIT | LLM-emits-real-.cube-LUT pattern (corrective + creative) | frame-scoped; no segmentation front-end |
| **Breakthrough/PySceneDetect** | BSD | true single-file shot segmentation (the piece every prior-art misses) | — (use as-is) |
| **collinswakholi/ColorCorrectionPackage** | MIT | multi-step measured correction chain (FFC+GC+WB+CC) → per-shot neutralizer | not video/temporal |
| **seunghyuns98/VideoColorGrading** | (ICCV 2025) | video-native reference-driven creative LUT (diffusion) — study as the creative stage | no neutral correction or shot detect |
| **regiellis/ComfyUI-EasyColorCorrector** | — | mine for creative-look presets (auto-WB + 30 looks) | image-only, ComfyUI-GUI-bound |
| **LumiVideo** (arXiv 2604.02409) | paper | decision-layer design (Perception/Reasoning/Execution/Reflection, RAG + ToT) | no code; one global LUT, no segmentation |

- **Avoid for commercial:** Afifi Deep-White-Balance, NeuralPreset (research/non-commercial); `color-matcher` (GPL).
- **Adopt ASC-CDL + .cube as the interchange format** (what LumiVideo + pro tools standardize on) — keeps grades
  inspectable, reversible, and NLE-compatible.
- **The hard part nobody has packaged:** per-shot constant correction kills flicker *within* a shot but can create
  visible *jumps at cut boundaries* — the continuity-match stage (§4 Stage 2) is what reconciles them. Budget real
  effort there.
