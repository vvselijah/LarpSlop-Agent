# grading-too-complicated — analysis

*Source: Darren Mostyn, 36K views (HIGH authority) · framesRead: 18*

## Overview
A deliberate "back to basics" antidote to overcomplicated modern Resolve tutorials. Mostyn lays out 5 pro fundamentals that produce consistent, technically-clean grades WITHOUT advanced tools (no Magic Mask, no Color Warper, no heavy secondaries): (1) use a FIXED node tree as a map/checklist; (2) always use color management (CST/ACES/DRT) to get the source to a good starting point; (3) nail balance + exposure + contrast solid before anything else; (4) use a saturation method that does NOT raise luminance (avoid the primary Sat slider); (5) NEVER key skin — fix skin in the balance node instead. He demos on a 3-shot interview scene (bearded man in red jumper) shot ARRI LogC3 / ARRI Wide Gamut 3, graded in DaVinci Wide Gamut, output to Rec.709 gamma 2.4. He repeatedly contrasts a "vanilla Resolve" way of doing each thing with his preferred Mononodes paid-DCTL way, but is careful to teach the free/built-in technique first. Authority is high: he reads scopes by eye with target-driven discipline (skin-tone line, waveform floor/ceiling, exposure heatmap zero) rather than chasing numbers.

## Order of operations
1. 1. COLOR MANAGEMENT FIRST: input CST CAM>DWG (ARRI Wide Gamut 3 / ARRI LogC3 -> DaVinci Wide Gamut / DaVinci Intermediate, tone-map None, gamut-map None) at the head of the tree; output transform (CST DWG>Rec709 g2.4, OR a DRT like Mononodes Look/Lab/Print) at the tail. Grade everything in DaVinci Wide Gamut in between.
2. 2. FIXED NODE TREE between the transforms, used as a checklist (not strictly in order): Node02 BAL/EXP -> Node03 CONTRAST -> Node04 SAT -> Node05 HSV SAT.
3. 3. BALANCE + EXPOSURE (node 02): set exposure for the subject (skin), then balance skin onto the vectorscope skin-tone line. Mostyn does all three of balance/exposure/contrast 'at once' but insists they are locked before moving on.
4. 4. CONTRAST (node 03): set with gain+offset (or the Contrast slider with a correct pivot) watching the waveform floor (not below 0) and highlights.
5. 5. SATURATION (node 04): add saturation with a method that does not lift luma (HDR global sat, ColorSlice, or Mononodes color-shift) — NOT the primary Sat slider.
6. 6. HSV SAT (node 05): optional extra filmic saturation via a node whose color space is switched to HSV, isolating channel 2 (saturation) and driving it with Gain.
7. 7. Tip 5 governs the whole flow: if skin is wrong, go BACK to the balance node and re-do it with your balance tool — do not key skin.
8. 8. QC: use the Skin Balance heatmap + Light Box (update thumbnails) to confirm all shots' skin tones land in the same region (all yellow / on the line).

## Node tree
"Two trees shown. FULL fixed tree (f004): CAM>DWG (01) -> BAL/EXP (02) -> CONTRAST (03) -> SAT (04) -> HSV SAT (05) on the main spine, with a vertical stack of optional nodes branching (TEMP, HDR, WARPER, CURVES), a TRIM node, three PARALLEL power-window nodes PW1/PW2/PW3, then a tail chain Texture -> Density -> FILM -> DRT. SIMPLIFIED tree used for the lesson (f007): CAM>DWG (01) -> BAL/EXP (02) -> CONTRAST (03) -> SAT (04) -> HSV SAT (05) -> DWG>709 (06). All serial. Node 05 (HSV SAT) is special: its node Color Space is changed to the HSV color model (right-click > Color Space > HSV, f036) so saturation can be isolated on channel 2. The two CSTs/DRT bracket the creative nodes so all grading happens in DaVinci Wide Gamut. He stresses the tree is a fixed MAP/checklist (balance, exposure, contrast, saturation) so that under time pressure you always know what to do next — adapt node count per shot but keep the order."

## Scopes
- **Waveform (RGB/luma, 0-1023 10-bit scale visible)** — Read by eye watching the bottom and top of the trace while pushing gain/offset; watch overall trace height change as saturation is added (f033, f036, f045). · targets: Black floor of the trace must NOT go below 0; highlights need not hit the top (1023) — just enough for good contrast. Also used to PROVE the saturation point: primary Sat raises the trace (bad), HDR/ColorSlice/Mononodes sat keeps or lowers it (good).
- **Vectorscope** — Read the skin trace's angle vs the diagonal skin line; Mononodes Skin Balance color-codes it: green = under the line, yellow = on the line, magenta = over (f020 illustrates the magenta/yellow/green mapping; f026/f036 show the live scope). · targets: Skin tone should sit ON or consistently near the skin-tone line (the upper-left I-line). Under (greenish side) or over is fine AS LONG AS it is consistent across the scene.
- **Exposure Heat Map (Mononodes Utility false-color, -5..+5 scale, 0=perfect)** — False-color overlay on the image with a -5 to +5 legend; split the frame (vertical/horizontal) to see real image vs map side-by-side (f021, f023). · targets: Subject skin should read ~0 (perfect) in flat light; a key-lit side is expected to read slightly hot (above 0) and that's correct, not an error.
- **Vectorscope skin-line / Light Box QC** — Apply the Skin Balance heatmap at the TIMELINE level, open Light Box, right-click > Update Thumbnails, and eyeball all thumbnails at once (f049). · targets: All shots in a scene land in the SAME region (all on the yellow/line, or all consistently green/magenta).

## Primaries
"See above — HDR Global wheel for exposure/balance (0.63 on screen), primary Gain+Offset for contrast (Offset 25.00 x3, Pivot 0.435/0.336, Contrast 1.000-1.010), with the linear-gamma+Gain 'linear gain' method shown as the more advanced alternative he considers cleaner than primary-wheel offset."

## Secondaries
"Deliberately minimal — the whole video argues you usually don't need heavy secondaries. The only qualifier-like work is per-vector saturation control: ColorSlice and the Mononodes color-shift DCTL let him pull skin saturation/density back while pushing reds (the jumper) without a manual key. Power Windows / Magic Mask / Color Warper are explicitly named as things to AVOID doing before balance/exposure/contrast are solid. He sanctions keying NON-skin objects (e.g. 'key this sofa to make it change') but draws a hard line at keying skin (Tip 5). The full 'fixed node tree' (f004) does contain optional secondary/effect nodes (TEMP, HDR, WARPER, CURVES, PW1-3 parallel power-window nodes, TRIM, Texture, Density, FILM, DRT) for when a shot needs them, but the taught workflow collapses to just 4-5 nodes."

## Skin tone
"Core method: get skin onto the vectorscope SKIN-TONE LINE (the upper-left flesh-line). Manual way (no plugins): watch the vectorscope and adjust exposure/balance until the skin trace sits on/just-under the line; sitting slightly under or over is acceptable provided it's CONSISTENT across the scene. Plugin way: Mononodes Utility 'Skin Balance' color-codes it — GREEN = under the line, YELLOW = on the line, MAGENTA = over (illustrated cleanly in f020 with the three vectorscopes; live in f026). He drives the HDR Global exposure until the readout turns YELLOW = on the line. Crucial discipline (Tip 5): if skin looks wrong, FIX IT IN THE BALANCE NODE (reset and re-balance with whatever tool — gamma, offset, HDR offset), do NOT key the skin and push gamma/offset on the key. Scene-level QC via Skin Balance heatmap + Light Box thumbnails to confirm all skins land in the same region (f049)."

## Color management
"Manual CST-based color management (NOT automatic RCM, NOT ACES — though he says any of automatic CM / ACES / CSTs / CSTs+DRTs is fine, the point is just USE color management). Demo project: input CST node 'CAM>DWG' set to Input Color Space ARRI Wide Gamut 3, Input Gamma ARRI LogC3, Output Color Space DaVinci Wide Gamut, Output Gamma DaVinci Intermediate, Tone Mapping None, Gamut Mapping None, 'Use White Point Adaptation' checked (read directly off the CST panel, f009). Grade happens in DaVinci Wide Gamut. Output options he names: (a) a tail CST DWG>Rec709 gamma 2.4; or (b) a DRT — he mentions JP2499-style free DRTs and the one he actually uses now, the Mononodes 'Look/Lab/Print' DRT (MONO-LAB DCTL, shown in f011 with Exposure 0.000, Contrast 1.000, Pivot 0.391, Tone Compression 0.000, Highlights 1.000, Black Point 0.000, Shadows 0.000) as his DWG->Rec709 output. Working/output spec for the piece: DaVinci Wide Gamut working space, Rec.709 gamma 2.4 deliverable."

## Look design
"Look design here is mostly RESTRAINT-as-look: clean balance + correct contrast + non-luma-lifting saturation already yields a pleasing, 'filmic' image — that's the thesis. The 'look' layer is delivered through the OUTPUT DRT (Mononodes Look/Lab/Print 'print' emulation, MONO-LAB, f011) standing in for a print film emulation, plus density-style saturation (ColorSlice 'Density'/'Den.Depth' and Mononodes color-shift 'Den'/'Deep' controls) that adds filmic richness in the reds/jumper while holding skin. The full node tree (f004) reserves dedicated FILM and DRT nodes for emulation at the tail. No split-tone / hue-vs-hue curve work is taught in this episode — it's intentionally fundamentals-only. Paid look tools shown: the entire Mononodes suite (Utility heatmaps, color-shift saturation DCTLs, Look/Lab/Print DRT), all optional ('you don't need to rush out and buy Mononodes')."

## Numeric settings seen on screen
- CST CAM>DWG (f009): Input Color Space = ARRI Wide Gamut 3, Input Gamma = ARRI LogC3, Output Color Space = DaVinci Wide Gamut, Output Gamma = DaVinci Intermediate, Tone Mapping = None, Gamut Mapping = None, Use White Point Adaptation = ON
- Mononodes MONO-LAB DRT (f011): Exposure 0.000, Contrast 1.000, Pivot 0.391, Tone Compression 0.000, Highlights 1.000, Black Point 0.000, Shadows 0.000
- Primaries during contrast demo (f033/f038/f047): Contrast 1.000, Pivot 0.435, Gain 1.00/1.00/1.00/1.00, Offset 25.00/25.00/25.00, Lift 0.00, Gamma 0.00, Temp 0.0, Tint 0.00, Saturation 50.00, Hue 50.00, Lum Mix 100.00, Mid/Detail 0.00
- Pivot teaching overlay (f030): use Pivot 0.336 for correct middle grey in DaVinci Wide Gamut (contrast read 1.010 there)
- HDR palette Global Exposure = 0.63 (f026, f028); HDR Global x/y offset ~0.01/0.00
- Mononodes Balance Utility 'MONO-Balance-v1.4' (f021/f023): Skin Tone Range 0.500, Deviation Range 1.000, Hue Angle 0.000, Split Position 0.500 (0.271 in f023); checkboxes: Exposure Heatmap ON, Split Vertically ON, Show Guide ON; Exposure Heat Map legend -5..+5 with 0 = perfect exposure
- ColorSlice (f040): Saturation 1.50 global, Skin density 0.59 (pulled back), other vectors 1.00; (f043 ColorSlice Saturation 1.00)
- Mononodes color-shift 'MONO-3-SAT-DEN-HUE-v4.0' (f043): Global Sat 0.442, all per-vector Sat/Den/Hue 0.000, Deep Sat / Global Den / Deep Den / Deep Hue present
- Waveform scale shown 0-1023 (10-bit)

## Teaching points
- A FIXED node tree is a checklist, not a recipe: label nodes balance/exposure/contrast/saturation and always follow that order so you never freeze under time pressure. Beginners should literally name their nodes.
- Color management is step zero: a Color Space Transform (or ACES, or automatic CM) un-does the camera's log/wide-gamut encoding so you start grading from a neutral, predictable image. Input = camera's space+gamma; Output = your delivery (Rec709 g2.4) or a DRT.
- Do balance, exposure and contrast FIRST and make them rock-solid; only then reach for fancy tools. Building a look on a wrong foundation wastes the look.
- Read scopes against TARGETS, not magic numbers: waveform floor not below 0, skin on the vectorscope skin line, exposure heatmap ~0 on skin. There is no single 'correct exposure number' — it's experience + the image + the lighting (a key-lit cheek SHOULD read hot).
- The vectorscope skin-tone line is the anchor for believable skin; consistency across shots matters more than hitting it perfectly. Green=under, yellow=on, magenta=over (Mononodes heatmap mnemonic).
- Contrast is the single most important match between shots — a contrast mismatch is more visible than a balance mismatch. Balance is forgiving; contrast is not.
- When using the Contrast slider, the PIVOT must match your working space's middle grey, or contrast pivots around the wrong point (Rec709 default vs ~0.336 for DaVinci Wide Gamut).
- The primary Saturation slider RAISES luminance — proven live on the waveform — giving a harsh video/digital look. Use a saturation method that holds or lowers luma: HDR global sat, ColorSlice, the HSV-channel-2 trick, or a Mononodes density DCTL, for a richer filmic result.
- The HSV-color-space node trick: change a node's color space to HSV, kill channels 1 (hue) and 3 (value), keep channel 2 (sat), then push Gain — clean saturation that doesn't blow luma.
- NEVER key skin to fix it. If skin is off, return to the balance node, reset, and re-balance with your balance tool. Keying skin then pushing gamma/offset on the key is the worst thing you can do. Keying non-skin objects (a sofa) is fine.
- QC the whole scene at once with the Light Box: apply a skin-balance heatmap at the timeline level, update thumbnails, and confirm every shot's skin sits in the same region — that's how you know a scene is balanced.
- You don't NEED paid plugins (Mononodes) — every technique has a free/built-in equivalent; the plugins just make the same correct technique faster.

## Quotable claims
- "My first tip for you is to use a fixed node tree... Treat it like a map. You don't necessarily use them in order, but it's like building blocks." (00:00:46)
- "Make sure you're using color management... This is the best way of getting your camera source technically to the best starting point ready to do your grade." (00:01:48)
- "Balance exposure and contrast. Make sure these are absolutely solid before you start moving on... You don't want to start doing things like color warper and magic mask... until you've got your balance exposure and contrast absolutely solid." (00:04:25)
- "There's no one number that I can give you that says this is perfect exposure. So it's really a case of having a bit of experience and looking at the image." (00:05:12)
- "Sitting right on it [the skin-tone line] is a general guide as to where skin tone should sit... you can sit under, you can sit over as long as you're consistent across your scene." (00:06:45)
- "Contrast... it's the most important part of your grade. When you're doing a scene match, if your contrast is out between shots people will really notice it more than if your balance was out slightly." (00:08:54)
- "When you're using saturation, use one that doesn't increase brightness... [the primary tool] gives you a very video digital look. It's not that pleasing to the eye." (00:09:10)
- "If you are working in DaVinci Wide Gamut set the pivot to 0.336 for correct middle grey." (00:08:20)
- "Tip number five, don't key skin. If your skin tone is not looking correct, the worst thing you can do is key it and then start playing around with your gamma or your offset... Go back to the balance node, reset it... get it balanced correctly." (00:12:47)
- "Go to light box, right click, update my thumbnails, and I can see at a glance that the skin tones are all in the same region." (00:13:34)

## Key frames
- `f004.jpg` — The FULL fixed node tree — labeled spine CAM>DWG/BAL/EXP/CONTRAST/SAT/HSV SAT plus optional TEMP/HDR/WARPER/CURVES, TRIM, three parallel PW power-window nodes, and a Texture->Density->FILM->DRT tail. The 'map' concept of Tip 1.
- `f007.jpg` — The SIMPLIFIED 4-creative-node tree used for the lesson: CAM>DWG(01) -> BAL/EXP(02) -> CONTRAST(03) -> SAT(04) -> HSV SAT(05) -> DWG>709(06), all serial — the actual teaching tree.
- `f009.jpg` — The input CST panel: ARRI Wide Gamut 3 / ARRI LogC3 in -> DaVinci Wide Gamut / DaVinci Intermediate out, Tone Mapping None, Gamut Mapping None, Use White Point Adaptation on. Tip 2 color management, with exact settings.
- `f023.jpg` — Mononodes Utility Exposure Heat Map (false color, -5..+5 legend, 0=perfect) split-screen real-image-vs-map, with the MONO-Balance panel (Skin Tone Range 0.500, Deviation 1.000, Split Vertically). How exposure is read as zero on skin.
- `f030.jpg` — Primaries with overlay 'SET THE PIVOT TO 0.336 FOR CORRECT MIDDLE GREY' in DaVinci Wide Gamut — the contrast-pivot teaching point (Contrast 1.010, Pivot 0.435).
- `f033.jpg` — Primaries Color Wheels (Lift/Gamma/Gain/Offset) + waveform: the gain+offset contrast technique with on-screen values Contrast 1.000, Pivot 0.435, Offset 25.00 x3, Sat 50, Hue 50, Lum Mix 100.
- `f036.jpg` — Right-click node > Color Space menu open with HSV being selected — the HSV-color-model trick that powers the HSV SAT node (isolate channel 2 for clean saturation).
- `f043.jpg` — Mononodes color-shift DCTL 'MONO-3-SAT-DEN-HUE-v4.0' with per-vector Sat/Den/Hue + Global Sat 0.442, Deep Sat, and the Deep-Sat skin-restore control — his 2026 saturation tool.
- `f049.jpg` — Light Box with all 3 shots' thumbnails carrying the Skin Balance heatmap, all reading yellow (on the skin line) — the scene-balance QC trick that closes the video.
