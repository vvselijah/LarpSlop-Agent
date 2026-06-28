"""colorkit.decide -- the "pick-the-look" DECISION layer (auto-look selection).

The engine's architecture splits **measurement** (pixel-math; ``measure.py`` / ``correct.py``) from
**decision** (which creative look to apply). Correction is deterministic and always safe; the *look*
is an editorial choice. So far that choice has been the operator's (``--look NAME``). This module is
the optional layer that makes it automatic: given a representative frame, choose a look.

Two brains, one interface (``suggest_look``):

1. **Deterministic brain (DEFAULT, no API, runs now).** Maps cheap scene signals from
   :func:`colorkit.measure.scene_stats` (skin fraction, foliage, warmth, saturation, brightness,
   contrast) onto a look using the masterclass color-theory: skin-heavy talking-head -> a flattering
   warm interview look; foliage/nature -> the Fuji greens; warm low-skin (golden-hour / interior) ->
   warm print density; cool/high-variety outdoor -> the cinematic teal-orange; otherwise the gentle
   neutral pass. This is intentionally conservative -- it never picks a portrait look for a clip with
   no people, which is the failure mode the build-status backlog flagged.

2. **AI brain (SKETCH, opt-in).** :func:`suggest_look_ai` is the interface for a vision model
   (TwelveLabs Pegasus via the video-analyzer MCP, a Claude vision agent à la auto-clip's
   ``--provider agent``, or Gemini when its key is live) to classify mood/content/genre and pick a
   look with a rationale. It is a stub here -- it falls back to the deterministic brain -- with the
   full design in ``docs/plans/2026-06-24-color-ai-decision-layer.md``. Wiring a real model is
   Elijah-gated (cost / external call), per the hub's golden rule.

A :class:`LookChoice` is a plain dict ``{"look", "opacity", "reason", "confidence", "stats"}``.
DRAFT-only and side-effect-free: this module returns a recommendation; ``color.py`` decides whether
to apply it. It never publishes, never calls the network on its own.
"""
from __future__ import annotations

from typing import Dict, Optional

__all__ = ["suggest_look", "suggest_look_ai", "LookChoice", "VALID_LOOKS"]

# The set the deterministic brain may auto-pick from -- ALL 10 looks (widened 2026-06-27). Each look is
# still reached by a conservative, scene-gated rule (see suggest_look), so the brain only picks a look
# when its scene signal is clearly present; the safe default remains neutral_correct. The 2026-06-24
# looks (golden_hour, moody_blue, bleach_bypass, clean_pop, portra_style) are now auto-pickable as
# refinements of the original five branches. All entries must exist in stylize.LOOKS / luts.
VALID_LOOKS = (
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
)

LookChoice = Dict[str, object]

# --- decision thresholds (tunable; conservative by design) ------------------
_SKIN_PORTRAIT = 0.08      # >=8% skin pixels -> a person is meaningfully in frame
_GREEN_NATURE = 0.18       # >=18% foliage -> nature/outdoor scene
_WARM_CAST = 0.06          # mean (R-B)/255 above this reads as a warm/golden scene
_COOL_CAST = -0.02         # below this reads cool (blue hour / shade / overcast)
_DEFAULT_OPACITY = 0.7     # the masterclass "tasteful, not a filter" default
# refinement thresholds for the widened (10-look) brain
_BRIGHT = 0.55             # >= this mean luma reads as a bright/high-key scene
_BRIGHT_POP = 0.60         # ...brighter still -> a clean commercial/product key
_DARK = 0.32               # <= this mean luma reads as a dark/night scene
_SOFT_CONTRAST = 0.18      # <= this tonal spread reads as soft/low-contrast (gentle portrait)
_SAT_POP = 0.33            # >= this saturation reads as punchy/vivid
_GRIT_CONTRAST = 0.26      # >= this contrast with...
_GRIT_SAT = 0.18           # ...<= this saturation reads as gritty/desaturated (bleach bypass)


def suggest_look(stats: Dict[str, float], *, opacity: float = _DEFAULT_OPACITY) -> LookChoice:
    """Deterministic look pick from :func:`colorkit.measure.scene_stats` signals (all 10 looks).

    Ordered rules, first match wins (so a portrait is decided by its skin, not its background). Each
    original branch now refines into a 2026-06-24 look when a secondary signal (brightness / contrast /
    saturation) is decisive, else keeps the safe original:

    1. **skin-heavy** (``skin_frac >= 0.08``) -> ``portra_style`` if the frame is bright + soft (a gentle
       high-key portrait), else ``warm_interview`` (the flattering default). Opacity eased on tight
       close-ups so the look stays gentle on faces (never key skin hard; masterclass).
    2. **foliage/nature** (``green_frac >= 0.18`` and low skin) -> ``fuji_style`` -- the Fuji greens.
    3. **warm scene** (``warmth >= 0.06`` and low skin) -> ``golden_hour`` if bright (aspirational amber
       glow), else ``kodak_2383_style`` (warm print density for warm interiors).
    4. **cool scene** (``warmth <= -0.02``) -> ``moody_blue`` if dark (night / urban), else
       ``teal_orange`` (the cinematic complementary look).
    5. **cinematic high-contrast + saturated** (``contrast >= 0.22`` and ``sat >= 0.30``) ->
       ``teal_orange``.
    6. **bright + punchy** (``brightness >= 0.60`` and ``sat >= 0.33``) -> ``clean_pop`` -- a clean
       commercial / product / IG key.
    7. **gritty** (``contrast >= 0.26`` and ``sat <= 0.18``) -> ``bleach_bypass`` -- silver-retention.
    8. **otherwise** -> ``neutral_correct`` -- let the develop speak; a whisper of a look.

    Returns a :class:`LookChoice`. ``confidence`` is a rough 0..1 from how decisively the signals
    matched (it is advisory -- ``color.py`` always applies the chosen look; confidence is for logs).
    """
    s = {k: float(v) for k, v in (stats or {}).items()}
    skin = s.get("skin_frac", 0.0)
    green = s.get("green_frac", 0.0)
    warmth = s.get("warmth", 0.0)
    sat = s.get("saturation", 0.0)
    bright = s.get("brightness", 0.5)
    contrast = s.get("contrast", 0.0)

    op = float(opacity)

    if skin >= _SKIN_PORTRAIT:
        # Tighter on faces -> ease the look so skin stays natural (never key skin hard; masterclass).
        conf = min(1.0, 0.5 + skin * 2.0)
        if skin >= 0.30:
            op = min(op, 0.6)
        if bright >= _BRIGHT and contrast <= _SOFT_CONTRAST:
            return _choice("portra_style", op,
                           f"skin_frac={skin:.2f}, bright {bright:.2f}/soft {contrast:.2f} -> high-key "
                           f"portrait; Portra soft pastel keeps skin gentle", conf, s)
        return _choice("warm_interview", op,
                       f"skin_frac={skin:.2f} -> talking-head/portrait; warm interview look "
                       f"keeps skin flattering", conf, s)

    if green >= _GREEN_NATURE:
        conf = min(1.0, 0.5 + green)
        return _choice("fuji_style", op,
                       f"green_frac={green:.2f} -> foliage/nature; Fuji greens suit it", conf, s)

    if warmth >= _WARM_CAST:
        conf = min(1.0, 0.5 + warmth * 3.0)
        if bright >= _BRIGHT:
            return _choice("golden_hour", op,
                           f"warmth={warmth:+.2f}, bright {bright:.2f} -> golden/high-key; "
                           f"golden-hour amber glow", conf, s)
        return _choice("kodak_2383_style", op,
                       f"warmth={warmth:+.2f} -> warm/golden scene; Kodak print density", conf, s)

    if warmth <= _COOL_CAST:
        conf = min(1.0, 0.45 + max(0.0, -warmth) * 2.0 + contrast)
        if bright <= _DARK:
            return _choice("moody_blue", op,
                           f"warmth={warmth:+.2f}, dark {bright:.2f} -> night/urban; moody teal-blue",
                           conf, s)
        return _choice("teal_orange", op,
                       f"warmth={warmth:+.2f} -> cool/cinematic; teal-orange complementary", conf, s)

    if contrast >= 0.22 and sat >= 0.30:
        conf = min(1.0, 0.45 + contrast + sat * 0.3)
        return _choice("teal_orange", op,
                       f"contrast={contrast:.2f}, sat={sat:.2f} -> high-variety cinematic; "
                       f"teal-orange complementary", conf, s)

    if bright >= _BRIGHT_POP and sat >= _SAT_POP:
        conf = min(1.0, 0.45 + (bright - _BRIGHT_POP) * 2.0 + sat * 0.3)
        return _choice("clean_pop", op,
                       f"bright {bright:.2f}, sat {sat:.2f} -> clean commercial key; clean_pop punch",
                       conf, s)

    if contrast >= _GRIT_CONTRAST and sat <= _GRIT_SAT:
        conf = min(1.0, 0.45 + contrast)
        return _choice("bleach_bypass", op,
                       f"contrast {contrast:.2f}, low sat {sat:.2f} -> gritty; bleach-bypass "
                       f"silver retention", conf, s)

    return _choice("neutral_correct", op,
                   "no strong content/colour signal -> neutral pass; let the develop speak", 0.4, s)


def suggest_look_ai(
    video_path: Optional[str] = None,
    stats: Optional[Dict[str, float]] = None,
    *,
    provider: str = "auto",
    opacity: float = _DEFAULT_OPACITY,
) -> LookChoice:
    """SKETCH: pick a look with a vision model (mood/content/genre), falling back to the brain.

    Intended providers (see ``docs/plans/2026-06-24-color-ai-decision-layer.md``):
      - ``"pegasus"``  : TwelveLabs Pegasus via the video-analyzer MCP -- classify scene/mood from the
                          actual clip (it already powers ``auto-clip``).
      - ``"agent"``    : a Claude vision agent reading a few representative frames (auto-clip's
                          ``--provider agent`` pattern; "Claude IS the brain", no API key).
      - ``"gemini"``   : Gemini video (currently quota-blocked in this hub).

    This stub does NOT call any model (that is an external call -> Elijah-gated). It returns the
    deterministic :func:`suggest_look` result, tagged so the caller can see the AI path was a no-op.
    When a provider is wired, it should return the SAME :class:`LookChoice` shape with a model-written
    ``reason`` and may override ``opacity``; on any model error it MUST fall back to ``suggest_look``.
    """
    # Shallow-copy before mutating so this never corrupts a (future) cached/shared LookChoice.
    base = dict(suggest_look(stats or {}, opacity=opacity))
    base["reason"] = f"[ai:{provider} not wired -> deterministic] " + str(base.get("reason", ""))
    base["ai"] = False
    return base


# --------------------------------------------------------------------------- #
# helpers                                                                      #
# --------------------------------------------------------------------------- #
def _choice(look: str, opacity: float, reason: str, confidence: float,
            stats: Dict[str, float]) -> LookChoice:
    """Assemble a validated LookChoice (clamps opacity/confidence; guards the look name)."""
    if look not in VALID_LOOKS:
        look = "neutral_correct"
    return {
        "look": look,
        "opacity": float(min(max(opacity, 0.0), 1.0)),
        "reason": reason,
        "confidence": float(min(max(confidence, 0.0), 1.0)),
        "stats": stats,
        "ai": False,
    }
