"""
colorkit/io_utils.py -- I/O + subprocess plumbing for the headless color-grading engine.

This module is the single place that shells out to ffmpeg / ffprobe and owns the output
directory. It deliberately uses NO cv2 / numpy so it is cheap to import and safe to call from
the stdlib-only LUT writer's neighbours. Per the COLORKIT CONTRACT all final outputs live ONLY
under ``OUT_DIR`` (= auto-clip/out), and the engine NEVER publishes -- it stops at files on disk.

Public surface (contract-locked signatures):
  OUT_DIR                                  absolute Path to auto-clip/out
  ensure_out_dir() -> Path                 create OUT_DIR if missing, return it
  run_ffmpeg(args)  -> CompletedProcess    run `ffmpeg  <args>` (ffmpeg on PATH)
  run_ffprobe(args) -> CompletedProcess    run `ffprobe <args>` (ffprobe on PATH)
  extract_frame(video_path, t_seconds, dst_png) -> str
                                           pull ONE frame at t seconds to dst_png (no cv2)
  ffprobe_signalstats(video_path) -> list[dict]
                                           per-frame YAVG/SATAVG/UAVG/VAVG (+ pts time), JSON-parsed

Env note (hub): always invoked through the auto-clip/.venv python on PowerShell; ffmpeg/ffprobe
are expected on PATH (winget Gyan.FFmpeg). We pass capture_output=True so callers get text back
and nothing is written to the user's terminal unless they choose to log it.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Union

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# This file lives at  auto-clip/colorkit/io_utils.py ; OUT_DIR is  auto-clip/out .
# Resolve via __file__ so it is correct no matter the process cwd (the contract says
# "run from the auto-clip/ directory", but we never rely on cwd for the output path).
_THIS = Path(__file__).resolve()
AUTO_CLIP_DIR: Path = _THIS.parent.parent           # auto-clip/
OUT_DIR: Path = AUTO_CLIP_DIR / "out"               # auto-clip/out  (absolute)

# Accept str or Path for any path-shaped argument.
PathLike = Union[str, Path]


def ensure_out_dir() -> Path:
    """Create ``OUT_DIR`` (and parents) if it does not exist; return it as an absolute Path."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUT_DIR


# ---------------------------------------------------------------------------
# subprocess helpers
# ---------------------------------------------------------------------------
def _run(binary: str, args: list, cwd=None) -> subprocess.CompletedProcess:
    """Run ``<binary> <args>`` and return the CompletedProcess (text mode, output captured).

    ``args`` is the list of arguments AFTER the binary name. Every element is stringified so
    callers can pass numbers/Paths without ceremony. We do NOT raise on a non-zero exit code --
    the caller inspects ``.returncode`` / ``.stderr`` and decides (some ffprobe lavfi graphs warn
    on stderr while still succeeding). ``binary`` itself is invoked from PATH. ``cwd`` (optional)
    sets the working directory for the child -- used so ffmpeg ``lut3d`` filters can reference a
    ``.cube`` by BARE FILENAME (motivated by a Windows lut3d path bug, but applied on ALL platforms
    for consistency -- do not remove the cwd staging on Linux/mac).
    """
    cmd = [binary] + [str(a) for a in args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def run_ffmpeg(args: list, cwd=None) -> subprocess.CompletedProcess:
    """Run ``ffmpeg <args>`` (ffmpeg resolved from PATH). Returns the CompletedProcess.

    Does not raise on failure; inspect ``result.returncode`` and ``result.stderr``. Callers
    that want quiet, deterministic behaviour should include ``-y -hide_banner -loglevel error``
    in ``args`` themselves -- this helper stays unopinionated about flags. Pass ``cwd`` to set the
    child working directory (the video path uses this so ``lut3d`` cubes resolve by bare filename).
    """
    return _run("ffmpeg", args, cwd=cwd)


def run_ffprobe(args: list) -> subprocess.CompletedProcess:
    """Run ``ffprobe <args>`` (ffprobe resolved from PATH). Returns the CompletedProcess.

    Like ``run_ffmpeg``, this never raises on a non-zero exit; the caller decides.
    """
    return _run("ffprobe", args)


# ---------------------------------------------------------------------------
# Frame extraction (NO cv2 -- ffmpeg only, by contract)
# ---------------------------------------------------------------------------
def extract_frame(
    video_path: PathLike,
    t_seconds: float,
    dst_png: PathLike,
    vf: "str | None" = None,
    pre_input_args: "list | None" = None,
) -> str:
    """Extract a single frame at ``t_seconds`` from ``video_path`` to ``dst_png`` via ffmpeg.

    Uses ``ffmpeg [pre] -ss <t> -i <v> [-vf <vf>] -frames:v 1 -y dst`` -- the classic reliable
    single-frame grab, with ``-ss`` BEFORE ``-i`` for a fast keyframe seek. No cv2 is involved,
    which keeps this decoder-robust on the 10-bit H.265 MP4s the camera produces. ``t_seconds`` is
    clamped to >= 0.

    ``vf`` (optional): a filtergraph applied during extraction -- used so the representative frame
    is measured in the SAME domain the per-shot render produces (e.g. the HDR->SDR tonemap chain).
    ``pre_input_args`` (optional): extra args inserted BEFORE ``-i`` (e.g. ``["-hwaccel","cuda"]``
    or ``["-init_hw_device","vulkan"]``) so the rep frame can use the same decode path as the render.

    Returns the destination path as a string on success. Raises RuntimeError if ffmpeg fails or
    the output file was not produced, with the last line of ffmpeg's stderr for diagnosis.
    """
    v = str(Path(video_path))
    dst = Path(dst_png)
    dst.parent.mkdir(parents=True, exist_ok=True)
    t = max(0.0, float(t_seconds))

    args = ["-hide_banner", "-loglevel", "error"]
    if pre_input_args:
        args += [str(a) for a in pre_input_args]
    args += ["-ss", f"{t:.6f}", "-i", v]
    if vf:
        args += ["-vf", str(vf)]
    args += ["-frames:v", "1", "-y", str(dst)]
    result = run_ffmpeg(args)

    if result.returncode != 0 or not dst.exists():
        tail = ""
        if result.stderr and result.stderr.strip():
            tail = result.stderr.strip().splitlines()[-1]
        raise RuntimeError(
            f"extract_frame failed at t={t:.3f}s for {v} -> {dst} "
            f"(rc={result.returncode}): {tail or 'no output produced'}"
        )
    return str(dst)


# ---------------------------------------------------------------------------
# Cheap whole-clip triage: per-frame signalstats via ffprobe lavfi
# ---------------------------------------------------------------------------
# The tag keys ffprobe emits under frame.tags for the signalstats filter.
_SIGNALSTATS_TAGS = {
    "lavfi.signalstats.YAVG": "yavg",
    "lavfi.signalstats.SATAVG": "satavg",
    "lavfi.signalstats.UAVG": "uavg",
    "lavfi.signalstats.VAVG": "vavg",
}


def _to_float(value) -> Union[float, None]:
    """Best-effort float parse; return None for missing / unparseable tags (tolerant by contract)."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ffprobe_signalstats(video_path: PathLike) -> list:
    """Return per-frame signalstats for ``video_path`` as a list of dicts.

    Runs::

        ffprobe -f lavfi -i "movie=<v>,signalstats" -show_frames
                -show_entries frame=pts_time,pkt_pts_time,best_effort_timestamp_time:frame_tags=
                              lavfi.signalstats.YAVG,lavfi.signalstats.SATAVG,
                              lavfi.signalstats.UAVG,lavfi.signalstats.VAVG
                -of json

    We request ``pts_time`` first because modern ffmpeg (>= 5.0; the installed Gyan build is 8.1)
    EMITS ``pts_time`` and no longer emits ``pkt_pts_time`` -- requesting the old name alone yields
    an empty/absent field for every frame, which silently kills the brightness-median
    representative-frame selection (it falls back to the shot midpoint for every shot). We still
    request ``pkt_pts_time`` (and ``best_effort_timestamp_time``) so the parse degrades gracefully
    on legacy ffmpeg, then surface whichever one is present under the single ``pts_time`` key.

    and parses the JSON. Each returned dict has keys::

        {"pts_time": float|None, "yavg": float|None, "satavg": float|None,
         "uavg": float|None, "vavg": float|None}

    Missing tags are tolerated -- their value is ``None`` rather than an error -- so a clip whose
    decoder omits, say, SATAVG still yields a usable list. On total failure (ffprobe error or
    unparseable JSON) an EMPTY list is returned; callers (e.g. measure.representative_frame_time)
    are expected to fall back to a shot midpoint, never to crash.

    NOTE: the ``movie=`` source needs the path with backslashes / drive colons escaped for the
    lavfi graph parser; we build that escaping here so Windows paths work.
    """
    movie_src = _movie_lavfi_source(video_path)
    args = [
        "-hide_banner",
        "-loglevel", "error",
        "-f", "lavfi",
        "-i", movie_src,
        "-show_frames",
        "-show_entries",
        "frame=pts_time,pkt_pts_time,best_effort_timestamp_time:frame_tags="
        "lavfi.signalstats.YAVG,lavfi.signalstats.SATAVG,"
        "lavfi.signalstats.UAVG,lavfi.signalstats.VAVG",
        "-of", "json",
    ]
    result = run_ffprobe(args)
    if result.returncode != 0 or not (result.stdout and result.stdout.strip()):
        return []

    try:
        payload = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        return []

    frames = payload.get("frames") or []
    out: list = []
    for frame in frames:
        tags = frame.get("tags") or {}
        row = {
            # ffmpeg 8.1 emits ``pts_time``; old builds emit ``pkt_pts_time``. Prefer the modern
            # name and fall back so this stays correct across ffmpeg versions. measure.py probes
            # ``pts_time`` in its PTS_KEYS, so surfacing it here closes the loop end-to-end.
            "pts_time": _to_float(
                frame.get("pts_time")
                or frame.get("pkt_pts_time")
                or frame.get("best_effort_timestamp_time")
            ),
            "yavg": _to_float(tags.get("lavfi.signalstats.YAVG")),
            "satavg": _to_float(tags.get("lavfi.signalstats.SATAVG")),
            "uavg": _to_float(tags.get("lavfi.signalstats.UAVG")),
            "vavg": _to_float(tags.get("lavfi.signalstats.VAVG")),
        }
        out.append(row)
    return out


def _movie_lavfi_source(video_path: PathLike) -> str:
    """Build the ``movie=<path>,signalstats`` lavfi source string with the path safely escaped.

    The lavfi graph parser treats ``\\``, ``:``, ``'`` and ``,`` as special, so a raw Windows path
    like ``C:\\Users\\...\\clip.mp4`` would break the ``movie=`` source. We forward-slash the path
    (ffmpeg accepts forward slashes on Windows) and backslash-escape the remaining ``:`` and any
    stray special characters so the graph parses on every platform.
    """
    p = str(Path(video_path)).replace("\\", "/")
    # Escape characters that are significant to the lavfi filtergraph option parser.
    for ch in ("\\", ":", "'", ",", "[", "]", ";"):
        p = p.replace(ch, "\\" + ch)
    return f"movie={p},signalstats"
