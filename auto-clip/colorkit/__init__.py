"""colorkit -- headless color-grading engine for the auto-clip pipeline.

A two-tier, fully-headless Python + FFmpeg color engine (no DaVinci dependency):
**pixel-math measures and corrects** (OpenCV + NumPy + scikit-image + colour-science)
while a thin CLI / optional semantic layer **decides the look**. It runs the canonical
pro order -- correct each shot to neutral -> match shots -> stylize on top -- and obeys
one non-negotiable video rule: derive ONE correction per shot and apply it as a constant
transform (never per-frame-independently), or you get flicker/pumping.

See ``docs/plans/2026-06-23-agentic-color-pipeline.md`` for the full architecture.

This package is a thin namespace marker. The real work lives in the sibling modules:

    io_utils   -- OUT_DIR, ffmpeg/ffprobe runners, frame extraction, signalstats
    measure    -- per-pixel measurement (channel means, LAB, low-contrast, rep frame)
    correct    -- white-balance / exposure / contrast correction params + apply
    stylize    -- creative looks (.cube LUTs, split-tone) for stills and video
    segment    -- PySceneDetect shot segmentation (graceful single-shot fallback)
    match      -- Reinhard shot-to-hero matching (constant per shot)
    luts       -- STDLIB-ONLY .cube LUT writer + film-look generators
    (the ``color.py`` CLI one level up routes image-vs-video and orchestrates these)

Lazy by design
--------------
``import colorkit`` must stay cheap and side-effect-free: it MUST NOT import cv2,
numpy, scikit-image, colour-science or scenedetect at module load. Those are heavy
(and known to hang on the OneDrive disk for cv2/torch). Instead we expose a curated
set of convenience names that are resolved on first access via PEP 562
``__getattr__`` -- so ``colorkit.measure_image`` only imports ``colorkit.measure``
(and thus cv2) at the moment you actually touch it.

Usage::

    import colorkit
    print(colorkit.__version__)            # cheap, no heavy deps

    # heavy deps load only on first attribute access:
    bgr = ...                              # an OpenCV BGR ndarray
    params = colorkit.compute_correction(bgr)
    fixed = colorkit.apply_correction_image(bgr, params)

    # the submodules are also lazily importable as attributes:
    shots = colorkit.segment.detect_shots("clip.mp4")

The ``luts`` module stays free of cv2/numpy (pure stdlib) so it can run on a bare
Python; accessing ``colorkit.luts`` here does NOT pull in any heavy dependency.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

__version__ = "0.1.0"

# ---------------------------------------------------------------------------
# Lazy re-export registry.
#
# Maps a public convenience name -> the submodule (relative to this package)
# that defines it. Nothing here is imported at package-load time; resolution
# happens in __getattr__ on first access (PEP 562). This keeps ``import colorkit``
# free of cv2/numpy/skimage/colour/scenedetect.
#
# Keep this table aligned with the COLORKIT CONTRACT signatures.
# ---------------------------------------------------------------------------
_LAZY_EXPORTS: dict[str, str] = {
    # --- io_utils (ffmpeg/ffprobe glue; no cv2) -------------------------------
    "OUT_DIR": "io_utils",
    "ensure_out_dir": "io_utils",
    "run_ffmpeg": "io_utils",
    "run_ffprobe": "io_utils",
    "extract_frame": "io_utils",
    "ffprobe_signalstats": "io_utils",
    # --- measure (per-pixel measurement; pulls cv2/skimage on access) ---------
    "measure_image": "measure",
    "scene_stats": "measure",
    "representative_frame_time": "measure",
    # --- decide (the optional "pick-the-look" decision layer) -----------------
    "suggest_look": "decide",
    "suggest_look_ai": "decide",
    # --- correct (v2 linear-light develop: WB / black point / exposure / tone) -
    "compute_correction": "correct",
    "apply_correction_image": "correct",
    "develop_fn": "correct",
    "bake_develop_cube": "correct",
    # --- tonemap (linear-light transfer fns + filmic curves) ------------------
    "srgb_eotf": "tonemap",
    "srgb_oetf": "tonemap",
    "highlight_soft_clip": "tonemap",
    # --- stylize (creative looks / LUTs) --------------------------------------
    "LOOKS": "stylize",
    "list_looks": "stylize",
    "ffmpeg_lut_filter": "stylize",
    "apply_look_image": "stylize",
    "ffmpeg_splittone_filter": "stylize",
    # --- hdr (HLG/PQ detection + HDR->SDR tonemap, Stage -1) -------------------
    "probe_color": "hdr",
    "is_hdr": "hdr",
    "tonemap_filter": "hdr",
    "resolve_tonemap_spec": "hdr",
    # --- accel (optional hardware-accelerated decode for 8K throughput) --------
    "detect_hwaccels": "accel",
    "resolve_hwaccel": "accel",
    "hwaccel_decode_args": "accel",
    # --- segment (shot detection; graceful single-shot fallback) --------------
    "detect_shots": "segment",
    # --- match (Reinhard shot-to-hero) ----------------------------------------
    "reinhard_transfer": "match",
    "compute_match_params": "match",
    # --- luts (STDLIB-ONLY .cube writer + film generators) --------------------
    "write_cube": "luts",
    "neutral_correct": "luts",
    "warm_interview": "luts",
    "teal_orange": "luts",
    "kodak_2383_style": "luts",
    "fuji_style": "luts",
}

# The submodules themselves are also lazily importable as ``colorkit.<name>``.
_SUBMODULES: tuple[str, ...] = (
    "io_utils",
    "measure",
    "correct",
    "tonemap",
    "stylize",
    "segment",
    "match",
    "luts",
    "hdr",
    "accel",
    "decide",
)

__all__ = ["__version__", *_SUBMODULES, *_LAZY_EXPORTS.keys()]


def __getattr__(name: str) -> Any:
    """Resolve convenience names and submodules lazily (PEP 562).

    Importing a submodule is deferred until the corresponding attribute is first
    touched, so ``import colorkit`` never eagerly loads cv2/numpy/skimage/colour/
    scenedetect. Once resolved, the value is cached on the package module's
    ``__dict__`` so subsequent lookups are plain attribute reads.
    """
    # Direct submodule access: colorkit.measure, colorkit.luts, ...
    if name in _SUBMODULES:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module  # cache so we don't re-import next time
        return module

    # Convenience symbol re-exported from one of the submodules.
    submodule_name = _LAZY_EXPORTS.get(name)
    if submodule_name is not None:
        module = import_module(f"{__name__}.{submodule_name}")
        try:
            value = getattr(module, name)
        except AttributeError as exc:  # contract drift: name missing in sibling
            raise AttributeError(
                f"{__name__!s} expected {submodule_name!r} to export {name!r}, "
                f"but it does not (check the COLORKIT CONTRACT)."
            ) from exc
        globals()[name] = value  # cache the resolved object
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """Expose lazy names to ``dir()`` / autocomplete without importing them."""
    return sorted(set(globals()) | set(__all__))


# Static type-checkers and IDEs don't run __getattr__, so surface the lazy
# names here for them only. This block is skipped at runtime (TYPE_CHECKING is
# False), so it imports nothing heavy when the package is actually used.
if TYPE_CHECKING:  # pragma: no cover
    from .io_utils import (  # noqa: F401
        OUT_DIR,
        ensure_out_dir,
        extract_frame,
        ffprobe_signalstats,
        run_ffmpeg,
        run_ffprobe,
    )
    from .measure import measure_image, representative_frame_time, scene_stats  # noqa: F401
    from .decide import suggest_look, suggest_look_ai  # noqa: F401
    from .correct import (  # noqa: F401
        apply_correction_image,
        bake_develop_cube,
        compute_correction,
        develop_fn,
    )
    from .tonemap import (  # noqa: F401
        highlight_soft_clip,
        srgb_eotf,
        srgb_oetf,
    )
    from .stylize import (  # noqa: F401
        LOOKS,
        apply_look_image,
        ffmpeg_lut_filter,
        ffmpeg_splittone_filter,
        list_looks,
    )
    from .segment import detect_shots  # noqa: F401
    from .hdr import (  # noqa: F401
        is_hdr,
        probe_color,
        resolve_tonemap_spec,
        tonemap_filter,
    )
    from .accel import (  # noqa: F401
        detect_hwaccels,
        hwaccel_decode_args,
        resolve_hwaccel,
    )
    from .match import compute_match_params, reinhard_transfer  # noqa: F401
    from .luts import (  # noqa: F401
        fuji_style,
        kodak_2383_style,
        neutral_correct,
        teal_orange,
        warm_interview,
        write_cube,
    )
