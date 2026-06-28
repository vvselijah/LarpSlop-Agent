"""
auto-clip/colorkit/luts.py -- pure-stdlib 3D .cube LUT writer + five film-look generators.

This module is deliberately DEPENDENCY-FREE: STDLIB ONLY -- no numpy, no cv2, no
colour-science. It must run on a bare Python 3.12 interpreter so the look library can be
(re)generated anywhere, including environments where the heavy imaging stack is unavailable
or slow to import (e.g. cv2/torch on the OneDrive disk). Everything here is plain Python math.

What it provides
----------------
- ``write_cube(path, size, fn)`` -- writes a valid Iridas ``.cube`` 3D LUT. ``fn`` is a pure
  callback ``fn(r, g, b) -> (r, g, b)`` operating in normalized 0..1 space (input grid sample ->
  output color). The file follows the Iridas spec: a ``LUT_3D_SIZE`` header followed by
  ``size**3`` RGB triplets, with the **red channel varying fastest** (then green, then blue).
- Five pure-math look generators, each an ``fn(r, g, b) -> (r, g, b)`` suitable for ``write_cube``:
  ``neutral_correct``, ``warm_interview``, ``teal_orange``, ``kodak_2383_style``, ``fuji_style``.
- A ``__main__`` (``python -m colorkit.luts --all [--out DIR] [--size N]``) that writes all five
  ``<name>.cube`` files (default dir: ``colorkit/luts/``, default ``LUT_3D_SIZE=33``).

These ``.cube`` files are consumed downstream by ``colorkit.stylize`` (the ``LOOKS`` registry +
``ffmpeg_lut_filter`` / ``apply_look_image``) and applied uniformly across all shots in the
STYLIZE stage of the pipeline -- they encode the creative "look", never the per-shot correction.

The math here is approximate film-emulation by design (channel curves + split-toning + a gentle
S-curve), not a colorimetric profile of any real stock. Names ending in ``_style`` signal that.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Callable, Tuple

__all__ = [
    "write_cube",
    "neutral_correct",
    "warm_interview",
    "teal_orange",
    "kodak_2383_style",
    "fuji_style",
    "golden_hour",
    "moody_blue",
    "bleach_bypass",
    "clean_pop",
    "portra_style",
    "GENERATORS",
    "DEFAULT_SIZE",
    "DEFAULT_OUT_DIR",
]

# A LUT function maps an input color (0..1 each) to an output color (0..1 each).
LUTFn = Callable[[float, float, float], Tuple[float, float, float]]

# Default 3D LUT cube resolution (33 is the de-facto interchange standard).
DEFAULT_SIZE = 33

# Default output directory: the package's own ``luts/`` folder (absolute via __file__),
# which is exactly where ``colorkit.stylize.LOOKS`` expects to find the .cube files.
DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "luts"


# --------------------------------------------------------------------------------------------
# Small pure-math helpers (no numpy)
# --------------------------------------------------------------------------------------------
def _clamp01(x: float) -> float:
    """Clamp a scalar into the closed [0, 1] range."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate from ``a`` to ``b`` by ``t`` (t in 0..1)."""
    return a + (b - a) * t


def _smoothstep(x: float) -> float:
    """Hermite smoothstep on [0, 1]; an S-shaped easing used for gentle contrast."""
    x = _clamp01(x)
    return x * x * (3.0 - 2.0 * x)


def _s_curve(x: float, strength: float = 0.0) -> float:
    """
    Apply a contrast S-curve around mid-grey (0.5).

    ``strength`` 0 is identity; positive adds contrast (lift highlights, crush shadows) by
    blending toward a smoothstep response. ``strength`` is clamped to a sane 0..1 range.
    """
    x = _clamp01(x)
    s = _clamp01(strength)
    return _clamp01(_lerp(x, _smoothstep(x), s))


def _gamma(x: float, g: float) -> float:
    """Apply a power-law gamma (output = input ** g) with safe clamping. g>1 darkens mids."""
    x = _clamp01(x)
    if g <= 0.0:
        return x
    return _clamp01(x ** g)


def _lift_gamma_gain(x: float, lift: float, gamma_g: float, gain: float) -> float:
    """
    Classic ASC-style lift/gamma/gain on a single channel (all in 0..1-ish ranges).

    lift shifts shadows, gain scales highlights, gamma_g reshapes midtones. Clamped to [0,1].
    """
    x = _clamp01(x)
    # gain then lift (affine), then gamma on the result.
    y = x * gain + lift * (1.0 - x)
    y = _clamp01(y)
    return _gamma(y, gamma_g)


def _split_tone(
    r: float,
    g: float,
    b: float,
    shadow_rgb: Tuple[float, float, float],
    highlight_rgb: Tuple[float, float, float],
    amount: float = 0.15,
) -> Tuple[float, float, float]:
    """
    Tint shadows toward ``shadow_rgb`` and highlights toward ``highlight_rgb``.

    Luminance (Rec.709-ish) selects how shadow-like vs highlight-like a pixel is; the tint is
    added proportionally and scaled by ``amount``. Tints are expressed as signed offsets around
    neutral grey (0.5), so e.g. a cool shadow uses a low-R / high-B triplet.
    """
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # Weight: 1.0 in deep shadows -> 0.0 in highlights (and vice-versa).
    hi_w = _smoothstep(luma)
    lo_w = 1.0 - hi_w
    sr, sg, sb = shadow_rgb
    hr, hg, hb = highlight_rgb
    r = r + amount * (lo_w * (sr - 0.5) + hi_w * (hr - 0.5))
    g = g + amount * (lo_w * (sg - 0.5) + hi_w * (hg - 0.5))
    b = b + amount * (lo_w * (sb - 0.5) + hi_w * (hb - 0.5))
    return _clamp01(r), _clamp01(g), _clamp01(b)


def _srgb_eotf_s(c: float) -> float:
    """Scalar sRGB encoded->linear (pure math, stdlib-only)."""
    c = _clamp01(c)
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _srgb_oetf_s(c: float) -> float:
    """Scalar sRGB linear->encoded (pure math, stdlib-only). Clamps to [0,1]."""
    c = _clamp01(c)
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055


def _skin_protect_weight(r: float, g: float, b: float) -> float:
    """Density-protection weight (0..~0.7) for skin-hued grid colors.

    Density baked into the look cube must NOT over-saturate skin (and must not fight the G1 skin
    solver, which steers skin to the ~123 deg I-line). We compute the grid color's vectorscope hue
    angle (atan2(R-Y, B-Y), the SAME convention as measure.skin_signature / correct._skin_angle_ire)
    and, within +/-30 deg of 123 deg, return a weight that lerps the density effect back toward the
    input -- strongest (0.7) on the line, fading to 0 by 30 deg off. Per-COLOR (not a pixel mask), so
    it works in the stdlib cube generator and protects every skin pixel that maps through these grid
    points. ev: synthesis_v2 (deepen-not-electrify, protect skin); engine_gap_map P2 density row.
    """
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    ang = math.degrees(math.atan2(r - Y, b - Y)) % 360.0
    d = abs((ang - 123.0 + 180.0) % 360.0 - 180.0)
    if d >= 30.0:
        return 0.0
    return 0.7 * (1.0 - d / 30.0)


def _saturate(r: float, g: float, b: float, sat: float, k: float = 0.12) -> Tuple[float, float, float]:
    """Saturation, the colorist way: DESATURATE luma-safely for ``sat<=1``; DENSITY-deepen for ``sat>1``.

    ``sat == 1.0`` is identity. For ``sat < 1`` this is the classic luma-preserving chroma scale
    (deepens nothing, just pulls toward grey -- correct for the muted/bleach looks). For ``sat > 1`` it
    uses the demonstrated **subtractive density** model instead of a naive chroma multiply: it works in
    LINEAR light, deepens chroma sublinearly AND darkens proportional to chroma magnitude (``k``) so
    colors gain DENSITY ("deepen") rather than brightening into neon ("electrify"), and it PROTECTS the
    skin hue band (:func:`_skin_protect_weight`). This fixes the encoded-domain "electrify" failure the
    research flagged, and bakes into the look ``.cube`` as one constant transform (flicker-safe, and the
    still and video paths match automatically). ev: frenchie 22:28 (+14% subtractive deepens not
    electrifies); grading-too-complicated 09:38-11:51 (never RGB gain); mullins 32:12 (luma-preserving).
    """
    if sat <= 1.0:
        luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return (_clamp01(luma + (r - luma) * sat),
                _clamp01(luma + (g - luma) * sat),
                _clamp01(luma + (b - luma) * sat))
    # sat > 1: subtractive density in linear light, skin-protected.
    lr, lg, lb = _srgb_eotf_s(r), _srgb_eotf_s(g), _srgb_eotf_s(b)
    L = 0.2126 * lr + 0.7152 * lg + 0.0722 * lb
    dr, dg, db = L + (lr - L) * sat, L + (lg - L) * sat, L + (lb - L) * sat
    cmag = min(1.0, math.sqrt((lr - L) ** 2 + (lg - L) ** 2 + (lb - L) ** 2) / (L + 1e-3))
    dark = 1.0 - k * cmag
    dr, dg, db = dr * dark, dg * dark, db * dark
    w = _skin_protect_weight(r, g, b)  # measure hue on the encoded grid color
    if w > 0.0:
        dr, dg, db = dr * (1.0 - w) + lr * w, dg * (1.0 - w) + lg * w, db * (1.0 - w) + lb * w
    return _clamp01(_srgb_oetf_s(dr)), _clamp01(_srgb_oetf_s(dg)), _clamp01(_srgb_oetf_s(db))


# --------------------------------------------------------------------------------------------
# Look generators -- pure fn(r, g, b) -> (r, g, b), all in 0..1
# --------------------------------------------------------------------------------------------
def neutral_correct(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    A near-identity "technical" LUT: a whisper of contrast and chroma, no color shift.

    Use as the default stylize when you want correction-only output to still pass through the
    LUT stage cleanly (it is intentionally close to a pass-through so it never fights the
    upstream neutral correction).
    """
    r = _s_curve(r, 0.06)
    g = _s_curve(g, 0.06)
    b = _s_curve(b, 0.06)
    return _saturate(r, g, b, 1.02)


def warm_interview(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    Clean, flattering warm look for talking-head / interview footage.

    Gentle warm white balance (lift red, ease blue), soft contrast, slightly lifted shadows for
    a friendly feel, modest saturation. Designed to keep skin tones healthy, not stylized.
    """
    # Warm WB: nudge red up, blue down, leave green as the anchor.
    r = _clamp01(r * 1.05)
    b = _clamp01(b * 0.95)
    # Whisper of body only -- the develop already set contrast; looks must not re-stack it
    # (masterclass consensus: ONE source of contrast). Character lives in the hue split below.
    r = _s_curve(r, 0.04)
    g = _s_curve(g, 0.04)
    b = _s_curve(b, 0.04)
    # Warm highlight / neutral-warm shadow split.
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.49, 0.50, 0.55),    # barely-cool shadow keeps it from going muddy
        highlight_rgb=(0.56, 0.51, 0.45),  # warm highlights
        amount=0.13,
    )
    return _saturate(r, g, b, 1.05)


def teal_orange(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    The cinematic teal-shadows / orange-highlights complementary look.

    Push shadows toward teal and highlights toward orange via split-toning over a contrast
    S-curve, with a saturation lift. The hero "blockbuster" grade; stronger than warm_interview.
    """
    # Light body only (develop owns contrast); the LOOK is the complementary hue split.
    r = _s_curve(r, 0.07)
    g = _s_curve(g, 0.07)
    b = _s_curve(b, 0.07)
    # Teal shadows, orange highlights -- ASYMMETRIC (env carries teal, subject keeps orange);
    # stronger hue so the look still reads when run UNDER the grade at ~0.7 opacity.
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.41, 0.52, 0.57),    # teal/cyan
        highlight_rgb=(0.59, 0.52, 0.41),  # orange
        amount=0.27,
    )
    return _saturate(r, g, b, 1.10)


def kodak_2383_style(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    Approximate the look of a Kodak 2383 print-film emulation: warm, rich, with crushed,
    slightly cool blacks and creamy, warm highlights (NOT a colorimetric 2383 profile -- a
    pleasing print-film *style*).

    Per-channel lift/gamma/gain shapes the classic print toe and shoulder; a warm highlight /
    cool-toe split-tone and a healthy saturation finish it.
    """
    # Print-film tonality: lifted-then-rolled shadows, gentle highlight shoulder.
    r = _lift_gamma_gain(r, lift=0.015, gamma_g=0.95, gain=1.02)
    g = _lift_gamma_gain(g, lift=0.010, gamma_g=0.97, gain=1.00)
    b = _lift_gamma_gain(b, lift=0.020, gamma_g=1.02, gain=0.97)
    # The lift/gamma/gain above IS the print-film toe/shoulder (the real density character);
    # keep only a whisper of extra S so we don't re-stack the develop's contrast.
    r = _s_curve(r, 0.06)
    g = _s_curve(g, 0.06)
    b = _s_curve(b, 0.06)
    # Warm highlights, slightly cool/teal blacks (the 2383 signature).
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.47, 0.50, 0.54),    # cool-ish blacks
        highlight_rgb=(0.56, 0.52, 0.45),  # warm highlights
        amount=0.16,
    )
    return _saturate(r, g, b, 1.12)


def fuji_style(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """
    Approximate a Fujifilm-stock look: green-leaning midtones, gentle contrast, restrained
    highlights, and slightly muted-but-vibrant color (the "Fuji greens" feel). Cooler and softer
    than the Kodak look. Again a *style*, not a measured emulation.
    """
    # Slight green bias in mids; ease red a touch, keep blue honest.
    g = _clamp01(g * 1.03)
    r = _clamp01(r * 0.99)
    # Very soft body only (develop owns contrast); the Fuji character is the green-cyan split.
    r = _s_curve(r, 0.04)
    g = _s_curve(g, 0.04)
    b = _s_curve(b, 0.04)
    # Cool-green shadows, soft neutral-warm highlights.
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.48, 0.53, 0.51),    # green-cyan shadows
        highlight_rgb=(0.52, 0.51, 0.49),  # near-neutral, faintly warm highlights
        amount=0.12,
    )
    # Fuji reads vibrant but not loud -> modest saturation.
    return _saturate(r, g, b, 1.06)


# --------------------------------------------------------------------------------------------
# Fresh film looks (2026-06-24) -- distinct moods for Elijah's content. Same v2 design discipline:
# the develop already owns exposure + contrast, so each look carries HUE + DENSITY character (a tiny
# s-curve/density at most, never a re-stacked contrast), tuned to read well UNDER the grade at ~0.7.
# --------------------------------------------------------------------------------------------
def golden_hour(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """Warm, aspirational golden-hour glow: amber highlights, soft warm shadow lift, inviting.

    For lifestyle / faith / motivational content -- flattering and warm without becoming an
    orange one-tap filter. Warmer and softer than warm_interview, with a gentle shadow lift.
    """
    # warm WB nudge (red up, blue down; green anchored)
    r = _clamp01(r * 1.05)
    b = _clamp01(b * 0.94)
    # soft, lifted shadows for the golden glow (small lift, gentle gamma -- the density, not contrast)
    r = _lift_gamma_gain(r, lift=0.022, gamma_g=0.97, gain=1.02)
    g = _lift_gamma_gain(g, lift=0.016, gamma_g=0.98, gain=1.00)
    b = _lift_gamma_gain(b, lift=0.010, gamma_g=1.00, gain=0.98)
    # amber/golden highlights, faintly warm shadows
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.52, 0.50, 0.47),     # barely-warm shadow
        highlight_rgb=(0.60, 0.53, 0.40),  # amber highlight
        amount=0.18,
    )
    return _saturate(r, g, b, 1.07)


def moody_blue(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """Cool cinematic night/urban look: teal-blue shadows, cool highlights, slightly desaturated.

    The complement to the warm looks -- suits night b-roll, driving footage, or a moody talking-head.
    Deliberately a touch muted so it reads as atmosphere, not a blue cast.
    """
    b = _clamp01(b * 1.05)
    r = _clamp01(r * 0.98)
    r = _s_curve(r, 0.05)
    g = _s_curve(g, 0.05)
    b = _s_curve(b, 0.05)
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.43, 0.49, 0.58),     # blue-teal shadow
        highlight_rgb=(0.49, 0.51, 0.55),  # cool highlight
        amount=0.20,
    )
    return _saturate(r, g, b, 0.96)        # slightly muted = moody


def bleach_bypass(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """Silver-retention 'bleach bypass': heavily desaturated, crisp, neutral-cool -- gritty/dramatic.

    The look's identity is desaturation (the develop supplies the base contrast), so it carries almost
    no hue -- a whisper of body + a faint cool tint over a strong desaturation.
    """
    # contrast IS this look's character, but the develop already set the base -> keep this a whisper.
    r = _s_curve(r, 0.10)
    g = _s_curve(g, 0.10)
    b = _s_curve(b, 0.10)
    r, g, b = _saturate(r, g, b, 0.45)     # strong silver desaturation
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.49, 0.50, 0.52),     # faint cool blacks
        highlight_rgb=(0.51, 0.51, 0.50),  # near-neutral highlights
        amount=0.08,
    )
    return r, g, b


def clean_pop(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """Bright, punchy, clean commercial look: neutral whites, lively colour -- product / ad / IG.

    Modern and crisp; lets colour sing without a tint cast. The bright, saturated, neutral-white feel
    that reads well for product shots, ad creative and high-energy talking-head.
    """
    r = _s_curve(r, 0.05)
    g = _s_curve(g, 0.05)
    b = _s_curve(b, 0.05)
    r, g, b = _saturate(r, g, b, 1.16)     # vibrant, not garish
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.50, 0.50, 0.50),     # neutral blacks
        highlight_rgb=(0.53, 0.51, 0.48),  # faintly warm, clean highlight (healthy skin/product)
        amount=0.08,
    )
    return r, g, b


def portra_style(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """Soft Kodak Portra-style film: lifted toe, warm-pink skin highlights, low contrast, muted-pretty.

    A gentler, more pastel alternative to warm_interview for portraits / lifestyle -- creamy shadows
    and flattering, slightly pink skin, with restrained saturation.
    """
    # lifted, soft shadows (the Portra toe) -- density, not contrast
    r = _lift_gamma_gain(r, lift=0.022, gamma_g=0.96, gain=1.00)
    g = _lift_gamma_gain(g, lift=0.018, gamma_g=0.98, gain=1.00)
    b = _lift_gamma_gain(b, lift=0.020, gamma_g=1.00, gain=0.99)
    r, g, b = _split_tone(
        r, g, b,
        shadow_rgb=(0.49, 0.51, 0.50),     # faintly cool-green shadow (Portra balance)
        highlight_rgb=(0.55, 0.50, 0.49),  # warm-pink highlight (skin)
        amount=0.12,
    )
    return _saturate(r, g, b, 0.98)        # muted-pretty, not punchy


# Registry of named generators (name -> fn). The original five + the 2026-06-24 fresh looks;
# this is what ``--all`` iterates over.
GENERATORS: dict[str, LUTFn] = {
    "neutral_correct": neutral_correct,
    "warm_interview": warm_interview,
    "teal_orange": teal_orange,
    "kodak_2383_style": kodak_2383_style,
    "fuji_style": fuji_style,
    "golden_hour": golden_hour,
    "moody_blue": moody_blue,
    "bleach_bypass": bleach_bypass,
    "clean_pop": clean_pop,
    "portra_style": portra_style,
}


# --------------------------------------------------------------------------------------------
# The .cube writer (Iridas spec, stdlib-only)
# --------------------------------------------------------------------------------------------
def write_cube(path, size: int, fn: LUTFn) -> str:
    """
    Write a valid Iridas ``.cube`` 3D LUT to ``path``.

    Parameters
    ----------
    path : str | os.PathLike
        Destination file. Parent directories are created if missing.
    size : int
        3D LUT edge length (``LUT_3D_SIZE``). Must be >= 2; 33 is the interchange standard.
    fn : Callable[[float, float, float], tuple[float, float, float]]
        Pure mapping from an input grid sample ``(r, g, b)`` in 0..1 to an output color
        ``(r, g, b)`` in 0..1. Called ``size**3`` times.

    Returns
    -------
    str
        The absolute path written, as a string.

    Notes
    -----
    Data ordering follows the Iridas convention used by FFmpeg's ``lut3d`` and by
    ``colour-science``: the **red index varies fastest**, then green, then blue. Concretely the
    loop nesting is ``for b: for g: for r:`` (red innermost) and the input sampled for a given
    ``(ri, gi, bi)`` is ``(ri/(size-1), gi/(size-1), bi/(size-1))``. Output triplets are clamped to
    [0, 1] and written with fixed 6-decimal precision, one ``R G B`` line per entry.
    """
    if int(size) < 2:
        raise ValueError(f"LUT_3D_SIZE must be >= 2, got {size!r}")
    size = int(size)
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    denom = float(size - 1)
    lines: list[str] = []
    title = out_path.stem
    lines.append(f'TITLE "{title}"')
    lines.append(f"LUT_3D_SIZE {size}")
    lines.append("DOMAIN_MIN 0.0 0.0 0.0")
    lines.append("DOMAIN_MAX 1.0 1.0 1.0")
    lines.append("")

    # R fastest-varying: outer loop blue, then green, then red (innermost).
    for bi in range(size):
        ib = bi / denom
        for gi in range(size):
            ig = gi / denom
            for ri in range(size):
                ir = ri / denom
                orr, ogg, obb = fn(ir, ig, ib)
                lines.append(
                    f"{_clamp01(orr):.6f} {_clamp01(ogg):.6f} {_clamp01(obb):.6f}"
                )

    # Trailing newline; LF endings so FFmpeg/colour-science parse cleanly on any OS.
    out_path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
    return str(out_path.resolve())


# --------------------------------------------------------------------------------------------
# CLI: write all five looks
# --------------------------------------------------------------------------------------------
def _write_all(out_dir, size: int) -> list[str]:
    """Generate every look in ``GENERATORS`` into ``out_dir`` as ``<name>.cube``."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for name, fn in GENERATORS.items():
        dst = out_dir / f"{name}.cube"
        written.append(write_cube(dst, size, fn))
    return written


def main(argv: list[str] | None = None) -> int:
    """CLI entry: ``python -m colorkit.luts --all [--out DIR] [--size N]``."""
    parser = argparse.ArgumentParser(
        prog="colorkit.luts",
        description="Generate the colorkit film-look .cube LUT library (stdlib-only).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Write all five looks (neutral_correct, warm_interview, teal_orange, "
             "kodak_2383_style, fuji_style).",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT_DIR),
        help=f"Output directory for the .cube files (default: {DEFAULT_OUT_DIR}).",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=DEFAULT_SIZE,
        help=f"LUT_3D_SIZE / cube edge length (default: {DEFAULT_SIZE}).",
    )
    args = parser.parse_args(argv)

    if not args.all:
        parser.error("nothing to do: pass --all to write the look library.")

    written = _write_all(args.out, args.size)
    print(f"Wrote {len(written)} LUT(s) (LUT_3D_SIZE={args.size}) to {Path(args.out).resolve()}:")
    for p in written:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
