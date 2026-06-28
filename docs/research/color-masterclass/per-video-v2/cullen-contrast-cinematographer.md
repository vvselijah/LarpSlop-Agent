## cullen-contrast-cinematographer — Cullen Kelly - contrast secrets for cinematographers

**Tooling:** DaVinci Resolve Studio 20, project `2026-005 Grading for DPs Pt 1`. Working space = DaVinci Wide Gamut / DaVinci Intermediate (DWG/DI). All grading decisions made *through* the display transform.

### Governing philosophy
- **"Greatest Gains for Least Effort"** (00:54) — at every step ask "what's the next most impactful thing I can do to achieve my creative intent?" Prioritize moves by impact-per-cost.
- **"Macro Beats Micro"** (04:29) — a fix that works for many shots beats one that fixes a single shot. In the ideal case, one output transform finishes the whole timeline (04:39).
- **The order is fixed (00:08, 07:43):** Step 1 = set up the imaging pipeline / DRT / viewing LUT (the single most important first choice, 06:30). Step 2 = per-shot exposure + color balance. Pipeline BEFORE any primary grade.
- **"80% in two moves" (12:19):** the first two balance moves (separation + skin) define most of the look.

### Node tree / workflow order (as built on screen)
1. **Node 01 — input CST** (camera → working space). Tagged `DWG`. Tone Mapping = None, Gamut Mapping = None (container conversion only, not a look). Primaries left at identity (01:30–02:39).
2. **Node 02/03 — output DRT** (working space → display). Either Resolve's stock CST or the **Referent** display LUT, stacked above node 01 (05:04, 06:59). Two-node stack (01 over 02/03) is the baseline pipeline.
3. **Per-shot grade** done on a corrector node *after* the pipeline, using the **Offset wheel** only (07:53 onward).

### Input CST settings (Node 01) — per camera, all → DWG / DaVinci Intermediate
| t | Input Color Space | Input Gamma | Tone/Gamut map | Note |
|---|---|---|---|---|
| 01:54 | ARRI Wide Gamut 3 | ARRI LogC3 | None / None | Apply Forward OOTF |
| 02:01 | Panasonic V-Gamut | Panasonic V-Log | None / None | same common output |
| 02:39 | REDWideGamutRGB | RED Log3G10 | None / None | **White Point Adaptation ✓** |

Every camera lands in the SAME working space (one common mapping).

### Output DRT settings
- **Stock Resolve CST as DRT** (03:03, 03:29): Input DWG/DI → **Output Rec.709 / Gamma 2.4**. Tone Mapping = **Luminance Mapping**; Use Custom Max Input ✓ = **10000 nits**; Use Custom Max Output ✓ = **100 nits**; **Adaptation = 9.00**. Gamut Mapping = **Saturation Compression**, **Saturation Knee = 0.900**, **Saturation Max = 1.000**. Apply Forward OOTF ✓, Use White Point Adaptation ✓.
- **Alternative DRT = Referent LUT** (05:04): `Referent_DWG_to_Rec709_v1.0`, installed under the **CKC** LUT folder — a free DWG→Rec709 display LUT, hot-swapped in place of the stock CST. Cullen's recommended look: deeper blacks, more contained/healthier saturation, "healthy contrast and healthy colors" straight out of the transform (05:50, 06:18 A/B). Free download (07:25).
- A/B framing (03:49, 04:02): the stock CST leaves footage flatter (esp. high-key skywalk shot, 06:18) — contrast you'd then have to add downstream. DRT choice IS the contrast lever.

### Pipeline-default parameter baseline (neutral, repeated across frames)
At every pre-grade state the primaries sit at: Lift 0.00 / Gamma 0.00 / **Gain 1.00** / **Offset 25.00** (R=G=B), **Contrast 1.000**, **Pivot 0.435**, **Saturation 50.00**, **Hue 50.00**, Lum Mix 0.00, Temp 0.0, Tint 0.00 (01:44, 02:58, 03:03, 07:53, 11:58). Offset neutral = 25.00; Pivot 0.435 ≈ mid-grey anchor.

### Per-shot exposure + balance — the Offset wheel (only tool)
Offset = "the oldest tool in motion-image mastering" (07:48), the digital analog of analog color-timing printer lights (07:54). Used for BOTH exposure (level) and balance (chroma).

| t | Shot | Offset R / G / B | Move |
|---|---|---|---|
| 07:53 | window/dusk | 25.00 / 25.00 / 25.00 | neutral start |
| 08:41 | underexposed dusk | **34.13 / 34.13 / 34.13** | expose up, equal RGB (~+9 master lift, pure level) |
| 09:13 | same | **39.07 / 39.07 / 39.07** | continue lifting to taste, still R=G=B (zero hue shift) |
| 10:05 | nightclub closeup | 22.92 / 22.92 / 22.92 | balanced pull-down |
| 10:16 | (low-sep example) | 17.11 / 17.11 / 17.11 | balanced |
| 11:40 | female portrait | 24.71 / 25.15 / 25.44 | slight warm/asymmetric balance |
| 13:47 | florist/plaid | **29.49 / 27.24 / 29.45** | R+B up, **G held ~2 below** = magenta/warm push to separate skin from green foliage |

- **Expose up** = raise all three Offset channels equally (master level), keep R=G=B for a neutral lift (08:41, 09:13).
- **Balance** = nudge Offset chroma asymmetrically; here pulling Green down ~2pts vs R/B counters a heavy green garden background (13:47).
- **"Spin the offset" probe** (09:44): even on a well-exposed shot, routinely rotate the offset chroma a touch to test whether a slight balance improves the image.

### Two Keys for Color Balance (framework, 09:57–11:30)
1. **Max out color separation** — get as much spread between distinct hue regions on the vectorscope as possible (10:02). Low separation = the whole trace bunched in one lobe/region (10:16). Push separation *aggressively* — "I can always kill it later" (11:30).
2. **Improve (or maintain) skin tones** — skin must get better or at least *no worse* as a result of the balance (11:14). Hard constraint, not a free variable.
- These are the **two anchors** Cullen "clocks" to decide: is the balance good / done / needs more work (11:21). Iterative loop: tweak → re-read scope separation → check skin → repeat (11:28).

### Distinctive opinions
- **Skin judged BY EYE, not by snapping the trace to the vectorscope skin line** (11:40) — rejects the "arbitrary metric" of forcing skin onto the 123° I-line; perceptual call beats the gauge.
- **Balance = "resensitizing the sensor"** (12:48): conceptually you're rescaling the camera's red/green/blue *buckets* to a color of light — i.e. channel-wise gain in sensor/linear space, NOT a hue rotation.
- DRT/pipeline is swappable and free; the single highest-leverage decision in the whole grade is which display transform you view through.

### ENGINE: what a headless auto-grader should adopt
- **Order of ops:** (1) per-camera input CST → DWG/DI (tone+gamut map = None; white-point adaptation for RED); (2) output DRT DWG/DI → Rec.709 Gamma 2.4; (3) per-shot Offset pass. Never primary-grade before the pipeline is set.
- **Pin the DRT as the contrast/look engine.** Default baseline to diff against = stock CST luminance tone-map (max-in 10000 / max-out 100 nits, adaptation 9.0, gamut saturation-compression knee 0.9). Allow hot-swapping a DWG→Rec709 display LUT (Referent-style) as the look-defining transform — set once, applies timeline-wide (macro-beats-micro).
- **Per-shot correction = a single Offset stage** (additive RGB lift on a 0–100/neutral-25 scale), applied AFTER the output transform. Exposure = equal R=G=B step (e.g. +9 → 34); balance = small asymmetric per-channel deltas (~±2).
- **Detect underexposure** per shot (median luma below target) and correct only the gap — trust the transform for the base render.
- **Balance objective = constrained optimization:** maximize vectorscope hue-spread (separation) SUBJECT TO skin-tone delta ≥ 0. Two-term loss: separation score + skin-fidelity score; iterate until both hold. Search a small offset-hue neighborhood and keep the variant that improves separation without hurting skin.
- **Skin metric should be perceptual, not a hard 123° snap.** Push separation aggressively (recoverable), gate on skin health.
- **~80% of the look = 2 ops** (separation push + skin-safe balance) per shot — a cheap default to converge on.