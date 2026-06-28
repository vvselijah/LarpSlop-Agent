## 2hr-beginner-course — How To Color Grade for Beginners (2hr)

DaVinci Resolve Studio 19 · "DaVinci Resolve Starter Powergrade" (DRSR, free from meliorstudios.com). The whole course is built around a prebuilt CST-sandwich node tree applied from the Gallery, then taught node by node.

### Project / Color Management setup (00:19–01:27)
- **Color science:** DaVinci YRGB; "Use separate color space and gamma" ON (01:21).
- **Timeline color space:** DaVinci WG/Intermediate; **Output:** Rec.709-A (01:21, 01:27). → grade in wide-gamut, deliver Rec.709 = CST sandwich.
- **Project format:** 3840×2160 UHD, 24 fps timeline + 24 fps playback, **10-bit** depth; video monitoring 1920×1080 24p (01:24).
- 3D LUT interpolation Trilinear; no input/output/monitor LUT loaded.

### The DRSR node tree — canonical build order (03:04, 03:47, 07:38, 63:10, 75:45)
Serial backbone with a parallel secondary block and a parallel adjustment/window stack:

`01 CST in → 02 Exp/bal → 03 Contrast → 04 Sat → [05 background / 06 2nd obj / 07 Main obj] (parallel, merged by layer mixer) → 09 Global → {10 ADJ1, 11 ADJ2, 12 ADJ3} + {13 PW1, 14 PW2, 15 PW3} → 17 Final look → 18 Fine Tune → 19 Film grain → 20 CST out → 21 Sharpening`

(Early frames show grain absent; by the finished tree at 63:10 the order is locked **Film grain (19) → CST out (20) → Sharpening (21)** — grain before output transform, sharpen dead last.) Texture sub-nodes also seen labelled Grain/Dust/Den+Sub (04:04).

### Identity / neutral defaults (the zero state) — 02:03, 03:22
Lift/Gamma 0.00, **Gain 1.00**, **Offset 25.00**, **Contrast 1.000**, **Pivot 0.435**, **Saturation 50.00**, Hue 50.00, **Lum Mix 100.00**, Color Boost/Shadows/Highlights 0.00, curve = straight 45°. Parade graticule 0–1023 (128 steps).

### Input transform — CST in (07:06)
Per-camera: Input **Canon Cinema Gamut / Canon Log 3** → Output **DaVinci Wide Gamut / DaVinci Intermediate**; Tone Mapping = DaVinci, Adaptation 9.00; Gamut Mapping None; White Point Adaptation ON.

### Demonstrated parameter moves (with timecodes)

**Contrast / pivot**
- Contrast → **1.170**, Pivot 0.435 (11:23).
- Contrast 1.106, **Pivot raised to 0.702** to protect highlights while darkening mids (12:11).

**Saturation**
- Global sat raised **50 → 62** (~+24%) (12:52).
- Sat lowered to **44** for skin work (22:47, 30:45).
- Cool look: global sat **38.60** (38:16).
- Film/cinematic desaturation: sat **32.80** (~0.66× neutral; Lum Mix kept 100 = luma-safe) (55:02).

**Offset (whole-image tint)**
- Shadow-floor lift: Offset 29.10 across RGB to keep blacks off 0 (11:02).
- Blue background push via Offset (B raised) (26:00).
- Green film tint: Offset R 24.42 / G 25.15 / B 24.42 (55:25).

**Channel gain (looks)**
- Cool "bluey-greeny": Gain 0.82/0.90/1.03, sat 38.60 (38:16).
- Region blue push via gradient window: Gain 0.77 all ch (40:49).

### Scope targets / reading (the recurring discipline)
- **Parade is the balance tool** — "whatever you see is copying what the image is doing" (35:30–35:34); equalize per-channel highs/lows toward neutral; green-dominant foliage frame counter-graded.
- **Clip guard both ends:** keep highlights off the 1023 ceiling and blacks off the 0 floor — "clipping = you've lost all information" (10:55, 11:02). Target = full 0–1023 spread, no channel pinned (05:54, 06:05).
- **Vectorscope** to validate skin lands on the skin line and to read look direction (lower-left lobe = cool/teal) (21:45, 40:03).

### Secondaries — qualifiers, windows, masks
- **Skin HSL key:** Hue Center ~31.7, Width ~17.3, Soft 3.2, Sym 50; Sat Low 0.7 / High 3.4; **Luminance 54–63**; Matte Finesse Blur Radius 8.6, Denoise 4.9, Morph Shrink (21:38, 38:36). Widen Width→22.1 + raise softness "so it's not as harsh" (39:02).
- **Shirt/jacket key:** Hue Center ~91 (blue/cyan band) vs ~32 skin band (24:19, 24:38).
- **Blue sky/water key (iPhone shot):** Hue Center ~92.3, Width 16.8, Lum 56–66; Matte Blur Radius 19.5, Denoise 5.9 (83:41).
- **Matte preview** via Shift+H to inspect the binary key; minus-eyedropper erodes; Shrink/Denoise = morphology (15:24, 19:42).
- **Negative example (why mask):** unmasked magenta Offset (49.76/16.86/28.27) tints the whole frame (23:48).
- **Power windows:** ellipse/rect/polygon/gradient with Transform Pan/Tilt/Rotate + Softness (17:38). Gradient window example: Pan 71.22 / Tilt 52.02 / **Rotate 87.05** (near-vertical ramp), Soft1 17.52 (40:49). Window **tracking** = per-frame affine pan/tilt/zoom/rotate; clear track before re-tracking (20:18).
- **Magic Mask (Object)** face isolation as a qualifier substitute (20:32).
- **Vignette** = circular PW; **Key Output Invert** flips selection (white = selected); darken surround OR brighten subject (keep lift single-digit % to avoid halo) (42:08–42:52).
- **Teal-and-orange separation:** orange skin key + blue-offset background = complementary split (26:40).

### Look tools (curves + per-hue)
- **Master Custom curve** is the main contrast tool — gentle S, 3 control points (shadow/mid/highlight thirds), pivot ~0.435; Soft Clip section rolls off highlight/shadow knees (32:12, 34:13, 54:44).
- **Lum vs Sat** curve = saturate by brightness (protect blown highlights) (33:12).
- **Hue vs Hue** = piecewise hue remap; e.g. Input Hue 325° rotated +24.73° (48:27).
- **Color Warper** (HSP) hue/sat mesh warp targeting one hue sector — control point Hue 0.76 / Sat 0.69 / Luma 0.50 (47:18–47:45).
- **ColorSlice (6-vector: Red/Skin/Yellow/Green/Cyan/Blue/Magenta)** for per-hue sat + **Density/Den.Depth** ("color density" — richer than flat global sat). Den.Depth raised to 0.62; **Skin vector +0.35** to "fill in the skin ever so slightly" (31:52, 44:38, 46:10).

### Face Refinement (AI face node) — 49:24–52:44
Detect Faces → Show Overlay → Effect Strength 1.0. Distinctive moves:
- Skin Texture **Amount 0.523, Scale 0.109** = gentle smooth (keep detail, "not plastic") (49:47); or **Amount −0.500** = ADD grit/character (50:19).
- Skin Grading face-only **Contrast 0.612**, **Midtone −0.426** (50:25–50:42).
- **Eyes › Brightening** lifted to 1.0 then backed to **0.163** — "many small adjustments, don't overdo it" (51:37–52:21).
- Per-feature sub-masks available: Lips/Teeth/Cheeks/Forehead/Chin/Eyeshadow/Blush (52:44).

### Film grain (texture, near-final) — 56:38–63:00
- Free path: drop a Melior 16mm/35mm grain plate on a track above footage, Inspector › Composite Mode = **Overlay @ 100%** (raw plate is ~50% grey + noise) (56:38–57:52).
- Studio FX path (node 19): preset **16mm** → Composite **Overlay**, Opacity 0.500, Saturation 0.000 (monochrome), Grain Size 0.660, Strength 0.149, Softness 0.298 (58:59). "Rougher" preset **16mm Archival Print** = smaller Grain Size 0.273 + higher Strength 0.341 (59:18).
- Final settled (Custom): Size 0.357, Strength 0.380, Softness 0.209; **luma-weighted Advanced** Shadows 0.357 / Mids 0.535 / Highs 0.500 (keep shadows clean), per-channel R/G/B 1.0 (62:14–62:58).
- Always judge grain at full res; grain is the most GPU-expensive node (60:35, 61:03).

### Sharpening (final node 21) — 64:58–65:48
- Done via **Blur palette**: Resolve sharpens when **Radius < 0.50**. Settled **Radius 0.48**, H/V Ratio 0.50, **Scaling 0.64** (wide spread).
- Distinctive: widen Scaling (0.35→0.64) **for social-media compression resilience** — light strength + wide spread beats a tight aggressive radius (65:17).
- Hard rule: **sharpen AFTER grain** ("the grain looks a little better as well") (65:37).

### Delivery (65:59–75:43)
- Deliver › Custom Export: **MP4 / H.264**, hardware accel ON, Resolution = Timeline (3840×2160), Frame rate = Timeline (24 fps), Quality Automatic.
- **In/Out range** export (I/O keys) — single clip or widen to chain clips into one continuous span; ~2.5s example (67:29–67:42).
- **Vertical reel:** Project Settings › "Use vertical resolution" flips the timeline to portrait (1080×1920) (71:45–71:57).
- Lock output fps to source fps — no frame-rate conversion (72:20).
- Advanced: Color Space Tag / Gamma Tag = "Same as project"; subtitles via **Burn into video** (toggleable) (73:48).
- Delivered master validated in Finder: 3840×2160 H.264 + AAC MP4, Rec.709 (1-1-1) tag (75:43).

### Distinctive opinions
- Apply the whole saved grade from the Gallery (right-click › Apply Grade) and transplant the entire node tree onto new footage, incl. iPhone XR 4K24 (77:46).
- Prefers **darker, desaturated, filmic** imagery (54:44, 55:02).
- "**Many small adjustments**" philosophy — conservative values everywhere.
- **8-bit phone footage caution:** don't overpush secondary color or it "breaks up" (banding/posterization) — cap secondary moves on low-bit-depth source (84:11).
- Parametric mask+adjustment stacks are preferred over a baked LUT because "everything is completely adjustable" (40:55).

### ENGINE: what a headless auto-grader should adopt
- **Fixed op order = the DRSR tree:** CST-in (per-camera) → exposure/balance → contrast(pivot) → saturation → secondaries (skin + object + background, parallel/merged) → global → adjustment + power-window layers → look → **grain → CST-out → sharpen**. Grain before output transform; sharpen last.
- **CST sandwich:** linearize/transform camera → DWG-Intermediate working space → grade → transform to Rec.709-A on output. Assume **10-bit / UHD / 24 fps** working container.
- **Identity constants** to reset to: contrast 1.0, pivot 0.435, sat 50, lum mix 100, offset 25.
- **Contrast = S-curve around pivot** (default 0.435; raise pivot ~0.70 to protect highlights). Expose contrast factor + pivot per shot.
- **Auto-balance from RGB parade:** measure per-channel low/high on 0–1023, equalize toward neutral; **clip guards** both ends (no channel at 0 or 1023).
- **Skin keyer = narrow HSL band:** hue ~32°, low sat, **luma 54–63%**, soft edges + mask blur/denoise; validate skin lands on the vectorscope skin line; keep sat luma-safe (Lum Mix 100).
- **Looks as channel-gain recipes:** cool = R-gain <1, B-gain >1, global sat ~38; film = sat ~33 + tiny green offset.
- **Per-hue control (ColorSlice/6-vector)** with a dedicated **Skin** band; small **density** weighting reads richer than flat sat. Skin sat boost ~+0.35, kept small.
- **Grain = monochrome (sat 0) Overlay noise plate** at ~50% opacity, mid-weighted by luma (shadows<mids), size ~0.36 / strength ~0.38 / softness ~0.21; pre-render a tiled plate once (per-frame regen is the heaviest cost).
- **Sharpen = unsharp mask, strength = (0.50 − radius), wide spread (~0.64) for compression resilience**, applied after grain.
- **Bit-depth guardrail:** cap secondary saturation/offset magnitude on 8-bit inputs; detect banding.
- **Look = a serializable preset** (the .drx graph) reusable across clips/cameras; expose a named look/LUT library (DigiFilm 16mm/35mm, etc.).
- **Delivery target:** MP4/H.264 + AAC, hardware accel, timeline res/fps, Rec.709 (1-1-1) tag; optional portrait 1080×1920 flag; trim by in/out timecodes; optional subtitle burn-in.