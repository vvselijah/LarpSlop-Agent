## euro-pro-level-64min — European Filmmaker - Learn PRO-Level Color Grading in 64 Min

**Tool:** DaVinci Resolve Studio 19 (Version 19.1.3 Build 7, © 2024 Blackmagic Design; "DaVinci Resolve 19.1 Studio") (07:46, 07:54). Color-managed timeline, DaVinci YRGB / DaVinci Wide Gamut + DaVinci Intermediate intermediate → Rec.709 output. Mixed multi-camera source: Apple Log, BM/Film Gen 5, D-Log-M (DJI), F-Log 2 / F-Log 2C (Fujifilm), Blackmagic RAW, Apple ProRes, H.265. Premiere Pro shown only as a foil for the node-vs-effects-stacking contrast (02:29, 02:58). Free version covers most features; Studio ($295) recommended for advanced tools (07:54).

### Workflow order
The colorist's full annotated template tree (25:03), the showcase tree (24:30 / 03:02), and the simple beginner chain (25:01) together define the order:

1. **Input transform** — `>DWG` / IN node (DaVinci Wide Gamut + DaVinci Intermediate input) (24:30, 03:02, 32:32-equiv CST)
2. **NR** — noise reduction (24:30)
3. **Highlight Recovery** — group, nodes 02/03/04 incl. one "No Color Correction" reference node (25:03)
4. **EXP hdr** — exposure (24:30); **Balancing** group — `Bal: Exp` (06), `Bal: Color` (07), `Bal:` (08) (25:03)
5. **SAT scv / Color slice / Col Dens** — saturation + color separation + color density (24:30)
6. **Light Shaping** — Character, Vignette, Eyes, Gradient (nodes 09-16) (25:03)
7. **Look** — `Look I`, `Look II` (nodes 17/18) (25:03); creative `LUT` node (24:30)
8. **Eigener Workflow** (own workflow) — Glow, Clean W, Pop (21/23/24); **Denoise/Sharpen** (20/25); **Projektspezifische Nodes** (project-specific, 28-32) (25:03)
9. **Output transform** — `>REC.709` / OUT node (24:30, 03:02)

Beginner minimal chain: **Exposure → Balance → Saturation** (25:01, 25:27, 25:43). The core rule throughout: build the **CST sandwich** — IN (input) conversion node + OUT (output) conversion node, do ALL grading on nodes *between* them, keeping the large working color space in the middle (12:32, 26:22).

### Demonstrated parameters (number @ mm:ss)

**Neutral/default reference values (Resolve scale guards, confirmed repeatedly):**
- **Offset neutral**: 25.00 / 25.00 / 25.00 (R/G/B) — Resolve neutral, NOT a black lift (00:33, 01:19, 02:32, 03:09, 03:41, 10:50, 13:49, 26:10)
- **Gain neutral**: 1.00 / 1.00 / 1.00 (00:33, 02:32, 03:09)
- **Lift / Gamma neutral**: 0.00 (00:33, 02:32, 03:09)
- **Contrast neutral**: 1.000; **Pivot** 0.435 (default DWG pivot); **Mid/Detail** 0.00 (00:33, 02:32, 03:09)
- **Saturation neutral**: 50.00; **Hue neutral**: 50.00; **Lum Mix** 0.00; **Color Boost / Shadows / Highlights** 0.00 (00:33, 01:19, 02:32, 03:09)
- **Temp** 0.0, **Tint** 0.00 (00:33, 03:09)
- **RGB Mixer identity**: Red out 1.00/0.00/0.00, Green out 0.00/1.00/0.00, Blue out 0.00/0.00/1.00; Preserve Luminance ON, Monochrome OFF (03:11, 22:39, 23:08)
- **Custom Curves neutral**: straight diagonal, Y/R/G/B Edit = 100; **Soft Clip** Low 50.0 / High 50.0 / L.S. 0.0 / H.S. 0.0 (03:13, 17:12, 17:23, 23:23)
- **Color Slice neutral**: Den 0.00, Den.Depth 0.00, Sat 1.00, Sat.Balance 0.00, Sat.Depth 0.00, Hue 0.00; per-vector Center/Hue 0.000, sliders 0.00/1.00 (03:14)
- **Qualifier HSL default**: Hue Center 50.0 / Width 100.0; Sat 0.0-100.0; Lum 0.0-100.0; Matte Finesse White Clip 100.0, rest 0.0 (03:16)
- **Power Window default**: Size/Aspect/Pan/Tilt 50.00, Rotate 0.00, Opacity 100.00; Softness ~50.00 (03:17)
- **Blur palette neutral**: Radius R/G/B 0.50 (neutral = no blur), H/V Ratio 0.50, Scaling 0.25 (23:40)

**Small intro contrast/exposure grade (showcase clip):**
- **Contrast**: 1.032 (00:44, 00:47, 01:19); 1.032 with Gamma -0.01/-0.01/-0.01, Gain 1.01/1.01/1.01 at 00:39
- **Lift**: 0.04 (master, near-neutral) (00:44, 00:47, 01:19)
- **Gain**: 1.02 (master, a hair high) (00:44, 01:19)

**Offset (balance) move — warm/yellow push via Offset wheel only:**
- **Offset**: 25.71 / 24.47 / 23.45 (R/G/B) — R +0.71, G −0.53, B −1.55 from 25.00 neutral = slight warm/yellow push, Lift/Gamma/Gain untouched (03:48)

**Active primary grade demonstrations:**
- **Contrast 1.178 around Pivot 0.435 + Offset-master brightening 36.20** (above 25.00 neutral) (21:34)
- **Contrast 1.178 + Offset-master 34.80** (above neutral, positive brightening) (22:18, 22:19)
- **Full contrast/exposure node** (24:44): Lift −0.02, Gamma +0.09 (midtone lift), Gain 0.96 (highlights pulled down), Contrast 1.160 @ Pivot 0.435, **Highlights slider −100.00** (full crush), Offset still 25.00 neutral, Saturation 50.20
- **Uniform luminance master Offset** 42.55 / 42.55 / 42.55 (equal across channels = brightening, not a color cast) (14:56) [flag: frame dimmed by transition overlay, medium confidence]
- **Offset 5.00 / 25.00 / 25.00** during Input-Color-Space menu — likely the leading "2" of "25.00" occluded by the context menu, NOT a real −20 red offset (14:47) [flag: menu-overlay occlusion of Offset R digit; low confidence, recheck]

**Color Space Transform (CST) node configs:**
- **DWG → Rec.709 output**: Input DaVinci Wide Gamut / DaVinci Intermediate → Output Rec.709 / Gamma 2.2; Tone Mapping Method = DaVinci, Adaptation = 9.00 (20:48, 22:15, 23:18, 23:38)
- **Apple Log → DWG input**: Input Rec.2020 / Apple Log → Output DaVinci Wide Gamut / DaVinci Intermediate; Tone Mapping DaVinci, Adaptation 9.00 (21:24)
- **Manual conversion example**: Input Rec.2020 / Apple Log → Output "Use timeline" (13:49); Input DWG / DaVinci Intermediate → Output Rec.709, picking Output Gamma from dropdown (08:55)

**Project Settings — color management:**
- **Unmanaged baseline**: Color science DaVinci YRGB; Timeline color space DaVinci WG/Intermediate; Output Rec.709-A (04:15); variant Timeline Rec.709 (Scene) / Output Same as Timeline (04:22, 14:10, 15:20)
- **Managed**: Color science DaVinci YRGB Color Managed; Automatic color management CHECKED; Color processing mode SDR; Output SDR Rec.709 (04:19, 14:15, 15:02)
- **Instructor's recommended manual setup**: DaVinci YRGB; Timeline DaVinci WG/Intermediate; **Output Rec.709 Gamma 2.2** (08:21)
- **Color science dropdown options**: DaVinci YRGB, DaVinci YRGB Color Managed, ACEScc, ACEScct (08:30, 09:19, 15:07)
- **Per-clip Input Color Space**: right-click → Input Color Space → e.g. Fujifilm → F-Log2 (14:47)
- **Camera Raw master**: RAW profile ARRI, Decode quality Full res., Decode using Camera metadata (04:12, 04:14)
- **Dolby Vision mastering preset** (present, unchecked everywhere): version 4.0, Analysis tuning Balanced, Mastering display 4000-nit P3 D65 ST.2084 Full (04:15, 15:02)

**Project Settings — timeline / monitoring / LUT:**
- **Timeline**: 3840×2160 UHD, Square pixels, 30 fps timeline + playback (08:06); Video monitoring 1920×1080, 30p, Dual link SDI, Video data levels (08:06)
- **3D LUT interpolation**: changed Trilinear → **Tetrahedral** ("improves how LUTs work") (16:57, confirmed Tetrahedral at 18:43)
- **Broadcast Safe**: IRE levels 20–120 (16:51) / shown as −20–120 (16:53, 18:43) [flag: IRE low-bound reads "20" vs "−20" across frames; medium confidence], "Make broadcast safe" CHECKED (16:51, 18:43)
- **LUT slots**: Input/Output/Video-monitor = No LUT; Color-viewer + Scopes = Use video monitoring selection (16:51, 18:43)

**Monitor gamma rule of thumb (teaching cards):**
- **Gamma 2.2** = computer screens / web / online video (sRGB displays) (16:08)
- **Gamma 2.4** = TV broadcast / cinematic / darker home-theater viewing (16:30, 16:45)

**Frame-rate conforming (multicam match):**
- Source clips 25.000 / 50.000 / 29.970 fps → all conformed to **25.000 fps** via Clip Attributes > Video Frame Rate (09:50, 10:19, 10:23)

**Gaussian Blur (effects-on-node demo):** Horizontal & Vertical Strength 0.364, "Same H and V" checked (20:06)

**Source clip metadata:** A002...C003.braw — Blackmagic RAW, 3728×3104 16-bit, 25.000 fps (23:29); X-Rite ColorChecker Classic – Legacy 24-patch chart preset in Color Match (23:32)

### Distinctive techniques / opinions
- **Log is un-finished, not a look**: ungraded Fujifilm log is flat/milky; "ungraded footage always looks unfinished" — grading adds contrast + saturation + clean/warm whites (02:02, 02:05).
- **Node system vs effects-stacking**: Resolve nodes explicitly sold against Premiere's Adjustment-Layer effects-stacking model (02:29, 02:58).
- **"Slap a LUT on it" is the beginner trap**: importing a free .CUBE LUT pack in another NLE is shown as the approach being criticized (03:34).
- **Color management is the smart path**: "DaVinci YRGB Color Managed does the work for you" — auto-converts every camera format (f-log, b-raw, d-log-m, apple log) to one unified space; with it enabled the per-clip CST plugin is NOT needed (04:07, 04:19, 09:08, 14:57).
- **DaVinci YRGB = display-referred (manual, more control); YRGB Color Managed = scene-referred (automated)** (08:43, 09:01). ACES set aside for this lesson in favor of DaVinci YRGB (09:27, 09:46).
- **Don't convert log→Rec.709 in the FIRST node then grade** — the explicit beginner mistake warned against; use proper CST conversion nodes instead of a baked LUT in node 01 (25:58, 26:02, 26:10).
- **Use two conversion nodes (input + output) and keep the LARGER color space in between for grading** — the CST sandwich (12:32, 26:22). Output gamma choice matters (Gamma 2.2 vs 2.4) for the target display (16:08, 16:30).
- **Set 3D LUT interpolation to Tetrahedral** for better LUT accuracy (16:57).
- **Grade in a wide gamut to keep more color data**: CIE diagram nests DaVinci Wide Gamut > ARRI Wide Gamut > ACES AP1 > Rec.2020 > P3 > Rec.709 (06:52, 07:16); Rec.709 is the smallest / the standard for TVs and YouTube (06:05, 07:07).
- **Conform mixed frame rates first** (Clip Attributes) so multicam cuts together before color matching (09:50-10:23).
- **Shot-matching via Image Wipe**: dual-viewer / diagonal-wipe / blend (alpha) overlay modes to compare a clip against a reference still (21:07, 21:14, 21:25, 21:27); Color Match palette from an X-Rite ColorChecker chart for auto-match (23:32).
- **Build per-clip stills + PowerGrade albums**: !DWG album holds per-camera log→DWG/709 conversion PowerGrades (Apple Log, BM Gen 5, D-Log M, F-Log 2, F-Log 2C, Rec.709); Stills = per-project, PowerGrades = cross-project (17:23-17:42).
- **Serial nodes are a one-way road trip**: each node = a sequential stop building on the prior; output of one feeds the next, can't go back without "turning around" (25:21, 25:43).
- **Live LUT preview by hover-scrub** before committing, watching the scopes move (18:31, 18:34).

### ENGINE: what a headless auto-grader should adopt
- **Scale guards are confirmed and load-bearing** — bake these into `measure.py`/`correct.py` neutral checks: Offset neutral = 25.00 (NOT a lift), Gain = 1.00, Lift/Gamma = 0.00, Contrast = 1.000 @ Pivot 0.435, Saturation/Hue = 50.00, Soft Clip 50.0/50.0, Blur Radius 0.50, RGB-Mixer identity diagonal. Any value off these = a real move (confirmed across dozens of frames).
- **Adopt the CST-sandwich pipeline as the canonical node order** in `correct.py`/`stylize.py`: input transform → NR → highlight recovery → exposure/balance → saturation/color-separation/density → light shaping → look/LUT → output transform. Do ALL creative work in the wide working space (DWG/Intermediate), apply the gamut→Rec.709 transform only at the tail (12:32, 24:30, 26:22).
- **Color-managed-first**: default to DaVinci-WG/Intermediate working space, Output Rec.709 Gamma 2.2 (web) — make output gamma a parameter (2.2 web / 2.4 broadcast) (08:21, 16:08, 16:30). For `tonemap.py`: CST Tone Mapping Method = DaVinci, Adaptation = 9.00 is the demonstrated default (20:48, 21:24).
- **Per-source input-color-space mapping table** for `luts.py`/`correct.py`: support Apple Log (with Rec.2020 primaries), F-Log/F-Log2, D-Log-M, BM Film Gen 5, ARRI, Rec.709 → normalize each to the working space before grading (14:47, 09:08, 17:38).
- **Balance via the Offset (master/global) wheel, not per-wheel fights**: small Offset shifts around 25.00 do white-balancing (e.g. 25.71/24.47/23.45 = warm push); equal-channel Offset (e.g. 42.55×3) is a pure luminance lift (03:48, 14:56). `correct.py` should expose an Offset-style global trim distinct from lift/gamma/gain.
- **Contrast-around-pivot is the core exposure move**: Contrast 1.16–1.18 @ Pivot 0.435 is the demonstrated working range; pair with Gamma midtone lift + Gain highlight pull for shaping (21:34, 22:18, 24:44).
- **Default scope contract for `scopes.py`/`measure.py`**: RGB Parade and Histogram on a 0–100 (IRE-style) scale; Vectorscope for chroma/skin-line check. Targets seen: full-range distribution roughly 5–95 with no crushed blacks, watch for highlight clipping at 100 on backlit shots.
- **Broadcast-safe + Tetrahedral LUT interpolation** as engine defaults: enable broadcast-safe clamp (IRE ~20–120 [flag: low-bound 20 vs −20 ambiguous across frames]) and use tetrahedral (not trilinear) 3D-LUT interpolation for accuracy (16:51, 16:57, 18:43).
- **Frame-rate conform before matching** in any multi-source `match.py` pass — normalize all clips to one project rate first (09:50-10:23).
- **Shot-matching primitives for `match.py`**: support reference-still comparison (image-wipe equivalent: diagonal split + alpha-blend overlay) and ColorChecker-chart auto-match (X-Rite ColorChecker Classic) (21:14-21:27, 23:32).
- **LUTs are creative-look-only at the tail, never the conversion**: in `luts.py`, treat a creative LUT as a node late in the chain (Look stage), and do source→working conversion with a proper color-space transform, never a baked log→709 LUT in node 1 (25:58, 26:02, 26:22).
