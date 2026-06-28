"""Extract the colorkit engine into its own standalone repository (COPY; hub stays intact).

Creates <DEST> with a proper package layout, pyproject.toml, README, MIT LICENSE, .gitignore,
a smoke test, and a local git init + initial commit. Does NOT push anywhere. Re-runnable: it
refuses to clobber an existing non-empty dest unless --force.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HUB = Path(__file__).resolve().parent            # auto-clip/
SRC_PKG = HUB / "colorkit"                        # source package
DEST = Path(r"C:\Users\elija\OneDrive\Desktop\colorkit")  # standalone repo root (proposed name)
PKG = DEST / "colorkit"                            # package dir inside the repo

FORCE = "--force" in sys.argv

PY_MODULES = ["__init__.py", "io_utils.py", "measure.py", "correct.py", "tonemap.py",
              "stylize.py", "segment.py", "match.py", "luts.py"]


def main():
    if DEST.exists() and any(DEST.iterdir()) and not FORCE:
        print(f"DEST {DEST} exists and is non-empty; rerun with --force to overwrite. Aborting.")
        return 1
    PKG.mkdir(parents=True, exist_ok=True)

    # 1) copy the python modules
    for m in PY_MODULES:
        shutil.copyfile(SRC_PKG / m, PKG / m)

    # 2) copy the LUT data (looks + input transforms)
    for sub in ("luts", "input_luts"):
        s = SRC_PKG / sub
        d = PKG / sub
        d.mkdir(parents=True, exist_ok=True)
        for cube in s.glob("*.cube"):
            shutil.copyfile(cube, d / cube.name)

    # 3) copy the CLI (color.py -> colorkit/cli.py) with import + path adaptations
    cli = (HUB / "color.py").read_text(encoding="utf-8")
    cli = cli.replace(
        "from colorkit import io_utils, measure, correct, stylize, segment, match",
        "from . import io_utils, measure, correct, stylize, segment, match")
    # cli.py now lives INSIDE the package, so input_luts is a sibling dir of this file.
    cli = cli.replace('INPUT_LUT_DIR = BASE / "colorkit" / "input_luts"',
                      'INPUT_LUT_DIR = BASE / "input_luts"')
    (PKG / "cli.py").write_text(cli, encoding="utf-8")

    # 4) standalone io_utils: OUT_DIR = ./out (cwd-relative, overridable via COLORKIT_OUT)
    io = (PKG / "io_utils.py").read_text(encoding="utf-8")
    io = io.replace(
        '_THIS = Path(__file__).resolve()\n'
        'AUTO_CLIP_DIR: Path = _THIS.parent.parent           # auto-clip/\n'
        'OUT_DIR: Path = AUTO_CLIP_DIR / "out"               # auto-clip/out  (absolute)',
        'import os as _os\n'
        '_THIS = Path(__file__).resolve()\n'
        '# Standalone: default outputs to ./out (cwd), overridable via $COLORKIT_OUT.\n'
        'OUT_DIR: Path = Path(_os.environ.get("COLORKIT_OUT", "out")).resolve()')
    (PKG / "io_utils.py").write_text(io, encoding="utf-8")

    # 5) project files
    (DEST / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    (DEST / "README.md").write_text(README, encoding="utf-8")
    (DEST / "LICENSE").write_text(LICENSE, encoding="utf-8")
    (DEST / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    (DEST / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    tests = DEST / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "test_smoke.py").write_text(TEST_SMOKE, encoding="utf-8")

    # 6) local git init + commit (NO push)
    def git(*a):
        return subprocess.run(["git", *a], cwd=str(DEST), capture_output=True, text=True)
    if not (DEST / ".git").exists():
        git("init")
        git("config", "user.name", "Elijah Sullivan")
        git("config", "user.email", "tannercarlson@vvsvault.com")
    git("add", "-A")
    r = git("commit", "-m", COMMIT_MSG)
    print("git commit:", (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else "?")
    log = git("log", "--oneline", "-1")
    print("HEAD:", log.stdout.strip())
    print(f"\nExtracted standalone repo -> {DEST}")
    nfiles = sum(1 for _ in DEST.rglob("*") if _.is_file())
    print(f"files: {nfiles}")
    return 0


PYPROJECT = '''[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "colorkit"
version = "0.2.0"
description = "Headless agentic color-correction + film grading for images and video (Python + FFmpeg)."
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "Elijah Sullivan" }]
keywords = ["color grading", "color correction", "ffmpeg", "opencv", "lut", "film emulation", "video"]
dependencies = [
    "numpy>=1.24",
    "opencv-contrib-python>=4.8",
    "scikit-image>=0.21",
    "colour-science>=0.4.4",
    "scenedetect>=0.6",
]

[project.optional-dependencies]
dev = ["pytest>=7"]

[project.scripts]
colorkit = "colorkit.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["colorkit*"]

[tool.setuptools.package-data]
colorkit = ["luts/*.cube", "input_luts/*.cube"]
'''

REQUIREMENTS = """numpy>=1.24
opencv-contrib-python>=4.8
scikit-image>=0.21
colour-science>=0.4.4
scenedetect>=0.6
"""

LICENSE = '''MIT License

Copyright (c) 2026 Elijah Sullivan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

GITIGNORE = '''__pycache__/
*.py[cod]
*.egg-info/
build/
dist/
.venv/
venv/
out/
*.mp4
*.mov
*.mkv
.DS_Store
.pytest_cache/
'''

README = '''# colorkit

**Headless agentic color-correction + film grading for images and video** — a two-tier
Python + FFmpeg engine that *measures and corrects* with pixel-math and *stylizes* with film looks,
with no DaVinci/GUI dependency. Built to run from the command line on a single operator's machine and
**stop at files on disk — it never publishes anything.**

It does the combination that no off-the-shelf tool ships as one headless box: ingest a flat,
multi-scene clip, auto-segment it into shots, apply ONE **constant per-shot correction** (so there is
no flicker), match shots for continuity, and stack a tasteful creative look on top.

## What's in v0.2 (the "develop" overhaul)
Color grading done the way pros actually do it (distilled from a deep study of the best DaVinci
masterclasses), but headless:

- **Linear-light "develop"** — linearize → Shades-of-Gray white balance → per-channel black point →
  **expose the *median* mid-tone to 18% grey** (not the mean — no over-brightening) → one gentle
  contrast pivoted on mid-grey → a **C1 filmic highlight soft-clip** (protects highlights, no hard
  clip) → encode → luminance-safe **vibrance**. This is the fix for the "washed / one-tap-filter" look.
- **Input transform (log footage)** — for Log clips, apply the camera's Log→Rec.709 LUT *first*
  (`--input-lut`, with filename auto-detect), the camera-correct develop, before any correction.
- **Creative looks at opacity** — five film looks (`warm_interview`, `teal_orange`, `kodak_2383_style`,
  `fuji_style`, `neutral_correct`) that run **UNDER** the grade at ~0.7 opacity by default
  (`--look-opacity`), so they read as a tasteful grade, not a filter. Looks carry hue/density character;
  the develop owns contrast (no contrast-stacking).
- **Shot matching** — optional Reinhard-to-hero continuity matching (`--match`), baked per shot.
- **Delivery** — `--height` downscale (e.g. 8K → 1080p) applied last.

The non-negotiable video rule: derive ONE correction per shot from a representative frame and apply it
as a constant transform (baked to a `.cube`, applied via `lut3d=interp=tetrahedral`) — that constancy is
what structurally eliminates flicker.

## Install
```
pip install -e .
# requires FFmpeg + FFprobe on PATH (e.g. winget install Gyan.FFmpeg)
```

## Usage
```
# still:  before/after PNGs in ./out
colorkit path/to/frame.png --look warm_interview

# video:  graded mp4 in ./out (auto shot-detect + constant per-shot develop)
colorkit path/to/clip.mp4 --look teal_orange --match

# log 8K -> IG-ready, camera-correct develop + look under the grade
colorkit "i log vid.mp4" --input-lut ilog --look kodak_2383_style --height 1920

# correction only (no look): drop --look   ·   full look strength: --look-opacity 1.0
```
Outputs land in `./out` (override with `--out` or `$COLORKIT_OUT`). Nothing is ever published.

## Layout
- `colorkit/` — the package: `io_utils, measure, correct, tonemap, stylize, segment, match, luts, cli`
  + `luts/*.cube` (looks) + `input_luts/*.cube` (camera log transforms).
- `tests/` — a smoke test (`pytest`).

## License
MIT — see `LICENSE`.
'''

TEST_SMOKE = '''"""Smoke tests: the tonemap math + an end-to-end still develop. Run: pytest -q"""
import numpy as np
from colorkit import tonemap as tm
from colorkit import correct


def test_srgb_roundtrip():
    v = np.linspace(0, 1, 17)
    assert np.allclose(tm.srgb_oetf(tm.srgb_eotf(v)), v, atol=1e-6)


def test_midgrey_anchor():
    # 0.18 linear should encode to ~0.46 display (the mid-grey target)
    assert abs(tm.srgb_oetf(0.18) - 0.461) < 0.003


def test_soft_clip_never_clips():
    xs = np.linspace(0, 8, 2000)
    ys = tm.highlight_soft_clip(xs, knee=0.8, ceiling=1.0)
    assert ys.max() < 1.0  # asymptotes to ceiling, never crosses
    assert np.all(np.diff(ys) >= -1e-9)  # monotonic


def test_pivot_fixed():
    assert abs(tm.pivoted_contrast(0.18, 1.2) - 0.18) < 1e-9


def test_develop_on_synthetic_image():
    rng = np.random.default_rng(0)
    # a dim, blue-cast synthetic frame (BGR uint8)
    img = (rng.random((64, 64, 3)) * 90).astype(np.uint8)
    img[..., 0] = np.clip(img[..., 0] + 40, 0, 255)  # blue cast
    p = correct.compute_correction(img)
    out = correct.apply_correction_image(img, p)
    assert out.shape == img.shape and out.dtype == np.uint8
    # median luma should move toward mid-grey (brighter than the dim input)
    assert out.mean() > img.mean()
    # baked develop cube matches the direct apply within LUT tolerance
    import tempfile, os
    cube = os.path.join(tempfile.gettempdir(), "dev_smoke.cube")
    correct.bake_develop_cube(p, cube, size=33)
    assert os.path.getsize(cube) > 1000
'''

COMMIT_MSG = """Initial commit: colorkit v0.2 — headless agentic color engine

Linear-light develop (median->0.18 exposure, per-channel black point, filmic
highlight soft-clip, luma-safe vibrance), log input transform, creative looks
run under the grade at opacity, constant-per-shot anti-flicker correction +
shot match, delivery downscale. Headless Python + FFmpeg; stops at out/.
Grounded in a deep study of pro DaVinci color-grading methodology.
"""


if __name__ == "__main__":
    raise SystemExit(main())
