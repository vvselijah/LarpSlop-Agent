"""colorkit.hdr -- HDR (HLG/PQ) detection + the HDR->SDR tonemap stage (Stage -1).

The Insta360 Luna (and most modern phones/cameras) can shoot **HLG** (Rec.2020 primaries +
``arib-std-b67`` transfer) and **PQ** (``smpte2084``) in their HDR modes. That footage cannot be
graded directly by the engine's Rec.709 linear-light develop: decoding HDR code values as if they
were SDR yields the washed, lifted-black, desaturated look (empirically verified -- a naive 8-bit
decode of an HLG clip is milky/flat; a proper tonemap restores deep blacks, contrast and colour).

So for HDR sources we insert a **Stage -1** that tone-maps Rec.2020 HDR -> Rec.709 SDR BEFORE the
input transform / develop. It is the FIRST per-shot filter and is applied identically to the
representative frame used for measurement, so the develop measures the same SDR signal the render
produces (the constant-per-shot anti-flicker rule is preserved -- the whole tonemap+develop is one
fixed transform per shot).

Two engines (both verified on this hub's ffmpeg 8.1-full Gyan build):

* ``"zscale"`` -- the **DEFAULT**. CPU / libzimg, fully deterministic, no GPU dependency. Pipeline:
  ``zscale`` linearize (HLG/PQ -> scene-linear) -> ``tonemap`` (hable filmic shoulder) -> ``zscale``
  encode to Rec.709 SDR. Operators: ``hable`` (default), ``mobius`` (gentler highlights),
  ``reinhard``.
* ``"placebo"`` -- libplacebo (Vulkan GPU). ITU-R **BT.2390** reference tone-mapping: best gamut /
  hue handling, richest result, but adds a Vulkan device dependency, so it is opt-in. Requires the
  caller to also pass ``device_args("placebo")`` (``-init_hw_device vulkan``) to ffmpeg.

This module is pure-stdlib (only ``io_utils`` for the ffprobe call) -- no cv2/numpy -- so importing
it is cheap and side-effect-free, matching the package's lazy-by-design discipline.
"""
from __future__ import annotations

import json
from typing import Dict, List, Optional, Tuple

from . import io_utils

__all__ = [
    "probe_color",
    "is_hdr",
    "describe",
    "tonemap_filter",
    "device_args",
    "resolve_tonemap_spec",
    "HDR_TRANSFERS",
    "ZSCALE_OPERATORS",
]

# Transfer characteristics that mean the signal is HDR (must be tonemapped before an SDR grade).
HLG_TRANSFER = "arib-std-b67"
PQ_TRANSFER = "smpte2084"
HDR_TRANSFERS = {HLG_TRANSFER, PQ_TRANSFER, "bt2020-10", "bt2020-12"}

# tonemap operators the CPU ``tonemap`` filter (libavfilter) accepts.
ZSCALE_OPERATORS = {"none", "clip", "linear", "gamma", "reinhard", "hable", "mobius"}
# operators of that set which take a numeric ``param`` (others reject it).
_PARAM_OPERATORS = {"mobius", "reinhard", "gamma"}
# libplacebo's reference tonemapper.
_PLACEBO_TONEMAP = "bt.2390"
# Matrix-coefficient names ``zscale``'s ``min=`` accepts (ffprobe-style + zimg aliases). Any
# ``color_space`` tag outside this set would make the first zscale filter fail to init, so we fall
# back to bt2020nc (the camera's HLG/PQ matrix) for anything unrecognized.
_ZSCALE_MATRIX_OK = {
    "bt709", "709", "bt2020nc", "2020_ncl", "bt2020c", "2020_cl",
    "smpte170m", "170m", "smpte240m", "240m", "bt470bg", "470bg",
    "fcc", "ycgco", "unspecified", "unspec", "input",
}


# --------------------------------------------------------------------------- #
# Probe                                                                        #
# --------------------------------------------------------------------------- #
def probe_color(video_path) -> Dict[str, object]:
    """ffprobe the first video stream's colour tagging + basic geometry.

    Returns a plain dict (JSON-safe) with keys: ``codec_name``, ``width``, ``height``,
    ``pix_fmt``, ``color_transfer``, ``color_primaries``, ``color_space`` (any may be ``None`` /
    ``"unknown"`` when the file omits the tag). Never raises -- on any ffprobe failure it returns a
    dict of ``None`` values so callers degrade to "treat as SDR".
    """
    empty = {
        "codec_name": None, "width": None, "height": None, "pix_fmt": None,
        "color_transfer": None, "color_primaries": None, "color_space": None,
    }
    try:
        r = io_utils.run_ffprobe([
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries",
            "stream=codec_name,width,height,pix_fmt,color_transfer,color_primaries,color_space",
            "-of", "json",
            str(video_path),
        ])
        if getattr(r, "returncode", 1) != 0 or not (r.stdout and r.stdout.strip()):
            return empty
        streams = (json.loads(r.stdout) or {}).get("streams") or []
        if not streams:
            return empty
        s = streams[0]
        out = dict(empty)
        for k in empty:
            v = s.get(k)
            if v is not None and v != "unknown":
                out[k] = v
        return out
    except Exception:
        return empty


def is_hdr(meta: Dict[str, object]) -> bool:
    """True if ``meta`` (from :func:`probe_color`) describes an HDR signal needing a tonemap.

    HDR if the transfer is HLG/PQ/bt2020-10/12, OR the primaries are Rec.2020 (a wide-gamut signal
    we still want mapped to Rec.709 even if the transfer tag is missing/odd).
    """
    t = str(meta.get("color_transfer") or "").lower()
    p = str(meta.get("color_primaries") or "").lower()
    return t in HDR_TRANSFERS or p == "bt2020"


def describe(meta: Dict[str, object]) -> str:
    """Short human label for logs, e.g. ``HLG bt2020 (yuv420p10le)``."""
    t = str(meta.get("color_transfer") or "?")
    label = "HLG" if t == HLG_TRANSFER else ("PQ" if t == PQ_TRANSFER else t)
    return f"{label} {meta.get('color_primaries') or '?'} ({meta.get('pix_fmt') or '?'})"


# --------------------------------------------------------------------------- #
# Tonemap filtergraph construction                                            #
# --------------------------------------------------------------------------- #
def _zscale_transfer_in(meta: Dict[str, object]) -> str:
    """The ``zscale`` input-transfer name for this HDR meta (defaults to HLG for the camera)."""
    t = str(meta.get("color_transfer") or "").lower()
    if t == PQ_TRANSFER:
        return PQ_TRANSFER
    if t == HLG_TRANSFER:
        return HLG_TRANSFER
    # Wide-gamut primaries but missing/odd transfer -> assume HLG (the camera's HDR default).
    return HLG_TRANSFER


def tonemap_filter(
    meta: Dict[str, object],
    *,
    engine: str = "zscale",
    operator: str = "hable",
    npl: int = 100,
    desat: float = 0.0,
    param: Optional[float] = None,
) -> str:
    """Build the ffmpeg filtergraph STRING that maps this HDR signal to Rec.709 SDR.

    Parameters
    ----------
    meta
        Colour metadata from :func:`probe_color` (used to set the zscale input hints).
    engine
        ``"zscale"`` (CPU, default) or ``"placebo"`` (libplacebo, Vulkan; remember
        :func:`device_args`).
    operator
        zscale tonemap operator (``hable`` default; ``mobius``/``reinhard`` alternatives). Ignored
        for the placebo engine (which always uses BT.2390).
    npl
        Nominal peak luminance (nits) of the SDR target for the tonemap (100 = standard SDR).
    desat
        Highlight desaturation strength passed to the ``tonemap`` filter (0 = keep colour;
        higher fades bright pixels toward white -- film-like but can wash, so default 0).
    param
        Numeric parameter for operators that accept one (``mobius``/``reinhard``/``gamma``).

    Returns
    -------
    str
        A comma-joined filtergraph ending in ``format=yuv420p`` (SDR Rec.709, limited range), ready
        to be the FIRST element of a per-shot vf chain (or applied to a single frame for
        measurement).
    """
    if engine == "placebo":
        # libplacebo handles linearization, gamut + tone mapping, and Rec.709 encode in one pass.
        return (
            f"libplacebo=tonemapping={_PLACEBO_TONEMAP}:colorspace=bt709:"
            "color_primaries=bt709:color_trc=bt709:range=tv,format=yuv420p"
        )

    tin = _zscale_transfer_in(meta)
    matrix_in = str(meta.get("color_space") or "").strip().lower()
    if matrix_in not in _ZSCALE_MATRIX_OK:  # reject odd/unknown tags zscale's min= would choke on
        matrix_in = "bt2020nc"
    pin = str(meta.get("color_primaries") or "bt2020") or "bt2020"
    op = operator if operator in ZSCALE_OPERATORS else "hable"

    tone = f"tonemap=tonemap={op}"
    if param is not None and op in _PARAM_OPERATORS:
        tone += f":param={param}"
    tone += f":desat={desat}"

    # linearize (read HDR tags) -> 32-bit float linear RGB -> map primaries to 709 -> tonemap ->
    # encode to Rec.709 gamma, limited range, 8-bit 4:2:0 (the engine's SDR working/delivery domain).
    return (
        f"zscale=tin={tin}:min={matrix_in}:pin={pin}:rin=tv:t=linear:npl={npl},"
        "format=gbrpf32le,zscale=p=bt709,"
        f"{tone},"
        "zscale=t=bt709:m=bt709:p=bt709:r=tv,format=yuv420p"
    )


def device_args(engine: str) -> List[str]:
    """ffmpeg global args required by the chosen engine (``-init_hw_device vulkan`` for placebo)."""
    return ["-init_hw_device", "vulkan"] if engine == "placebo" else []


def resolve_tonemap_spec(spec: Optional[str]) -> Optional[Tuple[str, str]]:
    """Map the ``--hdr-tonemap`` CLI value to ``(engine, operator)`` or ``None`` (disabled).

    ``auto`` (default) / ``on`` -> zscale + hable.  ``hable``/``mobius``/``reinhard`` -> zscale with
    that operator.  ``placebo`` -> libplacebo BT.2390.  ``none``/``off`` -> ``None``.
    """
    val = (spec or "auto").strip().lower()
    if val in {"none", "off", "false", "0", "no"}:
        return None
    if val in {"auto", "on", "true", "1", "default", ""}:
        return ("zscale", "hable")
    if val in {"placebo", "libplacebo", "vulkan"}:
        return ("placebo", "bt2390")
    if val in ZSCALE_OPERATORS:
        return ("zscale", val)
    # Unknown token -> safe default rather than an error (engine is robustness-first).
    return ("zscale", "hable")
