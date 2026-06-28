## mostyn-perfect-node-tree — Darren Mostyn - My Perfect Node Tree

**Authority's core method:** one pre-built, saved "FIXED NODE TREE" PowerGrade (~15–20 named nodes) reused on every clip; unused stages stay dormant (pass-through, harmless) and are toggled on per shot rather than rebuilt. Project is **DaVinci YRGB (manual, NOT color-managed)** — all transforms live in node-level CSTs. Resolve Studio 19 (Public Beta), project "RESOLVECON 2024".

### Canonical node-tree order (labels as seen on screen)
Serial backbone → parallel mixer → window bank → look → output:

`CST in (>DWG / CWG / IWG)` → `exp/bal` → `con (contrast)` → `sat` → **parallel block** {`highlights` 06, `shadows` 08, `density`/`colour` 09, `warper` 10, `curves` 11} → `trim`/`srm`/`mix` (12) → **parallel power-window bank** {`PW left` 13, `PW right` 15, `PW top` 16, `PW bottom` 17} → finishing nodes 18/19/20 → `FLC` (Film Look Creator) → `>709` output CST (07:34, 20:04, 25:28, 33:37, 46:41, 46:45, 51:40).

One job per node (exposure, contrast, sat each on dedicated nodes); tonal work (highlights/shadows/density/curves) split into a **parallel mixer**, not stacked serially (07:35).

### Project / color-management settings (09:08, 12:24, 50:42, 51:34)
- Color science **DaVinci YRGB** (not YRGB Color Managed — hence in-node CSTs)
- Timeline (working) color space **DaVinci WG/Intermediate**
- Output color space **Rec.709 Gamma 2.4**
- Dolby Vision 4.0, Legacy CM analysis, Mastering display 4000-nit P3 D65 ST.2084
- Broadcast Safe IRE **−20 … 120**, all LUTs "No LUT selected", 3D-LUT interp Tetrahedral
- Proves the project Output-space flag is **inert** in a manual YRGB project — switching to P3 DCI + Save changes nothing on screen; the in-node `>709` CST does the actual conversion (50:47, 50:56)

### Input CSTs (per-camera, placed first)
- **Canon Cinema Gamut / Canon Log 3 → DaVinci Wide Gamut / DaVinci Intermediate**; Tone Mapping DaVinci, Gamut Mapping None, White Point Adaptation ON, OOTF off. Adaptation seen at **0.00** (18:07), **9.00** (47:00, 48:43) (11:11, 33:37)
- Rec.709 source still wrapped to working space and back (`>DWG … DWG>709` tail) so one look graph fits any source (32:23, 33:14)
- **Rec.709 → DWG/DI** input CST, Tone Mapping DaVinci, Adaptation **5.00** (41:14)
- Output/look CST: **DWG/DI → Rec.709 / Gamma 2.4**, Tone Mapping DaVinci **Adaptation 5.00**, White Point Adaptation ON (12:29)
- Workflow for unknown source: inspect waveform flatness (lifted blacks, compressed ~256–512 = log) to infer log vs 709 before assigning the CST (32:20, 33:16)

### Primaries / demonstrated parameter baseline (08:49, 11:48, 41:14, 46:41)
- Lift/Gamma/Gain RGB **0.00**; Gain **1.00**; **Offset 25.00/25.00/25.00** (master print-light style lift)
- **Contrast 1.000, Pivot 0.435** (his S-curve pivot in log/intermediate — not 0.5); HDR-wheel variant pivot region 0.225 (51:04)
- **Saturation 50.00** neutral (raised to **57.60** when grading, 25:28); Hue 50.00, **Lum Mix 100.0**
- Temp/Tint 0.0; ColorSlice all 6/7 zones Center 0.000 at default
- Prefers **HDR (log) Color Wheels** (Dark/Shadow/Light/Global) over Lift/Gamma/Gain for tonal-zone nodes (50:00, 51:04)

### Exposure / balance / saturation moves
- **exp/bal** node = exposure+balance after input CST; driven via **Offset wheel** (RGB read ≈ 4.20 / 32.62 / 26.41), targeting skin trace toward the upper-left orange/skin line on the **vectorscope** (13:58)
- **Color Warper (Hue-vs-Sat hex grid)** on the `sat`/`warper` node: single control point pulled outward along the orange/skin lobe to push skin warmth/sat (16:35, 30:03)
- **ColorSlice** "density" worked on the **Skin** vector specifically to add tone/sat depth on the skin band only (15:32, 29:37)

### Secondaries — Power Windows (pre-built, relocated not redrawn)
- Stored **Circle** window relocated to subject: Size 50.00, Aspect 2.47, Pan 50.00, Tilt 56.00, Rotate 0, Opacity 100, **Soft 1 6.36** (20:21, 20:24)
- Active circle qualifier (face vignette): Size 59.96, Aspect 15.14, Pan 56.75, Tilt 49.06, **Soft 1 6.67** (46:41)
- **Linear/Gradient** sky window: Softness Inside **7.62** / Outside **7.14**; relocatable (31:23)
- Four-direction parallel bank (left/right/top/bottom) for directional vignette/relight; ITV face window Soft 1 **6.70**, Pan 53.56 / Tilt 45.00 (35:28)

### Noise reduction (his explicit rule)
NR on its own dedicated early node — **before/early, never after the grade** (flattens the image); deleted when not needed to save compute (46:36, 47:43, 48:43, 49:33). Params: **Temporal** Frames 2, Better, Small range, Luma/Chroma threshold 7.0, Motion 50.0; **Spatial** Enhanced, Medium radius, Luma/Chroma 14.9.

### Look stages (Resolve FX + gallery presets)
- **Film Look Creator** = terminal look node, partially blended so the grade underneath stays visible: **Film-Look Blend 0.321, Core Look "Rochester", Skin Bias 0.000**, Exposure 0.05, WB 6500K, Tint +10, Subtractive Sat 1.0, Output White Point DCI (52:36, 52:38)
- **Glow** (Resolve FX Light): on imagery use **Show Threshold 0.750, Spread 0.500, Gain 0.500, Composite = Screen** (Screen beats Overlay for additive bloom), Opacity 0.500, Alpha Masks Light Sources ON (40:19, 40:24); for text/graphics use a **low threshold ~0.147, Spread 0.000, Screen** (41:07)
- Looks saved as reusable **gallery stills / PowerGrades**: GLOW SOFT, SHARP, TOP WINDOW, and per-camera input CSTs **"ARRI LogC3 → DWG"**, "S.Gog3 Gamut Cine → DWG" — one-click presets (38:35, 41:14, 46:41)
- Available FX library = Film Grain, Halation, Glow, Lens Reflections, Light Rays, Beauty, Face Refinement, Contrast Pop, CST, Dehancer (used on the ITV job, sits late, before final CST out) (35:14, 37:33)
- Node **Composite Mode** menu used to blend look layers (Screen/Overlay/etc.) (38:18)

### Distinctive opinions
- **Do NOT use Resolve's Broadcast Safe** — it crudely clips everything; manage levels by eye on the waveform instead (53:00, 53:03)
- QC by eye on the **0–1023 waveform**: aware of clipping, **controlled highlight clip OK**, crushing blacks to 0 OK, but keep an eye on legal whites (soft-knee, not hard clamp) (53:11, 53:31)
- **DaVinci Wide Gamut over ACES** by default; ACES only for spec-mandated (Netflix) deliveries — he does BBC/non-Netflix (44:09, 44:15)
- **Tiered grade:** fast-turnaround YouTube (1 video/week) = first ~3 nodes only (balance/contrast/sat), skip Film Look Creator & heavy FX (44:57, 45:29)
- **Look by genre:** music-video = opposing-color contrast, everything pushed into the warm vectorscope quadrants; documentary = clean/neutral (55:04)
- ColorChecker/ARRI chart in frame as a neutral calibration reference (40:05)

### Delivery (49:44, 51:43, 52:08)
- Timeline 1920×1080, 25p, 10-bit, square PAR, ProRes 422 HQ proxies
- Render: **MXF OP1A / DNxHR HQX 10-bit**, 1080p, CBR, Color/Gamma tag = "Same as project"
- Advanced: Flat Pass off, Data Levels Auto, Bypass re-encode ON

### ENGINE — what a headless auto-grader should adopt
- **Hard-code the ordered op-chain:** input CST → exposure/balance (via offset) → contrast → saturation → parallel per-range corrections (highlights/shadows/density/curves) recombined → trim → directional power-window bank (L/R/T/B) → film-look → output CST. Keep it a fixed superset; **disabled stages = identity pass-through** (toggle by flag, never rebuild).
- **CST sandwich every clip:** per-camera input CST (e.g. Canon Cinema Gamut/CLog3, ARRI LogC3) → **DWG/DaVinci Intermediate** working space → terminal **Rec.709 Gamma 2.4** output; DaVinci tone-map, Adaptation ~5, White Point Adaptation on, Gamut Mapping none.
- **Seed primaries:** Offset 25 lift, Contrast pivot **0.435** (log space), Sat baseline 50 (≈+15% for grade), Lum Mix 100.
- **Skin pipeline:** push the orange/skin lobe in hue-vs-sat (Color Warper) and add **density on the Skin vector** (ColorSlice); aim the skin trace at the vectorscope skin line.
- **Source detection:** read waveform flatness/lifted blacks to classify log vs Rec.709 and pick the input CST automatically.
- **NR is an early, separable, low-strength stage** (temporal frames 2 + spatial), placed before the grade — never after.
- **Look layer:** film emulation as a **partially-blended (~0.32) terminal pass**; bloom via threshold-gated bright-region blur (thr 0.75 imagery / ~0.15 text) composited **Screen**.
- **QC guardrails:** judge on a 0–1023 waveform — shadows above 0, highlights under 1023, **soft-knee not hard legal clamp**; allow controlled highlight clip / black crush. Do **not** auto-apply Broadcast Safe.
- **Tier the cost:** cheap 3-node base (balance/contrast/sat) for fast jobs; gate the expensive look/FX stage. Genre-keyed look selector (music-video = warm-quadrant opposing contrast; documentary = neutral).