## beginners-guide-grading — Beginner's Guide to Colour Grading

**Tool:** DaVinci Resolve Studio 20 · **Source clips:** H.264 High L4.0 stock footage · **Scope scale:** 10-bit 0–1023, ref Low 0 / High 1023.

### Workflow taxonomy (00:24)
Primary Grading = **Normalization → Colour Balancing → Shot Matching**, then Secondary Grading. Normalization adjusts four axes: **Colour / Luminance / Detail / Contrast** (01:07).

### Node tree / order actually built
Every clip is a **single serial node chain**, labeled on screen:
- **Example 1 (warehouse):** `01 Normalize` → `02 Balance` (12:13, 13:01).
- **Example 2 (subway):** `01 Normalize` → `02 Balance` (15:16, 17:06).
- **Desert match:** `01 Normalize` → renamed `Shot Match` for the match op (23:08), plus a `Sizing` (Input) reframe stage.

Separation-of-concerns rule: **Normalize carries the contrast/exposure** (Contrast 1.048 / Pivot 0.563 / Mid-Detail 31.5); the **Balance node is reset to neutral** (Contrast 1.000 / Pivot 0.435 / Mid-Detail 0) so the cast fix is isolated and measurable (12:13, 12:25).

### Neutral/default identity state (00:58, 05:54, 23:12)
Temp 0.0 · Tint 0.0 · **Contrast 1.000 · Pivot 0.435** · Mid/Detail 0.0 · Lift 0.00 · Gamma 0.00 · **Gain 1.00 · Offset 25.00** · Color Boost 0.0 · Shadows 0.0 · Highlights 0.0 · **Saturation 50.00 · Hue 50.00 · Lum Mix 100.00** · Curves identity (Y/R/G/B = 100).

### The four wheels — demonstrated weighting (05:54–07:03)
- **Lift** = shadows (max effect at black). Down → crush toe to ~0–64 (06:32); +0.07 → milky lifted blacks (06:35).
- **Gain** = highlights (anchored at black). Down 0.95 → highlight tops to ~768–896 (06:48/06:50); up 1.66 → blown, clipped flat at 1023 (07:22/07:28).
- **Gamma** = midtones. +0.01 brightens mids, ends pinned (06:55).
- **Offset** = uniform shift of the entire trace; 25.00→26.40 raises whole pedestal (07:03).

### Scope targets hit
- Highlights → **"second line from top" ≈ 896/1023 (~87.5%)**, below clip (07:09).
- Black floor kept **~64–128 (off 0)** to preserve shadow detail (08:11); but **don't lift naturally-black scenes** (moon clip, 08:23) — scene-adaptive, not a fixed full-range stretch.
- Normalize result target: trace spans **~128 (black) → ~896 (white)** (16:15).

### Example 1 — warehouse grade (concrete moves)
- Lift **+0.01**, Gain **0.93** (preserve toe, tame highlights) (08:11).
- Gamma master **−0.01** to darken mids for depth (09:16).
- **Contrast 1.052** then settled **1.048**, value-field drag (double-click label = reset) (09:16/09:28).
- **Pivot 0.435 → 0.533 → 0.563** to darken globally while keeping contrast slope (09:31/09:35).
- **Mid/Detail 45.50** (later 31.50) for midtone texture/local-contrast sharpening (09:44, 10:00).
- **Saturation 50 → 52.40 → 52.80** gentle global lift (10:04/10:18).
- **Balance:** diagnosed red highlight cast (red trace highest, 10:37) → on Gain wheel pushed toward **cyan: R 1.00→0.97, B 1.00→1.01** (12:28/12:41); or via **Color Bars** lower red Gain bar to **0.97** (13:06). Complementary rule: neutralize by adding the opposite (red↔cyan) (11:16/11:25).

### Example 2 — subway grade (curves-driven)
- Dark green-cast clip; Y waveform floor pinned at 0 = crushed (15:50).
- **Normalize via Custom Curves:** raise black point ~⅔ to first line (→ ~128) (15:59/16:03); raise white point so top hovers ~second line from top (~896) (16:12/16:15); add midtone control point and lift to brighten (16:19).
- **Saturation 50 → 70.00** (=1.4× on the 0–100 scale where 50=1.0×) (16:39).
- **Mid/Detail 60.50** (16:49). **Contrast 1.036 / Pivot 0.533** (16:54).
- **Balance via per-channel curves** (separate node): isolate **G**, drag green highlight point DOWN until green trace overlaps red (17:57–18:21); then isolate **B**, drag white point left/up to **raise blue** until trace overlaps (yellow↔blue complement) (18:45–18:55). Target = R/G/B traces converge to a **white (neutral) trace**.

### Curves mechanics taught (13:47–14:50)
- Black point (bottom-left): drag **right = darken/crush lows**, **up = lift/milk blacks**.
- White point (top-right): drag **left = brighten/stretch highlights**, **down = dim/cap output white**.
- Add control points to isolate regions for local contrast (S-curve). Histogram sits behind the curve to guide anchor placement.

### Shot matching — desert (hero-shot method, 19:44–end)
- **Hero-shot approach:** pick the road-to-horizon clip as reference; match others to it (20:26).
- Workflow: **Grab Still** (viewer right-click) → still auto-named `1.1.1` → double-click to load as **reference wipe** (vertical split preferred; checkerboard available) (22:12–22:50).
- **Input Sizing** to frame matching content first: Pan **−1056.253**, Tilt **−71.000**, Zoom **1.120** (align horizons) (23:51).
- Read **Parade** (R|G|B side-by-side) to align each channel's target lobe to the reference lobe (20:44, 25:22).
- **Critical setting: set Lum Mix = 0 before per-channel work** so channel gain doesn't auto-compensate luma (25:03/25:32).
- **Zone-separation rule:** mids via **Gamma**, highlights via **Gain**, shadows via **Lift** — pick the control by where the region's trace sits.
- Demonstrated bar moves (Color Bars): **Red Gain → 0.85 then 0.74**; **Blue Gamma −0.46**; **Green Gamma −0.55**; **Blue Gain → 1.02** (sky); **Blue Lift −0.03** (ground shadows); **Green Gain → 0.97** (24:52–26:32).
- Use the **HSL qualifier** to map scope traces to regions (sky vs ground); lower the qualifier gain-luma bar to isolate the bright sky (24:02/24:05).

### Distinctive opinions / techniques
- **"Scopes cannot be deceived"** — trust the numeric channel delta over the eye (12:41).
- Per-channel **Custom Curves** (not just wheels) as the primary white-balance tool — drag one channel's curve until its trace overlaps the others.
- **Scene-adaptive black/white points** — don't force a full-range stretch on every shot.
- **No neutral reference?** Temporarily neutralize, keep only if it looks natural (19:33).
- Node hygiene: right-click → Node Label; named stages = readable grade tree. Cmd/Ctrl-D disables a node; Shift-D bypasses all for before/after (08:42, 13:11).

### ENGINE: what a headless auto-grader should adopt
- **Stage order:** Normalize (exposure/contrast) → Balance (per-channel cast removal) → Match → secondaries — as separate ops; keep cast-correction on its own neutral stage.
- **Identity reset constants:** Gain 1.0, Offset 25, Sat 50, Contrast 1.0, Pivot 0.435, Lum Mix 100, curves Y/R/G/B=100. Express targets on **0–1023**.
- **Normalize targets:** black point ≈128, diffuse white ≈896 (~87.5%); never clip at 1023; keep shadow toe >0 unless the scene is intentionally dark (scene-adaptive).
- **Cast detection = compare per-channel means by tonal zone** on the parade; correct the imbalanced channel where its trace lives (highlights→Gain, mids→Gamma, shadows→Lift). Push toward the complement (hue+180°).
- **Convergence metric:** minimize max R/G/B trace separation → neutral grey axis.
- **Lum Mix = 0** when doing per-channel gain/gamma so luma isn't auto-compensated.
- **Clip guards:** cap gain so diffuse white < 1023; detect clipping as % of samples at 1023; cap black lift to avoid unintended wash.
- **Mid/Detail** ≈ unsharp-mask / local-contrast on the midtone band (demonstrated +30 to +60).
- **Contrast S-curve** ≈ +0.04–0.05 over 1.0 around a pivot ~0.53–0.56 (slightly above mid-grey to protect shadows); raising pivot = global darken at constant slope.
- **Saturation:** gentle (+3 on 0–100) for clean footage, up to 70 (1.4×) for flat/log-ish; hold at 50 baseline.
- **Shot match:** choose a hero/reference frame, align each non-hero clip's per-channel parade lobes (highlight + shadow populations) to the hero's; reframe comparable regions (input-sizing) and exclude regions with no counterpart before computing match stats.