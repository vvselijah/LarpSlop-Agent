# SESSION-COMPACT — 2026-06-27 (cinematic look-stack VIDEO path)

**READ THIS on resume.** This session executed baton §3 **item 1** from
`SESSION-COMPACT-2026-06-26-g1-resolve.md`: wire the cinematic optical look-stack
(**halation / grain / vignette**) into the per-shot **VIDEO** ffmpeg filtergraph in `color.py`, so
rendered video gets the same film character the still path already had. Live tracker:
`auto-clip/COLOR-BUILD-STATUS.md` (**2026-06-27 section, top**). Memory: `[[project-color-engine]]`.
**DRAFT throughout — nothing committed, nothing pushed, nothing published.**

---

## 1. WHAT THIS SESSION DID (done + verified)

**The look-stack VIDEO path is DONE.** A look = its colour cube (applied in the per-shot `vf`) **PLUS**
an ordered optical stack layered AFTER the delivery scale, constant for every frame → flicker-free.

- **`colorkit/stylize.py` (new VIDEO surface):**
  - `optical_stack_plan(name, opacity)` — resolves a look's `LOOK_STACKS` entry → ordered
    `[(effect, params)]` with `strength` faded by look opacity (the SAME scaling `apply_look_stack_image`
    uses → still/video agree). `[]` for color-only / no look.
  - `bake_grain_plate` / `bake_vignette_mask` — deterministic seeded grain plate (mid-grey-centred) /
    elliptical multiply mask, **same numpy formulas as the still**, baked ONCE at delivery res.
  - `ffmpeg_halation_segment` / `ffmpeg_grain_segment` / `ffmpeg_vignette_segment` — filtergraph
    fragments wired by in/out labels.
- **`color.py::process_video`:** when the look has a stack, the colour chain becomes the head of a
  `filter_complex` (`[0:v]<vf>[m0]`) and halation→grain→vignette layer on top; looped plate inputs +
  `-map [final] -map 0:a?`. **Color-only looks / no-look keep the plain `-vf` path → byte-identical.**
  New helper `_probe_output_dims` (coded dims + rotation → post-scale dims) for plate sizing.
- **The recipes (masterclass-faithful + ffmpeg-robust):**
  - **Halation** = red-weighted highlight bloom **screened in LINEAR light**, kept ALL-float
    (`setparams`→`zscale t=linear`→`gbrpf32le`; an 8-bit intermediate poisons `blend` format-negotiation
    and round-trips the base ~2 levels). Highlight mask = squared soft-knee on linear luma via `geq`
    (exact on float). Glow computed at **1/4 res** (`scale`+`scale2ref`) — visually identical, ~16×
    cheaper geq (full-res geq was ~4× slower than realtime).
  - **Grain** = pre-baked **STATIC seeded plate** overlay on LUMA only (monochrome), shadow/mid-weighted.
    NEVER ffmpeg temporal `noise` (= flicker).
  - **Vignette** = pre-baked elliptical **multiply mask** in RGB (exact `rgb*v`, matches the still).

### Verified (real footage, proofs in `auto-clip/out/ftest/`)
- **FLICKER-FREE (headline):** rendered a STATIC input (one frame looped → zero source temporal
  variation). Output frame-to-frame meanabs = **0.010** (x264 quant) vs **12.3** for ffmpeg temporal
  `noise` — ~1200× margin. Holds for the all-three `portra` stack.
- **Still↔video parity:** kodak video vs still preview meanabs **2.73** (p95 6) — same grade (residual =
  expected sRGB-vs-bt709 / FIR-vs-IIR preview gap; the still is APPROXIMATE by design).
- **All 7 stack shapes render** (kodak hal+grain, teal hal+vig, moody_blue grain+vig, fuji grain,
  warm_interview hal, portra all-3, clean_pop color-only→`-vf`). Full pipeline (develop + **G1 skin-solve**
  + look + optical) composes on the approved talking-head `a test.mov`. Montages:
  `_VIDEOSTACK_lookbook.png`, `_VIDEOSTACK_kodak_src_vid_still.png`.
- **3 real bugs found+fixed mid-build:** (1) `-map` of a filter_complex label needs **brackets**
  (`[opt1]`); (2) looped-plate blends **hang on audio-less clips** → `shortest=1` on grain/vignette
  blends; (3) zscale **"no path between colorspaces"** on unspecified-tag sources → `setparams` stamp.
- **22/22 pytest** (18 prior + 4 new in `colorkit/tests/test_look_stack.py`). **Synced** dev tree
  (`auto-clip/colorkit/stylize.py` + `color.py`) → standalone (`colorkit/colorkit/stylize.py` + `cli.py`;
  diff = only the 4 package-vs-script lines). **Perf ~0.6× realtime @1080p.**

## 2. PENDING ELIJAH (decisions / gates)
- **Eyeball the looks:** `auto-clip/out/ftest/_VIDEOSTACK_lookbook.png` (source · kodak · teal · portra)
  and `_VIDEOSTACK_kodak_src_vid_still.png` (still↔video parity). Strengths in `stylize.LOOK_STACKS` are
  tuned to read UNDER the grade; say the word to dial any up/down.
- **Pick favorite looks** → `--look auto` defaults (still pending from prior batons).
- **Commit/sync?** Everything DRAFT/uncommitted; hub-root `colorkit/` is local-only (not pushed); the
  older `Desktop\colorkit` git repo does NOT have G1 or the look-stack.

## 3. NEXT — remaining of Elijah's "all four" (resume here; research cached in wf_3dbfcfdb-3f5)
Baton §3 item 1 (this) is DONE. Remaining, in order:
2. **Scopes `--validate` into the render** (correctness): `scopes.validate` exists but isn't auto-run.
   Add a `--validate` JSON sidecar + per-shot verdict log in `color.py`. Cheap, makes every grade
   falsifiable.
3. **Skin-LOCAL exposure** (faces): the under-exposed-skin G1 can't globally lift. Do it as a
   skin-COLOR-qualifier lift (bakeable into a constant cube → flicker-safe, NOT a spatial/keyed mask),
   gated like G1, reuse `correct._skin_mask`/`_skin_angle_ire`.
4. **Auto-pilot** (smarter): wire a real Claude-vision look-picker into `decide.suggest_look_ai`
   (opt-in, API-gated, deterministic fallback); widen `--look auto` to all 10 looks (`decide.VALID_LOOKS`
   is the original 5).
- DWG working space = DEFERRED (revisit at 10-bit/HDR delivery).

## 4. KEY PATHS
- Engine: `auto-clip/colorkit/stylize.py` (optical: `ffmpeg_*_segment`, `bake_*`, `optical_stack_plan`,
  `_LINEARIZE_709`) + CLI `auto-clip/color.py` (`process_video` filter_complex, `_probe_output_dims`,
  `_optical_chain`) · Standalone (synced): `colorkit/colorkit/{stylize,cli}.py` · Tests:
  `colorkit/tests/test_look_stack.py` (22 pass) · Tracker: `auto-clip/COLOR-BUILD-STATUS.md` ·
  venv: `auto-clip\.venv\Scripts\python.exe` (run via **PowerShell**, not Bash).
- Run a stacked look: `…\.venv\Scripts\python.exe auto-clip\color.py <clip.mp4> --look kodak_2383_style`
  (looks with a stack: kodak/teal_orange/moody_blue/fuji/warm_interview/portra/golden_hour; color-only:
  clean_pop/neutral_correct). HLG Luna clips: add `--hdr-tonemap auto`.

## 5. WORKING-TREE STATE (uncommitted DRAFT — exact files this session touched)
**Nothing is committed or pushed** (consistent with every prior color-engine session). `git status` shows
all of these as **untracked** (`??`) — the whole color engine is draft. Files changed/created THIS session:
- **`auto-clip/colorkit/stylize.py`** — MODIFIED: new VIDEO surface (`optical_stack_plan`, `bake_grain_plate`,
  `bake_vignette_mask`, `ffmpeg_{halation,grain,vignette}_segment`, `_LINEARIZE_709`/`_ENCODE_709`, `_fg`);
  `apply_look_stack_image` refactored to use `optical_stack_plan`; `__all__` extended.
- **`auto-clip/color.py`** — MODIFIED: `process_video` optical-stack setup block + `_optical_chain` closure +
  per-shot `filter_complex` branch in `_encode`; new `_probe_output_dims` helper.
- **`colorkit/colorkit/stylize.py`** — SYNCED copy of the dev stylize.py (identical).
- **`colorkit/colorkit/cli.py`** — SYNCED: same 3 edits ported (diff vs `auto-clip/color.py` = only the 4
  package-vs-script lines: BOM, `INPUT_LUT_DIR`, `from . import decide`, `prog`).
- **`colorkit/tests/test_look_stack.py`** — MODIFIED: +4 video-path tests (22 pass total).
- **`auto-clip/COLOR-BUILD-STATUS.md`** — MODIFIED: new 2026-06-27 section at top.
- **`SESSION-COMPACT-2026-06-27-lookstack-video.md`** (this file) + `HANDOFF.md` baton pointer + memory
  `[[project-color-engine]]` — updated.
- Scratch test clips were cleaned from `out/`; review proofs kept in `auto-clip/out/ftest/_VIDEOSTACK_*.png`.
- The OLDER git repo `C:\Users\elija\OneDrive\Desktop\colorkit` does **NOT** have G1, density, or the
  look-stack — only the hub-root standalone `ai agent team\colorkit\` is current.

**60-second re-verify after a clear** (PowerShell + the auto-clip venv):
```
cd "C:\Users\elija\OneDrive\Desktop\ai agent team\colorkit"; & ..\auto-clip\.venv\Scripts\python.exe -m pytest -q   # expect 22 passed
# render a stacked look on any clip -> out/<stem>_graded.mp4 (no flicker):
cd "..\auto-clip"; & .venv\Scripts\python.exe color.py <clip.mp4> --look kodak_2383_style
```
