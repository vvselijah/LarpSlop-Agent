"""colorkit.correct — Stage 0-4 "DEVELOP": measure a frame, emit grey-anchored correction params, apply them.

**v2 rewrite (2026-06-24).** v1 pushed the *mean* luma to a fixed 0.46 and did a *linear* contrast
stretch on gamma-encoded values, then a contrasty LUT on top — the "washed / overblown / one-tap
filter" look (see ``docs/plans/2026-06-24-color-v2-grading-spec.md`` §1). v2 replaces that with a
**linear-light develop** that hits real colorist scope targets:

    encoded --EOTF--> linear --[WB, black point, exposure(median->0.18), contrast, highlight shoulder]
                                                                              --OETF--> encoded --[vibrance]

The develop is one constant transform per shot (the non-negotiable anti-flicker rule). It is expressed
as a single pure function :func:`develop_fn` (encoded RGB -> encoded RGB), which is used three ways:
  1. :func:`apply_correction_image` — exact vectorized apply for stills / before-after previews.
  2. :func:`bake_develop_cube` — sample it onto a grid and write a ``.cube`` so the VIDEO path can
     apply the SAME transform as a constant per-shot ``lut3d`` (flicker-free, and able to express
     linear-light filmic math that ffmpeg ``eq`` cannot).
  3. (still + video share one source of truth — no drift between preview and render.)

Key fixes vs v1 (all from the verified research):
- Exposure anchors the **median** mid-tone luma to **0.18 linear** (robust to bright outliers), not
  the mean — kills the over-brightening.
- A per-channel **black point** (low percentile, linear) neutralizes casts (aligns parade blacks) and
  removes milky blacks — without crushing to 0.
- The only contrast is ONE gentle **pivoted** contrast around 0.18 (never a 0-pivot linear stretch),
  applied on luminance — no contrast-stacking.
- A C1 **highlight soft-clip** on luminance protects highlights (no hard clip), hue-safe.
- **Shades-of-Gray** WB (Minkowski p=6) replaces gray-world (robust when one color dominates).
- **Vibrance** (protects saturated pixels + skin) replaces the global saturation multiplier.

``Params`` (plain dict, JSON-safe)::

    {
      "version": 2,
      "transfer": "srgb",                 # linearization model
      "wb_gains": [gB, gG, gR],           # multiplicative, green-anchored, applied in LINEAR
      "black":    [bB, bG, bR],           # per-channel black point in LINEAR (subtract + renorm)
      "exposure": float,                  # linear gain: median mid-tone luma -> 0.18
      "contrast": float,                  # pivoted-contrast amount c (1.0 = none)
      "shoulder": {"knee": float, "ceiling": float},
      "desat_hi": float,                  # highlight desaturation amount (linear)
      "vibrance": float,                  # vibrance amount (encoded domain)
    }
"""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np

try:
    import cv2  # used by apply_correction_image / WB measurement on real frames
except Exception:  # pragma: no cover - cv2 guaranteed present per contract
    cv2 = None  # type: ignore

from . import tonemap as tm

__all__ = [
    "compute_correction",
    "develop_fn",
    "apply_correction_image",
    "bake_develop_cube",
    "default_params",
]


# --- tuning constants (the v2 develop defaults) -----------------------------
_MID = tm.MIDDLE_GREY                # 0.18 linear exposure/contrast anchor
_BLACK_PCT = 0.5                     # per-channel black point percentile (linear)
_BLACK_MAX = 0.05                    # clamp black point so we never crush
_EXP_LO_PCT, _EXP_HI_PCT = 2.0, 98.0  # mid-tone mask for the exposure median (drop crushed/clipped)
_EXPOSURE_CLAMP = (0.25, 4.0)        # linear exposure gain bounds
_WB_GAIN_CLAMP = (0.5, 2.0)          # per-channel WB gain bounds (research: 0.5..2.0)
_WB_MINKOWSKI_P = 6.0                # Shades-of-Gray norm (p=1 gray-world, p->inf white-patch)
_DEFAULT_CONTRAST = 1.08             # ONE gentle contrast (tasteful 1.05..1.25)
_DEFAULT_KNEE = 0.82                 # highlight shoulder knee (linear)
_DEFAULT_DESAT_HI = 0.20             # gentle highlight desaturation
_DEFAULT_VIBRANCE = 0.18             # gentle vibrance

# --- low-light "hard scene" guards (2026-06-24 task #8 hardening) ------------
# These engage ONLY when a scene DEMANDS a large lift (i.e. it's genuinely dark): a well-exposed
# scene's lift is < the knee and its demanded gain is < _WB_FULL_LIFT, so both guards are no-ops and
# the approved v2 look is byte-identical. They fix the night/mixed-light over-warm + over-lift
# (gray-world WB over-warms dark artificial light; the median->0.18 exposure slams its 4x ceiling).
_EXP_KNEE = 2.0                      # exposure LIFT at/below this is linear (normal scenes untouched)
_EXP_SOFT_CEIL = 3.2                 # ...above it the lift soft-rolls toward this (no hard 4x blowout)
_EXP_HI_PROTECT_PCT = 97.5           # broad-highlight percentile for blow-out protection (sky, not speculars)
_EXP_HI_TARGET = 0.72                # ...cap the lift so that percentile lands here in linear (under the knee)
_WB_FULL_LIFT = 1.5                  # WB at full strength when the demanded lift <= this
_WB_FADE_LIFT = 4.0                  # ...fading to _WB_MIN_STRENGTH by this demanded lift (dark scene)
_WB_MIN_STRENGTH = 0.5               # never fade WB below half (still neutralize some cast)

# --- G1: skin-tone-line solver (2026-06-26) ---------------------------------
# The develop neutralizes the OVERALL cast (shades-of-gray WB) but can leave/push skin a few degrees
# off the demonstrated ~123 deg vectorscope I-line (measured: the approved talking-head drifts to
# ~136.9 deg post-develop). The solver re-balances GLOBALLY (a small luma-preserving WB tint folded
# back into wb_gains -- never a hard skin key, per the research consensus "fix skin globally, never
# key it") so skin lands closer to the line, plus a conservative two-band skin-exposure trim. It is
# self-gating: it only fires when skin is a real part of the frame, so a non-portrait clip's develop
# is byte-identical to before. Caps keep it a *nudge*, not a snap (cullen 11:40 "judge by eye, reject
# hard snap"). All evidence: docs/research/color-masterclass/extracted/engine_gap_map.md (P0).
_SKIN_ILINE_DEG = 123.0              # the vectorscope skin/I-line target (== scopes.SKIN_ILINE_DEG)
_SKIN_FRAC_MIN = 0.08               # GATE: only solve when skin is >= this fraction of the frame
_SKIN_DEADBAND_DEG = 3.0           # don't chase a drift smaller than this (consistency > exactness)
_SKIN_MAX_CORRECT_FRAC = 0.6       # correct at most this fraction of the deviation (soft, no snap)
_SKIN_MAX_MOVE_DEG = 10.0          # absolute cap on the attempted hue move (deg)
_SKIN_TINT_CLAMP = (0.92, 1.08)    # per-channel cap on the skin tint (<=8%) -> hard bound on the move
_SKIN_SOLVE_MAXDIM = 480           # downscale the rep frame to this for the (global) skin solve
_SKIN_SAMPLE_MAX = 4000            # cap skin pixels fed to the tint search (speed)
_SKIN_ERODE_KSIZE = 3              # erode the skin mask -> require a COHERENT region (a face is a
_SKIN_ERODE_ITER = 2              #   blob; scattered warm/tan pixels on a landscape are not) so the
#                                     gate doesn't false-fire on non-portrait footage (byte-identical).
_SKIN_TINT_M = (-0.06, 0.06, 7)    # green<->magenta search axis (lo, hi, n)
_SKIN_TINT_W = (-0.05, 0.05, 5)    # warm<->cool search axis (lo, hi, n)
# two-band skin EXPOSURE trim (mostyn-read-scopes 02:21-05:21): 40-50 IRE bulk, 55-65 hi, ~70 ceiling.
# A GLOBAL exposure trim toward skin is blunt (it moves the whole frame), so keep it a gentle ASSIST:
# only fire when skin is clearly out of band, aim for the nearest band EDGE (not centre), cap <=6%.
_SKIN_IRE_LO, _SKIN_IRE_HI = 40.0, 52.0   # the good skin-midtone (p50) band edges (trim targets these)
_SKIN_IRE_TRIM_LO, _SKIN_IRE_TRIM_HI = 36.0, 56.0  # only trim when p50 is OUTSIDE this wider band
_SKIN_EXP_TRIM_CLAMP = (0.94, 1.06)  # cap the skin exposure trim factor (<=6%, blunt lever -> gentle)
_SKIN_IRE_HOT = 70.0               # warn when skin highlights (p90) exceed this (over-exposed skin)
_LUMA_W = (0.2126, 0.7152, 0.0722)  # Rec.709 luma weights (R,G,B) -- matches measure/scopes

# --- G1b: skin-LOCAL exposure (color-qualifier lift, 2026-06-27) -------------
# A GLOBAL exposure trim (above) cannot lift genuinely under-exposed skin (~22 IRE on the interview
# clip) without lifting the whole background, so it is capped tiny (<=6%). G1b instead lifts ONLY
# skin-CHROMATICITY colours, as a smooth function of COLOUR (not pixel position): a pure encoded
# RGB->RGB stage folded into develop_fn, so it BAKES into the constant per-shot cube -> flicker-free
# (a spatial/keyed mask would flicker frame-to-frame; the baton's explicit choice). It is gated +
# capped + strength-scaled exactly like G1, and emitted ONLY when a real eroded-skin region is present
# AND skin is still below band after the global trim -> develops without under-exposed skin are
# byte-identical (develop_fn skips the stage when no "skin_lift" gain is present). Documented limit:
# other skin-chromaticity objects (wood, sand) lift too -- the unavoidable price of a bakeable
# colour-qualifier over a (flickering) spatial face mask.
_SKIN_QUAL_CR = (133.0, 173.0)     # Cr box (0..255 YCrCb), == _skin_mask
_SKIN_QUAL_CB = (77.0, 127.0)      # Cb box
_SKIN_QUAL_Y = (40.0, 210.0)       # luma box (slightly under _skin_mask's 230 so near-clip isn't lifted)
_SKIN_QUAL_SOFT = 14.0             # smoothstep ramp width (codes) -> soft edges, no LUT banding
_SKIN_QUAL_CHROMA_MIN = 10.0       # require real chroma (dist from neutral Cr=Cb=128) -> reject neutrals
_SKIN_QUAL_CHROMA_SOFT = 12.0      #   ...which sit at the skin box's edge (Cr~128) and would else leak
_SKIN_LIFT_TRIGGER_IRE = 36.0      # only add the local lift when post-trim skin p50 is below this
_SKIN_LIFT_TARGET_IRE = 42.0       # aim skin p50 here (lower-middle of the 40-50 good band)
_SKIN_LIFT_GAIN_CLAMP = (1.0, 1.6)  # cap the encoded luma gain (<= +60%; skin-only, still bounded)


def _clamp(v: float, lo: float, hi: float) -> float:
    return float(max(lo, min(hi, v)))


def _round(v: float, n: int = 5) -> float:
    return float(round(float(v), n))


def _soft_knee_gain(g: float, knee: float, ceil: float) -> float:
    """Soft-compress an exposure LIFT above ``knee`` toward asymptote ``ceil`` (C1, never hard-clips).

    ``g <= knee`` (including any darken ``g < 1``) is returned unchanged, so a normally-exposed scene's
    exposure is untouched. Above the knee the lift rolls off rationally toward ``ceil`` instead of
    climbing to (and clamping at) the hard 4x ceiling -- a genuinely dark scene is still lifted, but
    not blown out (which is what amplified the colour cast + noise on the night footage).
    """
    g = float(g)
    if g <= knee:
        return g
    rng = max(1e-6, ceil - knee)
    over = g - knee
    return knee + rng * over / (over + rng)


def _lowlight_wb_strength(lift_demand: float) -> float:
    """WB confidence 1.0 -> ``_WB_MIN_STRENGTH`` as the demanded lift grows ``_WB_FULL_LIFT``->``_WB_FADE_LIFT``.

    Gray-world / Shades-of-Gray WB is unreliable on dark, mixed-artificial-light scenes and tends to
    over-warm them (the night-scene green/warm cast). We fade the WB correction toward neutral exactly
    where it is least trustworthy -- in low light -- and keep it at full strength for normal scenes.
    """
    d = float(lift_demand)
    if d <= _WB_FULL_LIFT:
        return 1.0
    if d >= _WB_FADE_LIFT:
        return _WB_MIN_STRENGTH
    t = (d - _WB_FULL_LIFT) / (_WB_FADE_LIFT - _WB_FULL_LIFT)
    return 1.0 - (1.0 - _WB_MIN_STRENGTH) * t


def default_params() -> Dict[str, object]:
    """Identity-ish develop params (no measurement); used as a safe fallback."""
    return {
        "version": 2, "transfer": "srgb",
        "wb_gains": [1.0, 1.0, 1.0], "black": [0.0, 0.0, 0.0],
        "exposure": 1.0, "contrast": 1.0,
        "shoulder": {"knee": _DEFAULT_KNEE, "ceiling": 1.0},
        "desat_hi": 0.0, "vibrance": 0.0,
    }


# --------------------------------------------------------------------------- #
# MEASUREMENT -> params                                                       #
# --------------------------------------------------------------------------- #
def _to_rgb01(bgr: "np.ndarray") -> "np.ndarray":
    """BGR uint8/array -> float RGB in 0..1, shape (...,3)."""
    arr = np.asarray(bgr)
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    rgb = arr[..., 2::-1].astype(np.float64) / 255.0  # BGR->RGB, normalize
    return np.ascontiguousarray(rgb)


def _shades_of_gray_gains(lin: "np.ndarray", p: float = _WB_MINKOWSKI_P) -> List[float]:
    """Shades-of-Gray white-balance gains [gB, gG, gR], green-anchored, from LINEAR RGB.

    Illuminant estimate per channel = the Minkowski p-norm mean ``(mean(c**p))**(1/p)``; gains pull
    each channel toward the common grey. p=1 is gray-world, p->inf is white-patch; p~6 is the robust
    middle ground (research lane `washed-fix`). Clipped (>0.98) and near-black (<0.02) pixels are
    excluded so a blown window or a crushed shadow can't bias the estimate.
    """
    flat = lin.reshape(-1, 3)  # R,G,B
    enc = flat ** (1.0 / 2.4)  # rough perceptual for the mask thresholds
    mask = np.all((enc > 0.02) & (enc < 0.98), axis=1)
    use = flat[mask] if mask.sum() > 64 else flat
    p = float(p)
    illum = np.power(np.mean(np.power(np.clip(use, 0, None), p), axis=0), 1.0 / p) + 1e-9  # [R,G,B]
    gray = float(illum.mean())
    gains_rgb = gray / illum  # [gR, gG, gB]
    gain_g = gains_rgb[1] if gains_rgb[1] > 1e-6 else 1.0
    gains_rgb = gains_rgb / gain_g  # green-anchored
    gR = _clamp(float(gains_rgb[0]), *_WB_GAIN_CLAMP)
    gG = _clamp(float(gains_rgb[1]), *_WB_GAIN_CLAMP)
    gB = _clamp(float(gains_rgb[2]), *_WB_GAIN_CLAMP)
    return [_round(gB), _round(gG), _round(gR)]  # BGR order to match the contract


# --------------------------------------------------------------------------- #
# G1: the skin-tone-line solver (measure on the developed frame, fold a global  #
#     luma-preserving tint back into wb_gains -> skin nearer the I-line)        #
# --------------------------------------------------------------------------- #
def _downscale_rgb(rgb: "np.ndarray", maxdim: int) -> "np.ndarray":
    """Area-downscale an encoded RGB float array so its long side <= ``maxdim`` (global solve only)."""
    h, w = rgb.shape[:2]
    m = max(h, w)
    if m <= maxdim:
        return rgb
    s = maxdim / float(m)
    nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
    if cv2 is not None:
        return cv2.resize(rgb.astype(np.float32), (nw, nh),
                          interpolation=cv2.INTER_AREA).astype(np.float64)
    ys = np.linspace(0, h - 1, nh).astype(int)
    xs = np.linspace(0, w - 1, nw).astype(int)
    return rgb[np.ix_(ys, xs)]


def _skin_mask(dev_rgb: "np.ndarray", erode: bool = True) -> "np.ndarray":
    """Boolean skin mask of an encoded RGB frame, via the same YCrCb rule as measure.skin_signature.

    When ``erode`` (default), the raw mask is morphologically eroded so only a SPATIALLY COHERENT
    skin region survives -- a real face is a contiguous blob, but scattered warm/tan pixels on a
    landscape (or noise) erode away. This is what keeps the G1 gate from false-firing on non-portrait
    footage, so those develops stay byte-identical. (Operates on a 2-D image; not used on (N,3) samples.)
    """
    u8 = np.clip(np.rint(dev_rgb * 255.0), 0, 255).astype(np.uint8)
    if cv2 is not None:
        bgr = np.ascontiguousarray(u8[..., ::-1])
        ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
        Y, Cr, Cb = ycrcb[..., 0], ycrcb[..., 1], ycrcb[..., 2]
    else:  # pragma: no cover - cv2 present per contract
        R, G, B = (u8[..., 0].astype(np.float64), u8[..., 1].astype(np.float64),
                   u8[..., 2].astype(np.float64))
        Y = 0.299 * R + 0.587 * G + 0.114 * B
        Cr = (R - Y) * 0.713 + 128.0
        Cb = (B - Y) * 0.564 + 128.0
    mask = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127) & (Y >= 40) & (Y <= 230)
    if erode and cv2 is not None and _SKIN_ERODE_ITER > 0 and mask.ndim == 2:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (_SKIN_ERODE_KSIZE, _SKIN_ERODE_KSIZE))
        mask = cv2.erode(mask.astype(np.uint8), k, iterations=_SKIN_ERODE_ITER).astype(bool)
    return mask


def _skin_angle_ire(dev_skin: "np.ndarray") -> tuple:
    """(hue_deg, L_ire_p50, L_ire_p90, chroma) of an (N,3) encoded RGB skin sample.

    Hue is the mean ``atan2(R-Y, B-Y)`` and IRE the Rec.709 luma percentiles -- the exact conventions
    of :func:`colorkit.measure.skin_signature` / :func:`colorkit.scopes.vectorscope`, so the solver
    optimizes the very quantity the ruler reports.
    """
    R, G, B = dev_skin[..., 0], dev_skin[..., 1], dev_skin[..., 2]
    L = _LUMA_W[0] * R + _LUMA_W[1] * G + _LUMA_W[2] * B
    ry = float(np.mean(R - L))
    by = float(np.mean(B - L))
    ang = float(np.degrees(np.arctan2(ry, by)) % 360.0)
    p50, p90 = np.percentile(L, [50.0, 90.0])
    chroma = float(np.mean(np.sqrt((R - L) ** 2 + (B - L) ** 2)))
    return ang, float(p50 * 100.0), float(p90 * 100.0), chroma


def _apply_skin_solve(enc_rgb: "np.ndarray", params: Dict[str, object],
                      target_deg: float, strength: float,
                      exp_hi_cap: float = float("inf")) -> Dict[str, object]:
    """G1: nudge skin toward ``target_deg`` on the I-line + trim skin exposure to band. Returns params.

    Develops a downscaled copy of the encoded rep frame with the base ``params``, masks skin, and (only
    if skin is a real part of the frame and clearly off the line) searches a SMALL, luma-preserving,
    capped WB tint that moves the skin hue partway back toward the line, folds it into ``wb_gains``,
    then conservatively trims ``exposure`` if skin sits outside the 40-52 IRE band. The tint is global
    (never a skin key) and capped (<=8%/channel, <=60% of the drift, <=10 deg) so it is a nudge, not a
    snap. Attaches a JSON-safe ``"skin"`` diagnostic. On too-little-skin / in-band it returns the base
    params unchanged (so non-portrait develops stay byte-identical). ``strength`` scales the whole
    correction toward identity (strength 0 -> no change), matching the rest of the develop.
    """
    small = _downscale_rgb(np.asarray(enc_rgb, dtype=np.float64), _SKIN_SOLVE_MAXDIM)
    dev = develop_fn(params)(small)               # developed encoded RGB (display-referred domain)
    mask = _skin_mask(dev)
    total = int(mask.size)
    frac = float(np.count_nonzero(mask)) / max(1, total)
    diag: Dict[str, object] = {"frac": round(frac, 4), "target_deg": round(float(target_deg), 1)}

    if frac < _SKIN_FRAC_MIN:
        return {**params, "skin": {**diag, "applied": False, "reason": "insufficient_skin"}}

    dev_skin = dev[mask]
    ang0, p50_0, p90_0, chroma0 = _skin_angle_ire(dev_skin)
    dev0 = ang0 - target_deg
    diag.update(hue_before=round(ang0, 1), dev_before=round(dev0, 1),
                L_ire_p50_before=round(p50_0, 1), L_ire_p90_before=round(p90_0, 1))

    # Source (pre-develop) skin pixels the tint search re-develops, subsampled deterministically.
    src_skin = small[mask]
    if src_skin.shape[0] > _SKIN_SAMPLE_MAX:
        src_skin = src_skin[:: int(np.ceil(src_skin.shape[0] / _SKIN_SAMPLE_MAX))]

    if abs(dev0) <= _SKIN_DEADBAND_DEG and _SKIN_IRE_TRIM_LO <= p50_0 <= _SKIN_IRE_TRIM_HI:
        return {**params, "skin": {**diag, "applied": False, "reason": "in_band",
                                   "hue_after": round(ang0, 1), "dev_after": round(dev0, 1)}}

    base_wb = np.array([float(params["wb_gains"][2]), float(params["wb_gains"][1]),
                        float(params["wb_gains"][0])], dtype=np.float64)  # -> [R,G,B]
    Lw = np.array(_LUMA_W, dtype=np.float64)

    best = None  # ((err_deg, tint_mag), wb_rgb, tint, ang)
    if abs(dev0) > _SKIN_DEADBAND_DEG:
        aim = ang0 - float(np.clip(dev0 * _SKIN_MAX_CORRECT_FRAC,
                                   -_SKIN_MAX_MOVE_DEG, _SKIN_MAX_MOVE_DEG))
        for m in np.linspace(*_SKIN_TINT_M):
            for w in np.linspace(*_SKIN_TINT_W):
                # green<->magenta (m): boost R&B, cut G; warm<->cool (w): R up, B down.
                t = np.array([(1.0 + m) * (1.0 + w), (1.0 - m), (1.0 + m) * (1.0 - w)])
                t = np.clip(t, _SKIN_TINT_CLAMP[0], _SKIN_TINT_CLAMP[1])  # bound the raw move FIRST
                t = t / float(np.dot(t, Lw))                             # THEN normalize -> luma-preserving
                cand_wb = np.clip(base_wb * (1.0 + (t - 1.0) * strength),
                                  _WB_GAIN_CLAMP[0], _WB_GAIN_CLAMP[1])
                cand = {**params, "wb_gains": [cand_wb[2], cand_wb[1], cand_wb[0]]}  # -> BGR
                cang, _, _, _ = _skin_angle_ire(develop_fn(cand)(src_skin))
                d_ang = abs((cang - aim + 180.0) % 360.0 - 180.0)        # wrapped angular distance
                score = (d_ang, float(np.sum(np.abs(t - 1.0))))
                if best is None or score < best[0]:
                    best = (score, cand_wb, t, cang)

    if best is not None:
        _, best_wb, best_t, _ = best
        params = {**params, "wb_gains": [_round(float(best_wb[2])), _round(float(best_wb[1])),
                                         _round(float(best_wb[0]))]}
        diag["tint"] = [round(float(x), 4) for x in best_t]

    # Two-band skin EXPOSURE trim: re-measure with the chosen tint; nudge exposure if skin off-band.
    sdev = develop_fn(params)(src_skin)
    ang1, p50_1, p90_1, _ = _skin_angle_ire(sdev)
    exp_trim = 1.0
    # Only trim when skin is CLEARLY out of band; aim for the nearest GOOD-band edge (small move).
    target_ire = (_SKIN_IRE_LO if p50_1 < _SKIN_IRE_TRIM_LO
                  else _SKIN_IRE_HI if p50_1 > _SKIN_IRE_TRIM_HI else None)
    if target_ire is not None:
        # display IRE ratio -> linear exposure factor (~gamma 2.4), strength-scaled + clamped small.
        factor = (target_ire / max(p50_1, 1e-3)) ** 2.4
        factor = float(np.clip(1.0 + (factor - 1.0) * strength, *_SKIN_EXP_TRIM_CLAMP))
        prev_exp = float(params["exposure"])
        # Respect the highlight-protection ceiling: a dark-skin LIFT must not push exposure back above
        # what the highlight cap allowed (else it re-inflates a protected bright background). A DARKEN
        # is always safe. exp_trim is reported as the EFFECTIVE (post-ceiling) factor.
        new_exp = min(prev_exp * factor, exp_hi_cap)
        exp_trim = new_exp / prev_exp if prev_exp > 1e-6 else 1.0
        if abs(exp_trim - 1.0) > 1e-4:
            params = {**params, "exposure": _round(new_exp)}
            sdev = develop_fn(params)(src_skin)
            ang1, p50_1, p90_1, _ = _skin_angle_ire(sdev)

    # G1b: skin-LOCAL exposure lift (colour-qualifier, bakeable) for skin STILL under-band after the
    # global trim. A GLOBAL exposure can't lift dark skin without the whole background, so lift only
    # skin-chromaticity colours via a constant develop_fn stage (-> bakes into the cube, flicker-free).
    # Gated (only when skin is genuinely below band), capped (<=+60%), and strength-scaled like G1.
    skin_lift = 1.0
    if p50_1 < _SKIN_LIFT_TRIGGER_IRE:
        # encoded-IRE ratio ~= the encoded luma gain (multiplying encoded RGB ~scales encoded luma).
        raw = _SKIN_LIFT_TARGET_IRE / max(p50_1, 1e-3)
        gain = float(np.clip(1.0 + (raw - 1.0) * strength, *_SKIN_LIFT_GAIN_CLAMP))
        if abs(gain - 1.0) > 1e-4:
            params = {**params, "skin_lift": _round(gain)}
            ang1, p50_1, p90_1, _ = _skin_angle_ire(develop_fn(params)(src_skin))  # true post-lift read
            skin_lift = gain

    diag.update(applied=True, hue_after=round(ang1, 1), dev_after=round(ang1 - target_deg, 1),
                L_ire_p50_after=round(p50_1, 1), L_ire_p90_after=round(p90_1, 1),
                exp_trim=round(exp_trim, 4), skin_lift=round(skin_lift, 4),
                skin_hot=bool(p90_1 > _SKIN_IRE_HOT))
    return {**params, "skin": diag}


def compute_correction(bgr: "np.ndarray", *, learning_based: bool = False,
                       strength: float = 1.0, skin_solve: bool = True,
                       skin_offset: float = 0.0) -> Dict[str, object]:
    """Analyse one BGR frame and EMIT v2 develop :class:`Params`.

    Measures, in order, on the LINEARIZED frame: a darkness estimate -> Shades-of-Gray WB gains (faded
    toward neutral in low light) -> apply -> per-channel black point (low percentile) -> apply ->
    exposure gain (masked **median** mid-tone luma -> 0.18, soft-kneed so a dark scene isn't blown to
    the hard ceiling). Contrast / shoulder / vibrance use tasteful defaults. The returned params are
    what both the still applier and the per-shot baked cube re-apply, so the correction is a single
    constant transform.

    Low-light guards (task #8): a well-exposed scene demands only a small lift, so both guards are
    no-ops and the params are identical to the prior calibration -- they engage ONLY on genuinely dark
    / mixed-light footage, where gray-world WB over-warms and a full median->0.18 lift over-brightens
    and amplifies the cast (the observed night-scene failure).

    ``strength`` (0..1, default 1.0) scales ALL develop deviations from identity (WB, exposure,
    black point, contrast, vibrance). 1.0 = the calibrated auto develop (unchanged); lower = a gentler
    grade for footage where the auto-develop reads too strong. ``learning_based`` is accepted for v1
    signature compatibility but ignored.

    ``skin_solve`` (default True) runs the G1 skin-tone-line solver as a final, self-gating refinement:
    when skin is a real part of the frame (>= 8%) and clearly off the ~123 deg I-line, it folds a small
    capped luma-preserving WB tint into ``wb_gains`` (global, never a skin key) so skin lands nearer the
    line, plus a conservative two-band skin-exposure trim. When skin is still genuinely under-band after
    that GLOBAL trim, a final **G1b skin-LOCAL exposure lift** (a smooth colour-qualifier folded into
    ``develop_fn`` as a constant stage -> bakeable/flicker-free) raises only skin-chromaticity colours
    toward the band. Both are no-ops (params byte-identical) on footage without enough / without
    under-exposed skin, so non-portrait grades are unchanged. ``skin_offset`` shifts the target off
    123 deg (e.g. a slightly-green filmic resting point). The chosen correction is reported in a
    JSON-safe ``params["skin"]`` diagnostic (incl. ``skin_lift``); ``develop_fn`` reads only the top-level
    ``skin_lift`` gain and ignores the diagnostic.
    """
    if bgr is None:
        raise ValueError("compute_correction: bgr frame is None (failed decode?)")
    arr = np.asarray(bgr)
    if arr.ndim != 3 or arr.shape[2] < 3:
        raise ValueError(f"compute_correction: expected H x W x 3 BGR, got {arr.shape!r}")

    rgb = _to_rgb01(arr)                     # encoded RGB 0..1
    lin = tm.srgb_eotf(rgb)                  # -> linear

    # 0) Darkness estimate (pre-WB luma median) -> the lift the scene "demands". Drives the low-light
    #    WB fade; a well-exposed scene gives lift_demand ~1 (guards inert).
    med0 = float(np.median(tm.luminance(lin)))
    lift_demand = _MID / max(med0, 1e-4)
    wb_strength = _lowlight_wb_strength(lift_demand)

    # 1) White balance (Shades-of-Gray), FADED toward neutral in low light, applied in linear.
    gB, gG, gR = _shades_of_gray_gains(lin)
    if wb_strength < 1.0:
        gB = 1.0 + (gB - 1.0) * wb_strength   # gG stays 1.0 (green-anchored)
        gR = 1.0 + (gR - 1.0) * wb_strength
    lin_wb = lin * np.array([gR, gG, gB], dtype=np.float64)
    lin_wb = np.clip(lin_wb, 0.0, None)

    # 2) Per-channel black point: low percentile in linear (neutralizes cast, lifts off milky).
    black_rgb = np.percentile(lin_wb.reshape(-1, 3), _BLACK_PCT, axis=0)  # [R,G,B]
    black_rgb = np.clip(black_rgb, 0.0, _BLACK_MAX)
    denom = np.maximum(1.0 - black_rgb, 1e-6)
    lin_bp = np.clip((lin_wb - black_rgb) / denom, 0.0, None)

    # 3) Exposure: map the MEDIAN mid-tone luminance to 0.18 linear (robust to bright outliers), with
    #    a soft-knee on the LIFT so a genuinely dark scene rolls off toward _EXP_SOFT_CEIL instead of
    #    slamming the hard ceiling (the over-lift that amplified the night cast/noise).
    Llin = tm.luminance(lin_bp)
    lo, hi = np.percentile(Llin, [_EXP_LO_PCT, _EXP_HI_PCT])
    mid = Llin[(Llin >= lo) & (Llin <= hi)]
    med = float(np.median(mid)) if mid.size else float(np.median(Llin))
    exposure = _clamp(_soft_knee_gain(_MID / max(med, 1e-4), _EXP_KNEE, _EXP_SOFT_CEIL),
                      *_EXPOSURE_CLAMP)

    # Highlight protection (bright / high-dynamic-range scenes): the median->0.18 anchor over-lifts a
    # scene whose mid-tones read dark but whose BROAD highlights (sky, golden hour) are bright, blowing
    # them out (e.g. an outdoor clip clipping 30%+ of the sky). Cap the lift so the top ~2.5% of the
    # image lands under the soft-clip knee. This ONLY ever REDUCES exposure, so a controlled or
    # genuinely-dark scene with dim highlights is a no-op (a small specular won't trip the 97.5th
    # percentile) -- the same self-gating discipline as the low-light guards. Regression-safe on the
    # approved talking-head develop, whose highlights sit well under the target so the cap never binds.
    exp_hi_cap = float("inf")  # the max exposure the highlight protection allows (passed to the skin trim)
    hi_lin = float(np.percentile(Llin, _EXP_HI_PROTECT_PCT))
    if hi_lin > 1e-6:
        exp_hi_cap = _clamp(_EXP_HI_TARGET / hi_lin, *_EXPOSURE_CLAMP)
        exposure = _clamp(min(exposure, exp_hi_cap), *_EXPOSURE_CLAMP)

    contrast = _DEFAULT_CONTRAST
    vibrance = _DEFAULT_VIBRANCE

    # --strength: scale every deviation from identity (1.0 = calibrated auto develop, unchanged).
    s = _clamp(float(strength), 0.0, 1.0)
    if s != 1.0:
        gB = 1.0 + (gB - 1.0) * s
        gR = 1.0 + (gR - 1.0) * s
        exposure = 1.0 + (exposure - 1.0) * s
        black_rgb = black_rgb * s
        contrast = 1.0 + (contrast - 1.0) * s
        vibrance = vibrance * s
        if np.isfinite(exp_hi_cap):
            exp_hi_cap = 1.0 + (exp_hi_cap - 1.0) * s  # scale the ceiling with the develop

    params: Dict[str, object] = {
        "version": 2,
        "transfer": "srgb",
        "wb_gains": [_round(gB), _round(gG), _round(gR)],
        "black": [_round(float(black_rgb[2])), _round(float(black_rgb[1])), _round(float(black_rgb[0]))],  # BGR
        "exposure": _round(exposure),
        "contrast": _round(contrast),
        "shoulder": {"knee": _DEFAULT_KNEE, "ceiling": 1.0},
        "desat_hi": _DEFAULT_DESAT_HI,
        "vibrance": _round(vibrance),
        "strength": _round(s),
        "lowlight_wb": _round(wb_strength),
    }

    # G1 skin-tone-line solver (gated on skin presence -> non-portrait develops are byte-identical).
    # Runs LAST, on the assembled params, so it refines whatever the develop produced. Wrapped so a
    # solver fault can never sink a render (the codebase's defensive contract).
    if skin_solve:
        try:
            params = _apply_skin_solve(rgb, params, target_deg=_SKIN_ILINE_DEG + float(skin_offset),
                                       strength=s, exp_hi_cap=exp_hi_cap)
        except Exception as exc:  # pragma: no cover - defensive
            params = {**params, "skin": {"applied": False, "reason": f"error:{type(exc).__name__}"}}

    return params


# --------------------------------------------------------------------------- #
# The develop transform (single source of truth)                              #
# --------------------------------------------------------------------------- #
def _vibrance(enc_rgb: "np.ndarray", amount: float, protect: float = 2.0) -> "np.ndarray":
    """Vibrance in the encoded/perceptual domain: boost low-chroma pixels, protect saturated + skin.

    ``scale = 1 + amount*(1 - chroma)**protect`` where ``chroma = max-min`` per pixel (0..1). High-
    chroma pixels (already saturated, including skin) get scale~1; muted pixels get the boost. Chroma
    is scaled around the pixel's luma so hue is preserved.
    """
    if abs(amount) < 1e-6:
        return enc_rgb
    rgb = np.asarray(enc_rgb, dtype=np.float64)
    mx = rgb.max(axis=-1)
    mn = rgb.min(axis=-1)
    chroma = np.clip(mx - mn, 0.0, 1.0)
    luma = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    scale = 1.0 + float(amount) * np.power(1.0 - chroma, float(protect))
    out = luma[..., None] + (rgb - luma[..., None]) * scale[..., None]
    return np.clip(out, 0.0, 1.0)


def _skin_qualifier_weight(enc_rgb: "np.ndarray") -> "np.ndarray":
    """Smooth skin-CHROMATICITY membership ``w`` in [0,1], a pure function of encoded RGB (so it bakes).

    Reproduces :func:`_skin_mask`'s YCrCb box (Cr/Cb/luma) but with C1 smoothstep ramps of width
    ``_SKIN_QUAL_SOFT`` instead of hard edges -> no banding in the baked LUT and a soft falloff at the
    region border. Used by the G1b skin-LOCAL exposure lift to weight which colours get raised.
    """
    rgb = np.asarray(enc_rgb, dtype=np.float64)
    R, G, B = rgb[..., 0] * 255.0, rgb[..., 1] * 255.0, rgb[..., 2] * 255.0
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cr = (R - Y) * 0.713 + 128.0
    Cb = (B - Y) * 0.564 + 128.0

    def _band(x, lo: float, hi: float, soft: float):
        up = np.clip((x - (lo - soft)) / soft, 0.0, 1.0)
        dn = np.clip(((hi + soft) - x) / soft, 0.0, 1.0)
        up = up * up * (3.0 - 2.0 * up)   # smoothstep up at the low edge
        dn = dn * dn * (3.0 - 2.0 * dn)   # smoothstep down at the high edge
        return up * dn

    # Chroma gate: neutrals (Cr~Cb~128) sit at the box's lower-Cr edge and would leak a partial lift;
    # require a real distance from neutral so only chromatic skin colours qualify.
    chroma = np.sqrt((Cr - 128.0) ** 2 + (Cb - 128.0) ** 2)
    cu = np.clip((chroma - _SKIN_QUAL_CHROMA_MIN) / _SKIN_QUAL_CHROMA_SOFT, 0.0, 1.0)
    w_chroma = cu * cu * (3.0 - 2.0 * cu)

    return (_band(Cr, _SKIN_QUAL_CR[0], _SKIN_QUAL_CR[1], _SKIN_QUAL_SOFT)
            * _band(Cb, _SKIN_QUAL_CB[0], _SKIN_QUAL_CB[1], _SKIN_QUAL_SOFT)
            * _band(Y, _SKIN_QUAL_Y[0], _SKIN_QUAL_Y[1], _SKIN_QUAL_SOFT)
            * w_chroma)


def _apply_skin_lift(enc_rgb: "np.ndarray", gain: float) -> "np.ndarray":
    """G1b: raise the luma of skin-chromaticity pixels by ``gain`` (membership-weighted), hue-preserving.

    A per-pixel encoded multiplicative gain blended by the smooth skin qualifier: full ``gain`` where
    membership is 1, identity where 0. Multiplying encoded RGB by a scalar lifts brightness while
    preserving the channel ratio (hue). Pure function of colour -> bakes into the develop cube, so the
    still preview and the per-shot ``lut3d`` apply it identically (flicker-free).
    """
    g = float(gain)
    if abs(g - 1.0) < 1e-4:
        return enc_rgb
    w = _skin_qualifier_weight(enc_rgb)
    px_gain = 1.0 + (g - 1.0) * w
    return np.clip(np.asarray(enc_rgb, dtype=np.float64) * px_gain[..., None], 0.0, 1.0)


def develop_fn(params: Dict[str, object]):
    """Return a pure function ``f(enc_rgb)->enc_rgb`` implementing the v2 develop for ``params``.

    ``enc_rgb`` is float RGB in 0..1 of shape ``(...,3)``. The function linearizes, applies WB ->
    black point -> exposure -> pivoted contrast (on luma) -> highlight soft-clip (on luma) ->
    highlight desaturation, encodes, then applies vibrance. Deterministic and vectorized, so it is
    valid both for a full image and for a baked LUT grid.
    """
    p = {**default_params(), **(params or {})}
    gB, gG, gR = [float(x) for x in p["wb_gains"]]
    bB, bG, bR = [float(x) for x in p["black"]]
    exposure = float(p["exposure"])
    contrast = float(p["contrast"])
    sh = p.get("shoulder") or {}
    knee = float(sh.get("knee", _DEFAULT_KNEE))
    ceiling = float(sh.get("ceiling", 1.0))
    desat_hi = float(p.get("desat_hi", 0.0))
    vib = float(p.get("vibrance", 0.0))
    skin_lift = float(p.get("skin_lift", 1.0))  # G1b skin-LOCAL exposure gain (1.0 = no lift)
    wb = np.array([gR, gG, gB], dtype=np.float64)
    black = np.array([bR, bG, bB], dtype=np.float64)
    denom = np.maximum(1.0 - black, 1e-6)

    def f(enc_rgb: "np.ndarray") -> "np.ndarray":
        rgb = np.asarray(enc_rgb, dtype=np.float64)
        lin = tm.srgb_eotf(rgb)
        lin = np.clip(lin * wb, 0.0, None)                 # WB
        lin = np.clip((lin - black) / denom, 0.0, None)    # black point
        lin = lin * exposure                                # exposure: median -> 0.18
        if abs(contrast - 1.0) > 1e-4:                      # ONE gentle contrast, pivot 0.18, on luma
            lin = tm.apply_to_luminance(lin, lambda L: tm.pivoted_contrast(L, contrast, _MID))
            lin = np.clip(lin, 0.0, None)
        lin = tm.apply_to_luminance(lin, lambda L: tm.highlight_soft_clip(L, knee, ceiling))  # protect
        if desat_hi > 1e-6:
            lin = tm.desaturate_highlights(lin, start=0.7, amount=desat_hi)
        enc = tm.srgb_oetf(lin)                            # encode
        enc = _vibrance(enc, vib)                          # vibrance (perceptual)
        if abs(skin_lift - 1.0) > 1e-4:                    # G1b skin-LOCAL exposure (colour-qualifier)
            enc = _apply_skin_lift(enc, skin_lift)
        return np.clip(enc, 0.0, 1.0)

    return f


def apply_correction_image(bgr: "np.ndarray", params: Dict[str, object]) -> "np.ndarray":
    """Apply the v2 develop to a still BGR image, returning BGR uint8 (exact, not LUT-quantized)."""
    if bgr is None:
        raise ValueError("apply_correction_image: bgr image is None")
    src = np.asarray(bgr)
    was_u8 = src.dtype == np.uint8
    rgb = _to_rgb01(src)
    out_rgb = develop_fn(params)(rgb)
    out_bgr = out_rgb[..., ::-1]  # RGB->BGR
    if was_u8 or np.issubdtype(src.dtype, np.integer):
        return np.clip(np.rint(out_bgr * 255.0), 0, 255).astype(np.uint8)
    return out_bgr.astype(src.dtype, copy=False)


# --------------------------------------------------------------------------- #
# Bake the develop into a constant per-shot .cube (the VIDEO apply)           #
# --------------------------------------------------------------------------- #
def bake_develop_cube(params: Dict[str, object], dst_cube: str, size: int = 33) -> str:
    """Bake :func:`develop_fn` into an Iridas ``.cube`` 3D LUT (R fastest), for ffmpeg ``lut3d``.

    Samples the encoded RGB unit cube at ``size**3`` grid points, runs the SAME develop function the
    still path uses, and writes the result with the red channel varying fastest (the convention
    ``colorkit.luts.write_cube`` uses and ffmpeg ``lut3d`` expects). Because the develop is one fixed
    set of numbers, the baked LUT applied via ``lut3d`` is constant for every frame of the shot ->
    structurally flicker-free, and identical to the still preview.
    """
    from pathlib import Path

    n = int(size)
    if n < 2:
        raise ValueError(f"size must be >= 2, got {size!r}")
    axis = np.linspace(0.0, 1.0, n, dtype=np.float64)
    bb, gg, rr = np.meshgrid(axis, axis, axis, indexing="ij")  # rr fastest in ravel
    grid = np.stack([rr.ravel(), gg.ravel(), bb.ravel()], axis=1)  # (N,3) R,G,B
    out = develop_fn(params)(grid)  # (N,3) encoded RGB
    out = np.clip(out, 0.0, 1.0)

    dst = Path(dst_cube)
    dst.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Generated by colorkit.correct.bake_develop_cube -- constant per-shot v2 develop.",
        f"LUT_3D_SIZE {n}",
    ]
    lines.extend(f"{r:.6f} {g:.6f} {b:.6f}" for r, g, b in out)
    dst.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
    return str(dst)
