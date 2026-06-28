# SPEC — Color Engine v2: tasteful grade, not a one-tap filter

**Date:** 2026-06-24 · **Status:** SPEC (drives the v2 rewrite of `auto-clip/colorkit/`).
**Source:** synthesized from the verified `pro-grade-craft-research` workflow (run `wf_7107b183-886`, 6 lanes +
adversarial verify). The final synthesis agent was interrupted, so this doc IS that synthesis, written from the
6 verified lane outputs (extracted to `~/v2_lanes.json`). Companion plan: `2026-06-23-agentic-color-pipeline.md`
(the v1 architecture). Status tracker: `auto-clip/COLOR-BUILD-STATUS.md`.

---

## 1. Diagnosis — exactly why v1 looks washed / "Instagram Edits app"

v1's pipeline is: gray-world WB → push **mean** luma to a fixed target (~0.46) → **linear** contrast expansion
→ apply a creative `.cube` that *also* adds contrast. Every primary source in the research names the same root
causes, and they compound:

1. **Look/contrast applied with no highlight protection → hard clipping.** A naive linear contrast stretch is an
   unbounded straight line: any value pushed above 1.0 hard-clips to flat white, below 0 crushes to black. That
   *is* the "overblown" look. Film/filmic curves never do this — they have a **shoulder** that rolls highlights
   off smoothly.
2. **Exposure anchored to the MEAN, not middle-grey.** A few bright pixels (a window, a lamp, a specular)
   drag the mean, so "push mean to 0.46" over-brightens the whole frame. Exposure must anchor the **median**
   (robust) of mid-tones to **middle grey ≈ 0.18 linear (~0.40–0.46 gamma-encoded / ~41 IRE)**.
3. **Contrast stacking.** Correction adds contrast (linear stretch) AND the creative LUT adds contrast again →
   double contrast crushes shadows and blows highlights. There must be **ONE** source of contrast.
4. **No true black point + milky blacks.** Without setting a real black point per channel, blacks sit grey/raised
   = washed. (But don't crush to 0 either — a tiny filmic toe lift to ~3–5 IRE reads as "real grade.")
5. **Wrong working domain.** Contrast/tone applied on gamma-encoded values, not in linear light, desaturates and
   washes. Tone-mapping must happen in **linear light**.
6. **Global saturation ignores skin.** A flat saturation multiplier clips already-saturated pixels and pushes
   skin off its natural hue. Pros use **vibrance** (protects saturated pixels + skin) and key the grade to the
   **skin-tone line**.
7. **Creative LUT run at 100%.** Pros dial a creative look to **60–80%** opacity; at 100% it dominates and reads
   as a filter.

**The fix in one sentence:** enforce the canonical order, set exposure by **median→middle-grey**, set a real
**per-channel black/white point**, replace the linear stretch with a **single filmic tone curve that has a toe and
a shoulder (no clip), computed in linear light**, key color to the **skin line** with **vibrance** discipline, and
apply the rebuilt creative looks at **reduced opacity on the balanced base**.

---

## 2. The corrected pipeline order (the spine of v2)

Canonical colorist order (Noam Kroll / Pomfort / Resolve workflow, confirmed load-bearing across 4 lanes):

| # | Stage | Does | Why it's here |
|---|-------|------|---------------|
| 0 | **Input transform** (log only) | Apply the camera's official Log→Rec709 LUT FIRST (Insta360 I-Log→Rec709 BT1886). | The camera-accurate "develop". Only de-log ONCE; never stack two output transforms. |
| 1 | **White balance** | Shades-of-Gray (Minkowski p≈6) channel gains, green-anchored, exclude clipped/near-black. | Neutralize the cast before anything tonal; gray-world fails when one color dominates. |
| 2 | **Exposure** | Multiply so **median** mid-tone luma → **0.18 linear**; set per-channel black point (0.5–1st pct → ~0.012–0.02) and white point (99–99.5th pct → ~0.90), in linear. | Robust exposure + neutral, non-milky blacks. Anchors every shot to the same place (also helps shot-match). |
| 3 | **Tone / contrast** | ONE filmic curve with a toe + shoulder, pivoted at 0.18, applied in **linear light**, then encode. | Protects highlights (no clip), gives "film" body. The *only* contrast in the chain. |
| 4 | **Secondaries / memory color** | Nudge skin onto the flesh line; gentle vibrance (protect skin/saturated). | Makes the grade read as *intentional*, not a flat tint. |
| 5 | **Shot match** (video, ≥2 shots) | Reinhard LAB transfer toward a hero shot (existing Stage 2). | Inter-shot continuity. Sits on the corrected base. |
| 6 | **Creative LOOK** | Rebuilt `.cube` look at **0.6–0.8 opacity**, on the balanced base, NO extra exposure/contrast. | The style. Reduced opacity = tasteful, not a filter. |
| 7 | **Output / delivery** | Encode to Rec.709 gamma; `--height` downscale LAST. | Output transform is always last. |

Stages 0–4 are the **"develop"** (per-shot constant correction). Stages 5–7 are unchanged in spirit from v1.

---

## 3. Tone mapping — the filmic curve (replaces the linear stretch)

**Work in linear light.** Decode the gamma-encoded frame to linear (sRGB EOTF or BT.1886 ≈ `v^2.4`), do
WB/exposure/tone in linear, then encode back (`lin^(1/2.4)` or sRGB OETF) as the *last* develop step.

### 3.1 Primary recommendation: **ACES filmic (Narkowicz fit)** for the default, **AgX** for highlight-heavy footage

**ACES Narkowicz fit** — cheapest credible shoulder, public domain, drop-in (verified, max error 0.0138 vs full
ACES RRT+ODT):

```
# x = linear RGB (per channel), pre-exposed so middle-grey already sits near 0.18
def aces_narkowicz(x):
    x = x * 0.6                      # pre-scale for the true-ACES match (input 1.0 -> ~0.8)
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    return clamp((x*(a*x + b)) / (x*(c*x + d) + e), 0.0, 1.0)
```
Note: the ACES fit slightly **over-saturates bright colors**. For neon/bright-highlight footage prefer AgX.

**AgX (Sobotka/Wrensch minimal)** — best hue/highlight stability for an *automated* grade; **desaturates as light
increases** (an inset matrix mixes channels toward grey BEFORE the per-channel sigmoid → smooth highlight rolloff,
no "Notorious 6" hue skew). Verified concrete params:
```
log2 EV range: min_ev = -12.47393, max_ev = 4.026069   # clamp linear to [2^min, 2^max], normalize 0..1 (≈16.5 stops)
pivot: 0.18 (middle grey)
inset  = [[0.8424,0.0784,0.0792],[0.0423,0.8785,0.0792],[0.0424,0.0784,0.8791]]  # mix toward grey
outset = inverse(inset) ≈ [[1.1969,-0.0980,-0.0990],[-0.0529,1.1519,-0.0990],[-0.0530,-0.0784,1.1511]]
sigmoid: 6th-order polynomial on the normalized log value (Wrensch), or a logistic S-curve toe+shoulder.
```
Pipeline: `linear → inset matrix → log2 encode over EV range → sigmoid → outset matrix → encode`.

### 3.2 Alternatives (parametric control if we want knobs)

- **Hable / Uncharted-2** (piecewise filmic): `A=0.15, B=0.50, C=0.10, D=0.20, E=0.02, F=0.30`, exposureBias=2.0,
  white point `W=11.2`. `f(x)=((x*(A*x+C*B)+D*E)/(x*(A*x+B)+D*F))-E/F`; output `= f(x*bias)/f(W)`. Raise `W` to
  protect more highlights.
- **Lottes** (4 colorist knobs): contrast `a=1.6`, shoulder `d=0.977`, `hdrMax=8.0`, `midIn=0.18`, `midOut=0.267`;
  solve `b,c` so mid-grey lands exactly. Lower `a`→softer toe; raise `d`→gentler shoulder.
- **Extended Reinhard with white point** (featherweight rolloff): `out = C*(1 + C/Cwhite²)/(1 + C)`, set
  `Cwhite` = 99.5th-percentile luminance. **Apply to luminance only**, scale RGB by `L_out/L_in` to preserve chroma.

### 3.3 Pivoted contrast (if any extra contrast is applied at all — keep it minimal)

The filmic curve already provides contrast/body. If a separate contrast knob is exposed, it MUST pivot on
middle-grey, never on 0:
```
out = pivot * (in / pivot) ** c          # pivot = 0.18 linear (or 0.435 gamma); c in 1.05–1.25 (start 1.15; >1.4 = "filtered")
# ASC-CDL equivalent: out = (in*slope + offset)**power, slope 1.0–1.2, offset ±0.02, power 0.9–1.1
```
Default v2: **let the filmic curve be the only contrast.** Do NOT also run a pivoted contrast unless a look needs it.

---

## 4. Highlight protection

- The filmic **shoulder** is the protection — it asymptotes toward 1.0 instead of crossing it. With ACES/AgX this
  is built in.
- Guard rail: after tone-map, ensure the **99.5th-percentile luminance ≤ ~0.90** before display-encode (scale down
  if exceeded); reserve 0.90–1.0 for speculars only. **<0.5% of pixels at exactly 1.0** (clip check).
- Simple soft-knee (if not using a full filmic curve), C0/C1 continuous above `knee=0.8`:
  `for x>knee: out = knee + (1-knee)*(x-knee)/((x-knee)+(1-knee))`; identity below.
- Desaturate highlights slightly (AgX does this natively; for ACES, optionally lerp highlight chroma toward luma)
  to avoid the over-saturated bright look.

---

## 5. Color-theory rules (codeable, enforceable)

1. **Skin-tone line.** Skin should sit on the vectorscope **flesh line = the YIQ +I axis at phase ~123°** (range
   116–126°, target 122±1°), i.e. on the vectorscope clock ~**33.5°**. In YCbCr: the direction where
   `atan2(V-128, U-128) ≈ 123°`. CIELAB skin center `a*≈21, b*≈24, hue ≈49°`. **Enforce a band (±~5–10°), not a
   hard target** — the I-line is a rough guide. Algorithm: detect skin pixels (HSV/LAB skin range), measure their
   mean hue angle, and apply a small global hue rotation to bring that mean onto 123° (only if skin is present and
   off-line by more than the tolerance). Skin sits **slightly more chromatic and slightly yellower** than measured
   reality (memory color).
2. **Harmony = complementary, ASYMMETRIC.** Teal-orange works because skin is biologically orange; push the
   complement (teal, ~180–200°) into the **environment/shadows**, keep skin orange (~25–40°). Let **one pole
   dominate** (environment carries one, subject the other) — symmetric pushing reads as a cliché/fake filter.
3. **Vibrance, not global saturation.** `scale = 1 + amount*(1 - chroma/max_chroma)**protection`,
   `amount 0.15–0.35`, `protection ≈ 2.0` (higher = protect more). This boosts muted colors while protecting
   already-saturated pixels and skin. SweetFX form:
   `rgb = lerp(luma, rgb, 1 + Vibrance*(1 - sign(Vibrance)*color_saturation))`.
4. **Per-channel S-curves cause the "Notorious 6"** (hue skew at the secondaries). Apply contrast/tone on
   **luminance** (or use AgX's channel-mixing) and **desaturate highlights** to avoid it.
5. **Split-toning: small amounts.** Tasteful = subtle hue offsets per tonal region (warm highlights, cool shadows),
   never a heavy global tint.

---

## 6. Scope targets (the numbers an algorithm grades TO)

| Scope | Metric | Target |
|-------|--------|--------|
| Waveform | Black point | ~3–5 IRE (0.012–0.02), per channel; **not** crushed to 0 (keep shadow detail / filmic toe) |
| Waveform | Middle grey | 0.18 linear ≈ 0.40–0.46 gamma ≈ **41 IRE** (anchor the **median** mid-tone here) |
| Waveform | Diffuse white | ~**90 IRE** (0.90) for white shirt/paper/bright skin |
| Waveform | Speculars | may reach 95–100 IRE but **must not clip flat** (≤0.5% pixels at 1.0) |
| Waveform | Light skin luma | ~**65–75 IRE** (50–70% by tone); darker skin ~15–35% |
| RGB Parade | Neutrality | align channel **blacks** (shadows R=G=B) and **whites**; that neutralizes casts |
| Vectorscope | Skin | trace on the **flesh line ~123°** (band 116–126°) |
| Vectorscope | Overall sat | keep the trace inside ~**75%** of the graticule (broadcast-safe); skin at moderate radius |

These are directly measurable from `cv2`/`numpy`: median/percentile luma for exposure, per-channel percentiles for
black/white point, `atan2(V-128,U-128)` mean over skin pixels for the flesh-line check, HSV S percentiles for
saturation.

---

## 7. Look design — rebuild the 5 `.cube`s so they feel designed

The current looks are "a flat tint + a contrast S-curve" (reads as a filter). A *designed* look has:
- A **density / characteristic curve**: gentle **toe** (lifted, rolled shadows), straight mid, soft **shoulder**
  (rolled highlights) — film tonality, not a symmetric S around 0.5.
- **Subtle per-region hue shifts**: warm highlights / cool shadows but **small** (the discipline is "less is more").
- **Per-channel crosstalk** (what real film does): a touch of channel mixing rather than independent per-channel
  curves (avoids the Notorious 6).
- Optional texture (halation, grain) — *not* load-bearing; the **tonescale** is.

Because v2's looks now sit on a **properly corrected + tone-mapped base**, they should be **gentler** than v1
(the base already has body and protected highlights). Rebuild each as a low-amount design and run them at
**0.6–0.8 opacity** in the pipeline:

- **neutral_correct** — near-identity: a whisper of shoulder + ~1.02 vibrance. The "no look" pass-through.
- **warm_interview** — small warm shift in highlights, neutral-cool shadow, gentle toe; protect skin on the line.
- **teal_orange** — teal in **shadows/environment only**, orange highlights, ASYMMETRIC; modest sat; the hero look.
- **kodak_2383_style** — print-film toe/shoulder, warm highlights, slightly cool blacks, healthy density.
- **fuji_style** — green-leaning mids, soft low-contrast curve, restrained sat.

---

## 8. Implementation plan (concrete, ordered)

**Architecture decision:** keep the non-negotiable **constant-per-shot** rule by computing the develop from the
representative frame and **baking it into ONE per-shot 3D `.cube`** (numpy linearize→WB→exposure→filmic→encode),
applied via `lut3d` for video (constant ⇒ flicker-free) and via the same pure develop function for stills (exact,
not 33³-quantized). This lets us do honest **linear-light filmic** math that ffmpeg `eq` cannot express, and reuses
the proven cube-staging machinery (`_bake_match_cube`, cwd/bare-filename lut3d).

1. **`colorkit/tonemap.py` (new, stdlib+numpy):** pure functions — `srgb_eotf`/`srgb_oetf` (or BT.1886),
   `aces_narkowicz(x)`, `agx(rgb)`, `hable(x)`, `reinhard_ext(L,Cwhite)`, plus `pivoted_contrast`. All operate in
   linear; unit-test against known anchors (0→0, 0.18→~mid, 1→<1 no clip).
2. **`correct.py` rewrite:**
   - `compute_correction(bgr)` → params: `wb_gains` (shades-of-gray p=6), `black_pt`/`white_pt` per channel
     (percentiles), `exposure_gain` (median→0.18 linear), `tone` (curve name + params), `vibrance`, optional
     `skin_rotation_deg`.
   - `develop_fn(params)` → pure `f(r,g,b)->(r,g,b)` in encoded 0..1 (linearize→WB→exposure→black/white→filmic→
     encode→vibrance). Single source of truth.
   - `apply_correction_image(bgr, params)` → vectorized `develop_fn` over the array.
   - `bake_develop_cube(params, dst, size=33)` → sample `develop_fn` onto the grid, write `.cube`
     (mirrors `luts.py`/`_bake_match_cube`).
   - Drop the `colorchannelmixer`+`eq`+linear-contrast path. Remove `_TARGET_Y=0.46` mean-push.
3. **`color.py`:** add `--input-lut auto|none|<path>` (default `auto`); auto-detect I-Log via filename
   (`log`/`ilog`/`i-log`) → stage `Luna_I-Log_to_Rec709_BT1886_s65_v2.cube` as the FIRST filter (video) / first
   apply (still). Per shot: bake develop cube → chain `input_lut?, develop_lut, match_lut?, look_lut@opacity, scale`.
4. **`stylize.py`:** add look **opacity/mix** (blend graded toward original by `1-opacity`, default 0.7) for both
   the ffmpeg path (`lut3d` then `blend`/`mix`, or bake opacity into the look cube) and the still path.
5. **`luts.py` rebuild:** new toe/shoulder density base (`_film_tone`) + subtle per-region hue shifts + channel
   crosstalk; regenerate the 5 `.cube`s. Keep stdlib-only.
6. **Test loop** (non-negotiable, §9 of the autonomous prompt): run on `i log vid.mp4` (I-Log 8K), `a test.mov`,
   a photo, the HLG clip; build before/after AND **v1-vs-v2** hstack montages; READ the PNGs; judge: less washed?
   highlights intact? skin natural? graded not filtered? Fix, re-test, loop.

---

## 9. Caveats / open questions

- **ffmpeg zscale/tonemap availability** is uncertain on the Gyan build → the **bake-to-LUT-in-numpy** path avoids
  depending on it entirely (we linearize in numpy). Confirm by test; if zscale exists it's a future optimization.
- **Skin detection** for the flesh-line rotation is heuristic (HSV/LAB range) and can misfire on non-skin orange;
  gate it (only rotate if a meaningful skin-pixel fraction exists and it's off-line beyond tolerance), keep the
  rotation small, and make it optional per look.
- **AgX matrices** must be verified numerically (the inset/outset above are approximate); unit-test
  `outset == inverse(inset)` and that mid-grey 0.18→~0.18 round-trips.
- **Per-shot baked develop** assumes the representative frame is representative; strong intra-shot lighting change
  still needs the (future) smoothed-params escalation — unchanged from v1.
- **HLG/HDR** still needs a real tonemap stage (stretch goal); for now SDR-decode + filmic is a partial fix.
- **Opacity default** (0.7) is a starting point — tune by eye on the test footage.
