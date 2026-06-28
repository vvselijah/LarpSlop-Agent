## content-creators-indepth — Content Creators - In Depth DaVinci Resolve Tutorial (2026)

**Tool:** DaVinci Resolve Studio 20 (PUBLIC BETA) (footer confirmed @09:54, @19:44). Project "DaVinci Training YT" (export user /Users/connorsmith @64:36). Source footage: Sony S-Log3 / S-Gamut3.Cine, H.264 High 4:2:2 L5.1, 3840×2160 vertical, 23.976 fps, 10-bit (@08:58, @37:12). This is a beginner end-to-end EDIT tutorial; the actual color-grading content is a small fraction (two short Color-page passes plus a power-window cut-out). Most of the corpus is Edit-page Transform/audio/captions/transitions/deliver and is explicitly NOT color.

### Workflow order
Stated "level one" beginner order (title-card overview @15:46): 1) Frame the clip → 2) Color grade the clip → 3) Audio adjustments. The grading method demonstrated:
1. Apply a conversion LUT first as the technical base (S-Log3/S-Gamut3.Cine → Rec.709) on the single corrector node 01 — the LUT does the heavy contrast lift, not the wheels (@19:26, @19:44).
2. Make "small tweaks" in Primaries Color Wheels after the LUT: Lift (shadows) → Gamma (midtones) → Gain (highlights), tonal-range hierarchy explained as a pyramid Lift=base / Gamma=middle / Gain=top / Offset=whole (@21:06).
3. Propagate the grade to all clips at once via Edit-page Paste Attributes (Color Correction checkbox) (@32:20).
Compositing/masking pass (later chapter): single corrector node 01 → draw a Pen/Curve Power Window around the subject → Tracker (Window mode) to follow the subject → composite over a gradient plate (@80:50–@84:44).

### Demonstrated parameters (number @ mm:ss)
Neutral baselines (DaVinci defaults, repeatedly confirmed):
- **Primaries top bar**: Temp 0.0, Tint 0.00, Contrast 1.000, Pivot 0.435, MD 0.00 (@19:54, @37:12, @81:14)
- **Lift / Gamma neutral**: 0.00 per channel; **Gain neutral**: 1.00; **Offset neutral**: 25.00 (explicitly "= NEUTRAL, not a black lift") (@20:26, @37:16, @44:22)
- **Sat 50.00, Hue 50.00, L.Mix 100.00; Col Boost 0.00, Shad 0.00, Hi/Light 0.00** (@19:54, @37:16, @81:14)
- **Curves – Custom neutral**: Y/R/G/B all = 100; **Soft Clip neutral**: Low 50.0, High 50.0, L.S. 0.0, H.S. 0.0 (@16:44, @19:26, @19:44)

Demonstrated grade moves (A-roll talking-head, after LUT):
- **Lift (over-pushed demo)**: 0.24/0.24/0.24/0.24 — washed/milky on purpose to show shadow lift (@21:36)
- **Lift (backed off)**: 0.01; **Gamma**: −0.02 ("it was just a little too hot") (@21:56, @23:14)
- **Final A-roll correction**: Lift 0.01, Gamma −0.01, Gain 0.97 (highlights pulled below 1.00), Offset 25.00 (@23:18)

Per-clip B-roll grades (mostly slight Offset-master brightening; Offset neutral = 25.00):
- **Offset 32.35 master** (slight brighten) (@44:14)
- **Lift 0.05 + Offset 33.40** (@44:16)
- **Offset 29.65** (@44:32, @44:44); **Offset 30.35 + Gamma −0.01** (@44:40); **Lift −0.01 + Offset 32.35** (@44:38)
- **White-balance start**: Temp field selected at 0.0, about to warm (@44:56)
- **B-roll near-neutral with slight Offset 32.35** (@44:14)

LUT install/apply (Color page):
- Custom conversion LUT installed by dropping `.cube` into the matching Sony folder, then right-click → Refresh (@18:24, @18:58, @19:18)
- Applied LUT full name: **`CCT_SLOG3 Sgamut3cine to REC709`** (must start with "CCT") (@19:24); same LUT reused on B-roll ("Sony CST") (@37:16)
- Built-in Sony LUTs present: SLog3SGamut3.CineToCine+709, …ToLC-709, …709TypeA, …ToSLog2-709, Slog3.Cine_High_Contrast (@18:24)

Power Window / Tracker (cut-out compositing):
- **Window Transform neutral**: Size 50.00, Pan 50.00, Tilt 50.00, Rotate 0.00, Opacity 100.00; Softness Soft 1 0.00, Inside 0.00, Outside 0.00 (@81:24, @82:02)
- **Tracker – Window**: Pan/Tilt/Zoom/Rotate/3D all checked, mode Clip, engine Cloud Tracker (@82:34)
- Tracked deltas (motion output, not a set value): Pan −3.18 / Tilt −8.66 / Zoom 7.01 / Rotate −0.02 [flag: tracker deltas are computed motion, marked surprising — values are plausible per-frame offsets, recheck only if reused as inputs] (@82:40)

Non-color (Edit page — recorded so they're not mistaken for grade values):
- **Transform** uses Zoom 1.000 = neutral, Position/Rotation/Anchor 0.000 = neutral; reframes e.g. Zoom 1.300 / Position X 14 Y 18 (@23:24, @25:04), punch-in Zoom 1.900 / Position X 27 Y 244 (@37:08), rotated B-roll Zoom 0.790 / Rotation 90 (@40:54). These are geometry, NOT Gain (@25:04, @50:50 both flagged surprising) [flag: ~1.7–1.9 Transform Zoom can be mis-read as a color Gain magnitude — confirmed Transform-panel scale, not color]
- **Audio**: incoming ≈ −20 dB (@24:14); Normalize → True Peak, target −1.0 dBTP (@24:40); clip Volume +20.7 dB (@25:30); Fairlight Compressor Threshold −15.0 dB / Ratio 2.0:1 / Attack 1.4 ms / Release 93 ms, Limiter Threshold −21.0 dB (@25:42)
- **Project/timeline**: vertical 1080×1920, "Use vertical resolution" checked, Square pixels, 23.976 fps timeline+playback (@13:06–@14:08)
- **Captions**: Open Sans Semibold, Size 58, Position X 540 / Y 384→460, red badge background (@57:08–@57:36); AI Create Subtitles from Audio, max 18 chars/line (@56:32)
- **Deliver**: QuickTime / H.264, hardware accel, Timeline Resolution + Timeline Frame Rate (23.976), burn-in subtitles (@64:24–@65:10)

### Distinctive techniques / opinions
- **LUT-first as the grade**: ships a downloadable S-Log3→Rec.709 conversion LUT in his starter pack so beginners reach the look "way quicker"; the LUT carries the contrast and the wheels only do "small tweaks" (@17:32, @19:26).
- **Install custom LUTs by manufacturer folder + Refresh**: drop the `.cube` into the camera-matching folder (Sony) so it indexes next to the built-ins, then right-click Refresh (@18:24–@19:18).
- **Tonal-range mental model**: Lift = shadows/base, Gamma = midtones/middle, Gain = highlights/top, Offset = the whole mountain (@21:06).
- **Over-push then back off**: deliberately overdoes Lift (0.24, milky) to teach what it does, then dials to 0.01 — "it was just a little too hot" (@21:36→@21:56).
- **Restraint on B-roll**: most B-roll clips get only a tiny Offset-master brighten (~+5 to +8 on the 25-neutral scale) rather than full grades (@44:14–@44:44).
- **Batch-propagate the grade**: copy one graded clip, Option/Alt+V → Paste Attributes with Color Correction (+ Position/Zoom/Scale) checked to push the grade to many clips at once; "Maintain Timing" for keyframes (@32:20).
- **Record too-low audio over too-hot**: prefers ~−20 dB capture and lifts in post (@24:14).
- **Studio Power-Window tracking is far better than free**: Cloud Tracker conforms a hand-drawn pen mask to the moving subject; free version "struggles" (@82:34, @82:58).
- **Offset neutral is 25.00, not 0** — stated repeatedly so 25 isn't misread as a black lift (@20:26, @44:20).

### ENGINE: what a headless auto-grader should adopt
- **luts.py — input-transform first**: detect S-Log3/S-Gamut3.Cine source (codec metadata available: H.264 4:2:2, 10-bit, @08:58) and apply the matching log→Rec.709 conversion LUT as the technical base BEFORE any primary move; the conversion LUT, not the wheels, should supply the bulk of the contrast (@19:26). Keep a manufacturer→conversion-LUT registry (Sony S-Log3→Rec.709, plus Arri/Canon/Panasonic/RED/DJI categories enumerate the camera families to support @16:42).
- **correct.py — small post-LUT trim, in tonal order**: after the LUT, default to gentle moves only — shadow Lift ≈ +0.01, midtone Gamma ≈ −0.01, highlight Gain ≈ 0.97 was the colorist's settled correction (@23:18). Work Lift→Gamma→Gain order. Treat the over-pushed 0.24 lift as the do-NOT-exceed example (it goes milky) (@21:36).
- **Offset as a cheap global brightness knob**: for shot-to-shot leveling, a master Offset nudge (Resolve scale, 25.00 neutral; +5 to +8 observed) is the colorist's go-to for B-roll instead of a full grade — implement a single global-offset/exposure-match pass as the lightweight default (@44:14–@44:44).
- **Neutral constants for the value model (Resolve readout scale)**: Lift/Gamma 0.00, Gain 1.00, **Offset 25.00**, Contrast 1.000, Pivot 0.435, Sat 50.00, Hue 50.00, L.Mix 100.00, Curves Y/R/G/B 100, Soft Clip 50/50/0/0. Hard-code these so measure.py/scopes never misreport an offset of 25 as a lift or a 1.0 Gain as boosted (@19:54, @37:16, @44:22).
- **match.py — propagate one grade across a shot family**: emulate Paste Attributes "Color Correction" — grade a hero clip, copy its correction (and optionally transform) to sibling shots; expose a "maintain timing vs stretch" choice for any keyframed grade (@32:20).
- **scopes/measure.py**: no waveform/parade/vectorscope was ever shown in this video (scope_reading empty throughout; explicitly "none" @65:10) — this corpus gives no scope-target evidence, so do not derive numeric IRE/scope targets from it.
- **stylize.py / power windows**: subject-isolation via a tracked freehand window (pen mask + Cloud-Tracker, Pan/Tilt/Zoom/Rotate/3D) is the demonstrated path for treating subject vs background separately; an auto-grader's local-correction stage should similarly support a tracked subject mask before background-vs-foreground grading (@81:24–@82:40).
- **Caution / negative evidence**: the bulk of "numbers" in this source are Edit-page Transform (Zoom ~1.0 neutral) and audio dB — an extractor feeding the engine must filter by page (Color vs Edit) so a Transform Zoom of 1.7–1.9 is never ingested as a color Gain (@25:04, @50:50 flagged).
