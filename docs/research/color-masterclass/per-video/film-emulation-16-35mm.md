# film-emulation-16-35mm — analysis

*Source: serr, 836K views (HIGH) · framesRead: 27*

## Overview
A practical, options-first masterclass on emulating 16mm/35mm motion-picture film in DaVinci Resolve 17. The thesis (00:35) is that the film "look" is not one setting but the SUM of many physical characteristics — negative stock, exposure, print process — so emulation = stacking many small node-level effects, not flipping a LUT. The creator demonstrates FOUR methods and explicitly frames the video as a buyer's-guide rather than an ad for his own product: (1) his own paid PowerGrade + LUT (FilmVision-style, built on a Cineon/ARRI LogC pipeline); (2) a from-scratch FREE build using only stock DaVinci tools + the built-in Film Looks print-emulation LUTs; (3) a third-party PowerGrade — Juan Melara's Kodak 2383 print emulation (and a mention of Tom Bolles' CinePrint16, $59.99); (4) the paid Dehancer Pro 4.0.0 plugin ($400). The load-bearing teaching is Method 2 (the free from-scratch build) because it exposes the actual node architecture and order of operations. Core pipeline for every method: convert camera log into a known working/print space via Color Space Transform, do exposure + white balance FIRST, then layer film characteristics (softness/diffusion, grain, halation, vignette, dust/damage, gate weave, film breath), then a print-emulation LUT/look, then export with grain-preserving settings. The footage graded is mixed-camera (Fujifilm F-Log, DJI Osmo Pocket 2, etc.) night/exterior city + a subway interior. Throughout, the waveform scope is the primary reference. Skin tone and the vectorscope skin-line are NOT explicitly taught here — this is a look-design tutorial, not a primaries/skin masterclass, so secondaries are used only for the vignette power window.

## Order of operations
1. 1. COLOR MANAGEMENT / INPUT TRANSFORM first: drop a Color Space Transform (CST) to convert camera log into the working/print space the look expects. Method 1 LUT expects Rec.709 input (so a 'TO REC.709' CST precedes the LUT). Method 2 print-emulation LUT expects a Cineon Film Log input, so the CST is Input Rec.2020 / Fujifilm F-Log -> Output Rec.709 / ARRI LogC->Cineon Film Log. If DaVinci's CST lacks your camera's space/gamma, substitute a conversion LUT (he uses 'GC Titans / d2x709' for DJI Osmo Pocket 2) (06:26-07:12).
2. 2. GAMUT MAPPING fix: in the CST, set Tone Mapping and especially Gamut Mapping Method = Saturation Compression to kill clipped/artifacting saturated highlights (e.g. a pink light) (08:51-09:23, Saturation Knee 0.900 / Max 1.000).
3. 3. EXPOSURE node: correct brightness BEFORE anything creative. He drops Offset, lifts Gamma slightly, adds Contrast (demonstrated: Offset ~13.25, Gamma +0.02, Contrast 1.092) (09:38-10:08).
4. 4. WHITE BALANCE node: fix WB, then push it creatively toward the intended mood (he adds a greenish-orange tint for the subway scene) (10:08-10:25).
5. 5. SOFTNESS / diffusion: Gaussian Blur node (Pro-Mist / diffusion-filter emulation). 16mm ~150 radius, 35mm ~50-80; he uses 120 (10:25-10:56).
6. 6. GRAIN: DaVinci Studio Film Grain (16mm vs 35mm presets with their own softness/detail/grain); free alternative = a grain overlay (10:56-11:28).
7. 7. HALATION: compound node — Layer node set to composite mode ADD, CST F-Log->Linear in, Linear->F-Log out, isolate highlights with a curve, then blur with R/G channels raised and Blue lowered (red/orange glow around lights) (11:28-13:17).
8. 8. VIGNETTE: circular Power Window pushed outside frame, max softness, INVERTED, then drop Offset in Primaries (more controllable than the Vignette OFX) (13:17-14:03).
9. 9. DUST / DAMAGE: Film Damage OFX with everything zeroed except Dirt (color white, density 1, size 1, blur 0) (14:03-14:52).
10. 10. LOOK / PRINT-EMULATION LUT last: the creative color identity — his Looks node (3 looks at 50 key-output, adjustable) or DaVinci's Film Looks print LUTs, or Kodak 2383 PG, or Dehancer profile. Order of operations is stressed as mattering 'a lot' (07:34-09:38).
11. 11. EXPORT: 4K timeline + 4K export, restrict data rate to 100,000 kb/s so YouTube compression doesn't destroy grain (21:31-22:22).

## Node tree
"Method 1 (paid PowerGrade) full serial chain (f011/f012): 01 CONVERSION (CST) -> GRAIN (compound: 16mm/35mm) -> HALATION (compound) -> PRO-MIST -> DSS WARMTH -> COLOR DENSITY -> VIGNETTE -> DUST -> GATE WEAVE -> FILM BREATH -> EXPOSURE (11) -> WHITE BALANCE (12) -> SATURATION (13) -> FADE (14, 'Log Grade/Custom Curves') -> WHITES (15) -> BLACKS (16) -> LOOKS (17) -> LUT (18). Grain compound (f009) = SOFTNESS -> DETAIL -> GRAIN (separate 16mm vs 35mm nodes). Looks compound (f013) = Warm Love -> Cine Green -> Tungsten Blue, serial, each a 50-key-output look. Method 2 (free from-scratch, f021/f031/f035): 9 serial nodes 01-09 — SOFTNESS (Gaussian Blur) -> GRAIN (DaVinci Film Grain OFX) -> HALATION (compound) -> VIGNETTE (circle power window) -> DUST (Film Damage OFX, dirt only) -> EXPOSURE (06) -> WB (07) -> CST (08) -> LUT (09, Film Print Emulation). HALATION compound internals (f026/f028): node 01 -> splits to a layer/parallel; layer node composite mode = ADD; CST in (gamma F-Log->Linear) and CST out (Linear->F-Log) sandwich a highlight-isolating Curve + an unlinked Blur (R 0.82 / G 0.66 / B 0.40). Method 3 reuses Method 2's exact node tree (grab still -> apply) and swaps the LUT for the Kodak 2383 PowerGrade compound. Method 4 (Dehancer): just 01 CST (Rec.709) -> 02 Dehancer Pro OFX node."

## Scopes
- **Waveform (RGB parade overlay)** — The only scope visible the entire video, docked bottom-right with a 0-1023 (10-bit) vertical scale and gridlines at 128/256/384/512/640/768/896. Used to watch where shadows/mids/highlights land while setting Offset/Gamma/Contrast and to confirm the print LUT isn't clipping. After the Cineon-log CST (f020/f021) the trace is lifted and low-contrast (log), and after the EXPOSURE+contrast node (f022) the blacks sit down near the bottom and highlights spread up — the visual proof contrast was added. · targets: No explicit numeric IRE targets are stated; he reads it qualitatively (blacks low, a contrasty spread he personally prefers). The faded-film looks deliberately LIFT the bottom of the waveform off 0 (raised blacks).
- **Vectorscope** — Not shown/used in this tutorial. · targets: Skin-tone line not taught here.
- **Histogram / Parade (separate)** — Not separately used; the waveform shows R/G/B simultaneously which he uses as a de-facto parade. · targets: n/a

## Primaries
"Primaries are used sparingly and only for CORRECTION, not the look (the look comes from the LUT/print emulation). On the EXPOSURE node (f022) he works the Primaries-Bars/Wheels: drops OFFSET (master wheel) so blacks sit down, nudges GAMMA up ~+0.02 across RGB, and raises CONTRAST to 1.092 around the default Pivot 0.500 (Pivot left at 0.500 throughout). Default/neutral wheels read Lift 0.00, Gamma 0.00, Gain 1.00, Offset 25.00 (f017). He uses OFFSET (the log-style master shift) for exposure rather than Lift, which is correct for log footage. White-balance is done on a separate dedicated node via Temp/Tint, then pushed creatively (green-orange). For the VIGNETTE he again uses Primaries Offset (dropped) but gated by a power window. In Method 2's Kodak 2383 PG he does NOT use primary wheels for contrast — he goes into the LUT's internal Curve node with Editable Splines ON to dial contrast inside the print emulation itself (f038)."

## Secondaries
"Secondaries here are minimal and purpose-built, not skin work. The ONLY qualifier/window used is the VIGNETTE: a CIRCLE power window (Window palette, Circle shape) scaled larger than the frame (Size 64.06, Aspect 71.04 in f030), softened heavily (Softness 1 = 2.07), then INVERTED so the effect lives in the corners, with Primaries Offset dropped to darken the edges — he explicitly prefers this over the Vignette OFX because the OFX is 'really hard to get a usable result out of.' Halation is effectively a luminance-qualified secondary done with a curve isolating highlights (not the HSL qualifier). No skin isolation, no HSL qualifier pull, no tracking is demonstrated."

## Skin tone
"Skin tone and the vectorscope skin line are NOT explicitly taught in this video. He mentions only in passing (05:39) that his three built-in 'Looks' were each 'balanced for skin tones' across lighting scenarios — i.e. the skin-balancing is baked into his paid Looks, not demonstrated as a technique. There is no vectorscope skin-line pull, no target hue/angle, no qualifier-based skin isolation shown. This is a deliberate scope choice: the video is look-design/film-emulation, so it leans on print-LUT color science to handle skin rather than manual skin grading."

## Color management
"Project works in YRGB (NOT RCM/ACES) with per-clip Color Space Transforms doing all conversions — the conscious choice so each method's LUT/PG receives exactly the input it expects. Method 1: CST converts camera footage TO Rec.709 (the LUT expects Rec.709 in); internally everything is built around converting INTO ARRI LogC ('probably the best log profile to work on'). For F-Log footage no CST is needed because the PowerGrade is pre-configured to F-Log. Method 2 (free print-emulation): CST Input Color Space Rec.2020, Input Gamma Fujifilm F-Log -> Output Color Space Rec.709, Output Gamma Cineon Film Log (because the built-in Film Print Emulation LUT expects a Cineon input); ARRI LogC is offered as an alternative output gamma, noted as better for overexposed footage. Gamut Mapping Method = Saturation Compression (Saturation Knee 0.900, Saturation Max 1.000) inside the CST to fix saturated-highlight artifacts; 'Use White Point Adaptation' checked. When a camera's space/gamma is absent from the CST list, a conversion LUT replaces the CST. LUTs are installed via Project Settings > Color Management > LUT folder (create subfolder, paste .cube, Update Lists). PowerGrades imported via the Gallery, right-click Apply Grade."

## Look design
"(see lookDesign field above)"

## Numeric settings seen on screen
- CST (Method 2): Input Color Space Rec.2020, Input Gamma Fujifilm F-Log, Output Color Space Rec.709, Output Gamma ARRI LogC then Cineon Film Log (f016/f020/f021)
- CST Gamut Mapping Method = Saturation Compression; Saturation Knee 0.900; Saturation Max 1.000 (f016)
- CST Tone Mapping = Luminance Mapping; Adaptation 9.00; Use White Point Adaptation checked (f016)
- EXPOSURE node demonstrated: Contrast 1.092, Pivot 0.500, Gamma +0.02 (RGB), Offset 13.25 (RGB) (f022)
- Primaries default/neutral reference: Lift 0.00 / Gamma 0.00 / Gain 1.00 / Offset 25.00; Contrast 1.000; Pivot 0.500; Sat 50.00; Hue 50.00; Lum Mix 100.00 (f017)
- Softness Gaussian Blur radius 120 (talked 150 for 16mm, 50-80 for 35mm) (f008 ~ R/G/B 0.50)
- Halation Blur unlinked: Red 0.82, Green 0.66, Blue 0.40 (f028)
- Vignette circle window: Size 64.06, Aspect 71.04, Softness1 2.07, Opacity 100, inverted (f030)
- Dust/Film Damage: Dirt color white, Density 1, Dirt Size 1, Dirt Blur 0, everything else 0
- Looks node Key Output 0.500 (50%); Key Input Gain 1.000 (f013)
- Dehancer Pro 4.0.0: Profile CineStill 800T; Black Point -3.03; White Point 100.0; Print Exposure 0.000; Tonal Contrast 0.0; Color Density 0.0; Saturation 100.0 (f043)
- Dehancer Halation/Bloom panel: Background Gain 80.0, Local Diffusion 15.0, Global Diffusion 15.0, Amplify 40.0, Hue 50.0, Impact 80.0; Bloom Highlights 80.0 (f045)
- Dehancer Input: Fujifilm X-T3, F-Log; Defringe 50.0 (f042)
- Export: 4K timeline + 4K export, data rate restricted to 100,000 kb/s (21:31-22:22)
- DaVinci CST output-gamma dropdown options seen: Cineon Film Log, Canon Log 1/2/3, BMD Film/Video Gen5, DaVinci Intermediate, DJI D-Log (f020)

## Teaching points
- The film 'look' is a SUM, not a setting. Build it as a stack of small node effects (grain, halation, softness, vignette, dust, gate weave, film breath) plus a print-color LUT — never expect one LUT to do it all (00:35, 03:35).
- ALWAYS color-manage your input first. A LUT/print emulation only works if it receives the input it was authored for. Use a Color Space Transform to convert camera log into that space (Rec.709 for a Rec.709 LUT; Cineon Film Log for a print-emulation LUT). If your camera isn't in the CST list, use a conversion LUT instead (03:02, 06:26, 08:05).
- Order of operations matters 'a lot.' Correct exposure and white balance BEFORE adding characteristics, and apply the look/print LUT LAST (09:38).
- For LOG footage, use OFFSET (the master log-style shift) for exposure rather than Lift — seen demonstrated on the EXPOSURE node (Offset 13.25) (09:53).
- Read the waveform to confirm contrast and avoid clipping. After a Cineon-log CST the trace is lifted and flat; adding contrast pushes blacks down and spreads highlights — you watch this happen on the scope (f020->f022).
- Fix saturated-highlight artifacts (e.g. a blown pink light) with Gamut Mapping = Saturation Compression inside the CST, not by desaturating manually (09:06).
- Halation is highlights-only red/orange bleed: isolate highlights with a curve, blur them, and weight the blur to Red/Green over Blue — built in linear light (CST F-Log->Linear and back) with an ADD composite (11:28-13:17).
- Build vignettes with an inverted, heavily-softened circular power window + dropped Offset, not the Vignette OFX — far more controllable (13:32).
- Film is not 'super saturated' — its richness comes from color DENSITY (subtractive saturation baked into print stocks), so reach for density/print color over cranking the Saturation slider (04:53).
- Faded-film looks come from LIFTING the blacks (raising the bottom of the waveform) via dedicated fade/contrast-lowering nodes (05:08).
- Make looks reusable and dialable: store them in a node at a fixed Key Output (e.g. 50%) so you can scale intensity per shot, and save the whole chain as a PowerGrade so you don't re-add the LUT every time (05:39, 06:11).
- A rebuilt PowerGrade (e.g. Juan Melara's Kodak 2383) beats a baked LUT because you can open it, see how the print emulation is constructed, and learn/modify it — flexibility + education (16:41, 18:12).
- Grain dies to YouTube compression — shoot/finish 4K, export 4K, and restrict the data rate (~100,000 kb/s) so the grain survives encoding (21:31).

## Quotable claims
- "There's a lot that goes into replicating 16 or 35mm film... the negative stock, the way it was exposed, the print process — it all creates its own unique look." (00:35)
- "The reason we're converting our footage into ARRI LogC is because that's probably the best log profile to work on." (03:19)
- "This LUT is expecting a Rec.709 input, which is why I have a color space transform here." (03:02)
- "When dealing with these nodes, order of operation matters a lot." (09:23)
- "A lot of times we think film is super saturated, but most times it's down to just the color density and the richness of the colors." (04:53)
- "This [Kodak 2383 PG] is just a rebuilt version of the LUT... it allows you more flexibility and you can actually see the characteristics of the film print and learn from it." (16:41)
- "Use 4K footage and export at 4K because YouTube's compression isn't as bad on 4K as on 1080p... restrict this to 100,000 so your quality is high enough that YouTube's compression won't entirely kill your grain." (21:46-22:22)
- "For the output gamma you're going to put your Cineon Film Log because this is a film print emulation and it's expecting a Cineon input." (08:35)

## Key frames
- `f011.jpg` — The complete Method-1 paid PowerGrade node tree spread out — every film-characteristic node labeled (CONVERSION, GRAIN, HALATION, PRO-MIST, COLOR DENSITY, VIGNETTE, DUST, GATE WEAVE, FILM BREATH, then EXPOSURE/WHITE BALANCE/SATURATION/FADE/WHITES/BLACKS, LOOKS, LUT). The single best map of 'film look = stacked characteristics.'
- `f016.jpg` — The Color Space Transform settings panel: Input Rec.2020 / Fujifilm F-Log, Output ARRI Alexa / ARRI LogC, Tone Mapping Luminance, Gamut Mapping = Saturation Compression with Knee 0.900 / Max 1.000 — the color-management core.
- `f020.jpg` — The CST output-gamma dropdown open with 'Cineon Film Log' being selected (Input Rec.2020/F-Log -> Output Rec.709), teaching why a print LUT needs a Cineon input. Waveform shows lifted low-contrast log trace.
- `f022.jpg` — The EXPOSURE node with on-screen values Contrast 1.092, Gamma +0.02, Offset 13.25 — the demonstrated primaries correction — and the waveform showing blacks sitting down after contrast.
- `f028.jpg` — The HALATION compound node internals: a parallel/layer structure with ADD composite, CST nodes converting F-Log<->Linear, and the unlinked Blur (R 0.82 / G 0.66 / B 0.40) that tints the highlight bleed red-orange.
- `f030.jpg` — The VIGNETTE built as an inverted circular Power Window pushed outside the frame (Size 64.06, Softness 2.07) with Offset dropped — the 'better than the OFX' vignette method.
- `f036.jpg` — Juan Melara's Kodak 2383 PowerGrade opened up into its component nodes (Hue&Sat, Luma, Luma, Blue, Curve, Shadow, D55 WP) — the 'learn from a rebuilt print emulation' moment.
- `f049.jpg` — The final 4-up split comparison: DaVinci FPE Kodak 2383 D55 LUT vs Juan Melara Kodak 2383 PG vs Film Vision PG+LUT vs Dehancer 500T — same exposure/WB, showing how each method interprets color differently.
