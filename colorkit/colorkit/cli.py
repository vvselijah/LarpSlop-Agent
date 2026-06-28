"""
auto-clip/color.py -- the agentic color-grading CLI orchestrator (Stage 0: Router).

Headless color engine entry point. Routes an input image OR video through the colorkit
pipeline and writes results ONLY under auto-clip/out/. NEVER publishes (CLAUDE.md rule 1).

Architecture (see docs/plans/2026-06-23-agentic-color-pipeline.md):
  - MEASUREMENT (pixel-math) decides numeric corrections; DECISION (the look) is a chosen LUT.
  - Canonical pro order: 1) correct each shot to neutral -> 2) match shots for continuity ->
    3) stylize on top.
  - NON-NEGOTIABLE video rule: derive ONE correction per shot from a representative frame and
    apply it as a CONSTANT transform to EVERY frame of that shot. Never per-frame-independent
    auto-correction -> that is what causes flicker / pumping.

Stage 2 (SHOT MATCHING -- inter-shot continuity, colorkit.match):
  Per-shot constant correction kills flicker *within* a shot but can leave visible color/exposure
  JUMPS at cut boundaries. Stage 2 reconciles them: pick a HERO shot, and for every other shot
  derive a constant Reinhard LAB mean/std transform (match.compute_match_params) that maps the
  shot's representative frame onto the hero's. Because the transform is constant per shot it stays
  flicker-free; we bake it into a tiny per-shot 3D LUT (.cube) and slot it into the per-shot
  filtergraph AFTER correction and BEFORE the creative look (correct -> match -> stylize). This is
  gated behind --match (opt-in): when off, color.py ships Stages 0/0b/1/3 and inter-shot matching
  is skipped, so a multi-shot clip may show cut-boundary jumps unless --match is passed.

Two input routes (by file extension):
  IMAGE  (.jpg/.jpeg/.png/.webp/.tif/.tiff):
      cv2.imread -> compute_correction -> apply_correction_image -> [apply_look_image]
      -> write <stem>_before.png + <stem>_after.png to out/.
  VIDEO  (.mp4/.mov/.mkv/.webm):
      detect_shots -> for EACH shot: extract a representative frame -> compute_correction ->
      build an ffmpeg filtergraph = correction (CONSTANT for the whole shot) [+ shot-match LUT
      when --match] [+ uniform look LUT]; apply per shot, then concat; write a single graded
      .mp4 to out/.

Usage (run from the auto-clip/ directory with the venv python):
  # still:
  .venv\\Scripts\\python.exe color.py path\\to\\frame.png --look teal_orange
  # video:
  .venv\\Scripts\\python.exe color.py path\\to\\clip.mp4 --look kodak_2383_style
  # correction only (no look):
  .venv\\Scripts\\python.exe color.py clip.mp4
  # stylize only, skip correction:
  .venv\\Scripts\\python.exe color.py clip.mp4 --look fuji_style --no-correct

Flags:
  input              positional; an image or a video file.
  --look NAME        a look from colorkit.stylize.LOOKS (default: none = correct-only).
  --no-correct       skip the auto color-correction stage (look-only).
  --out DIR          output directory (default: auto-clip/out). Resolved under colorkit OUT_DIR
                     when left at default, so outputs always land in the canonical out/.
  --match            VIDEO only: Stage 2 inter-shot continuity matching (Reinhard LAB transfer to
                     a hero shot, baked as a constant per-shot LUT). No-op on single-shot clips.
  --match-alpha A    strength of the shot-match transfer in [0,1] (default 0.8); lower = gentler.
  --deflicker        optional temporal backstop on the final video (ffmpeg deflicker+normalize).
  --keep-temp        keep per-shot intermediate files (debug); default removes them.

Writes (review only -- NOTHING is published):
  IMAGE: out/<stem>_before.png, out/<stem>_after.png
  VIDEO: out/<stem>_graded.mp4
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

# colorkit lives next to this file (auto-clip/colorkit/). We run from auto-clip/, so it imports
# directly. We import the package eagerly but rely on its lazy internals (no cv2 at top level).
from . import io_utils, measure, correct, stylize, segment, match, hdr, accel

BASE = Path(__file__).resolve().parent

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm"}

# --- v2 INPUT TRANSFORM (Stage 0) ------------------------------------------ #
# For camera Log footage the camera-correct first step is the manufacturer Log->Rec709 transform,
# applied BEFORE correction (the develop then refines a properly-developed Rec709 signal, not flat
# Log). We ship the official Insta360 Luna I-Log packs in colorkit/input_luts/. s65 = quality
# (the default), s33 = speed. Auto-detect targets I-Log by filename (the camera's H.265 MP4 carries
# no reliable "I-Log" metadata), or pass --input-lut explicitly.
INPUT_LUT_DIR = BASE / "input_luts"
ILOG_REC709_S65 = INPUT_LUT_DIR / "Luna_I-Log_to_Rec709_BT1886_s65_v2.cube"
ILOG_REC709_S33 = INPUT_LUT_DIR / "Luna_I-Log_to_Rec709_BT1886_s33_v2.cube"
_ILOG_NAME_RE = re.compile(r"(?:^|[ _\-])i[ _\-]?log|(?:^|[ _\-])log(?:[ _\-]|$)|slog|s-log|logc|vlog", re.I)


def _detect_input_lut(src: Path, arg: Optional[str]) -> Optional[Path]:
    """Resolve the Stage-0 input-transform LUT from the --input-lut arg + filename auto-detect.

    arg semantics:
      None / "auto"  -> auto-detect I-Log by filename; use the bundled Rec709 BT1886 s65 LUT if matched.
      "none"/"off"   -> no input transform.
      a known short name ("ilog","ilog_s33") or a path to a .cube -> use it.
    Returns an absolute Path to an existing .cube, or None (no input transform).
    """
    val = (arg or "auto").strip().lower()
    if val in {"none", "off", "false", "0"}:
        return None
    if val in {"auto", ""}:
        if _ILOG_NAME_RE.search(src.name):
            return ILOG_REC709_S65 if ILOG_REC709_S65.exists() else (
                ILOG_REC709_S33 if ILOG_REC709_S33.exists() else None)
        return None
    if val in {"ilog", "i-log", "ilog_s65", "rec709"}:
        return ILOG_REC709_S65 if ILOG_REC709_S65.exists() else None
    if val in {"ilog_s33", "fast"}:
        return ILOG_REC709_S33 if ILOG_REC709_S33.exists() else None
    # Otherwise treat as an explicit path.
    p = Path(arg).expanduser()
    if p.exists():
        return p.resolve()
    log(f"WARNING: --input-lut '{arg}' not found; proceeding without an input transform")
    return None


def log(msg: str) -> None:
    """Timestamped stdout line; tolerate the Windows cp1252 console choking on non-ASCII."""
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def _import_cv2():
    """Import cv2 lazily (heavy on the OneDrive disk; only needed for the image route)."""
    import cv2  # noqa: WPS433  (intentional lazy import)
    return cv2


def _log_skin(skin: Optional[dict], prefix: str = "") -> None:
    """One-line report of the G1 skin-tone-line solver's decision (from params['skin'])."""
    if not skin:
        return
    if not skin.get("applied"):
        log(f"{prefix}skin-solve: no-op ({skin.get('reason', 'n/a')}; "
            f"skin {float(skin.get('frac', 0.0)) * 100:.0f}%)")
        return
    tint = skin.get("tint")
    hot = "  [!] skin >70 IRE" if skin.get("skin_hot") else ""
    log(f"{prefix}skin-solve: hue {skin.get('hue_before')}°->{skin.get('hue_after')}° "
        f"(dev {skin.get('dev_before')}°->{skin.get('dev_after')}° to I-line) "
        f"p50 {skin.get('L_ire_p50_before')}->{skin.get('L_ire_p50_after')} IRE "
        f"tint={tint} exp_trim={skin.get('exp_trim')} lift={skin.get('skin_lift')}{hot}")


# --------------------------------------------------------------------------- #
# --validate -- scope self-validation (advisory; makes a grade falsifiable)    #
# --------------------------------------------------------------------------- #
# The masterclasses are unanimous that "scopes are ground truth". colorkit.scopes.validate() reads a
# CORRECTED (post-develop, PRE-creative-look) frame the way a colorist reads waveform/parade/
# vectorscope and asserts the demonstrated targets (black off-floor-not-milky, white in range, no
# clip, parade converged, skin on the ~123 deg I-line, skin 40-50 IRE). We validate the DEVELOPED
# domain -- a creative look intentionally departs from neutral, so it is NOT scored against neutral
# targets. Everything here is measurement only: it logs a verdict + writes an optional JSON sidecar,
# and NEVER alters a pixel or gates the render.
def _validate_frame(bgr) -> Optional[dict]:
    """Run scopes.validate on a developed BGR frame (+ its skin signature). Returns the verdict dict."""
    from . import scopes
    try:
        skin = measure.skin_signature(bgr)
    except Exception:
        skin = None
    try:
        return scopes.validate(bgr, skin)
    except Exception as exc:  # validation is advisory -- never let it crash a render
        log(f"  (validate skipped: {exc})")
        return None


def _log_validate(result: Optional[dict], prefix: str = "") -> None:
    """One-line verdict + any FAILING checks with value/target (advisory: scopes guide, eyes decide)."""
    if not result:
        return
    checks = result.get("checks") or {}
    fails = [n for n, c in checks.items() if not c.get("pass")]
    msg = f"{prefix}validate: {result.get('verdict', 'n/a')}"
    if fails:
        det = "; ".join(f"{n}={checks[n]['value']} (want {checks[n]['target']})" for n in fails)
        msg += f"  FAIL: {det}"
    log(msg)


def _write_validate_sidecar(out_dir: Path, stem: str, payload: dict) -> Path:
    """Write the --validate JSON sidecar (review only -- NOT published). Returns its path."""
    import json
    dst = out_dir / f"{stem}_validate.json"
    dst.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return dst


# --------------------------------------------------------------------------- #
# IMAGE route                                                                  #
# --------------------------------------------------------------------------- #
def process_image(
    src: Path,
    out_dir: Path,
    look_name: Optional[str],
    do_correct: bool,
    height: Optional[int] = None,
    input_lut: Optional[Path] = None,
    look_opacity: float = 0.7,
    strength: float = 1.0,
    skin_solve: bool = True,
    validate: bool = False,
) -> list[Path]:
    """Stage 0 (input transform) + Stage 1 + Stage 3 for a still: [input LUT] -> correct ->
    [stylize@opacity] -> before/after PNGs in out/."""
    cv2 = _import_cv2()

    bgr = cv2.imread(str(src), cv2.IMREAD_COLOR)
    if bgr is None:
        log(f"FATAL: could not decode image: {src}")
        sys.exit(1)

    h, w = bgr.shape[:2]
    log(f"image {w}x{h} -- {src.name}")

    before = bgr
    graded = bgr

    # Stage 0: input transform (Log->Rec709) FIRST, so correction develops a Rec709 signal.
    if input_lut is not None:
        graded = stylize.apply_look_image(graded, str(input_lut))
        log(f"input transform (Stage 0): {Path(input_lut).name}")

    if do_correct:
        # Measure the post-input-transform frame so the develop refines a Rec709 signal.
        params = correct.compute_correction(graded, strength=strength, skin_solve=skin_solve)
        graded = correct.apply_correction_image(graded, params)
        wb = params.get("wb_gains")
        log(
            "developed: wb_gains="
            f"{[round(float(g), 3) for g in wb] if wb else None} "
            f"exposure={params.get('exposure')} black={params.get('black')} "
            f"contrast={params.get('contrast')}"
        )
        _log_skin(params.get("skin"))
    else:
        log("correction skipped (--no-correct)")

    # --validate: read scopes on the DEVELOPED frame (post-correction, pre-creative-look) -- the
    # domain the demonstrated targets are defined in. Advisory; captured before the look is applied.
    validate_result: Optional[dict] = None
    if validate:
        validate_result = _validate_frame(graded)
        _log_validate(validate_result)

    if look_name:
        cube = _resolve_look(look_name)
        graded = stylize.apply_look_stack_image(graded, cube, opacity=look_opacity, stack_name=look_name)
        stk = stylize.look_stack(look_name)
        log(f"look applied: {look_name}  ({Path(cube).name}) @ opacity {look_opacity:.2f}"
            + (f"  + optical stack {list(stk)}" if stk else ""))

    if height:
        before = _resize_h(before, int(height))
        graded = _resize_h(graded, int(height))
    before_path = out_dir / f"{src.stem}_before.png"
    after_path = out_dir / f"{src.stem}_after.png"
    cv2.imwrite(str(before_path), before)
    cv2.imwrite(str(after_path), graded)
    written = [before_path, after_path]

    if validate and validate_result is not None:
        payload = {
            "input": src.name,
            "mode": "image",
            "validated_domain": (
                "developed (post-correction, pre-look)" if do_correct else "source (no correction)"
            ),
            "look": look_name,
            "generated": datetime.now().isoformat(timespec="seconds"),
            "results": [{"shot": None, **validate_result}],
        }
        written.append(_write_validate_sidecar(out_dir, src.stem, payload))
    return written


# --------------------------------------------------------------------------- #
# VIDEO route -- constant-per-shot correction (the load-bearing anti-flicker rule)
# --------------------------------------------------------------------------- #
def process_video(
    src: Path,
    out_dir: Path,
    look_name: Optional[str],
    do_correct: bool,
    deflicker: bool,
    keep_temp: bool,
    match_shots: bool = False,
    match_alpha: float = 0.8,
    height: Optional[int] = None,
    input_lut: Optional[Path] = None,
    look_opacity: float = 0.7,
    hdr_tonemap: Optional[str] = "auto",
    hwaccel: Optional[str] = "auto",
    strength: float = 1.0,
    skin_solve: bool = True,
    validate: bool = False,
) -> list[Path]:
    """Segment into shots; derive ONE constant correction per shot; apply + concat to out/.

    When ``match_shots`` is True and there is more than one shot, Stage 2 (inter-shot
    continuity matching, colorkit.match) is wired in: a HERO shot is chosen and every other
    shot gets a CONSTANT Reinhard LAB transfer toward the hero, baked into a tiny per-shot
    ``.cube`` LUT and slotted into the filtergraph AFTER correction and BEFORE the look
    (correct -> match -> stylize). Constant-per-shot => still flicker-free. ``match_alpha``
    (0..1) dials the transfer strength.
    """
    cv2 = _import_cv2()

    # --- Stage -1 (HDR -> SDR tonemap): detect HLG/PQ and build the tonemap filtergraph. ------ #
    # HDR footage must be tone-mapped to Rec.709 SDR BEFORE the input transform / develop, else
    # decoding HDR code values as SDR yields the washed/lifted-black look. The tonemap is the FIRST
    # per-shot filter and is applied to the rep frame too (so the develop measures the SDR signal).
    tonemap_vf: Optional[str] = None
    tonemap_engine: Optional[str] = None
    tonemap_dev_args: list[str] = []
    meta = hdr.probe_color(src)
    if hdr.is_hdr(meta):
        # An I-Log->Rec709 input LUT is meaningless on an HDR (Rec.2020 HLG/PQ) signal, whether or
        # not we tonemap: applying it would map Log code values that aren't there. Drop it for ANY
        # HDR source (covers a filename that auto-matched the I-Log regex but is actually HDR), so a
        # disabled tonemap (--hdr-tonemap none) never leaves a Log transform on HDR pixels.
        if input_lut is not None:
            log(f"  (skipping input LUT {Path(input_lut).name}: source is HDR, not I-Log Rec.709)")
            input_lut = None
        spec = hdr.resolve_tonemap_spec(hdr_tonemap)
        if spec is None:
            log(f"HDR source ({hdr.describe(meta)}) detected but --hdr-tonemap=none -- "
                "grading the HDR signal as SDR (expect a washed look)")
        else:
            tonemap_engine, op = spec
            tonemap_vf = hdr.tonemap_filter(meta, engine=tonemap_engine, operator=op)
            tonemap_dev_args = hdr.device_args(tonemap_engine)
            log(f"Stage -1 HDR tonemap: {hdr.describe(meta)} -> Rec.709 SDR "
                f"(engine={tonemap_engine}, op={op if tonemap_engine=='zscale' else 'bt2390'})")

    # --- Hardware-accelerated decode (8K throughput): resolve once, validated on the real file. -- #
    hw = accel.resolve_hwaccel(hwaccel, src, log=log)
    decode_pre_args = tonemap_dev_args + accel.hwaccel_decode_args(hw)

    shots = segment.detect_shots(str(src))
    log(f"segmented into {len(shots)} shot(s)")

    cube = _resolve_look(look_name) if look_name else None
    if cube:
        log(f"look (uniform across all shots): {look_name}  ({Path(cube).name})")

    work_dir = Path(tempfile.mkdtemp(prefix="colorkit_", dir=str(out_dir)))
    shot_files: list[Path] = []
    rep_dir = work_dir / "rep"
    rep_dir.mkdir(parents=True, exist_ok=True)
    lut_dir = work_dir / "lut"
    lut_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Stage the look cube into lut_dir so the per-shot ffmpeg (run with cwd=lut_dir) can
        # reference EVERY cube (look + per-shot match) by BARE FILENAME. ffmpeg's lut3d filtergraph
        # parser rejects Windows absolute paths (drive colon + spaces) no matter the escaping, so
        # running ffmpeg from the cube directory sidesteps it entirely.
        # Stage the look cube into lut_dir; GUARD the copy so a OneDrive file lock can't sink the
        # whole render before any shot is processed, and skip a needless self-copy.
        look_cube_in_lut: Optional[Path] = None
        if cube:
            try:
                if look_opacity < 1.0:
                    # Bake an opacity-reduced variant (identity->look lerp) so the look runs UNDER
                    # the grade at look_opacity -- a tasteful look, not a 100% one-tap filter.
                    staged = lut_dir / f"{Path(cube).stem}_op{int(round(look_opacity*100)):03d}.cube"
                    stylize.bake_look_at_opacity(str(cube), look_opacity, str(staged))
                    log(f"look @ opacity {look_opacity:.2f} (baked {staged.name})")
                else:
                    staged = lut_dir / Path(cube).name
                    if Path(cube).resolve() != staged.resolve():
                        shutil.copyfile(cube, staged)
            except OSError as exc:
                log(f"FATAL: could not stage look cube into {lut_dir} ({exc})")
                sys.exit(1)
            look_cube_in_lut = staged

        # Stage the Stage-0 input transform (Log->Rec709) cube the same way (bare filename, cwd).
        input_cube_in_lut: Optional[Path] = None
        if input_lut is not None:
            staged_in = lut_dir / Path(input_lut).name
            try:
                if Path(input_lut).resolve() != staged_in.resolve():
                    shutil.copyfile(input_lut, staged_in)
                input_cube_in_lut = staged_in
                log(f"input transform (Stage 0): {Path(input_lut).name}")
            except OSError as exc:
                log(f"WARNING: could not stage input LUT ({exc}); skipping input transform")
                input_cube_in_lut = None

        # --- optical look-STACK (Stage 3b): halation/grain/vignette in the per-shot graph -------- #
        # The look's COLOR (its .cube) is applied in the per-shot vf below; its OPTICAL character
        # (halation/grain/vignette) layers AFTER the delivery scale, constant for every frame (so it
        # is flicker-free) and identical across shots. Halation runs as an in-graph linear-light
        # screen; grain/vignette overlay a pre-baked seeded plate / elliptical mask -- baked ONCE at
        # the delivery resolution and reused for every shot (a STATIC plate, never ffmpeg's temporal
        # `noise`). When the look has no stack (or there is no look) this is empty and the render uses
        # the plain `-vf` path below -- byte-identical to the pre-stack behaviour.
        optical_plan = stylize.optical_stack_plan(look_name, look_opacity) if look_name else []
        optical_inputs: list[str] = []   # extra ffmpeg looped-plate -i args for the filter_complex
        grain_label: Optional[str] = None
        vig_label: Optional[str] = None
        opt_sigma = 0.0
        if optical_plan:
            ow, oh = _probe_output_dims(src, height)
            opt_sigma = max(1.0, 0.012 * oh)  # halation blur radius in OUTPUT px (matches the still)
            eff = dict(optical_plan)
            next_in = 1  # input 0 is the source; looped plates follow
            if "grain" in eff:
                gp = lut_dir / "_grain_plate.png"
                stylize.bake_grain_plate(str(gp), ow, oh, **eff["grain"])
                optical_inputs += ["-loop", "1", "-i", str(gp)]
                grain_label = f"{next_in}:v"
                next_in += 1
            if "vignette" in eff:
                vm = lut_dir / "_vignette_mask.png"
                stylize.bake_vignette_mask(str(vm), ow, oh, **eff["vignette"])
                optical_inputs += ["-loop", "1", "-i", str(vm)]
                vig_label = f"{next_in}:v"
                next_in += 1
            log(f"optical stack: {[e for e, _ in optical_plan]} @ {ow}x{oh}"
                + (f" (halation sigma {opt_sigma:.1f})" if "halation" in eff else ""))

        def _optical_chain(src_label: str):
            """Build the halation->grain->vignette filter_complex fragments off ``src_label``.

            Returns ``(fragment_chain_strings, final_output_label)``. The fragments are constant
            across shots; only the upstream colour segment (which feeds ``src_label``) differs.
            """
            frags: list[str] = []
            cur = src_label
            for i, (e_name, e_params) in enumerate(optical_plan):
                out_lbl = f"opt{i}"
                if e_name == "halation":
                    frags.append(stylize.ffmpeg_halation_segment(
                        cur, out_lbl, strength=e_params["strength"], sigma=opt_sigma))
                elif e_name == "grain":
                    frags.append(stylize.ffmpeg_grain_segment(cur, grain_label, out_lbl))
                elif e_name == "vignette":
                    frags.append(stylize.ffmpeg_vignette_segment(cur, vig_label, out_lbl))
                cur = out_lbl
            return frags, cur

        # --- PASS 1: derive ONE correction per shot from its representative frame. -------- #
        # We hold each shot's correction params AND its corrected representative frame so
        # Stage 2 (match) can compute a constant LAB transfer against a hero shot. The
        # corrected rep frame is the right reference domain because matching happens AFTER
        # correction in the canonical correct -> match -> stylize order.
        plan: list[dict] = []  # per-shot: {shot, idx, start, end, dur, params, corrected_rep}
        for shot in shots:
            idx = int(shot["index"])
            start = float(shot["start"])
            end = float(shot["end"])
            dur = max(0.0, end - start)

            params: Optional[dict] = None
            corrected_rep = None
            develop_cube: Optional[str] = None
            shot_validate: Optional[dict] = None
            if do_correct:
                t = measure.representative_frame_time(shot, str(src))
                rep_png = rep_dir / f"shot{idx:03d}_rep.png"
                # Apply the SAME Stage -1 HDR tonemap (if any) during extraction so the develop is
                # measured on the SDR Rec.709 signal the per-shot render will produce; reuse the
                # validated hwaccel/device decode args for the (8K) rep grab too. GUARD it like the
                # PASS-2 render: extract_frame RAISES on ffmpeg failure, and the hwaccel was only
                # validated on a bare decode (no filtergraph) -- so if the hwaccel+tonemap grab
                # fails, retry in software (keep the tonemap device args), then degrade to identity.
                # Never let a rep-frame failure crash the whole run.
                rep_bgr = None
                attempts = [decode_pre_args] + ([list(tonemap_dev_args)] if hw else [])
                for ai, pre in enumerate(attempts):
                    try:
                        io_utils.extract_frame(str(src), t, str(rep_png),
                                               vf=tonemap_vf, pre_input_args=pre or None)
                        rep_bgr = cv2.imread(str(rep_png), cv2.IMREAD_COLOR)
                    except Exception as exc:
                        where = f"hwaccel {hw}" if (ai == 0 and hw) else "software"
                        log(f"  shot #{idx}: rep-frame grab failed ({where}: {exc})")
                        rep_bgr = None
                    if rep_bgr is not None:
                        break
                if rep_bgr is None:
                    log(f"  shot #{idx}: rep-frame unavailable (t={t:.2f}s) -- correcting with identity")
                    params = None
                else:
                    # Apply the Stage-0 input transform to the rep frame FIRST so the develop is
                    # measured on the developed Rec709 signal (matches the filtergraph order below).
                    # (input_lut is forced None when an HDR tonemap is active -- never stack both.)
                    if input_lut is not None:
                        rep_bgr = stylize.apply_look_image(rep_bgr, str(input_lut))
                    params = correct.compute_correction(rep_bgr, strength=strength,
                                                        skin_solve=skin_solve)
                    _log_skin(params.get("skin"), prefix=f"  shot #{idx}: ")
                    # The corrected rep frame is the post-develop domain Stage 2 matches in.
                    corrected_rep = correct.apply_correction_image(rep_bgr, params)
                    # --validate: score this shot's DEVELOPED rep frame against the scope targets
                    # (advisory; the per-shot corrected rep is exactly the developed domain).
                    if validate:
                        shot_validate = _validate_frame(corrected_rep)
                        _log_validate(shot_validate, prefix=f"  shot #{idx}: ")
                    # Bake the develop into a constant per-shot .cube (the VIDEO apply -- lets us run
                    # linear-light filmic math ffmpeg eq cannot, while staying constant per shot).
                    dcube = lut_dir / f"shot{idx:03d}_develop.cube"
                    correct.bake_develop_cube(params, str(dcube))
                    develop_cube = str(dcube)

            plan.append({
                "shot": shot, "idx": idx, "start": start, "end": end, "dur": dur,
                "params": params, "corrected_rep": corrected_rep, "develop_cube": develop_cube,
                "validate": shot_validate,
            })

        # --- Stage 2 (MATCH): pick a hero shot, derive a constant LAB transfer per shot. -- #
        # Gated behind --match. With <2 shots there is nothing to reconcile, so it is a no-op.
        match_cubes: dict[int, str] = {}  # idx -> baked per-shot .cube path
        usable = [p for p in plan if p["corrected_rep"] is not None]
        if match_shots and len(usable) >= 2:
            hero = _pick_hero(usable)
            hero_rep = hero["corrected_rep"]
            log(f"shot-match (Stage 2): hero=shot #{hero['idx']}, alpha={match_alpha:.2f}")
            for p in usable:
                if p["idx"] == hero["idx"]:
                    continue  # the hero matches itself -> identity, skip
                try:
                    mp = match.compute_match_params(p["corrected_rep"], hero_rep)
                    cube_path = lut_dir / f"shot{p['idx']:03d}_match.cube"
                    _bake_match_cube(mp, match_alpha, str(cube_path))
                    match_cubes[p["idx"]] = str(cube_path)
                except Exception as exc:  # never let a match failure sink the render
                    log(f"  shot #{p['idx']}: match skipped ({exc})")
        elif match_shots:
            log("shot-match (Stage 2): skipped -- need >=2 corrected shots")

        # --- PASS 2: build the CONSTANT filtergraph per shot and render. ----------------- #
        for p in plan:
            idx, start, end, dur = p["idx"], p["start"], p["end"], p["dur"]
            params = p["params"]

            # Order: HDR tonemap (Stage -1) -> input transform (Stage 0) -> develop (Stage 1)
            # -> shot-match LUT (Stage 2) -> creative look (Stage 3) -> delivery scale. The lut3d
            # stages are constant per-shot (flicker-free); the tonemap is a fixed transform too.
            chain: list[str] = []
            if tonemap_vf:
                chain.append(tonemap_vf)
            if input_cube_in_lut is not None:
                chain.append(stylize.ffmpeg_lut_filter(str(input_cube_in_lut), expect_dir=str(lut_dir)))
            dcube = p.get("develop_cube")
            if dcube:
                chain.append(stylize.ffmpeg_lut_filter(dcube, expect_dir=str(lut_dir)))
            mcube = match_cubes.get(idx)
            if mcube:
                chain.append(stylize.ffmpeg_lut_filter(mcube, expect_dir=str(lut_dir)))
            if look_cube_in_lut:
                chain.append(stylize.ffmpeg_lut_filter(str(look_cube_in_lut), expect_dir=str(lut_dir)))
            # Delivery downscale LAST (after the grade) -- essential for 8K source so libx264 encodes
            # a sane resolution. -2 keeps width even and preserves aspect.
            if height:
                chain.append(f"scale=-2:{int(height)}")
            vf = ",".join(chain) if chain else "null"

            # When the look carries an optical stack, the colour chain becomes the head of a
            # filter_complex ([0:v]<colour vf>[m0]) and the halation/grain/vignette fragments layer
            # on top (off [m0]); otherwise the simple `-vf` path is used unchanged (byte-identical).
            shot_filter_complex: Optional[str] = None
            final_lbl: Optional[str] = None
            if optical_plan:
                opt_frags, final_lbl = _optical_chain("m0")
                shot_filter_complex = ";".join([f"[0:v]{vf}[m0]"] + opt_frags)

            shot_out = work_dir / f"shot{idx:03d}.mp4"

            # -ss/-to slice this shot; the SAME filtergraph is applied to every frame of the shot.
            # ``pre`` carries the decode-side args (Vulkan device for placebo + the validated
            # -hwaccel). NOTE: io_utils.run_ffmpeg prepends the "ffmpeg" binary itself, so the cmd
            # list starts at the first ARGUMENT (a leading "ffmpeg" would run `ffmpeg ffmpeg ...`).
            def _encode(pre: list) -> object:
                cmd = ["-y", "-hide_banner", "-loglevel", "error"]
                cmd += [str(a) for a in pre]
                cmd += ["-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(src)]
                if shot_filter_complex:
                    # Looped plate inputs (grain/vignette) follow the source; map the graph's final
                    # video + the source audio. The grain/vignette blends carry framesync shortest=1
                    # so the (infinite) looped plates are bounded to the source -- no output-level
                    # -shortest (which can race the muxer into "no packets" on some sources).
                    cmd += [str(a) for a in optical_inputs]
                    cmd += ["-filter_complex", shot_filter_complex,
                            "-map", f"[{final_lbl}]", "-map", "0:a?"]
                else:
                    cmd += ["-vf", vf]
                cmd += [
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", str(shot_out),
                ]
                # Run from lut_dir so the lut3d filters (bare filenames) resolve; input/output paths
                # in cmd are absolute, so cwd does not affect them.
                return io_utils.run_ffmpeg(cmd, cwd=str(lut_dir))

            log(f"  shot #{idx} [{start:.2f}-{end:.2f}s, {dur:.2f}s]"
                f"{' hw=' + hw if hw else ''}"
                f"{' +optical' if optical_plan else ''} vf={vf}")
            r = _encode(decode_pre_args)
            if getattr(r, "returncode", 1) != 0 and hw:
                # Hardware decode failed for this shot -> retry once in software (keep any tonemap
                # device args, e.g. the Vulkan device libplacebo needs regardless of decode path).
                tail = (r.stderr or "").strip().splitlines()
                log(f"  shot #{idx}: hwaccel '{hw}' failed ({tail[-1] if tail else 'error'}); "
                    "retrying in software")
                r = _encode(list(tonemap_dev_args))
            if getattr(r, "returncode", 1) != 0:
                tail = (r.stderr or "").strip().splitlines()
                log(f"  shot #{idx} FAILED: {tail[-1] if tail else 'unknown ffmpeg error'}")
                continue
            shot_files.append(shot_out)

        if not shot_files:
            log("FATAL: no shots rendered -- nothing to concat")
            sys.exit(1)

        # --- concat all graded shots into one master (stream copy where possible) -------- #
        graded_path = out_dir / f"{src.stem}_graded.mp4"
        concat_path = _concat_shots(shot_files, graded_path)

        # --- optional temporal safety net (Stage 3b) ------------------------------------- #
        if deflicker:
            concat_path = _apply_deflicker(concat_path, out_dir, src.stem)

        written = [concat_path]

        # --- --validate sidecar: per-shot scope verdicts on the developed rep frames ------ #
        if validate:
            results: list[dict] = []
            for p in plan:
                vr = p.get("validate")
                if vr is None:
                    results.append({
                        "shot": p["idx"], "start": round(p["start"], 3), "end": round(p["end"], 3),
                        "validated": False,
                        "note": "no corrected rep frame (correction off or rep-frame grab failed)",
                    })
                else:
                    results.append({
                        "shot": p["idx"], "start": round(p["start"], 3), "end": round(p["end"], 3),
                        **vr,
                    })
            scored = [p.get("validate") for p in plan if p.get("validate")]
            payload = {
                "input": src.name,
                "mode": "video",
                "validated_domain": "developed (post-correction, pre-look)",
                "look": look_name,
                "generated": datetime.now().isoformat(timespec="seconds"),
                "n_shots": len(plan),
                "n_validated": len(scored),
                "min_pass": min((v["n_pass"] for v in scored), default=None),
                "results": results,
            }
            written.append(_write_validate_sidecar(out_dir, src.stem, payload))

        return written
    finally:
        if not keep_temp:
            _rmtree(work_dir)
        else:
            log(f"kept intermediates in {work_dir}")


def _concat_shots(shot_files: list[Path], dst: Path) -> Path:
    """Concat per-shot mp4s into one file via the ffmpeg concat demuxer (no re-encode)."""
    list_file = dst.parent / f"{dst.stem}.concat.txt"
    # ffmpeg concat list: forward slashes are safest cross-platform; single-quote the paths.
    lines = [f"file '{p.as_posix()}'" for p in shot_files]
    list_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # io_utils.run_ffmpeg prepends the "ffmpeg" binary -> cmd starts at the first ARGUMENT.
    cmd = [
        "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c", "copy", "-movflags", "+faststart", str(dst),
    ]
    log(f"concat {len(shot_files)} shot(s) -> {dst.name}")
    r = io_utils.run_ffmpeg(cmd)
    if getattr(r, "returncode", 1) != 0:
        # Fallback: timestamps may not splice cleanly under stream-copy -> re-encode.
        log("  stream-copy concat failed; re-encoding concat")
        cmd[cmd.index("copy") - 1:] = [
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(dst),
        ]
        r = io_utils.run_ffmpeg(cmd)
        if getattr(r, "returncode", 1) != 0:
            tail = (r.stderr or "").strip().splitlines()
            log(f"FATAL concat: {tail[-1] if tail else 'unknown ffmpeg error'}")
            sys.exit(1)
    try:
        list_file.unlink()
    except OSError:
        pass
    return dst


def _apply_deflicker(src_video: Path, out_dir: Path, stem: str) -> Path:
    """Optional Stage-3b backstop: residual luminance pumping smoothing on the final master."""
    dst = out_dir / f"{stem}_graded_deflicker.mp4"
    vf = "deflicker=mode=pm:size=5,normalize=smoothing=10"
    # io_utils.run_ffmpeg prepends the "ffmpeg" binary -> cmd starts at the first ARGUMENT.
    cmd = [
        "-y", "-hide_banner", "-loglevel", "error", "-i", str(src_video),
        "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(dst),
    ]
    log("temporal backstop: deflicker+normalize")
    r = io_utils.run_ffmpeg(cmd)
    if getattr(r, "returncode", 1) != 0:
        tail = (r.stderr or "").strip().splitlines()
        log(f"  deflicker FAILED ({tail[-1] if tail else 'unknown'}); keeping un-deflickered master")
        return src_video
    return dst


# --------------------------------------------------------------------------- #
# Stage 2 (MATCH) helpers                                                      #
# --------------------------------------------------------------------------- #
def _pick_hero(usable: list[dict]) -> dict:
    """Choose the HERO shot to match every other shot toward (Stage 2 reference).

    Heuristic: the shot whose corrected representative frame has the MEDIAN mean luma -- the
    most 'typical'-exposure shot, so matching pulls outliers toward a sensible centre rather
    than chasing the brightest or darkest cut. Deterministic and dependency-light (uses the
    already-decoded corrected rep frames). ``usable`` is the subset of the plan that actually
    has a ``corrected_rep`` (len >= 2 is guaranteed by the caller).
    """
    import numpy as np

    scored: list[tuple[float, dict]] = []
    for p in usable:
        rep = p["corrected_rep"]
        # BT.601 luma mean on the corrected rep frame (BGR uint8) -> a single exposure scalar.
        y = (0.114 * rep[..., 0] + 0.587 * rep[..., 1] + 0.299 * rep[..., 2])
        scored.append((float(np.mean(y)), p))
    scored.sort(key=lambda yp: yp[0])
    # Lower-median entry: a real shot, robust to one very bright / very dark outlier.
    return scored[(len(scored) - 1) // 2][1]


def _bake_match_cube(match_params: dict, alpha: float, dst_cube: str, size: int = 33) -> str:
    """Bake a constant Reinhard LAB match (from match.compute_match_params) into a 3D .cube LUT.

    The LUT encodes EXACTLY ``match.apply_match_params(., match_params, alpha)``: we sample a
    ``size**3`` RGB grid, run the same constant LAB transfer over it, and write the result as an
    Iridas ``.cube`` with the RED channel varying fastest (the Iridas convention that
    ``colorkit.luts.write_cube`` uses and that ffmpeg ``lut3d`` expects). Because the transform is
    one fixed set of numbers, baking it to a LUT and applying it via ffmpeg ``lut3d`` is constant
    for every frame of the shot -> structurally flicker-free, matching the still-path math.

    Returns the destination path.
    """
    import numpy as np

    n = int(size)
    # Build the grid as an (n*n*n, 3) RGB-0..1 array with RED fastest, then GREEN, then BLUE.
    axis = np.linspace(0.0, 1.0, n, dtype=np.float32)
    bb, gg, rr = np.meshgrid(axis, axis, axis, indexing="ij")  # bb slowest, rr fastest
    rgb = np.stack([rr.ravel(), gg.ravel(), bb.ravel()], axis=1)  # (N,3) R,G,B

    # match.apply_match_params works in BGR uint8 image space -> feed it the grid as an image.
    bgr = rgb[:, ::-1].reshape(1, -1, 3)  # (1, N, 3) BGR, 0..1 float
    bgr_u8 = np.clip(bgr * 255.0 + 0.5, 0, 255).astype(np.uint8)
    out_bgr_u8 = match.apply_match_params(bgr_u8, match_params, alpha=alpha)
    out_rgb = (out_bgr_u8.reshape(-1, 3)[:, ::-1].astype(np.float32)) / 255.0

    dst = Path(dst_cube)
    dst.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Generated by color.py Stage 2 (shot match) -- constant Reinhard LAB transfer.",
        f"LUT_3D_SIZE {n}",
    ]
    for r, g, b in out_rgb:
        lines.append(f"{r:.6f} {g:.6f} {b:.6f}")
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(dst)


# --------------------------------------------------------------------------- #
# helpers                                                                      #
# --------------------------------------------------------------------------- #
def _resolve_look(look_name: str) -> str:
    """Map a --look NAME to its absolute .cube path via colorkit.stylize.LOOKS."""
    looks = stylize.LOOKS
    if look_name not in looks:
        available = ", ".join(sorted(stylize.list_looks())) or "(none built yet)"
        log(f"FATAL: unknown look '{look_name}'. Available: {available}")
        sys.exit(1)
    cube = Path(looks[look_name])
    if not cube.exists():
        log(f"FATAL: look '{look_name}' maps to a missing .cube: {cube}\n"
            f"       Build the LUTs first: python -m colorkit.luts --all")
        sys.exit(1)
    return str(cube)


def _auto_pick_look(src: Path, ext: str, input_lut: Optional[Path],
                    hdr_tonemap: Optional[str] = "auto") -> Optional[dict]:
    """``--look auto``: measure ONE representative frame and let colorkit.decide pick a look.

    For video, the frame is grabbed ~40% into the clip (avoids intro/outro) and tonemapped using the
    SAME ``hdr_tonemap`` spec the render will use -- so the look is *chosen* on the identical SDR
    signal it will be *graded onto* (measurement/render parity; honoring ``--hdr-tonemap none`` means
    measuring the un-tonemapped signal too). For a Log still/video, the input LUT is applied first
    (HDR sources never get the I-Log LUT). Returns a colorkit.decide LookChoice dict, or None.
    """
    cv2 = _import_cv2()
    from . import decide

    bgr = None
    is_hdr_src = False
    if ext in IMAGE_EXTS:
        bgr = cv2.imread(str(src), cv2.IMREAD_COLOR)
        if bgr is not None and input_lut is not None:
            bgr = stylize.apply_look_image(bgr, str(input_lut))
    else:
        meta = hdr.probe_color(src)
        is_hdr_src = hdr.is_hdr(meta)
        vf = None
        if is_hdr_src:
            # Match process_video exactly: honor the user's --hdr-tonemap (None disables tonemap).
            spec = hdr.resolve_tonemap_spec(hdr_tonemap)
            if spec:
                vf = hdr.tonemap_filter(meta, engine=spec[0], operator=spec[1])
        dur = segment._probe_duration(str(src))  # package-internal duration probe
        t = max(0.0, float(dur) * 0.4)
        tmp = io_utils.ensure_out_dir() / f".{src.stem}_autolook.png"
        try:
            io_utils.extract_frame(str(src), t, str(tmp), vf=vf)
            bgr = cv2.imread(str(tmp), cv2.IMREAD_COLOR)
        except Exception:
            bgr = None
        finally:
            try:
                tmp.unlink()
            except OSError:
                pass
        # Log input transform only when we did NOT already tonemap to Rec.709 (never stack both).
        if bgr is not None and input_lut is not None and not is_hdr_src:
            bgr = stylize.apply_look_image(bgr, str(input_lut))

    if bgr is None:
        return None
    stats = measure.scene_stats(bgr)
    return decide.suggest_look(stats)


def _resize_h(img, height: int):
    """Downscale a BGR image to ``height`` px tall (preserve aspect, even width); never upscales."""
    import cv2
    h, w = img.shape[:2]
    if height <= 0 or h <= height:
        return img
    nw = int(round(w * height / h))
    nw -= nw % 2  # keep width even (encoder-friendly, consistent with the video -2 scale)
    return cv2.resize(img, (max(2, nw), height), interpolation=cv2.INTER_AREA)


def _probe_output_dims(src: Path, height: Optional[int]) -> tuple:
    """Best-effort (width, height) of the delivery (post-scale) frame, for sizing optical plates.

    Reads the source's DISPLAY dims (coded dims + rotation, since ffmpeg decodes to display
    orientation) via ffprobe, then applies the same ``scale=-2:height`` delivery math the render
    uses. Falls back to 1080x1920 if probing fails -- the optical segments ``scale2ref`` the plate to
    the real frame anyway, so a small mismatch self-corrects (this only needs to be close enough that
    the grain size is right). Never raises.
    """
    import json as _json
    w = h = 0
    rot = 0
    try:
        r = io_utils.run_ffprobe([
            "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height:stream_side_data=rotation:stream_tags=rotate",
            "-of", "json", str(src),
        ])
        s = ((_json.loads(r.stdout or "{}") or {}).get("streams") or [{}])[0]
        w = int(s.get("width") or 0)
        h = int(s.get("height") or 0)
        for sd in (s.get("side_data_list") or []):  # modern: Display Matrix rotation
            if sd.get("rotation") is not None:
                rot = int(round(float(sd["rotation"])))
                break
        else:  # legacy: stream tag rotate
            tr = (s.get("tags") or {}).get("rotate")
            if tr is not None:
                rot = int(round(float(tr)))
    except Exception:
        pass
    if w <= 0 or h <= 0:
        w, h = 1080, 1920
    if abs(rot) % 180 == 90:  # ffmpeg decodes to display orientation -> swap coded dims
        w, h = h, w
    if height and h > int(height):
        nh = int(height)
        nw = int(round(w * nh / h))
        nw -= nw % 2
        w, h = max(2, nw), nh
    return int(w), int(h)


def _rmtree(path: Path) -> None:
    """Best-effort recursive delete of a temp work dir (OneDrive locks files sometimes)."""
    import shutil
    try:
        shutil.rmtree(path, ignore_errors=True)
    except OSError:
        pass


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="colorkit",
        description="Headless agentic color-correction + stylized grading (images + video). "
                    "Outputs ONLY to out/. Never publishes.",
    )
    p.add_argument("input", help="input image or video file")
    p.add_argument("--look", default=None, metavar="NAME",
                   help="stylized look from colorkit.stylize.LOOKS (default: none = correct-only). "
                        "Pass 'auto' to let the decision layer (colorkit.decide) pick a look from a "
                        "representative frame's scene signals (skin/foliage/warmth/contrast).")
    p.add_argument("--no-correct", dest="correct", action="store_false", default=True,
                   help="skip the auto color-correction stage (look-only)")
    p.add_argument("--out", default=None, metavar="DIR",
                   help="output directory (default: auto-clip/out)")
    p.add_argument("--match", dest="match", action="store_true", default=False,
                   help="VIDEO only: Stage 2 inter-shot continuity matching toward a hero shot "
                        "(Reinhard LAB transfer baked as a constant per-shot LUT). No-op single-shot.")
    p.add_argument("--match-alpha", dest="match_alpha", type=float, default=0.8, metavar="A",
                   help="strength of the shot-match transfer in [0,1] (default 0.8; lower = gentler)")
    p.add_argument("--deflicker", action="store_true",
                   help="optional ffmpeg deflicker/normalize backstop on the final video")
    p.add_argument("--height", type=int, default=None, metavar="N",
                   help="downscale output to N px tall (preserve aspect); essential for 8K source -> "
                        "fast IG-ready delivery (e.g. --height 1920). Default: keep source resolution.")
    p.add_argument("--input-lut", dest="input_lut", default="auto", metavar="SPEC",
                   help="Stage-0 input transform (Log->Rec709) applied FIRST. 'auto' (default) "
                        "auto-detects I-Log by filename and uses the bundled Insta360 Rec709 BT1886 "
                        "s65 LUT; 'none' disables; 'ilog'/'ilog_s33' force it; or pass a .cube path.")
    p.add_argument("--look-opacity", dest="look_opacity", type=float, default=0.7, metavar="O",
                   help="apply the creative --look at O in [0,1] opacity (default 0.7). Pros run a "
                        "look UNDER the grade at ~0.5-0.8, never 100%%, so it reads as a tasteful look "
                        "not a one-tap filter. 1.0 = full strength.")
    p.add_argument("--hdr-tonemap", dest="hdr_tonemap", default="auto", metavar="SPEC",
                   help="VIDEO only: HDR (HLG/PQ) -> Rec.709 SDR tonemap applied FIRST when an HDR "
                        "source is detected (Stage -1). 'auto' (default)=zscale+hable (CPU, "
                        "deterministic); 'mobius'/'reinhard'=other zscale operators; "
                        "'placebo'=libplacebo BT.2390 (Vulkan GPU, richest); 'none' disables "
                        "(grades the HDR signal as SDR = washed). No-op on SDR sources.")
    p.add_argument("--hwaccel", dest="hwaccel", default="auto", metavar="MODE",
                   help="VIDEO only: hardware-accelerated DECODE for throughput (esp. 8K; ~4x on "
                        "NVDEC). 'auto' (default) picks a working accelerator validated on the source "
                        "(cuda/qsv/d3d11va/...), with a per-shot software fallback; name one "
                        "explicitly, or 'none' to force software decode.")
    p.add_argument("--strength", dest="strength", type=float, default=1.0, metavar="S",
                   help="overall develop intensity in [0,1] (default 1.0 = the calibrated auto "
                        "develop). Lower = a gentler grade (scales WB, exposure, black point, contrast "
                        "and vibrance toward identity) for footage where the auto-develop reads too "
                        "strong. Independent of the automatic low-light guards, which always protect "
                        "dark/mixed-light scenes from over-lift/over-warm.")
    p.add_argument("--skin-solve", dest="skin_solve", default="auto",
                   choices=["auto", "off"], metavar="MODE",
                   help="G1 skin-tone-line solver (default 'auto'): when skin is a real part of a "
                        "frame and off the ~123 deg I-line, fold a small capped luma-preserving WB "
                        "tint into the develop so skin lands nearer the line, plus a two-band skin "
                        "exposure trim. Self-gating: a no-op on footage without enough skin (those "
                        "develops are byte-identical). 'off' disables it.")
    p.add_argument("--validate", action="store_true",
                   help="run colorkit.scopes self-validation on the DEVELOPED frame(s) (post-correction, "
                        "pre-look) and write a <stem>_validate.json sidecar + per-shot verdict log. "
                        "Advisory only -- asserts the demonstrated scope targets (black off-floor, white "
                        "in range, no clip, parade converged, skin on the ~123 deg I-line); it never "
                        "alters pixels or gates the render. Makes every grade falsifiable.")
    p.add_argument("--keep-temp", action="store_true",
                   help="keep per-shot intermediate files for debugging")
    return p


def main(argv: Optional[list[str]] = None) -> None:
    args = _build_parser().parse_args(argv)

    src = Path(args.input).expanduser().resolve()
    if not src.exists():
        log(f"FATAL: input not found: {src}")
        sys.exit(1)

    # Default output = canonical colorkit OUT_DIR (auto-clip/out); honor --out if given.
    if args.out:
        out_dir = Path(args.out).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = io_utils.ensure_out_dir()

    ext = src.suffix.lower()
    look_name: Optional[str] = args.look
    do_correct: bool = args.correct
    match_shots: bool = args.match
    match_alpha: float = max(0.0, min(1.0, float(args.match_alpha)))
    look_opacity: float = max(0.0, min(1.0, float(args.look_opacity)))
    strength: float = max(0.0, min(1.0, float(args.strength)))
    skin_solve: bool = (args.skin_solve != "off")
    input_lut: Optional[Path] = _detect_input_lut(src, args.input_lut)

    # --look auto -> the decision layer (colorkit.decide) picks a look from a representative frame.
    if (look_name or "").lower() == "auto":
        choice = _auto_pick_look(src, ext, input_lut, hdr_tonemap=args.hdr_tonemap)
        if choice:
            look_name = str(choice["look"])
            look_opacity = float(choice["opacity"])
            log(f"--look auto -> {look_name} @ opacity {look_opacity:.2f} "
                f"(confidence {float(choice['confidence']):.2f}): {choice['reason']}")
        else:
            log("--look auto: could not measure a representative frame -> correct-only")
            look_name = None

    if not do_correct and not look_name:
        log("FATAL: nothing to do -- you passed --no-correct with no --look. "
            "Give a --look or drop --no-correct.")
        sys.exit(1)

    if match_shots and not do_correct:
        # Stage 2 matches in the post-correction domain; with correction off there is no
        # corrected rep frame to derive a transfer from, so --match becomes a no-op.
        log("NOTE: --match needs correction on (it matches corrected shots); --no-correct "
            "disables it -- proceeding without inter-shot matching.")

    log(f"input: {src.name}  |  out: {out_dir}  |  "
        f"correct={'on' if do_correct else 'off'}  look={look_name or 'none'}  "
        f"match={'on' if match_shots else 'off'}  "
        f"input_lut={Path(input_lut).name if input_lut else 'none'}")

    if ext in IMAGE_EXTS:
        written = process_image(src, out_dir, look_name, do_correct, height=args.height,
                                input_lut=input_lut, look_opacity=look_opacity, strength=strength,
                                skin_solve=skin_solve, validate=args.validate)
    elif ext in VIDEO_EXTS:
        written = process_video(
            src, out_dir, look_name, do_correct, args.deflicker, args.keep_temp,
            match_shots=match_shots, match_alpha=match_alpha, height=args.height,
            input_lut=input_lut, look_opacity=look_opacity,
            hdr_tonemap=args.hdr_tonemap, hwaccel=args.hwaccel, strength=strength,
            skin_solve=skin_solve, validate=args.validate,
        )
    else:
        log(f"FATAL: unsupported extension '{ext}'. "
            f"Images: {sorted(IMAGE_EXTS)}  Videos: {sorted(VIDEO_EXTS)}")
        sys.exit(1)

    # --- manifest (review only -- NOTHING published, CLAUDE.md rule 1) ---------------- #
    log(f"DONE -- {len(written)} file(s) written to {out_dir}")
    log("MANIFEST (review only -- NOT published, per CLAUDE.md rule 1):")
    for f in written:
        try:
            size_kb = f.stat().st_size / 1024
        except OSError:
            size_kb = 0.0
        log(f"  {f.name}  ({size_kb:,.0f} KB)  {f}")


if __name__ == "__main__":
    main()
