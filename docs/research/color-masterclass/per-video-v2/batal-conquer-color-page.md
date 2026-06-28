## batal-conquer-color-page — Daniel Batal - CONQUER the COLOR Page

**Tool:** DaVinci Resolve Studio 18.6 (Color Page), project "New Footage 3". Source clip C0296.MP4 (source TC 18:31:02;11) — a warm/red-cast wood-paneled interior of a drummer in a "Yaritis" shirt. Talking-head intro filmed in a separate guitar-decorated room. The clip is split into two events (01 and 02) so a graded clip (02) can be compared against an ungraded reference (01).

### Workflow order
This is a beginner orientation lesson, not a multi-node pipeline. The grading happens on a **single serial corrector node ("01")** throughout — no multi-node tree is demonstrated. The teaching order is:
1. **Orient on the page** — Primaries palette, Curves, Scopes (Parade), node graph, Effects Library (00:21–02:16).
2. **Concept: correct vs grade** — correction = neutral/accurate baseline; grading = creative mood/atmosphere from how the scene was lit (04:16–05:06).
3. **Read the scope** — Parade as the primary scope, 0–1023 (10-bit) axis, RGB channel reading (06:08–08:00).
4. **Learn the three Primaries modes** (same params, different UI): Color Wheels → Color Bars → Log Wheels (03:12–04:00, 13:42–17:44).
5. **Tour each wheel in isolation** (Lift → Gamma → Gain → Offset), each pushed then reset (09:56–13:22).
6. **Apply a basic correction** to the dark/red clip: Gamma lift + warmth split, Gain lift, Offset neutral (18:30–22:20).
7. **Before/after check** via a second graded clip or the Bypass toggle (22:21–23:13).

### Demonstrated parameters (number @ mm:ss)

**Neutral / baseline reference values (the scale-guard contract):**
- **Log Wheels neutral**: Shadow 0.00/0.00/0.00, Midtone 0.00/0.00/0.00, Highlights 0.00/0.00/0.00, Offset 25.00/25.00/25.00 (00:21, 00:57, 02:10, 03:53, 06:02)
- **Color Wheels neutral**: Lift 0.00/0.00/0.00/0.00, Gamma 0.00/0.00/0.00/0.00, Gain 1.00/1.00/1.00/1.00, Offset 25.00/25.00/25.00 (03:28, 03:58, 08:34, 09:25, 13:42)
- **Color Bars neutral** (same params as wheels): Lift 0.00 ×4, Gamma 0.00 ×4, Gain 1.00 ×4, Offset 25.00 ×3 (03:42, 13:50, 17:30)
- **Offset neutral = 25.00** (master "volume" wheel; explicitly NOT a black/shadow lift) — repeated as the key scale-confusion guard (01:47, 09:33, 12:45, 13:55)
- **Master row defaults**: Temp 0.0, Tint 0.00, Contrast 1.000, Pivot 0.435 (00:21, 00:40, 02:10, 03:53)
- **Log-only Range controls**: ↓Range (Low/Shadow) 0.333, ↑Range (High/Highlight) 0.550 (00:21, 03:50, 03:53, 15:05, 17:44)
- **Secondary/bottom row defaults**: Mid Detail 0.00, Color Boost 0.00, Shadows 0.00, Highlights 0.00, Saturation 50.00 (neutral), Hue 50.00 (neutral), Lum Mix 100.00 (neutral) (00:21, 02:10, 03:42, 23:20)
- **Curves - Custom neutral**: identity 45° diagonal; Edit channel intensities Y/R/G/B all 100 (00:19, 01:02, 02:29, 06:08, 08:00)

**Lift (Color Wheels) — black/shadow lift, whole-range move:**
- Lift +0.11/0.11/0.11/0.11 — lifted milky blacks; scope floor pushed up to ~256 (10:25, 10:37)
- Lift +0.01 — pulled almost back to neutral for A/B (10:42)
- Lift +0.19 — hard push; floor up to ~384–400, mids squished upward (10:47)
- Lift +0.03/0.03/0.03/0.03 — small black lift, base off the floor to ~128–256 (15:54)
- Lift +0.11 (second demo) — base lifted markedly to ~256 (15:55)
- Lift +0.08/0.08/0.08/0.08 — whole trace shifted up, peaks toward ~640–896 (17:00)
- Lift extreme — entire trace pinned to top of scale (~128→~896-1023 solid block); numeric readout appears reset at-neutral mid-demo while the scope shows the lifted result (transitional frame) (17:05) [flag: Lift wheel numeric readout reads 0.00 while scope shows full lift — transitional/ambiguous frame, value not trustworthy]

**Gamma (Color Wheels) — midtone lift (drags lows/highs a little, "stretch the middle"):**
- Gamma +0.12/0.12/0.12/0.12 — positive midtone lift (11:32)
- Gamma +0.03/0.03/0.03/0.03 — slight "fill-light" midtone lift (11:45)
- Gamma +0.09/0.09/0.09/0.09 — mid lift (dissolve frame) (11:48)
- Gamma +0.19/0.19/0.19/0.19 — strong midtone lift before reset (11:51)
- Gamma +0.10/0.10/0.10/0.10 — "natural fill-light" midtone lift; mids stretched up, lows/highs nudged (21:04, was 0.00 at 20:36 before the move)

**Gain (Color Wheels) — highlights/brightest tones:**
- Gain 1.42/1.42/1.42/1.42 — hard highlight push; tops reach/exceed 1023 (clipping above scope) (12:07)
- Gain 1.12/1.12/1.12/1.12 — uniform +0.12 overall brightness lift (12:42)
- Gain 1.08/1.08/1.08/1.08 — slight uniform lift (12:45)
- Gain 1.13/1.13/1.13/1.13 — modest uniform highlight lift toward (not past) 1023 (19:53)

**Offset (Color Wheels) — "master volume", uniform whole-image shift (neutral = 25.00):**
- Offset 42.15/42.15/42.15 — dragged UP (~+17), whole parade shifts up, shadows lift off 0 to ~128+ (12:58)
- Offset 25.25/25.25/25.25 — reset to near-neutral (13:01)
- Offset 37.75/37.75/37.75 — up (~+12.75), everything brighter (13:14)
- Offset 58.30/58.30/58.30 — strong up (~+33), shadow floor ~256 (13:15)
- Offset 26.95/26.95/26.95 — back down toward neutral, "everything darker evenly" (13:22)

**Log Wheels — Shadow wheel (narrow lower-band action, contrasted against Lift):**
- Shadow 0.40/0.40/0.40 — darks lifted off 0, green band ~128→384 (16:18)
- Shadow 0.50/0.50/0.50 — exaggerated; floor lifted, annotation pin near ~384 (16:30)
- Shadow 0.44/0.44/0.44 — narrow-band: below ~384 squashed, 384–512 largely unmoved (16:46)
- Shadow 0.10/0.10/0.10 — reduced back toward neutral (16:55)
- Shadow 0.10/0.10/0.10 — shown in three-mode tour (17:44)

**Color Bars — Lift split (warm-shadow correction):**
- Lift Y/R/G/B = 0.00 / 0.05 / -0.01 / -0.04 — red up, green/blue down a touch to push shadows warm/away-from-blue; Gamma/Gain/Offset neutral (15:00, 15:01)

**Final demonstrated grade on clip 02 (the "basic correction"):**
- Gamma Y/R/G/B = 0.10 / 0.05 / 0.10 / 0.10 (R slightly lower = touch of warmth in mids) (22:20, 22:50, 23:20)
- Gain Y/R/G/B = 1.13 / 1.13 / 1.13 / 1.13 (uniform brightness raise) (22:20, 22:50, 23:20)
- Lift Y/R/G/B = 0.00 / -0.00 / -0.00 / -0.00 (neutral) (22:50, 23:20)
- Offset 25.00/25.00/25.00 (left neutral), Contrast 1.000, Pivot 0.435, Saturation 50.00, Hue 50.00, Lum Mix 100.00 (22:20, 22:50)
- Curves - Custom shows a slight S/contrast shape pulled in the final overview (22:50)

**Scope readings of the source (dark, warm/red-cast log-ish clip):**
- RGB Parade 0–1023 (ticks 0/128/256/384/512/640/768/896/1023); bulk below ~512, nothing pinned at 1023; red strongest, green mid, blue lowest (01:02, 06:08, 06:28, 18:30)
- Channel peaks read out: Red ~880–900, Green ~768–820, Blue ~768 (07:02, 14:51, 14:52)
- BYPASSED (original): red dominant/tall, green markedly lower, blue lowest — heavily red-weighted (23:11)
- GRADED: blue raised/expanded, green/blue sit closer to red — more balanced distribution (23:13)

### Distinctive techniques / opinions
- **Correcting ≠ grading**: correction brings footage to a neutral/accurate baseline (fixing what the camera baked in); grading creates atmosphere/mood by intentionally pushing color to support how the scene was lit (04:16, 04:49).
- **Shoot flat/RAW** to preserve latitude — "ask the camera to add nothing" so the color page has the most data/flexibility (04:29, 04:33).
- **Parade is his most-used scope**; read it dark→light vertically (0 = pitch black at bottom, 1023 = brightest the eye picks up at top) and R→G→B horizontally as three independent channels (06:08, 06:39, 07:02, 07:29).
- **The three Primaries modes are the same controls** in different UIs — "the names are the same: lift, gamma, gain, offset, and those all do the same things"; Color Bars is "just another iteration" of the wheels for finer per-channel tuning; "really only two choices: color wheels or log wheels" (13:50, 17:27, 17:30).
- **Wheel mental model**: Lift = base/lows/shadows, Gamma = mids, Gain = highs/treble, Offset = "master volume" moving everything up/down together — explicitly framed as a luma/audio analogy (09:28–09:33, 12:45, 21:44).
- **Lift vs Log-Shadow is the key contrast**: Lift (Color Wheels) moves the WHOLE image up (anchored, drags everything toward the top); the Log-Wheels Shadow acts only on a NARROW lower band (below ~384), leaving the 384–512 range largely unmoved — choose the wheel by what part of the footage needs correcting (16:46, 17:00, 17:05, 17:07).
- **Use the wheel, not just the slider** for Gamma: dragging the wheel gives "a nice even curve" that brings up lows a little and highs a little rather than "a harsh middle change on a narrow band" (20:36).
- **A Gamma lift reads as a fill light** — raising mids "feels natural, as if a light brought out the mid-range," and it stretches values across the middle (Low/Middle/High) (11:45, 21:04).
- **Don't have to clip past 1023** when raising Gain — push highlights toward the top of what's visible, but how far depends on the look (19:53).
- **Before/after without two clips**: use the "Bypass Color Grades and Fusion Effects" toggle (sparkle icon top-right of viewer; default shortcut Shift+D) (22:42); or split the clip into two events and grade only one for an in-timeline A/B (01:44, 22:21).
- **Effects/Resolve FX are explicitly NOT used** in this basic lesson (00:50).

### ENGINE: what a headless auto-grader should adopt
- **Hard-code Resolve neutral constants** so an auto-grader never misreads a baseline: Lift/Gamma/Shadow/Midtone/Highlights neutral = **0.00**; Gain neutral = **1.00**; Offset neutral = **25.00** (NOT a lift); Contrast = 1.000; Pivot = 0.435; Saturation/Hue = 50.00; Lum Mix = 100.00; Log ↓Range = 0.333, ↑Range = 0.550. Treat any Offset reading near 25 as zero-shift (correct.py / measure.py scale-guard).
- **Adopt the 10-bit 0–1023 code-value axis** for scopes (NOT IRE/%) when emulating this corpus; map gridlines at 128/256/.../1023 (scopes/measure.py).
- **Order of operations = broad-to-fine, single node**: a basic correction can be a one-node primaries move — Offset for global level, Lift for black floor, Gamma for mids, Gain for highlight ceiling, in that mental order (correct.py).
- **Default "basic correction" recipe** for a dark, red-cast interior, validated on screen: small **Gamma +0.10** master with a slight **red-gamma pullback (R 0.05 vs 0.10)** for warmth control, a uniform **Gain ~1.13** to lift highlights toward (not past) 1023, Offset left neutral, Lift neutral (correct.py / stylize.py — usable as a parameterized "warm interior lift" preset).
- **Warm-shadow split via Lift bars**: R +0.05, G −0.01, B −0.04 pushes shadows warm/away-from-blue without touching mids/highs — a cheap channel-balance primitive (correct.py).
- **Model Lift vs Log-Shadow distinctly**: Lift = whole-range multiplicative lift anchored at the top; Log-Shadow = narrow-band lift confined below the ↓Range split (~384). An engine should expose both, not collapse them (correct.py).
- **Channel-balance objective for auto-correct**: target is pulling the blue channel up so R/G/B sit closer together (the demonstrated before→after moved from heavily red-weighted toward balanced) — a concrete loss function for measure.py/match.py (read off Parade per-channel means/peaks).
- **Don't auto-clip**: cap Gain so highlights approach but do not pin 1023 unless the look explicitly calls for it (correct.py guardrail).
- **Provide a one-flag Bypass/before-after render** mirroring Resolve's Shift+D toggle so a headless grade is always A/B-verifiable (engine UX).
- **Saturation/Hue/Contrast/Pivot stay at neutral** for a pure correction pass — creative saturation/contrast belong in a separate grade stage (stylize.py), matching the correct-then-grade split.
