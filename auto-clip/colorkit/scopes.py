"""colorkit.scopes -- headless scopes + self-validation (numpy-only, no GUI, no creative decisions).

The masterclasses are unanimous that **"scopes are ground truth"** (beginners-guide 12:41 "scopes
cannot be deceived"; cullen-master-scopes 08:25; mostyn-read-scopes 00:24) and colorkit had NONE: it
could grade but never *prove* a grade was right. This module reads a corrected representative frame the
way a colorist reads waveform / parade / vectorscope -- on a 0..100 IRE (and 0..1023 10-bit-equivalent)
scale -- and validates it against the DEMONSTRATED targets distilled in
``docs/research/color-masterclass/extracted/`` (frame-cited):

  - black floor OFF 0 but not milky (mostyn 11:52; 2hr 10:55 "clip = lost information");
  - diffuse white ~896/1023 (~87.5 IRE), nothing pinned at 1023 (beginners-guide 07:09/16:15);
  - parade per-channel convergence toward neutral = the balance metric (beginners-guide 17:57-18:55);
  - skin lobe near the ~123 deg vectorscope I-line (cullen-master-scopes 03:20; mostyn 00:42);
  - skin exposure 40-50 IRE bulk / 55-65 hi / ~70 ceiling (mostyn-read-scopes 02:21-05:21).

Everything here is **measurement only** (no decisions, the COLORKIT contract) and **advisory** (a verdict
for the per-shot log + an optional ``--validate`` sidecar) -- it does not alter pixels. It is the ruler
the skin solver and look-stack are tuned against. Pairs with :func:`colorkit.measure.skin_signature`.
"""
from __future__ import annotations

from typing import Dict, Optional

import numpy as np

# Rec.709 luma weights (luma is computed on the display-referred, gamma-encoded signal -- which is
# exactly what a hardware waveform/IRE reads on a graded Rec.709 image).
_R, _G, _B = 0.2126, 0.7152, 0.0722
_CODE10 = 1023.0
SKIN_ILINE_DEG = 123.0  # the vectorscope skin/I-line target (R-Y vs B-Y plane), consistency-first.

__all__ = [
    "waveform", "parade", "clip_stats", "vectorscope", "summary", "validate", "SKIN_ILINE_DEG",
]


def _to_rgb01(bgr) -> "np.ndarray":
    """BGR uint8/float array -> contiguous float RGB in 0..1, shape (...,3)."""
    arr = np.asarray(bgr)
    if arr.ndim != 3 or arr.shape[2] < 3:
        raise ValueError(f"scopes expects an H x W x 3 BGR image, got {getattr(arr, 'shape', None)!r}")
    a = arr[..., :3]
    if a.dtype == np.uint8:
        rgb = a[..., ::-1].astype(np.float64) / 255.0
    else:
        af = a.astype(np.float64)
        mx = float(np.nanmax(af)) if af.size else 1.0
        rgb = np.clip(af[..., ::-1] / (255.0 if mx > 1.5 else 1.0), 0.0, 1.0)
    return np.ascontiguousarray(rgb)


def _luma(rgb01: "np.ndarray") -> "np.ndarray":
    return _R * rgb01[..., 0] + _G * rgb01[..., 1] + _B * rgb01[..., 2]


def waveform(bgr) -> Dict[str, float]:
    """Luma occupancy as IRE percentiles (the waveform read): black floor, mid, diffuse white."""
    L = _luma(_to_rgb01(bgr))
    p = np.percentile(L, [0.1, 1.0, 50.0, 90.0, 99.0, 99.9])
    return {
        "black_p0_1_ire": round(float(p[0] * 100), 2),
        "black_p1_ire": round(float(p[1] * 100), 2),
        "mid_p50_ire": round(float(p[2] * 100), 2),
        "p90_ire": round(float(p[3] * 100), 2),
        "white_p99_ire": round(float(p[4] * 100), 2),
        "white_p99_9_ire": round(float(p[5] * 100), 2),
        "white_p99_code10": round(float(p[4] * _CODE10), 1),
    }


def parade(bgr) -> Dict[str, object]:
    """Per-channel R/G/B low/high points (IRE) + their cross-channel spread (the balance metric).

    A neutrally-balanced image has the three channels' low points (and high points) converged -- a
    large spread is a color cast in that tonal band (beginners-guide 17:57-18:55; best-node-tree 13:04).
    """
    rgb = _to_rgb01(bgr)
    out: Dict[str, object] = {}
    lows, highs = [], []
    for i, ch in enumerate("rgb"):
        lo, hi = np.percentile(rgb[..., i], [1.0, 99.0])
        out[ch] = {"low_ire": round(float(lo * 100), 2), "high_ire": round(float(hi * 100), 2)}
        lows.append(float(lo))
        highs.append(float(hi))
    out["low_spread_ire"] = round((max(lows) - min(lows)) * 100, 2)
    out["high_spread_ire"] = round((max(highs) - min(highs)) * 100, 2)
    return out


def clip_stats(bgr) -> Dict[str, float]:
    """Clip percentages -- '% pinned at 0 / 1023' (2hr 10:55: clipping = information lost)."""
    arr = np.asarray(bgr)[..., :3]
    if arr.dtype != np.uint8:
        af = arr.astype(np.float64)
        mx = float(np.nanmax(af)) if af.size else 1.0
        arr = np.clip(af * (255.0 if mx <= 1.5 else 1.0), 0, 255).astype(np.uint8)
    total = float(arr.shape[0] * arr.shape[1]) or 1.0
    black_all = np.all(arr == 0, axis=-1)
    white_any = np.any(arr >= 255, axis=-1)
    return {
        "pct_black_clip": round(float(np.count_nonzero(black_all)) / total * 100, 3),
        "pct_white_clip": round(float(np.count_nonzero(white_any)) / total * 100, 3),
    }


def vectorscope(bgr) -> Dict[str, float]:
    """Whole-frame hue centroid (deg) + chroma spread in the R-Y / B-Y plane (vectorscope analog).

    Angle convention matches :func:`colorkit.measure.skin_signature` (``atan2(R-Y, B-Y)``) so the skin
    lobe and the I-line target (~123 deg) are read in the same coordinates. Used for shot-match
    hue-mass comparison (cullen-master-scopes 08:52-11:07) and look-direction sanity.
    """
    rgb = _to_rgb01(bgr)
    Y = _luma(rgb)
    ry = rgb[..., 0] - Y
    by = rgb[..., 2] - Y
    chroma = np.sqrt(ry * ry + by * by)
    m = chroma > 0.02
    if int(np.count_nonzero(m)) < 64:
        m = np.ones_like(chroma, dtype=bool)
    ang = float(np.degrees(np.arctan2(float(np.mean(ry[m])), float(np.mean(by[m])))) % 360.0)
    return {
        "hue_centroid_deg": round(ang, 1),
        "mean_chroma": round(float(chroma[m].mean()), 4),
        "sat_p95": round(float(np.percentile(chroma, 95)), 4),
    }


def summary(bgr, skin_sig: Optional[Dict] = None) -> Dict[str, object]:
    """Bundle all scope reads (+ optional skin signature) for the per-shot log."""
    out: Dict[str, object] = {
        "waveform": waveform(bgr), "parade": parade(bgr),
        "clip": clip_stats(bgr), "vectorscope": vectorscope(bgr),
    }
    if skin_sig is not None:
        out["skin"] = skin_sig
    return out


def validate(bgr, skin_sig: Optional[Dict] = None) -> Dict[str, object]:
    """Assert the demonstrated scope targets against ``bgr`` (a corrected rep frame). Advisory.

    Returns ``{checks, n_pass, n_total, verdict, <scopes>}``. Skin checks only run when a
    :func:`colorkit.measure.skin_signature` with enough skin (``skin_frac >= 0.08``) is supplied.
    Thresholds are the demonstrated targets, kept lenient (defaults, not a hard gate -- "scopes guide,
    eyes decide"); they exist so the engine can self-report and later auto-tune.
    """
    wf, pr, cl, vs = waveform(bgr), parade(bgr), clip_stats(bgr), vectorscope(bgr)
    checks: Dict[str, Dict] = {}

    def chk(name: str, ok: bool, value, target: str) -> None:
        checks[name] = {"pass": bool(ok), "value": value, "target": target}

    chk("black_off_floor", wf["black_p1_ire"] >= 0.2, wf["black_p1_ire"], ">=0.2 IRE (not crushed)")
    chk("black_not_milky", wf["black_p1_ire"] <= 8.0, wf["black_p1_ire"], "<=8 IRE (off, not lifted)")
    chk("white_in_range", wf["white_p99_ire"] <= 100.0, wf["white_p99_ire"], "<=100 IRE (~87-100)")
    chk("no_white_clip", cl["pct_white_clip"] <= 1.0, cl["pct_white_clip"], "<=1% pinned at 255")
    chk("no_black_clip", cl["pct_black_clip"] <= 1.0, cl["pct_black_clip"], "<=1% pinned at 0")
    chk("parade_low_converged", pr["low_spread_ire"] <= 6.0, pr["low_spread_ire"], "<=6 IRE R/G/B spread")
    chk("parade_high_converged", pr["high_spread_ire"] <= 12.0, pr["high_spread_ire"], "<=12 IRE spread")

    if skin_sig and skin_sig.get("skin_frac", 0.0) >= 0.08 and skin_sig.get("skin_hue_deg") is not None:
        dev = skin_sig.get("skin_dev_from_iline_deg")
        chk("skin_on_iline", dev is not None and abs(float(dev)) <= 15.0,
            skin_sig.get("skin_hue_deg"), "~123 +/-15 deg")
        p50 = skin_sig.get("skin_L_ire_p50")
        chk("skin_mid_ire", p50 is not None and 38.0 <= float(p50) <= 58.0, p50, "40-50 IRE bulk")
        p90 = skin_sig.get("skin_L_ire_p90")
        chk("skin_hi_not_hot", p90 is not None and float(p90) <= 72.0, p90, "<=70 IRE highlights")

    n_pass = sum(1 for c in checks.values() if c["pass"])
    n_total = len(checks)
    return {
        "checks": checks, "n_pass": n_pass, "n_total": n_total,
        "verdict": f"{n_pass}/{n_total} demonstrated targets met",
        "waveform": wf, "parade": pr, "clip": cl, "vectorscope": vs,
    }
