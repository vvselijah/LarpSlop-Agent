# best-node-tree-any-camera — analysis

*Source: Darren Mostyn, 561K views (HIGH) · framesRead: 28*

## Overview
A reusable "fixed node tree" that lets you grade footage from ANY camera by changing only ONE setting (the input color space on node 01). The whole philosophy is manual color management via Color Space Transform (CST) nodes — NOT Resolve's automatic RCM/ACES. You bookend the tree with two CST nodes: node 01 (CAM>DWG) converts the camera's native color space up into a large working space (DaVinci Wide Gamut / DaVinci Intermediate), and the final node 02 (DWG>709) converts back down to the display space (Rec.709 Gamma 2.4) so you always grade while SEEING the correct display-referred image. Between those bookends sits a fixed, disciplined, labeled node structure: Balance/Exposure → Contrast → Saturation as the foundation, then a parallel cluster of fine-tune nodes (Temp, HDR, Warper, Curves), a Trim node, a parallel cluster of Power Windows, then Texture and an optional Kodak 2383 film-print-emulation look (built as a compound node with its own internal CST so its strength can be keyed). The same saved tree is dropped onto every clip; for each new camera you only re-point node 01's input color space. Mostyn frames this as the discipline that makes his broadcast grades (BBC/Amazon/ITV) fast and consistent. Key universal fallback shown on-screen: if you don't know the camera profile, set the input CST to Rec.709 / Rec.709.

## Order of operations
1. Project Settings > Color Management: set Color science = DaVinci YRGB (NOT automatic/RCM), Timeline color space = DaVinci Wide Gamut / DaVinci Intermediate, Output color space = Rec.709 Gamma 2.4 (match the calibrated monitor). Optionally save as a preset.
2. Node 01 (CAM>DWG): add a Color Space Transform. Input = the camera's native space (e.g. Canon Cinema Gamut / Canon Log3); Output = DaVinci Wide Gamut / DaVinci Intermediate. Trust Resolve's auto-ticked OOTF/tone-map checkboxes.
3. Node 02 (DWG>709): add a second CST at the very END of the tree. Input = DaVinci Wide Gamut / DaVinci Intermediate; Output = Rec.709 / Gamma 2.4. Label it DWG>709. This stays on permanently so you grade under display space.
4. Build the EMPTY node skeleton first, then fill it: serial nodes BAL/EXP (03), CONTRAST (04), SAT (05) — the solid foundation.
5. Add a serial node (06) then Alt/Option+P parallels for fine-tuning: TEMP, HDR, WARPER, CURVES (each pulls from the foundation point, not from each other, via the layer/parallel mixer).
6. Add TRIM (11) — a global tweak node for overall contrast/shadow lifts after fine-tuning.
7. Add a serial + parallels for POWER WINDOWS (PW1/PW2/PW3) for isolations.
8. Add TEXTURE / SPARE nodes for grain/texture.
9. Optional film look: append two serials, apply Kodak 2383 print-emulation LUT, then stick a CST in front of the LUT (Rec.709 Gamma 2.4 IN -> Rec.709 Cineon Film Log OUT). Select both, right-click > create Compound Node so the LUT strength can be keyed 0-100 via the key/mix tool.
10. Save the whole tree as a still/PowerGrade (with the look disabled). For reuse, set node 01 input to 'Use timeline' so it re-applies camera-agnostic.
11. GRADE: switch on look, grade UNDER it. Balance/exposure (HDR exposure + offset wheel), then contrast (primaries contrast + pivot), then saturation (HDR global sat). Get this foundation looking good BEFORE branching. Then fine-tune in the parallels and isolate in the power windows.

## Node tree
"~17 nodes, bookended by two CST nodes with a parallel-heavy middle. SERIAL spine: 01 CAM>DWG (input CST) -> 03 BAL/EXP -> 04 CONTRAST -> 05 SAT -> [parallel cluster A via layer/parallel mixer: 06 TEMP, 08 HDR, 09 WARPER, 10 CURVES] -> 11 TRIM -> [parallel cluster B: 12 PW1, 14 PW2, 15 PW3 power windows] -> 16 TEXTURE -> 17 SPARE -> 02 DWG>709 (output CST) -> [optional appended: film-look compound node 'KODAK' = inner CST + Kodak 2383 LUT, keyable strength]. Parallel clusters use Alt/Option+P parallels feeding a layer mixer so each fine-tune/window node draws from the clean foundation rather than chaining. Every node is hand-labeled. The skeleton is built EMPTY first as a 'disciplined reminder' to grade in a methodical order, then filled in; unused nodes are left empty in the tree."

## Scopes
- **Waveform / RGB Parade** — Read on the 10-bit 0-1023 vertical scale (labels 128/256/384/512/640/768/896/1023 visible). Mostyn checks the bottom of the traces for lifted shadows and the channel balance left-to-right to spot casts, correcting with the offset/balance wheels until the trace bottoms align. · targets: Used as the primary tool for balance and exposure: watch the three R/G/B traces and align them to neutralize color casts and set black/white levels. Parade shown constantly through the grade on the bottom-right Scopes panel (0-1023 10-bit scale).
- **Histogram** — Visual spread check — a tall central spike = flat/low-contrast log image; spreading it out = adding contrast. Used while pushing the primaries contrast slider. · targets: Secondary exposure/contrast reference, shown to the left of the parade. Watch the spread and the spike position to judge contrast and clipping.
- **Vectorscope** — Watch the overall trace extension from center (saturation amount — don't over-extend past the target boxes) and the dominant lobe direction. Mostyn watches the trace lean toward the I-line/skin region after warming via offset; he keeps saturation disciplined (Sat slider left at 50 default, adds only small HDR sat). · targets: Used to judge saturation and color balance, and implicitly the skin-tone direction. The trace points toward the upper-left quadrant (skin/orange region) once graded.

## Primaries
"Mostyn works primarily on the OFFSET wheel and the HDR palette rather than lift/gamma/gain. For BALANCE/EXPOSURE (node 03): he opens the HDR tool, drops exposure slightly, then nudges the Offset wheel to neutralize the cast (offset wheel observed at ~24.01/24.91/25.63 then reset toward 25.00/25.00/25.00 neutral). The Lift/Gamma/Gain wheels are seen at or near default (0.00/1.00/1.00) — he explicitly prefers offset for balance and the HDR wheels for everything else. For CONTRAST (node 04): he uses the primaries Contrast slider with Pivot left at the default 0.435 (clearly visible on screen), saying you can also add contrast via the HDR wheel — many ways, he prefers primaries contrast. For SATURATION (node 05): Saturation slider stays at the 50.00 default; he adds only a small amount of GLOBAL saturation via the HDR tool. On the Canon non-log clip he notes that profile comes in flat and 'you add contrast and saturation to taste yourself.' Hue stays 50.00, Lum Mix 100.00 (defaults visible). Grading is always done UNDER the DWG>709 CST and under any active film look."

## Secondaries
"Secondaries live in dedicated parallel clusters so they branch off the clean foundation rather than stacking. WARPER node (09): used with Hue vs Sat / Hue vs Hue curves to selectively desaturate a subject's dress without affecting the temperature node — pulls its feed from the SAT foundation point, not from TEMP. POWER WINDOWS (PW1/PW2/PW3, nodes 12/14/15): a parallel cluster reserved for isolations/shapes (Window palette with Linear/Circle/Polygon/Curve/Gradient + softness controls shown); he draws a window, then lifts gain/offset inside it and toggles on/off to confirm it improves the shot. The TRIM node (11) sits before the windows for a global post-fine-tune tweak (e.g. lifting shadows with Lift). The architecture point: each parallel takes its feed from the solid graded foundation, giving consistent, independent adjustments."

## Skin tone
"Not taught as an explicit skin-tone-line/I-line targeting exercise — there is no moment where he qualifies skin and pulls it to the vectorscope skin line by angle. Skin tone is handled implicitly: after warming the image via the offset wheel and HDR temperature, the vectorscope trace leans toward the upper-left orange/skin region, which he uses as a sanity check for a natural, warm broadcast look. The dress-desaturation in the Warper (Hue vs Sat) is the closest secondary skin/wardrobe isolation shown."

## Color management
"MANUAL color management via CST nodes — explicitly NOT Resolve's automatic color management. Project Settings > Color Management (frames f003-f006): Color science = DaVinci YRGB; the 'Use separate color space and gamma' checkbox is discussed/highlighted; Timeline color space set to a large working space = DaVinci Wide Gamut / DaVinci Intermediate (he says you could use ACES, ARRI Wide Gamut, or your preference, but he works in DWG/DI); Output color space = Rec.709 Gamma 2.4 to match his calibrated broadcast monitor. He recommends saving these as a preset. The two CST nodes do the actual transforms: node 01 camera->DWG/DI, node 02 DWG/DI->Rec.709/Gamma2.4. The output CST shows Tone Mapping Method = DaVinci, Adaptation = 9.00, Gamut Mapping = None, Apply Forward OOTF / Use White Point Adaptation auto-ticked — he says trust Resolve's auto-ticked transform-function checkboxes because it knows whether each space is camera/working/display. iPhone caveat: iPhone 14 footage is Rec.709 with NO source gamma, so set input gamma to Rec.709 (NOT Gamma 2.4, which is a display gamma); newer iPhones may be Rec.2020/HDR."

## Look design
"Film look = the built-in Kodak 2383 print-film emulation LUT (Film Looks > Rec.709 Kodak 2383 D55), one of several (Fujifilm 3513DI options also visible). Critical technique: the 2383 LUT expects Cineon film-log input, NOT Rec.709/Gamma 2.4 — feeding it the wrong space makes it look too strong/wrong. Fix: place a CST immediately before the LUT converting Rec.709 Gamma 2.4 -> Rec.709 Cineon Film Log, which makes the emulation usable. Then select the CST+LUT pair and create a COMPOUND NODE (two nodes inside one) so the look's strength can be dialed 0-100 via the key/mix tool (he runs it at ~50% 'half mix'). You can right-click > show compound node and swap the LUT for any other film stock. The look node sits near the end of the tree, and ALL grading is done UNDERNEATH the look so you grade through it. He also keeps the look DISABLED when saving the tree, and on the clean kitchen clip leaves it off entirely for a neutral look. Texture/grain handled in separate Texture/Spare nodes (Resolve FX Texture / Film Grain seen in the FX library)."

## Numeric settings seen on screen
- Pivot 0.435 (primaries contrast pivot, default, visible across f024/f032/f034)
- Saturation 50.00 (primaries default, left unchanged)
- Hue 50.00 (default)
- Lum Mix 100.00 (default)
- Contrast 1.000 (slider baseline before adding)
- Offset wheel R/G/B 24.01 / 24.91 / 25.63 (during Canon non-log balance, f032)
- Offset wheel R/G/B ~25.00 / 25.00 / 25.00 (neutral reset)
- Lift 0.00 0.00 0.00 / Gamma 1.00 1.00 1.00 / Gain 1.00 1.00 1.00 (wheels at default)
- Color Boost 0.00, Shadows 0.00, Highlights 0.00 (defaults)
- Output CST: Tone Mapping Method = DaVinci, Adaptation = 9.00, Gamut Mapping = None
- Broadcast safe IRE levels -20 - 120 (Color Management panel)
- Scopes scale 10-bit 0-1023 (parade/histogram Y axis)
- Film look mix ~50% ('half mix') via compound-node key
- Input CST examples seen: Canon Cinema Gamut + Canon Log3; REDWideGamutRGB + RED Log3G10; Sony S-Gamut3.Cine + S-Log3; Blackmagic Design Pocket 4K Film Gen 4; Rec.709/Rec.709 (iPhone & unknown-camera fallback)

## Teaching points
- A 'fixed node tree' is a saved, pre-labeled node structure you drop on EVERY clip. Its real value is discipline: it forces a methodical grade order (balance -> contrast -> sat -> fine-tune -> windows -> look) so results are consistent. You don't have to use every node — empty ones are reminders.
- The two-CST bookend is the core idea. Node 01 lifts the camera's native log/gamut into a big neutral working space (DaVinci Wide Gamut/Intermediate); node 02 at the very end converts to your display (Rec.709 Gamma 2.4). You ALWAYS grade beneath node 02 so your eyes see the corrected display image, not raw log.
- To support ANY camera you change ONE thing: node 01's input color space. Canon Log3, Sony S-Log3, RED, BMRAW, ARRI, iPhone — same tree, different input. If you don't know the profile, use Rec.709/Rec.709.
- Use MANUAL color management (CST nodes under DaVinci YRGB), not Resolve's automatic RCM/ACES — that's what makes camera-switching instant and keeps you in control.
- Trust the CST's auto-ticked OOTF/tone-map checkboxes: Resolve knows whether each space is a camera, working, or display space and ticks correctly. Swapping spaces flips the ticks automatically.
- Build the foundation (Balance/Exposure, Contrast, Saturation) and get it looking good BEFORE branching. If the foundation is wrong, don't move forward — everything downstream inherits it.
- Parallel nodes (Alt/Option+P + layer mixer) let each fine-tune (temp, highlights, warper, curves) and each power window pull from the CLEAN foundation instead of stacking on each other — this is the secret to consistent, independent adjustments.
- Mostyn grades on the OFFSET wheel for balance and the HDR palette for most moves; he leaves Pivot at 0.435 and Saturation at 50 default, adding contrast/sat sparingly to taste.
- Film LUTs like Kodak 2383 expect Cineon film-log input, not Rec.709 — put a CST (Rec.709 Gamma2.4 -> Rec.709 Cineon Film Log) BEFORE the LUT, then wrap both in a compound node so you can dial the look strength 0-100. Grade UNDERNEATH the look so you grade through it.
- iPhone/Rec.709 gotcha: Rec.709 source footage has no camera gamma — set input gamma to Rec.709, NOT Gamma 2.4 (Gamma 2.4 is a DISPLAY gamma, not a source gamma).

## Quotable claims
- "a slightly broken down version of my fixed broadcast node tree that I use on every single job ... for BBC Amazon ITV branded content whatever it is I use the same fixed node tree" (00:00:00)
- "if your camera profile is not in this list I promise you that this fixed node tree will work for any camera profile" (00:00:31)
- "I'm not going to work in the automatic color management, we're going to use color space transforms ... we do want to work color managed but we want to do it manually not automatically and this is the key to being able to switch between these different camera profiles really easily" (00:01:03)
- "our timeline color space wants to be a larger color space ... I work in DaVinci Wide Gamut Intermediate ... and my output color space needs to match my display which is currently calibrated to Rec.709 gamma 2.4" (00:01:18)
- "basically DaVinci Resolve knows what it's doing with these settings so it's going to apply the correct transform function ... you can trust what DaVinci Resolve is doing with those tick boxes ... just trust it, it works" (00:05:02)
- "this one feeds this one feeds this one and then we're feeding off into these various branches and this gives us a really good solid consistent grade — this is kind of one of the secrets to my grading being very consistent" (00:07:56)
- "the input into here needs to be a different color space ... they're expecting cineon film log not gamma 2.4" (00:10:34)
- "if it doesn't look good you shouldn't move forward, this is the point at where you want this good because ... we're going to branch off into these different nodes" (00:14:45)
- "the only thing we have to change is this [node 01 input color space] ... by using the fixed node tree you're staying disciplined and you can switch between your different camera profiles really easily" (00:16:50)
- "don't put gamma 2.4 because it's not got a gamma, it's Rec.709 ... the gamma 2.4 is a display gamma, it's not a source camera gamma" (00:21:27)

## Key frames
- `f025.jpg` — The cleanest full node-tree map: serial spine CAM>DWG/01 -> BAL/EXP/03 -> CONTRAST/04 -> SAT/05, the TEMP/HDR/WARPER/CURVES parallel cluster (06/08/09/10) into a layer mixer, TRIM/11, the PW1/PW2/PW3 power-window cluster (12/14/15), then TEXTURE/16 + SPARE/17. The definitive structure diagram.
- `f010.jpg` — The OUTPUT CST (node 02): DaVinci Wide Gamut / DaVinci Intermediate IN -> Rec.709 OUT, with Apply Forward OOTF and Use White Point Adaptation auto-ticked, Adaptation 9.00 — the 'grade under display space' bookend.
- `f008.jpg` — The INPUT CST (node 01): Canon Cinema Gamut input with the Input Gamma dropdown open (Canon Log3 etc.) — the single setting you change per camera.
- `f024.jpg` — Primaries color wheels (Lift/Gamma/Gain/Offset near-neutral), Pivot 0.435 and Sat 50.00 on the slider row, the full tree with the appended Kodak film-look node, and the Film Looks LUT browser listing Rec.709 Kodak 2383 D55 — primaries technique + look design in one frame.
- `f028.jpg` — The LUT right-click menu open to LUTs > Film Looks > Rec.709 Kodak 2383 D55, plus the node context menu (compound node workflow) — how the film emulation is applied.
- `f046.jpg` — RED clip with the input CST set to REDWideGamutRGB / RED Log3G10 -> DaVinci Wide Gamut / DaVinci Intermediate — proof the same tree adapts by changing only node 01.
- `f049.jpg` — On-screen teaching text 'IF YOU ARE UNSURE OF CAMERA PROFILE USE INPUT OF REC 709/REC 709' over the iPhone beach clip with the CST input set to Rec.709 — the universal fallback rule.
- `f003.jpg` — Project Settings > Color Management panel: Color science DaVinci YRGB, the 'Use separate color space and gamma' checkbox highlighted, Timeline/Output color space rows, LUT slots empty, Broadcast safe -20-120 — the manual color-management setup.
