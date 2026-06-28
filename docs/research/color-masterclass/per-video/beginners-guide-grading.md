# beginners-guide-grading — analysis

*Source: Bill Blakely, 250 views (LOW - weight lightly) · framesRead: 24*

## Overview
A clean, mechanics-first beginner walkthrough of a primary color-correction workflow on the Resolve color page, taught entirely through scopes rather than by eye. It defines the full pipeline — primary grading (normalization -> color balancing -> shot matching), then secondary grading (deferred to another video), then creative look — and demonstrates each stage twice: once with the Primaries (color wheels) palette and once with the Curves palette. Three footage sets are used: a warehouse two-shot (normalization + red-cast removal), three desert stock clips (shot matching to a hero shot), and two office clips (curves-based match). It closes with two simple creative looks (cool/blue and warm) built on the color wheels and propagated across matched shots by dragging a look node / re-grabbing a still. No color management (RCM/ACES/CST), no secondaries (qualifier is used only as a measurement pointer, not for isolation), and no skin-tone-line / vectorscope work are taught — those are explicitly out of scope. Default Resolve project (Rec.709, no input/output transforms shown).

## Order of operations
1. 1. PRIMARY GRADING begins with NORMALIZATION — set luminance/contrast first to preserve detail and create depth.
2. 2. Luminance pass: switch waveform to Y (luma) channel, uncheck Colorize, so only brightness is shown.
3. 3. Set highlights: bring top of trace to ~the 2nd graticule line from the top (just under clipping) using Gain; raising past it blows out / loses detail.
4. 4. Set shadows: bring bottom of trace to between 0 and the 1st line (about halfway) using Lift; pushing too low 'crunches' shadows and loses detail.
5. 5. Refine midtones with Gamma; fine-tune Contrast + Pivot (pivot darkens/brightens while holding contrast), add Mid/Detail, nudge Saturation.
6. 6. COLOR BALANCING — switch waveform back to RGB, enable Colorize; look for a color cast (a channel predominance, or a non-white trace over something that should be neutral).
7. 7. Add a NEW serial node labelled 'balance' so normalization isn't disturbed; introduce the complementary color in the affected tonal range (Gain wheel for a highlight cast, etc.) until the neutral object's trace goes white. Color Bars are an easier alternative to the wheel indicator.
8. 8. SHOT MATCHING — pick a HERO shot (one with elements common to all shots), normalize/balance only it; grab a still (or wipe a timeline clip) to set a split-screen reference; use the PARADE scope; on a new 'shot match'/'match' node line up each channel's trace to the reference, channel by channel and tone by tone.
9. 9. CREATIVE LOOK last — only after shots are matched, add a 'look' node on one clip, then copy that node to the others so they stay matched.

## Node tree
Serial node chain, one labelled node per stage, built left to right: NORMALIZE -> BALANCE -> (SHOT) MATCH -> LOOK. Nodes are added via right-click on a node -> Add Node -> Add Serial, and named via right-click -> Node Label (seen on screen: 'Normalize' f028, 'Shot Match' f034/f039, 'Match' f042/f044, plus 'Corrector 1' in the node-graph keyframe panel). The teaching reason for separate serial nodes is non-destructive staging: balance on a fresh node so normalization isn't disturbed; look on a fresh node so it can be copied to other clips and reset independently. Shift-D toggles ALL nodes (full before/after); Cmd/Ctrl-D toggles the current node.

## Scopes
- **Waveform (Y / luma mode)** — Vertical axis is luminance 0 (pure black, bottom) to 1023 (pure white, top); trace replicates the frame left-to-right, top=highlights, middle=midtones, bottom=shadows. Settings: click Y, UNCHECK Colorize so it shows only brightness. Waveform slider dims/brightens the trace; Graticule slider adjusts the scale. · targets: Highlights: top of trace at the 2nd graticule line from the top (just below 1023 clip). Shadows: bottom of trace between 0 and the 1st line (~halfway). Stay inside these to preserve detail during correction (rules can be broken later for a look).
- **Waveform (RGB / Colorize on)** — Same graph but R/G/B traces drawn in color; where R=G=B they overlap into WHITE. Used to detect a color cast: a channel predominance, or place the qualifier over something that should be neutral and check whether its trace is white. · targets: A neutral object (white wall, paper rolls, area under a window) should read as a WHITE trace. In the warehouse the white paper rolls read red-predominant = red cast; office read green-predominant = green cast.
- **Parade (RGB)** — Three side-by-side graphs, one per channel (R,G,B), each 0-1023, each replicating the image left-to-right. Lets you compare per-channel amount/intensity and is THE scope for shot matching because you can see each channel's position independently. · targets: For matching: make each channel's trace in the clip-to-match line up with the same channel's trace in the reference, separately for the sky band and the ground band. Goal is to approximate, not match exactly; ignore trace regions that have no counterpart in the reference.
- **Histogram (behind the Curves graph)** — Shown as the grey background of the curves graph: pixel count per luminance level, black on the left, white on the right; used to decide where to place a curve control point. · targets: In the curves examples most pixels sat on the left (shadows), guiding where to add control points to redistribute tones.

## Primaries
Four color wheels in Primaries-Color Wheels: LIFT (mostly shadows, some midtones, least highlights), GAMMA (mainly midtones), GAIN (mostly highlights, then midtones, least shadows), OFFSET (whole image uniformly). Each wheel has a luminance DIAL under it (drag left=darker, right=brighter) plus the color ring indicator. Demonstrated warehouse normalization landed at (read off f010): Lift master/R/G/B all 0.07, Gamma all -0.10, Gain all 0.95, Offset all 25.00, Contrast 1.000, Pivot 0.435 (Resolve default). Later refinement (f015) showed Contrast 1.048, Pivot 0.563, Mid/Detail 31.50, Saturation 52.80. Color balancing of a HIGHLIGHT cast uses the GAIN wheel (because the neutral object's trace sat high in the scope), dragging its indicator toward the complementary color (cyan to kill red) until the trace turns white; an easier route is the Color BARS view (per-channel vertical sliders) — lower the offending channel's bar, double-click the color swatch to reset. Tonal rule of thumb taught: pick the wheel whose tonal range matches WHERE the target trace sits (highlights->Gain, midtones->Gamma, shadows->Lift). Key shot-matching trick: set LUM MIX (bottom-right of Primaries) to 0 so the color sliders stop dragging luminance around while you balance channels.

## Secondaries
Secondary grading is explicitly DEFERRED to a separate video — not taught here. The Qualifier is used only as a measurement aid ('display qualifier focus' from the scope menu, then the eyedropper qualifier in the viewer) to point at a region and see WHERE it lands in the trace — never to isolate and grade a secondary. No power windows, no HSL keying, no tracking are demonstrated.

## Skin tone
Not taught. There is no vectorscope work, no skin-tone line, and no I-bar/11-o'clock skin target in this video. Color neutrality is judged entirely from the waveform/parade by checking that supposedly-neutral objects read as a white trace.

## Color management
None shown. The project runs in the default Resolve pipeline (effectively Rec.709, YRGB) — no RCM (Resolve Color Management), no ACES, no Color Space Transform (CST) node, no input/output transform, no working-space discussion. The scope scale is 0-1023 (10-bit Rec.709 video levels). This is a deliberately bare beginner setup; a knowledge base should flag the absence of a managed pipeline as a limitation of this source.

## Look design
(see lookDesign field above)

## Numeric settings seen on screen
- Scope scale 0 (black) to 1023 (white) — 10-bit Rec.709 levels
- f010 normalize: Lift 0.07/0.07/0.07/0.07, Gamma -0.10/-0.10/-0.10/-0.10, Gain 0.95/0.95/0.95/0.95, Offset 25.00/25.00/25.00, Contrast 1.000, Pivot 0.435
- f012: Lift 0.01, Gamma 0.93, Gain 0.93 (channels), Offset 25.00 — interim state
- f015 refined warehouse: Contrast 1.048, Pivot 0.563, Mid/Detail 31.50, Saturation 52.80
- f024 second example (subway/couch): Contrast 1.036, Pivot 0.473, Mid/Detail 60.50, Saturation 70.00
- Default unchanged fields seen repeatedly: Pivot 0.435, Mid/Detail 0.00, Hue 50.00, Lum Mix 100.00, Saturation 50.00, Contrast 1.000
- f036 color-bars match: Gain 1.00/0.74/1.00/1.00 (red gain lowered to 0.74) with Lum Mix set to 0.00
- f038 color-bars match further: Lift 0.00/0.00/0.04/-0.03, Gamma 0.00/0.00/-0.55/-0.46, Gain 1.00/0.74/0.97/1.02, Lum Mix 0.00
- f036/f038 Sizing-Input Sizing: Pan -1056.253, Tilt -71.000, Zoom 1.120, Rotate 0.000 (used to crop hero/match clips to comparable framing before matching)
- Curves Edit panel channel values shown as 100/100/100/100 (Y/R/G/B gains at default)

## Teaching points
- Scopes over eyes: 'scopes cannot be deceived' — every decision (exposure, cast, match) is verified on the waveform/parade, not judged by the monitor alone. This is the single biggest beginner takeaway of the video.
- Read the trace as the image: top=highlights, middle=midtones, bottom=shadows, and left-to-right = the frame left-to-right. Use the qualifier eyedropper to point at a region and watch where it shows up in the trace until this becomes intuitive.
- Correct luminance FIRST with Colorize off (Y mode), then color. Highlights to the 2nd line from the top, shadows between 0 and the 1st line — staying inside those preserves detail; exceeding them blows out or crunches.
- Which wheel to use = where the trace sits: highlights->Gain, midtones->Gamma, shadows->Lift, whole image->Offset. Pivot shifts brightness without changing contrast.
- A color cast = a non-neutral trace over something that should be neutral. Fix by adding the COMPLEMENTARY color (red<->cyan, green<->magenta, yellow<->blue) in the matching tonal range until that trace turns white. The color wheel in the palette IS the reference — no need to memorize complements.
- Work non-destructively in named SERIAL nodes (normalize / balance / match / look) so each stage is independent, toggleable (Shift-D vs Cmd/Ctrl-D), and copyable.
- Shot matching: choose a hero shot with common elements, grade only it, then line up parade traces channel-by-channel; set LUM MIX to 0 so color moves don't shove luminance around; crop with input/reference Sizing so only comparable regions are compared; aim to approximate, ignore non-corresponding trace regions.
- Curves equivalents: black point (bottom-left) and white point (top-right) set shadow/highlight; a mid control point sets midtones; isolate a single channel (R/G/B button) and raise/lower it to add/remove that color — lowering green adds magenta, etc. Watch for an overshoot (killing green produced yellow -> then add blue).
- Build the creative look LAST and copy the look node across already-matched shots so trying different looks stays easy and the match is preserved.

## Quotable claims
- "The aim of color correction is to create an even starting point for creative grading where all shots in the scene display visual continuity with consistent luminance and color." (00:00:00)
- "A basic color correction workflow begins with primary grading, which consists of normalization, color balancing, and then shot matching." (00:00:17)
- "We'll generally want to keep the highlights at around the second line from the top. Details are preserved at this level. Raising it higher causes the highlights to be blown out." (00:07:12)
- "For the shadows, we want the bottom of the trace to usually be somewhere between zero and the first line." (00:07:43)
- "To neutralize a color cast, the opposite or complimentary color must be introduced... Cyan is opposite red on the color wheel. There's no need to memorize the color wheel. It's right there in the primaries palette." (00:11:10)
- "That's the beauty of scopes. They cannot be deceived." (00:12:32)
- "A hero shot should have elements that are common to every shot. This makes matching the other shots to it easier." (00:20:11)
- "This will drive you insane as well as waste your time. To avoid this, I'll set lum mix in the bottom right of the primaries palette to zero." (00:24:45)
- "The goal is not to match the trace exactly, but to approximate it." (00:29:24)
- "Once clips are matched, provided you matched them before applying a creative look, trying out different looks is fairly easy." (00:35:37)

## Key frames
- `f010.jpg` — Primaries-Color Wheels fully legible during warehouse normalization: all four wheels with per-channel numeric fields (Lift 0.07, Gamma -0.10, Gain 0.95, Offset 25.00) plus Contrast 1.000 / Pivot 0.435 / Mid-Detail 0.00 / Saturation 50 — the cleanest read of the primaries technique.
- `f008.jpg` — Scopes Waveform settings popover: Y/CbCr/RGB tabs, the Colorize and Extents checkboxes, Waveform + Graticule brightness sliders, Show Reference Levels Low 0 / High 1023 — exactly how to put the scope into luma-only mode.
- `f011.jpg` — Y-luma waveform (Colorize off) of the warehouse shot during normalization — the monochrome trace used to set highlights to the 2nd line and shadows above 0.
- `f021.jpg` — Curves palette with the Y master curve and a midtone control point added over the histogram background; Edit panel R/G/B/Y channel buttons and 100 values — the curves-based normalization tool.
- `f026.jpg` — Curves color-balance move: the GREEN channel curve dragged down (top-right point lowered) to remove a green cast / introduce magenta, with the colored trace visible top-right — the curve equivalent of a complementary-color correction.
- `f028.jpg` — Node graph with the labelled 'Normalize' node and the 3-clip desert thumbnail timeline — establishes the hero-shot shot-matching setup and serial-node naming.
- `f030.jpg` — RGB Parade scope (three separate R/G/B graphs, 0-1023) — the scope used for shot matching and how each channel is read independently.
- `f034.jpg` — Desert shot-match: split-screen wipe in the viewer, the 'Shot Match' node, and the parade with the two clips' traces being aligned channel-by-channel — the core matching mechanic.
- `f036.jpg` — Primaries in COLOR BARS mode (per-channel vertical luma sliders, Gain red lowered to 0.74) alongside Sizing-Input Sizing (Pan -1056.253, Tilt -71.000, Zoom 1.120) — color-bars matching plus the crop-to-compare trick, with Lum Mix 0.
