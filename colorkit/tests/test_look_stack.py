"""Cinematic look-stack: color-only no-op, stacked looks differ, grain determinism. Run: pytest -q"""
import numpy as np

from colorkit import stylize


def _frame():
    return (np.random.RandomState(0).rand(80, 120, 3) * 255).astype(np.uint8)


def test_color_only_look_has_no_stack():
    """A look with an empty stack (clean_pop) -> apply_look_stack_image == apply_look_image."""
    f = _frame()
    a = stylize.apply_look_image(f, "clean_pop", opacity=0.7)
    b = stylize.apply_look_stack_image(f, "clean_pop", opacity=0.7)
    assert np.array_equal(a, b)


def test_stacked_look_differs_and_preserves_shape_dtype():
    f = _frame()
    a = stylize.apply_look_image(f, "kodak_2383_style", opacity=0.7)            # color only
    b = stylize.apply_look_stack_image(f, "kodak_2383_style", opacity=0.7)      # + optical stack
    assert b.shape == f.shape and b.dtype == f.dtype
    assert not np.array_equal(a, b)  # halation/grain changed it


def test_grain_is_deterministic():
    """Seeded static plate -> reproducible (the anti-flicker guarantee)."""
    f = _frame()
    assert np.array_equal(stylize.apply_grain_image(f, strength=0.4, seed=7),
                          stylize.apply_grain_image(f, strength=0.4, seed=7))


def test_vignette_darkens_corners_not_center():
    f = (np.ones((60, 60, 3)) * 200).astype(np.uint8)
    out = stylize.apply_vignette_image(f, strength=0.3)
    assert int(out[0, 0].mean()) <= int(out[30, 30].mean())


def test_spatial_effects_preserve_shape_dtype():
    f = _frame()
    for fn in (stylize.apply_halation_image, stylize.apply_grain_image, stylize.apply_vignette_image):
        out = fn(f)
        assert out.shape == f.shape and out.dtype == f.dtype


# --- VIDEO path: optical-stack plan, plate bakers, ffmpeg filtergraph segments ------------------- #

def test_optical_stack_plan_scales_strength_with_opacity():
    """The video plan mirrors apply_look_stack_image: ordered effects, strength faded by opacity."""
    full = dict(stylize.optical_stack_plan("kodak_2383_style", 1.0))
    half = dict(stylize.optical_stack_plan("kodak_2383_style", 0.5))
    assert set(full) == {"halation", "grain"}
    assert abs(half["grain"]["strength"] - full["grain"]["strength"] * 0.5) < 1e-9
    # color-only look / no look -> empty plan (the render takes the byte-identical -vf path)
    assert stylize.optical_stack_plan("clean_pop", 0.7) == []
    assert stylize.optical_stack_plan(None, 0.7) == []
    # order is always halation -> grain -> vignette
    portra = [e for e, _ in stylize.optical_stack_plan("portra_style", 0.7)]
    assert portra == ["halation", "grain", "vignette"]


def test_grain_plate_deterministic_and_sized(tmp_path):
    """Seeded plate -> reproducible (flicker-free across frames/shots), correct size, mid-grey centred."""
    import cv2
    a, b = tmp_path / "g1.png", tmp_path / "g2.png"
    stylize.bake_grain_plate(str(a), 64, 96, strength=0.4, seed=7)
    stylize.bake_grain_plate(str(b), 64, 96, strength=0.4, seed=7)
    ia = cv2.imread(str(a), cv2.IMREAD_GRAYSCALE)
    ib = cv2.imread(str(b), cv2.IMREAD_GRAYSCALE)
    assert ia.shape == (96, 64)
    assert np.array_equal(ia, ib)                 # deterministic -> the anti-flicker guarantee
    assert abs(float(ia.mean()) - 127.5) < 6.0    # centred on mid-grey (overlay identity point)


def test_vignette_mask_darkens_edges_not_center(tmp_path):
    import cv2
    p = tmp_path / "v.png"
    stylize.bake_vignette_mask(str(p), 80, 80, strength=0.4)
    m = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
    assert m.shape == (80, 80)
    assert int(m[40, 40]) == 255                  # center: no darken (v == 1)
    assert int(m[0, 0]) < int(m[40, 40])          # corner is darkened


def test_ffmpeg_segments_are_wellformed():
    """The filtergraph fragments are wired by label and carry the load-bearing options."""
    hal = stylize.ffmpeg_halation_segment("m0", "opt0", strength=0.385, sigma=23)
    assert hal.startswith("[m0]") and hal.endswith("[opt0]")
    assert "t=linear" in hal and "blend=all_mode=screen" in hal  # screened in linear light
    grn = stylize.ffmpeg_grain_segment("opt0", "1:v", "opt1")
    assert grn.endswith("[opt1]") and "scale2ref" in grn and "shortest=1" in grn  # bounded looped plate
    vig = stylize.ffmpeg_vignette_segment("opt1", "2:v", "opt2")
    assert vig.endswith("[opt2]") and "multiply" in vig and "shortest=1" in vig
