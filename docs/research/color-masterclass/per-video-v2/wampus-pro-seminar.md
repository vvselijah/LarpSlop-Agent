## wampus-pro-seminar — Wampus - DaVinci Pro Teaches Me the Color Page (Full Seminar)

**Tool:** DaVinci Resolve Studio 20, Color page. Project/timeline `COLOR_COURSE`. Co-grading session (Wampus + camera op Tim) on two main clips: a daylight-exterior disc-golf clip shot Canon Cinema Gamut / Canon Log 2 (one frame mentions Canon Log 3), and a darker sit-down interview clip. Media pool bins include Canon Flext / Apple Log / Canon E log sources; clip `A001_06141352_C051.mov`; reference source `Wampus_Camera.mov`. **Scale guard used throughout:** Offset wheel neutral = 25.00 (NOT a black lift); Gain neutral = 1.00; Lift/Gamma neutral = 0.00.

### Workflow order
1. **Identify the source** in a Color Space Transform (CST): set Input Color Space + Input Gamma to the camera's native space (e.g. Canon Cinema Gamut / Canon Log 2) (30:42–35:18).
2. **CST sandwich** — input CST converts camera → DaVinci Wide Gamut / DaVinci Intermediate working space; tail CST converts working space → Rec.709 / Gamma 2.4 (2.2 for web/YouTube) for delivery (37:16, 38:32, 50:12, 79:32). Build the second CST by copy/paste + swap input↔output rather than re-dragging the OFX (37:10, 45:34).
3. **Grade between the two CSTs**, in the wide working space (38:32, 45:58 — same gain move behaves differently pre- vs post-CST).
4. Optionally set a grading node's working **gamma to Linear** so Gain acts like a clean exposure/stop change with blacks anchored (50:26, 53:08–54:12, 70:30).
5. Evaluate against scopes throughout — primary set Waveform + Vectorscope, sometimes Parade; CIE Chromaticity for gamut (04:28, 22:12).

### Demonstrated parameters (number @ mm:ss)
**Neutral baselines (reference defaults):**
- **Lift / Gamma / Gain / Offset neutral**: 0.00 / 0.00 / 1.00 / 25.00 (01:16, 02:18, 12:06, 46:32, 56:02, 77:16)
- **Contrast / Pivot**: 1.000 / 0.435 (01:16, 02:18 — Pivot is the Resolve project default)
- **Saturation / Hue / Lum Mix neutral**: 50.00 / 50.00 / 100.00 (01:16, 02:18)
- **Color Boost / Shadows / Highlights / Mid-Detail neutral**: 0.00 (01:16, 02:18); Temp 0.0, Tint 0.00 (02:18)
- **Curves Edit Soft Clip default** Y/R/G/B = 100 (no soft clip) (02:34, 03:16, 04:04)

**Lift / black-clip demo (Grey Scale ramp + disc-golf):**
- **Lift master**: -0.18 (crush demo, flattens shadows at waveform floor) (07:50)
- **Lift master**: -0.40 then eased to -0.10 (ramp: black end moves, white stays anchored — "lift will never touch pure white") (56:50, 56:56)

**Gain demos:**
- **Gain master**: 0.97 (slight highlight pull-down, "remain flatlined" teaching) (10:02, 10:32)
- **Gain master**: 1.57 (prior demo state before reset) (11:06)
- **Gain master**: 1.34 (highlights begin to flatline at top) (39:56)
- **Gain master**: 1.52 (dialed back to keep highlights off ceiling — "much more room to work with") (41:32, 41:40)
- **Linear-gamma Gain**: 2.95, then pushed to 6.70 — exposure rises while blacks stay pinned at floor (53:14, 53:34); repeated 2.87 / 3.51 (54:06, 54:12)
- **Gain (color, per-channel)** Y/R/G/B = 1.00 / 0.77 / 1.00 / 1.24 (white-balance via Gain multiplier — red down, blue up) (63:42, 64:08)

**Offset demos:**
- **Offset master**: -62.75 (pulled to full black, waveform flat at 0) (17:44, 17:52)
- **Offset master**: 151.00 (pushed to full white, waveform flat at top) (17:58)
- **Offset master** sweep back through neutral: 53.00 → -2.75 → 25.00 (18:10, 18:14, 18:18)
- **Offset (complementary demo)**: R 84.32 / G 0.18 / B 93.54 → image magenta ("opposite of green is magenta") (12:32)
- **Offset (complementary demo)**: R 25.06 / G 25.43 / B -43.45 → image yellow/green ("opposite of blue is yellow") (12:34)
- **Offset additive ramp demo**: 56.45 then 50.00 (whole ramp translates up uniformly) (59:14, 59:48)
- **Offset exposure-lift demo**: 41.00 (whole image incl. blacks shifts up — the move he does NOT want) (53:06)
- **Offset (non-linear node)**: ~45.70/45.70/44.20 (lifts + flattens darks, becomes "flat and noisy") (53:46)
- **Offset (color WB)**: R 21.00 / G 24.82 / B 25.62 (small per-channel WB push) (64:22)
- **Gain reset state during exposure-vs-offset talk**: Gain 0.75 (before resetting to 1.00) (52:56)

**HSV-mapped node demo (node Color Space → HSV):**
- **Gain slot pushed to 2.22** (one HSV axis, others 1.00) → image goes strongly RED, channels stretch apart (78:28) [flag: "Gain 2.22" is a real ~2.2× on a 1.00-neutral slot, but the slot is an HSV axis not literal Blue — surprising=true, value plausible]

**CST configurations:**
- **Input CST**: Input Color Space Canon Cinema Gamut; Input Gamma Canon Log 2; Tone Mapping Method DaVinci; Adaptation 9.00; Gamut Mapping None; Use White Point Adaptation checked (31:50, 35:18, 50:12)
- **Output (delivery) CST**: Output Rec.709 / Gamma 2.4 ("2.2 for YouTube/web generally") (35:56, 36:38)
- **Working-space CST**: → DaVinci Wide Gamut / DaVinci Intermediate (37:16, 50:12); tail CST DWG/DI → Rec.709 (38:32, 79:32)
- **CST Output Gamma → Linear** to view footage linear ("linear is how cameras capture light") (48:04, 48:18)
- **CIE Chromaticity Rec.709 primary readouts** (reference, not a grade): R 0.6400,0.3300 / G 0.3000,0.6000 / B 0.1500,0.0600 / W 0.3127,0.3290 (D65) (22:50)

**HDR (zone) wheels:**
- Zones Dark / Shadow / Light / Highlight / Specular / Global; zone range markers e.g. Dark -1.50/+1.00, Light -1.00/+1.50, Highlight +1.50 (these are zone-edge positions in stops, NOT wheel coordinates) (67:30, 67:42)
- **HDR Global exposure +1 stop** == "global tab" adjustment (identical result) (68:42, 68:52) [flag: surprising=true; the captured on-screen Global readout sat at ~neutral so the +1 stop is stated, not frozen in a number]

### Distinctive techniques / opinions
- **Clipping defined precisely:** a flat line at the very top (100 = blown, no highlight detail) OR very bottom (0 = crushed) of the waveform = lost information (10:32, 17:22). Waveform = "monitoring your exposure" of the entire image (19:20).
- **Scope scale is 0–100** (0 = black, 100 = white); the scale style is changeable; a channel reading 100 is overexposed with no detail (05:30, 17:22).
- **Recommended scope set:** Waveform + Vectorscope most often, Parade sometimes (04:28). Parade = same data as Waveform split into R/G/B columns for channel-balance comparison (14:30).
- **CST only when needed:** if you recorded Rec.709 AND deliver Rec.709, you do NOT need a CST — just set Rec.709/Rec.709 in/out "and you'll be fine" (31:48, 45:10). Multi-camera shoots need per-source input identification (Rec.709, Sony S-Gamut3, etc.) (33:54).
- **Output gamma 2.4 vs 2.2:** 2.4 standard, 2.2 for YouTube/web viewing (35:56).
- **Lift vs Gain are inverses:** Lift pivots on white (never touches pure white), Gain pivots on black; Offset is purely additive (translates the whole ramp) (56:50, 59:14).
- **Math model of the wheels:** y = (Gain/Lift slope)·X^(power−Gamma) + Offset → Gain/Lift = multiplicative slope, Gamma = exponent (curve), Offset = additive constant B (59:50, 60:18).
- **Linear-gamma exposure trick:** set a node's gamma to Linear, then raise Gain — it behaves like an in-camera stop change; blacks stay anchored at the floor instead of lifting (53:14–54:12). In the default (non-linear) space the same lift makes darks "flat and noisy" (53:46).
- **Primary wheels vs Log wheels vs HDR wheels:** Primaries (Lift/Gamma/Gain/Offset) affect the whole image; Log wheels (Shadow/Midtone/Highlight/Offset) are range-limited to part of the tonal range (60:40); HDR zone wheels are **color-space aware** — they adapt to the working/timeline color space, unlike the legacy primaries (69:16).
- **Offset is slower to white-balance with** because it shifts two things (lift+gain together); prefer Gain for a WB move on highlights — result on skin "basically the same" but Gain preferred (64:08, 65:40).
- **Saturation is "basically a gain"** (a multiplicative gain on chroma) (71:06); read it on the Vectorscope (distance from center = saturation, angle = hue) (14:12, 71:24).
- **Vectorscope skin-tone line is a guideline, not a hard target** (69:38).
- **When a node is switched to HSV/HSL color space, the Lift/Gamma/Gain/Offset R/G/B controls remap to Hue/Saturation/Value** — adjusting only the "green" slot adjusts only Saturation (77:16, 77:44); pushing one HSV axis can throw the image to an unexpected hue (78:28).
- **A/B a node** with Ctrl+D (disable/enable current node) (64:26).
- **Build the second CST by copy/paste + swap**, not re-dragging the OFX (37:10, 45:34).
- Complementary/opposite pairs: R↔Cyan, G↔Magenta, B↔Yellow (additive RGB emit; subtractive CMY) (11:46).

### ENGINE: what a headless auto-grader should adopt
- **measure.py / scopes:** Treat the 0–100 IRE waveform as the exposure contract. Detect clipping as a *flat plateau* at the 0 or 100 rail per channel (not just any pixel touching the rail) — that's the colorist's own definition (10:32, 17:22). Implement per-channel RGB parade reads for white-balance balance checks (14:30) and a vectorscope angle/radius read for hue/saturation (14:12).
- **correct.py — color management first (CST sandwich):** Make the pipeline color-managed: tag input as camera native (Canon Cinema Gamut / Canon Log 2 etc.), convert to a wide working space (DaVinci Wide Gamut / DaVinci Intermediate), grade, then convert to Rec.709 / Gamma 2.4 (default) or 2.2 for web (35:56, 50:12, 79:32). Expose a "skip CST if input==output==Rec.709" fast path (31:48).
- **correct.py — exposure in linear:** Offer a "linear exposure" mode: convert to linear, apply a scalar gain (a stop multiply) so highlights move while blacks stay anchored at 0, then convert back — this is the clean exposure adjustment vs an offset that lifts and flattens shadows (53:14–54:12, 53:46). Implement exposure as gain-in-linear, not offset.
- **correct.py — control semantics:** Encode the wheel math literally: Gain = multiplicative slope (pivots on black), Lift = inverse slope (pivots on white, never touches 1.0), Offset = additive constant, Gamma = power exponent (59:50). Use these as the primitive ops.
- **correct.py — white balance:** Prefer per-channel Gain (highlight multiplier) for WB over Offset; Offset moves lift+gain together and is slower/less clean (63:42, 64:08, 65:40).
- **stylize.py — saturation:** Implement saturation as a multiplicative chroma gain (71:06); validate against vectorscope excursion toward primary/secondary targets, keep skin near (not nailed to) the skin-tone line as a soft guideline (69:38, 71:24).
- **tonemap.py:** CST tone mapping in the corpus uses Method = DaVinci, Adaptation 9.00, Gamut Mapping None, Use White Point Adaptation on (31:50, 50:12) — reasonable defaults for a Canon-log → Rec.709 tonemap. Optionally expose a Y-Gamut reshaping hook (mentioned at 80:18).
- **luts.py / output:** Default delivery transform Rec.709 + Gamma 2.4; provide a 2.2 variant for web/YouTube targets (35:56).
- **Headroom rule of thumb:** keep highlights just under the 100 rail (avoid the flatline) for more grading room — bake a "don't clip" guard into auto-exposure (41:32, 41:40).
