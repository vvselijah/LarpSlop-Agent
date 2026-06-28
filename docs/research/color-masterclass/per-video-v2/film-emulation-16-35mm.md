## film-emulation-16-35mm — Emulating 16mm/35mm Film

**Authority's thesis (00:34–01:03):** The film look is multi-factor, not one LUT — it stacks negative stock + exposure + print process (00:51). Presents **four methods** of rising fidelity (01:03): (1) DaVinci's built-in FPE LUTs, (2) Juan Melara's Kodak 2383 PowerGrade, (3) FilmVision PowerGrade+LUT, (4) Dehancer 500T. Core conviction: **build film emulation as one labeled, ordered, toggle-able node graph, then save it as a portable PowerGrade still** — not per-shot grading.

### Canonical node order (the deliverable graph)
Two equivalent layouts are shown:

**FilmVision full tree (02:57, 06:02, 06:21):**
`CONVERSION → GRAIN → HALATION → PRO MIST → [GSO/CDG WARMTH · COLOR DENSITY · VIGNETTE] → [DUST · GATE WEAVE · FILM BREATH] → EXPOSURE → WHITE BALANCE → SATURATION → [FADE · WHITES · BLACKS] → LOOKS → LUT`
(node numbers seen: EXPOSURE 11, WB 12, SAT 13, FADE 14, LOOKS 17, LUT 18.)

**Self-built FPE chain — 9 serial nodes (07:40–13:33):**
`SOFTNESS(01) → GRAIN(02) → HALATION(03) → VIGNETTE(04) → DUST(05) → EXPOSURE(06)+WB(07) [parallel] → CST(08) → LUT(09)`
Rule he enforces: **input CST first, texture in the middle, primaries + look LUT last** (06:02). LUT/PowerGrade is a **swappable terminal node** (16:22).

### Concrete demonstrated parameters (number @ mm:ss)
**Project settings**
- Color science **DaVinci YRGB**; 3D LUT interpolation **Trilinear**; Broadcast safe **-20–120** (02:31).
- LUT install = Project Settings ▸ Color Management ▸ **Open LUT Folder**, drop pack in subfolder, **Update Lists** + Save (02:31, 02:42).
- PowerGrade applied via Gallery still ▸ right-click ▸ **Apply Grade** (02:57); saved back as a Gallery still ("L508 FilmVision PG_1") to make it portable (06:21).

**Input transform — CONVERSION node (Color Space Transform OFX)**
- FilmVision CST (03:13): In **Rec.2020 / FujiFilm F-Log** → Out **ARRI Alexa / ARRI LogC**; Tone Mapping **Luminance Mapping**, Adaptation **9.00**; Gamut **Saturation Compression**, Sat Knee **0.900**, Sat Max **1.000**; White Point Adaptation **ON**.
- FPE-method CST (08:39 → 09:12): In **Rec.2020 / FujiFilm F-Log** → Out **Rec.709 / Cineon Film Log**; Tone Mapping **DaVinci**, Adaptation **9.00**, Gamut **None**. Print-emulation LUTs expect a **Cineon film-log** container (notes "weird artifacting" 09:12).
- **No-CST-profile fallback (DJI Osmo Pocket 2):** use a found conversion LUT **"d2x709"** (DJI→Rec.709) on the CONVERSION node via right-click ▸ LUT (06:33–06:59).

**Exposure / WB primaries (10:00)**
- Default neutral state: Gain **1.00**, Offset **25.00**, Contrast **1.000**, Pivot **0.500**, Sat **50.00**, Hue **50.00**, Lum Mix **100.00** (07:41).
- Exposure move: drop **Offset**, raise **Gamma** slightly, pull **Gain 25.00 → 13.25** (R/G/B) to bring highlights into range (10:00).

**Halation (CST-sandwich, built in LINEAR light) — 11:36–12:26, 17:56**
- Branch = **SOFTNESS + GRAIN** parallel nodes, Composite Mode set to **Add** (11:51).
- CST #1: In **Use timeline / F-Log** → Out **Linear** (12:06–12:09) — do the highlight blur in linear.
- CST #2 (inverse): In **Linear** → Out **F-Log** (12:16) — re-encode after blur.
- FX used: **Gaussian Blur + Glow** for the bloom, separate **Film Grain** (Resolve FX Texture); Dehancer Pro 4.0 noted as alt (11:36).
- Highlight mask = custom Luma curve **flat ~0 through mids, steep ramp only in top ~20%** (12:59, 17:58). Halation strength is **per-clip tunable** via the node's Key Output Gain (17:56).

**Film texture nodes**
- **16MM GRAIN** compound = three serial passes **SOFTNESS → DETAIL → GRAIN**; SOFTNESS Blur palette Radius R/G/B **0.50**, H/V Ratio **0.50**, Scaling **0.25** (neutral default, diverges for 16mm vs 35mm) (03:59).
- **DUST = Film Damage (Resolve FX Revival)** (14:17): Film Blur **0.150**, Temp Shift **0.250**, Tint Shift **-0.100**; Vignetting Focal **0.100** / Geometry **0.250**; Dirt (Changing) Density **2**, Size **1.758**, Blur **0.245**, Seed **5**; Scratch1 Position **0.159**, Width **0.044**, Strength **0.500**. Then simplified to **dirt only, color = white, Density = 1** (14:31).

**Vignette (13:33–13:43)**
- Resolve FX **Vignette** (Stylize): Operating Mode **Basic**, Shape Size **0.500**, Anamorphism **1.780**, Softness **0.500**, Color **black**.
- Power Window alt: **Circle** shape, Opacity **100.00**, Soft 1 ≈ **2.07** (13:43).

**Tone curve auditioning (12:59–13:17)** — A/B'd three luma curves: linear identity → aggressive near-vertical **crush hockey-stick** (flat floor + steep highlight-only rise) → reverted to the **gentler straight diagonal**. Verdict: **default to the subtle curve; the extreme crush "won't work with every type of footage"** (13:10).

**LOOKS compound (05:50, 07:08)**
- Three look nodes in series: **WARM LOVE → CINE GREEN → TUNGSTEN BLUE**.
- **Each look node's Key Output Gain = 0.500** = looks applied at **50% strength by default** (05:50). Per-clip tunable (Tungsten Blue bumped to **0.590** on the warm DJI sunset, 07:08).
- Looks are **skin-protected** color casts (green pushed to shadows/highlights, skin lobe left warm) (05:43–05:45). Look choice is **scene-dependent** (cool Tungsten Blue for warm/tungsten scenes).
- The "film LUT" **decomposes** into discrete nodes — Blue&Sat → Luma → Blue → Curve → Shadow → Luma — i.e. hue-vs-sat split-tone + luma-windowed curve + shadow tint, **not an opaque 3D LUT** (16:24).

**Print-emulation sources cited**
- **Juan Melara Kodak 2383 PowerGrade** — "Kodak 2383 D65/D55 Print Film Emulation LUT, fully editable PowerGrade, pay-what-you-want" (15:48). Catalog also lists camera→Alexa conversions (P6K2Alexa etc.) + Kodak 2393 (15:24). **2383 signature = warm highlights / cool-teal shadows** (15:22); **D55 reads cooler than default** (22:46).
- **CinePrint16** (Tom Bolles, $59.99) = 16mm reference: heavier grain, green-yellow midtones, softer print (15:40).

**Scope / waveform targets (0–1023 scale)**
- Flat log source = trace compressed mid-range with **lifted floor ~256, nothing near 0 or 1023** → flags need for input transform (02:15, 16:13).
- Graded film tone = **lifted milky toe ~80–120, rolled shoulder below clip, mids ~250–512** (16:15, 18:12). Watch for **highlight clipping** when a contrast preset pins a sign/sky to ~1023 (06:38, 16:22).

### Distinctive opinions / techniques
- Build halation in **linear light via a symmetric CST sandwich** (linearize → Gaussian-blur+glow → re-encode); composite the glow with **Add** blend mode.
- Looks ship at **50% Key-Output opacity** so one "look intensity" knob = the mix factor.
- Print LUTs need a **Cineon log container** upstream, not Rec.709 video.
- Honest framing: shows all 4 methods side-by-side (22:37) so the video "isn't just an ad" for his own PG+LUT; differentiator between methods is **highlight roll-off + print-LUT white point (D55/D65)**.
- **Film look = preserve, don't neutralize, mixed-light color casts** (warm highlights / cool-green shadows held intact) (23:07).
- Final deliverable adds a **film-gate matte** (rounded/frayed black border + corner light-leak/halation) as a **compositing overlay**, separate from the grade (15:02, 18:37).

### ENGINE: what a headless auto-grader should adopt from THIS video
- **Pipeline as ordered, toggle-able stages:** input-CST → softness → grain → halation → vignette → dust → exposure/WB → saturation → look LUT → print/output LUT. Serialize the whole chain as one reusable preset.
- **Per-camera input transform first:** parametric CST (e.g. F-Log/Rec.2020 → Cineon or ARRI LogC); fall back to a **camera-specific log→709 conversion LUT** (DJI d2x709) when no IDT exists. Detect "needs transform" from a **compressed lifted-floor waveform**.
- **Halation done right = linearize (CST) → red-weighted highlight blur+glow → re-encode**, masked to the **top ~20% luma** (curve ~0 below a high knee); expose intensity as a scalar (default ≈ Key Gain 0.5, scale per scene).
- **Film texture = three separable passes** (lowpass softness blur ~0.50, hi-freq detail, additive grain) + procedural **dust/scratch sprites** (white, density-controlled) — 16mm = heavier than 35mm.
- **Look = a 50%-opacity blend** of a skin-protected split-tone (decomposed into hue-vs-sat + luma-windowed curve + shadow tint, not an opaque cube); pick the look by scene white balance.
- **Print-LUT illuminant (D55/D65/D60) is a selectable parameter.** Tone curve = lifted toe (~+0.05–0.10) + rolled shoulder, desaturated, warm bias; default to a gentle contrast curve (aggressive crush is opt-in, footage-gated). Guard against highlight clipping at 1023.
- **Film-gate border/grain** is a final **compositing overlay**, not a grade op.