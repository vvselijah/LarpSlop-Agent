"""colorkit.accel -- optional hardware-accelerated DECODE for the video path (8K throughput).

The Insta360 Luna produces 8K (7680x4320) 10-bit H.265. On the video path the wall-clock
bottleneck is *decoding* those frames, not the grade itself (the per-shot ``lut3d`` develop/look is
cheap). This hub's machine has an NVIDIA GPU (RTX 5070) with NVDEC; measured on the real 8K I-Log
clip, ``-hwaccel cuda`` decodes ~4x faster than software (60 frames: 7.7s software -> 1.9s NVDEC).

Design: **hardware DECODE ONLY** -- we do NOT pass ``-hwaccel_output_format``. ffmpeg decodes on the
GPU then auto-downloads frames to system memory, so the existing CPU filtergraph (the ``lut3d``
develop/look, the HDR ``zscale`` tonemap, ``scale``) is unchanged and needs no GPU-filter variants.
This is the safe integration: it never changes pixels, only how fast they are decoded, and it
degrades gracefully to software when a given file/accelerator combination fails.

Robustness contract:
  * ``resolve_hwaccel(mode, src)`` validates the chosen accelerator by actually decoding ONE frame
    of the real source before committing to it for the whole run (so an incompatible file falls
    back to software cleanly, once, up front -- not mid-render).
  * The caller (``color.py``) additionally retries any per-shot render in software if the
    hardware-decode attempt fails, as a second safety net.

Pure-stdlib (only ``io_utils`` for the ffmpeg calls). No cv2/numpy.
"""
from __future__ import annotations

from typing import List, Optional

from . import io_utils

__all__ = [
    "detect_hwaccels",
    "resolve_hwaccel",
    "hwaccel_decode_args",
    "PREFERRED",
]

# Preference order for ``--hwaccel auto``. NVDEC/CUDA was fastest on this machine; d3d11va is the
# most universally-robust Windows path (works for NVIDIA/AMD/Intel); qsv/dxva2/vaapi follow.
PREFERRED: List[str] = ["cuda", "qsv", "d3d11va", "dxva2", "vaapi"]

_DISABLE = {"none", "off", "false", "0", "no"}

# Module-level cache for the parsed ``-hwaccels`` list (it never changes within a process).
_HWACCELS_CACHE: Optional[List[str]] = None


def detect_hwaccels() -> List[str]:
    """Return the hardware-acceleration methods this ffmpeg build lists (cached).

    Parses ``ffmpeg -hwaccels``. Never raises -- returns ``[]`` on any failure (so callers fall
    back to software decode).
    """
    global _HWACCELS_CACHE
    if _HWACCELS_CACHE:  # trust only a non-empty cached result
        return _HWACCELS_CACHE
    methods: List[str] = []
    try:
        r = io_utils.run_ffmpeg(["-hide_banner", "-hwaccels"])
        text = (r.stdout or "") + "\n" + (r.stderr or "")
        started = False
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.lower().startswith("hardware acceleration methods"):
                started = True
                continue
            if started and " " not in s:  # the list is one bare method per line
                methods.append(s.lower())
    except Exception:
        methods = []
    # Only cache a real (non-empty) result, so a transient ffmpeg hiccup / parse miss on the first
    # call does not permanently disable hardware decode for the whole process -- a later call retries.
    if methods:
        _HWACCELS_CACHE = methods
    return methods


def _candidates(mode: Optional[str], available: List[str]) -> List[str]:
    """Resolve ``mode`` -> an ordered list of accelerator names to try (intersected w/ available)."""
    m = (mode or "auto").strip().lower()
    if m in _DISABLE:
        return []
    if m in {"auto", "on", "true", "1", "yes", "default", ""}:
        return [a for a in PREFERRED if a in available]
    # Explicit request: honour it only if the build actually has it.
    return [m] if m in available else []


def _validate(method: str, src) -> bool:
    """Decode ONE frame of ``src`` with ``-hwaccel method``; True iff ffmpeg exits 0.

    This is the real-source probe: it proves the accelerator can actually decode THIS file's codec /
    bit-depth (e.g. 10-bit HEVC) before we rely on it for every shot.
    """
    try:
        r = io_utils.run_ffmpeg([
            "-hide_banner", "-loglevel", "error",
            "-hwaccel", method,
            "-ss", "0", "-i", str(src),
            "-frames:v", "1", "-f", "null", "-",
        ])
        return getattr(r, "returncode", 1) == 0
    except Exception:
        return False


def resolve_hwaccel(mode: Optional[str], src, log=None) -> Optional[str]:
    """Pick a working hwaccel for ``src`` (validated on the real file), or ``None`` for software.

    ``mode``: ``auto`` (default; first working from :data:`PREFERRED`), an explicit method name, or
    ``none``/``off`` to force software. ``log`` is an optional ``callable(str)`` for a one-line note.
    """
    avail = detect_hwaccels()
    cands = _candidates(mode, avail)
    if not cands:
        if log and (mode or "").strip().lower() not in _DISABLE and mode not in (None, "auto", ""):
            log(f"hwaccel: '{mode}' not available in this ffmpeg (have: {', '.join(avail) or 'none'}) "
                "-- using software decode")
        return None
    for m in cands:
        if _validate(m, src):
            if log:
                log(f"hwaccel: using '{m}' for decode (validated on source)")
            return m
        elif log:
            log(f"hwaccel: '{m}' failed to decode this source -- trying next / software")
    if log:
        log("hwaccel: no accelerator could decode this source -- using software decode")
    return None


def hwaccel_decode_args(method: Optional[str]) -> List[str]:
    """ffmpeg input args for the chosen method: ``['-hwaccel', method]`` (or ``[]`` for software)."""
    return ["-hwaccel", method] if method else []
