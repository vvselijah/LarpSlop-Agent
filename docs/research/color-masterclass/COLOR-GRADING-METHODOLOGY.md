<!-- AUTO-SYNTHESIZED from deep analysis of 14 DaVinci masterclasses (yt-dlp+frames; see README.md). Engine-facing + teaching. 2026-06-24. -->
# The Cinematic Color-Grading Method — Consensus Reference, Engine Spec & Masterclass Outline

*Synthesized from Mostyn, Mullins, Cullen Kelly, Blakely, Frenchie, and the film-emulation/qualifier sources. Where authorities disagree, the dispute is flagged inline rather than papered over.*

---

## 1. The professional color-grading method (consensus)

The professional method is a **managed, ordered, stage-by-stage pipeline**: put the image into a known wide working space, build a fixed labeled node tree, then grade broad-to-fine (balance → contrast → saturation), match shots, add secondaries, build a look, and finish — verifying each stage on scopes against numeric targets but deciding final intent by eye on a calibrated monitor.

### Stage 0 — Color management / input transform
**Tool:** Project = DaVinci YRGB. Node 01 = a CST (Color Space Transform) or RCM input mapping.
**Do:** Map the camera's native color space + transfer function into a large working space — **DaVinci Wide Gamut / DaVinci Intermediate (DWG/DI)** is the consensus working space (6 sources). Detect/accept per clip:

| Camera | Input color space | Input gamma |
|---|---|---|
| ARRI | ARRI Wide Gamut 3 | LogC3 |
| Sony | S-Gamut3.Cine | S-Log3 |
| RED | REDWideGamutRGB | Log3G10 |
| Fujifilm | F-Gamut | F-Log |
| Blackmagic | BMD Wide Gamut | BMD Film |
| Phone / unknown | Rec.709 | Rec.709 (fallback) |

**Project hygiene set here, before any node is created:**
- **3D LUT interpolation = Tetrahedral** (never Trilinear — causes banding when LUTs/film emulation apply). *(2 sources, "cannot stress this enough" — Mullins.)*
- **"Luminance mixer defaults to zero" = ON** — must be set before node creation so color wheels stop dragging luma.
- Broadcast-safe OFF in a managed pipeline; timeline res ≥ highest deliverable.

**Scope check:** trace is lifted, low-contrast, milky (log) — **this is expected**; nothing should clip.

### Stage 1 — Output / display transform (the other half of the "CST sandwich")
**Tool:** Final node = CST DWG → Rec.709, **Gamma 2.4** (broadcast/calibrated) or **Gamma 2.2** (web/social/phone). Or a DRT / viewing LUT.
**Do:** Convert the working space back to display space so **all grading happens UNDER a correct display-referred image**. Set Tone Mapping = DaVinci / Luminance Mapping; Gamut Mapping = Saturation Compression to fold out-of-gamut highlights back in.
**Why it's done first (after input):** Kelly's "macro beats micro" — the output transform is the *single most impactful decision* because it corrects every shot at once. Build the sandwich, then grade inside it.
**Scope check:** image now reads as a finished/contrasty starting point. Confirm no hard clip at **1023** (top) or **0** (bottom).

> **Disputed — output gamma:** 2.4 (Mostyn best-node-tree, Kelly contrast) vs 2.2 (Mullins, Kelly project-settings, Frenchie — "grade for how it's actually viewed: Mac/iPhone/YouTube"). **Deliverable-dependent.** For IG/Reels, default **2.2**.

### Stage 2 — Build the empty labeled node skeleton
**Tool:** Serial nodes, hand-named, built empty *first* as a checklist:
`CAM>DWG → BAL/EXP → CONTRAST → SAT → [optional: TEMP/HDR/CURVES] → [TRIM] → [PW1–3] → [TEXTURE] → [FILM/LOOK] → DWG>709`
**Do:** Lay the fixed tree so under time pressure the order is never in question; fill in order, leave unused nodes empty. One idea per node → each independently toggleable (`Cmd/Ctrl+D` one node, `Shift+D` whole clip) and copyable.

### Stage 3 — Balance + exposure (≈80% of the image — Kelly)
**Tool:** BAL/EXP node — **Offset wheel** and/or **HDR Global wheel**. Advanced variant: set **Gamma = Linear**, then balance with the **Gain wheel only** (Kelly/Mullins/Cullen-settings).
**Do:** Set overall brightness where the image should "live"; neutralize color casts so neutrals read neutral. **Fix skin here, globally — do NOT key skin** (2 sources, Mostyn's explicit Tip 5: if skin is wrong, reset and re-balance; never qualify skin).
**Scope checks:**
- **Waveform:** blacks near **0** (not crushed below), highlights high but **under 1023** (not clipped).
- **Parade:** over a neutral object, drive **R = G = B** so it reads as a white (overlapping) trace; channel separation = a cast.
- **Vectorscope:** skin lobe toward the **upper-left I-axis skin line (~11 o'clock, ~123°)**, consistent across shots.
- **Skin IRE (false color):** bulk of face **~40–50 IRE** ("~50, maybe a little less" — Mostyn); range ~35 low to 55–60, only a small forehead/cheek highlight reaching ~70. Keep the *bulk* of the face below the 55–65 IRE "gray" highlight band.

### Stage 4 — Contrast
**Tool:** CONTRAST node — primaries **Contrast + Pivot**, or Gain up / Lift down.
**Do:** Add tonal separation/pop around the correct pivot. **Judge with saturation pulled to zero** — color deceives the eye when setting contrast.
**Pivot value (disputed):** **0.435** in Rec.709 (Resolve default, beginner demos) vs **0.336** for true middle-gray in DWG/Intermediate (Mullins, grading-too-complicated overlay). Use the pivot matching your working space.
**Scope check:** waveform trace spreads floor-to-ceiling without clipping; the log histogram spike spreads out.

> **Disputed — S-curve project setting:** Kelly leaves "use S-curve for contrast" OFF (wants a clean *linear* contrast operator so he can crush to the floor and let the downstream look/output transform supply the roll-off). Beginner default ON soft-clips. Taste + pipeline dependent.

### Stage 5 — Saturation
**Tool:** SAT node — **HDR global saturation** OR **Color Slice saturation** (subtractive "density," deepest/most natural). Optional HSV-channel node. **Leave the primary Saturation slider at its 50.00 default.**
**Do:** Add saturation **without raising luminance**. The primary Sat slider lifts the waveform (bad); HDR/Color Slice hold or lower it (good).
**Scope check:** waveform height does **NOT** rise when sat is added (the luma-safe proof); vectorscope trace extends but stays within target boxes / doesn't splay.

> **Disputed — saturation engine:** Mostyn favors HDR global sat; Mullins specifically favors Color Slice (subtractive); Frenchie uses Color Slice "density." They agree on the **principle (luma-safe)**, disagree on the exact tool.

### Stage 6 — Shot matching
**Tool:** MATCH node + **Parade scope** (THE scope for matching); reference still / split-screen wipe; **Lum Mix = 0**.
**Do:** Pick a hero shot, normalize + balance it, then line up each clip's per-channel parade trace to the reference **tone-band by tone-band** (shadows, mids, highlights).
**Scope check:** each channel approximates the reference in shadows and highlights; ignore regions with no counterpart in the reference.

### Stage 7 — Secondaries (only if needed)
**Tool:** Parallel cluster — HSL qualifier (roll off edges), Power Windows (+ tracker), Color Warper, Curves. **Key NON-skin only.** Feather every key.
**Do:** Isolate a color/luma zone for targeted fixes — recover sky, vignette, desaturate wardrobe, split-tone a region.
**Scope check:** toggle the isolated node on/off to confirm it improves the shot; watch for hard-clipped/artifacting keys.

### Stage 8 — Look development / film emulation
**Tool:** FILM/LOOK node — split-tone curves (**Lum Mix = 0** for independent RGB) OR a print-emulation LUT (**Kodak 2383**) fed **Cineon film log via a pre-CST**, compounded for keyable 0–100 strength.
**Do:** Build the creative identity — warm highlights / cool shadows, density, print emulation. **Run the grade UNDER the look at partial mix (~50%).**
**Critical:** print LUTs expect **Cineon/film-log input, NOT Rec.709 g2.4** (3 sources). Insert CST (Rec.709 g2.4 → Rec.709 Cineon Film Log) immediately *before* the 2383 LUT.
**Scope check:** watch for LUT-lifted/washed blacks; restore the low end with a correction node beneath the LUT.

### Stage 9 — Texture / finishing
**Tool:** TEXTURE node — film grain, **halation**, optional diffusion/sharpen.
**Halation recipe:** isolate highlights → blur → weight **red/orange high, blue low** → composite **ADD in linear light**.
**Grain:** sparing; lives in **shadows/mids**.
**Scope check:** confirm grain survives export (needs high data rate; ~100,000 kb/s at 4K so platform compression doesn't smear it).

### Stage 10 — QC + propagate
**Tool:** Gallery **Still / PowerGrade**; **Light Box**; skin-balance heatmap at timeline level.
**Do:** Grab the approved look as a Still, apply across the timeline, then eyeball all thumbnails — skin/exposure should land in the same region across the scene.
**Scope check:** Light Box — all shots consistent (all on the line, or all consistently under).

---

## 2. Node tree + why

**Consensus structure — the "CST sandwich" with a fixed labeled spine:**

```
[01 CST: CAM → DWG]         ← INPUT transform (head)
   │
[BAL/EXP]                    ← Offset/HDR; balance + exposure; skin fixed here
   │
[CONTRAST]                   ← contrast + pivot, judged at sat=0
   │
[SAT]                        ← HDR/Color Slice, luma-safe
   │
[ (optional parallel cluster: TEMP · HDR · WARPER · CURVES) ]
   │
[ TRIM ]
   │
[ (parallel cluster: PW1 · PW2 · PW3) ]   ← windows, NON-skin secondaries
   │
[ TEXTURE ]                  ← grain · halation
   │
[ FILM/LOOK ]                ← split-tone curves OR [pre-CST → 2383 LUT] compound, ~50% mix
   │
[ CST: DWG → Rec.709 2.4/2.2 ]  ← OUTPUT transform (tail), grade UNDER this
```

**The 4–6 node core** (the two transforms + `BAL/EXP → CONTRAST → SAT`) is what 4+ independent sources converge on. The minimal teaching tree (grading-too-complicated) is exactly:
`CAM>DWG → BAL/EXP → CONTRAST → SAT → [HSV SAT] → DWG>709`.

**Why this structure:**
- **Sandwich** → every move happens in a wide working space but is *seen* display-referred; you never grade "blind" on log.
- **Fixed broad-to-fine order** → you lock the foundation before any look; foundation errors don't propagate into creative decisions.
- **One idea per node** → free before/after (toggle a node), free copy/paste of a single fix, and a self-documenting tree.
- **Built empty-first as a checklist** → under deadline the order is never improvised.
- **Saved as a Still/PowerGrade** → one approved look propagates to the whole timeline; for a new camera you only **re-point node 01's input transform** — the rest of the tree is camera-agnostic.

**Where authorities differ (all sanctioned):**
1. **Parallel vs serial** for fine-tune/secondary clusters — Mostyn/grading-too-complicated use `Alt+P` parallels off the clean foundation; simpler tutorials keep everything serial.
2. **Look as a separate node vs a compound node** with an internal CST (Mostyn/film-emulation compound it for keyable strength).
3. **Branch count** — Frenchie: one parallel branch (split-tone); Mostyn: two parallel clusters. Mullins inserts MATRIX (3×3 skin) + HSV/HK DCTL nodes.
4. **Automatic color management (DRCM/ACES) vs manual node CSTs** — Frenchie runs DaVinci Color Managed with per-clip input transforms; Mostyn/Mullins/Kelly prefer explicit CST nodes for transparency. Preference split, both valid.

**Consensus discipline regardless of node count:** every node hand-labeled, one purpose per node, built empty-skeleton-first, saved as a Still/PowerGrade, re-pointed at node 01 per camera.

---

## 3. Scopes — how pros actually read them

Scopes are a **guide, not a target** (3 sources). They park exposure, catch clipping, and catch casts; **taste finishes the grade** on a calibrated monitor. "Get exposure to FEEL right, not BE right" (Kelly); "I'm not grading by scopes" (Mostyn).

**Universal scale (all sources):** 10-bit, **0 = black, 1023 = white**; gridlines at 128 / 256 / 384 / 512 / 640 / 768 / 896.

### Waveform (the workhorse)
- **Black floor:** sit blacks **near 0**, do NOT crush below 0 (loses shadow detail). Faded-film looks deliberately lift the floor off 0.
- **Highlight ceiling:** high but **below 1023**. Blakely's rule: top of trace at the **2nd graticule line from the top** (just under 1023).
- **Shadow placement (Blakely):** bottom of trace between 0 and the 1st line up (~halfway).
- Reads overall exposure + contrast spread at a glance.

### Parade (R / G / B separate — THE matching scope)
- Over a **neutral object**, the three channels should **overlap = white trace**. Separation over a neutral = a **color cast** in that tonal region (e.g. green channel high in shadows = green shadows).
- Shot matching is done here, **channel-by-channel, tone-band by tone-band**, against a reference clip.

### Vectorscope (hue + saturation, polar)
- **Skin-tone line:** upper-left I-axis, **~11 o'clock / ~123°**. Land the skin lobe **on or near** it.
- Mostyn prefers skin **slightly UNDER** the line (reads slightly green) — real cinema skin sits under. Color-coded: **green = under / yellow = on / magenta = over**.
- **Consistency across shots > absolute position.** "On, under, or over — but consistently."
- Saturation discipline: trace **extends but stays within target boxes**, doesn't splay.

> **Disputed — is the skin line a hard target?** Mostyn uses it as the primary skin method (but values consistency over exact position). **Kelly explicitly rejects it as a target** — "health of skin to my eye, not by some arbitrary metric." Mullins also avoids a numeric angle (skin by-eye via 3×3 matrix/HSV in DWG). Treat the on-line vs under-line position as **tunable**; the **load-bearing, agreed target is cross-shot consistency.**

### Histogram
- Log footage = a **tall central spike** (low contrast). A correct grade **spreads the spike** toward both ends without piling up at 0 or 1023.

### Skin / exposure targets (numeric)
| Metric | Target |
|---|---|
| Skin IRE (false color) | Bulk ~**40–50 IRE**; range 35 → 55–60; small highlight to ~70. Keep bulk below the 55–65 "gray" band. |
| Skin hue | On/near the ~123° line; slightly under = slightly green (Mostyn); **consistency first**. |
| Exposure heatmap (Mononodes) | Flat-lit skin ~**0** (perfect); a key-lit side reading slightly hot (>0) is **correct**, not an error. |
| Neutral balance | Neutral object = overlapping R=G=B (white) trace. |
| Contrast pivot | **0.435** Rec.709 / **0.336** DWG. |
| Resolve neutral defaults | Lift 0.00, Gamma 1.00, Gain 1.00, Offset 25.00; Contrast 1.000, Sat 50.00, Hue 50.00, Lum Mix 100.00. |

---

## 4. What this means for our headless engine

Target architecture: a Python + ffmpeg (and/or OpenColorIO) auto-grader structured as the **same CST sandwich**: `input_transform → [working-space ops, broad-to-fine] → output_transform`, with the grade represented as a serialized labeled node graph (JSON) you can save once, apply to many clips, diff, and toggle per node.

### 4.0 Color management / log handling (6 sources — most important knob)
- Implement an **input-transform stage**. Per clip, detect/accept camera color space + transfer function (LogC3, S-Log3, Log3G10, F-Log, BMD Film, Rec.709 fallback) and convert to a wide working space **before any op**.
- Use **OpenColorIO** (ACES or a DWG-equivalent config) as the headless analog of Resolve's CST, or ffmpeg `zscale` + `lut3d`. OCIO is the right primitive.
- **The single most important config knob = correct input transform per clip.** Everything downstream assumes it. Expose `--input-colorspace` / `--input-gamma` with auto-detect from metadata + a fallback.

```python
# config knobs
input_colorspace = autodetect(clip) or "rec709"     # logc3|slog3|log3g10|flog|bmdfilm|rec709
working_space    = "dwg_linear"                       # do all math here
output_gamma     = 2.2                                # 2.2 social default; 2.4 broadcast flag
lut_interp       = "tetrahedral"                       # never trilinear
```

### 4.1 CST sandwich + output (4 sources)
- Pipeline = `input_transform → working ops → output_transform`. **Last stage** bakes to Rec.709 — **Gamma 2.2 default** (IG/Reels viewing) with a `--gamma 2.4` broadcast flag.
- Apply output as an OCIO display/view transform, or a baked `.cube` via ffmpeg `lut3d` with **`interp=tetrahedral`** (2 sources — checkable detail).

### 4.2 Broad-to-fine order, hard-coded (6 sources)
- Fixed pass order, never reordered: **(1) exposure normalization → (2) white balance / cast removal → (3) contrast → (4) saturation.** Each is a separate, independently-toggleable function (`{label, op, params, enabled}`) so A/B and per-clip overrides work. Maps to a small DAG of numpy/ffmpeg stages.

### 4.3 Exposure to mid-grey (7 scope sources)
- Headless scope module: compute waveform/parade (per-channel row histograms) and vectorscope per frame.
- **Auto-exposure:** push black floor toward **~0** (clamp, **no negative crush**); push highlights toward but **under 1023**; **flag clipping**. Anchor mid-grey (e.g. drive scene mid-grey toward pivot **0.336 in DWG** / 0.435 Rec.709).
- Prefer **global Offset** (additive in log) and **gain-on-linear-gamma** over lift/gamma/gain — additive offset is the cleanest least-destructive global move and maps directly to a per-channel add/multiply.

### 4.4 White balance (7 sources)
- Over **detected-neutral regions**, drive **R/G/B means to equality** (white parade trace).
- **Decouple luminance** when balancing channels — operate on chroma with luma locked (the headless **Lum Mix = 0** equivalent) so balancing doesn't drift exposure (3 sources).
- Avoid temp/tint-style hue tints for primary balance; use additive offset.

### 4.5 Filmic tone / contrast (6 sources)
- Contrast operator around the **correct pivot** (0.336 DWG / 0.435 Rec.709), **judged with saturation forced to 0** internally if you auto-tune the amount.
- Keep the contrast operator **linear** (don't bake an S-curve) so the look/output transform supplies roll-off — mirrors Kelly's S-curve-OFF stance and keeps shadows controllable.

### 4.6 Skin line (4 sources, with dispute)
- Analysis pass: convert a face region to YCbCr / the vectorscope plane, find the skin cluster (Cb/Cr or HSV orange band), measure its angle vs the **I-line (~123°)**, nudge WB until skin sits **on/just-under** the line.
- **Optimize for CONSISTENCY across clips** (minimize variance of skin angle + IRE between shots), not a single fixed angle — that consistency metric is the load-bearing, agreed target.
- **Never key skin** (2 sources): fix skin via the **global WB/exposure solver** (use skin as a balance reference). Reserve masked/keyed ops for **non-skin** targets only.
- Treat exact on-line vs under-line as a **tunable** (`skin_offset_deg`), since authorities split.

### 4.7 Saturation discipline (3 sources)
- **Do NOT** implement saturation as a naive HSV-S multiplier (raises luma). Use **luminance-preserving saturation**: operate in a luma-chroma space, scale **chroma only, hold Y constant** (Color Slice / HDR-sat analog).
- **Automated luma-safe check:** assert mean luma is unchanged after the sat pass (the "waveform-doesn't-rise" proof), within tolerance — fail the build if it rises.

### 4.8 Look design (3 sources — film look = stacked effects)
- Model the look as a **composable, toggleable stack**, not one filter:
  - **split-tone** = curves with luma decoupled (cool shadows / warm highlights);
  - **grain** = `geq`/`noise`, weighted into shadows/mids;
  - **halation** = highlight-extract → blur → **red-weighted** → composite **`blend=addition` in linear light**;
  - **vignette** = ffmpeg `vignette` / inverted-power-window + dropped offset;
  - **density** = subtractive saturation.
- **Print-emulation LUTs need log input** (3 sources): feed the 2383-style LUT **Cineon film log** (pre-LUT transform stage), NOT display Rec.709. Run the look at configurable **opacity ~50% default**, corrections applied **beneath** it. Restore washed blacks under the LUT.

### 4.9 Scopes-as-guide, intent knobs (3 sources)
- Target defensible defaults (skin ~50 IRE, neutral whites, no clipping) but expose **creative-intent knobs** (`warm_cool`, `exposure_bias`, `contrast_amount`, `look_mix`) so "feel" can override the technically-correct result. **Don't hard-lock numeric targets — make them defaults.**

### 4.10 Engine config hygiene (mirror Kelly's project gems)
- Bake in: **tetrahedral interpolation**; **luminance-decoupled ops by default**; **output gamma 2.2** for social; **high export bitrate** (~100 Mbps masters) so grain/detail survives platform recompression; cache/output after the display conversion.

**Validation checklist the engine should self-run:** (a) input transform applied (log flattened then expanded); (b) no negative crush, no 1023 clip unless intended; (c) neutrals → equal RGB means; (d) skin angle/IRE variance across clips below threshold; (e) mean-luma-unchanged after sat; (f) LUT interp = tetrahedral; (g) film LUT fed log not Rec.709.

---

## 5. Zero-to-hero teaching outline (sellable masterclass)

**Promise:** by the end you can take *any* camera's footage to a consistent, cinematic, film-emulated grade using a repeatable node tree — and *read scopes like a pro*.

**Chapter 0 — Why color grading (the mindset)**
- Correction vs look development (Mullins' two-bucket model: "could've been done in-camera" vs "pushing past natural").
- Macro beats micro: the biggest wins are made once, globally (Kelly). Scopes guide, eyes decide.

**Chapter 1 — Setup & color management (the foundation everyone skips)**
- DaVinci YRGB vs Color Managed. Working space = **DaVinci Wide Gamut / Intermediate** and why.
- The **input transform** per camera (ARRI/Sony/RED/Fuji/BMD/phone table).
- **Project-settings gems**, set BEFORE node creation: Tetrahedral LUT interpolation, Luminance-mix-defaults-to-zero, broadcast-safe off, timeline res. *(Demo: switching Timeline to ACES changes nothing — those dropdowns only tag metadata.)*

**Chapter 2 — The CST sandwich & node tree**
- Input transform (head) + output transform (tail); grade UNDERNEATH the output transform.
- Build the **empty labeled skeleton** as a checklist: `BAL/EXP → CONTRAST → SAT`.
- One idea per node; toggling (`Ctrl+D`, `Shift+D`); saving the tree as a Still/PowerGrade; re-pointing node 01 for a new camera.
- Output gamma **2.4 vs 2.2** — deliverable-dependent; choose by where it's watched.

**Chapter 3 — Reading scopes (the literacy chapter)**
- Waveform: 0–1023 scale, black floor near 0 without crush, highlights under clip (Blakely's graticule rules).
- Parade: neutrals = overlapping white; separation = cast; THE matching scope.
- Vectorscope: the skin line (~123°), on/under/over, consistency over position.
- Histogram: log spike → spread. False color / IRE for skin (~40–50 IRE).

**Chapter 4 — Primaries part 1: balance & exposure (80% of the image)**
- Offset wheel and HDR wheels over Lift/Gamma/Gain; the gamma-Linear-push-Gain advanced variant.
- Neutralize casts on the parade; set where the image "lives."
- **Skin fixed globally here — never keyed.** Land it on the vectorscope line; check IRE.

**Chapter 5 — Primaries part 2: contrast & saturation**
- Contrast + pivot (**0.336 DWG / 0.435 Rec.709**); judge contrast at saturation = 0.
- The S-curve debate (clean linear operator vs soft-clip).
- **Luma-safe saturation**: HDR vs Color Slice "density"; leave the primary Sat slider at 50; prove it on the waveform (trace must not rise).

**Chapter 6 — Shot matching**
- Pick the hero, normalize, propagate the Still, then **trim per shot on the parade** tone-band by tone-band. Lum Mix = 0. Split-screen wipe + reference stills.

**Chapter 7 — Secondaries**
- HSL qualifiers (feather/roll-off edges), Power Windows + tracking, Color Warper, Curves.
- **Key non-skin only.** Recover sky, vignette, desaturate wardrobe.
- Bonus pro trick: qualifier as a **noise-reduction mask** (key dark/noisy areas, exclude highlights so NR doesn't smear clouds).

**Chapter 8 — Skin (its own chapter, because it's everything)**
- The skin line debate: Mostyn's vectorscope method vs Kelly/Mullins by-eye. The honest takeaway: **consistency across shots beats hitting an exact angle.**
- Skin IRE placement; the exposure heatmap (key-lit side hot is correct).
- Why you correct skin in balance, not with a key.

**Chapter 9 — Look development**
- Split-tone via curves (Lum Mix 0): cool shadows / warm highlights; density; the narrative color arc (warm/glowy ↔ cold/desaturated to externalize emotion — Frenchie).
- Run the grade UNDER the look at ~50% mix.

**Chapter 10 — Film emulation**
- The film look = **stacked effects**, not a LUT flip: print emulation + grain + halation + diffusion + vignette + density.
- **Print LUTs need log input** — the pre-CST to Cineon Film Log before a 2383 LUT; compound for keyable strength; restore washed blacks beneath it.
- Halation recipe (red-weighted highlight blur, ADD in linear); grain in shadows/mids; build-your-own DWG-native emulation that doesn't lift/crush blacks (Mullins' Terra approach).

**Chapter 11 — QC, propagation & delivery**
- Light Box: scan all thumbnails for skin/exposure consistency (all on the line, or all consistently under).
- PowerGrade reuse across the timeline.
- Delivery: gamma 2.4 vs 2.2 per platform; **export bitrate high enough that grain survives** social recompression (~100 Mbps masters at 4K); cache at the end of the tree for ProRes 422 HQ render cache.

**Capstone project:** grade a mixed-camera scene (e.g. ARRI + phone) start to finish — input transforms per clip, one approved hero look, propagate, match on the parade, skin consistent on the Light Box, film emulation at 50%, delivered at 2.2 high-bitrate.

---

*Disputes deliberately preserved as teachable nuance: skin-line-as-target (Mostyn yes / Kelly no), 2.4 vs 2.2 output, 0.435 vs 0.336 pivot, manual CST vs DRCM/ACES, S-curve on/off, and HDR-sat vs Color Slice. Each is a "depends on deliverable/taste" decision, not a settled fact — teach the principle, expose the knob.*
