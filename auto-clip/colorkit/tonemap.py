"""colorkit.tonemap -- linear-light tone-mapping & transfer-function math for the v2 develop.

This is the numeric heart of the v2 "develop" (the grey-anchored, highlight-protected correction
that replaced v1's naive *push-mean-to-0.46 + linear-contrast-stretch* — the cause of the washed,
one-tap-filter look). See ``docs/plans/2026-06-24-color-v2-grading-spec.md``.

The whole point: **do tonal work in LINEAR light, not on gamma-encoded values.** Failing to
linearize is exactly what desaturates and washes an image (research lane `sota-autograde`). So the
develop chain is::

    encoded(0..1) --EOTF--> linear --[WB, black point, exposure, shoulder, contrast]--> linear --OETF--> encoded

Everything here is pure NumPy/scalar math (no cv2, no I/O, no network), deterministic, CPU-only.
Functions accept either a Python float or a NumPy array (any shape) and return the same kind.

What it provides
----------------
- Transfer functions: :func:`srgb_eotf` / :func:`srgb_oetf` (sRGB), and :func:`gamma_eotf` /
  :func:`gamma_oetf` (pure-power, e.g. BT.1886 2.4 for de-log'd Rec.709).
- Highlight protection / tone curves (all operate in linear):
    * :func:`highlight_soft_clip` -- the DEFAULT shoulder. C1-continuous soft knee: identity below
      ``knee`` (so middle-grey and contrast are untouched -> exposure is preserved), smooth rolloff
      of everything above it toward ``ceiling`` with no hard clip. Apply to LUMINANCE and scale RGB
      by ``L'/L`` to preserve hue (avoids the per-channel "Notorious 6" hue skew).
    * :func:`reinhard_extended` -- featherweight rolloff with an explicit white point.
    * :func:`aces_narkowicz` -- the public-domain ACES RRT+ODT fit (a=2.51,b=0.03,...). Note it
      slightly over-saturates bright colors and bakes in display response, so we expose it but it is
      NOT the default; use as a per-channel filmic look operator when wanted.
    * :func:`hable` -- Uncharted-2 / Hable piecewise filmic.
- :func:`pivoted_contrast` -- contrast that pivots on middle-grey (0.18 linear), never on 0 (the
  v1 bug). c in ~1.05..1.25 is a tasteful amount.
- Helpers: :func:`luminance`, :func:`apply_to_luminance` (run a 1-D tone fn on luma, preserve chroma),
  :func:`desaturate_highlights`.

Scope-target anchors this math is tuned to hit (after OETF, on the 0..1 display scale):
    black ~0.04 (≈4 IRE) · middle-grey 0.18 linear -> ~0.46 display (≈41-46 IRE) ·
    diffuse white ~0.75-0.9 linear -> ~88-95 display · speculars roll off, <0.5% pixels at 1.0.
"""
from __future__ import annotations

from typing import Callable, Union

import numpy as np

Number = Union[float, "np.ndarray"]

__all__ = [
    "srgb_eotf", "srgb_oetf", "gamma_eotf", "gamma_oetf",
    "luminance", "apply_to_luminance", "desaturate_highlights",
    "highlight_soft_clip", "reinhard_extended", "aces_narkowicz", "hable",
    "pivoted_contrast",
    "MIDDLE_GREY",
]

#: Scene-linear middle grey (18% grey). The contrast pivot and the exposure target.
MIDDLE_GREY = 0.18


# --------------------------------------------------------------------------- #
# Transfer functions (encoded <-> linear)                                     #
# --------------------------------------------------------------------------- #
def srgb_eotf(v: Number) -> Number:
    """sRGB EOTF: encoded display value in [0,1] -> scene/display linear.

    Piecewise: linear segment below 0.04045, power 2.4 above. Vectorized; negatives are clamped to 0
    so a stray sub-black value can't produce NaNs downstream.
    """
    x = np.asarray(v, dtype=np.float64)
    x = np.clip(x, 0.0, None)
    lin = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    return float(lin) if np.isscalar(v) or np.ndim(v) == 0 else lin


def srgb_oetf(lin: Number) -> Number:
    """Inverse sRGB (OETF): linear -> encoded display value in [0,1]. Clamps to [0,1]."""
    x = np.asarray(lin, dtype=np.float64)
    x = np.clip(x, 0.0, 1.0)
    enc = np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1.0 / 2.4) - 0.055)
    enc = np.clip(enc, 0.0, 1.0)
    return float(enc) if np.isscalar(lin) or np.ndim(lin) == 0 else enc


def gamma_eotf(v: Number, gamma: float = 2.4) -> Number:
    """Pure-power EOTF (encoded -> linear): ``lin = v ** gamma``. BT.1886 uses gamma=2.4.

    Use for footage already developed to a pure-gamma Rec.709 (e.g. after an I-Log->Rec709 BT1886
    input LUT). Negatives clamped to 0.
    """
    x = np.clip(np.asarray(v, dtype=np.float64), 0.0, None)
    lin = np.power(x, float(gamma))
    return float(lin) if np.isscalar(v) or np.ndim(v) == 0 else lin


def gamma_oetf(lin: Number, gamma: float = 2.4) -> Number:
    """Pure-power OETF (linear -> encoded): ``v = lin ** (1/gamma)``. Clamps to [0,1]."""
    x = np.clip(np.asarray(lin, dtype=np.float64), 0.0, 1.0)
    enc = np.power(x, 1.0 / float(gamma))
    enc = np.clip(enc, 0.0, 1.0)
    return float(enc) if np.isscalar(lin) or np.ndim(lin) == 0 else enc


# --------------------------------------------------------------------------- #
# Luminance helpers                                                           #
# --------------------------------------------------------------------------- #
def luminance(rgb: "np.ndarray") -> "np.ndarray":
    """Rec.709 luminance of a linear RGB array. ``rgb`` is ``(..., 3)`` in R,G,B order."""
    arr = np.asarray(rgb, dtype=np.float64)
    return 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]


def apply_to_luminance(rgb: "np.ndarray", fn: Callable[["np.ndarray"], "np.ndarray"]) -> "np.ndarray":
    """Apply a 1-D tone function to the LUMINANCE of a linear RGB array and rescale chroma.

    This is the hue-preserving way to tone-map: compute ``L``, map it to ``L' = fn(L)``, then scale
    every channel by ``L'/L``. Because all channels scale by the same factor, hue and saturation are
    preserved (no per-channel "Notorious 6" skew). Pixels with ``L<=0`` are left untouched.
    """
    arr = np.asarray(rgb, dtype=np.float64)
    L = luminance(arr)
    Lp = np.asarray(fn(L), dtype=np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        scale = np.where(L > 1e-8, Lp / np.maximum(L, 1e-8), 1.0)
    return arr * scale[..., None]


def desaturate_highlights(rgb: "np.ndarray", start: float = 0.7, amount: float = 0.6) -> "np.ndarray":
    """Lerp bright pixels toward their luminance to tame over-saturated highlights.

    For each pixel, a weight ramps 0->``amount`` as luminance goes ``start``->1.0; the pixel is
    blended toward grey (its luma) by that weight. Mimics how AgX/film desaturate as light increases,
    preventing the neon-highlight look. Operates in linear RGB.
    """
    arr = np.asarray(rgb, dtype=np.float64)
    L = luminance(arr)[..., None]
    w = np.clip((L - start) / max(1e-6, (1.0 - start)), 0.0, 1.0) * float(amount)
    return arr * (1.0 - w) + L * w


# --------------------------------------------------------------------------- #
# Tone curves / highlight protection (linear domain)                          #
# --------------------------------------------------------------------------- #
def highlight_soft_clip(x: Number, knee: float = 0.8, ceiling: float = 1.0) -> Number:
    """C1-continuous soft-knee highlight rolloff (the DEFAULT shoulder).

    Identity for ``x <= knee`` (so middle-grey, shadows and mid contrast are untouched -> exposure is
    preserved exactly), then smoothly compresses ``(knee, +inf)`` into ``(knee, ceiling)`` with the
    rational map ``compressed = range * over / (over + range)`` where ``over = x-knee`` and
    ``range = ceiling-knee``. The map asymptotes to ``ceiling`` (never crosses it -> no hard clip)
    and is C1 at the knee (derivative 1 on both sides), so there's no visible kink. This is the
    feather-light, hue-safe protection used on luminance via :func:`apply_to_luminance`.
    """
    x = np.asarray(x, dtype=np.float64)
    rng = max(1e-6, float(ceiling) - float(knee))
    over = np.clip(x - float(knee), 0.0, None)
    compressed = rng * over / (over + rng)
    out = np.where(x > float(knee), float(knee) + compressed, x)
    return float(out) if np.isscalar(x) or np.ndim(x) == 0 else out


def reinhard_extended(x: Number, c_white: float = 4.0) -> Number:
    """Extended Reinhard tone-map with an explicit white point.

    ``out = x * (1 + x / c_white**2) / (1 + x)``. Values at/above ``c_white`` map to ~1.0 with a
    knee (plain Reinhard's flat desaturated rolloff, fixed). Best applied to luminance. Note it
    darkens mid-grey slightly (0.18 -> ~0.16 at c_white=4), so prefer :func:`highlight_soft_clip`
    when you need exposure preserved; use this when you want a softer global compression.
    """
    x = np.asarray(x, dtype=np.float64)
    cw2 = max(1e-6, float(c_white) ** 2)
    out = x * (1.0 + x / cw2) / (1.0 + x)
    return float(out) if np.isscalar(x) or np.ndim(x) == 0 else out


def aces_narkowicz(x: Number, pre_scale: float = 1.0) -> Number:
    """ACES RRT+ODT filmic approximation (Krzysztof Narkowicz fit; public domain).

    ``out = clamp((x*(a*x+b))/(x*(c*x+d)+e), 0, 1)`` with a=2.51,b=0.03,c=2.43,d=0.59,e=0.14.
    ``pre_scale=0.6`` gives the true-ACES match (input 1.0 -> ~0.8). This fit bakes in display
    response and slightly over-saturates bright colors, so it is offered as a per-channel filmic
    operator, not the default develop shoulder. Apply in linear; do NOT also OETF-encode its output
    if you treat it as display-referred.
    """
    x = np.asarray(x, dtype=np.float64) * float(pre_scale)
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    out = np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0)
    return float(out) if np.isscalar(x) or np.ndim(x) == 0 else out


def hable(x: Number, exposure_bias: float = 2.0, w: float = 11.2) -> Number:
    """Hable / Uncharted-2 piecewise filmic tone curve, normalized by white point ``w``.

    A=0.15,B=0.50,C=0.10,D=0.20,E=0.02,F=0.30. ``out = f(x*exposure_bias) / f(w)``. Raise ``w`` to
    protect more highlights. Operates in linear; treat output as display-referred.
    """
    A, B, C, D, E, F = 0.15, 0.50, 0.10, 0.20, 0.02, 0.30

    def _f(v):
        v = np.asarray(v, dtype=np.float64)
        return ((v * (A * v + C * B) + D * E) / (v * (A * v + B) + D * F)) - E / F

    x = np.asarray(x, dtype=np.float64)
    out = _f(x * float(exposure_bias)) / _f(np.asarray(float(w)))
    out = np.clip(out, 0.0, 1.0)
    return float(out) if np.isscalar(x) or np.ndim(x) == 0 else out


def pivoted_contrast(x: Number, c: float = 1.1, pivot: float = MIDDLE_GREY) -> Number:
    """Contrast that pivots on middle-grey: ``out = pivot * (x/pivot) ** c``.

    Unlike a linear stretch (which pivots on 0 and pushes values past 1.0 -> hard clip = the v1
    washed look), this scales contrast around 0.18 so the image doesn't drift brighter/darker.
    ``c=1.0`` is identity; 1.05-1.25 is tasteful; >1.4 starts to look filtered. Input clamped >=0
    before the power (pow of a negative is NaN).
    """
    x = np.clip(np.asarray(x, dtype=np.float64), 0.0, None)
    p = float(pivot)
    out = p * np.power(x / p, float(c))
    return float(out) if np.isscalar(x) or np.ndim(x) == 0 else out
