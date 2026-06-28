"""
colorkit/segment.py -- Stage 0b of the headless color pipeline: SHOT SEGMENTATION.

Splits a flat, multi-scene video file into its component shots so the rest of the
engine can derive ONE constant correction per shot (the anti-flicker rule, see the
plan's section 3/4). Each shot is later treated as "a still of length 1": we analyze
a single representative frame, compute one correction, and apply it as a constant
transform across every frame of that shot.

Public API (per the COLORKIT contract):
    detect_shots(video_path) -> ShotList

A ``Shot`` is a plain dict ``{"index": int, "start": float, "end": float}`` (seconds),
and a ``ShotList`` is ``list[Shot]``.

Segmentation uses PySceneDetect's ``AdaptiveDetector`` via the convenience
``detect()`` entry point::

    from scenedetect import detect, AdaptiveDetector
    scenes = detect(video_path, AdaptiveDetector())

Graceful degradation is mandatory:
  * If PySceneDetect cannot be imported, we DO NOT raise -- we fall back to a single
    shot spanning the whole clip (duration probed via ffprobe).
  * If detection finds 0 or 1 scene, we likewise return one whole-clip shot.
  * If detection itself throws for any reason, we degrade to the same single shot.

This module deliberately depends only on ``scenedetect`` (optional) and the sibling
``io_utils`` module for the ffprobe-based duration fallback -- it never imports cv2,
numpy, or any heavy stack at module load.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Optional

# Sibling module: ffmpeg/ffprobe helpers. Imported eagerly because it is pure-stdlib
# (subprocess + json) and carries no heavy/optional dependencies of its own.
from . import io_utils

# Type aliases for documentation/clarity (kept as plain dicts/lists per the contract).
Shot = dict
ShotList = list


# --------------------------------------------------------------------------- #
# Duration probing (fallback path)
# --------------------------------------------------------------------------- #

def _probe_duration(video_path: str) -> float:
    """Return the video duration in seconds via ffprobe, or 0.0 if undeterminable.

    Tries the container/format duration first (cheapest, most reliable), then the
    first video stream's duration as a backup. Never raises -- on any failure it
    returns ``0.0`` so the caller can still emit a valid (if zero-length) single
    shot rather than blowing up the whole pipeline.

    Args:
        video_path: Path to the source video file.

    Returns:
        Duration in seconds as a float (``0.0`` when it cannot be determined).
    """
    # 1) Format-level duration (covers the vast majority of well-formed files).
    try:
        proc = io_utils.run_ffprobe([
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            video_path,
        ])
        if getattr(proc, "returncode", 1) == 0 and proc.stdout:
            data = json.loads(proc.stdout)
            raw = (data.get("format") or {}).get("duration")
            if raw is not None:
                dur = float(raw)
                if dur > 0:
                    return dur
    except Exception:
        # Fall through to the stream-level probe below.
        pass

    # 2) Stream-level duration (some containers only carry it on the video stream).
    try:
        proc = io_utils.run_ffprobe([
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=duration",
            "-of", "json",
            video_path,
        ])
        if getattr(proc, "returncode", 1) == 0 and proc.stdout:
            data = json.loads(proc.stdout)
            streams = data.get("streams") or []
            if streams:
                raw = streams[0].get("duration")
                if raw is not None:
                    dur = float(raw)
                    if dur > 0:
                        return dur
    except Exception:
        pass

    return 0.0


def _single_shot(video_path: str) -> ShotList:
    """Build a one-element ShotList spanning the entire clip [0, duration].

    This is the universal fallback: used when scenedetect is missing, when only one
    scene is found, or when detection errors out. A duration of ``0.0`` (unprobeable)
    still yields a structurally valid shot so downstream stages never see an empty list.

    Args:
        video_path: Path to the source video file.

    Returns:
        ``[{"index": 0, "start": 0.0, "end": <duration>}]``.
    """
    duration = _probe_duration(video_path)
    return [{"index": 0, "start": 0.0, "end": float(duration)}]


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def detect_shots(video_path: str) -> ShotList:
    """Segment ``video_path`` into shots using PySceneDetect's AdaptiveDetector.

    This is Stage 0b of the pipeline. The returned shots drive the constant-per-shot
    correction rule: every frame inside a shot receives the SAME correction, which is
    what structurally prevents flicker/pumping (see the plan, section 3).

    Behavior:
      * Imports ``scenedetect`` lazily so this module can be imported (and the image
        path of the engine can run) even when PySceneDetect is not installed.
      * Runs ``detect(video_path, AdaptiveDetector())`` and converts each
        ``(start, end)`` FrameTimecode pair into a ``Shot`` dict with float seconds.
      * If the import fails, detection raises, or detection yields 0 or 1 scene, it
        degrades gracefully to ONE shot spanning the whole clip (duration via ffprobe).
        It NEVER raises on a missing/failed scenedetect.

    Args:
        video_path: Path to the source video file. May be a ``str`` or path-like;
            it is coerced to ``str`` for both scenedetect and ffprobe.

    Returns:
        ShotList -- a non-empty ``list[Shot]`` ordered by start time, each
        ``{"index": int, "start": float, "end": float}`` in seconds.
    """
    vp = str(video_path)

    # Lazy import: a missing PySceneDetect must NOT break the module or the engine.
    try:
        from scenedetect import detect, AdaptiveDetector  # type: ignore
    except Exception:
        # scenedetect unavailable -> degrade to a single whole-clip shot.
        return _single_shot(vp)

    # Run detection. Any failure here (bad file, decoder issue, etc.) also degrades
    # gracefully rather than propagating -- segmentation is best-effort.
    try:
        scenes = detect(vp, AdaptiveDetector())
    except Exception:
        return _single_shot(vp)

    # 0 or 1 scene -> treat the clip as a single shot (cleaner timings via ffprobe,
    # and it satisfies the contract's "1 shot -> ONE Shot spanning the whole clip").
    if not scenes or len(scenes) <= 1:
        return _single_shot(vp)

    shots: ShotList = []
    for idx, scene in enumerate(scenes):
        try:
            start_tc, end_tc = scene[0], scene[1]
            start = float(start_tc.get_seconds())
            end = float(end_tc.get_seconds())
        except Exception:
            # A malformed scene tuple shouldn't sink the whole list; skip it.
            continue
        # Guard against zero/negative-length shots from edge-case detector output.
        if end <= start:
            continue
        shots.append({"index": idx, "start": start, "end": end})

    # If post-filtering left us with nothing usable, fall back to the single shot.
    if not shots:
        return _single_shot(vp)

    # Re-index sequentially in case any malformed scenes were skipped above, so the
    # indices remain a clean 0..N-1 run for downstream stages.
    for new_idx, shot in enumerate(shots):
        shot["index"] = new_idx

    return shots


# --------------------------------------------------------------------------- #
# Manual smoke test (not part of the engine entrypoint; color.py is the CLI).
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: python -m colorkit.segment <video_path>")
        raise SystemExit(2)

    _shots = detect_shots(sys.argv[1])
    print(f"{len(_shots)} shot(s):")
    for _s in _shots:
        print(f"  [{_s['index']:>3}] {_s['start']:8.3f} -> {_s['end']:8.3f}s")
