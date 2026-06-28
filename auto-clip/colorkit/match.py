"""
auto-clip/colorkit/match.py -- Stage 2 of the color pipeline: SHOT MATCHING (continuity).

After each shot has been corrected to neutral (Stage 1), neighbouring shots can still sit at
slightly different exposures / casts -- the per-shot constant correction kills flicker *within* a
shot but can leave visible *jumps at the cut boundaries*. This module reconciles them: it transfers
the color statistics of a chosen HERO (reference) shot onto a source shot so a sequence of cuts
reads as one continuous look.

Method = classic **Reinhard global color transfer** (Reinhard et al., 2001) computed in CIELAB:
match the per-channel mean and standard deviation of the source to the reference. LAB is used
because its L/a/b axes are roughly perceptually decorrelated, so shifting each independently behaves
well. This is a *global, parametric* transform -- a single (shift, scale) pair per LAB channel -- which
is exactly what we want: it is derived ONCE from a representative frame of the shot and then applied
as a CONSTANT transform to every frame of that shot. Constant params => structurally no flicker
(the §0/§3 temporal-consistency rule of the plan).

Two public entry points, by use case:
  - reinhard_transfer(src_bgr, ref_bgr, alpha=1.0) -> bgr
        Pixel-domain transfer for STILLS / representative frames (compute + apply in one call).
        `alpha` blends toward the matched result (0 = untouched src, 1 = full match) so an
        over/under-shooting match can be dialled back -- the plan's "blend with alpha, gate to
        review" guardrail for distribution transfer.
  - compute_match_params(src_bgr, ref_bgr) -> dict
        Returns the same transform as serialisable numbers (per-LAB-channel shift + scale) so the
        caller can apply ONE constant transform across a whole video shot rather than re-deriving it
        per frame. Pairs with `apply_match_params` to reproduce `reinhard_transfer` exactly.

All pixel math is cv2 + numpy only (no GPL deps, no network). LAB here is OpenCV's 8-bit LAB
encoding (L,a,b each 0..255, with a/b biased by +128); statistics are taken in float on that scale,
which is internally consistent for a mean/std match.
"""
from __future__ import annotations

from typing import Optional

import cv2
import numpy as np

# OpenCV's 8-bit LAB channels are quantised to [0, 255]; we clamp back into this range after the
# affine transfer so the round-trip to BGR is well-defined.
_LAB_MIN = 0.0
_LAB_MAX = 255.0
# Floor on a channel's std so a perfectly flat source channel doesn't blow the scale up to infinity.
_STD_EPS = 1e-6


def _to_lab_f32(bgr: np.ndarray) -> np.ndarray:
    """BGR uint8/array -> float32 LAB (OpenCV 8-bit LAB encoding, channels ~0..255)."""
    if bgr is None:
        raise ValueError("input image is None")
    arr = bgr
    if arr.dtype != np.uint8:
        # Accept float 0..1 or 0..255 inputs; normalise to uint8 for a defined cvtColor.
        a = np.asarray(arr, dtype=np.float32)
        if a.size and float(a.max()) <= 1.0:
            a = a * 255.0
        arr = np.clip(a, 0, 255).astype(np.uint8)
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ValueError(f"expected an H x W x 3 BGR image, got shape {getattr(arr, 'shape', None)}")
    lab = cv2.cvtColor(arr, cv2.COLOR_BGR2LAB)
    return lab.astype(np.float32)


def _lab_f32_to_bgr(lab: np.ndarray) -> np.ndarray:
    """float32 LAB (0..255 encoding) -> BGR uint8."""
    lab_u8 = np.clip(lab, _LAB_MIN, _LAB_MAX).astype(np.uint8)
    return cv2.cvtColor(lab_u8, cv2.COLOR_LAB2BGR)


def _channel_stats(lab_f32: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per-channel (L,a,b) mean and std over all pixels. Returns (means[3], stds[3]) float64."""
    flat = lab_f32.reshape(-1, 3)
    means = flat.mean(axis=0)
    stds = flat.std(axis=0)
    return means, stds


def compute_match_params(src_bgr: np.ndarray, ref_bgr: np.ndarray) -> dict:
    """
    Derive the constant per-LAB-channel Reinhard transfer that maps `src_bgr`'s color statistics
    onto `ref_bgr`'s, so it can be applied UNCHANGED to every frame of a shot.

    For each LAB channel c the transform is the affine map that takes the source distribution to the
    reference distribution under a mean/std match:

        out_c = (in_c - src_mean_c) * (ref_std_c / src_std_c) + ref_mean_c
              = in_c * scale_c + shift_c

    with   scale_c = ref_std_c / src_std_c
           shift_c = ref_mean_c - src_mean_c * scale_c

    Returns a plain (JSON-serialisable) dict:
        {
          "space": "lab",                 # OpenCV 8-bit LAB encoding (0..255, a/b +128 biased)
          "scale": [sL, sa, sb],          # per-channel multiplicative gain
          "shift": [tL, ta, tb],          # per-channel additive offset (in the SAME 0..255 space)
          "src_mean": [...], "src_std": [...],   # diagnostics / reproducibility
          "ref_mean": [...], "ref_std": [...],
          "clip": [0.0, 255.0],           # valid output range before LAB->BGR
        }

    The scale/shift pair is the *constant per-shot transform* (plan §4 Stage 2). Feed it to
    `apply_match_params` (or `reinhard_transfer`, which is the fused compute+apply form) on each
    frame; because the numbers never change, the match introduces no temporal flicker.
    """
    src_lab = _to_lab_f32(src_bgr)
    ref_lab = _to_lab_f32(ref_bgr)

    src_mean, src_std = _channel_stats(src_lab)
    ref_mean, ref_std = _channel_stats(ref_lab)

    # Guard flat channels (std ~ 0): a degenerate source channel carries no info to rescale, so we
    # fall back to scale=1 and only re-centre the mean.
    safe_src_std = np.where(src_std < _STD_EPS, 1.0, src_std)
    scale = ref_std / safe_src_std
    scale = np.where(src_std < _STD_EPS, 1.0, scale)
    shift = ref_mean - src_mean * scale

    return {
        "space": "lab",
        "scale": [float(x) for x in scale],
        "shift": [float(x) for x in shift],
        "src_mean": [float(x) for x in src_mean],
        "src_std": [float(x) for x in src_std],
        "ref_mean": [float(x) for x in ref_mean],
        "ref_std": [float(x) for x in ref_std],
        "clip": [_LAB_MIN, _LAB_MAX],
    }


def apply_match_params(bgr: np.ndarray, params: dict, alpha: float = 1.0) -> np.ndarray:
    """
    Apply a constant Reinhard match (from `compute_match_params`) to a BGR frame.

    out = clip( in_lab * scale + shift )  in LAB, then LAB->BGR; optionally blended toward the
    original by `alpha` (0 = no change, 1 = full match). This is the per-frame apply that runs the
    SAME params for every frame of a shot, guaranteeing temporal consistency.
    """
    a = float(np.clip(alpha, 0.0, 1.0))
    if a == 0.0:
        # Round-trip through the same dtype normalisation as the matched path for a fair blend baseline.
        return _lab_f32_to_bgr(_to_lab_f32(bgr))

    scale = np.asarray(params["scale"], dtype=np.float32).reshape(1, 1, 3)
    shift = np.asarray(params["shift"], dtype=np.float32).reshape(1, 1, 3)
    clip_lo, clip_hi = params.get("clip", [_LAB_MIN, _LAB_MAX])

    src_lab = _to_lab_f32(bgr)
    matched_lab = src_lab * scale + shift
    matched_lab = np.clip(matched_lab, float(clip_lo), float(clip_hi))

    if a < 1.0:
        matched_lab = (1.0 - a) * src_lab + a * matched_lab

    return _lab_f32_to_bgr(matched_lab)


def reinhard_transfer(
    src_bgr: np.ndarray,
    ref_bgr: np.ndarray,
    alpha: float = 1.0,
) -> np.ndarray:
    """
    Reinhard LAB mean/std color transfer: re-grade `src_bgr` so its color statistics match
    `ref_bgr`'s, returning a BGR image of the same shape/dtype as the source.

    This is the fused "compute the match from this frame, then apply it to this frame" form -- ideal
    for stills and for the representative frame of a shot (the numbers it derives are identical to
    `compute_match_params(src, ref)`, so you can persist those and replay them across the whole shot
    for flicker-free video). For each LAB channel:

        out = (src - mean(src)) * (std(ref) / std(src)) + mean(ref)

    `alpha` in [0, 1] blends the matched result back toward the untouched source (the plan's
    "transfer overshoots -> blend with alpha, gate to review" guardrail): 0 returns the source,
    1 the full match, 0.5 a half-strength continuity nudge.

    cv2 + numpy only; no network, no GPL.
    """
    params = compute_match_params(src_bgr, ref_bgr)
    return apply_match_params(src_bgr, params, alpha=alpha)


__all__ = [
    "reinhard_transfer",
    "compute_match_params",
    "apply_match_params",
]
