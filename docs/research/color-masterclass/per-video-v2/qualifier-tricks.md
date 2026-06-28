## qualifier-tricks — BEST Pro Colorist Qualifier Tricks

Pro colorist grading noisy/high-contrast Sony FX6 S-Log3 landscape footage in **DaVinci Resolve Studio 20**. The whole video is one idea: **use the HSL qualifier as a luma mask to confine an effect (NR, highlight/shadow level, saturation, temp) to one tonal band — inside the SAME node — instead of letting it act globally.**

### Node tree / workflow order (labels as seen on screen)
Base serial chain (00:05): **`01` (clean/source) → `EX` (exposure) → `WB` (white balance) → `LUT` (S-Log3→Rec.709 conversion).** Conversion LUT is **last** so the camera→Rec709 transform sits on top of the primaries.
- **00:32** — added a NEW serial node **before EX** to hold Noise Reduction → chain becomes `01/NR → EX → WB → LUT`. NR runs first so the LUT doesn't amplify grain.
- **02:31 → 04:06** — built a **parallel** architecture: `EX (01)` splits into **three parallel nodes (01/02/03)** → **Parallel Mixer** → `WB (05)` → `LUT (06)`. Each luma band fixed independently and **summed**, not stacked serially.
- **05:39** — `Add Parallel` via right-click (Alt+P; menu also: Add Serial Alt+S, Serial Before Shift+S, Add Layer Alt+L, Add Outside Alt+O). Each new luma band = its own additive parallel node.
- **06:29** — final tree: `EX → secondaries (01/02/03) → WB → 05/06 → LUT (09)`.

### Demonstrated parameters (value @ mm:ss)
**Input / LUT (00:19):** Conversion LUT = `2 Nebula Cold - Slog3` (.CUBE) from a per-camera S-Log3 set under `C:/ProgramData/Blackmagic` (Nebula Neutral/Cold/Warm/Vision/XTR/Eternal/Split/5213/2393/Teal&Orange). "Conversion LUT that takes my S-Log3, turns it into Rec.709 with a little bit of a look."

**Primary — Log Wheels, dusk clip (00:23–00:31):** Contrast `1.000`, Pivot `0.435`, Lo Range `0.333`, Hi Range `0.550`; Offset `25.00/25.00/25.00` (only the Offset wheel pushed — global lift); Shadow/Mid/Highlight wheels `0.00`; Saturation `50.00`, Hue `50.00`. 4-wheel Log view (Shadow/Mid/High/Offset) also exposes Temp `0.0`, Tint `0.00`, Mid Detail `0.00`, Color Boost `0.00`.

**Primary — Log Wheels, warm sunset clip (02:09):** Contrast `1.104`, Pivot `0.435`, Lo/Hi Range `0.333/0.550`; Shadow `-0.38` (×3), Midtone `+0.32` (×3), Highlights `0.00`, Offset `16.05` (×3). (Combined "both nodes" look re-confirms these same values at 04:19.)

**Final warm-offset grade (06:29):** Offset pushed warm `R 0.47 / G 29.29 / B 53.88` readout (R high, B low → orange lift); Contrast `1.000`, Pivot `0.435`. Warm-WB baseline also seen at 05:39 as Offset `R27.47 > G24.64 > B20.98`.

**Noise Reduction (Motion Effects palette):**
- **00:43** — Spatial NR Mode `Better`, Radius `Medium`, Threshold Luma `60.0` / Chroma `60.0` (lock-linked), Blend `0.0`; Temporal Frames `0`; Motion Est `Faster`, Range `Medium`. Strong denoise but smears highlight/cloud detail (QC'd at 00:48–00:50: waveform trace thins = noise gone, but highlight texture destroyed).
- **01:48** — **UNLINK luma/chroma**: Mode `Enhanced`, Radius `Medium`, Luma `64.4`, **Chroma `100.0` (maxed)**. Opinion: *"chroma is always removable"* → push chroma hard, keep luma gentle, footage looks less smudgy. Especially for super-bright shots (01:54).

**Qualifier (HSL) — luma masks:**
- **01:15–01:39** — Luminance key for targeted NR. Hit shadows (Lum High `31.7`, H.Soft `17.8`) then widen to highlights (Lum High `91.2`), then settle Lum High `62.4`, H.Soft `3.6` so the sky keeps less NR. Sat High `5.1`, H.Soft `6.0`. **Shift+H toggles the mask overlay.**
- **02:31** — Highlight key: **Hue row OFF**, Sat effectively off (High `100.0`), **Luminance-only** band tightened from full to isolate bright sky.
- **03:42–03:59** — Shadow key: Lum Low `0.0` High `10.3` (low end isolated), then operator-tuned. On that node, lift via the **Shadows slider = +100.00** (brightens only masked darks).
- **04:42–05:33** — Skin/warm **Hue** key: Center `~33.8→32.4`, Width `42.7→14.1` (narrowed to skin), Soft `3.2→7.7`; Lum `~54–69`. Then boost saturation / push warm on that masked band only.
- **05:52–06:08** — Dark-luma key with heavy feather (Lum Low `0.0` High `27.6`, **H.Soft `40.6`**) → cool the masked shadows toward blue while Offset stays warm = **split tone**.

**Scopes:** Waveform `0–1023` (gridlines 128/256/384/512/640/768/896). Dusk clip: bulk of signal `0–256`, cloud band `~256–512`, **nothing pinned at 1023** (no clip). Masked highlight pull drops the ceiling from `~896` toward `~640–700` (03:08).

### Distinctive opinions / techniques
- **Qualifier = mask, not just a key.** Same node: apply effect → qualify a luma band → effect only acts there. Used for NR, highlight rolloff, shadow lift, sat, temp.
- **NR before exposure**, so the look LUT doesn't amplify grain.
- **Chroma noise is "always removable"** — unlink and max chroma NR (`100`) while keeping luma NR low (`~64`) to avoid smudging texture.
- **Parallel > serial for tonal bands** — shadow/mid/highlight/skin corrections summed in a Parallel Mixer, each independent and non-destructive.
- **"Roll everything off"** — always feather (H.Soft / L.Soft, Soft on hue) the qualifier; *"you don't want anything hard… otherwise you'll get clipping."*
- **Split-tone via masks:** warm highlights (warm offset) + cool shadows (cool a dark-luma masked node) = "much more punchy" orange-teal.
- Confirmed at 03:19 the whole point: a luma/sat-keyed change "didn't affect any of the other parts of the footage."

### ENGINE:
- **Implement a luma-mask primitive**: build a soft mask from a luminance band `[low, high]` with feathered rolloff (Gaussian/`H.Soft`+`L.Soft` analog), then apply any op only inside it. This is the core reusable trick.
- **Op order**: `denoise → exposure-normalize → (parallel luma-masked corrections) → white-balance → creative LUT`. Denoise FIRST.
- **Split luma vs chroma denoise**: aggressive chroma (`~100`), gentle luma (`~64`); chroma denoise is "free."
- **Parallel-sum, don't serial-stack** band corrections (shadow lift, highlight rolloff, skin sat) so they don't compound.
- **Standard log-wheel primitives** to map: Contrast `1.0–1.10`, Pivot `0.435`, Lo/Hi Range `0.333/0.550`, Offset = global RGB lift (warm offset R>G>B for sunset).
- **Masked moves to support**: highlight rolloff (negative highlight gain inside high-luma mask ~`0.61–1.0`), shadow lift (positive inside low-luma mask ~`0–0.10`), skin warm/sat (hue center ~`32°`, width ~`14`), cool-shadow split-tone.
- **Scope checks**: waveform `0–1023` occupancy — flag mass `<128` (crushed) and any pixels at `1023` (clipped); after-denoise trace-thinning in highlights = over-smoothing flag.
- **Always feather masks** before applying gain to avoid banding/clipping.