## frenchie-masterclass — Frenchie - Pro Colorist Reveals all (MASTERCLASS)

**Tool/app:** DaVinci Resolve Studio 19 (Public Beta), Color page. Grade name on title bar: "HEARTSUPPORT LOOK". Discipline: one purpose per node, every node labeled.

### Project color-management contract (06:12)
Set in Project Settings > Color Management before any grading:
- Color science = **DaVinci YRGB Color Managed**; processing mode = **Custom**
- Input CS = **Blackmagic Design 4K Film Gen 3** (project default); Timeline CS = **DaVinci WG/Intermediate**; working luminance = **HDR 1000**; Output CS = **Rec.709 Gamma 2.2**
- Limit output gamut to Output CS; Input DRT = DaVinci, Output DRT = DaVinci; resize in **Gamma**; graphics white = **100 nits**
- Checked: inverse DRT for SDR→HDR, white-point adaptation, color-space-aware grading tools
- Dolby Vision 4.0, mastering display 4000-nit P3 D65 ST.2084

This is the CST-sandwich: decode each camera → DWG/Intermediate → grade in HDR1000 → output-transform to Rec.709 G2.2.

### Node tree / workflow order (built + reused as a portable "look")
The finished HEARTSUPPORT graph, named nodes in build order (final form, 25:21):
`HDR (02) → BALANCE (04) → CONTRAST/CONTRA (06) → COLOR/COLOR A / HUES (03) → SPLIT TONE (01) → DENSITY (05/07) → FACE RE[finement] (07) → VIGN (09) → OVERLAY (11)`

Early in the build the split-tone + hue work sat on a **parallel branch** (`SPLIT TONE 01 → HUES 03`) feeding a layer-mixer alongside the serial `HDR→BALANCE→CONTRAST` backbone (07:41, 08:11, 17:56, 20:09); later passes flatten it into the serial chain above. Core principle: **the look lives entirely in the downstream nodes — primary wheels stay neutral on most clips; per-shot work is only white-balance correction.**

### Demonstrated parameters (value @ mm:ss)

**Input / interpret stage**
- Per-clip Input Color Space via right-click → Input Color Space; Rec.709 B-roll passes through unchanged, log clips get the CST (08:46–10:18)
- Failure case shown: Rec.709 source wrongly tagged Blackmagic Design 4K Film Gen 3 (log) → histogram goes choppy/multi-modal "weird"; correction = right-click → Input Color Space → Rec.709 (09:16, 09:22)
- Log detection cue = compressed mid-band waveform (~256–640), lifted black floor, low saturation, isolated black spike + thin highlight tail (09:34, 09:37)
- Output target = **Rec.709 gamma 2.2** (10:28)

**BALANCE node**
- Master **Offset** R/G/B = **19.93 / 19.93 / 19.93** (equal = neutral exposure/black-floor lift), called "~21" (11:12)
- Warmth via **Blue offset down B/Ofs = −0.01** (subtract blue, not the temp slider) (12:19)
- Light/midtone wheel **Sat = −0.04** (slight midtone desat) (14:39)

**CONTRAST node**
- Dedicated node after BALANCE; **Cont 1.000, Pivot 0.000** at default; shape via Custom Curves not the contrast slider (13:30, 15:25)
- Compare with **SHIFT+S** split-screen wipe while shaping (13:30)
- **Soft Clip Low 50.0 / High 50.0**, L.S. 0.0 / H.S. 0.0 — roll off highlights/shadows instead of hard clamp (constant 05:57, 15:25, 17:03)
- Per-channel curve work available (Green channel toggled active); subtle highlight knee ~700/1023 + slightly lowered shadow point for mild contrast (17:15, 17:55)
- Curves default linear (master/R/G/B Edit all = 100) until points pulled (05:57, 07:41)

**HUES — Color Warper (Hue–Saturation)**
- **Hue Resolution raised 6 → 16** for more control points (18:07, 18:13)
- Polar grid: hue = circumference, saturation = radius; pushed the blue/violet wedge outward (18:17, 18:18)
- Committed blue point: **Hue 0.41, Sat 1.15, Luma 0.50** — a +15% sat push on the blue hue bin, luma held (18:57)

**OVERLAY / texture nodes (post-mixer)**
- Node 07 = strong blend-mode layer (Hard Mix-style); dialed back via **Node Key → Key Output Gain = 0.133** (~13% strength, "134 is good") — uses key-output gain as the layer's opacity, not node opacity (19:29, 19:37)
- Node 08 = second blend layer set to **OVERLAY** composite mode, stacked after the 0.133 Hard-Mix node (19:50)

**DENSITY node (Color Slice palette)**
- Added in the look chain; **Pivot 0.435** (lowered midtone pivot to deepen/enrich) (22:18)
- Global **Sat 1.00 → 1.14** — explicit opinion: Color Slice saturation is **subtractive, not additive**, so it deepens colors rather than electrifying them ("makes a better image") (22:28, 22:33)

**VIGN — Power Window vignette (finishing)**
- Circle/elliptical window, feathered, darkens outside to make subjects stand out; added near-last (19:51, 20:07, 20:17)
- On street clip: Window Circle, **Size 52.96, Aspect 78.03, Pan 44.03, Tilt 48.56, Opacity 100.00, Soft 1 = 18.00** (20:49)

**FACE REFINEMENT node (terminal, after the look, before/with vignette)**
- DaVinci Face Refinement FX: **Effect Strength 1.000**; Skin Texture mode **Beauty Automatic**, Amount 0.000, Scale 0.500; Skin Grading Contrast/Midtone/Color Boost/Tint all 0.000 — deliberately restrained (no plastic skin) (25:21, 26:30)
- Show Overlay (face-track) on; used for under-eye/eye-bag cleanup as the last creative touch (27:01)

### Shot-matching (look held constant, only WB per shot)
"Correct-then-style": neutralize the source first, look is re-applied downstream.
- Warm-exterior crowd, very orange source → **Temp −90.0**, Tint 0, Offset 21.02, Gain 1.00 (24:49)
- Two-guys exterior interview → **Temp −130.0**, Lift 0.02, Offset 21.02 (23:47)
- HeartSupport banner daylight exterior → primaries fully neutral, **Temp 0 / Tint 0, Offset 25.00** (look is 100% downstream-driven) (24:53)
- **Cold-interior sub-look** (shared param block across interior shots): negative Temp + positive **Tint ~+12–14** (magenta to counter green skin) + black crush via Lift:
  - Eye ECU: Temp −344.0, Tint 3.15, Lift −0.10, Gamma 0.04, Gain 1.24, Offset 53.23 (24:04)
  - Girl-in-bed: Temp 66.0, **Tint 14.65**, Lift −0.08, Gain 1.18, Offset 53.23 (24:07)
  - Dark-lipstick ECU: Temp −150.0, **Tint 12.10**, Lift −0.08, Gain 1.12, Offset 53.23 (24:11, 25:03)
- Common across matched shots: **Contrast 1.000, Pivot 0.435** (the look's pivot), Sat 50.00, Hue 50.00, L.Mix 100.00

### Scope targets demonstrated
- Reference scope = **Waveform** on the 0–1023 (10-bit) scale (05:57)
- Graded festival B-roll: luma trace held ~256–768, **nothing pinned at 0 or 1023** (no crushed blacks / clipped whites), consistent with the engaged soft clip (05:57, 07:41 trace ~384–640)

### Distinctive opinions / techniques
1. **One purpose per node, every node named** — balance, contrast, hues, density, vignette, overlay each isolated; no stacking on node 1.
2. **Color-managed HDR1000 working space**, not raw log primaries — even the first node is named "HDR".
3. **Warmth via Blue offset (−0.01), not the temp slider** for the base look.
4. **Subtractive (Color Slice / "density") saturation** preferred over additive HSV gain — deepens instead of electrifies; the chroma-finishing move is +14% there, not on the primaries.
5. **Soft Clip 50/50** always on — never hard-clip.
6. **Correct-then-style:** neutralize each shot's WB first (often large negative Temp), keep the look chain identical downstream.
7. **Restrained Face Refinement** as the terminal node — skin cleanup last, very low amounts.
8. **Portable look:** middle-click copy the whole node graph to a new clip, then re-derive only balance from that shot's scopes (20:42, 20:53).

### ENGINE: what a headless auto-grader should adopt
- **Ordered, named stage pipeline (fixed):** input-CST → exposure/HDR → balance(WB) → contrast → hue-warp → split-tone → density → face-refine → vignette → overlay. One transform per stage.
- **Per-clip input detection:** classify Rec.709 (display-ready, pass through) vs log (compressed mid-band ~256–640 + lifted black floor + low sat → apply camera→DWG CST). Guardrail: never apply a log input-CST to display-referred footage.
- **CST endpoints:** decode camera → DaVinci WG/Intermediate @ HDR1000 → output Rec.709 G2.2.
- **Balance = master Offset add (~+20 on 0–100), uniform RGB; warmth = Blue offset down (~−0.01)**, not a temp control. Per-shot WB correction = Temp offset only, large negative for warm sources; cold-interior preset = −Temp, +Tint ~+12, Lift ~−0.08.
- **Soft-clip both ends (knee 50/50, tanh roll-off near 0 and 1023)** instead of hard clamp; validate output luma stays inside ~256–768 of 0–1023 (no pinning).
- **Contrast:** pivot-based; the look's pivot ≈ **0.435**.
- **Saturation = subtractive/density model** (darken-as-you-saturate, ~+14%), not naive HSV multiply; plus a targeted per-hue warp (blue bin ×1.15 sat, luma held).
- **Texture layer:** blend a strong composite (Hard Mix/Overlay) at ~0.133 opacity for subtle contrast/glow.
- **Vignette last:** feathered elliptical power window (store Size/Aspect/Pan/Tilt/Softness), radial luma falloff darkening edges.
- **Face cleanup terminal:** face-detect → under-eye mask → frequency-separation smoothing at very low amount, after the look not before.
- **Portable preset:** treat the look graph as reusable; re-derive only the balance stage per shot from its scopes.