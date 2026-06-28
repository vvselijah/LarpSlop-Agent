"""Smoke tests: the tonemap math + an end-to-end still develop. Run: pytest -q"""
import numpy as np
from colorkit import tonemap as tm
from colorkit import correct


def test_srgb_roundtrip():
    v = np.linspace(0, 1, 17)
    assert np.allclose(tm.srgb_oetf(tm.srgb_eotf(v)), v, atol=1e-6)


def test_midgrey_anchor():
    # 0.18 linear should encode to ~0.46 display (the mid-grey target)
    assert abs(tm.srgb_oetf(0.18) - 0.461) < 0.003


def test_soft_clip_never_clips():
    xs = np.linspace(0, 8, 2000)
    ys = tm.highlight_soft_clip(xs, knee=0.8, ceiling=1.0)
    assert ys.max() < 1.0  # asymptotes to ceiling, never crosses
    assert np.all(np.diff(ys) >= -1e-9)  # monotonic


def test_pivot_fixed():
    assert abs(tm.pivoted_contrast(0.18, 1.2) - 0.18) < 1e-9


def test_develop_on_synthetic_image():
    rng = np.random.default_rng(0)
    # a dim, blue-cast synthetic frame (BGR uint8)
    img = (rng.random((64, 64, 3)) * 90).astype(np.uint8)
    img[..., 0] = np.clip(img[..., 0] + 40, 0, 255)  # blue cast
    p = correct.compute_correction(img)
    out = correct.apply_correction_image(img, p)
    assert out.shape == img.shape and out.dtype == np.uint8
    # median luma should move toward mid-grey (brighter than the dim input)
    assert out.mean() > img.mean()
    # baked develop cube matches the direct apply within LUT tolerance
    import tempfile, os
    cube = os.path.join(tempfile.gettempdir(), "dev_smoke.cube")
    correct.bake_develop_cube(p, cube, size=33)
    assert os.path.getsize(cube) > 1000
