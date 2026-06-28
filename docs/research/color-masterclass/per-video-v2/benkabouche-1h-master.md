## benkabouche-1h-master — Zakaria Benkabouche - 1h to Master Color Grading

**Tool:** DaVinci Resolve Studio 20 (Public Beta) (splash @03:01). Project "1h to Master Color Grading (Session)", single-user. Footage = mixed cinema sources: Blackmagic Cinema Camera 2.5K RAW CinemaDNG (12-bit, 2400×1350, 23.976 fps, 13 stops; @03:17, 03:33, 10:48) and RED Dragon 6K (REDcolor3 / REDWideGamutRGB-Log3G10; @20:54, 21:03), plus Apple ProRes 422 HQ clips (@21:43, 23:32). Camera-capture illustration uses a Panasonic body (V-Log, C4K 24p 4:2:2 10-bit; @09:58). Reference display: EIZO ColorEdge CG2700S via ColorNavigator 7 (@13:37, 15:21, 17:08). Optional hardware: DaVinci Advanced/Mini trackball panel.

### Workflow order
This is a teaching video, not a single linear grade; the demonstrated *setup* order is:
1. **Import + verify source** — Media page, inspect clip metadata/codec (DNG, fps, bit depth) before grading (@03:17, 03:33, 04:19).
2. **Build timeline** — Create New Timeline from selected clips; set timeline resolution/fps (@03:56, 04:00, 04:03); project master = 4096×2160 DCI, 23.976 fps (@04:47).
3. **Decode RAW correctly** — Project Settings > Camera Raw: pick RAW profile per camera, Full-res decode, decode-using source; verify the data decoded correctly (@04:49, 11:09–11:29).
4. **Set up color management (RCM)** — Project Settings > Color Management: choose Input color space (camera native wide gamut), Timeline working space (DaVinci WG/Intermediate), working luminance, Output color space + gamma (delivery); DaVinci DRTs; Save (@16:07–16:30, 18:24, 19:10–19:48, 21:17–21:21).
5. **Per-clip input overrides** for mixed-source clips whose metadata differs (right-click clip > Input Color Space) (@21:52–21:57).
6. **Then grade** on the Color page — Primaries (Gain/Lift/Gamma, Offset, Temp/Tint, Saturation), Curves (Custom + Hue-vs-Hue), Color Warper, HSL Qualifier; diagnose with scopes (Parade/Vectorscope/CIE) (@06:46 onward).
7. Deferred fixes noted (e.g. white-balance correction "later") (@22:21).

### Demonstrated parameters (number @ mm:ss)

**Scale anchors used throughout:** Primary-wheel Offset neutral = 25.00; Gain neutral = 1.00; Lift/Gamma/Contrast(adj) neutral = 0.00; Saturation neutral = 50.00 (0–100); Temp/Tint neutral = 0.00; Camera Raw decode sliders neutral = 0.00 (Sharpness default 10.00). Color Warper Center/Hue/Sat on its own normalized −1..1 / 0..1 scale.

- **Camera Raw decode defaults (project)**: Lift 0.00, Gain 0.00, Contrast 0.00, Sharpness 10.00, Highlights 0.00, Shadows 0.00, Color boost 0.00, Saturation 0.00 (@04:50). Same neutral block repeated @11:18 (Saturation/Midtone detail/Lift/Gain/Contrast 0.00).
- **Camera Raw profile/decode**: RAW profile ARRI → switched to CinemaDNG; Decode quality Full res.; Decode using Camera metadata (@04:49, 04:50, 11:13). White balance As shot → Custom; decode Color space Rec.709, Gamma 2.4; Highlight recovery ON (@11:18, 11:25, 11:28). Alt BMD-RAW decode: Color space Blackmagic Design, Gamma Blackmagic Design Film, Highlight recovery ON (@15:06). Per-clip CinemaDNG panel: Exposure 6500, Color temp 0.00 (@17:05).
- **Primaries — Gain (Y/R/G/B, neutral 1.00)**: all 1.00 (@06:46); R 1.62 / G 1.59 / B 1.63, master 1.00 (@07:38); blue isolated DOWN to 0.85, R/G/master 1.00 (@07:46); red isolated DOWN to 0.82, G/B/master 1.00 (@07:55); warm push R 1.52 / G 1.04 / B 1.00 / master 1.00 (@08:31). Hardware-panel Gain readouts: all 1.06 (@06:53); 1.11 and 1.06 (@13:57); RED channel 1.00 (@14:00, 17:10).
- **Primaries — Saturation (0–100, neutral 50.00)**: 50.00 (@06:46, 07:38); 10.47 = heavily desaturated (@07:43); panel readout 75.58 = boost (@17:29).
- **Primaries — Temp/Tint (neutral 0.00)**: Temp 240.0 slight warm (@08:32); Temperature 55.00 + Tint 7.30 (@14:00); panel Temperature 34.00 + Tint 9.10 (@17:10) [flag: panel "Temperature" scale ambiguous — readout units, not Kelvin]; Tint −22.70 toward green (@17:28).
- **Primaries — Offset / Pivot (Offset neutral 25.00)**: Offset 25.00/25.00/25.00 with Pivot 0.435 (@06:53, 08:40, 17:04); same Offset 25.00 ×3 + Pivot 0.435 + Gain 1.00 ×3 (@17:04).
- **Primaries — Lift / Gamma (neutral 0.00)**: Lift master 0.00, R/G/B 0.00; Gamma master −0.06 (tiny mids darken) (@17:04).
- **Primaries — Contrast / Pivot / Mid-Detail**: Contrast 1.000 (neutral), Pivot 0.435, Mid/Detail 0.00 (@21:43).
- **Global (4-way) wheel**: master 1.00, Exp 0.92 (slightly down), Sat 1.04 (slight boost), wheel X 0.00 Y 0.00 (@17:27).
- **Curves**: Custom curve near-identity with small midtone bump (@17:27, 08:33); Hue-vs-Hue bump over yellow/orange→green with a node in green (no numeric degrees shown) (@14:12); per-channel Y/R/G/B intensity readouts all = 100 default (@21:48).
- **Color Warper (Hue-Saturation; own −1..1 / 0..1 scale)**: Range select Hue 0.00, Sat 0.16, Luma 0.50, Auto Lock on, color space HSP (@09:07); Density 0.00, Den.Depth 0.00, Skin Center −0.363 Hue 0.000, others Center/Hue 0.000 (@17:17); master Saturation 1.00, Sat.Balance 0.00, Sat.Depth 0.00, Cyan Hue −0.143, per-zone strengths ~1.00/0.20/1.00/0.00 (@17:20).
- **HSL Qualifier**: Mid/Detail 0.00 (@08:40); Lum Mix 100.00 (@08:44).
- **Project master timeline**: 4096×2160 DCI, Square pixels, 23.976 fps (@04:47); custom timeline option ____×2160 (@04:03); Create-Timeline start TC 01:00:00:00, 1 video / 1 audio track (@04:00).
- **Color Management (RCM) — BMD configuration**: Color science DaVinci YRGB Color Managed, processing mode Custom; Input = Blackmagic Design Film Gen 1; Timeline = Rec.709 (Scene) (then DaVinci WG/Intermediate); Timeline working luminance SDR 100; Output = Rec.709 (Scene); Input DRT DaVinci, Output DRT DaVinci; inverse-DRT-for-SDR-to-HDR ON, white-point adaptation ON (@16:07–16:20).
- **Color Management — V-Log/BMD HDR pipeline variant**: Input BMD Film Gen 1 (gamut) + Blackmagic Design Film (gamma); Timeline DaVinci WG / DaVinci Intermediate; working luminance HDR 1000; Output Rec.709 / Gamma 2.4; Input+Output DRT DaVinci; "203 nits Rec.2100" OFF; inverse-DRT ON; white-point adaptation ON; color-space-aware grading ON; resize in Gamma (@19:10–19:22).
- **Color Management — P3 cinema variant**: Timeline DaVinci WG / DaVinci Intermediate, working luminance HDR 1000, Output P3-DCI / Gamma 2.6, "Use 203 nits reference for Rec.2100 HDR" (@18:24–18:29).
- **Color Management — RED mixed-source applied state**: Input REDWideGamutRGB/Log3G10; Timeline DaVinci WG/Intermediate; working luminance HDR 1000; Output Rec.709 Gamma 2.4 (@21:21). ACM path: DaVinci YRGB Color Management, Automatic color management ON, mode SDR Rec.709, color-science version 4.0 (@19:39–19:44).
- **Per-clip Input Color Space override**: default checked "Project – Blackmagic Design Film Gen 1"; RED-shot clips set to REDWideGamutRGB (pairs with Log3G10) (@21:52–21:57).

**Reference / spec values shown (not grading controls):**
- **V-Log code values (Panasonic spec)**: 18% grey = code 433, 0% black = 128, 90% white = 602 (10-bit); log toe lifts black off floor to ~code 128; OETF out = 5.6·in+0.125 below cut1, else c·log10(in+b)+d (cut1 0.01, b 0.00873, c 0.241514, d 0.598206) (@10:03, 10:04, 10:34).
- **Blackmagic Log3G10 constants**: a 0.224282, b 155.975327, c 0.01, g 15.1927; 18% mid-grey = 0.18 linear (@16:01, 16:04).
- **EIZO calibration target**: BT.709, gamma (EOTF) 2.40, white point D65 (6500 K), brightness 120 cd/m², BT.709 primaries R(0.6400,0.3300) G(0.3000,0.6000) B(0.1500,0.0600), Gamut Clipping off, ICC v4.2, Tone curve LUT (@13:37, 15:21, 17:08, 17:44). DCI-P3 target shown as gamma 2.60 paired with D65 (i.e. P3-D65) (@18:46) [flag: 2.60 gamma normally pairs with DCI white, not D65 — possible P3-D65 vs theatrical-DCI labeling].
- **EIZO Rec.2020 coverage**: Adobe RGB 99% / DCI-P3 99% / Rec.2020 80% (@13:12).
- **DaVinci Wide Gamut primary (red)**: CIE x 0.8000, y 0.3130; DWG = wide gamut + DaVinci Intermediate log encoding >9 stops above mid-grey (@17:22, 17:24).
- **Bit depth**: 12-bit = 4,096 tonal steps/channel (@14:23).
- **Scope scale**: video scopes read 10-bit code values 0–1023 (gridlines 0/128/256/384/512/640/768/896/1023) (@06:37, 09:37, 21:48), NOT IRE/%.

### Distinctive techniques / opinions
- **Get the pipeline right before touching a wheel.** The first ~21 min is decode + color-management setup; grading controls only appear after the source is correctly decoded and the gamut/gamma chain is configured (@04:49, 16:07, 21:17).
- **"Make sure it has been decoded correctly"** is an explicit verification step after RAW import (@04:38).
- **Teach grading as Y'RGB signal manipulation:** image = four signals Y + R + G + B; lowering Y → black; lowering RGB intensity → desaturated/B&W; raising it → more colorful (@06:33–07:20). Gain is framed as the single "intensity" control over those four signals (@06:46).
- **Shoot log or RAW for gradable data**, and prefer higher bit depth (12-bit RAW = 13 stops on the BMCC) (@09:58, 10:21, 10:48).
- **Color space = gamma (tone curve/EOTF) + gamut (color set)** — repeated as the core mental model (@17:40, 17:56, 18:13). Rec.709 ⇒ gamma 2.4; DCI-P3 ⇒ gamma 2.6 (@18:13, 18:24, 18:46).
- **Decode to a WIDE space, not a display space.** Decoding RAW straight to Rec.709 "deletes all the colors outside this tiny space"; choose the camera's native wide gamut (BMD Film Gen 1 / DaVinci WG) so out-of-gamut data survives (@15:09–15:11, 14:55, 16:51). Verbal estimate: a Rec.709 display shows only ~30% of the captured colors (@15:50) [flag: 30% is a spoken estimate, not an on-screen readout].
- **DaVinci Wide Gamut / Intermediate is the recommended working ("man-in-the-middle") space** between input and output (@16:51, 17:22).
- **Match input color space to source-camera metadata**, and use per-clip Input Color Space overrides for mixed-source timelines (BMD DNG vs RED REDWideGamutRGB/Log3G10 vs ProRes) (@21:03, 21:21, 21:52–21:57).
- **Diagnose log vs standard with the Parade:** flat/compressed mid-band = log (no clipping); full-height traces slammed to floor/ceiling = crushed/clipped standard profile (@09:19, 09:32).
- **Defer white-balance fixes:** an over-orange tungsten interior is flagged as a WB issue "to fix later," not corrected in place (@22:21).
- **Show-wide look direction:** cool, slightly-desaturated daylight exteriors vs warm/orange tungsten interiors with retained skin warmth, kept consistent across all shots (@23:29).
- Camera-raw "Highlight recovery" is left ON in every decode shown (@11:25, 15:06).

### ENGINE: what a headless auto-grader should adopt
- **scopes / measure.py**: Treat the working scale as 10-bit code values 0–1023, not IRE/%; map gridlines 0/128/256/384/512/640/768/896/1023 (@06:37, 09:37, 21:48). Implement a Parade-based log-vs-standard classifier: if R/G/B traces are compressed to a mid-band with no top/bottom touch → flag "log/flat, no clip"; if traces span full height with energy pinned at 0 and 1023 → flag "standard, crushed+clipped" (@09:19, 09:32). Add a CIE-chromaticity gamut check that reports what fraction of the source color cloud falls outside the target (Rec.709) triangle (@14:49, 15:50).
- **correct.py (color management first)**: Build a color-management stage BEFORE primaries — set Input gamut/gamma from camera metadata, convert to a wide working space (DaVinci WG / DaVinci Intermediate), then transform to delivery (Rec.709/Gamma 2.4 SDR, or P3-DCI/Gamma 2.6, or Rec.2020). Use camera→working→output as the canonical pipeline, with per-clip input overrides keyed off detected source (BMD Film Gen 1, REDWideGamutRGB/Log3G10) (@16:09, 19:10, 21:21, 21:52). Keep RAW "Highlight recovery" on, decode at full res (@11:25, 04:49).
- **tonemap.py / luts.py**: Encode the published log transfer functions as ground truth — V-Log OETF (cut1 0.01, b 0.00873, c 0.241514, d 0.598206; 18%→433, 0%→128, 90%→602) and Log3G10 (a 0.224282, b 155.975327, c 0.01, g 15.1927; 0.18 = mid-grey) for accurate log→linear and gamut transforms (@10:34, 16:01–16:04). Standard gamma anchors: Rec.709 = 2.4, DCI-P3 = 2.6, DWG primary red = (0.8000, 0.3130) (@18:13, 18:24, 17:24).
- **stylize.py (primaries scale contract)**: Hard-code Resolve neutral points so values are never misread — Gain 1.00, Offset 25.00, Lift/Gamma/Contrast-adj 0.00, Saturation 50.00 (0–100), Temp/Tint 0.00, Pivot ~0.435 default. Implement the demonstrated moves as primitives: per-channel Gain push for color cast (e.g. warm = R↑/G slight↑/B flat, @08:31), single-channel Gain pull to bias hue (B↓→yellow, R↓→cyan, @07:46/07:55), Saturation up/down via the 50-neutral scale (@07:43, 17:29).
- **match.py / look**: Adopt the teal-cool-exterior / warm-tungsten-interior split as a default editorial look profile, applied consistently across a shot set, with skin warmth preserved (@23:29). Use the Color Warper Hue-Saturation model (per-hue Center/Hue/Sat on −1..1/0..1) for targeted skin/secondary moves rather than broad saturation (@17:17, 17:20).
- **Pre-grade gate**: refuse/flag footage that is not log or RAW (low gradable headroom) and prefer ≥12-bit sources; surface bit depth and stop count from metadata before grading (@09:58, 10:48, 14:23).
