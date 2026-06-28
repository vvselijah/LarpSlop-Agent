## mullins-grading-philosophy — Mitchell Mullins - Color Grading Mastery philosophy

**Source:** DaVinci Resolve Studio 19. Two pillars: *corrections* then *look development*. All footage RED-originated log (REDWideGamutRGB / RED Log3G10). Grades inside DaVinci Wide Gamut / DaVinci Intermediate (DWG/DI), transforms to Rec.709 only at output.

### Project / color-management setup (do this first)
- Timeline: UHD 3840×2160, 24 fps, 10-bit, square pixels; Video Monitoring 1080p 24p, Dual-link SDI, **Video (legal) data levels** (02:37).
- Color science = **DaVinci YRGB** (not ACES/managed); Timeline color space = DWG/Intermediate; **Output = Rec.709 Gamma 2.2** — he switched off his old 2.4 default ("for the longest time I used to work in Rec 709 gamma 2.4," 02:59).
- **No baked grading LUTs** — Input/Output/Video-monitor LUT all "No LUT selected"; only a viewer-side `CXC macOS Viewing Transform v1.3` to grade accurately underneath without rendering it in (03:25–03:39).
- **3D-LUT interpolation = Tetrahedral** (not trilinear); Broadcast-safe IRE −20–120 (03:39, 04:15, 32:46).

### The CST "sandwich" (core philosophy)
Wrap the grade between an input CST and output CST so all work happens in one wide-gamut space (06:44, 07:43):
- **Input CST (DWG node 01):** In = REDWideGamutRGB / RED Log3G10 → Out = DaVinci Wide Gamut / DaVinci Intermediate; Tone Mapping = DaVinci, Adaptation 9.00, Gamut Mapping = None, White-Point Adaptation on (06:10, 55:46).
- **Output CST (REC709 node, last):** In = DWG / DI → Out = Rec.709 / Gamma 2.2; DaVinci tone-map; at 28:48 Gamut Mapping = **Saturation Compression, Knee 0.800, Max 1.000**; Forward+Inverse OOTF + White-Point Adaptation on (10:46, 28:48).
- Grading in DWG means even maxed RGB-mixer/sat moves stay "a workable image" — the wide container holds data instead of clipping (10:36; sat auto-dropped 50→48.55).

### The canonical 12-node tree (broad-to-fine; "about as many nodes as I'd ever use," 26:45)
Top row: **01 DWG → 02 HDR Exp → 03 Lin Bal → 04 Con → 05 Sat → 06 Matrix**
Bottom row: **07 Split Tone → 08 HSV Hue → 09 Post Con → 10 HK → 11 Texture → 12 REC709**
(26:45, 36:28, 47:00, 54:15, 63:34). Each node = a named "point of contact." Tree is camera/look-agnostic — only the LUT node changes (64:18). Quick-grade path = 2–5 nodes: CST-in + 1 look LUT + tweak + CST-out (60:48, 65:34).

### Demonstrated parameters (with mm:ss)

**Log-wheel neutral baseline (memorize):** Contrast **1.000**, Pivot **0.435**, Lo Range **0.333**, Hi Range **0.550**, Offset **25.00/25.00/25.00**, all wheels 0.00, Saturation **50.00**, Hue **50.00** (02:29, 04:15, 60:01).

**Exposure — use multiply, never additive Offset:**
- HDR "Global" wheel exposure is the broadest exposure control: nudged −1.49 (14:06), +1.96 / +0.45 / +0.40 (15:51, 15:48, 15:57) — highlights compress gently into rolloff vs hard-clipping at 1023.
- Lifting Offset to ~49.13/49.15/49.15 raises the black floor (perceived exposure up, 14:44); **dropping Offset to ~5.65 crushes data off the bottom edge** (16:09) → he resets to 25 and states he'd "personally never adjust exposure" with Offset (16:15). Rule: exposure = gain/multiply; Offset = additive lift only.

**Contrast around Pivot (pivot = the key param):**
- Default Pivot **0.435** = where 18% middle-gray lands in log (NOT 0.5) — proven with a `MONO-MIDDLE-GRAY-v1.0` DCTL (Middle Gray 18.0, 21 linear/exp steps) reading low on the waveform, below the 512 center line (21:05–21:52). He sets Pivot at the image's middle-gray, judging luma in monochrome.
- Contrast 1.724 @ Pivot **0.934** = expansion biased into shadows (20:34); Contrast 1.724 @ Pivot **0.374** = pushed into highlights, shadows protected (20:41). Low pivot → highlight expansion / shadow protect.
- Working contrast moves: 1.318 (23:22), reset 1.000 (23:29), 1.130 @ Pivot 0.336 +Lift 0.02 (58:10), 1.352 @ Pivot 0.320 +Lift 0.04 under-LUT (46:40).

**Balance:** Offset master raised 25→33.65 to shift middle-gray warm (24:49). Linear white-balance lives on the "Lin Bal" node.

**Saturation:** DaVinci default = **50.00** (unity) — treated as the *blunt* instrument vs targeted matrix/HSV/ColorSlice (29:04). HDR Global Sat trimmed to 0.58 on the widescreen grade (61:40).

**Matrix / channel mixing (node 06):** RGB Mixer at identity (R 1/0/0, G 0/1/0, B 0/0/1) with **Preserve Luminance ON, Monochrome off** = luma-preserving 3×3 (10:20, 32:12, 34:05). Same math as the `Tetrainterp`/Tetrahedral DCTL identity matrix (32:52, 58:55). ColorSlice global Sat pushed to 1.42 (58:31).

**Curves:** Contrast done as a **gentle near-linear luma curve with a soft toe**, not a hard S; Soft-Clip (Low/Low-Soft/High/High-Soft) used to knee extremes instead of hard-clipping (11:10–11:15).

**Secondaries / skin:**
- Hue-vs-Hue: Input Hue 316.63 → Hue Rotate +17.89 on the orange/skin region (48:45).
- Skin via ColorSlice "Skin" vector + `TetraInterpHSV` DCTL: small **Red Hue +0.101→−0.054, Red Sat +0.116, Red Value −0.163** to keep skin natural / "see the blood under the skin" (49:31, 49:56).

**Texture (node 11, applied last, "use very sparingly"):**
- Film Grain: **Overlay** composite, Opacity **0.659**, Texture 0.750, Strength 0.620, Softness 0.234, **Saturation 0.000 (desaturated)**, weighted **Shadows 0.605 > Midtones 0.287 > Highlights 0.000** — grain confined to shadows keeps speculars clean (54:44). Evaluated at "Zoomed for Effect Viewing" 100%+ (53:53).
- Alternative: **Contrast Pop** FX instead of grain for a clarity/local-contrast look (55:04).

**HK (node 10):** `Nayatani_HK` DCTL — Helmholtz-Kohlrausch perceptual lightness correction (L-adapt 63.6, D65, method VCC, input gamut DWG). "Such a small difference, but when I A/B it…" — perceived-brightness correction for saturated hues (53:13).

**Looks / LUTs (his "secret sauce," applied late on their own node):**
- His **"Legacy LUT Collection"** — print-film emulations organized per-camera-gamut: 1 DWG, 2 ARRI (ARRILogC3→Rec709), 3 RED, 4 Sony, 5 Canon, 6 Blackmagic, 7 Panasonic, 8 Nikon, 9 DJI, 10 Fuji (45:59, 57:06, 63:42).
- Named .cube looks: **Terra, Sol, Pyre, Nova, Helios, Ember, Dusk, Bloom, Aether** (all `_DWG`/`_RED`/`_ARRIC3_709`). Favorites used: **Terra** (46:26), **Nova_RED** one-click on widescreen ("absolutely incredible," 60:54), **Sol_DWG** as finishing look (52:55).
- A single CST can itself create the film-print response: adding one CST turned the linear ramp's straight parade into a **soft S — lifted toe + rolled-off shoulder** (no hard clip at 1023); 2383-style print looks = warm-biased S-curve with raised black + soft shoulder (43:45, 44:10, 44:24).
- LUTs sit downstream of balance so primaries stay editable underneath (46:30, 46:40). Grade copy/pasted across shots in a scene (55:46).

### Scope discipline
- Identity/linear ramp → three straight diagonal RGB-parade traces; any look's tone-curve effect = deviation from that diagonal (42:29, 42:50).
- Reads neutral gray as points on the **R=G=B diagonal of the 3D Color Cube** (Nobe OmniScope); chroma/split-tone = departure from that line (43:08).
- Verifies gamut containment on **CIE-xy** (image cluster must sit inside the Rec.709 triangle) + 3D cube (27:42, 32:58).
- Detects un-transformed log by a **lifted black floor + compressed mid band** ("milky"); fix via input CST, never brute lift/gain (04:29, 04:29).
- Skin-tone gut-check before committing contrast (16:36).

### Distinctive opinions
- Output **Gamma 2.2, not 2.4**, for delivery.
- **Never set exposure with the Offset wheel** — it crushes/clips data; use multiplicative (HDR/gain) exposure.
- **Pivot = scene middle-gray ≈ 0.435 in log, not 0.5.**
- Grade in **DWG/DI**, transform to Rec.709 only at the output bookend.
- He **doesn't split-tone** ("things that are already tested, tried and true… I don't split tone") — that node defaults off (42:04).
- Tetrahedral LUT interpolation everywhere; texture/grain "very sparingly."

### ENGINE: what a headless auto-grader should adopt
- **Operate in a wide working space**: input-CST camera-log → DWG/DI, do all ops there, output-CST → Rec.709/**Gamma 2.2** last. Prevents premature clipping.
- **Fixed broad-to-fine op order**: input transform → exposure → linear white-balance → contrast(pivot) → saturation → channel matrix → (split-tone, default off) → hue → post-contrast → HK perceptual → texture → output transform.
- **Exposure = multiply, not additive offset.** Gate against additive shadow-crush; prefer a soft highlight knee (shoulder rolloff) over hard clip at 1023.
- **Contrast pivot at ≈0.435 (log 18% gray), not 0.5**; expose a `--strength` (contrast multiplier ~1.1–1.7) and a pivot param (low pivot protects highlights, high pivot protects shadows).
- **Filmic tone curve = lifted toe + rolled shoulder** (raised black, no white clip) — implementable as a single S-shaped LUT/CST.
- **Saturation default = unity (Resolve 50)**; treat global sat as blunt — prefer a luma-preserving 3×3 channel matrix (RGB-mixer with Preserve-Luminance) and per-hue (ColorSlice/HSV) moves for targeted color.
- **Skin lobe**: tiny red-hue rotation + small +sat / −value to keep skin natural; keep on the ~123° I-line.
- **Looks = swappable .cube LUTs** keyed to detected input gamut (per-camera library); apply on a dedicated late node downstream of balance so structural grade stays editable; reuse one preset per scene (copy/paste).
- **Tetrahedral 3D-LUT interpolation**; output gamut-map via saturation-compression (knee 0.8).
- **Texture last, sparing**: overlay-blend desaturated grain (~0.66 opacity) weighted into shadows>mids, zero in highlights.
- **Scope-driven verification**: ramp→diagonal parade as the baseline; flag lifted-black/compressed-mid = un-transformed log; check CIE-xy containment inside Rec.709 and R=G=B-diagonal neutrality in the 3D cube.