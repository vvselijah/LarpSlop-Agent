# DaVinci Resolve — HLG Luna footage setup (your camera, your delivery)

**Purpose:** grade your **Insta360 Luna Ultra** clips correctly in **DaVinci Resolve Studio** and deliver
**1080×1920 SDR Rec.709** for Instagram Reels — without the washed/over-bright look you hit when grading
them as plain SDR. Built 2026-06-26 from an **adversarially-verified, primary-source** research pass
(Blackmagic Reference Manual + official Blackmagic forum; full citations at the bottom). Pairs with the
zero-to-hero grading method in the vault (`40-Projects/LarpSlop/Color-Grading-Masterclass/`) and the
colorkit engine's methodology.

> **Why your footage looked washed:** your Luna clips are **HLG (HDR)** — verified by ffprobe:
> `color_transfer = arib-std-b67` (HLG), `color_primaries = bt2020`, `color_space = bt2020nc`,
> 8K (7680×4320) 10-bit, **rotation 90°**, 29.97 fps — *even though the camera was in "Standard" mode.*
> Dropping HLG/Rec.2020 code values onto a Rec.709 SDR timeline with no conversion shows them lifted and
> milky. The fix is a proper **HLG → Rec.709 transform** before you grade.

---

## ⚠️ The two traps to avoid (read first)

1. **Do ONE HLG→SDR conversion, never two.** If you turn on Resolve Color Management (RCM) tone-mapping
   *and* also add a Color Space Transform (CST) node, the HLG→SDR compression runs **twice** → washed /
   milky (or crushed). **Pick one path** (the single-CST path below is recommended).
2. **Output Gamma 2.2 for Instagram, not 2.4.** 2.4 is the dark-room/broadcast standard; phones view SDR
   at ~2.2/sRGB in bright light, so a 2.4 master reads **crushed/dark** in the IG app. Grade and output at
   **Gamma 2.2**, then phone-test; only switch to 2.4 if 2.2 looks washed *on the phone*. Your grading
   monitor's transfer and the output tag must match.

And the one you already suspected, now **confirmed**: **do NOT use the Insta360 "Luna I-Log" .cube LUTs on
this footage.** Their header reads *"Insta360 I-Log to Rec709 Rendering LUT"* — they expect **I-Log-encoded**
input. This clip is **HLG-encoded**, a different curve. That includes the `..._to_Rec2020_HLG` variant (its
*output* is HLG but its *input* is still I-Log). The I-Log LUTs are only correct for clips actually shot in
the camera's **I-Log** profile. For HLG, use Resolve's built-in HLG→Rec.709 transform below.

---

## ✅ Recommended path — a single CST node (most control, no double-map)

This keeps the project in plain **DaVinci YRGB** (not Color Managed), so there's zero chance of RCM +
CST double tone-mapping. Best for a solo creator.

### Project setup
1. **Color Science:** Project Settings → Color Management → **DaVinci YRGB** (plain, *not* Color Managed).
2. **Timeline:** **1080×1920**, **29.97 fps** (match source — never frame-rate-convert this footage).
3. Import `VID_*.mp4`. Confirm it lands **upright** on the vertical timeline (the rotation=90 flag).
   - If it's sideways: right-click the clip → **Clip Attributes → Image Orientation**, rotate once. Use
     Clip Attributes (metadata), **not** an Inspector Transform (avoids interpolation), and **don't stack**
     a manual rotate on top of an auto-applied one.
   - **Re-check orientation after generating proxies** — proxies/optimized media sometimes ignore the flag.
4. **8K performance:** generate **Optimized Media** or **Proxies**, and enable **Force sizing to highest
   quality** + **Force debayer to highest quality** (Project Settings) so the 8K→1080 downscale is sharp.

### Node 01 — the HLG → Rec.709 transform (Color page)
Add **OpenFX → Resolve FX Color → Color Space Transform** to the **first** node:

| CST setting | Value |
|---|---|
| Input Color Space | **Rec.2020** |
| Input Gamma | **Rec.2100 HLG** *(this is Resolve's label for the ARIB-STD-B67 / HLG curve — matches your footage)* |
| Output Color Space | **Rec.709** |
| Output Gamma | **Gamma 2.2** *(for Instagram; see trap #2)* |
| Tone Mapping Method | **DaVinci** *(mandatory — HLG's range far exceeds Rec.709; without it highlights hard-clip)* |
| Gamut Mapping Method | **Saturation Compression** *(mandatory — fits Rec.2020's wide gamut into 709 without neon/clipping)* |
| Advanced → Apply Forward OOTF | **OFF** *(naming the input "Rec.2100 HLG" already applies the HLG OOTF; ticking this re-adds ~1.2 system gamma → crushes/darkens)* |
| Advanced → Apply Inverse OOTF | **OFF** |
| Advanced → Use White Point Adaptation | default ON *(no-op here — both spaces are D65)* |
| Advanced → Use Custom Max Input/Output | **unchecked** for the first pass |

**Verify on a scope:** put up a **Rec.709 Waveform/Parade**. Highlights should be rolled off (not pinned
at 100% / 1023), blacks near 0. If highlights look flat/washed, tick **Use Custom Max Input** and lower it
toward **~600–800 nits** (HLG nominal peak is ~1000), or nudge the **Adaptation** slider. There is **no
PQ-style "mastering nits" field** to set for HLG — it's a relative/system-gamma transform.

### Nodes 02+ — grade on tamed Rec.709 values (this is where OUR method lives)
Everything after Node 01 operates on clean, display-referred Rec.709 — exactly what the masterclass
methodology and the colorkit engine assume. Mirror the engine's order:

1. **Balance to neutral (Node 02).** Use the **Parade** — drive the three channels' black points together
   (kills cast), set white point so diffuse white sits ~85–90 IRE, nothing pinned at the top. This is the
   engine's per-channel black-point + Shades-of-Gray WB, done by eye on the scope.
2. **Contrast / tone (Node 03).** One gentle contrast pivoted on mid-grey (~Resolve "Pivot" around 0.34–0.44
   in 709), soft highlight roll-off. Don't stack contrast. (Engine: pivoted contrast around 0.18 linear +
   highlight soft-clip.)
3. **Skin to the I-line (by eye).** On the **Vectorscope**, nudge skin toward the **~123° skin/I-line** —
   *consistency over exactness* (Cullen: "judge by eye, reject a hard snap"; film trends slightly green of
   the line). Aim skin midtones ~40–50 IRE on the waveform. This is the manual twin of the engine's new
   **G1 skin-tone-line solver**.
4. **Creative look LUT (Node 04+).** See the looks section below.

### Optional — the "CST sandwich" (max grading latitude)
Grade in **DaVinci Wide Gamut / Intermediate** instead of 709: set Node 01's CST **output** to
**DaVinci Wide Gamut / DaVinci Intermediate** (keep Tone Mapping = DaVinci, Gamut = Saturation
Compression), grade on Nodes 02..N in DWG, then add a **final** CST node **DWG/DI → Rec.709 / Gamma 2.2**
with **Tone Mapping = None and Gamut Mapping = None** (the compression already happened on the input CST —
doing it twice double-darkens). For a quick reel, the single-node HLG→709 CST above is perfectly fine.

---

## Alternative path — full Resolve Color Management (RCM)
If you prefer RCM: Color Science = **DaVinci YRGB Color Managed**, Color Processing = **SDR (Rec.709)**,
Input Color Space = **Rec.2020 HLG**, Timeline = **Rec.2020** (or DWG — grade wide, don't clip early),
Output = **Rec.709 Gamma 2.2**, gamut/luminance tone-map **ON**, **"Limit Output Gamut To" OFF**. Then
**do NOT add any CST conversion node** (that would be the double-map). The look LUT still goes *after*, on
Rec.709 pixels. **The cardinal rule in both paths: exactly one HLG→SDR compression happens.**

---

## The colorkit looks as Resolve LUTs (10 looks)

The engine's 10 film looks are staged as Resolve-ready `.cube` files in
[`colorkit/resolve-luts/`](../colorkit/resolve-luts/): `neutral_correct, warm_interview, teal_orange,
kodak_2383_style, fuji_style, golden_hour, moody_blue, bleach_bypass, clean_pop, portra_style`.

### Install (Windows)
1. Project Settings → Color Management → **LUTs → "Open LUT Folder"** (this lands you in the exact path,
   typically `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT` — ProgramData is hidden).
2. Copy the 10 `.cube` files in (a named subfolder like `colorkit/` keeps them tidy).
3. Back in Color Management → LUTs → click **Update Lists** (no app restart). They now appear in a node's
   right-click **3D LUT** menu and the LUT browser.

### Apply them the RIGHT way (this is the order trap for looks)
- **A look LUT must sit AFTER the HLG→Rec.709 transform**, on **Rec.709-coded pixels** — these looks were
  built to grade a *developed Rec.709* image. Putting one on raw HLG/Rec.2020 (before Node 01) gives a
  broken, over-saturated/crushed result (confirmed on the BMD forum).
- Put the look on its **own node** *after* your balance/contrast nodes, then **dial it to ~70%**: open the
  **Key** palette → **Key Output → Gain = 0.70**. That's the engine's `--look-opacity 0.7` default — a
  tasteful look, not a one-tap filter. (For heavy film looks, "grade underneath" is cleaner than opacity.)
- **If grading in DWG (the sandwich):** wrap the 709 look LUT → `CST(DWG→709, tone/gamut = None)` → LUT →
  `CST(709→DWG, tone/gamut = None)`.

---

## Deliver for Instagram Reels
- **Deliver page:** MP4, **H.264** (more predictable than H.265 through Meta's re-encoder), **1080×1920**,
  **29.97 fps** (match source), **~10–15 Mbps**, AAC audio, Encoding Profile High.
- **Force sizing / debayer to highest quality** for the sharp 8K→1080 downsample.
- **Export, then watch the actual file in the IG app on a phone.** If shadows look crushed → you're on 2.4,
  switch to 2.2. If it looks washed/flat → try 2.4. 2.2 is the right *starting* default for IG.

---

## Sources (primary-first; verified 2026-06-26)
- **Blackmagic Reference Manual (mirror) — Color Space Transform parameters** (Input/Output space & gamma,
  Tone Mapping methods, Gamut Mapping/Saturation Compression, OOTF, Max nits):
  steakunderwater mirror `…/part2262.htm`.
- **Blackmagic Reference Manual (mirror) — Using Resolve Color Management** (DaVinci YRGB Color Managed,
  Automatic vs manual, Input Color Space override): `…/part1914.htm`.
- **BMD forum — Grading HLG BT2020** (grade in Rec.2020 timeline, don't hard-clip gamut, "Limit Output
  Gamut To" is not for HLG→709): forum thread `t=78098`.
- **BMD forum — Rec.709 gamma 2.2 vs 2.4** (`t=180164`, `t=159173`): 2.2/sRGB for web, 2.4 dark-room.
- **BMD forum — Using a look LUT in a DWG timeline** (look LUTs expect Rec.709 input; CST-sandwich order):
  `t=204521`. **BMD forum — LUT intensity via Key Output Gain:** `t=160091`.
- **Insta360 Luna Ultra manual — I-Log Mode** (I-Log is a distinct profile; the I-Log LUTs/CST are for
  I-Log clips, not HLG): insta360 online manual. **+ local verification** of the `Luna_I-Log_to_Rec709…`
  `.cube` header ("Insta360 I-Log to Rec709 Rendering LUT") against this footage's `arib-std-b67` tag.

*Genuine judgment calls (flagged, not fact): 2.2-vs-2.4 final pick is viewing-environment dependent —
phone-test. Exact menu labels shift slightly across Resolve 18/19/20; the principles hold.*
