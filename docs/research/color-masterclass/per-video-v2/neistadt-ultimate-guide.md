## neistadt-ultimate-guide — Jason Neistadt - Color Grading: The ULTIMATE GUIDE

**Tool:** DaVinci Resolve Studio 20 (macOS), color-managed project "VID_0014_Learn_Color_Grading_Full Tutorial_06-13-2025". Source footage: Nikon N-RAW 4K 12-bit 60fps, Nikon N-Log gamma. Scopes on 10-bit 0–1023 scale; CIE diagram on Rec.709 (D65) gamut. Resolve neutral conventions confirmed throughout: Lift/Gamma neutral = 0.00, Gain neutral = 1.00, Offset neutral = **25.00** (NOT a black lift), Saturation/Hue neutral = 50.00 (0–100 scale), Lum Mix neutral = 100.00.

### Workflow order
The course's reference "professional node tree" — a CST sandwich, broad-to-fine, single-purpose nodes (00:26, frame f0020_0026):
1. **CST In** (input transform) → 2. Exposure / Balance → 3. Log → 4. Curves → 5. Saturation → 6–8 Secondaries (parallel branch: Second / Main) → 10 Global → 11–16 Adjustment + Power-Window layer/parallel branches → 18 Look → 19 Fine Tune → 20 Sharpen → 21 Glow → 22 FX → 23 Grain → 24 **CST Out**.
- Simplified recommended node order also shown (00:33, f0028_0035): **01 Exposure/Correction → 02 White Balance → 03 Creative → 04 (further secondary)**.
- Conceptual framing: each node = one part of the grade, like Photoshop layers — one node for exposure, another for color (03:08).
- Within the primaries, broad-to-fine tonal split: **Lift = shadows, Gamma = midtones, Gain = highlights, Offset = overall brightness/exposure** (03:57–03:59).
- OFX best-practice ordering: apply OFX on color-managed workflows BEFORE creative grading; avoid clipping highlights / crushing shadows (55:05).

### Demonstrated parameters (number @ mm:ss)

**Neutral baseline (recurring reference):**
- **Lift / Gamma**: 0.00 ×4; **Gain**: 1.00 ×4; **Offset**: 25.00 ×3 = neutral (00:02, 01:34, 02:43, 26:51, 30:14, 40:25)
- **Top bar neutral**: Temp 0.0, Tint 0.00, Contrast 1.000, Pivot 0.435, Mid/Detail 0.00 (00:02, 01:34)
- **Bottom bar neutral**: Color Boost 0.00, Shadows 0.00, Highlights 0.00, Saturation 50.00, Hue 50.00, Lum Mix 100.00 (00:02, 01:34)
- **Lift small uniform pull**: -0.15 ×4 (00:04); -0.14 ×4 (15:57, 16:02); -0.07 (00:28); -0.10 (56:47)

**Primaries — Color Wheels (Lift / Gamma / Gain / Offset modes):**
- **Bars mode** identical neutral values to wheels — confirms shared control system (04:17)
- **Log Wheels mode**: Shadow/Midtone/Highlight 0.00, Offset 25.00; Low Range 0.333, High Range 0.550 (default log range split) (04:27, 05:03)
- **Lift demo (shadow pull, luma-only)**: -0.13 ×4 (16:23); -0.05 ×4 (17:03) — shadows drop, highlights anchored
- **Offset demo (global brightness, with residual Lift -0.14, Gamma -0.01, Gain 1.10)**: raised 69.55 (18:10), lowered 6.55 (18:12), mid 42.55 (18:15), just-below-neutral 17.00 (18:19) — whole trace moves together
- **Inspected applied grade**: Lift -0.31, Gamma 0.00, Gain 0.92, Offset 55.80 (above neutral = lifted exposure / blacks off floor, highlights down ~8%) (25:40, 25:53)
- **Contrast move (color wheels, not curve)**: Lift -0.18 ×3, Gain 1.25 ×3, Offset 25.00 neutral, Saturation 76.00 (27:37); saturation then pulled back to 54.40 (27:56)
- **Night-street base correction**: Lift +0.02 (raised blacks), Gamma 0.00, Gain 0.92 (highlights down), Offset 25.00 neutral, Saturation 56.20 [flag: extraction notes "56.20 = slightly raised" vs stated default 50 — readout/scale ambiguity on the Saturation 0–100 control] (35:53)
- **Warm skin lift on qualified node**: Lift 0.02 / 0.04 / 0.07 (R/G/B warm shift) vs 0.02 neutral baseline; Gain 0.92, Offset 25.00 (37:56, 38:09)
- **Power-window background darken (node 03)**: Lift -0.05 ×4, all else neutral (42:30)
- **Man-on-phone base grade**: Lift -0.16 ×4, Gamma 0.08 ×4, Gain 1.23 ×4, Offset 25.00, Color Boost 20.90, Saturation 57.43 (45:01, 46:13, 48:19)
- **Second phone-clip grade**: Lift -0.17/-0.15/-0.17/-0.21, Gamma 0.10/0.16/0.12/0.10, Gain 0.89/0.92/0.89/0.84 (master 0.89, R>G,B; slight green/cool), Offset 25.00, Color Boost 20.90, Saturation 57.43 (47:17, 47:24, 48:06)

**Curves (Custom + 2D side curves):**
- **Custom S-curve** for contrast — shadows down, highlights up; point coordinates not numerically exposed by Resolve UI (31:06, 31:15); waveform visibly stretches toward both ends
- **Hue vs Hue**: neutral Input Hue 256.00, Hue Rotate 0.00 (31:21); applied skin shift Input Hue 277.34, Hue Rotate -12.08 (39:14)
- **Hue vs Sat**: neutral Input Hue 256.00, Saturation 1.00 (multiplier, not 0–100) (32:01)
- **Hue vs Lum**: neutral Input Hue 256.00 / Lum Gain 1.00 (32:31); teaser Input Hue 119.68, Lum Gain 0.71 (00:36); applied night clip Input Hue 100.88, Lum Gain 0.35 (hue darkened to 35%) (32:40)
- **Lum vs Sat**: neutral Input Lum 0.00, Saturation 1.00 (08:28, 32:48); slight shadow desat Saturation 0.99 (33:12)
- **Sat vs Sat**: neutral Input Sat 0.00, Output Sat 1.00 (33:13); pull-down high-sat demo with primary Saturation bar reading 81.40 (33:15) [flag: surprising=true — 81.40 is on the 0–100 primary Saturation control, NOT the Sat-vs-Sat curve's 0.00–1.00 output; do not conflate the two scales]
- **Right-click a single curve point** to reset it without clearing the whole curve (34:08)

**HSL Qualifier (skin isolation):**
- **Default HSL**: Hue Center 50.0 / Width 100.0 / Soft 0.0 / Sym 50.0; Sat Low 0.0 / High 100.0; Lum Low 0.0 / High 100.0 (36:02)
- **Auto-built skin key** (after eyedropper on skin): Hue Center 37.9, Width 4.4, Soft 3.2, Sym 50.0; Sat Low 3.4, High 7.8; Lum Low 59.9, High 70.0 (36:37); refined Hue Center 36.7, Sat Low 2.7 / High 8.6, Lum Low 55.3 / High 70.9, L/H.Soft 2.6 (38:09); teaser key Hue 37.3, Width 3.1 (00:22)
- **Matte Finesse cleanup**: Clean Black 16.8, Clean White 60.2, Blur Radius 21.4 (37:56, 38:09)
- **Other qualifier modes**: RGB (per-channel Low/High) and LUM (brightness-only) shown at defaults (36:12, 36:19)
- **Shift+H** toggles highlight/matte (gray=excluded) view to verify the selection (36:43)

**RGB Mixer:**
- **Identity matrix**: R 1/0/0, G 0/1/0, B 0/0/1; Preserve Luminance checked (06:29)
- **Monochrome B&W with Rec.709 luma weights**: Red 0.21, Green 0.71, Blue 0.07 (06:46)

**Scopes / reference levels:**
- **Waveform/Histogram/Parade** vertical & horizontal scale 0–1023 (ticks 128/256/384/512/640/768/896) (00:18, 21:06)
- **CIE Rec.709 (D65) primaries**: R 0.6400,0.3300 / G 0.3000,0.6000 / B 0.1500,0.0600 / W 0.3127,0.3290 (28:02)
- **Scope type toggle**: Y / CbCr / RGB (Y = luma) (21:35)
- **Colorize** trace by hue, **Extents** to show out-of-range signal (22:29, 22:37)
- **Show Reference Levels** narrowed to Low 83 / High 964 (vs default 0/1023) for a range-limited "cinematic" floor/ceiling (24:10)
- **Per-band Vectorscopes** split All/Low/Mid/High; Low Range 0.30, High Range 0.70 thresholds; Colorize ON, Skin Tone Indicator toggle, Graticule ON (28:28, 28:33)

**Power Window / Tracker:**
- **Circle window Transform**: Size 50.00, Aspect 32.92 (oval), Pan 53.12, Tilt 52.02, Rotate 14.14, Opacity 100.00, Soft 1 24.68 (43:02); tight face circle Soft 1 4.13 (45:08)
- **Sizing (Input Sizing, transform not grade)**: Pan 14.656, Tilt 0.000, Zoom 1.538, Rotate -4.122 punch-in (12:30/12:34)
- **Tracker types (Resolve 20)**: Cloud Tracker, Point Tracker, AI IntelliTrack (Neural Engine); DOF toggles Pan/Tilt/Zoom/Rotate/Perspective 3D all default-on; Clip vs Frame mode (45:32, 46:26, 47:26)
- **Stabilizer defaults**: Cropping Ratio 0.50, Smooth 0.25, Strength 1.00, mode Perspective; analysis ~87 fps (10:32, 48:06)

**OFX (Open Effects):**
- **CST (utility)**: Input Gamma Nikon N-Log → Output Rec.709 / Rec.709-A; Tone Mapping DaVinci; Adaptation 9.00; Gamut Mapping None; Apply Forward OOTF ON, Inverse OOTF off, White Point Adaptation ON (53:21, 53:36)
- **Film Grain (Film Emulation)** preset "35mm 400T": Composite Overlay, Opacity 0.500, Texture 0.750, Grain Size 0.000, Strength 0.284, Softness 0.234 (52:22); Custom preset Texture 0.791, Grain Size 0.721, Strength 0.310 (52:33)
- **Lens Flare (Light)** preset Headlight: Composite Add, Glare Brightness 0.034, Glare Color cyan; tracked to follow a car headlight (00:28, 53:02)
- **Halation, Dehaze** located via search (53:59, 54:13)
- **Render Cache** (Playback menu) + Smart cache mode for OFX-heavy footage (51:42)

**Key palette (node strength):**
- Key Output Gain 1.000 = neutral (node "opacity") (11:33)

### Distinctive techniques / opinions
- **Offset = global exposure control** — the quick whole-image brightness fix; raising/lowering it moves shadows+mids+highlights together; likened to exposure in photography (03:57, 18:10–18:19).
- **Lift is anchored at the top** — pulling Lift moves shadows while highlights barely change (17:03).
- **Build contrast with a subtle S-curve** and confirm it by watching the waveform expand toward both ends (31:06–31:15).
- **Skin tone discipline**: isolate skin with the HSL qualifier, then check it on the Vectorscope against the **skin-tone indicator (I-bar, ~11 o'clock between Red and Yellow)**; do the alignment while the skin is isolated in highlight mode (27:25, 38:28–38:37). Don't push skin to a "Hulk" extreme (37:56).
- **Don't over-qualify** — over-adjusting qualifiers causes harsh edges / color artifacts; clean the matte with Finesse (Clean Black/White, Blur Radius) instead (38:46, 37:56).
- **Label your nodes** (e.g. node 02 → "Skin Adjustment") to keep the node tree organized (39:08–39:15); same discipline restated for tracking (49:10).
- **Desaturate shadows** with Lum vs Sat to avoid noisy colors in the darks (32:48–33:12).
- **Tame harsh colors** with Sat vs Sat — pull down the already-highly-saturated areas (33:15).
- **CST over a creative LUT** for normalizing log/RAW — a LUT can clip or distort colors; the CST gives a clean Rec.709 starting point (53:05).
- **Reference Levels as a cinematic guardrail** — set a black floor / highlight ceiling (e.g. 83/964) so blacks never crush and highlights never clip (24:10).
- **Combine qualifiers with Power Windows** for spatial restriction, and **track** the window onto moving subjects (38:14, 42:55).
- **Loop the clip while grading** and use **Lightbox** to check exposure/color consistency across the whole timeline at a glance (02:10, 14:52).
- **OFX use-cases**: Glow for beauty/weddings/emotional moments; Film Grain to unify digital footage with an organic texture; apply OFX in color-managed order before the creative grade (54:45, 55:05).
- **Gallery / PowerGrades** to save stills and reuse developed looks across clips (12:56).

### ENGINE: what a headless auto-grader should adopt
- **measure.py / scopes**: Standardize on the 10-bit 0–1023 internal scale (matches Resolve's waveform/histogram/parade). Encode the Rec.709 (D65) primaries exactly as R 0.6400,0.3300 / G 0.3000,0.6000 / B 0.1500,0.0600 / W 0.3127,0.3290 for gamut/CIE checks and clamping (28:02).
- **correct.py — Offset as global exposure**: implement a single "offset/exposure" control that lifts shadows+mids+highlights together (additive in working space), distinct from Lift (shadow-anchored-at-top) and Gain (highlight pivot). Mirror the demonstrated tonal split: Lift→shadows, Gamma→mids, Gain→highlights, Offset→whole image (03:57, 17:03, 18:10–18:19).
- **correct.py — auto-contrast**: default to a gentle S-curve (lower point pulls shadows below the diagonal, upper shoulder lifts highlights) and validate by checking the output waveform spread vs input — auto-strength gated so it expands but does not clip (31:06–31:15, 00:24 soft-clip shoulder).
- **measure.py — skin detection + scoring**: detect skin via an HSL window centered ~Hue 37 (narrow Width ~4, Sat ~3–8, Lum ~55–70 on the 0–100 qualifier scale) and score how close the qualified cluster sits to the vectorscope skin-tone line (~11 o'clock, R→Yl). Use this as a correctness target the auto-grader nudges toward, with a hard cap to avoid over-correction (36:37, 27:25, 27:36).
- **stylize.py — matte finesse**: when keying for secondaries, expose Clean Black / Clean White / Blur Radius equivalents to clean the matte rather than tightening the key bounds (avoids harsh edges) (37:56, 38:46).
- **stylize.py — B&W**: use Rec.709 luma weights 0.2126/0.7152/0.0722 (shown 0.21/0.71/0.07) for any monochrome conversion (06:46).
- **stylize.py — film finishing**: model grain (texture/size/strength sliders, default ~"35mm 400T": strength ~0.28, overlay composite), halation (subtle red glow on highlights), and an optional lens-flare-on-tracked-light pass as separate finishing nodes after the grade (52:22, 53:59, 53:02).
- **tonemap.py — CST sandwich**: normalize log/RAW with an input→output color-space transform (e.g. Nikon N-Log → Rec.709/Rec.709-A, DaVinci tone-map, Adaptation 9.0, OOTF forward ON, white-point adaptation ON) as the FIRST node, and a matching CST-out as the last; prefer this over a baked creative LUT to avoid clip/distortion (53:21–53:36, 53:05).
- **scopes — reference-level guardrails**: implement a configurable black-floor / highlight-ceiling clamp (demonstrated 83/964 on 0–1023) so auto-grades never crush blacks or blow highlights; expose as a "cinematic range" toggle (24:10).
- **match.py — still/PowerGrade reuse**: support saving a developed grade as a reusable still and applying it across clips for shot-to-shot consistency; pair with a Lightbox-style whole-timeline consistency pass before export (12:56, 14:52).
- **pipeline order**: enforce broad-to-fine, single-purpose stages (CST in → exposure/balance → curves → saturation → secondaries → windows → look → finishing → CST out) and label every stage, matching the demonstrated node tree (00:26, 00:33).
- **node strength**: expose a per-stage "opacity"/key-output gain (1.0 neutral) so any correction can be blended back (11:33).
