## faris-full-course-2026 — Casey Faris - Introduction to DaVinci Resolve Full Course (2026, 5.2hr, editing-heavy)

**Tool:** DaVinci Resolve Studio 20, project `Intro_to_Resolve_2025`. Color science = DaVinci YRGB Color Managed; processing = HDR DaVinci Wide Gamut Intermediate; output color space = Rec.709 (Scene); Automatic color management OFF (00:39). Source footage = H.264 High L4.0, 23.976 fps, 1920×800, 8-bit (most narrative clips); VFX plates 1920×800 / 1920×1080 float32; ProRes 422 LT "ColorClip" set. This is a beginner full-course; **almost no Color-page grading is demonstrated**. The color content lives in (a) project color-management setup, (b) per-clip Input Color Space tagging, and (c) an extended *Fusion-page* day-to-night grade. All "wheel" values below from Fusion are on Fusion-tool scales, NOT Color-page primary scales.

### Workflow order
Faris teaches color as a *pipeline stage*, not a node-tree method:
1. Recording → 2. Media Management (Media page) → 3. Editing (Cut/Edit) → 4. Effects/Graphics (Fusion) → 5. **Color** → 6. Audio (Fairlight) → 7. Rendering (Deliver) (103:32). Color is explicitly placed AFTER edit/effects and BEFORE audio+render.
Fusion day-to-night grade tree (the one real color sequence, 132:58–146:36): `MediaIn → BrightnessContrast (darken) → Merge1 (Polygon mask restores lit areas) → ColorCorrector1 (push blue) → Merge2 (original footage back through Ellipse masks for lit windows) → Merge3 (FastNoise fog) → MediaOut`.

### Demonstrated parameters (number @ mm:ss)

**Project / color-management setup (00:39)**
- **Color science**: DaVinci YRGB Color Managed (00:39)
- **Color processing mode**: HDR DaVinci Wide Gamut Intermediate (00:39)
- **Output color space**: Rec.709 (Scene); Automatic color management UNCHECKED (00:39)
- **Mastering display** (Dolby Vision section, disabled): 4000-nit, P3, D65, ST.2084, Full; Dolby Vision v4.0 (00:39)

**Color-page primary controls at NEUTRAL (default-state tour, no grade)** — capture as the engine's neutral reference:
- **Lift / Gamma**: 0.00 / 0.00 / 0.00 (master 0.00) (00:24, 12:55, 00:39)
- **Gain**: 1.00 / 1.00 / 1.00 (master 1.00) (12:55, 00:39) — note at 00:24 Gain read 1.13/1.13/1.13 [flag: likely wheel-color swatch readout, not the gain coefficient; 12:55 & 00:39 both confirm neutral = 1.00]
- **Offset**: 25.00 / 25.00 / 25.00 — this is Resolve's NEUTRAL offset readout, NOT a black lift (00:24, 12:55, 00:39)
- **Contrast 1.000, Pivot 0.435** (00:24, 12:55, 00:39)
- **Temp 0.0, Tint 0.00** (00:24, 12:55)
- **Sat 50.00, Hue 50.00, L.Mix 100.00** (00:24, 12:55, 00:39)
- **Soft Clip**: High 50.0 / Low 50.0 / H.S. 0.0 / L.S. 0.0 (00:39, 12:55)
- **Curves**: "Curves - Custom", straight 45° diagonal (default) (12:55); Hue-vs-Hue mode Input Hue 256.00, Hue Rotate 0.00 (00:24)

**Per-clip Input Color Space tagging (123:44)** — right-click Media Pool clip > Input Color Space:
- Current tag = **Rec.709** (checked); project default = "Rec.709 Gamma 2.4" (123:44)
- Navigates to **Blackmagic Design > Pocket 4K Film** (camera-native) (123:44). Full IDT list available: ACES, ARRI, Canon, Cineon, DaVinci Intermediate, RED, Sony, Linear, P3, Rec.709/2020/2100, HLG, PQ, sRGB, etc.

**Fusion day-to-night grade — Fusion-tool scales (neutral: Gain/Gamma/Contrast=1.0, Lift/Brightness=0.0, Saturation=1.0)**
- **ColorCorrector1** (round-trip-proof magenta demo, 121:12): wheel Hue 0.0 / Sat 1.0 / Tint -0.1363 / Strength 1.0; per-channel Contrast/Gain/Lift/Gamma all 1.0/1.0/1.0/1.0 → extreme magenta result
- **ColorCorrector1, blue night attempt** (133:44): wheel Tint 0.6347 toward blue / Strength 0.2809; Contrast 1.32; Gain 1.0
- **ColorCorrector1** (133:50): Contrast 1.38; **Gain pulled to 0.14** (highlights crushed, "take brightness of brightest parts down")
- **BrightnessContrast1** (134:20): Gamma 0.42 (down from 1.0 → darker mids)
- **BrightnessContrast1** (134:41): Gamma 0.31; **Saturation 0.42** (desaturated dusk)
- **BrightnessContrast2 (sky branch)** (136:00): Gain 0.17 (sky highlights crushed hard), Gamma 0.61, Sat 1.0
- **BrightnessContrast2 (later review)** (146:21→146:36): Gain 0.208, Gamma 0.52→0.61, Saturation 0.14
- **Final whole-composite ColorCorrector1** (139:14): wheel Tint -0.3819 toward blue / Strength 0.2471; Saturation 0.77 (below neutral); all RGB channels neutral
- **FastNoise fog** (125:24→131:15): Detail 8.43→9.61, Scale 7.56→5.35, Seethe 0.239, Seethe Rate 0.0→0.005; Color tab Two Color (Color1 alpha 0 = transparent, Color2 alpha 1 = opaque black)
- **FastNoise fog v2** (143:50→145:06): Detail 7.56, Scale 3.15, Seethe Rate 0.022; **Merge3 Blend 0.205 → final 0.134** (~13% fog opacity)
- **Masks** (Fusion, 0–1 normalized): Polygon Soft Edge raised 0.0 → 0.0362 → 0.0614 for sky-blend feather (138:04, 138:32); Ellipse window masks Width/Height ~0.026–0.077 to reveal lit windows (140:54, 141:30, 141:52)

**Fusion source-pixel float samples (status-bar probe, 0–1 float — reference points, NOT grades)** [flag: these are pointer pixel-samples, not grade controls — do not ingest as wheel values]:
- Wide plate mids R0.454/G0.424/B0.399 (122:07); shadow R0.121/G0.104/B0.076 (123:16); highlight R0.956/G0.850/B0.821 (124:26); day-plate baseline R0.281/G0.211/B0.171 (133:07); post-darken near-black R0.005/G0.006/B0.004 (134:41)

**Edit-page Transform / OFX (not grades, scale-noted to prevent mis-ingest)**
- Transform neutral: Zoom 1.000, Position 0.000, Rotation 0.000 (75:21); punch-in Zoom 2.660 / 3.650, Position X 555/619 (76:46, 77:01)
- Resolve FX Color OFX *category exists and is browsable on the Edit page* (82:10): ACES Transform, Chromatic Adaptation, Color Compressor, Color Space Transform, Color Stabilizer, Contrast Pop, DCTL, Dehaze, Despill, False Color, Gamut Limiter, Gamut Mapping, Invert Color, NVIDIA RTX Video HDR
- Title text color picker (84:35) is 0–255 HSV (Hue 173/Sat 213/Val 255, #2affe6 teal) [flag: 0–255 title-fill scale, NOT a Lift/Gamma/Gain wheel value]

### Distinctive techniques / opinions
- **Color-managed-first project setup**: defines color science + wide-gamut log processing + Rec.709 output *before* any grading (00:39).
- **Day-for-night as a Fusion node comp, not a Color-page grade**: darken (BrightnessContrast) → restore lit areas through masks → tint blue (ColorCorrector) → merge original footage back only inside ellipse masks for glowing windows → add masked FastNoise fog (132:58–146:36). "Color correct it blue, put original footage over everything but only within masks, then fog only inside a mask" (145:36).
- **Split tonal treatment**: separate darken-branches for foreground vs sky (sky crushed harder, Gain 0.17), merged via a soft-edged Polygon mask (136:00–138:32).
- **Tag Input Color Space per clip to the camera-native space** (Pocket 4K Film) rather than leaving Rec.709 (123:44) — the color-managed input discipline.
- **Fog opacity is dialed low** (Merge3 Blend ~0.13) so atmosphere reads as subtle (145:06).
- **Viewer Gain/Gamma is display-only**, explicitly does NOT affect render/output (152:19) — a guard against confusing preview brightness with a grade.

### ENGINE: what a headless auto-grader should adopt
- **measure.py neutral reference**: lock the Color-page neutrals confirmed here — Lift/Gamma 0.00, Gain 1.00, Offset readout 25.00 (=neutral, not a lift), Contrast 1.000, Pivot 0.435, Sat 50.0, L.Mix 100.0 (12:55/00:39). Treat Offset=25 as zero so the engine never mistakes it for a black raise.
- **correct.py color-management-first**: replicate the setup order — set working space (DaVinci Wide Gamut Intermediate / a wide log space) + Rec.709 output transform BEFORE grading, and tag each input clip's source color space (camera IDT) rather than assuming Rec.709 (00:39, 123:44). This is the single most reusable lesson in the video.
- **tonemap.py / day-for-night recipe** (portable to a stylize look): (1) reduce gain on highlights hard (Gain≈0.14–0.17), (2) pull gamma down (≈0.31–0.42) to darken mids, (3) desaturate (Sat≈0.42–0.77), (4) push tint toward blue, (5) optionally mask the sky for an even darker treatment, (6) reveal practical lights by compositing untouched source back through small soft masks. Concrete value envelope: highlights −85%, mids gamma ≈0.3–0.4, sat ≈0.4–0.8 (133:44–139:14).
- **match.py / split-region grading**: support a sky-vs-foreground split with independent tone curves merged under a soft-edged mask (feather ≈0.04–0.06 normalized) — directly mirrors the Polygon-masked sky branch (136:00–138:32).
- **stylize.py atmospherics**: a low-opacity procedural-noise fog layer (Two-Color black-with-alpha, Blend ≈0.13, slow Seethe Rate ≈0.005–0.02) is a cheap, effective mood add (125:24–145:06).
- **scopes**: the course relies on Waveform + Parade (00:24, 00:39) as the default reads; ensure the engine's scope read defaults match (1023-scale waveform/parade). Pixel values reported by the engine should use 0–1 float internally (every Fusion probe here is 0–1), matching a float32 working pipeline.
- **Guardrail**: distinguish *viewer/display* gain from *image* gain (152:19) — an auto-grader must never measure off a display-adjusted preview. Also never ingest title-text color (0–255) or Fusion-tool wheel coords as Color-page primary values; the scale differs.
