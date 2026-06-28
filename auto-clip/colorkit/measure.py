"""
colorkit/measure.py -- the MEASUREMENT layer of the headless color engine (pixel-math, no decisions).

Two jobs, per the COLORKIT CONTRACT:

  1. measure_image(bgr) -> Measurement
        Decode-free per-pixel analysis of a single BGR frame already in memory. Computes the
        gray-world channel means (the basis for white-balance correction), the CIE-Lab means
        (perceptual position of the frame's average color), a luma/saturation summary, and a
        boolean low-contrast flag. This is the "where/how is the color" snapshot that correct.py
        turns into params -- measure NEVER decides creative intent (see the plan's MEASUREMENT vs
        DECISION split).

  2. representative_frame_time(shot, video_path) -> float
        Pick ONE timestamp inside a shot to stand in for the whole shot. We choose the frame whose
        whole-frame luma (FFmpeg signalstats YAVG) is the MEDIAN of the shot -- i.e. the most
        "typical"-brightness frame, robust to a flash/cut-frame at either edge. This is the frame
        color.py decodes once and corrects, then applies that ONE correction CONSTANTLY across every
        frame of the shot (the non-negotiable anti-flicker rule). Falls back to the shot midpoint
        whenever signalstats is unavailable or returns nothing usable.

Design notes:
  - cv2 / numpy / skimage are imported lazily inside the functions, not at module top level, so that
    merely importing colorkit (or running luts.py) never drags in the heavy native stack. This mirrors
    the lazy-import discipline the package __init__ uses.
  - signalstats parsing is delegated to io_utils.ffprobe_signalstats(); this module only consumes its
    list[dict] output and is tolerant of missing tags / empty results.
"""

from __future__ import annotations

from typing import Dict, List, Optional, TypedDict


# --------------------------------------------------------------------------------------------------
# Typed data shapes (plain dicts at runtime; these annotations document the contract).
# --------------------------------------------------------------------------------------------------
class Measurement(TypedDict):
    """Per-frame measurement. All values are plain floats / a bool / lists of floats (JSON-safe)."""
    channel_means: List[float]  # gray-world means, [B, G, R] order (matches OpenCV channel order)
    y_avg: float                # mean luma (BT.601 Y) over the frame, 0..255 scale
    sat_avg: float              # mean HSV saturation over the frame, 0..255 scale
    low_contrast: bool          # skimage.exposure.is_low_contrast verdict
    lab_means: List[float]      # CIE-Lab means, [L, a, b] in OpenCV's 8-bit Lab convention


class Shot(TypedDict):
    """A single shot/scene span in seconds (see segment.py)."""
    index: int
    start: float
    end: float


# --------------------------------------------------------------------------------------------------
# 1. measure_image -- per-pixel measurement of a single BGR frame.
# --------------------------------------------------------------------------------------------------
def measure_image(bgr) -> Measurement:
    """Measure a single BGR image (an ``H x W x 3`` uint8/array as returned by ``cv2.imread``).

    Returns a :class:`Measurement` dict:
      - ``channel_means`` : gray-world per-channel means ``[B, G, R]`` (floats, 0..255).
      - ``y_avg``         : mean luma (BT.601), float on the 0..255 scale.
      - ``sat_avg``       : mean HSV saturation, float on the 0..255 scale.
      - ``low_contrast``  : ``skimage.exposure.is_low_contrast(rgb)`` boolean.
      - ``lab_means``     : CIE-Lab channel means ``[L, a, b]`` in OpenCV's 8-bit Lab convention
                            (L in 0..255, a/b in 0..255 with 128 as neutral).

    The gray-world channel means are the raw signal correct.py uses to derive white-balance gains;
    the Lab means give the perceptual average color (and feed shot-matching in match.py). This
    function does no decoding and no I/O -- it operates purely on the array handed to it.
    """
    import cv2
    import numpy as np
    from skimage import exposure

    arr = np.asarray(bgr)
    if arr.ndim != 3 or arr.shape[2] < 3:
        raise ValueError(
            f"measure_image expects an H x W x 3 BGR image, got shape {getattr(arr, 'shape', None)!r}"
        )

    # Work on the 3 color channels only (drop any alpha) and ensure 8-bit for the cv2 conversions.
    bgr8 = arr[:, :, :3]
    if bgr8.dtype != np.uint8:
        # Tolerate float (0..1) or other dtypes by scaling/clipping into 8-bit.
        if np.issubdtype(bgr8.dtype, np.floating):
            scale = 255.0 if float(bgr8.max(initial=0.0)) <= 1.0 else 1.0
            bgr8 = np.clip(bgr8 * scale, 0, 255).astype(np.uint8)
        else:
            bgr8 = np.clip(bgr8, 0, 255).astype(np.uint8)

    # --- Gray-world per-channel means, in OpenCV's native [B, G, R] order. ---
    channel_means = [float(bgr8[:, :, c].mean()) for c in range(3)]

    # --- Mean luma (BT.601 Y). cv2.COLOR_BGR2GRAY uses the BT.601 weights. ---
    gray = cv2.cvtColor(bgr8, cv2.COLOR_BGR2GRAY)
    y_avg = float(gray.mean())

    # --- Mean HSV saturation (the S channel, 0..255). ---
    hsv = cv2.cvtColor(bgr8, cv2.COLOR_BGR2HSV)
    sat_avg = float(hsv[:, :, 1].mean())

    # --- CIE-Lab means in OpenCV's 8-bit Lab convention ([L, a, b], 128 == neutral for a/b). ---
    lab = cv2.cvtColor(bgr8, cv2.COLOR_BGR2LAB)
    lab_means = [float(lab[:, :, c].mean()) for c in range(3)]

    # --- Low-contrast flag (skimage works in RGB; convert from BGR first). ---
    rgb = cv2.cvtColor(bgr8, cv2.COLOR_BGR2RGB)
    try:
        low_contrast = bool(exposure.is_low_contrast(rgb))
    except Exception:
        # Never let the contrast probe sink a measurement; default to "not low contrast".
        low_contrast = False

    return {
        "channel_means": channel_means,
        "y_avg": y_avg,
        "sat_avg": sat_avg,
        "low_contrast": low_contrast,
        "lab_means": lab_means,
    }


# --------------------------------------------------------------------------------------------------
# 1b. scene_stats -- content/colour signals for the auto-look decision layer (decide.py).
# --------------------------------------------------------------------------------------------------
def scene_stats(bgr) -> Dict[str, float]:
    """Cheap content/colour signals used by :mod:`colorkit.decide` to pick a look automatically.

    All values are plain floats (JSON-safe), normalized to 0..1 unless noted:
      - ``skin_frac``  : fraction of pixels in a YCrCb skin-tone range (portrait/talking-head signal).
      - ``green_frac`` : fraction of foliage-green pixels (nature/outdoor signal).
      - ``warmth``     : mean (R-B) / 255 in ``-1..1`` (>0 warm cast, <0 cool cast).
      - ``saturation`` : mean HSV S in 0..1.
      - ``brightness`` : mean luma (BT.601) in 0..1.
      - ``contrast``   : luma standard deviation in 0..1 (spread of tones).

    Pure measurement -- it expresses *what is in the frame*, never a creative decision (that is
    decide.py's job). Operates on the array handed to it; no decoding / I/O.
    """
    import cv2
    import numpy as np

    arr = np.asarray(bgr)
    if arr.ndim != 3 or arr.shape[2] < 3:
        raise ValueError(f"scene_stats expects H x W x 3 BGR, got {getattr(arr, 'shape', None)!r}")
    bgr8 = arr[:, :, :3]
    if bgr8.dtype != np.uint8:
        if np.issubdtype(bgr8.dtype, np.floating):
            scale = 255.0 if float(bgr8.max(initial=0.0)) <= 1.0 else 1.0
            bgr8 = np.clip(bgr8 * scale, 0, 255).astype(np.uint8)
        else:
            bgr8 = np.clip(bgr8, 0, 255).astype(np.uint8)

    total = float(bgr8.shape[0] * bgr8.shape[1]) or 1.0

    # Skin: classic YCrCb rule (robust, lighting-tolerant): Cr in [133,173], Cb in [77,127],
    # with a luma gate to drop crushed/blown pixels.
    ycrcb = cv2.cvtColor(bgr8, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = ycrcb[..., 0], ycrcb[..., 1], ycrcb[..., 2]
    skin = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127) & (Y >= 40) & (Y <= 230)
    skin_frac = float(np.count_nonzero(skin)) / total

    # Foliage green: HSV hue ~35-85 (OpenCV 0-180), with enough saturation + value.
    hsv = cv2.cvtColor(bgr8, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = (H >= 35) & (H <= 85) & (S >= 60) & (V >= 40)
    green_frac = float(np.count_nonzero(green)) / total

    b_mean = float(bgr8[..., 0].mean())
    r_mean = float(bgr8[..., 2].mean())
    warmth = (r_mean - b_mean) / 255.0

    saturation = float(S.mean()) / 255.0
    gray = cv2.cvtColor(bgr8, cv2.COLOR_BGR2GRAY).astype(np.float64)
    brightness = float(gray.mean()) / 255.0
    contrast = float(gray.std()) / 255.0

    return {
        "skin_frac": round(skin_frac, 4),
        "green_frac": round(green_frac, 4),
        "warmth": round(warmth, 4),
        "saturation": round(saturation, 4),
        "brightness": round(brightness, 4),
        "contrast": round(contrast, 4),
    }


# --------------------------------------------------------------------------------------------------
# 1c. skin_signature -- the skin ROI's hue angle + exposure, for the skin-tone-line solver.
# --------------------------------------------------------------------------------------------------
def skin_signature(bgr) -> Dict[str, Optional[float]]:
    """Measure the skin region's hue angle and exposure -- the input to the skin-tone-line solver.

    Masks skin with the same YCrCb rule as :func:`scene_stats` (Cr 133-173, Cb 77-127, luma-gated),
    then, on the skin pixels only (a bright background fools a whole-frame mean -- mostyn-read-scopes
    04:22-04:31), measures:
      - ``skin_frac``               : fraction of the frame that is skin.
      - ``skin_hue_deg``            : hue angle in the R-Y / B-Y vectorscope plane (``atan2(R-Y, B-Y)``,
                                      same convention as :func:`colorkit.scopes.vectorscope`); the
                                      demonstrated skin / I-line target is ~123 deg.
      - ``skin_dev_from_iline_deg`` : signed degrees off the 123 deg I-line (consistency-first; film
                                      references trend slightly green of it -- mostyn 04:55/05:37).
      - ``skin_L_ire_p50``/``_p90`` : Rec.709 luma of the skin ROI in IRE; demonstrated targets are a
                                      40-50 IRE bulk, 55-65 highlights, ~70 ceiling (mostyn 02:21-05:21).
      - ``skin_chroma``             : mean skin chroma magnitude (R-Y/B-Y), 0..~1.

    Returns ``skin_frac`` always; the rest are ``None`` when there is too little skin to trust
    (< ~1% of the frame or < 200 px). Pure measurement -- it steers nothing (correct.py does that).
    """
    import cv2
    import numpy as np

    arr = np.asarray(bgr)
    if arr.ndim != 3 or arr.shape[2] < 3:
        raise ValueError(f"skin_signature expects H x W x 3 BGR, got {getattr(arr, 'shape', None)!r}")
    bgr8 = arr[:, :, :3]
    if bgr8.dtype != np.uint8:
        if np.issubdtype(bgr8.dtype, np.floating):
            scale = 255.0 if float(bgr8.max(initial=0.0)) <= 1.0 else 1.0
            bgr8 = np.clip(bgr8 * scale, 0, 255).astype(np.uint8)
        else:
            bgr8 = np.clip(bgr8, 0, 255).astype(np.uint8)

    total = float(bgr8.shape[0] * bgr8.shape[1]) or 1.0
    ycrcb = cv2.cvtColor(bgr8, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = ycrcb[..., 0], ycrcb[..., 1], ycrcb[..., 2]
    skin = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127) & (Y >= 40) & (Y <= 230)
    count = int(np.count_nonzero(skin))

    res: Dict[str, Optional[float]] = {
        "skin_frac": round(count / total, 4),
        "skin_hue_deg": None, "skin_dev_from_iline_deg": None,
        "skin_L_ire_p50": None, "skin_L_ire_p90": None, "skin_chroma": None,
    }
    if count < max(200, int(0.01 * total)):
        return res

    rgb = bgr8[..., ::-1].astype(np.float64) / 255.0  # BGR->RGB, 0..1
    L = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    Ls = L[skin]
    p50, p90 = np.percentile(Ls, [50.0, 90.0])

    Rs, Bs = rgb[..., 0][skin], rgb[..., 2][skin]
    ry = float(np.mean(Rs - Ls))
    by = float(np.mean(Bs - Ls))
    ang = float(np.degrees(np.arctan2(ry, by)) % 360.0)
    chroma = float(np.mean(np.sqrt((Rs - Ls) ** 2 + (Bs - Ls) ** 2)))

    res.update(
        skin_hue_deg=round(ang, 1),
        skin_dev_from_iline_deg=round(ang - 123.0, 1),
        skin_L_ire_p50=round(float(p50) * 100, 1),
        skin_L_ire_p90=round(float(p90) * 100, 1),
        skin_chroma=round(chroma, 4),
    )
    return res


# --------------------------------------------------------------------------------------------------
# 2. representative_frame_time -- brightness-median frame time for a shot.
# --------------------------------------------------------------------------------------------------
def _shot_bounds(shot: Shot) -> tuple[float, float]:
    """Return ``(start, end)`` as floats, defensively coercing and ordering them."""
    start = float(shot.get("start", 0.0))
    end = float(shot.get("end", start))
    if end < start:
        start, end = end, start
    return start, end


def _median_pts(times: List[float]) -> Optional[float]:
    """Return the lower-median element of ``times`` (an actual frame time, not an average)."""
    if not times:
        return None
    ordered = sorted(times)
    # Lower median: for even counts pick the lower-middle so the result is always a real frame time.
    return ordered[(len(ordered) - 1) // 2]


def representative_frame_time(shot: Shot, video_path: str) -> float:
    """Choose the timestamp of the brightness-MEDIAN frame within ``shot``.

    Uses :func:`io_utils.ffprobe_signalstats` to read each frame's whole-frame luma (``YAVG``) and
    presentation time (``pkt_pts_time``), keeps only the frames whose pts falls inside the shot's
    ``[start, end]`` span, then returns the pts of the frame whose YAVG is the median of that set.

    The median (not mean) makes the pick robust: it lands on an actually-present frame and ignores a
    lone bright flash or a fade-frame at a cut boundary. This is the single frame color.py decodes and
    corrects, applying that one correction constantly across the whole shot (anti-flicker rule).

    Fallbacks (never raises on a measurement gap):
      - signalstats import/parse fails, or yields no frames inside the span -> return the shot
        midpoint ``(start + end) / 2``.
    """
    start, end = _shot_bounds(shot)
    midpoint = (start + end) / 2.0

    # Pull per-frame signalstats; tolerate any failure by degrading to the midpoint.
    try:
        from . import io_utils  # package-relative; io_utils owns the ffprobe invocation + JSON parse
        frames = io_utils.ffprobe_signalstats(str(video_path))
    except Exception:
        return midpoint

    if not frames:
        return midpoint

    # Collect (pts_time, yavg) for frames whose pts lies inside the shot span and has a usable YAVG.
    # signalstats keys vary by how io_utils flattens the JSON, so probe a few likely names.
    PTS_KEYS = ("pkt_pts_time", "pts_time", "best_effort_timestamp_time", "time")
    YAVG_KEYS = ("YAVG", "lavfi.signalstats.YAVG", "yavg")

    def _get(d: Dict, keys) -> Optional[float]:
        for k in keys:
            if k in d and d[k] is not None and d[k] != "":
                try:
                    return float(d[k])
                except (TypeError, ValueError):
                    continue
        return None

    # Small tolerance so a frame landing exactly on a boundary (or rounding) still counts.
    eps = 1e-3
    candidates: List[tuple[float, float]] = []  # (yavg, pts)
    for fr in frames:
        if not isinstance(fr, dict):
            continue
        pts = _get(fr, PTS_KEYS)
        yavg = _get(fr, YAVG_KEYS)
        if pts is None or yavg is None:
            continue
        if (start - eps) <= pts <= (end + eps):
            candidates.append((yavg, pts))

    if not candidates:
        # No in-span frames (e.g. signalstats sampled coarsely, or span shorter than a frame).
        return midpoint

    # Median BY YAVG: sort on luma, take the lower-median entry, return ITS pts (a real frame time).
    candidates.sort(key=lambda yp: yp[0])
    _, chosen_pts = candidates[(len(candidates) - 1) // 2]
    return float(chosen_pts)


# Convenience alias used by some callers / tests; keeps the YAVG-median semantics explicit.
def brightness_median_time(shot: Shot, video_path: str) -> float:
    """Alias for :func:`representative_frame_time` (brightness-median frame selection)."""
    return representative_frame_time(shot, video_path)


__all__ = [
    "Measurement",
    "Shot",
    "measure_image",
    "scene_stats",
    "skin_signature",
    "representative_frame_time",
    "brightness_median_time",
]
