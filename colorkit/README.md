# colorkit — headless agentic color engine

Automatic, DaVinci-free color **correction + film grading** for images and video, in pure Python + FFmpeg.
Point it at a frame or clip: it develops a neutral, exposure-anchored base, optionally matches shots and
lays a tasteful film look on top, and writes before/after stills or a graded `.mp4` to `out/`.
**It never publishes — it stops at files on disk.**

Built from a frame-by-frame study of pro DaVinci colorist masterclasses. New in v0.3: **headless scopes +
self-validation** (`scopes.py`) and a **skin signature** measurement (`measure.skin_signature`) that read a
grade the way a colorist reads a waveform/parade/vectorscope.

---

## Quick start (agent in this workspace — no install needed)

All dependencies are already in the auto-clip virtualenv, so the fastest path is to run with that
interpreter from this project directory:

```powershell
$py = "C:\Users\elija\OneDrive\Desktop\ai agent team\auto-clip\.venv\Scripts\python.exe"
Set-Location "C:\Users\elija\OneDrive\Desktop\ai agent team\colorkit"

# correct a still  -> writes out\<name>_before.png + out\<name>_after.png
& $py -m colorkit.cli "path\to\frame.jpg"

# correct + a film look on a video -> writes out\<name>_graded.mp4
& $py -m colorkit.cli "path\to\clip.mp4" --look warm_interview

# let it pick the look automatically
& $py -m colorkit.cli "path\to\clip.mp4" --look auto
```

`python run.py <input> [flags]` and `python -m colorkit <input> [flags]` are equivalent entry points.

## Or install it as a package

```bash
pip install -e .            # deps: numpy, opencv-contrib-python, scikit-image, colour-science, scenedetect
colorkit <input> [flags]    # console entry point
```

Requires **Python 3.10+** and **ffmpeg + ffprobe on PATH** (the video path shells out to FFmpeg).

---

## What it does (pipeline order)

```
HDR tonemap (-1) -> input transform / Log->Rec709 (0) -> develop (1) -> shot-match (2) -> film look (3) -> delivery scale
```

- **Develop (auto-correct).** Linear-light white balance (Shades-of-Gray), per-channel black point,
  exposure anchored to mid-grey, one pivoted contrast, highlight soft-clip, vibrance. Derived **once per
  shot** from a representative frame and applied as a **constant** transform to every frame (flicker-free).
- **Looks.** 10 film looks run **under** the grade at 0.7 opacity (tasteful, not a one-tap filter).
- **Shot match (`--match`).** Reinhard LAB transfer toward a hero shot for cut-to-cut continuity.
- **HDR (`--hdr-tonemap`).** HLG/PQ → Rec.709 SDR before grading.
- **I-Log.** Insta360 Luna I-Log → Rec.709 input LUT, auto-applied by filename (`--input-lut`).
- **Scopes (new).** Read a corrected frame against demonstrated colorist targets (black off 0, diffuse
  white ~896/1023, no clip, parade converged, skin on the ~123° I-line, skin 40–50 IRE). Advisory.

## Looks

`neutral_correct · warm_interview · teal_orange · kodak_2383_style · fuji_style · golden_hour · moody_blue ·
bleach_bypass · clean_pop · portra_style`

## Key flags

| flag | meaning |
|---|---|
| `--look NAME\|auto` | film look from the list above (default: correct-only) |
| `--look-opacity O` | look strength 0..1 (default 0.7) |
| `--strength S` | develop intensity 0..1 (default 1.0; lower = gentler) |
| `--no-correct` | look only, skip the develop |
| `--match` / `--match-alpha A` | inter-shot continuity matching (video; A default 0.8) |
| `--input-lut auto\|none\|ilog\|<path>` | Stage-0 Log→Rec709 transform |
| `--hdr-tonemap auto\|hable\|mobius\|reinhard\|placebo\|none` | HDR→SDR (video) |
| `--hwaccel auto\|cuda\|qsv\|d3d11va\|none` | hardware decode (8K throughput) |
| `--height N` | downscale output to N px tall (e.g. 1920 for IG) |
| `--out DIR` | output directory (default: `./out`) |
| `--deflicker` / `--keep-temp` | optional temporal backstop / keep intermediates |

## Output

- **Image** → `out/<name>_before.png`, `out/<name>_after.png`
- **Video** → `out/<name>_graded.mp4`

Outputs always land in `out/` (next to this README) unless `--out` overrides it. Nothing is ever published.

## Programmatic API

```python
import cv2, colorkit
from colorkit import correct, measure, scopes

bgr = cv2.imread("frame.jpg")
params = correct.compute_correction(bgr)            # measure -> develop params (dict, JSON-safe)
graded = correct.apply_correction_image(bgr, params)

# self-validation against demonstrated colorist targets:
sig = measure.skin_signature(graded)                # skin hue vs the 123° I-line + IRE exposure
report = scopes.validate(graded, sig)               # waveform/parade/vectorscope + pass/fail verdict
print(report["verdict"])                            # e.g. "10/10 demonstrated targets met"
```

`import colorkit` stays cheap (lazy) — cv2/numpy/etc. load only when you touch a function.

## Tests

```powershell
& $py -m pytest -q            # tonemap math, an end-to-end develop, and the scopes/skin layer
```

## Status (v0.3.0)

- ✅ Develop, 10 looks, shot-match, HDR tonemap, GPU decode, I-Log input, auto-look picker.
- ✅ **New:** headless scopes (`scopes.py`) + skin signature (`measure.skin_signature`) — measurement /
  self-validation only (advisory; they never alter pixels).
- 🔜 A **skin-tone-line correction** stage (nudging skin onto the I-line during the develop) is designed but
  not yet wired in — today the scopes only *measure* skin drift. See `colorkit/INTEGRATION.md` and the
  parent workspace's `docs/research/color-masterclass/extracted/engine_gap_map.md` for the roadmap.

DRAFT/local engine — outputs stop at `out/`, nothing is published.
```
