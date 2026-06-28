# COLOR ENGINE — autonomous build status (live)

**Started:** 2026-06-23 (Elijah's birthday dinner run) · **Mode:** autonomous looping build, DRAFT-only.
**Plan:** `docs/plans/2026-06-23-agentic-color-pipeline.md` · **Rules:** stops at `out/`, never publishes, not committed.

---

## ✅ 2026-06-27 (cont.) — ITEM 4 AUTO-PILOT (widen `--look auto` to all 10) — built + verified — "ALL FOUR" DONE

Baton §3 **item 4** (the "smarter" axis), safe portion. `--look auto` now picks from **all 10 looks**, not
the original 5. The deterministic brain (`decide.suggest_look`) keeps its conservative ordered first-match
structure but each branch now refines into a 2026-06-24 look when a secondary signal is decisive:
portrait→**portra_style** (bright+soft) else warm_interview · warm→**golden_hour** (bright) else kodak ·
cool→**moody_blue** (dark) else teal_orange · bright+punchy neutral→**clean_pop** · gritty desaturated
high-contrast→**bleach_bypass** · foliage→fuji · cinematic hi-contrast+sat→teal_orange · else neutral.
`decide.VALID_LOOKS` widened to all 10; thresholds added (`_BRIGHT`/`_DARK`/`_SOFT_CONTRAST`/`_SAT_POP`/
`_GRIT_*`). **DRAFT.** The **live Claude-vision look-picker stays Elijah-gated** — `suggest_look_ai` is
still a documented no-op stub (deterministic fallback, `ai=False`); wiring a real model = external call/cost,
his call.
- **Tested: 31/31 pytest** (27 prior + 4 new `tests/test_decide.py`: all 10 looks reachable by a crafted
  scene, cinematic rule, LookChoice shape+clamping, AI-stub fallback). Verified `--look auto` end-to-end
  through `color.py` on real clips (derwin + source_clip01 -> both correctly `warm_interview`, the auto-pick
  is wired and could now select any of the 10). **Synced** dev `decide.py` -> standalone (identical).
- **Real-footage adversarial check (the widened brain is NOT dead code):** ran the auto-pick across 18
  real Luna stills (`OneDrive\A footage`). It fires the new looks when warranted — **moody_blue ×8** (the
  dark/cool night shots: brightness 0.08-0.18, negative warmth), **teal_orange ×2** (brighter cool),
  **warm_interview ×4** (the portraits, skin 0.13-0.52), neutral ×4 (dark low-signal). golden_hour/
  clean_pop/bleach_bypass/portra/fuji didn't fire on THIS batch (no bright/golden/gritty/foliage scenes
  in it) — correct gating, and the unit tests prove each is reachable on its signal.
- **Lookbook for the "pick favourites" gate:** all 10 looks rendered on the real talking-head over the new
  G1+G1b develop + density -> `out/ftest/_LOOKBOOK_10_2026-06-27.png` (source · develop · 10 looks, each
  with its optical stack). Eyeball it to set the `--look auto` favourites.
- **Elijah's "all four" (baton §3) are COMPLETE:** (1) look-stack VIDEO path, (2) scopes `--validate`,
  (3) G1b skin-LOCAL exposure, (4) auto-pilot widen. **Remaining open items are all his calls** (pick
  favourite looks for the auto defaults; wire the live AI look-picker; commit/sync). DWG working space
  DEFERRED (10-bit/HDR delivery).

---

## ✅ 2026-06-27 (cont.) — G1b SKIN-LOCAL EXPOSURE (color-qualifier lift) — built + verified — read this first

Baton §3 **item 3** (the "faces" axis). G1 nudges skin HUE to the I-line, but a GLOBAL exposure trim
can't lift genuinely under-exposed skin (~20 IRE on the interview clip) without lifting the whole
background — so it's capped tiny (≤6%). G1b fixes that: it lifts ONLY skin-CHROMATICITY colours, as a
smooth function of COLOUR (not pixel position) → a pure encoded RGB→RGB stage folded into `develop_fn`,
so it **bakes into the constant per-shot cube → flicker-free** and carries to still + video identically.
A spatial/keyed face mask would flicker frame-to-frame; the bakeable colour-qualifier is the baton's
explicit choice. **DRAFT — nothing committed/pushed/published.**

- **Code (`colorkit/correct.py`):** `_skin_qualifier_weight` (smooth C1 YCrCb-box membership + a
  **chroma gate** that rejects neutrals, which sit at the skin box's Cr≈128 edge and would else leak a
  lift) and `_apply_skin_lift` (membership-weighted encoded luma gain, hue-preserving) — both pure
  colour functions. `develop_fn` reads a top-level `skin_lift` gain and applies the stage after
  vibrance; absent/1.0 → the guard skips → **byte-identical** to before. Emitted by `_apply_skin_solve`
  ONLY when a real eroded-skin region is present AND skin is still below band (`p50 < 36 IRE`) after the
  global trim; capped at **+60%** (`_SKIN_LIFT_GAIN_CLAMP`), strength-scaled, aimed at 42 IRE. Reported
  in the `skin` diag as `skin_lift` + surfaced in the `_log_skin` line (`lift=…`).
- **Verified on REAL footage** (`derwin_test_track.mp4`, both CLIs): skin p50 **22.8→36.7** (shot 0) and
  **20.7→32.0** (shot 1) — `--validate`'s `skin_mid_ire` moved from deeply-failing (~19–23) up to ~32.
  The source skin is *genuinely* badly under-exposed, so the +60% cap gets it most of the way **without
  an artificial glowing face** (a deliberate, honest tradeoff — not cranked to force a green check).
  Visual proof `out/ftest/_G1b_skinlift_derwin.png` (source · develop skin-off · develop +G1+G1b): the
  face opens out of shadow while the **white shirt + dark background stay put** (selective qualifier).
- **No-op guarantee:** non-portrait / well-exposed-skin develops are byte-identical (the stage only
  exists when a lift gain is emitted). **Tested: 27/27 pytest** (23 prior + 4 new in
  `test_skin_solve.py`: triggers+raises, bakes-into-cube, qualifier bounded+selective, no-op on
  well-exposed skin). **Synced** dev `correct.py` → standalone (identical); `_log_skin` updated in both
  CLIs.
- **NEXT (last of Elijah's "all four", baton §3):** (4) auto-pilot — wire a real Claude-vision
  look-picker into `decide.suggest_look_ai` (opt-in, API-gated, deterministic fallback) + widen
  `--look auto` to all 10 looks (`decide.VALID_LOOKS` is the original 5). DWG working space DEFERRED.

---

## ✅ 2026-06-27 (cont.) — SCOPES `--validate` INTO THE RENDER (G2 correctness) — built + verified — read this first

Baton §3 **item 2**. The engine had the *ruler* (`colorkit/scopes.py::validate`, the demonstrated
scope targets) but never auto-ran it — so a grade was never *proven*. Now `--validate` makes every
grade **falsifiable**: it scores the DEVELOPED frame(s) against the targets, logs a per-shot verdict
(with the failing checks + value/target), and writes a `<stem>_validate.json` sidecar. **Advisory only
— it never alters a pixel or gates the render.** DRAFT — nothing committed/pushed/published.

- **What it validates:** the **developed** domain — post-correction, **PRE-creative-look**. The scope
  targets (black off-floor-not-milky, white in range, no clip, parade converged, skin on the ~123° I-line,
  skin 40-50 IRE) are *neutral-correction* targets; a creative look intentionally departs from neutral, so
  the look is NOT scored against them. STILL: the post-develop frame (captured before the look is applied).
  VIDEO: each shot's `corrected_rep` (already computed in PASS 1 — zero extra ffmpeg work).
- **Code:** `color.py` — `_validate_frame` (runs `scopes.validate(bgr, measure.skin_signature(bgr))`,
  exception-safe), `_log_validate` (one-line verdict + FAILING checks), `_write_validate_sidecar`
  (`<stem>_validate.json`). Wired into `process_image` (pre-look capture) + `process_video` (per-shot in
  PASS 1, sidecar assembled after concat). New CLI flag `--validate`. **Synced** to standalone
  `colorkit/colorkit/cli.py` (diff vs `color.py` = only the 5 package-vs-script line-pairs).
- **Sidecar shape:** `{input, mode, validated_domain, look, generated, [n_shots, n_validated, min_pass],
  results:[{shot, start, end, checks, n_pass, n_total, verdict, waveform, parade, clip, vectorscope}]}`.
  Locked JSON-serializable by a new test (no stray numpy scalars reach the file).
- **Verified on real footage** (outputs to scratch, not `out/`): STILL (derwin face frame, kodak look) →
  `7/7` + sidecar; **VIDEO** (`derwin_test_track.mp4`, 2 shots, teal_orange + optical) → per-shot `8/10`
  and `9/10`, sidecar `min_pass:8`. The validator **caught a real issue** — skin under-exposed at ~22 IRE
  (vs the 40-50 target) on both shots + crushed black on shot 0 — which is exactly the documented G1
  known-limit and **baton §3 item 3** (skin-LOCAL exposure). Falsifiable, not rubber-stamping. Standalone
  `python -m colorkit.cli` path runs identically.
- **Tested:** **23/23 pytest** (22 prior + 1 new `test_validate_output_is_json_serializable` in
  `colorkit/tests/test_scopes.py`, locking the sidecar contract). `py_compile` clean on both CLIs.
- **NEXT (remaining of Elijah's "all four", baton §3):** (3) skin-LOCAL exposure (color-qualifier lift,
  bakeable — the fix for the under-exposed skin `--validate` just surfaced); (4) auto-pilot (Claude-vision
  look-picker + widen `--look auto` to all 10). DWG working space still DEFERRED.

---

## ✅ 2026-06-27 — CINEMATIC LOOK-STACK **VIDEO PATH** (G3 cont.) — built + verified — read this first

The optical stack (halation/grain/vignette) now runs in the **per-shot ffmpeg filtergraph**, matching the
still path — so looks finally read as *film* (optical character), not flat tints, in rendered VIDEO too.
This was baton §3 item 1. **DRAFT — nothing committed/pushed/published.**

- **Code:** `colorkit/stylize.py` — new VIDEO surface: `optical_stack_plan` (resolves a look's stack →
  ordered `(effect, params)` with strength faded by look opacity, the SAME scaling the still uses),
  plate bakers `bake_grain_plate` / `bake_vignette_mask` (deterministic seeded plate / elliptical mask,
  baked ONCE at delivery res), and filtergraph-segment builders `ffmpeg_halation_segment` /
  `ffmpeg_grain_segment` / `ffmpeg_vignette_segment`. Wired into `color.py::process_video`: when the
  chosen look has a stack, the colour chain becomes the head of a `filter_complex`
  (`[0:v]<colour vf>[m0]`) and halation→grain→vignette layer on top AFTER the delivery scale; looped
  plate inputs + `-map`. **Color-only looks / no-look keep the plain `-vf` path → byte-identical.**
- **The three effects, masterclass-faithful + ffmpeg-robust:**
  - **Halation** = red-weighted highlight bloom **SCREENED in linear light**. Rewrote the research's
    broken graph cleanly: `setparams`(stamp bt709)→`zscale t=linear`→**all-float gbrpf32le** (an 8-bit
    intermediate poisons `blend`'s format negotiation and round-trips the base through ~2 code values)
    → squared soft-knee highlight mask on linear luma via `geq` (exact on float) + red-weight
    (`colorchannelmixer`) + `gblur` → `blend=screen` → back to bt709. The heavily-blurred glow is
    computed at **1/4 res** (`scale`+`scale2ref`) — visually identical, ~16× cheaper geq.
  - **Grain** = pre-baked **seeded STATIC plate** overlay on the LUMA plane (monochrome), shadow/mid
    weighted, chroma untouched. NEVER ffmpeg's temporal `noise` (= flicker).
  - **Vignette** = pre-baked elliptical **multiply mask** in RGB (identical smoothstep falloff to the
    still → exact `rgb*v`).
- **Verified on real footage** (proofs in `auto-clip/out/ftest/`):
  - **FLICKER-FREE proof (the headline):** rendered a STATIC input (one frame looped → zero source
    temporal variation); output frame-to-frame meanabs = **0.010** (just x264 quant) vs **12.3** for
    ffmpeg temporal `noise` — a ~1200× margin. Holds for the all-three-effects `portra` stack too.
  - **Still↔video parity:** kodak video vs still preview meanabs **2.73** (p95 6) — reads as the same
    grade (residual is the expected sRGB-vs-bt709 / FIR-vs-IIR preview gap; still is APPROXIMATE).
  - **All 7 stack shapes render:** kodak(hal+grain), teal(hal+vig), moody_blue(grain+vig), fuji(grain),
    warm_interview(hal), portra(all 3), clean_pop(color-only→-vf). Full pipeline (develop + **skin-solve
    G1** + look + optical) composes on the approved talking-head. Lookbook: `_VIDEOSTACK_lookbook.png`,
    parity: `_VIDEOSTACK_kodak_src_vid_still.png`.
- **3 bugs found+fixed during the build (all real, all verified):** (1) `-map` of a filter_complex
  label needs **brackets** (`[opt1]`) — bare label = "Invalid argument"; (2) looped-plate blends hang on
  **audio-less** clips (framesync `eof_action=repeat` → infinite video) — fixed with **`shortest=1`** on
  the grain/vignette blends; (3) zscale **"no path between colorspaces"** on unspecified-tag sources —
  fixed by **`setparams`** stamping bt709 before linearize (forced `tin=` hints alone don't cut it).
- **Tested:** 22/22 pytest (18 prior + 4 new in `colorkit/tests/test_look_stack.py`: plan/opacity-fade,
  plate determinism+size, vignette-mask edges, segment well-formedness). **Synced** dev tree
  (`auto-clip/colorkit/stylize.py` + `color.py`) → standalone (`colorkit/colorkit/stylize.py` + `cli.py`;
  diff = only the 4 package-vs-script lines).
- **Perf:** ~0.6× realtime on 1080p (was ~4× *slower* before the glow-downscale). Optical applies POST
  delivery-scale (so plates are small + reused; 8K → use `--height` for fast delivery).
- **NEXT (remaining of Elijah's "all four", baton §3):** (2) scopes `--validate` JSON sidecar into the
  render; (3) skin-LOCAL exposure (color-qualifier lift, bakeable); (4) auto-pilot (Claude-vision
  look-picker + widen `--look auto` to all 10). DWG working space still DEFERRED.

---

## ✅ 2026-06-26 — G1 SKIN-TONE-LINE SOLVER (built + verified) + Resolve HLG setup — read this first

**G1 (the P0 headline gap) is DONE.** The engine now has the *corrector* to match the *ruler*
(`measure.skin_signature`): a self-gating, capped, **global luma-preserving WB tint** that nudges skin
toward the ~123° I-line, folded straight into `wb_gains` (so it **bakes into the per-shot develop cube →
flicker-safe**, no new pipeline stage), plus a conservative **two-band skin-exposure trim**.

- **Code:** `colorkit/correct.py` — `_apply_skin_solve` + `_skin_mask` (eroded → coherent-region gate) +
  `_skin_angle_ire`, gated in `compute_correction(..., skin_solve=True)`. CLI: `--skin-solve auto|off`
  (default auto) in `color.py` + the standalone `colorkit/cli.py`. Synced to the standalone repo.
- **Verified on real footage** (`a test.mov`, the approved talking-head): skin hue **116.6°→120.7°**
  (drift −6.4°→−2.3°, **64% closer to the I-line**), exposure **byte-identical** (the tightened trim
  leaves the approved develop untouched), parade highlights *converged* (1.57→1.18), 0 clip, validate
  held 9/10. Video path end-to-end: 2 shots both pulled to ~120°, baked + flicker-safe. Montage:
  `out/ftest/_g1_talkinghead.png`.
- **Non-portrait = byte-identical** (the no-op guarantee): flat / scattered-warm-noise / a **real 8K HLG
  Luna sunset frame** all gate-off (eroded skin <8%) → develop unchanged. The mask **erosion** is what
  kills the YCrCb false-positive on warm/textured non-portrait footage.
- **Tested:** 13/13 pytest (9 prior + 4 new G1 tests: no-op-without-skin, erosion-rejects-scattered,
  never-worsens-I-line, JSON-safe diag).
- **Adversarially reviewed** (subagent): channel-order / no-op / measure-parity / determinism all
  confirmed correct; **3 fixes applied + re-verified** — (1) clamp-before-normalize so the tint is truly
  luma-preserving, (2) wrapped angular distance in the search score, (3) the skin exposure LIFT now
  respects the highlight-protection ceiling (can't re-inflate a protected bright background).
- **Known limit (surfaced, not hidden):** the talking-head's skin is genuinely under-exposed (~36 IRE);
  a *global* exposure trim can't fix that without lifting the background, so it's capped (≤6%) and the
  diag reports `skin_mid_ire` under-band rather than chasing it. A future skin-LOCAL exposure tool is the
  real fix. Defaults are **on/gated** — flipping the default to off is one constant if Elijah prefers.

**Resolve HLG setup (the "Both" path) DONE.** Adversarially-verified, primary-source research →
**`docs/resolve-hlg-luna-setup.md`** (single-CST recipe: Input Rec.2020 / **Rec.2100 HLG**, Output
**Rec.709 Gamma 2.2** for IG, Tone Map **DaVinci**, Gamut **Saturation Compression**, **OOTF off**; the
node tree from our methodology; **I-Log LUTs confirmed WRONG for this HLG footage**; rotation/8K/export).
The 10 looks staged as importable Resolve LUTs → **`colorkit/resolve-luts/`** (+ README: apply AFTER the
CST at ~70% Key Output Gain). Two verified traps: never RCM+CST tone-map together (double-map = wash); 2.2
not 2.4 for IG. Footage facts (ffprobe): 8K HLG arib-std-b67 / bt2020, rotation 90°, 29.97.

**Still DRAFT** — nothing committed/pushed/published.

### ✅ 2026-06-26 (cont.) — CINEMATIC LOOK-STACK (G3) — still path done + density baked in
Elijah: "the engine itself could be improved." Diagnosis (baseline lookbook): the looks read as *tints*,
not film — no optical character. Fix = a look is now **color cube + an ordered optical STACK**. Grounded
in a 2-lens adversarially-verified research workflow (effect recipes + DWG); go/no-go folded in.
- **Density (subtractive saturation) — BUILT, baked into the look cube** (`luts.py::_saturate` upgraded):
  for sat>1 it deepens in LINEAR light + darkens-with-chroma ("deepen not electrify") and **protects the
  skin hue band** (±30° of 123°). Because it's in the cube it's constant/flicker-safe and **carries to
  still AND video automatically**. Verified: `clean_pop` (density 1.16, no warm split) keeps skin at
  −1.2° (G1's line) → **density does NOT fight G1**; only intentionally-warm looks warm skin (kodak +8.5°,
  intended, within ±15° validator).
- **Optical stack (halation/grain/vignette) — BUILT, still path** (`stylize.py`): `apply_halation_image`
  (red-weighted highlight bloom, **Screen in linear**), `apply_grain_image` (**deterministic seeded
  static plate**, Overlay, shadow/mid-weighted — NOT ffmpeg's temporal noise = flicker), `apply_vignette_image`
  (feathered elliptical, encoded). A `LOOK_STACKS` registry maps each look → its effects; `apply_look_stack_image`
  walks `halation→grain→vignette`, scaling each by look-opacity. Wired into `color.py` + standalone `cli.py`
  still path. Looks with empty stacks (clean_pop, neutral) are byte-identical to before.
- **Verified visually** (proofs in `out/ftest/`): `_stack_lookbook.png` (all 10), `_stack_hero_{kodak,teal,moody}.png`
  (develop · color-only · +stack — halation glow + vignette clearly read). 18/18 pytest (+5 stack tests).
- **DWG working space → DEFERRED** (verify: marginal for 8-bit SDR delivery, high blast radius into the
  load-bearing luma path + G1). Revisit at 10-bit/HDR delivery.
- **NEXT (this build, remaining of Elijah's "all four"):** (a) wire the optical stack into the **VIDEO**
  ffmpeg filtergraph (halation graph needs a careful rewrite — still is an approximate preview vs the
  linear ffmpeg render); (b) **scopes `--validate`** into the render (G2); (c) **skin-LOCAL exposure**
  (color-qualifier lift, bakeable — fixes the under-exposed-skin G1 can't globally reach); (d) **auto-pilot**
  (correction robustness + a real Claude-vision look-picker, opt-in/API-gated) + widen `--look auto` to all 10.

---

## 🔬 2026-06-25 — DEEP frame-by-frame RE-ANALYSIS (in progress) — read this first

**Why:** Elijah pushed back — "is the color workflow actually finished? did you watch every frame vs
everything they said?" **Honest audit: NO.** The first masterclass pass (`acquire.py`) took **50 evenly-
spaced frames per video** (1 frame / ~2 min on the long ones; ~700 frames / 7.7 h) + a 15s-window
transcript, and never fused the two — so `synthesis.md` is strong *theory* but its numbers are textbook,
not read off the colorists' actual demonstrations.

**Fix built + running (DRAFT, local):**
- `docs/research/color-masterclass/acquire_dense.py` — 1 fps sample → dHash perceptual-dedup (keep only
  frames where the screen changed) → **word-level** transcript fusion. Ran on all 14: **2,498 distinct
  timestamped frames** (vs 700), each tied to what was said at that second. Frames are legible at
  parameter level (read EX→WB→LUT nodes + Contrast 1.104/Pivot 0.435/Offset 16.05 off one frame).
- `build_batches.py` → 130 vision-agent batch briefs.
- **Workflow `color-masterclass-deep` (run `wf_015b4b41-129`) DONE:** 123/130 batches (7 lost to a
  transient rate-limit — all 14 videos still represented), **1,363 frame-cited technique entries**,
  145 agents / ~9.7M tokens / 23 min. Persisted via `persist_results.py` →
  `extracted/synthesis_v2.md` (the demonstrated-evidence methodology), `extracted/engine_gap_map.(json|md)`
  (**17 techniques: 3×P0, 4×P1, 8×P2, 2×P3** + 5 self-flagged claims for human re-check), `per-video-v2/*.md`.
  It also **validated existing good colorkit calls** (linear 0.18 pivot is RIGHT not 0.435; look-under-
  grade @0.7; luma-safe `apply_to_luminance`; match-alpha 0.8).

**INTEGRATION STARTED — measurement layer (the ruler) DONE + tested (pure-additive, develop untouched):**
- **`colorkit/scopes.py`** (new, numpy-only): headless waveform/parade/vectorscope + clip stats + a
  `validate()` that asserts the demonstrated targets (black off 0 / diffuse white ~896 / no clip /
  parade converged / skin on the ~123° I-line / skin 40-50 IRE). Advisory, no pixel change.
- **`measure.skin_signature()`** (new): skin ROI hue angle vs the 123° I-line + IRE exposure + chroma.
- **Tested on the real talking-head (same frame, raw vs develop):** develop fixes milky blacks
  (13.8→2.6 IRE, 10/10 targets) **but drifts skin hue +7.7° further off the I-line (129.2°→136.9°)** —
  the P0 skin-solver gap, now demonstrated on real footage, not asserted.

**PACKAGED (runnable standalone, 2026-06-25):** the full working engine is copied to a self-contained,
ready-to-use project at **`ai agent team\colorkit\`** (for another agent to use). It has the current package
(13 modules incl. `scopes.py`), a packaged CLI (`colorkit/cli.py`), `run.py`, `pyproject.toml`, `README.md`,
10 looks + 6 input LUTs, and tests (9 pass). Run with the auto-clip venv: `cd colorkit; <venv>\python.exe -m
colorkit.cli <input> [--look NAME|auto]` → outputs to `colorkit\out\`. Verified end-to-end on a real still.
The hub copy (`auto-clip/colorkit/`) remains the dev tree where integration continues.

**The plan:** `docs/plans/2026-06-25-color-deep-analysis-integration.md`. **Next (G1, P0):** a skin-gated
correction stage in `correct.py` that nudges skin back toward the I-line (capped, never a hard snap) +
the two-band skin-exposure trim — verified by `scopes.validate` + before/after montages. Then P1
halation+grain (look=stack). Nothing committed/pushed/published.

---

## ☀️ MORNING SUMMARY (2026-06-24) — read this first

Two big things shipped overnight, both for you to review:

### 1) Color-grading MASTERCLASS (your new P0 request) — ✅ DONE
I deeply analyzed **14 of the best-reviewed DaVinci color-grading masterclasses** (Darren Mostyn ×4,
Cullen Kelly ×3, Mullins, Frenchie, film-emulation, etc.) by actually *watching* them — Gemini was
quota-blocked (`limit:0`), so I built a local pipeline (yt-dlp captions + 720p → ffmpeg frames → 14
vision agents read every transcript + ~25 on-screen frames each, reading the real UI/scopes/node-trees).
- **Read it here:** the zero-to-hero teaching guide in your vault →
  `40-Projects/LarpSlop/Color-Grading-Masterclass/` (**12 chapters + a one-page cheat sheet + 95
  screenshots**; start at "00 - … (index)"). It's written to be sellable + to teach you to grade by hand.
- **Engine-facing distillation:** `docs/research/color-masterclass/COLOR-GRADING-METHODOLOGY.md` +
  `CONSENSUS.md` (15 universal truths, the canonical workflow, scope targets, the disputes-as-knobs).
- The agent now *remembers* this (memory: `reference-color-grading-method`).

### 2) Color engine v2 — ✅ Mission A (quality) + Mission B (own repo) DONE
- **The washed look is fixed.** Rewrote correction as a linear-light **"develop"**: median→18% grey
  exposure (no more over-bright), per-channel black point (**true blacks 0.001 vs v1's milky 0.078**), a
  **filmic highlight soft-clip** (no clipping), luma-safe vibrance. For Log footage it now applies your
  **Insta360 I-Log→Rec709 LUT first** (restores ~2× saturation). Looks now run **UNDER** the grade at
  0.7 opacity (tasteful, not a filter) and were rebuilt to stop double-contrast.
  Proof to eyeball: `auto-clip/out/ftest/_L_lookbook07b.png` (src · develop · warm · teal · kodak · fuji).
- **Extracted to its own repo:** **`C:\Users\elija\OneDrive\Desktop\colorkit`** — clean package, pyproject
  (`pip install -e .` → a `colorkit` command), README, **MIT** LICENSE, pytest (5/5 pass), **local commit
  only, NOT pushed**. The hub copy is untouched.

### ⚑ Your calls (gates)
- **Repo name** = I proposed **`colorkit`**; rename if you want. **Pushing it anywhere is your call.**
- Commit the hub's v2 changes? · The old **Gemini key** is still quota-dead — needs a paid/working key
  for any future Gemini video work (I routed around it this time).
- **Stretch goals (task #8) — ✅ DONE this session (2026-06-24 cont.):** HLG/HDR tonemap stage, GPU
  `-hwaccel` decode for 8K, and the AI "pick-the-look" decision layer. Details in the next section ↓.

---

---

## 🎯 TASK #8 — STRETCH GOALS DONE (2026-06-24, continued) — read this first

All three stretch goals built + **tested on your real footage**, DRAFT-only, in the **hub copy**
(`auto-clip/colorkit/`). The standalone `Desktop\colorkit` repo is untouched (NOT diverged, per your note).
Three new modules + small wiring; no production engine behaviour changed for SDR clips (the new stages are
no-ops unless an HDR source / `--look auto` / large 8K file is in play).

### 8a · HLG/HDR → SDR tonemap stage (`colorkit/hdr.py`) ✅
- **What:** detects HLG (`arib-std-b67`/bt2020) & PQ (`smpte2084`) sources via ffprobe and inserts a
  **Stage -1** HDR→Rec.709 SDR tonemap as the FIRST per-shot filter — applied identically to the
  representative frame so the develop measures the right (SDR) signal. Without it, your HLG clips grade
  **washed/milky** (HDR code values shown as SDR).
- **Engines:** default **zscale + `tonemap=hable`** (CPU, deterministic, zero GPU dep); `mobius`/`reinhard`
  operators; and **`placebo`** = libplacebo **BT.2390** (Vulkan GPU, richest) as an opt-in. Flag:
  `--hdr-tonemap auto|hable|mobius|reinhard|placebo|none` (default `auto`). No-op on SDR.
- **Tested:** found your 4 HLG clips (4K bt2020). Daytime montage `out/ftest/hdr/_HLG_daytime_full.png`
  (naive→tonemap→+develop→+teal_orange) shows the wash fixed, deep blacks, clouds retained, designed look.
  Full video ran end-to-end → `out/VID_20260621_000318_003_graded.mp4`. (The dark-night over-warm noted
  here originally is now **fixed** — see "Develop hardening" below.)

### 8b · GPU `-hwaccel` decode for 8K (`colorkit/accel.py`) ✅
- **What:** optional hardware **decode-only** (`-hwaccel`, no `-hwaccel_output_format`) — frames decode on
  the GPU, auto-download to CPU for the existing lut3d filters (no GPU-filter variants, no pixel change).
  Picks a working accelerator **validated on the real file** (decodes 1 frame first), with a **per-shot
  software-fallback** retry. Flag: `--hwaccel auto|cuda|qsv|d3d11va|none` (default `auto`).
- **Measured (RTX 5070, NVDEC):** pure 8K HEVC decode **7.7s → 1.9s (4×)**; full pipeline on a 9.8s 8K clip
  **107.7s → 91.0s (~15% e2e)** — the rest is the (unaccelerated) signalstats probe + scenedetect + x264
  encode. **NVENC tested and REJECTED:** h264_nvenc 7.8s vs libx264 7.9s (identical — pipeline is
  *decode-bound*, not encode-bound) but NVENC made a **79% bigger file**. So GPU *decode* is the right lever;
  encoder stays libx264. (Further e2e wins would need accelerating the probe/scenedetect — future.)

### 8c · AI "pick-the-look" decision layer (`colorkit/decide.py` + `measure.scene_stats`) ✅ (sketch + working brain)
- **What ships now:** a **deterministic brain** — `measure.scene_stats` reads 6 cheap signals
  (skin/foliage/warmth/saturation/brightness/contrast) and `decide.suggest_look` maps them to a look
  (skin→`warm_interview`, foliage→`fuji_style`, warm→`kodak_2383_style`, cool/cinematic→`teal_orange`,
  else `neutral_correct`). Wired as **`--look auto`** (rep frame is HDR-tonemapped / I-Log-developed first).
- **The AI brain is a SKETCH** (`decide.suggest_look_ai` stub → falls back to deterministic): design in
  `docs/plans/2026-06-24-color-ai-decision-layer.md` (providers in hub-preference order: a Claude vision
  **agent** = "Claude IS the brain", TwelveLabs **Pegasus**, then Gemini when its key is live). Wiring a real
  model is **Elijah-gated** (external call/cost).
- **Tested:** real talking-head (`a test.mov`) → `warm_interview`; cool still → `teal_orange`; `--look auto`
  runs end-to-end. Known limit (documented): YCrCb skin fires on warm surfaces (tan asphalt) → that's exactly
  what the AI brain upgrades; the deterministic brain stays *conservative* (safe flattering default).

### Develop hardening — dark / mixed-light scenes (2026-06-24, continued) ✅
The one real quality issue task #8 surfaced (the night-driving clip went **green-yellow**: auto-WB
over-warmed mixed artificial light + exposure slammed its 4.0× ceiling) is now fixed in `correct.py`,
**gated so the well-exposed v2 look you approved is byte-identical** (regression-checked: 0-pixel diff
on the daytime develop). Two automatic guards engage ONLY when a scene *demands a large lift* (i.e. it's
genuinely dark):
- **Exposure soft-knee** — lifts ≤2× are untouched; above that the lift rolls off toward ~3.2× instead
  of hard-clamping at 4× (no more dark-scene blowout). Night clip: 4.0× → 2.93×.
- **Low-light WB fade** — gray-world WB is unreliable on dark/mixed light, so it fades toward neutral as
  the demanded lift grows (full strength on normal scenes). Night clip: blue-gain 0.70 → 0.85 (much less
  over-warm). Proof: `out/ftest/hdr/_NIGHT_develop_fix.png` (tonemap | OLD | NEW | NEW+strength0.5).
- **New `--strength S` knob** (0..1, default 1.0=unchanged) — a manual dial that scales the *whole*
  develop (WB/exposure/black/contrast/vibrance) toward identity for footage where auto reads too strong.
  Independent of the automatic guards. Verified end-to-end.

### Fresh film looks + lookbook (2026-06-24, continued) ✅
Added **5 new looks** (now **10 total**), each designed in the v2 idiom (the develop owns exposure +
contrast, so a look carries HUE + DENSITY character, runs UNDER the grade at 0.7 — tasteful, not a filter):
- **`golden_hour`** — warm aspirational amber glow (lifestyle / faith / motivational).
- **`moody_blue`** — cool cinematic teal-blue (night b-roll / driving / moody talking-head; the complement
  to the warm looks — fits your night footage).
- **`bleach_bypass`** — gritty silver-retention, heavily desaturated (dramatic).
- **`clean_pop`** — bright punchy neutral-white commercial (product / ad / IG).
- **`portra_style`** — soft pastel film, creamy toe, warm-pink skin (gentle portrait alternative).

All regenerated as `.cube`s and verified end-to-end. **Pick favorites here:** the full menu on a
talking-head frame → `out/ftest/hdr/_LOOKBOOK_v2.png` (12 tiles: source · develop · all 10 looks); the 5
new ones larger → `out/ftest/hdr/_LOOKBOOK_new5.png`. The new looks are **manual-select** (`--look NAME`);
the auto-picker (`--look auto`) still uses the curated original 5 — widening it is a small follow-up.

### ⚑ Your calls / notes
- **Adversarial 4-lens review run (no critical issues; architecture confirmed sound)** → folded in **6
  fixes**, all re-verified: (1) guarded the PASS-1 rep-frame grab with a software fallback — the one real
  robustness hole (it could have crashed a run before the existing fallback engaged); (2) `--look auto` now
  honors `--hdr-tonemap` so the look is *chosen* on the same signal it's *graded onto* (parity — proven: the
  auto vs none measurements now correctly differ); (3) clear the I-Log LUT on ANY HDR source (not just when
  tonemapping); (4) hwaccel list cached only when non-empty (no permanent disable on a transient probe miss);
  (5) whitelist the zscale input-matrix tag (odd tags → bt2020nc); (6) copy-before-mutate in `suggest_look_ai`.
- Nothing committed/pushed; all outputs in `out/` only. To eyeball: `out/ftest/hdr/_HLG_*.png`.
- These live ONLY in the hub copy; say the word to sync them into the `Desktop\colorkit` standalone repo.

---

## ⚡ 2026-06-24 v2 PROGRESS (overnight) — read this first

**Pivot mid-run (Elijah's new P0):** before finishing the v2 engine, *deeply analyze the best
YouTube DaVinci color-grading masterclasses* (watch visuals, not just transcripts), build a durable
zero-to-hero grading guide in the Obsidian vault + engine MD + memory, THEN resume the v2 build.
Driver: this file + `docs/plans/2026-06-24-color-v2-grading-spec.md`.

**MISSION A v2 = ✅ COMPLETE + VISUALLY VERIFIED (2026-06-24).** Develop + I-Log input transform +
**look opacity (run looks UNDER the grade at 0.7, the masterclass's "tasteful not filter" lever)** +
**rebuilt looks** (dialed out contrast-stacking; looks now carry hue/density character, not extra
contrast). Lookbook on the talking-head (`out/ftest/_L_lookbook07b.png`) confirms: develop kills the
milky wash (deep blacks, clean whites, healthy skin); warm/teal/kodak/fuji at 0.7 each read as a
*designed* grade, restrained, not filter-y. Video opacity path validated (baked opacity-cube matches the
still blend to <1 level). Skin-line AUTO-rotation deferred as a documented knob (disputed in the
research — Kelly/Mullins reject the hard target; never-key-skin; consistency > exact angle — so a forced
auto-rotation is risky on non-portrait content; the warm look already nudges skin warm). **Next: Mission B
(extract to own repo).**

**v2 engine work already DONE + TESTED this run (solid, keep):**
- ✅ **v2 spec** written: `docs/plans/2026-06-24-color-v2-grading-spec.md` (synthesized from the
  verified `pro-grade-craft-research` lanes; the workflow's final synth agent had been interrupted).
- ✅ **`colorkit/tonemap.py`** (new): linear-light transfer fns (sRGB EOTF/OETF), C1 highlight
  soft-clip (default shoulder), ACES-Narkowicz/Hable/Reinhard alternatives, pivoted contrast. Unit-tested.
- ✅ **`colorkit/correct.py` rewritten = v2 "develop"**: linearize → Shades-of-Gray WB → per-channel
  black point (percentile) → exposure = **median→0.18** (not mean) → ONE gentle pivoted contrast on
  luma → highlight soft-clip → encode → vibrance. Emitted as a pure `develop_fn`; baked to a constant
  per-shot `.cube` (`bake_develop_cube`) for the flicker-free video apply. Removed the old
  `ffmpeg_correction_filter` (eq/colorchannelmixer linear-stretch — the washed-look cause).
- ✅ **`color.py`**: video route now bakes+applies the develop cube via `lut3d`; **`--input-lut`**
  added (auto-detects I-Log by filename → applies the official Insta360 Rec709 BT1886 s65 LUT FIRST).
- ✅ **`__init__.py`** updated (tonemap exports, develop_fn/bake_develop_cube).
- ✅ **Tested on real footage** (proofs in `out/ftest/`): photo, talking-head still+video (baked cube
  matches still), and **I-Log 8K frame**. Scope wins vs v1: blacks 0.001 (true) vs v1 milky 0.078;
  median lands on the 0.46 mid-grey target; **I-Log input-LUT restores ~2× saturation (0.176 vs generic
  0.088) + proper highlight range** — the camera-correct develop. No hard clipping (soft-knee works).

**v2 still TODO (resume AFTER the masterclass research):** color-theory skin-line + scope-driven
vibrance (task#4) · rebuild the 5 looks on the balanced base + look opacity 0.6–0.8 (task#5) · full
v1-vs-v2 montages on all footage (task#6) · extract to own repo (task#7) · stretch (task#8).

**✅ MASTERCLASS RESEARCH DONE (2026-06-24) — grounds the engine.** Deeply analyzed 14 best-reviewed
DaVinci masterclasses (Mostyn ×4, Cullen Kelly ×3, Mullins, Frenchie, film-emulation, etc.) by *watching*
them (yt-dlp + ffmpeg frames + 14 vision agents; Gemini quota-blocked). Outputs:
`docs/research/color-masterclass/{COLOR-GRADING-METHODOLOGY.md, CONSENSUS.md, per-video/*.md}` + a 12-chapter
zero-to-hero guide in the vault (`40-Projects/LarpSlop/Color-Grading-Masterclass/`, 95 screenshots) + memory
(`reference-color-grading-method`, `project-color-engine`). **Consensus VALIDATES v2** (color-mgmt-first/CST
sandwich = our `--input-lut`; exposure→mid-grey = our median→0.18; luma-safe sat = our vibrance; pivot
0.435 Rec709 ≈ our 0.18 linear). **New for the engine:** (a) skin = consistency on the ~123° vectorscope
line, fix GLOBALLY never key (task#4); (b) look = stacked effects run UNDER at ~50% mix (task#5 opacity);
(c) print LUTs need LOG input (our looks stay honest `_style` approximations); (d) tetrahedral interp ✓
already; (e) future: grade in a wider working space (DWG/OCIO) than linear-Rec709.

---

## What this is
Our own headless Python+FFmpeg color engine: auto color-correction (WB/exposure/contrast) + stylized grading
(film LUTs, split-tone, teal-orange) for stills and multi-scene video. No DaVinci Studio. Slots into `auto-clip`
as `color.py` (after `tighten`, before `caption`). Fork-and-extend of `perbhat/agentic-color-grader` patterns +
our two missing pieces (single-file per-shot anti-flicker segmentation + creative stylize layer).

## Build phases (autonomous loop)
- [x] **P0 — Deps:** ✅ venv at `auto-clip/.venv` (Python 3.12.10) with opencv-contrib-python 4.13, numpy 2.5, scikit-image 0.26, colour-science 0.4.7, scenedetect 0.7 — all permissive (Apache/BSD).
- [x] **P1 — Core modules:** ✅ all 9 files authored, adversarially reviewed, fixed (critical R/B LUT-order bug + gamma-sign bug caught & fixed), LUTs regenerated.
- [x] **P1 — Still proof:** ✅ VERIFIED end-to-end on a real frame (`source_clip01`): WB-neutralized a magenta cast, applied teal_orange correctly oriented (no channel swap), before/after in `out/`. cv2/colour/skimage import in 0.8s (no OneDrive hang).
- [x] **P1 — Film LUTs:** ✅ 5 `.cube` looks generated (neutral_correct, warm_interview, teal_orange, kodak_2383_style, fuji_style), regenerated after the R/B-order fix.
- [x] **P1 — Review + fix:** ✅ 4 adversarial lenses; critical R/B LUT-order + major gamma-sign + WB still/video-parity bugs caught and fixed.
- [x] **P2 — Smoke test (still):** ✅ verified on a real interview frame — warm cinematic grade, healthy skin, before/after in `out/`.
- [x] **P2 — Video leap:** ✅ VERIFIED on a 3-scene clip: segmented into 3 shots, 3 DIFFERENT per-shot constant corrections (anti-flicker), concat → graded mp4.
- [x] **P2 — Shot-match:** ✅ Stage 2 working — hero shot picked, per-shot match LUTs baked, order correct (correct→match→stylize). Also fixed an ffmpeg Windows lut3d path bug (cwd workaround).
- [x] **P3 — Docs + integration + cleanup + handoff** ✅: `colorkit/README.md`, `colorkit/INTEGRATION.md` (opt-in wiring proposal), `requirements.txt` updated, `auto-clip/README.md` updated, scratch removed. Adversarial review of the ffmpeg-cwd fix caught 2 robustness gaps (unguarded copy; silent path-strip) — both FIXED + re-verified.

## How to run it (when you're back)
```
# still:
auto-clip\.venv\Scripts\python.exe auto-clip\color.py <image> --look teal_orange
# video:
auto-clip\.venv\Scripts\python.exe auto-clip\color.py <video.mp4> --look kodak_2383_style
# outputs land in auto-clip\out\ as before/after — nothing is published.
```

## Test media (real footage, all 1080×1920)
- `source.mp4` — 6 min, HEVC 30fps → multi-scene flicker/segmentation test.
- `auto-clip/out/source_clip01.mp4` — 24s H.264 → still smoke-test frame + fast single-clip pass.
- `auto-clip/out/derwin_test_track.mp4` — 20s interview → secondary test.

## Status log
- 2026-06-23 — Build initialized: deps installing, Phase-1 build workflow launched.
- 2026-06-23 — P0 deps ✅ installed clean. First Phase-1 launch failed on a script bug (my regex); relaunched corrected (`wf_b10c6487-49d`). Test footage profiled.
- 2026-06-23 — **BUILD COMPLETE.** Engine authored + reviewed + fixed, LUTs generated, all paths VERIFIED on real footage, docs written, fix hardened + re-verified. Autonomous run finished here.
- 2026-06-24 — **v2 quality overhaul + own-repo extraction + masterclass research** done (see sections above).
- 2026-06-24 (cont.) — **TASK #8 STRETCH GOALS done:** HDR tonemap (`hdr.py`), GPU hwaccel decode (`accel.py`),
  AI decision layer (`decide.py` + `measure.scene_stats`, `--look auto`). New CLI: `--hdr-tonemap`,
  `--hwaccel`, `--look auto`. Validated on real HLG (day+night) + 8K footage; NVENC tested & rejected;
  adversarial 4-lens review run (no critical issues) → 6 fixes folded in & re-verified. Hub copy only;
  standalone repo NOT diverged.

---

## FINAL HANDOFF (2026-06-23)

**Status: the agentic color engine is BUILT, VERIFIED, DOCUMENTED — and DRAFT (uncommitted, never published).**

### How to run (from anywhere; use the venv python)
```
# still:  before/after PNGs in out/
auto-clip\.venv\Scripts\python.exe auto-clip\color.py <image.png> --look warm_interview
# video:  graded mp4 in out/ (auto shot-detect + per-shot constant correction)
auto-clip\.venv\Scripts\python.exe auto-clip\color.py <clip.mp4> --look teal_orange --match
# correction only (no look): drop --look   ·   looks: neutral_correct warm_interview teal_orange kodak_2383_style fuji_style
```

### Verified (all on YOUR real footage)
- Stills (interview frame: warm grade, healthy skin, no channel swap) · single-clip video · **multi-scene video** (3 shots → 3 distinct per-shot constant corrections [anti-flicker] → shot-match → look → concat) · all 5 LUTs render correctly · regression after the robustness hardening.

### Review these in `auto-clip/out/`
- `_elijah_compare.png` (before/after) · `_lookbook.png` (5-look menu) · `_multishot_test_graded.mp4` (multi-scene proof) · `source_clip01_graded.mp4` (single-clip).

### Code
- `auto-clip/color.py` (CLI) + `auto-clip/colorkit/` (io_utils, measure, correct, stylize, segment, match, luts) + `auto-clip/colorkit/luts/*.cube` (5 looks) + `colorkit/README.md` + `colorkit/INTEGRATION.md`.

### NOT done / open for Elijah
1. **Not committed** — left in the working tree for your review (your call to commit).
2. **Not wired into the auto-clip skill** — it's an opt-in proposal in `colorkit/INTEGRATION.md` (slots after `tighten`, before `caption`); enabling it is an Elijah-gated edit to SKILL.md.
3. **`warm_interview` runs a touch warm on backgrounds** — intensity is a one-number tunable (`amount=` in `luts.py`); say the word and I'll dial it.
4. **Untested:** the `--deflicker` backstop, a full 6-min `source.mp4` run, and there's no pytest yet.
5. **Shot-match quality** is good (Reinhard-to-hero), not Resolve-Color-Match-grade — a known ceiling from the prior-art research; bridgeable later.
6. **Pick a favorite look** (look book) — I can also author more film looks (you chose "fresh film looks" earlier).

---

## FOOTAGE VALIDATION (2026-06-24) — tested on real Luna Ultra footage (`OneDrive\A footage`)

Ran the engine across diverse real footage. Results (proofs in `auto-clip/out/ftest/`):
- **Photos (JPG)** ✅ — night Audi photo: correction + warm look → warmer, punchier, richer sky (`photo_compare.png`).
- **Normal video (`a test.mov`, 1080×1920)** ✅ — found 2 shots, per-shot constant correction + shot-match, cinematic talking-head result (`mov_compare.png`). Contrast runs a touch strong (tunable).
- **I-Log 8K** ✅ — the generic gray-world WB + contrast-normalize **develops flat Log footage well** (flat/milky → natural contrast, deep blacks) even WITHOUT a dedicated Log→709 LUT (`ilog_compare.png`).
- **HLG HDR (4K, bt2020/arib-std-b67)** ⚠️ — works (decoded as SDR), fine on dark scenes; **no proper HDR tone-mapping**, so bright HLG scenes would wash. Enhancement candidate.
- **8K video** ✅ via the **NEW `--height` flag** — decode 8K → grade → downscale → encode. `VID_…026` (8K, shot vertical w/ rotation flag) → clean **1080×1920 IG-ready** file, rotation handled automatically. ~100s for a 9.8s clip (8K *decode* is the bottleneck, not the grade); without `--height`, 8K→8K encode is impractical.

### NEW FEATURE added + tested this session
- **`--height N`** — delivery downscale (preserve aspect, even width; never upscales). Applied LAST in the per-shot filtergraph (video) and on write (stills). **Essential for the 8K camera** (`--height 1920` → IG-ready). Verified on real 8K.

### Improvement backlog (from footage testing)
1. **I-Log input transform — OFFICIAL LUTs NOW IN HAND** ✅ (2026-06-24) Elijah provided the Insta360 Luna packs → copied to `colorkit/input_luts/`: `Luna_I-Log_to_Rec709_BT1886_s33/s65` (SDR/IG — **the one to use**), plus HLG + St2084 (HDR, future). **v2 plan:** for I-Log footage, auto-apply the Rec709 BT1886 LUT as the FIRST step (input transform) BEFORE correction — the camera-accurate develop, far better than the generic gray-world. Use s65 for quality, s33 for speed. (Detect I-Log via filename/flag or a `--input-lut` arg.)
2. ✅ **DONE (task #8a, 2026-06-24)** **HLG/HDR tonemap stage** — `colorkit/hdr.py` detects
   `arib-std-b67`/`smpte2084`/bt2020 → zscale+tonemap (or libplacebo) to SDR Rec.709 as Stage -1.
   `--hdr-tonemap`. Tested on the 4 HLG clips.
3. ✅ **DONE (task #8b, 2026-06-24)** **GPU/hwaccel decode for 8K** — `colorkit/accel.py`, decode-only
   `-hwaccel` with on-source validation + SW fallback. `--hwaccel`. 4× decode (7.7→1.9s); NVENC tested &
   rejected (decode-bound, bigger files). No torch needed (NVDEC is in the ffmpeg build).
4. ✅ **DONE (task #8c, 2026-06-24)** **Auto-pick the look** — deterministic brain
   (`colorkit/decide.py` + `measure.scene_stats`) wired as `--look auto`; AI brain sketched
   (`suggest_look_ai` stub + design doc, Elijah-gated). Non-portrait clips no longer default to a skin look.
5. **Default correction contrast** is slightly strong on some content — consider a gentler default or a `--strength` knob. (Low.)
