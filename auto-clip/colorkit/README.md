# colorkit — headless agentic color engine

**Auto color-correction + stylized film grading for stills and multi-scene video. No DaVinci, no GUI,
no GPU, no API key on the default path.** Pixel-math measures and corrects; a chosen look (a `.cube`
LUT) stylizes. It runs the canonical pro order, segments video into shots and corrects each one with a
single constant transform (the anti-flicker rule), and **stops at `out/` — it never publishes**
(CLAUDE.md rule 1).

This is `auto-clip`'s color stage: `color.py` (the CLI) one level up + the `colorkit/` package here.
Full design and prior-art rationale: `docs/plans/2026-06-23-agentic-color-pipeline.md`.
Build/verification log: `auto-clip/COLOR-BUILD-STATUS.md`.

> **Status: BUILT and VERIFIED on real footage** — stills, single-clip video, and full multi-scene
> video (segment → constant per-shot correction → shot-match → uniform look → concat).

---

## What it is

A two-tier, fully-headless **Python + FFmpeg** color engine:

- **MEASUREMENT (pixel-math)** decides the numbers — OpenCV + NumPy read every pixel, scikit-image
  flags low contrast, colour-science applies LUTs. This is deterministic, free, CPU-only.
- **DECISION (the look)** is a chosen, pre-authored LUT — you pass `--look NAME`; the engine never lets
  pixel-math invent creative intent and never lets a semantic guess set numeric gains.

It handles two inputs through one CLI:

- **Stills** (`.jpg/.jpeg/.png/.webp/.tif/.tiff`) → one correction → optional look → `before/after` PNGs.
- **Video** (`.mp4/.mov/.mkv/.webm`) → shot-segment → one constant correction *per shot* → optional
  inter-shot match → optional uniform look → concat → one graded `.mp4`.

---

## The non-negotiable rule: constant per shot (anti-flicker)

> **Derive ONE correction per shot from a single representative frame, then apply it UNCHANGED to every
> frame of that shot. Never correct frames independently.**

Per-frame-independent auto-correction wobbles frame to frame and produces visible **flicker / pumping** —
the single most-cited failure mode in the color literature. The whole architecture exists to avoid it:
every numeric transform (WB gains, eq, shot-match) is computed once per shot and baked into a *constant*
FFmpeg filtergraph (or a baked-once `.cube`), so it is structurally flicker-free. Stay inside this rule
when extending the engine.

---

## Pipeline architecture

```
            color.py  (Stage 0 — ROUTER: image vs video by extension)
                 │
   ┌─────────────┴───────────────────────────────────────────────┐
   │ IMAGE route                          VIDEO route             │
   │                                                              │
   │ cv2.imread                  segment.detect_shots  (Stage 0b) │
   │   │                                  │  PySceneDetect        │
   │   │                          for EACH shot:                  │
   │   │                            measure.representative_frame   │
   │   │                            io_utils.extract_frame         │
   │ correct.compute_correction ──► correct.compute_correction     │  Stage 1 — MEASURE + CORRECT
   │ correct.apply_correction_image  (constant params per shot)    │            (constant per shot)
   │   │                                  │                        │
   │   │                          match.compute_match_params ──────┤  Stage 2 — MATCH (opt-in --match)
   │   │                            bake constant per-shot .cube    │            Reinhard LAB → hero
   │   │                                  │                        │
   │ stylize.apply_look_image ────► stylize.ffmpeg_lut_filter      │  Stage 3 — STYLIZE (uniform look)
   │   │                                  │                        │
   │ write before/after PNG       per-shot ffmpeg render → concat  │  Stage 4 — RENDER
   │                              [--deflicker backstop, Stage 3b] │
   └──────────────────────────────────────┬───────────────────────┘
                                           ▼
                                    auto-clip/out/   (review only — NEVER published)
```

**Canonical order is always `correct → match → stylize`:**

1. **Correct** each shot to neutral (white balance + exposure/contrast/gamma/saturation).
2. **Match** every shot toward a hero shot for cut-to-cut continuity (opt-in).
3. **Stylize** with one uniform creative look across the whole clip, last and on top.

In the video route this becomes a per-shot FFmpeg filtergraph:
`colorchannelmixer/eq (correct) → lut3d (match) → lut3d (look)`, applied identically to every frame of
the shot, then all shots are concatenated.

---

## Module map

| Module | Role | Heavy deps |
|---|---|---|
| `../color.py` | **CLI / Stage 0 router.** Image-vs-video routing, per-shot orchestration, concat, manifest. Lives one level up in `auto-clip/`. | cv2 (lazy) |
| `__init__.py` | Thin namespace marker with **lazy** (PEP 562) re-exports — `import colorkit` pulls in no cv2/numpy/skimage/colour/scenedetect until a name is actually touched. | none |
| `io_utils.py` | I/O + subprocess plumbing. Owns `OUT_DIR` (= `auto-clip/out`), `run_ffmpeg`/`run_ffprobe`, single-frame `extract_frame`, `ffprobe_signalstats`. **No cv2/numpy.** | none |
| `measure.py` | **Stage 1 measure.** `measure_image` (gray-world channel means, Lab means, luma/sat, low-contrast flag); `representative_frame_time` (brightness-median frame per shot via signalstats). | cv2, numpy, skimage (lazy) |
| `correct.py` | **Stage 1 correct.** `compute_correction` (emit WB gains + eq params), `apply_correction_image` (still bake), `ffmpeg_correction_filter` (the same params as a constant video filter). | cv2, numpy, skimage |
| `match.py` | **Stage 2 shot-match.** Reinhard LAB mean/std transfer toward a hero — `compute_match_params` / `apply_match_params` / `reinhard_transfer`. Constant per shot. | cv2, numpy |
| `segment.py` | **Stage 0b segmentation.** `detect_shots` via PySceneDetect `AdaptiveDetector`; **graceful single-shot fallback** if scenedetect is missing or detection finds ≤1 scene. | scenedetect (lazy, optional) |
| `stylize.py` | **Stage 3 stylize.** `LOOKS` registry, `ffmpeg_lut_filter` (video, bare-filename `lut3d`), `apply_look_image` (still, tetrahedral), split-tone helpers. | numpy; colour (lazy) |
| `luts.py` | **STDLIB-ONLY** Iridas `.cube` writer + the 5 film-look generators. Runs on a bare Python — regenerates the look library anywhere. | none |
| `luts/*.cube` | The 5 generated look LUTs (`LUT_3D_SIZE 33`, red-fastest Iridas ordering). | — |

**Lazy-import discipline is deliberate:** heavy native imports (cv2/torch) are slow and known to hang on
the OneDrive disk, so nothing heavy loads at package import — only when the relevant function runs.

---

## The 5 looks

Generated by `luts.py` (pure-math film *emulation*, not colorimetric profiles — names ending in `_style`
signal that). These are the exact `--look NAME` values the CLI accepts.

| `--look` | Look |
|---|---|
| `neutral_correct` | Near-identity technical pass — a whisper of contrast/chroma, no color shift. Lets correction-only output go through the LUT stage cleanly without fighting the neutral correction. |
| `warm_interview` | Clean, flattering warm talking-head look — gentle warm WB, soft contrast, lifted shadows, healthy skin. The default for interview footage. |
| `teal_orange` | The cinematic teal-shadows / orange-highlights "blockbuster" grade — split-tone over a contrast S-curve with a saturation lift. Stronger than `warm_interview`. |
| `kodak_2383_style` | Print-film *style* — warm rich body, slightly cool crushed blacks, creamy warm highlights, lift/gamma/gain print toe + shoulder. |
| `fuji_style` | Fuji-stock *style* — green-leaning midtones, gentle contrast, restrained highlights, vibrant-but-not-loud color. Cooler/softer than the Kodak look. |
| `golden_hour` | Warm, aspirational golden-hour glow — amber highlights, soft warm shadow lift. Lifestyle / faith / motivational; warmer and softer than `warm_interview`. |
| `moody_blue` | Cool cinematic night/urban look — teal-blue shadows, cool highlights, slightly muted. The complement to the warm looks; suits night b-roll / driving / moody talking-head. |
| `bleach_bypass` | Silver-retention *bleach bypass* — heavily desaturated, crisp, neutral-cool. Gritty / dramatic; carries almost no hue (desaturation is the character). |
| `clean_pop` | Bright, punchy, clean commercial look — neutral whites, lively saturation, no tint cast. Product / ad / IG / high-energy talking-head. |
| `portra_style` | Soft Kodak Portra *style* — lifted creamy toe, warm-pink skin highlights, low contrast, muted-pretty. A gentler, pastel alternative to `warm_interview` for portraits/lifestyle. |

> Looks run UNDER the develop at `--look-opacity` (default **0.7**) so they read as a tasteful grade, not
> a one-tap filter. Compare them all on one frame: `out/ftest/hdr/_LOOKBOOK_v2.png`.

**Regenerate the library** (stdlib-only, runs on any Python):

```powershell
auto-clip\.venv\Scripts\python.exe -m colorkit.luts --all
# optional: --out DIR  --size N   (default dir colorkit/luts/, default LUT_3D_SIZE 33)
```

---

## CLI usage

**Always run with the venv Python from the `auto-clip/` directory** (Python 3.12 venv with
opencv-contrib-python, numpy, scikit-image, colour-science, scenedetect — all permissive Apache/BSD):

```
auto-clip\.venv\Scripts\python.exe color.py <input> [flags]
```

### Stills

```powershell
# correct only (no look) → before/after PNGs:
auto-clip\.venv\Scripts\python.exe color.py path\to\frame.png

# correct + a creative look:
auto-clip\.venv\Scripts\python.exe color.py path\to\frame.png --look teal_orange

# look only, skip correction:
auto-clip\.venv\Scripts\python.exe color.py path\to\frame.png --look fuji_style --no-correct
```
→ writes `out/<stem>_before.png` and `out/<stem>_after.png`.

### Video

```powershell
# correct each shot to neutral (constant per shot), no look:
auto-clip\.venv\Scripts\python.exe color.py path\to\clip.mp4

# correct + uniform film look across all shots:
auto-clip\.venv\Scripts\python.exe color.py path\to\clip.mp4 --look kodak_2383_style

# correct + inter-shot continuity match toward a hero shot + look:
auto-clip\.venv\Scripts\python.exe color.py path\to\clip.mp4 --look warm_interview --match

# gentler match strength (default --match-alpha 0.8):
auto-clip\.venv\Scripts\python.exe color.py path\to\clip.mp4 --match --match-alpha 0.5

# look only, no correction:
auto-clip\.venv\Scripts\python.exe color.py path\to\clip.mp4 --look teal_orange --no-correct

# add the temporal backstop if any residual luminance pumping remains:
auto-clip\.venv\Scripts\python.exe color.py path\to\clip.mp4 --look teal_orange --deflicker
```
→ writes `out/<stem>_graded.mp4` (and `out/<stem>_graded_deflicker.mp4` when `--deflicker` is used).

### Flags

| Flag | Effect |
|---|---|
| `--look NAME` | Apply a look from the registry (default: none = correct-only). One of the 5 names above. |
| `--no-correct` | Skip the auto color-correction stage (look-only). Cannot be combined with no `--look` (nothing to do). |
| `--match` | **Video only.** Stage 2 inter-shot continuity match — pick a hero shot, derive a constant Reinhard LAB transfer per shot, bake it to a per-shot `.cube`. No-op on single-shot clips; needs correction on (it matches the *corrected* shots). |
| `--match-alpha A` | Strength of the shot-match transfer in `[0,1]` (default `0.8`; lower = gentler). |
| `--deflicker` | Optional temporal backstop on the final video (`ffmpeg deflicker + normalize`). |
| `--out DIR` | Output directory (default: `auto-clip/out`). |
| `--keep-temp` | Keep per-shot intermediate files for debugging (default removes them). |

---

## out/-only — the no-publish guarantee

Every output — before/after PNGs and graded MP4s — lands **only** under `OUT_DIR` (`auto-clip/out`,
resolved from `__file__`, not the cwd). The modules return strings/arrays/filter-graphs; only `color.py`
writes files, and it writes nothing outside `out/`. At the end it logs a manifest explicitly marked
*review only — NOT published, per CLAUDE.md rule 1*. **The engine never posts, uploads, or DMs. The
publish click is always Elijah's.**

---

## Troubleshooting

### FFmpeg `lut3d` rejects Windows absolute paths (the cwd gotcha)

**Symptom:** an `lut3d` filter fails to parse when handed an absolute Windows cube path
(`C:\...\teal_orange.cube`) — the drive colon is read as an option separator and spaces break it too. No
escaping or quoting we tested (`C\:`, single-quoting, `\ `) gets past the filtergraph parser.

**How the engine handles it (already built in):** `color.py` stages **every** cube used in a render
(the look LUT *and* every per-shot match LUT) into ONE temp directory under `out/`, then runs FFmpeg with
`cwd` set to that directory and references each cube by **bare filename**
(`lut3d=interp=tetrahedral:file=teal_orange.cube`). Input/output paths in the command stay absolute, so
the cwd only affects cube resolution. This is why `stylize.ffmpeg_lut_filter` emits a bare filename and
`io_utils.run_ffmpeg` takes a `cwd` argument — keep that contract if you add LUT-applying stages.

### `compute_correction: bgr frame is None` / `could not decode image`

The frame failed to decode. For video this is logged per shot and the shot is corrected with identity
rather than crashing. Confirm the input path and that ffmpeg/ffprobe are on PATH (`winget Gyan.FFmpeg`).

### A multi-shot clip shows color jumps at cut boundaries

Constant-per-shot correction is flicker-free *within* a shot but can leave exposure/cast jumps *between*
shots. Pass `--match` (with correction on) to reconcile them toward a hero shot. Lower `--match-alpha` if
the match overshoots.

### `look 'X' maps to a missing .cube`

The look library hasn't been generated (or was cleaned). Rebuild it:
`auto-clip\.venv\Scripts\python.exe -m colorkit.luts --all`.

### cv2 / colour-science import hangs on the OneDrive disk

The package imports heavy deps lazily for exactly this reason. Use the venv Python; prefer `pip show` over
`python -c "import cv2"` to check installs. Run via PowerShell (the hub's Bash lacks the venv tooling).
