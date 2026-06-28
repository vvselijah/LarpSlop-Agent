"""Smoke tests for the measurement layer: scopes + skin_signature. Run: pytest -q"""
import numpy as np

from colorkit import measure, scopes


def _skin_frame():
    """A frame with a believable skin patch (BGR uint8): warm midtone center on a neutral field."""
    img = np.full((128, 128, 3), 90, np.uint8)
    img[32:96, 32:96] = (110, 150, 190)  # BGR ~ skin orange (R high, B low)
    return img


def test_scope_reads_are_sane():
    img = _skin_frame()
    wf = scopes.waveform(img)
    assert 0.0 <= wf["black_p1_ire"] <= 100.0
    assert 0.0 <= wf["white_p99_ire"] <= 100.0
    pr = scopes.parade(img)
    assert "low_spread_ire" in pr and "high_spread_ire" in pr
    cl = scopes.clip_stats(img)
    assert 0.0 <= cl["pct_white_clip"] <= 100.0
    vs = scopes.vectorscope(img)
    assert 0.0 <= vs["hue_centroid_deg"] < 360.0


def test_skin_signature_keys():
    sig = measure.skin_signature(_skin_frame())
    expected = {"skin_frac", "skin_hue_deg", "skin_dev_from_iline_deg",
                "skin_L_ire_p50", "skin_L_ire_p90", "skin_chroma"}
    assert expected <= set(sig)
    assert 0.0 <= sig["skin_frac"] <= 1.0


def test_validate_verdict_shape():
    img = _skin_frame()
    sig = measure.skin_signature(img)
    rep = scopes.validate(img, sig)
    assert rep["n_total"] >= 7
    assert isinstance(rep["checks"], dict)
    assert rep["n_pass"] <= rep["n_total"]
    assert "verdict" in rep


def test_validate_without_skin():
    """A skin-free frame should still validate (skin checks simply skip)."""
    flat = np.full((64, 64, 3), 120, np.uint8)
    rep = scopes.validate(flat, measure.skin_signature(flat))
    assert rep["n_total"] >= 5  # the non-skin scope checks always run


def test_validate_output_is_json_serializable():
    """The --validate sidecar contract: every value scopes.validate returns must be plain-JSON.

    color.py / cli.py dump this dict straight to <stem>_validate.json, so a stray numpy scalar
    (np.float64/np.bool_) here would raise at render time. Lock that it never happens.
    """
    import json

    img = _skin_frame()
    rep = scopes.validate(img, measure.skin_signature(img))
    # Mirror the per-shot sidecar record color.py builds (context fields + the verdict dict).
    record = {"shot": 0, "start": 0.0, "end": 1.5, **rep}
    payload = {"input": "x.mov", "mode": "video", "results": [record]}
    text = json.dumps(payload)  # raises TypeError on a non-serializable (e.g. numpy) value
    round_trip = json.loads(text)
    assert round_trip["results"][0]["n_total"] == rep["n_total"]
    for chk in rep["checks"].values():
        assert isinstance(chk["pass"], bool)  # not np.bool_
