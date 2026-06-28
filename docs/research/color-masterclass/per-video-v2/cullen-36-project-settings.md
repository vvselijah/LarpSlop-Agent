## cullen-36-project-settings — Cullen Kelly - 36 Project Settings

A project-settings walkthrough, not a grading tutorial — Cullen builds a labeled node tree and demonstrates the DaVinci **Project Settings** flags that change how every grade behaves. The "grade" params seen are incidental test states on a red-cast plate; the real content is the global config contract.

### Node tree / workflow order (labels seen on screen)
- **Canonical primary chain (serial):** `01 Prim → 02 Bal → 03 Sat` feeding an output node, with a lower **parallel** branch (`05` + `06`) recombined via a **Parallel Mixer** [00:23, 24:21, 33:47, 38:28].
  - Order law: **Balance before Saturation**, with Sat isolated to its own dedicated stage.
- **Diagnostic test chain:** `Ramp → Contour → →709` (Rec.709 output node) — a grayscale-ramp DCTL rig used to literally draw the contrast transfer curve on the waveform [27:39, 27:44].
- Node defaults seen throughout: Lift/Gamma 0.00, **Gain 1.00**, **Offset 25.00**, **Contrast 1.000**, **Pivot 0.435**, **Saturation 50.00**, **Hue 50.00**, Lum Mix 100.00 (DaVinci default) vs 0.00 once the project flag is set [00:23, 24:21].

### Demonstrated parameters (number @ mm:ss)
| What | Value | @ |
|---|---|---|
| Contrast / Pivot (defaults) | Contrast **1.000**, Pivot **0.435** | 00:23, 24:21 |
| Contrast stretch (test) | **1.309** @ Pivot 0.435 | 32:04 |
| Saturation tool/value | DaVinci Saturation **50.00** (neutral), Hue 50.00 | throughout |
| Channel-balance gain (red-cast test) | Gain **R 1.00 / G 1.56 / B 0.65** (red up, blue down) | 25:39–38:28 |
| Lum Mix default flag | **100.00** off → **0.00** on | 24:21 → 32:04 |
| Contrast curve shape | S-curve: gentle **toe + shoulder**, not a straight 45° line | 27:44, 28:33 |

### Project Settings demonstrated (the actual subject)
- **General Options → Color flags** [00:27, 26:44, 28:36]:
  - **Luminance mixer defaults to zero** → ON. Cullen calls this *"huge"*: with it off, moving saturation/wheels also shifts luminance; ON keeps every new node's Lum Mix at 0 so chroma moves stay **luma-pure** [25:39, 38:28].
  - **Use legacy Log grading ranges and curve** → OFF.
  - **Use S-curve for contrast** → ON. Makes the Contrast control a film-style S-curve (toe lifts the black floor instead of hard-clipping to 0, preserving shadow detail) rather than a linear pivot stretch [27:36, 28:33, 28:36].
  - **Use local version for new clips in timeline** → ON.
- **Node Stack Layers** = set to **3** to expose stacked grade layers **L1 / L2 / L3** (per-clip alternate grade slots; clip selector reads `Clip - L3`) [32:04, 32:12].
- **Versions** = pre-named slots so names auto-populate: `1 = First Pass`, `2 = Second Pass`, `3 = Client Notes` (10 slots available) [34:03, 34:45].
- **Master Settings (timeline/delivery contract)** [01:49, 04:33]: Timeline **3840×2160 UHD**, **Square** pixels, **23.976 fps**; Video Monitoring 4:4:4 SDI single-link, **Data levels = Full**, **10-bit**, Bilinear scaling; Optimized/Render cache = **ProRes 422 HQ**; background caching after 5s. Processing resolution (e.g. 1920×1080) is set independently of monitor resolution.
- **Image Scaling** [11:03]: Resize filter = **Sharper**; mismatched-resolution input = **"Scale entire image to fit"**; Output "Match timeline settings", Super Scale = None.
- **Per-node input gamma tag** (right-click node → Color Space → Gamma) [26:07, 26:08]: full transfer-function list (Linear, ACEScc/cct, Apple Log, ARRI LogC3/4, Canon Log 1/2/3, V-Log, F-Log/2, Rec.709, Rec.2100 HLG/PQ…). Tagging working data to **Linear without a paired CST collapses contrast** (washes flat) — proves input/output transforms must be paired.
- **Blackmagic Cloud** [39:08]: proxy codecs incl. ProRes 422 10-bit 1080p; media-location + sync windows (24h/7d/30d) — ingest/proxy config, not a grading op.

### Distinctive opinions / techniques
- The single load-bearing flag is **Luminance mixer defaults to zero** — flagged *"huge"*; without it, hue/sat work secretly drags luma.
- **Contrast is a sigmoid anchored at the pivot**, not a linear slope — and he *proves* it with a 0→1 grayscale-ramp DCTL read straight off the waveform (toe + shoulder visible).
- Settings UI quirk: toggle any other flag off→on to re-activate a greyed-out **Save** button; **option+Save** to apply a node-default change.
- Balance target read on scopes: RGB waveform traces **overlapping/tracking together** ~0–95; skin lobe pointing to the **~123° I-line (skin axis)** on the vectorscope [25:50]. Cast diagnosis = the **R-vs-B mean separation** in the waveform (the red plate pins red high, floors blue, throws one long saturated red vector past the graticule) [25:51].

### ENGINE
- **Node order = Prim → Bal → Sat (balance BEFORE saturation), saturation in its own isolated stage**; support a parallel branch mixed back in.
- **Luma-safe by default:** treat Lum Mix = 0 as the default — saturation/channel moves must NOT auto-rebalance luminance (the engine's saturation op should be luminance-preserving).
- **Contrast op = S-curve (sigmoid) around a pivot (default 0.435), with a toe that rolls blacks off the floor instead of clamping to 0** — expose S-curve-vs-linear as a config flag; expose contrast strength (e.g. 1.309) and pivot.
- **Channel balance = multiplicative per-channel gain** (e.g. R 1.00 / G 1.56 / B 0.65); detect color cast from R-vs-B mean separation in the waveform.
- **Pair input/output transforms (CST):** a per-source input-gamma/Log-decode tag is mandatory; tagging to linear without a matching output transform collapses contrast.
- **Working-space contract to assume:** 3840×2160, square pixels, **Full data levels, 10-bit**, 23.976 fps; ProRes 422 HQ as intermediate; off-spec input → "Sharper" resize + scale-to-fit.
- Expose a small set of **global behavior constants** (lum-mix-zero, S-curve-contrast, legacy-log-ranges-off) plus a **named-version registry** (First Pass / Second Pass / Client Notes) for storing alternate grade variants.