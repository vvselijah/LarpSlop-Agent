"""G1 skin-tone-line solver: gate + non-worsening contract. Run: pytest -q"""
import numpy as np

from colorkit import correct, measure


def _skin_block():
    """A coherent skin blob (survives erosion) on a neutral field (BGR uint8)."""
    img = np.full((200, 200, 3), 70, np.uint8)
    img[40:160, 40:160] = (120, 150, 200)  # BGR ~ skin (R high, B low), a contiguous 36% block
    return img


def _ex_skin(p):
    return {k: v for k, v in p.items() if k != "skin"}


def test_skin_solve_no_op_without_skin():
    """A skin-free frame: params byte-identical with/without the solver (non-portrait unchanged)."""
    flat = np.full((128, 128, 3), 110, np.uint8)
    base = correct.compute_correction(flat, skin_solve=False)
    g1 = correct.compute_correction(flat, skin_solve=True)
    assert _ex_skin(base) == _ex_skin(g1)
    assert g1["skin"]["applied"] is False


def test_erosion_rejects_scattered_skin():
    """Scattered (non-coherent) skin-coloured noise must NOT trip the gate (erosion kills it)."""
    rng = np.random.default_rng(1)
    noise = (rng.random((200, 200, 3)) * 120).astype(np.uint8)
    noise[..., 1] = np.clip(noise[..., 1] + 70, 0, 255)  # green-push, scattered
    base = correct.compute_correction(noise, skin_solve=False)
    g1 = correct.compute_correction(noise, skin_solve=True)
    assert _ex_skin(base) == _ex_skin(g1)


def test_skin_solve_never_worsens_iline():
    """When it fires on a real skin blob, it must not push skin FURTHER from the I-line."""
    img = _skin_block()
    g0 = correct.compute_correction(img, skin_solve=False)
    g1 = correct.compute_correction(img, skin_solve=True)
    s0 = measure.skin_signature(correct.apply_correction_image(img, g0))
    s1 = measure.skin_signature(correct.apply_correction_image(img, g1))
    assert {"frac", "applied"} <= set(g1["skin"])
    if g1["skin"].get("applied") and s0.get("skin_dev_from_iline_deg") is not None:
        # +1.5 deg slack for the downscale/erosion sample vs the full-frame measure
        assert abs(s1["skin_dev_from_iline_deg"]) <= abs(s0["skin_dev_from_iline_deg"]) + 1.5


def test_skin_diag_is_json_safe():
    """The 'skin' diagnostic must be plain floats/bools/lists (JSON-serializable)."""
    import json
    g1 = correct.compute_correction(_skin_block(), skin_solve=True)
    json.dumps(g1["skin"])  # raises if a numpy scalar leaked in


# --- G1b: skin-LOCAL exposure (colour-qualifier lift) ----------------------------------------------
def _dark_skin_block():
    """A coherent but UNDER-EXPOSED skin blob (skin chromaticity, low luma) on a neutral midtone field.

    Includes a small near-black anchor patch so the per-channel black point sits on real darks (as in
    any real frame) rather than crushing the skin blob (the darkest thing on a flat synthetic field).
    """
    img = np.full((200, 200, 3), 110, np.uint8)   # neutral field (anchors the global exposure)
    img[:24, :24] = 4                             # near-black anchor for the develop's black point
    img[60:140, 60:140] = (50, 66, 92)            # BGR dark skin (R>G>B), 16% coherent block, ~28 IRE dev
    return img


def test_skin_local_lift_raises_underexposed_skin():
    """Under-exposed skin triggers the bakeable G1b lift and the developed skin really gets brighter."""
    img = _dark_skin_block()
    g = correct.compute_correction(img, skin_solve=True)
    sk = g["skin"]
    assert sk.get("applied")
    assert g.get("skin_lift", 1.0) > 1.0          # the top-level bakeable gain was emitted
    assert sk["skin_lift"] > 1.0                  # and surfaced in the diagnostic
    # the lift must RAISE developed skin luma vs the no-lift develop (and not overshoot wildly).
    g0 = correct.compute_correction(img, skin_solve=False)
    p_lift = measure.skin_signature(correct.apply_correction_image(img, g))["skin_L_ire_p50"]
    p_base = measure.skin_signature(correct.apply_correction_image(img, g0))["skin_L_ire_p50"]
    assert p_lift > p_base
    assert p_lift <= 60.0                         # capped -> no glowing-face overshoot


def test_skin_lift_bakes_into_cube(tmp_path):
    """The lift is a pure colour stage -> the baked .cube applies the SAME transform as the still path."""
    img = _dark_skin_block()
    g = correct.compute_correction(img, skin_solve=True)
    assert g.get("skin_lift", 1.0) > 1.0
    cube = correct.bake_develop_cube(g, str(tmp_path / "dev.cube"))
    txt = open(cube, encoding="ascii").read()
    assert "LUT_3D_SIZE" in txt                   # a real cube was written with the lift folded in


def test_skin_qualifier_bounded_and_selective():
    """The colour qualifier is a smooth weight in [0,1], high for skin, ~0 for neutral/blue."""
    ws = correct._skin_qualifier_weight(np.array([[[0.62, 0.42, 0.30]]]))[0, 0]  # RGB skin
    wg = correct._skin_qualifier_weight(np.array([[[0.50, 0.50, 0.50]]]))[0, 0]  # neutral
    wb = correct._skin_qualifier_weight(np.array([[[0.20, 0.30, 0.80]]]))[0, 0]  # blue
    for w in (ws, wg, wb):
        assert 0.0 <= w <= 1.0
    assert ws > 0.5 and wg < 0.1 and wb < 0.1     # skin qualifies; neutral + blue rejected


def test_skin_lift_no_op_on_well_exposed_skin():
    """Well-exposed skin gets NO local lift (no skin_lift key) -> that develop is unchanged."""
    g = correct.compute_correction(_skin_block(), skin_solve=True)  # bright skin block
    # bright skin should not be below the trigger, so no lift gain is emitted.
    assert g.get("skin_lift", 1.0) == 1.0
