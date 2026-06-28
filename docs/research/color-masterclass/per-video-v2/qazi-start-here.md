## qazi-start-here — Waqas Qazi - New to DaVinci? Start Color Grading Here

**Tool:** DaVinci Resolve Studio 21 (macOS, Apple M2 Ultra / 96 GB, 10-bit viewer). Projects "New to DaVinci Resolve" (grade timeline) + cutaway demo "100New to DaVinci Resolve". Footage: three Artlist ProRes 422 HQ LOG clips, 25 fps, 4096×1742, 10-bit (corridor/subway/storefront); plus ARRI/Alexa ARRI LogC3 demo clip and teal ballet/statue b-roll. Beginner-oriented "start here" tutorial: machine prep → project/color-management setup → page tour → CST sandwich → one-click film look.

### Workflow order
The colorist's color-managed pipeline (CST "sandwich") demonstrated on the 4-node tree (01-02-03-04):
1. **IDT / input node** (node 01, labeled "ist"/"idt") — Color Space Transform OFX converting camera-native into the working space: ARRI Wide Gamut 3 / ARRI LogC3 → DaVinci Wide Gamut / DaVinci Intermediate (21:19-21:43, 22:06).
2. **Grade nodes** (nodes 02, 03) — creative correction sits between IDT and ODT (22:02).
3. **ODT / output node** (node 04, labeled "odt") — CST converting working space → delivery: DaVinci Wide Gamut / DaVinci Intermediate → Rec.709 / Gamma 2.4 (22:34-22:39, 22:16).
- Pre-grade review pass: throw the whole timeline into **Lightbox**, hit play on the reference monitor, read the program holistically (count scenes/locations, find outliers) before touching a grade (16:10-16:21), then **group clips by location** (16:44-16:48).
- His personal node-tree template (separate cutaway): idt(01) → nr(02) → exp-bal(03) → adj(04) → skin(05) → mask(06) → … face(11) → vig(14) → depth-map(15) → look-dev(18) → sharpen(19) → odt(20), with a Layer Mixer combining parallel branches — "grade something that takes two days in two hours" (12:22).
- Broad-to-fine teaching order of the panels: Log Wheels (broad/main corrections) → Custom Curves ("the look DNA") → HSL curves (granular) → ColorSlice (secondaries/flair) (17:02-17:35).

### Demonstrated parameters (number @ mm:ss)

**Neutral/default reference values (Resolve baselines, repeatedly confirmed):**
- **Offset wheel neutral**: 25.00 / 25.00 / 25.00 — this is Resolve's OFFSET NEUTRAL, NOT a black lift (00:03, 00:13, 08:12, 17:02, 23:48, etc.)
- **Lift / Gamma / Shadow / Midtone / Highlights wheels neutral**: 0.00 / 0.00 / 0.00 (00:03, 18:55)
- **Gain wheel neutral**: 1.00 / 1.00 / 1.00 (00:03, 18:55)
- **Saturation neutral**: 50.00; **Hue neutral**: 50.00; **Lum Mix default**: 100.00 (00:03)
- **Contrast**: 1.000; **Pivot**: 0.435; **Mid/Detail**: 0.00 (00:03, 12:53)
- **Custom curve identity**: Edit Y/R/G/B all = 100 (08:10, 17:23, 17:34)
- **Log Wheels range splits**: Low Range 0.333, High Range 0.550 (default zone split points) (00:13)
- **HSL defaults**: Hue Vs Hue → Input Hue 256.00 / Hue Rotate 0.00 (17:28); Sat Vs Sat → Input Sat 0.00 / Output Sat 1.00 (17:30)

**Machine / preferences setup:**
- **System memory** 128.0 GB; **Limit Resolve memory usage to** 96.0 GB; **Limit Fusion memory cache to** 72.0 GB (GB allocation, "give Resolve all the juice") (01:22, 01:37, 01:42, 02:01)
- **GPU processing mode** Auto (Metal); **Neural Engine Processing** Auto; **GPU selection** Auto; device Apple M2 Ultra 96 GB (01:22, 02:01)
- **Use 10-bit precision in viewers if available** = CHECKED (02:19)
- **Use Mac display color profiles for viewers** = UNCHECKED (only turn on if exports differ wildly from canvas) (02:42)
- **Media Storage**: first location /Users/waqasqazi/Movies, **Direct I/O** = checked (02:07)
- **User > Color**: "Always perform copy and paste on selected nodes" = CHECKED; "Previous or next node navigates only to correctors" = checked; "Master reset maintains RGB balance" / "Use legacy auto color" / "Use legacy shot match" = unchecked; Color picker = DaVinci Resolve (03:07, 03:19)

**Project settings:**
- **Timeline resolution** 3840×2160 UHD; **Timeline frame rate** 23.976 fps (project); 25 fps for the grade timeline matched to source (03:50, 07:42)
- **Video Monitoring**: Use 4:4:4 SDI checked, Single link, Data levels Full, **Video bit depth** 8 bit default (03:57) — shown adjustable to **12 bit** as an example (04:11)
- **Image Scaling**: Resize filter = Sharper; mismatched resolution = Scale entire image to fit (default, left as-is) (04:21)
- **Color Management → Color Space & Transforms**: Color science = **DaVinci YRGB** (manual/node-based CM, NOT "Color Managed"); "Use separate color space and gamma" unchecked; **Timeline color space = DaVinci WG/Intermediate**; **Output color space = Rec.709 Gamma 2.4** (04:24, 04:42, 04:47, 04:57, 05:51)
- **Dolby Vision / HDR10+ / HDR Vivid** all = unchecked (Dolby Vision version 4.0, Mastering display 4000-nit P3 D65 ST.2084 — shown but off) (04:24, 04:57)
- **3D lookup table interpolation = Tetrahedral** (KEY: change from the default Trilinear for smooth gradients / no banding) (05:04, 05:32, 05:35)
- **Broadcast Safe IRE levels = -20 - 120**; "Make broadcast safe" = CHECKED (05:04, 05:35)
- All LUT slots = "No LUT selected" / "Use video monitoring selection" (05:27)
- **General Options > Color**: "Use S-curve for contrast" = CHECKED; "Use legacy Log grading ranges and curve" = unchecked; "Luminance mixer defaults to zero" = unchecked; gallery stills auto-labeled by Clip name, still number appended As Suffix; Node Stack Layers = 1 (05:53, 06:21, 06:24)

**Source spec:**
- Clips: Apple ProRes 422 HQ, 25.000 fps, 4096×1742 (timeline) / 4096×1478 (one read), Bit Depth 10, Progressive, LOG (07:29, 07:35, 09:38)

**CST node configuration (the core grade move of the video):**
- **IDT node**: Input Color Space = **ARRI Wide Gamut 3**, Input Gamma = **ARRI LogC3**; Output = **DaVinci Wide Gamut / DaVinci Intermediate** (21:19, 21:41, 21:42, 21:43)
- **CST Tone Mapping**: Method = DaVinci, **Adaptation = 9.00**; Gamut Mapping Method = None; Use Custom Max Input/Output unchecked; Use White Point Adaptation checked (21:41, 22:39)
- **Fresh/unconfigured CST default**: all four fields = "Use timeline" (21:46)
- **ODT node**: Input = DaVinci Wide Gamut / DaVinci Intermediate; Output = **Rec.709 / Gamma 2.4**; Apply Forward OOTF + Use White Point Adaptation checked (22:34, 22:39)

**Keyframed B&W→color reveal demo (single corrector, Color keyframes):**
- **Saturation 0.00** at first/start keyframe (fully desaturated, B&W) → **Saturation 50.00** at later keyframe (full color); keyframe at 00:00:04:21, ramps 0→50 (18:02-18:14)

**RapidGrade OFX one-click look (alternative consolidation tool):**
- **RapidGrade 1.6.12**: Color Space Primaries = DaVinci Wide Gamut; Transfer Function = DaVinci Intermediate; Master Blend = 1.000; Enable Charts + Enable Film Look ON (13:11, 13:19, 13:57)
- One Click Look: **Pack = Film, Look = Creamy Cinema** (13:57); film print preset **Kodak 2383** (14:14)
- RapidGrade internal Film Contrast (plugin-internal scale, NOT Resolve wheels): Blacks 0.92, Undertones 0.240, Midtones 0.255, Highlights -0.750, Whites -2.72; Color Contrast Blacks R -0.10 / G 0.00 / B 0.02, Undertones R 0.163 / G 0.256 / B 0.000, Midtones R 0.100 (14:14)
- Primaries left untouched while the plugin drives the grade (confirms look is plugin-driven) (13:57)

**HDR Color Wheels cutaway demo (separate "100New to DaVinci Resolve" project):**
- HDR Color Wheels zone readouts: Dark -1.50, Shadow +1.00, Light -1.00 (HDR zone-edge/tonal-range readouts, NOT lift amounts); per-wheel Exp 0.00 / Sat 1.00; Dark Y 0.20 (10:12) [flag: HDR zone-edge values vs. lift-amount scale ambiguity — surprising=true, medium confidence]
- Global Y pulled to -1.41 with a 2nd node added (10:16) [flag: HDR Global-wheel Y scale ambiguity — surprising=true, medium confidence]
- Midtone (gamma) RGB balance push demo: R 0.09 / G -0.05 / B 0.22 (warm-into-blue midtone), ~ -1..1 wheel-balance scale (10:29)

**Scope scale (consistent throughout):** Waveform on 0–1023 (10-bit) vertical scale, gridlines 0/128/256/384/512/640/768/896/1023 (00:03, 19:07, 23:48); Vectorscope with R/Mg/B/Cy/G/Yl target boxes (19:39).

### Distinctive techniques / opinions
- **"Find the real problem before touching the sexy controls"** — rule #1 of his beginner starter map; diagnose first (00:16, 01:23).
- **Color-management-first** is "a big one" — set Color Space & Transforms (Color/Timeline/Output) correctly and it "instantly makes your grades look 85% BETTER" (presenter's rhetorical figure, not measured) (04:24, 20:16). [flag: "85% better" is a marketing/rhetorical number, not a control value — surprising=true]
- **DaVinci Wide Gamut / DaVinci Intermediate as the working space** = "most juice possible," future-proof, retains full sensor latitude (16-17 stops vs ~10 in other editors / ~10 on today's TVs) (04:47, 13:21, 23:07-23:24).
- **CST sandwich on nodes, not just project RCM** — explicit idt → grade → odt structure so input/output transforms bookend the creative work (21:43, 22:02-22:16).
- **Tetrahedral over Trilinear** for 3D LUT interpolation — trilinear creates harsh banding, tetrahedral renders smooth gradients (05:04-05:32).
- **Set 10-bit viewers + don't trust the screen** — uncalibrated monitors/laptops/tablets all differ; trust scopes over the display; a $30k Sony BVM-HX310 is "truth," scopes are the affordable substitute (02:19, 18:35-18:47).
- **Lightbox-first onboarding** — "first thing I do anytime I get a new gig": Lightbox + play on reference monitor to read the whole program before grading; then group by location (16:10-16:48).
- **Vectorscope used for**: nailing color balance, shot matching, protecting skin tones, monitoring saturation limits (19:39).
- **Nodes > layers** — flexible left-to-right web vs strict vertical stack; node trees branch far deeper (parallel + Layer Mixer) than a layer stack (11:47, 12:22).
- **Broad-to-fine panel order**: Log Wheels (main/broad) → Custom Curves ("look DNA") → HSL curves (granular) → ColorSlice (secondaries) (17:02-17:35).
- **Export the grade as a LUT and ingest into the camera** (Sony a7 III shown) so on-set monitoring matches the final look (14:23).
- **Discipline on still naming** (As-Suffix + append still number) or Resolve overwrites/overlaps exported log vs Rec.709 ("X709") vs final stills (06:10).
- Power-user node template makes a 2-day grade take 2 hours; consolidating ~20 named nodes into one (RapidGrade) is the alternative for speed (12:22, 13:07-13:11).

### ENGINE: what a headless auto-grader should adopt
- **luts.py / pipeline order — enforce the CST sandwich.** Make the canonical chain `IDT (camera→DWG/DI) → corrections → ODT (DWG/DI→Rec.709 Gamma 2.4)`. Default working space DaVinci Wide Gamut / DaVinci Intermediate; default delivery Rec.709 Gamma 2.4. Tone-map params to mirror: method DaVinci, adaptation 9.0, gamut-mapping none, white-point adaptation on (21:41, 22:39).
- **correct.py — bake the Resolve neutral baselines** so detection logic never misreads them: Offset neutral = 25.0 (NOT a lift), Lift/Gamma/Shadow/Midtone/Highlight neutral = 0.0, Gain neutral = 1.0, Saturation/Hue neutral = 50.0, Lum Mix = 100.0, Contrast 1.0 / Pivot 0.435, curve identity = 100. Use these as the "no-op" reference when diffing a target grade against neutral (multiple cites; 00:03).
- **luts.py — tetrahedral interpolation only** for any 3D LUT apply (avoid trilinear banding) (05:04-05:22).
- **measure.py / scopes — adopt the 0–1023 10-bit waveform scale** with gridlines at 0/128/256/384/512/640/768/896/1023, and a vectorscope with R/Mg/B/Cy/G/Yl target boxes for skin-line + saturation-limit checks. Implement the vectorscope's four jobs as auto-checks: color balance, shot match, skin-tone protection, saturation-limit monitoring (19:07, 19:39, 23:48).
- **match.py — Lightbox-style program pass.** Before grading, batch-read the whole set: cluster shots into scene/location groups, flag outliers, and grade group-wise (shot-match within a group) rather than per-clip in isolation (16:10-16:48).
- **stylize.py — model the one-click film look** as a working-space (DWG/DI) film-print emulation: Kodak-2383-style print curve + per-zone film contrast (blacks slightly up, highlights/whites pulled down for shoulder roll-off) + per-zone color contrast, applied AFTER the IDT and BEFORE the ODT, with a single master-blend opacity (13:57, 14:14).
- **Always interpret input gamma/gamut explicitly** (e.g. ARRI Wide Gamut 3 / ARRI LogC3) rather than "use timeline" — declaring the source transform is Qazi's literal "Step 1: tell Resolve what the footage is" (20:58, 21:19).
- **Default contrast via S-curve** (project setting "Use S-curve for contrast" ON) and keep broadcast-safe clamping available (-20–120 IRE) as an optional output guard (05:53, 05:04).
- **tonemap.py — keep the DWG/DI latitude argument central**: preserve full capture range through the grade, only compress to display at the ODT, so HDR/SDR masters derive from one graded source (13:21, 23:07-23:24).
- **NOTE for human recheck**: the HDR Color Wheels zone readouts (Dark -1.50 / Shadow +1.00 / Light -1.00, Global Y -1.41) come from the cutaway demo and use the HDR-palette zone-edge scale, not the Lift/Gamma/Gain scale — do not feed these as primary-wheel offsets without verifying the scale (10:12, 10:16).
