# frenchie-masterclass — analysis

*Source: Frenchie, 7K views · framesRead: 26*

## Overview
A full real-world commercial grade built live from scratch on a charity landing-page video, mixing Rec.709 (colorful festival B-cam) and BMD log A-cam (the girl) footage. The whole job runs under DaVinci YRGB Color Managed (DRCM) rather than node-level CSTs, so the lesson is really two things: (1) set up color management correctly and assign per-clip input transforms, then (2) build a reusable "look" as a tidy, labeled node tree and copy/match it across every shot. Frenchie's signature moves: do contrast and shadow shaping in the HDR (Log) color wheels (not the primary wheels) to avoid sneaky saturation, fake a film print with split-toning via RGB curves instead of a LUT, refine hue with the Color Warper, "rub in" density with an Overlay-composite node keyed back via Key Output, finish with a power-window vignette, and on the hero shot add Face Refinement targeting only the eyes. A narrative color arc ties it together: warm/glowy festival vs. cold/desaturated bedroom to mirror the character's mental state, resolving to a hopeful, eye-lit final shot.

## Order of operations
1. 0. PROJECT SETUP — Project Settings > Color Management: Color science = DaVinci YRGB Color Managed; Color processing mode = Custom; Input color space = Blackmagic Design 4K Film Gen 3 (the A-cam); Timeline color space = DaVinci WG/Intermediate (chosen to give the lower-quality Rec.709 footage 'more room'); Timeline working luminance = HDR 1000; Output color space = Rec.709 Gamma 2.2 (web delivery on screens).
2. 1. PER-CLIP INPUT TRANSFORMS — Because everything is DNxHR HQX (no camera metadata survives), manually assign each clip's Input Color Space: the colorful festival clips = Rec.709 / Rec.709 Scene; all the 'girl' (grayish log) clips = right-click > Input Color Space > Blackmagic Design 4K Film Gen 3, so they de-log to what the camera saw. (Tip: if DRCM auto-interprets wrong, force it back to Rec.709 Scene.)
3. 2. WORKFLOW NOTE — A colorist first builds ONE look, shows it to the director for approval, THEN applies/matches it across all shots. The pre-approved looks were already saved in the gallery (PowerGrades); the video recreates the approved look node-by-node.
4. 3. NODE 1 (parallel node) 'BALANCE' — exposure + neutral balance in the HDR/Log wheels: pull Offset down (~21 i.e. ~0.21 below mid) to tame overexposure; raise only the LUMINANCE of Lift to ~0.01 (not the color, so blacks lift naturally); add warmth via HDR Global wheel axis at minus 0.01.
5. 4. NODE 2 'CONTRAST' — add pop using CONTRAST in the HDR wheels (NOT primary), raised slightly to ~1.024, because HDR-wheel contrast separates whites/blacks photometrically without adding compensating saturation.
6. 5. NODE (inserted BEFORE balance) 'HDR' — set this node's working gamma to Linear (HDR wheel three-dots > gamma > Linear) to 'simulate the heaviness of the lights'; then pull HDR Light down to minus 0.04 to knock down highlights on faces/foreheads and recover sky/tent detail.
7. 6. SECONDARIES BEGIN — SPLIT TONE node: fake a film print with RGB curves (unlinked Y/R/G/B). Remove red from shadows, compensate by lowering green + raising blue in shadows (cooler shadows); then add red to highlights + remove blue from highlights (warm, slightly yellow-green highlights). Alt/Option-drag keeps points on the linear baseline for precision.
8. 7. 'HUES' node — Color Warper (Hue vs Sat/Hue) at Hue resolution 16: push blue sky toward cyan, then nudge that cyan slightly toward green ('cyan sky' for cinematic feel against the warm look).
9. 8. 'OVERLAY' density node — new node after the parallel chain, right-click > Composite Mode > Overlay (adds density+contrast). Then dial it back via Node Key > Key Output Gain down to ~134 (~1.34 scaled, i.e. reduce opacity) so it 'rubs in' naturally.
10. 9. VIGNETTE 'VIGN' — Power Window (circle) around the subject, relink, push the window up slightly so they stand out; add an Outside node and pull it DOWN to darken everything outside the window for a 3D feel.
11. 10. MATCH TO A-CAM — middle-click to copy/paste the whole grade onto the BMD log footage of the girl, then readjust: re-warm the split tone (bring red back, raise blues), raise Offset, add DENSITY (a ColorSlice/color-slice saturation node) because subtractive saturation is more filmic than additive; final balance warmth via PRIMARY wheels Temp ~60 / Tint ~6 (image read slightly green).
12. 11. NARRATIVE GRADE — interior/bedroom shots intentionally graded COLD + desaturated vs. warm festival, to externalize the character's struggle (high mood-contrast between scenes).
13. 12. HERO FINAL SHOT — same look chain PLUS a FACE REFINEMENT node (Beauty/Eyes only): no skin smoothing, only Eyes — Sharpening 0.376 and Eyebag Removal 0.147 — to draw attention to the light already in her eyes = visual 'hope' beat.
14. 13. No final ungraded export shown; stops at the graded timeline.

## Node tree
A serial chain with one PARALLEL split, built and labeled left-to-right. Festival/base look (final order seen in f037/f041/f045): node 02 'HDR' (Linear gamma, Light down) → 'BALANCE' (offset/lift/global warmth) → 'CONTRAST' (HDR contrast) feeding into a parallel mixer with a lower branch carrying 'SPLIT TONE' (RGB curves) → 'HUES' (Color Warper) → 'DENSITY' (ColorSlice sat) → recombine → 'OVERLAY' (Composite mode Overlay, keyed back via Key Output) → 'VIGN' (power-window vignette + Outside node). Hero shot adds a 'FACE REFINEMENT' node at the tail. Nodes are individually named (Balance, Contrast, HDR, Split To…, Hues, Density, Overlay, Vign, Face Ref) — labeling/organization is itself part of the taught method. ~9-10 nodes total on the hero shot.

## Scopes
- **Waveform (RGB Parade-style, overlaid)** — Docked bottom-right the entire grade (labeled 'Waveform', scale 0-1023 in 10-bit). Used as the constant reference while pulling Offset/Lift/Contrast — watching the trace spread between blacks and whites when adding HDR contrast, and confirming shadows lift to a natural floor rather than crushing. · targets: Blacks lifted just off the floor (the ~0.01 luminance-lift move); highlights kept from clipping the top (the HDR Light minus 0.04 move to pull faces/sky off the ceiling). No explicit IRE numbers spoken — read by shape, not value.
- **Histogram / Curves-Custom backdrop** — The Curves panel shows the live RGB histogram behind the curve, used while drawing the split-tone points so she can see which tonal region (shadow spike vs. highlight tail) each curve point sits over. · targets: Shadow point placed over the large left histogram spike (festival blacks); highlight red boost placed over the upper tail (sunlit faces).
- **Vectorscope** — Not prominently shown on screen in the frames read; hue decisions were made visually + via the Color Warper grid rather than a called-out skin-line vectorscope read. · targets: No explicit vectorscope skin-line target stated.

## Primaries
Primaries are done almost entirely in the HDR (Log) color wheels, deliberately NOT the primary wheels. Exposure: OFFSET pulled down to ~0.21-below-mid to fix overexposure; LIFT raised by luminance only to ~0.01 (color untouched) to lift blacks naturally. Warmth: HDR Global wheel axis at minus 0.01 (subtle, 'less heavy than Temp'). Contrast: HDR-wheel CONTRAST ~1.024 with Pivot reading 0.435 on screen (the panel showed Contrast 1.000 / Pivot 0.435 baseline before the nudge) — chosen over primary contrast specifically because primary contrast auto-adds saturation while HDR contrast only separates luma. A pre-balance node is switched to Linear working gamma to make highlight roll-off feel like real light, then HDR LIGHT pulled to minus 0.04 to tame highlights. Final per-clip warmth on the log A-cam uses the PRIMARY wheels at Temp ~60 / Tint ~6.

## Secondaries
Three secondary stages, all as separate labeled nodes. (1) SPLIT TONE via unlinked RGB curves (no qualifier) — a hand-built film-print emulation: shadows pushed cool (less red, less green, more blue), highlights pushed warm (more red, less blue → yellow-green). (2) HUES via the Color Warper (Hue-Saturation grid, resolution 16) — blue sky steered toward cyan then slightly green. (3) DENSITY via a ColorSlice / Color-slicer node raising saturation subtractively (Sat read 1.14 on screen) for a more filmic, 'not adding light' result. Qualifier-based isolation is NOT used for the look; the only qualifier-style targeting is the Face Refinement on the hero shot. Power Window: a circular vignette window (with an Outside node) for subject separation.

## Skin tone
No explicit vectorscope skin-tone-line technique is taught (she doesn't park skin on the I-line). Skin is protected indirectly: the HDR Light pull-down (minus 0.04) stops foreheads/faces shining; subtractive density keeps skin from going neon; and on the hero shot she deliberately does NOT smooth or desaturate skin ('I really like her skin, she's beautiful') — Face Refinement Skin Grading values are all left at 0.000. So the skin philosophy here is restraint + tonal control, not a numeric hue-angle target.

## Color management
DaVinci YRGB Color Managed (DRCM / RCM), NOT ACES and NOT node-level CSTs — chosen so you don't manage color per-node. Project Settings > Color Management: Color processing mode = Custom; Input = Blackmagic Design 4K Film Gen 3; Timeline = DaVinci WG/Intermediate (picked to give weak Rec.709 footage more headroom); Working luminance = HDR 1000; Output = Rec.709 Gamma 2.2 for web/screen delivery; Input DRT = DaVinci, Output DRT = DaVinci; 'Use inverse DRT for SDR-to-HDR', 'white point adaptation', and 'color space aware grading tools' all checked; Graphics white level 100 nits; Dolby Vision OFF. Because all clips are DNxHR HQX proxies with no camera metadata, each clip's Input Color Space is set MANUALLY (Rec.709 Scene for festival cams, BMD 4K Film Gen 3 for the log girl footage).

## Look design
The look is a self-built faux film print rather than a purchased LUT or film-emulation LUT — she explicitly rejected the print-emulation LUTs as 'too strong' and wanted to keep manual control, so she recreated a print via split-toning (cool shadows / warm highlights). Cyan-leaning sky is a deliberate cinematic signature. The Overlay-composite 'density' node is her trademark for instant contrast+density that she then keys back. The macro design is a narrative split-look: warm, glowy, welcoming festival exteriors vs. cold, desaturated interior/bedroom shots to mirror the subject's mental-health arc, resolving on a warm, eye-lit hopeful hero shot. Pre-built approved looks live as PowerGrades in the gallery; the grade is copied (middle-click) and shot-matched across the timeline.

## Numeric settings seen on screen
- Project: Color science = DaVinci YRGB Color Managed; Color processing mode = Custom (f013)
- Input color space = Blackmagic Design 4K Film Gen 3 (f013)
- Timeline color space = DaVinci WG/Intermediate (f013)
- Timeline working luminance = HDR 1000 (f013)
- Output color space = Rec.709 Gamma 2.2 (f013)
- Graphics white level = 100 nits; Mastering display 4000-nit P3 D65 ST2084 (f013)
- BALANCE: Offset pulled down to ~0.21; Lift luminance raised ~0.01; HDR Global axis minus 0.01 (transcript/f021)
- HDR/Log wheels panel baseline shown: Contrast 1.000, Pivot 0.435 (f021, f039, f047, f048)
- CONTRAST node raised to ~1.024 in HDR wheels (transcript)
- HDR node: gamma set to Linear; HDR Light pulled to minus 0.04 (transcript)
- OVERLAY node: Composite Mode = Overlay; Key Output Gain reduced to ~134 (~1.34) (transcript/f035)
- DENSITY node (ColorSlice): Sat ~1.14 shown (f041)
- Final A-cam balance: Primary Temp 60.0, Tint 6.00 (f042)
- Curves Soft Clip Low 50.0 / High 50.0 visible (f019,f023)
- FACE REFINEMENT (hero shot) Eyes: Sharpening 0.376, Brightening 0.000, Eye Light 0.000, Eyebag Removal 0.147; all Skin Grading = 0.000; Skin Texture mode 'Beauty Automatic'; Effect Strength 1.000 (f048, f049)
- Color Warper Hue resolution = 16 (f033, f043)

## Teaching points
- Color management first, grading second: in DRCM you only need to set the project transforms once and assign each clip's input space — no per-node CSTs. Proxies (DNxHR) strip camera metadata, so you must tell Resolve what each clip is (Rec.709 vs BMD Film) or the de-log is wrong.
- WHY DaVinci WG/Intermediate as timeline space: a wide working space gives weak/low-bit footage 'more room' to be pushed without breaking.
- The single most transferable trick: do contrast and tonal shaping in the HDR (Log) color wheels, not the primary wheels — primary contrast secretly adds saturation; HDR/Log contrast separates luma cleanly. Same idea for using a Linear working gamma on a node to get natural highlight roll-off.
- Lift the LUMINANCE of lift, not the color — keeps blacks natural without tinting shadows.
- You can build a film 'print' look without any LUT: unlink RGB curves and split-tone (cool shadows, warm highlights). LUT print-emulations are often too strong and cost you control.
- Density two ways: (a) an Overlay composite-mode node for instant contrast/density that you then dial back with Key Output gain; (b) subtractive saturation (ColorSlice) which is more filmic than additive saturation because you're not 'adding light'.
- Build ONE look, get director approval, THEN match it across shots (middle-click copy). Keep the node tree labeled and tidy — organization is part of the craft.
- Color is storytelling: deliberately split warm-vs-cold between scenes to externalize a character's emotional state, and use a targeted Face Refinement (eyes only, no skin smoothing) to direct the viewer's eye to a 'hope' beat.
- Restraint on skin: leave good skin alone — refine eyes (sharpen + eyebag), not the complexion.

## Quotable claims
- "I like to put my color science to DaVinci YRGB Color Managed so you don't have to bother doing color management on a node-based level." (06:03)
- "We work in a DaVinci Wide Gamut/Intermediate color space because we have Rec.709 footage and it gives us more room to handle footage that's also not really in great quality." (06:49)
- "Output is Rec.709 Gamma 2.2 because we're delivering on the internet — gamma 2.2 is best to be viewed on computer and smartphone screens." (07:07)
- "When I receive the footage and the edit, the first thing I do is build a look to present to the director, and after I have approval I grade." (07:53)
- "If I raise contrast in the primary wheels it adds saturation to compensate, but if I raise contrast in the HDR wheels it only separates the whites and the blacks and doesn't add any colors." (12:41)
- "When you change to a linear color space it tells DaVinci you want a space that simulates the heaviness of the lights." (13:29)
- "I wanted something kind of like a film print but not a film print per se — the film-print emulations were a bit too strong, and I still wanted to handle and manage my film emulation, so I recreate a print with the split toning." (14:50)
- "I really use overlay a lot because it gives me density and contrast straight away." (19:03)
- "I prefer density / the color slice because the saturation is subtractive instead of additive, which makes a better, more real and more filmic image — you're not adding light to the overall image." (22:20)
- "I want to represent what the character is feeling — strong contrast between the warmth of the festival and the cold of this lady alone in her room." (24:11)
- "I haven't put any beauty — I really like her skin. I only went to eyes: more sharpening, more brightening, and raised the eye-bag removal so her eyes are sharper and she has more light, a strong message that the character is getting better and seeing hope." (26:36)

## Key frames
- `f013.jpg` — The Project Settings > Color Management panel fully legible — the entire DRCM setup: DaVinci YRGB Color Managed, Custom mode, Input = BMD 4K Film Gen 3, Timeline = DaVinci WG/Intermediate, HDR 1000, Output = Rec.709 Gamma 2.2. The single best frame for color management.
- `f015.jpg` — The complete labeled node tree in one view (HDR, Balance, Contrast, Split To, Hues, Overlay, Vign) over the festival-crowd shot — the architecture of the whole look.
- `f021.jpg` — HDR/Log color wheels open with Lift wheel and the Contrast 1.000 / Pivot 0.435 readout, plus the Balance node — demonstrates doing primaries in the HDR wheels.
- `f030.jpg` — The split-tone RGB curves mid-build: unlinked R/G/B points pulled in shadows and highlights — the hand-built faux film print.
- `f033.jpg` — The Color Warper Hue-Saturation grid (resolution 16) steering blue sky toward cyan — the 'Hues' secondary.
- `f041.jpg` — Cold interior/street scene with the full node chain incl. DENSITY node and the ColorSlice panel (Sat ~1.14) + primary wheels — the narrative cold look and subtractive density.
- `f045.jpg` — Hero final-shot node tree with every node including VIGN and the Face-Refinement node (10), 'LET'S REVIEW THE FINAL SHOT' card — the complete finished chain.
- `f048.jpg` — Face Refinement panel with exact Eyes values: Sharpening 0.376, Eyebag Removal 0.147, all Skin Grading 0.000 — the eyes-only hero finish.
