"""decide.py: the widened (10-look) deterministic brain + AI-stub fallback. Run: pytest -q"""
from colorkit import decide


def _pick(**stats):
    return decide.suggest_look(stats)["look"]


def test_all_ten_looks_reachable():
    """Each look has a crafted scene that selects it (first-match-wins rule coverage)."""
    cases = {
        # skin branch: bright+soft -> portra, else warm_interview
        "portra_style":     dict(skin_frac=0.20, brightness=0.70, contrast=0.10),
        "warm_interview":   dict(skin_frac=0.20, brightness=0.40, contrast=0.30),
        # foliage
        "fuji_style":       dict(skin_frac=0.0, green_frac=0.30),
        # warm branch: bright -> golden_hour, else kodak
        "golden_hour":      dict(warmth=0.15, brightness=0.70),
        "kodak_2383_style": dict(warmth=0.15, brightness=0.40),
        # cool branch: dark -> moody_blue, else teal_orange
        "moody_blue":       dict(warmth=-0.10, brightness=0.20),
        "teal_orange":      dict(warmth=-0.10, brightness=0.50),
        # bright+punchy neutral -> clean_pop (low contrast so the cinematic rule doesn't pre-empt)
        "clean_pop":        dict(warmth=0.0, brightness=0.70, saturation=0.40, contrast=0.15),
        # gritty desaturated high-contrast -> bleach_bypass
        "bleach_bypass":    dict(warmth=0.0, brightness=0.50, saturation=0.10, contrast=0.30),
        # nothing decisive -> neutral
        "neutral_correct":  dict(warmth=0.0, brightness=0.50, saturation=0.20, contrast=0.15),
    }
    for expected, stats in cases.items():
        assert _pick(**stats) == expected, f"{stats} -> {_pick(**stats)}, expected {expected}"
    # and the set actually exercises all ten distinct looks
    assert set(cases) == set(decide.VALID_LOOKS)


def test_cinematic_high_contrast_saturated_is_teal():
    """A saturated, high-contrast, hue-neutral scene reads cinematic -> teal_orange (rule 5)."""
    assert _pick(warmth=0.0, brightness=0.50, saturation=0.40, contrast=0.30) == "teal_orange"


def test_choice_shape_and_clamping():
    """LookChoice has the contract keys; opacity/confidence are clamped to [0,1]; bad look -> neutral."""
    c = decide.suggest_look({"skin_frac": 0.5}, opacity=1.7)
    assert set(c) >= {"look", "opacity", "reason", "confidence", "stats", "ai"}
    assert 0.0 <= c["opacity"] <= 1.0 and 0.0 <= c["confidence"] <= 1.0
    bad = decide._choice("does_not_exist", 0.7, "x", 0.5, {})
    assert bad["look"] == "neutral_correct"


def test_ai_stub_falls_back_to_deterministic():
    """suggest_look_ai is a no-op stub: same look as the brain, tagged ai=False (Elijah-gated)."""
    stats = {"skin_frac": 0.2, "brightness": 0.4, "contrast": 0.3}
    ai = decide.suggest_look_ai(stats=stats, provider="agent")
    assert ai["ai"] is False
    assert ai["look"] == decide.suggest_look(stats)["look"]
    assert "not wired" in ai["reason"]
