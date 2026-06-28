# qualifier-tricks — analysis

*Source: Edou Hoekstra, 3K views · framesRead: 23*

## Overview
This is a secondaries/qualifier masterclass, not a primaries one — the qualifier is the star, used in two non-obvious ways. Trick 1 (de-noising): Resolve's Spatial NR smears highlight detail (clouds look "smudgy"). Hoekstra adds a dedicated Noise Reduction node FIRST in the chain, then inside that SAME node opens the HSL Qualifier, turns OFF Hue, rolls Saturation down low, and uses Luminance to grab only the darker areas — so the NR mask EXCLUDES the bright sky. Result: noise killed in shadows where it lives, highlight detail preserved; he also unlinks Luma/Chroma in Motion Effects and pushes chroma NR harder ("chroma is always removable"). Trick 2 (parallel-node tone control): instead of curves/windows, he stacks PARALLEL nodes off the source, each carrying a qualifier keyed to a luma zone (highlights, shadows) or a hue (skin/orange), then adjusts that isolated zone — pull highlights down to recover the sky, lift shadows, push the warm skin/highlight hue warmer and the shadows cooler to build a precise SPLIT-TONE. The whole philosophy: ROLL OFF every qualifier edge (soften the key) to avoid hard clipping/artifacts, and don't overdo it ("be very careful, these were quite extreme"). Color management is LUT-based (a Nebula Cold conversion LUT for S-Log3→Rec.709), NOT RCM/ACES/CST.

## Order of operations
1. TRICK 1 — De-noising (clip 1, S-Log3 FX6 night shot). Base chain already built: 01 Exposure (darker) → 02 White Balance → 03 Nebula Cold LUT (S-Log3→Rec.709 + look).
2. Add a NEW serial node BEFORE the exposure node, dedicated to Noise Reduction.
3. Open Motion Effects panel → Spatial NR → set Mode (Faster/Better/Enhanced; he tries Enhanced), apply a small amount (Spatial Threshold Luma/Chroma ~64-69). Note highlight smudging in the clouds.
4. In the SAME NR node, open the HSL Qualifier. Turn OFF Hue. Roll Saturation range to the very low end. Use Luminance to select ONLY the darker areas (Low end), then roll off / feather the edge to EXCLUDE the brightest highlights. Shift+H to view/toggle the mask (highlight matte).
5. Net effect: NR is now applied via the qualifier key — strong in noisy shadows, backed off in the sky. Then unlink Luma/Chroma and push Chroma NR harder since chroma noise is 'always removable'.
6. TRICK 2 — Parallel-node tone & color control (clip 2, sunrise self-portrait). Same base chain (EX→WB→LUT).
7. Add a PARALLEL node off the source. Qualifier: Hue OFF, Saturation rolled to lowest, Luminance targets ONLY the HIGHLIGHTS, roll off the key. Then (qualifier still keyed) pull the highlights DOWN with the wheels to recover the blown sky — rest of frame untouched.
8. Add another PARALLEL node for SHADOWS: Hue OFF, low Saturation, Luminance keyed to the very darkest parts, roll off less soft. Lift/boost the shadows so nothing crushes.
9. Add a PARALLEL node for COLOR/SKIN: enable Hue, key the orange/skin band (Hue Center ~31-33), low saturation target, roll off the edges. Nudge that hue WARMER with the wheel (warms skin + existing warm tones = warm side of split-tone).
10. Add a PARALLEL node for a second tone: Luminance-key the dark parts again and push them COOLER (offset/shadow into blue) to complete the SPLIT-TONE.
11. All parallel nodes recombine into the chain (parallel/layer mixer) before the LUT. Compare each node solo, then all together: basic look → controlled highlights, lifted shadows, warm/cool split-tone. Warning: overdoing it causes artifacts — judge what the footage can handle.

## Node tree
Serial base chain (clip 1, de-noise): 01 Noise Reduction (NEW, inserted first, holds the NR + the masking qualifier) → 02 Exposure (EX) → 03 White Balance (WB) → 04 LUT (Nebula Cold). For clip 2 the structure becomes a PARALLEL fan: the source splits into multiple parallel nodes (one per qualifier-isolated zone — highlights, shadows, skin/warm hue, cool shadows; up to ~6 parallel nodes by the end) that recombine through a parallel/layer mixer node, then continue through WB and the final LUT node. Each parallel node carries its own HSL qualifier key. No power windows, no trackers — node count grows as each new tone/color zone gets its own keyed parallel node.

## Scopes
- **Waveform (RGB parade overlay / full waveform)** — Watches the top of the trace (highlights ~890-1023) staying off the ceiling when recovering the sky, and the bottom (shadows ~0-128) lifting slightly off zero. Channel separation in the waveform confirms warm-highlight / cool-shadow split-tone. · targets: Used throughout as the single reference scope (Scopes panel set to 'Waveform', 0-1023 10-bit scale). He reads it to confirm highlights aren't clipping at the top after the qualifier highlight pull, and that shadows lift off the floor without crushing. The split-tone shows as red/green/blue traces separating in the lows vs highs.

## Primaries
Primaries are demonstrated in the Log color wheels (Primaries - Log Wheels panel: Shadow / Midtone / Highlight / Offset) used INSIDE the qualifier-keyed parallel nodes, not as a global grade. On-screen project defaults visible: Contrast 1.000 (pushed to 1.104 on one node), Pivot 0.435, Lum Mix-style Range 0.333, S-Range 0.550, Temp 0.0, Tint 0.00, Offset 25.00/25.00/25.00 (neutral). Demonstrated moves: Highlights master wheel slider pulled to -41.50 to bring the blown sky down (qualifier-masked to highlights only); Shadow wheel RGB pulled to -0.38/-0.38/-0.38 to cool/darken keyed shadows; Offset wheel pushed toward blue (R 0.47 / G 29.29 / B 53.88) for the cool side of the split-tone; Saturation parameter raised (50→71.70). Technique is LOG wheels (zone-isolated, gentle, complementary to the qualifier key) rather than aggressive lift/gamma/gain primary wheels.

## Secondaries
The entire video IS secondaries technique. HSL Qualifier (Qualifier - HSL panel) is used two ways: (a) as a NOISE-REDUCTION MASK (Hue off, Sat low, Luma keyed to shadows, rolled off — so the NR node only de-noises the dark areas, sparing highlight detail); (b) as a TONE/COLOR ISOLATOR inside parallel nodes — luma-keyed to highlights or shadows for exposure-zone control, and hue-keyed to the skin/orange band for selective color. NO power windows and NO tracking are used — he explicitly says 'no advanced masking needed.' Matte Finesse is visible (Blur Radius, Clean Black/White, Denoise, In/Out Ratio) but he relies mainly on rolling off the L.Soft / H.Soft edges of each Luminance and Saturation range to feather the key and avoid hard/clipped selections. Shift+H toggles the highlight matte overlay to judge each selection.

## Skin tone
Skin is handled by HUE qualifier, not the vectorscope skin line. He enables Hue and keys the orange band — on-screen Hue Center ~31-33 (Width ~30-49), with Saturation targeted low (skin reads fairly desaturated) and Luminance mid-to-high, then rolls off all edges. With skin isolated he demonstrates nudging the hue WARMER via the wheel rather than just boosting saturation — 'you can nudge those colors towards a certain hue.' No vectorscope/skin-tone-line (I-bar at ~11 o'clock) is shown; selection and judgement are done by eye on the qualifier mask (Shift+H).

## Color management
NOT RCM / ACES / CST. Color management is LUT-driven: footage is Sony FX6 S-Log3, converted with a third-party 'Nebula Cold' conversion LUT that maps S-Log3 → Rec.709 with a built-in look (link in the creator's description). The LUT sits as the LAST node ('LUT' node) in the chain; all grading nodes (NR, exposure, WB, the qualifier-keyed parallels) live BEFORE the LUT. Project is DaVinci Resolve Studio 20. No working-color-space / timeline-color-space settings are shown or discussed — implied standard YRGB (non-color-managed) with a conversion LUT doing the transform.

## Look design
Look is a warm sunrise/golden split-tone built additively from qualifier-keyed parallel nodes on top of the Nebula Cold conversion LUT. Components: (1) recovered, controlled highlights (sky pulled down so it's not blown), (2) lifted shadows so nothing crushes ('a little lift in the shadows so nothing is too dark'), (3) warm skin + warm highlights nudged via hue, (4) cool shadows pushed toward blue/offset — together a SPLIT-TONE (warm highs / cool lows) done 'more precise' than a global split-tone tool. Stated design principle: roll off every qualifier edge to avoid clipping, keep moves subtle, and stop before artifacts appear. End comparison: flat 'basic look' → punchy, dimensional, split-toned result.

## Numeric settings seen on screen
- De-noise NR node — Spatial Threshold Luma 69.0 / Chroma 69.0 (f006); later Luma 64.4 / Chroma 64.4 (f013); Blend 0.0; Spatial NR Mode = Enhanced (f013), Radius Medium; Temporal NR Frames 0; Motion Blur 0.0
- Spatial NR Mode dropdown options seen: Faster / Better / Enhanced / AI UltraNR (f005)
- De-noise qualifier (shadow mask): Hue OFF; Saturation High ~5.1; Luminance High 59.7 (f009), later Luminance High 71.0 H.Soft 3.6 (f011) — keying the low/dark end
- Log Wheels project defaults: Contrast 1.000, Pivot 0.435, Range 0.333, S-Range 0.550, Temp 0.0, Tint 0.00, Offset 25.00/25.00/25.00 (f018)
- Highlight-recovery node: Highlights master slider -41.50 (f022); Saturation param 50.00
- Skin/shadow split-tone node: Contrast raised to 1.104; Shadow wheel -0.38/-0.38/-0.38; Midtone 0.32/0.32/0.32; Offset 16.05/16.05/16.05 (f030)
- Skin hue qualifier: Hue Center 33.1, Width 49.4, Sym 50.0 (f034); alt Center 31.2 Width 30.6 (f036); Luminance Low 51.9 High 65.2 (f034)
- Saturation param boosted to 71.70 (f038)
- Cool-shadow / split-tone node: Offset wheel R 0.47 / G 29.29 / B 53.88 (pushed into blue), Saturation 50.00 (f046)
- Qualifier feather values used repeatedly: L.Soft / H.Soft on Saturation and Luminance ranges (e.g. Sat H.Soft 12.5, Lum H.Soft 5.0) to roll off edges

## Teaching points
- The qualifier isn't only for color isolation — you can use its KEY to mask ANY operation. Here it masks Noise Reduction so NR runs only where noise lives (shadows) and spares highlight detail. Beginner takeaway: a qualifier creates a matte; whatever you do in that node is limited to the matte.
- Resolve Spatial NR trades detail for cleanliness — it smears highlights (clouds go 'smudgy'). Solution is selective NR, not less NR.
- 'Chroma is always removable' — unlink Luma/Chroma NR and push CHROMA harder than LUMA, because color noise can be crushed with little perceptual cost while luma NR is what destroys detail.
- To key a tone ZONE (not a color), turn Hue OFF, set Saturation to the lowest/widest, and drive the selection entirely with the LUMINANCE range. Low end = shadows, high end = highlights.
- ALWAYS roll off (feather) the qualifier edges via L.Soft / H.Soft. Hard keys clip and produce artifacts/banding; soft keys blend invisibly. This is repeated as the core safety rule.
- Shift+H toggles the highlight matte so you can SEE your selection while you tune it — essential for judging a key by eye.
- Parallel nodes let you target highlights, shadows, and specific hues INDEPENDENTLY and recombine them — a clean alternative to curves/windows for tone-zone control with 'no advanced masking needed.'
- Split-toning can be done precisely by hue-keying the warm tones (skin/highlights) and pushing them warmer in one node, then luma-keying the shadows and pushing them cooler in another — more controlled than a global split-tone tool.
- Recover a blown sky by luma-keying ONLY the highlights and pulling them down — the rest of the frame is mathematically untouched.
- Order matters: NR and these grading nodes go BEFORE the conversion/look LUT; grading after a Rec.709 LUT fights the look.
- Restraint is the whole point: 'if you overdo it you get weird artifacts.' Judge what the footage can handle; the demonstrated values were deliberately exaggerated for teaching.

## Quotable claims
- "Shot on FX6 which obviously means there's no noise processing within the camera." (00:00:00)
- "A nebula cold lot for S-Log3 — a conversion LUT that takes my S-Log3 footage, turns it into Rec.709 with a little bit of a look on top." (00:00:16)
- "Actually you can use the qualifier to fix this... turn off hue, lower saturation, and for luminance only grab the darker areas." (00:00:46)
- "You can unlink those, up the chroma because chroma is always removable, and your footage will look a little bit less smudgy." (00:01:34)
- "Now we only targeted the highlights... we pull down the highlights, the rest of the footage stays the same — no advanced masking needed, and boom, you recovered your highlights." (00:02:55)
- "Going to roll things off because you don't want anything hard in your footage... otherwise you're going to get clipping issues." (00:04:44)
- "You can also just nudge those colors towards a certain hue with this wheel... this is also a way you can kind of split tone, but a little bit more precise." (00:05:14)
- "Just be careful with it because if you overdo it, you're going to get some weird artifacts." (00:06:46)

## Key frames
- `f006.jpg` — Trick 1 setup: 4-node serial chain (NR→EX→WB→LUT) top-right, Motion Effects panel open with Spatial NR (Spatial Threshold Luma/Chroma 69.0) and Waveform scope — the de-noising starting point.
- `f009.jpg` — The KEY de-noise idea: HSL Qualifier inside the NR node with Hue OFF, Saturation/Luminance keyed to the dark areas (Luma High 59.7) so NR only affects shadows, not the smudgy highlights.
- `f013.jpg` — Motion Effects: Spatial NR Mode = Enhanced, Spatial Threshold Luma/Chroma 64.4 — confirms the actual NR settings and the unlink/chroma-push concept.
- `f018.jpg` — Trick 2: Log color wheels with all default values readable (Contrast 1.000, Pivot 0.435, Range 0.333, S-Range 0.550, Offset 25/25/25) and the parallel-node right-click context menu — the grading panel reference.
- `f022.jpg` — Highlight recovery: Highlights master slider pulled to -41.50 with the highlight-keyed parallel node active — blown sky brought down while the rest of the frame is untouched.
- `f030.jpg` — Split-tone shadow move: 3 parallel nodes, Shadow wheel at -0.38/-0.38/-0.38, Contrast 1.104 — cooling/shaping the keyed shadows.
- `f034.jpg` — Skin-tone qualifier: Hue ENABLED and keyed to orange (Center 33.1, Width 49.4), isolating the subject for a selective warm hue nudge.
- `f046.jpg` — Final split-tone: full ~6-node parallel fan, Offset wheel pushed to blue (R 0.47/G 29.29/B 53.88) for cool shadows — the cool side of the warm/cool split-tone.
