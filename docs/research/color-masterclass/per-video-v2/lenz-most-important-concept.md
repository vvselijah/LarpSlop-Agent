## lenz-most-important-concept — Eric Lenz - The MOST IMPORTANT Concept in Colour Grading

**Tool:** Multi-app demonstration of one concept (order of operations / signal flow). Apps shown: Affinity Photo (pixel layer demo), Final Cut Pro (Color Wheels / Custom LUT / Adjustment Clips), Premiere Pro (Lumetri Color), and DaVinci Resolve 19 (Color page, node trees + Color Space Transform). Demo footage: Sony FX3 S-Log3 / S-Gamut3.Cine misty-river/foggy-fisherman silhouette clip ("6332935_Silhouette Mist Woods River…"). Heavy use of hand-drawn paper cards as the teaching device — the bulk of the video is conceptual, not numeric.

### Workflow order
The recommended grading signal chain, taught at the end as paper cards (25:12–25:57). Signal flows left→right (clip-level processed first, then timeline-level):

1. **NR** — Noise Reduction first (operates before later ops amplify noise) (25:12)
2. **EXP/CON** — Exposure & Contrast ("a close second"; this is "shaping the light") (25:24)
3. **BAL** — Balance / white balance / overall mood (25:27)
4. **SECONDARIES** — skin, masks, qualified corrections (25:34)
5. **LOOK** — creative look (25:44)
6. **CST to Rec.709** (or other delivery) — output transform is the LAST node (25:44)

Level grouping (25:50–25:57): **CLIP-LEVEL** = NR → EXP/CON → BAL → SECONDARIES → (shaping light); **TIMELINE-LEVEL** = LOOK → CST-to-Rec.709. In Resolve, clip-level is processed first, then timeline-level (10:02). Caveat: this documented order is NOT necessarily the order in which you physically work (23:26).

Core CST color-management pattern (the "sandwich," 22:14–22:15): input CST → grade node (middle) → output CST, optionally widening into an even larger working space: Log → input CST → **DaVinci Wide Gamut / DaVinci Intermediate** (largest space) → output CST → Rec.709 (22:46, 22:52, 23:00). Exposure/contrast must precede the LUT/CST so log is graded before it is clipped (15:58, 23:56).

### Demonstrated parameters (number @ mm:ss)

**DaVinci Resolve — Primaries neutral baseline (scale anchors):**
- **Offset (neutral)**: 25.00 / 25.00 / 25.00 (Resolve Offset; 25.00 = NEUTRAL, NOT a black lift — proven by before/after vs the cast node) (08:24, 09:39, 20:33, 22:15)
- **Gain (neutral)**: 1.00 / 1.00 / 1.00 (08:24, 09:21, 22:15)
- **Lift / Gamma (neutral)**: 0.00 / 0.00 / 0.00 each (08:24, 09:21)
- **Contrast**: 1.000; **Pivot**: 0.435 (08:24, 20:33, 22:15)
- **Saturation**: 50.00; **Hue**: 50.00; **Lum Mix**: 100.00 (08:24, 09:21, 22:15)
- **Color Boost / Shadows / Highlights / Mid-Detail**: 0.00; **Temp**: 0.0; **Tint**: 0.00 (08:24, 09:21)

**DaVinci Resolve — demonstrated grade moves:**
- **Blue color-cast via Offset**: 16.73 / 24.97 / 46.46 (R/G/B) — strong blue cast (B raised to ~46, R lowered to ~17, G ≈ neutral); deleting this node returned Offset to 25.00/25.00/25.00 (09:21 → 09:39)
- **Negative master Offset (crush demo)**: -30.10 / -30.10 / -30.10 — heavy downward pull, signal crushed to black floor ("nothing comes back") (21:04)
- **Wrong-order extreme Gain**: 3.70 / 3.95 / 3.70 (~3.7–4× boost; neutral = 1.00) — extreme/destructive move required when grading in the wrong color space (21:36) [flag: medium-confidence read of Gain numeric readout]
- **Correct-order Gain (middle node of CST sandwich)**: 1.50 / 1.50 / 1.50 (moderate ~+50%, no clipping) — contrast with the 3.7–4× wrong-order value (22:22)
- **Reset transitional Gain readout**: -1.65 / -1.65 / -1.65 on the secondary readout row during reset (21:41) [flag: secondary-row Gain scale ambiguity]

**DaVinci Resolve — Color Space Transform (CST) settings:**
- Input Color Space = **Sony S-Gamut3.Cine**, Input Gamma = **Sony S-Log3**; Output Color Space = **Rec.709**, Output Gamma = **Gamma 2.4** (08:24, 08:31, 20:53)
- Tone Mapping Method = **DaVinci**; **Adaptation = 9.00**; Gamut Mapping Method = **None**; Use White Point Adaptation = checked; Apply Forward OOTF = checked (08:24, 20:53, 21:47)
- Second-CST (working-space) variant: Input Sony S-Gamut3.Cine / S-Log3 → Output **DaVinci Wide Gamut / DaVinci Intermediate**; **Swap** button reverses IN/OUT for the output-side node (22:05 → 22:06)
- "Use timeline" can be set for all four CST fields (21:47)

**Final Cut Pro — Color Wheels neutral defaults (scale note: NOT Resolve):**
- **Temperature = 5000.0** (Kelvin-style neutral), **Tint = 0**, **Hue = 0°**, **Mix = 100.0%**, four wheels (Global/Shadows/Midtones/Highlights) centered (06:27, 08:00, 16:35, 18:28)
- Container/Transform neutral: Blend Mode Normal, Opacity 100.0%, Scale 100%, Position 0px, Rotation 0°, Color Conform = Automatic (06:13, 06:56)
- Demonstrated move: lower **Global** wheel brightness ("offset") to pull blown highlights back into range (17:25–17:28)
- Custom LUT (S-Log3→Rec.709 conversion): LUT = "S-Log 3_S-Gamut3.Cine_to_rec709", Convert Input = Rec.709, Output = Rec.709, Mix = 100.0% (17:00)

**Premiere Pro — Lumetri Basic Correction neutral defaults (scale note: NOT Resolve):**
- **Temperature = 0.0**, **Tint = 0.0**, **Saturation = 100.0** (range 0–200, neutral 100), Exposure/Contrast/Highlights/Shadows/Whites/Blacks = 0.0; Intensity 50.0 (European decimal comma in UI) (10:17, 18:41, 19:35)
- Input LUT loaded as conversion: "S-Log 3_S-Gamut3.Cine_to_rec709.cube" (7.4 MB) (18:42, 18:49)

**Affinity Photo (tool-agnostic intro demo):**
- Image 3840×2160 @ 72 dpi; layer Opacity 100%, Blend Mode Normal; Curves on a normalized 0–1 axis (Max: 1) — NOT a 0–1023 scope (03:43, 04:11)

### Distinctive techniques / opinions
- **Thesis:** order of operations / signal flow is "the most important concept in colour grading" — the backbone of every good workflow; re-ordering steps changes the result (commutative-law analogy a+b=b+a fails for grading) (02:17, 26:07).
- **Tool-agnostic:** "Which tools you use really doesn't matter" — the same order concept demonstrated identically across Affinity, FCP, Premiere, and Resolve (03:43).
- **Signal-flow direction differs by app — memorize per app:** Resolve node tree flows **left→right** (09:09); FCP / Premiere Effect Controls (inspector) flow **top→bottom** (top = processed first) (06:56, 11:07, 17:06); but a **timeline/adjustment-clip stack flows bottom→top** — opposite of the inspector — so the topmost adjustment clip wins (18:15, 18:17, 18:19).
- **Key insight — grade BEFORE the LUT/CST:** a LUT/CST clips everything outside its range, and that information is lost permanently; once baked, lowering exposure afterward recovers nothing ("nothing will come back") (15:32, 15:48, 18:49). Putting exposure/Offset BEFORE the transform restores "all your precious dynamic range" (13:32). Demonstrated both ways in every app.
- **LUTs/CSTs require a specific INPUT to give a correct OUTPUT** — log must be exposed so middle grey lands correctly; over/under-exposure breaks the Rec.709 mapping (14:23, 14:45, 15:06). 18% / middle grey is the reference anchor (14:45).
- **CST "sandwich" / wider-working-space rationale:** transform from a large space into an even larger one (DWG / DaVinci Intermediate) to do all adjustments so "nothing will be clipped and nothing will be lost," then transform out to Rec.709 (22:46, 23:00). The **Swap** button builds the matching output-side CST (22:06).
- **Alternative to manual CST nodes:** enable color management in Project Settings (DaVinci YRGB Color Managed / RCM) instead of placing CST nodes (23:15).
- **Clip-level vs timeline-level division of labor:** NR/exposure/balance/secondaries are done at the clip level (per shot); LOOK + delivery CST live on the timeline-level node tree (applied across the whole timeline) (25:50–25:57).
- **Adjustment-layer equivalents are cross-app:** FCP "Add Adjustment Clip" (⌥A), Premiere "Adjustment Layer," Resolve timeline-level node tree — all the same role (07:22, 17:40, 20:04, 09:25).
- **Wrong order forces extreme values:** grading in the wrong color space needed ~3.7–4× Gain vs ~1.5× when ordered correctly — a diagnostic that your order is wrong (21:36 vs 22:22).

### ENGINE: what a headless auto-grader should adopt
- **Enforce a fixed pipeline order in `correct.py` / orchestration:** NR → exposure/contrast → balance → secondaries → look → output transform. Make order a hard contract, not an emergent property — this is the video's central, repeatedly-proven claim (25:12–25:44).
- **Color-management sandwich in `tonemap.py` / `luts.py`:** apply input transform (camera log/gamut → wide working space) FIRST, do all grading in the wide space, apply output transform (→ Rec.709 / delivery) LAST. Never bake the display LUT before grading — clipped data is unrecoverable (15:48, 18:49, 22:14).
- **Grade-before-clip guard:** any exposure/offset correction must run upstream of the display transform. Add an assertion/log if a destructive transform precedes an exposure op (13:32, 15:58).
- **Wide working space default:** use DaVinci-Wide-Gamut / DaVinci-Intermediate-equivalent (large) as the internal grading space so adjustments don't clip; only narrow to Rec.709 at output (22:46, 23:00).
- **CST presets to hardcode:** Sony S-Gamut3.Cine + S-Log3 → Rec.709 / Gamma 2.4, DaVinci tone mapping, Adaptation 9.00, Gamut Mapping None (08:24, 20:53). Provide a generic input-gamut/gamma → working-space → Rec.709 path; expose a "swap" to auto-generate the inverse output transform (22:06).
- **Scope/scale awareness in `measure.py`:** normalize per-app/scale conventions before reading values — Resolve Offset neutral = 25.00 (NOT 0), Gain neutral = 1.00, Lift/Gamma = 0.00, Sat/Hue = 50.00; FCP Temperature neutral = 5000.0 K, Mix in %; Premiere Saturation neutral = 100 (0–200), Temp/Tint = 0. Do not treat 25.00 as a lift or 100 as a ceiling (08:24, 16:35, 10:17).
- **Order-sanity heuristic:** if achieving a target requires extreme control values (e.g. Gain ≫ ~2×, or a large negative Offset crushing to floor), flag likely wrong operation order / wrong color space rather than accepting the destructive grade (21:04, 21:36 vs 22:22).
- **Expose middle-grey / exposure pre-check:** before applying the output transform, verify middle grey / exposure sits in the LUT's expected input range; warn if over/under-exposed log will break the Rec.709 mapping (14:23, 14:45, 15:06).
- **Two-stage scope targets:** measure on the wide working space during grading and again on the final Rec.709 output (0–100 IRE) to confirm no clipping was introduced by the output transform (22:54, 22:22).
