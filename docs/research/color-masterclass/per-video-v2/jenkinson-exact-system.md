## jenkinson-exact-system — Declan Jenkinson - The EXACT SYSTEM To Colour Grade Anything

**Tool:** DaVinci Resolve Studio 20 (project "Colour Grading Masterclass"). Color page + Project Settings. Sample footage = cinematic narrative b-roll (hooded figure at shrine, Barcelona arches, Scottish-highlands hiker, neon night-market, sports car on forest road, restaurant/interior people). Source clips shot in camera LOG (Sony S-Log3 used as the primary example). UHD timeline, 23.976 fps.

### Workflow order
The "system" is a color-managed CST sandwich with a fixed, named, broad-to-fine serial node order, then parallel look/secondary windows, then a creative LUT in display space. Saved as a per-camera PowerGrade for one-step reuse.

1. **CST IN** (node 01) — Input Color Space Transform: camera LOG/gamut → DaVinci Wide Gamut / Intermediate working space (03:44, 04:08)
2. **EXP** — Exposure (set with Global wheel on HDR/log wheels) (07:31)
3. **WB** — White Balance (Offset wheel; judged on RGB parade + Vectorscope skin line) (07:31, 12:39)
4. **CON** — Contrast (Contrast + Pivot) (07:31, 27:53)
5. **HSV SAT** — Saturation, node color space set to HSV (07:31, 14:05)
6. **Parallel look/secondary block** (nodes 06–09) — Power-Window vignettes, subject pop, glare tame (17:08–17:51, 38:46)
7. **CST OUT** — Output CST: DaVinci WG/Intermediate → Rec.709 / Rec.709-A (04:44)
8. **LUT** — creative film LUT, applied AFTER CST OUT (display-referred), strength dialed back via Key Output Gain (15:27, 23:33, 38:27)

### Demonstrated parameters (number @ mm:ss)

**Project / color management**
- **Timeline resolution**: 3840×2160 UHD, square pixels (00:35)
- **Frame rate**: 23.976 fps timeline + playback (00:35)
- **Video monitoring**: 1920×1080 HD, 23.976p, Dual-link SDI, Data levels = Video (00:35)
- **Color science**: DaVinci YRGB, Color Managed (01:47)
- **Timeline color space**: DaVinci WG/Intermediate (01:47); Output = Rec.709-A (01:47)
- **Mastering display (Dolby Vision, not enabled)**: 4000-nit, P3, D65, ST.2084, Full (01:47, 06:25)
- **Input/Output/Video-monitor LUT**: No LUT selected (01:47)
- **Mac viewer fix (Prefs > System > General)**: "Use Mac display color profiles for viewers" + "Viewers match QuickTime when using Rec.709 Scene" enabled (02:09)

**Neutral baselines (Resolve defaults — reference these in the engine)**
- **Lift / Gamma**: 0.00 / 0.00 / 0.00 = neutral (00:23, 02:03)
- **Gain**: 1.00 / 1.00 / 1.00 = neutral (00:23)
- **Offset**: 25.00 / 25.00 / 25.00 = NEUTRAL (NOT a black lift) (00:23, 12:04, 26:39, 34:33)
- **Contrast**: 1.000 neutral; **Pivot**: 0.435 (DWG default) (00:23)
- **Saturation**: 50.00 neutral; **Hue**: 50.00 neutral; **Lum Mix**: 100.00 (00:23)
- **HDR wheel neutral**: each zone Exp 0.00, Sat 1.00 (03:17)

**CST IN (input transform)**
- **Camera→CST reference table**: Sony → S-Gamut3.Cine / S-Log3; Canon → Canon Cinema Gamut / Canon Log 2 or 3; DJI → D-Gamut / D-Log; Panasonic → V-Gamut / V-Log (03:58)
- **CST IN set**: Input CS = Sony S-Gamut3.Cine, Input Gamma = Sony S-Log3; Output = Use timeline (04:08)
- **Tone Mapping = DaVinci, Adaptation 9.00, Gamut Mapping = None, Use White Point Adaptation = on** (03:44, 04:08)

**CST OUT (output transform)**
- **CST OUT set**: Input = DaVinci Wide Gamut / DaVinci Intermediate, Output = Rec.709 / Rec.709-A; Apply Forward OOTF = on; Use White Point Adaptation = on (04:44)
- **Gamut size hierarchy (rationale)**: DaVinci WG > ARRI WG > ACES AP1 > Rec.2020 > P3 > Rec.709 (04:48)
- **Wide-gamut recovery demo**: narrow Rec.709 timeline clips info; switching timeline to DaVinci WG/Intermediate recovers it (06:01, 06:21)

**Exposure (EXP / HDR Global wheel — HDR Exp scale, neutral = 0.00)**
- **Over-exposure clip demo**: Global Exp = +3.83 → waveform pinned ~95–100 (clipping) (09:58)
- **Under-exposure demo**: Global Exp = −2.33 → waveform bunched ~10–25 (crush) (10:06)
- **Demo slide-down**: Global Exp = −1.91 (07:31)
- **Night scene (correctly low)**: Global Exp = +0.14 (10:19)
- **Recovery push retained on Global**: Exp = +0.63 (06:25, 06:27)
- **Highlands baseline highlight pull**: Highlight zone Exp = −0.26 (09:34)

**White balance (Offset wheel; neutral = 25.00 per channel)**
- **Temple clip — cool cast fix**: Blue Offset 25.00 → 24.28 (~−0.72 blue) (12:56)
- **Porsche clip — blue/green cast fix**: Offset R 25.00 / G 24.60 / B 24.28 (22:29, 22:38)
- **Stage clip — cool the warm scene**: Offset R 22.95 / G 24.56 / B 25.65 (37:04)
- **Final clip — warming**: Offset R 25.00 / G 24.68 / B 23.64 (lower blue) (37:48)
- **Restaurant clip — cool back from orange**: Offset R 23.40 / G 24.65 / B 25.47 (34:41)
- **Barcelona match — warm nudge**: Offset R 25.15 / G 24.80 / B 24.50 (33:22)
- **WB on Gain wheel (alt, percent-style readout)**: G R/G/B 24.76 / 24.68 / 24.28 (blue lowest) (16:33) [flag: Gain readout shown on percent/bar scale, not the 1.0-centered scale — recheck f0069]
- **WB-node strength dialed back via Key Output Gain = 0.500** (16:18)
- **WB rule**: get the R/G/B waveform circles to line up (12:54)

**Contrast (CON node)**
- **Subtle add (already-contrasty image)**: Contrast 1.000 → 1.058, Pivot 0.435 (27:53)
- **Stronger add with lowered pivot**: Contrast 1.130, Pivot 0.337 (36:38)

**Saturation / midtone richness (HSV SAT node)**
- **Global lift via Gain master**: Gain 1.14 / 1.14 / 1.14 (31:00); also 1.13 lift (28:31)
- **Midtone richness via Gamma**: Gamma 0.02 → 0.03 across R/G/B (38:09–38:23)

**Secondaries / Power Windows**
- **Vignette window transform**: Size 50.87, Aspect 81.69, Pan 50.00, Tilt 50.00, Rotate 0.00, Opacity 100.00, Soft 1 = 9.06 (17:08)
- **Invert window** → grade outside the ellipse for vignette (17:16)
- **Vignette darken via Gamma**: −0.04 (17:40); −0.05 (35:53); −0.03 (36:15); −0.02 global vignette (36:28)
- **Subject brighten (parallel node)**: Gain 1.05 / 1.05 / 1.05 (+5%) (19:43)
- **Surround-darken vignette**: Gain 0.92 / 0.92 / 0.92 (29:08)
- **Glare/highlight tame**: Highlights = −49.00 (Primaries Highlights slider) (24:54)
- **Secondary mask strength**: Key Output Gain = 0.500 (31:10, 35:24)
- **Gradient Power Window** added to shape top of frame (38:57, 39:08)
- **Tracker (Window mode)**: Pan/Tilt/Zoom/Rotate/3D all on, Cloud Tracker, forward+reverse (29:30)

**LUT (creative, after CST OUT)**
- **LUT files (Declan LUTS)**: Barcelona.cube, DECSFILM.cube, DECSFILM clean blacks+.cube (15:31, 23:29)
- **Apply via right-click > Apply LUT to Current Node** (23:29, 38:25)
- **LUT too strong → pull back via Key Output Gain**: 0.559 → 0.571 (38:27, 38:33)

**Scope setup**
- **Reference levels**: Low = 20, High = 65 (07:59)
- **Waveform Y mode, Colorize OFF, Extents OFF** for luma reads (07:59)
- **RGB Parade** for white balance (07:47, 12:15)
- **Vectorscope + "Show Skin Tone Indicator"** (I-bar ~11 o'clock) for skin (26:55)

**PowerGrade reuse**
- **Gallery > My Powergrades** holds per-camera DEC POWERGRADE presets: Sony 1.1.1, Canon 1.2.1, DJI 1.3.1, Lumix 1.4.1 (+ L568) (20:05, 20:38)
- **Applying one recreates the full named node tree in one step** (20:19)
- **Import via right-click > Import** (PowerGrades stored as stills/DRX) (20:42)

### Distinctive techniques / opinions
- **Color-management-first is the whole foundation** — build the CST sandwich before any wheel move; grade *inside* it (03:44, 06:42).
- **Work in a wide gamut, deliver to Rec.709** — a narrow Rec.709 timeline throws away information; DWG/Intermediate timeline preserves it and can recover apparent clipping (06:01, 06:21, 04:48).
- **Strict broad-to-fine node order, each task on its own named node**: Exposure → White Balance → Contrast → Saturation → secondaries (07:31, 30:35).
- **Read the waveform spatially** — x-axis maps to image horizontal position; y-axis to brightness; teach exposure by dragging across the image (08:27, 08:37, 09:09).
- **Exposure is context-dependent** — a night scene legitimately sits low; backlit sun legitimately clips (specular). Don't force every scene to a textbook spread (10:19, 10:34).
- **WB target = align the R/G/B parade traces** ("get the circles to line up"); diagnose the offending channel and pull it on the Offset wheel (12:28, 12:54).
- **Skin-tone line on the Vectorscope is the WB/skin authority** — sample skin with the Qualifier and align it to the I-bar; match clips by how far skin sits off-center (26:55, 30:12, 33:00).
- **Set the saturation node's color space to HSV** so Gamma/Gain moves on it behave more softly (14:05).
- **Saturate via the Gamma (midtone) range** for "rich" color, and lift globally via the Gain master (31:00, 38:09).
- **Creative LUT goes AFTER CST OUT** (display-referred), and is almost always too strong on apply — dial it back with Key Output Gain, not by replacing the LUT (15:27, 23:33, 38:27).
- **Use Key Output Gain (~0.5) as a universal "strength" knob** for any node — WB correction, secondary mask, or LUT (16:18, 31:10, 38:27).
- **Power Windows direct the eye**: darken surroundings (Gain/Gamma down outside an inverted window), brighten the subject, tame glare with a windowed Highlights pull, then track the window to the moving subject (17:08–17:51, 24:54, 29:30, 38:46).
- **Match shots with split-screen gallery stills** — grab a still, wipe the split, and read the seam as a step in the waveform (31:53, 32:05).
- **PowerGrade = a saved node tree**; keep one per camera and apply it first, then tweak from exposure — this is how the "EXACT system" scales across clips (20:05, 20:19, 25:13).
- **Surprising flag** — at 29:52 the HDR wheels showed zone-boundary labels (Dark −1.50, Shadow +1.00, Light +1.00, Highlight +1.50) which are HDR *zone ranges* in stops, not applied grade values [flag: HDR zone-boundary readout vs applied Exp].

### ENGINE: what a headless auto-grader should adopt
- **correct.py / pipeline structure** — implement the grade as an explicit color-managed sandwich with a fixed broad-to-fine stage order: input-transform (camera LOG/gamut → working space) → exposure → white balance → contrast → saturation → secondaries → output-transform (working → Rec.709) → creative LUT. Treat each stage as its own operation so it can be enabled/strength-scaled independently (mirrors the node tree at 07:31).
- **tonemap.py** — input transform = camera LOG→DaVinci-WG-equivalent wide working space using the camera table at 03:58 (Sony S-Gamut3.Cine/S-Log3, Canon Cinema Gamut/Log2-3, DJI D-Gamut/D-Log, Panasonic V-Gamut/V-Log); output transform = working→Rec.709 with forward OOTF. Always grade in the wide space, never in Rec.709, to avoid the clipping shown at 06:01.
- **measure.py / scopes** — compute a luma waveform (Y), an RGB parade, and a vectorscope. Encode the skin-tone I-line (~11 o'clock) as the skin target and the parade-alignment test (R/G/B traces coincident) as the WB success metric (07:59, 12:54, 26:55). Reference levels Low 20 / High 65 as default guide rails (07:59).
- **correct.py — white balance** — auto-WB by picking a near-neutral/white reference and equalizing the RGB parade via an Offset-style move (per-channel additive around neutral). Magnitudes from the corpus are tiny: blue/green offsets typically within ±1.5 of neutral 25 (i.e. ~±0.06 normalized), e.g. blue −0.72 (12:56), or R 22.95/G 24.56/B 25.65 (37:04). Cap auto-WB moves to that small range.
- **correct.py — exposure** — set exposure on a global lift, but make it scene-aware: do NOT force a fixed target. Detect "legitimately dark/night" and "legitimately specular-clipped" scenes and leave them (10:19, 10:34). Only flag clipping when broad midtone energy is pinned, not when a small specular spike hits 100.
- **correct.py — contrast** — small contrast adds (Contrast 1.05–1.13) around a pivot (default 0.435, lower to ~0.34 for stronger contrast) keep the look natural (27:53, 36:38).
- **stylize.py — saturation** — add saturation in a perceptual (HSV-like) space; richen midtones via a gamma-range saturation push, lift global brightness via gain master (14:05, 31:00, 38:09).
- **stylize.py — vignette / subject pop** — implement an elliptical mask with strong feather; darken outside (gain/gamma −) and optionally brighten the subject (gain +5%). Values: vignette gamma −0.02 to −0.05, surround gain ~0.92, subject gain ~1.05 (17:40, 19:43, 29:08, 35:53). Add a glare-tame: windowed Highlights pull (e.g. −49) on hotspots (24:54).
- **luts.py** — apply creative LUTs in display space (AFTER the output transform), and expose a single strength/mix parameter; default it well below 1.0 (~0.5–0.57) because LUTs read too strong at full (15:27, 23:33, 38:27).
- **match.py** — match clips by aligning skin position on the vectorscope and by waveform comparison; a reference-still split (read as a waveform step) is the human-facing check (31:53, 32:05, 33:00). Implement a "warm/cool nudge" as an Offset move toward/away from the reference's skin angle (33:22).
- **Reusable look = a saved parameter set ("PowerGrade")** keyed per camera profile, applied first then trimmed from exposure — the engine's preset system should mirror this one-apply-then-tweak flow (20:05, 20:19, 25:13).
- **Universal strength knob** — every node/stage should support a 0–1 output-mix (Resolve's Key Output Gain ~0.5), so the auto-grader can globally dial intensity without rebuilding the grade (16:18, 31:10, 38:27).
