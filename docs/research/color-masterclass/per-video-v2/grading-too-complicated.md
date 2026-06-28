## grading-too-complicated — Has Colour Grading Got Too Complicated? (color mgmt)

**Authority's thesis:** A managed grade in DaVinci Wide Gamut, built on a *fixed* node tree, treated like a map. Get the three fundamentals (balance, exposure, contrast) right inside the working space, then output via a CST or print DRT. Heavy use of Mononodes DCTLs (Utility heatmaps, MONO-Balance, MONO-Density/Color Shift) over native tools.

### Tip 1 — Fixed node tree (build the same map every time)
The full production tree (project `2026_MAY_ PRO TIPS FOR BETTER GRADES`), node labels as seen `00:47`–`02:51`:
- **Serial trunk:** `01 CAM>DWG` (input CST) → `03 BAL/EXP` → `04 CONTRAST` → `05 SAT`
- **Parallel mixer off SAT:** `06 TEMP`, `08 HSV SAT`, `09 HDR`, `10 WARPER`, `20 CURVES` → recombine
- `11 TRIM` → **parallel power windows** `12 PW1` / `14 PW2` / `15 PW3` → recombine
- **Finishing tail:** `16/17 Texture` → `02/18 Density` → `19 FILM` → `21 DRT` (output)
- Node numbers are non-sequential — **layout order ≠ exec order**; execution follows the wiring (`01:05`).

**Simplified teaching chain** used for the rest of the episode (`01:37`, renumbered):
`01 CAM>DWG` → `02 BAL/EXP` → `03 CONTRAST` → `04 SAT` → `05 HSV SAT` → `06 DWG>709`
The two CSTs are the "sandwich" bookends; the four middle nodes are the grade.

### Tip 2 — Color management (the CST sandwich)
- **Input CST** `CAM>DWG` (`02:26`): Input Color Space = **ARRI Wide Gamut 3**, Input Gamma = **ARRI LogC3**; Output Color Space = **DaVinci Wide Gamut**, Output Gamma = **DaVinci Intermediate**. Tone Mapping = **None**, Gamut Mapping = **None**, Use White Point Adaptation = **on**, OOTF off. → Grade *between* the two transforms; never grade on log or Rec.709-tagged media.
- **Output CST** `DWG>709` (`02:38`): Input = DWG / DaVinci Intermediate; Output = **Rec.709 / Gamma 2.4**. Tone Mapping = **DaVinci**, Max Input **10000 nits**, Adaptation **9.00**. Gamut Mapping = **Saturation Compression**, Saturation Knee **0.900**, Saturation Max **1.000**. Apply Forward OOTF **on**, White Point Adaptation **on**.
- Output is **swappable** (`02:39`, `03:07`): plain CST *or* a print DRT, both landing in Rec.709.
- **Print-DRT alternative** — node 21 runs Mononodes **MONO-LAB** DCTL (`02:59`): Exposure 0.000, Contrast 1.000, **Pivot 0.391**, Tone Compression 0.000, Highlights 1.000, Black Point 0.000, Shadows 0.000.

### The three mandatory fundamentals (gate before any look)
Balance / Exposure / Contrast must all pass first; order among them doesn't matter (`08:14`).

**Exposure** — set on the **HDR Color Wheels Global** zone, *not* per-zone or the primary Lift/Gamma/Gain (`05:03`, `07:52`):
- Global **Exp 0.63** is the primary lever (`07:16`, `07:52`); zone wheels left at Exp 0.00 (Dark/Shadow/Light balance offsets only: Dark b0.20, Shadow b0.22, Light b0.22).
- Judged on the **waveform**, not a fixed number: mid-tones target **~384 / 1023** (`05:10`). HDR Global ≈ a scene-linear exposure multiplier (`07:52`).

**Balance (skin)** — uses Mononodes **MONO-Balance-v1.4** Utility DCTL on a `SKIN BAL` node, ordered *after* `EXPOSURE` (`06:26`):
- DCTL params: Skin Tone Range **0.500**, Deviation Range **1.000**, Hue Angle **0.000**, Split Position **0.271–0.500** (`05:52`–`08:09`). Modes: Exposure Heatmap / Skin Tone Indicator / Saturation Heatmap / Gray-Out Non-Skin; Split Vertically; Show Guide on.
- **Heatmap exposure scale** runs **−5…0…+5** false-color bands; **mid-gray reads 0.391 at band 0** (`05:36`, `05:37`). Lighter skin lands yellow band, darker skin green band — a reference, not a hard target.
- **Skin-on-line convergence trick** (`07:20`–`07:22`): push the Global wheel until the skin heatmap turns **yellow** = skin sitting *on* the vectorscope skin-tone line. Past that it goes **magenta** = overshot. Yellow is the precise sweet spot.
- Vectorscope: skin should sit **on the skin-tone (I) line**; here it reads slightly under (`06:52`–`07:02`). Under/over is fine **if consistent across the scene**. Without the DCTL, measure the skin lobe's hue angle vs the diagonal directly (`06:40`).

**Contrast** — preferred method is **Gain + Offset**, not the Contrast slider (`08:34`):
- Watch the waveform — **Gain** = highlight multiplier (top of trace), **Offset** = black floor (bottom), set white/black points independently against the 0–1023 scale (`08:37`).
- Demo move: **Gain 1.28** all channels, **Offset 22.95**, pivot held (`08:50`).
- If you *do* use the Contrast slider: in **DaVinci Wide Gamut set Pivot to 0.336** for correct middle grey (default 0.435 is wrong for DWG) (`08:26`).

### Saturation (his actual 2026 method)
- **Avoid native RGB saturation** — over-pushed global Sat (50→64.40) gives a harsh "video/digital" look (`09:38`). Negative example.
- **HSV-saturation trick** (`10:12`, `10:25`): right-click the `HSV SAT` node → Color Space = **HSV**, then push **Gain** in primaries — only channel 2 (S) responds, giving value-independent (luma-safe) saturation.
- **Color Slice** = per-hue-zone saturation, 7 named bands (Red / **Skin** / Yellow / Green / Cyan / Blue / Magenta), each with Center/Hue + dual faders under one global Saturation (`10:38`–`10:50`). Demo: global **Saturation 1.50** (`11:25`).
- **His preferred tool** — Mononodes **Color Shift** DCTL (`MONO-Density-v2.1`), Studio-only (`11:43`–`11:51`): per-channel **density** sliders (demo **Red Density 0.465**, others 0.000). The DCTL family exposes three orthogonal axes — **DEN / HUE / SAT** (density-aware, per-hue saturation).

### Distinctive opinions
- A fixed labeled node tree is the #1 productivity move ("treat it like a map") — keeps you on track under time stress.
- Color management (CST sandwich) is non-negotiable; the output transform is interchangeable (CST vs print DRT).
- Set exposure on the **HDR Global** wheel, not primaries; do contrast with **Gain+Offset**, not the slider; do saturation in **HSV / density**, never naive RGB.
- Heavy reliance on **Mononodes** DCTLs (Utility heatmaps, MONO-Balance, MONO-Density/LAB) as the modern "make-it-simple-again" toolkit — the irony answering the video's title.

### ENGINE: what a headless auto-grader should adopt from this video
- **Bracket every grade in a CST sandwich:** input transform (per-camera, e.g. ARRI WG3/LogC3 → DaVinci Wide Gamut / Intermediate, white-point adapt on, no tone/gamut map) → grade ops → output transform (DWG → Rec.709/Gamma 2.4, DaVinci tonemap @ 10000 nits / adapt 9.0, saturation-compression gamut map knee 0.9 / max 1.0). Never grade on log or display-tagged media.
- **Fixed ordered stage list:** input-CST → balance/exposure → contrast → saturation → (HSV sat / per-hue) → secondaries/windows → texture/film → output DRT. Labels ≠ exec order; follow the wired DAG.
- **Exposure as a single global linear multiplier** (HDR Global ≈ +0.63 here), targeting mid-tones ~384/1023 on the waveform; don't hard-code an IRE.
- **Contrast = Gain (highlight mult) + Offset (black floor) about a fixed pivot**; if using a pivot-contrast primitive, set pivot to the working-space mid-grey (0.336 for DWG), not 0.435.
- **Skin auto-balance:** compute the skin-pixel cluster's hue angle vs the vectorscope skin-tone (I) line (~123°); drive global exposure/tint until skin sits *on* the line (the heatmap "yellow" state); flag overshoot (magenta) and under (green/blue). Allow a consistent offset across a scene.
- **Exposure false-color = bucketize Rec.709 luma into −5…+5 bands**, band 0 ≈ mid-gray 0.391 (~18%); flag subject-under vs background-hot per region.
- **Saturation must be luma-safe:** operate on the S channel in HSV, not RGB gain; expose per-hue bands with a protected **Skin** band; model the pro path as **density-aware perceptual saturation** with three axes (density / hue / saturation).
- **Output transform is a choice:** expose `output = {CST | film-print DRT}` — model the print DRT as a tunable tone curve (mid-grey pivot ~0.391, tone compression, independent black-point/shadow lift), not a fixed LUT.