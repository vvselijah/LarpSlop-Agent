# SESSION-COMPACT — 2026-06-26 (G1 skin solver + Resolve HLG setup)

**READ THIS on resume.** This session executed the **"Both"** path from the prior baton
(`SESSION-COMPACT-2026-06-26.md`): **(1)** set up DaVinci Resolve for Elijah's HLG Luna footage, and
**(2)** built the engine's **G1 skin-tone-line solver** (the P0 headline gap). Live tracker:
`auto-clip/COLOR-BUILD-STATUS.md` (2026-06-26 section). Memory: `[[project-color-engine]]`.
**DRAFT throughout — nothing committed, nothing pushed, nothing published.**

---

## 1. WHAT THIS SESSION DID (done + verified)

### A) Engine G1 — the skin-tone-line solver (P0, the headline) — DONE
The engine had the *ruler* (`measure.skin_signature`) but not the *corrector*. Now it does.
- **`colorkit/correct.py`** — `_apply_skin_solve` + `_skin_mask` + `_skin_angle_ire` + `_downscale_rgb`,
  gated in `compute_correction(..., skin_solve=True, skin_offset=0.0)`. It develops a downscaled rep,
  masks skin (YCrCb **eroded** → coherent region only), and if skin is real (≥8%) and off the line,
  searches a small **luma-preserving, capped WB tint** (green↔magenta × warm↔cool grid) that moves skin
  toward the ~123° I-line, **folds it into `wb_gains`** (so it bakes into the per-shot develop cube →
  flicker-safe, no new stage), then a conservative **two-band skin-exposure trim** (only fires clearly
  out of band, ±6%, and **respects the highlight-protection ceiling**). Global, never a skin key.
- **CLI:** `--skin-solve auto|off` (default `auto`) in `auto-clip/color.py` + standalone `colorkit/cli.py`;
  per-shot `skin-solve:` log line via `_log_skin`.
- **Verified (real footage, `a test.mov` = the approved talking-head):** skin hue **116.6°→120.7°**
  (drift −6.4°→−2.3°, **64% closer to the I-line**), exposure **byte-identical**, parade highlights
  *converged* (1.57→1.18), 0 clip, validate held **9/10**. Video path: 2 shots both pulled to ~120°,
  baked + flicker-safe (montage `auto-clip/out/ftest/_g1_talkinghead.png`).
- **No-op guarantee proven:** flat / scattered-warm-noise / **a real 8K HLG Luna sunset frame** all gate
  off (eroded skin <8%) → develop byte-identical. The mask erosion kills the YCrCb false-positive.
- **Tested:** 13/13 pytest (9 prior + 4 new in `colorkit/tests/test_skin_solve.py`).
- **Adversarially reviewed** (subagent): channel-order / no-op / measure-parity / determinism all CORRECT;
  **3 fixes applied + re-verified** — clamp-before-normalize (true luma-preserve), wrapped-angle score,
  exposure-lift respects the highlight ceiling.
- **Synced** dev tree (`auto-clip/colorkit/`) → hub-root standalone (`colorkit/`). ⚠️ NOT synced to the
  *older* git repo `C:\Users\elija\OneDrive\Desktop\colorkit` (the 2026-06-24 extraction) — separate thing.

### B) Resolve HLG setup ("Both" path) — DONE
Footage facts (my ffprobe): **8K (7680×4320) 10-bit HEVC, HLG `arib-std-b67` / `bt2020`, rotation 90°,
29.97** — HDR even in "Standard" mode (that's why it graded washed).
- **Guide:** `docs/resolve-hlg-luna-setup.md` — adversarially-verified, primary-source (BMD manual +
  forum) via a background Workflow. **Single-CST recipe** (recommended): Input **Rec.2020 / Rec.2100 HLG**,
  Output **Rec.709 Gamma 2.2** (for IG), Tone Map **DaVinci**, Gamut **Saturation Compression**, **OOTF
  off**; the node tree mapped from our masterclass method (CST → balance-to-parade → pivoted contrast →
  skin-to-I-line by eye → look LUT under @70%); RCM alternative; rotation/8K-proxy/export.
- **10 looks → Resolve LUTs:** `colorkit/resolve-luts/` (+ README). Apply **AFTER** the CST, on Rec.709
  pixels, at **~70% Key Output Gain**.
- **Two verified traps:** (1) never run RCM tone-map AND a CST tone-map together (double-map = wash);
  (2) **2.2 not 2.4** for IG (phone-test). **I-Log LUTs CONFIRMED WRONG for this HLG footage** (their
  header reads "Insta360 I-Log to Rec709"; input is I-Log, footage is HLG) — incl. the `_to_Rec2020_HLG`
  variant.

---

### C) Cinematic look-stack (G3) — still path DONE + density baked in (2026-06-26 cont.)
Elijah: "the engine itself could still be improved." He chose **all four** quality axes (look-stack /
auto-pilot / faces / correctness). Sequenced by impact+safety; this session delivered the first + the
safe parts of the rest. Grounded in a 2-lens adversarially-verified research workflow (effect recipes +
DWG), go/no-go folded in. Full detail: `auto-clip/COLOR-BUILD-STATUS.md` (2026-06-26 cont. section).
- **Density (subtractive saturation) — BUILT, baked into the look cube** (`luts.py::_saturate`): sat>1
  deepens in LINEAR + darkens-with-chroma ("deepen not electrify"), **skin-band protected**. In the cube →
  flicker-safe, carries to still AND video. Verified it does NOT fight G1 (clean_pop density 1.16 keeps
  skin at −1.2°; only warm looks warm skin, intended).
- **Optical stack (halation/grain/vignette) — BUILT, STILL path** (`stylize.py`: `apply_halation_image`
  [Screen in linear], `apply_grain_image` [deterministic seeded plate — NOT ffmpeg temporal noise],
  `apply_vignette_image`; `LOOK_STACKS` registry + `apply_look_stack_image`). Wired into `color.py` +
  standalone `cli.py` still path. Color-only looks (clean_pop/neutral) byte-identical. 18/18 pytest
  (+5 stack tests). Proofs: `out/ftest/_stack_lookbook.png`, `_stack_hero_{kodak,teal,moody}.png`.
- **DWG working space — DEFERRED** (verify: marginal for 8-bit SDR, high blast radius into luma path + G1).
- Synced to standalone (`colorkit/`); Resolve LUT export `colorkit/resolve-luts/` refreshed with density.

## 2. PENDING ELIJAH (decisions / gates)
- **G1 default:** it's **on (auto)/gated** — i.e. portrait develops now include the skin nudge. Eyeball
  `out/ftest/_g1_talkinghead.png`; if you'd rather it be opt-in, flipping the default to off is one
  constant (`--skin-solve auto|off` already exists either way).
- **Resolve:** want me to actually drive Resolve (computer-use) to build the node tree / save it as a
  PowerGrade, or is the written guide enough? Also: pick the single-CST vs full-RCM path.
- **Pick favorite looks** → set as `--look auto` defaults (still pending from prior batons).
- **Commit/sync?** Everything DRAFT/uncommitted; the hub-root `colorkit/` is local-only (not pushed); the
  older `Desktop\colorkit` git repo does NOT have G1.

## 3. NEXT — finish Elijah's "all four" (resume here; research already done — see workflow results below)
The quality research (`colorkit-quality-research`, run `wf_3dbfcfdb-3f5`) gave linear-correct recipes +
adversarial go/no-go. Remaining, in order:
1. **Look-stack VIDEO path** (G3 cont.): wire halation/grain/vignette into the per-shot ffmpeg filtergraph
   in `color.py` (after the look cube, in order). The research's literal halation ffmpeg graph is BROKEN
   (8-bit knee in a float-linear segment, self-referential geq) — REWRITE it cleanly (linearize via
   zscale t=linear, gblur, blend=screen, back to bt709). Grain = overlay a PRE-BAKED seeded plate file
   (stage it like the look cube; bare-filename/cwd), NEVER `noise` with the temporal flag. Vignette = the
   geq elliptical form (match the still). Verify flicker-free on a real clip (the still is only an
   APPROXIMATE preview — gblur IIR ≠ cv2 FIR).
2. **Scopes `--validate` into the render** (correctness): `scopes.validate` exists but isn't auto-run; add a
   `--validate` JSON sidecar + per-shot verdict log in `color.py`. Cheap, makes every grade falsifiable.
3. **Skin-LOCAL exposure** (faces): the under-exposed-skin G1 can't globally lift. Do it as a **skin-COLOR-
   qualifier** lift (bakeable into a constant cube → flicker-safe, NOT a spatial/keyed mask), gated like G1,
   reuse `correct._skin_mask`/`_skin_angle_ire` so it agrees with G1.
4. **Auto-pilot** (smarter): harden auto-correction edge cases; wire a real **Claude-vision look-picker**
   into `decide.suggest_look_ai` (opt-in, API-gated, falls back to deterministic); widen `--look auto` to
   all 10 looks (currently `decide.VALID_LOOKS` = original 5).
- DWG working space = DEFERRED (revisit at 10-bit/HDR delivery).
- Research completion (~52 more masterclass videos) = a DIFFERENT conversation →
  `docs/research/color-masterclass/RESEARCH-HANDOFF.md`.

**Workflow results to reuse (cached):** `colorkit-quality-research` run `wf_3dbfcfdb-3f5` (effect recipes +
DWG + verify go/no-go) and `resolve-hlg-colormgmt-research` run `wf_f5b05f11-5ae` (Resolve setup). Both in
the session's workflow transcript dir; re-read or re-run via `{scriptPath, resumeFromRunId}` if needed.

## 4. KEY PATHS
- Engine dev: `auto-clip/colorkit/correct.py` (G1: `_apply_skin_solve`) + CLI `auto-clip/color.py` ·
  Standalone: `colorkit/` (synced) · Tests: `colorkit/tests/test_skin_solve.py` · Tracker:
  `auto-clip/COLOR-BUILD-STATUS.md` · Resolve guide: `docs/resolve-hlg-luna-setup.md` · Resolve LUTs:
  `colorkit/resolve-luts/` · Gap map (regenerated this session): `docs/research/color-masterclass/extracted/engine_gap_map.md`
  · venv: `auto-clip\.venv\Scripts\python.exe` (run via PowerShell, not Bash).
- Run G1: `…\.venv\Scripts\python.exe auto-clip\color.py <input>` (skin-solve on by default;
  `--skin-solve off` to disable). HLG Luna clips need `--hdr-tonemap auto --input-lut none`.
