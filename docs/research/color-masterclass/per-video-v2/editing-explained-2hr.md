## editing-explained-2hr — Editing Explained - 2hr EVERYTHING about Color Grading (FRAMES-ONLY, transcript unavailable)

**Tool:** DaVinci Resolve Studio (build ~18/19, dark UI; Color page Primaries - Color Wheels + Window/Tracker + Vectorscope/RGB-Parade scopes). Color-managed project ("Color Grading" timeline). Vertical 9:16 footage: a man on a bicycle in a park (TC 00:00:34;04), a woman in a green jacket interview (C0854.MP4, TC 00:00:11;19, multi-language audio/subtitle timeline), and a chrome water-tap/faucet b-roll. Teaching aids: Adobe Color web tool, Google Images reference searches, Dehancer Pro 6.0.0 film-emulation OFX, and slide/Zoom-class overlays. Scale-confusion guard applies throughout: Resolve Offset neutral = 25.00 (NOT a black lift), Gain neutral = 1.00, Lift/Gamma neutral = 0.00, Saturation neutral = 50.00, Hue neutral = 50.00, Lum Mix neutral = 100.00, Pivot default ~0.435.

### Workflow order
The colorist's repeated, demonstrated node structure (broad-to-fine, one task per node) across the interview clip (49:08, 51:26, 63:40, 64:36, 69:04, 72:48, 78:30, 91:18, 99:50):
1. **Node 01–02** — source / structural passthrough (neutral) (66:14, 70:24)
2. **Node 03 'Exposure'** — overall tone (66:00 sequence shows it precedes WB)
3. **Node 04 'White Balance'** — temp/tint correction; lives in Temp/Tint, wheels left neutral (66:00, 78:30, 87:10)
4. **Node 05 'Sat' (Saturation)** — saturation stage (51:26, 72:48)
5. **Parallel/layer-mixer block** (nodes 06/07/08 + 09 over 11/12/13/14 feeding a Layer Mixer) — windowed secondaries, keyed/tracked corrections (67:08, 70:04)
6. **Serial trim tail (nodes 16/17/18)** — final trims (69:04, 70:04)
- Dehancer Pro film-emulation OFX runs as its own dedicated node early in the chain (node 02 region), before the parallel correctors (70:18).

### Demonstrated parameters (number @ mm:ss)

**Cyclist clip — primary wheels**
- **Lift master -0.01 (R/G/B all -0.01); Gamma master -0.02 (all -0.02); Gain master 0.81 (all 0.81)**; Offset 25.00 (neutral); Contrast 1.000; Pivot 0.435; Mid/Detail 0.00; Temp 0.0; Tint 0.00 (00:34)
- **Highlight warm trim via Gain RGB only: Gain master 1.00, R 1.03, G 1.00, B 0.94** (raise red / lower blue); Lift+Gamma neutral; Offset 25.00 (00:40)
- Pivot 0.435, Mid/Detail 0.00 (header confirm) (00:42)
- All-neutral inspected node: Lift 0.00, Gamma 0.00, Gain 1.00, Offset 25.00, Pivot 0.435 (52:32)
- **Even pull-down with rectangle window: Lift -0.01 all, Gamma -0.02 all, Gain 0.88 all**; Offset 25.00; Pivot 0.435 (56:26)
- **Curve/pen window brighten: Gamma -0.01 all, Gain 1.07 all** (even highlight lift), Lift 0.00, Offset 25.00; Pivot 0.435 (59:42, 60:10–60:20)
- **Gain split (warm highlights): Gain Y 1.00 / R 1.00 / G 1.03 / B 0.94** (green up, master/blue down), Lift+Gamma neutral, Offset 25.00 (60:54–61:32)

**Green-jacket interview — primary wheels / header**
- **Lift 0.00/0.00/0.00/0.00; Gamma -0.01/-0.02/-0.01/-0.01; Gain 0.92/0.87/0.93/0.91** (green channel lowest 0.87); Offset 25.00 (49:08, 51:26, 63:40, 64:36)
- Header: Temp 0.0, **Tint 9.50** (toward magenta/green), Contrast 1.000, Pivot 0.435, Mid/Detail 0.00 (49:08, 51:26, 64:36)
- Lower row defaults: Color Boost 0.00, Shadows 0.00, Highlights 0.00, **Saturation 50.00, Hue 50.00, Lum Mix 100.00** (49:08)
- **Uniform Gain pull-down node: Gain 0.89 all**, Lift 0.00, Gamma 0.00, Offset 25.00, Pivot 0.435 (69:04, 69:06)
- White Balance node carries **Temp -560.0** (cool), Tint 0.00, wheels neutral, Offset 25.00 — the only non-neutral primary on that node (78:30, 87:10, 91:18, 99:50)
- In-window darken secondary: **Gamma 0.97 all, Gain 0.97 all, Mid/Detail -10.50**, Offset 25.00; Soft 1 0.00, Inside 3.90, Outside 2.28 (67:18, 68:04–68:44, 100:12, 101:38)
- Final secondary state: **Gain reset to 1.00 all; Offset nudged to 26.00/26.00/26.00** (+1 = tiny uniform lift via Offset) (102:34)

**Chrome faucet/tap b-roll**
- Clean before state: single node 01, all neutral (Lift 0.00, Gamma 0.00, Gain 1.00, Offset 25.00, Temp 0.0) (80:06, 86:58, 91:30)
- **Cool highlights via Gain RGB: Gain Y 1.00 / R 0.95 / G 1.01 / B 1.08** (red down, blue up) (92:32)
- **Burn region (linear window): Gain 0.46 all + Offset 6.80/6.80/6.80 (below 25 neutral = extra darken)** (93:00)
- **Dodge region (linear window): Gain 1.72 all, Offset 25.00 neutral** (93:56, 97:42)

**Other lamp/practical-light grades (interview room)**
- Gradient window darken: Gamma -0.01 all, Gain 0.83 all, Offset 25.00; Rotate -178.99, Soft 1 5.32 (69:42)
- Lamp-isolation circle window, wheels neutral on that node (69:26)

**Power Window geometry & softness**
- Cyclist circle→oval vignette: Size 50.00, **Aspect 18.72** (wide oval), Pan 65.43, Tilt 50.16, Rotate 0.00, Opacity 100.00, Soft 1 9.55 (53:46, 62:20)
- Cyclist rectangle, 4-edge feather: Size 50.00, Aspect 50.00, Pan 68.71, Tilt 59.37, Rotate 1.17; **Soft 1 4.86 / Soft 2 1.25 / Soft 3 1.25 / Soft 4 10.90** (56:26)
- Cyclist curve/pen window: Size 50.00, Pan 50.00, Tilt 50.00, Rotate 0.00, Opacity 100.00; **Soft 1 0.00, Inside 17.06, Outside 10.20** (59:42, 60:10)
- First window @00:34: Pan 28.28, Tilt 50.43, Rotate -89.80, Opacity 100.00, Soft 1 15.59 (00:34)
- Lamp circle window: Size 53.40, Aspect 60.13, Pan 45.22, Tilt 53.73, Soft 1 3.07 (69:26)
- Interview rectangle: Size 50.00, Aspect 50.00, Pan 50.00, Tilt 50.00; Soft 1/2/3/4 all 1.25 (67:04, 67:08)
- Faucet burn linear window: Pan 31.58, Tilt 50.20, Rotate -90.19, Soft 1 22.07 (93:00)
- Faucet dodge linear window: Pan 77.50, Tilt 48.92, Rotate 90.66, Soft 1 19.60 (93:56, 97:42)

**Scope readings**
- RGB Parade marked on 0–1023 (10-bit code-value) scale, gridlines 128/256/384/512/640/768/896 (63:56)
- Parade neutral graded shot: peaks ~768–896, bases lifted ~64–128, no clip at 1023, R/G/B roughly aligned (70:38)
- Parade on dark WB-node clip: traces bunched in bottom third (66:00)
- Vectorscope used to judge warm/skin direction: skin arm down the I-line toward orange, isolated orange blob = practical lamp, green/teal arm = green jacket / shadow separation (49:08, 52:32, 71:04, 71:06, 99:52)

**Edit-page Transform (distinguished from color geometry)**
- Interview clip reposition: Zoom 1.000, Position X 6.000 / Y 0.000, all rotation 0.000 (55:44, 99:48)
- Title/badge overlay: Zoom 0.590, Rotation 90.000 (78:54)

**Dehancer Pro 6.0.0 film-emulation OFX node (70:18)**
- Temperature Comp 0.0, Tint Comp 0.0; Defringe 50.0, Defringe Radius 50.0 (enabled)
- Film Profile = **Kodak Vision3 250D**, Push/Pull 0.000 Ev
- Expand: Black Point 0.00, White Point 100.0, Color Mode Normal
- Print: Profile Linear, Exposure 0.000 Ev, Tonal Contrast 0.0, Color Density 0.0, Saturation 100.0

**Adobe Color web tool harmony palettes (reference, NOT Resolve values)**
- Analogous (Blade Runner): #EB6C34 / #EBA834 / #EBB834 / #EB4C34 / #EBBE34 (+#EBB482) (81:30)
- Monochromatic green: #96BE75 / #829373 / #A2E868 / #606959 / #25331A (77:52)
- Monochromatic brown/skin: #C0785A / #966F5F / #EB7B46 / #6B5C56 / #413936 / #332722 (78:08, 80:14)
- Complementary (teal/orange): #00BAEB / #AB692B / #EB7201 / #328196 / #6B4F36 / #2B3C41 (82:44, 86:00)
- Split Complementary: #0070EB / #00EBCF / #EB7100 / #6B4F36 / #364F6B / #366865 (86:50); 2nd ex. #EBCB0C / #EB950C / #083CEB / #3B456B / #6B643B / #6B591B (87:28)
- Harmony rule list available: Analogous, Monochromatic, Triad, Complementary, Split Complementary, Square, Compound, Shades, Custom (77:08, 82:36)

### Distinctive techniques / opinions
- **One correction per labeled node, broad-to-fine.** Nodes are explicitly named Exposure → White Balance → sat, then a parallel/layer-mixer secondary block, then serial trim tail — a modular, self-documenting tree of ~18 nodes (49:08, 51:26, 64:36, 69:04, 72:48).
- **White balance belongs in Temp/Tint, not the wheels.** The WB node's wheels stay neutral; the entire correction is a Temp value (e.g. Temp -560.0 to cool a warm source) (66:00, 78:30, 87:10).
- **Grade lives in Gain + Gamma; leave Lift and Offset neutral.** Across nearly every primary node, Lift = 0.00 and Offset = 25.00, with the work done on Gain (highlight pull-down/boost) and small Gamma trims (51:26, 56:26, 69:04).
- **Per-channel Gain = white-balance-in-highlights.** Warm look = raise R / lower B in Gain (00:40); cool look = lower R / raise B in Gain (92:32); green-up warm variant (60:54).
- **Power Windows for focus points.** Demonstrates all four window types — rectangle (4-edge feather), circle→oval via Aspect (one-sided Soft 1), curve/pen freeform (Inside/Outside feather), and linear/gradient — and the matte/highlight view to verify the selection before grading (53:46, 56:26, 59:42, 60:18, 69:42, 93:00).
- **Dodge & burn with linear windows + Gain.** Burn = Gain ~0.46 (plus Offset below 25 for extra crush); dodge = Gain ~1.72 — two opposing windowed nodes on the same shot (93:00, 93:56).
- **Track moving windows.** Pen window around the subject's head/torso keyframed (Keyframes panel, Corrector 1–12 + Layer Mixer tracks) and/or Tracker palette (Pan/Tilt/Zoom/Rotate/3D) to follow the subject across the clip (68:04–68:44, 100:12, 101:38).
- **Scopes are the judge.** Vectorscope for hue/skin direction (orange-and-teal separation, skin on the I-line); RGB Parade on the 0–1023 scale for channel balance and clip headroom (52:32, 63:56, 70:38, 71:04).
- **Plan the palette before grading via color harmony theory.** Uses Adobe Color to generate Analogous/Monochromatic/Complementary/Split-Complementary palettes, each mapped to a film reference (Blade Runner / Short Film / Joker / Birds of Prey), and pulls Google Images film stills (Joker night-street teal-shadow + warm-lamp, Blade Runner warm-orange) as look targets (32, 74:20, 76:46–88:40).
- **Film look on top of the grade via Dehancer** (Kodak Vision3 250D profile, defringe + analog print stage) rather than a baked LUT (70:18).
- **Teaching fundamentals:** color = Hue, Contrast, Saturation, Temperature, Luminosity (11:28); higher luminosity ↔ weaker apparent saturation (22:34); shoot 10-bit (≈1.07B colors) not 8-bit to avoid banding/get grading headroom (24:30, 31:10, 34:58); banding worsened by fewer pixels/compression/resolution downscale, "Colors > Pixels" (37:36, 38:00).

### ENGINE: what a headless auto-grader should adopt
- **correct.py — stage order as a fixed pipeline.** Implement the demonstrated node order literally: Exposure → White Balance → Saturation → secondaries → trim. Each stage is an isolated op so it can be measured/tuned independently.
- **correct.py — keep lift/offset neutral by default; act on gain & gamma.** Match the colorist's bias: highlight control via per-channel Gain (multiply on highlights), mid control via small Gamma, and only touch black point (Lift/Offset) when explicitly needed. Encode neutral constants exactly: Offset 25, Gain 1.00, Lift/Gamma 0.00, Sat 50, Hue 50, Lum Mix 100, Pivot ~0.435 — and never interpret Offset 25 or Sat 50 as a non-neutral move (scale-confusion guard).
- **correct.py — white balance as Temp/Tint, not RGB wheels.** Expose a single Temp (Kelvin-style) + Tint pair for WB; warm/cool correction should map to Temp magnitude (the video uses ±hundreds, e.g. -560), with channel-wheel changes reserved for stylistic highlight tinting.
- **stylize.py / match.py — per-channel Gain as the white-balance-in-highlights primitive.** Warm = +R/−B gain, cool = −R/+B gain, "green-up warm" = +G/−B; small magnitudes (±0.03–0.19) give the demonstrated looks. Use this as the cheap stylization lever before any LUT.
- **stylize.py — palette planning via color-harmony.** Add a harmony-target mode (analogous / monochromatic / complementary / split-complementary) that drives the orange-and-teal split: push skin toward the orange/I-line vector and shadows/background toward teal — exactly the vectorscope separation the colorist aims for.
- **measure.py / scopes — vectorscope skin-line + parade headroom as acceptance tests.** Auto-check: (1) skin trace lies on the I-line toward orange; (2) parade peaks land ~768–896 on a 0–1023 scale with bases lifted off 0 (~64–128) and no clipping at 1023; (3) channels roughly aligned for neutral, deliberately split for orange/teal. These are concrete, frame-cited target windows to gate a grade.
- **masks/windows — focus-point localization.** Support the four window primitives (rect with 4-edge softness, ellipse via aspect with single-edge soft, freeform spline with inside/outside feather, linear/gradient) plus tracking, and a dodge/burn pair (gain ~0.46 burn / ~1.72 dodge) for local exposure shaping.
- **tonemap.py / source handling — assume/enforce 10-bit headroom.** Bake in the "10-bit, low contrast in capture, expand later" assumption; flag 8-bit inputs as banding-risk especially when stretching darks/gradients.
- **luts.py / film-emulation — film look as a separate late stage.** Model the Dehancer-style print stage (film profile + defringe + analog print contrast/density) as an optional terminal node applied after the primary grade, not as a replacement for it. Kodak Vision3 250D is the demonstrated default profile.
