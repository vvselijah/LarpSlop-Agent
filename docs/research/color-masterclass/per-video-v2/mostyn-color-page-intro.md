## mostyn-color-page-intro — Darren Mostyn - NEW to DaVinci? Color Grading

Beginner orientation to the Resolve Color page. Project: **DaVinci Resolve 18**, clip `FINISHED_WTTP_New_Interview_RADIO_EDIT`, **Apple ProRes 422 Proxy** media, Waveform scope on a **0–1023** scale throughout.

### Demonstrated workflow / node tree
Mostyn's core teaching is **one op per serial node**, built left→right:
- **Source → node 01 → 02 → 03 → 04 → display/output** — a serial chain; the connecting lines define processing order (08:47). The **green dot** at far left = the camera-original source feeding node 01 (08:48); the far-right output = the final render (09:05).
- Adds nodes via right-click > Add Node, one at a time, as the look builds (05:25, 07:00).
- By the end the tree restructures to **01→02→03 serial + node 04 on a lower branch** (a parallel/secondary node), carried into the saved still (11:45, 12:42).
- Build order he demonstrates per node: **balance (Lift/Gamma/Gain) → contrast (curve) → saturation → branched secondary** (12:42).

### Distinctive opinions / technique
- **Never cram multiple ops into one node.** He deliberately stacks level + saturation on one node (06:22, Sat 70.20), then shows the pain: to undo just the sat he must hand-reset the Saturation value while preserving the level move (06:31) — the argument for layering.
- **Layering = "very managed":** finish a node, reset what you don't want, then add a fresh node for the next move (07:00).
- Primary **Lift/Gamma/Gain wheels = "your main area"** for beginners to play in; everything else is more advanced (07:47).

### Concrete demonstrated parameters (value @ mm:ss)
**Neutral / identity baseline** (his repeated default state):
- Lift 0.00, Gamma 0.00, Gain 1.00, **Offset 25.00** R/G/B, **Contrast 1.000, Pivot 0.435**, **Sat 50.00**, Hue 50.00, **Lum Mix 100.00**, Temp 0.0, Tint 0.00 (05:34, 12:17). Soft Clip Low/High 0/100 (09:08). Pivot 0.435 = Resolve's default contrast pivot; Sat 50 and Offset 25 are unity in Resolve's 0–100 readout.

**Saturation (single combined node demo):**
- Sat raised to **70.20** from 50 baseline (06:22); **71.40** (06:31); reset back to **70.20** while gain held (07:00).

**Level move coupled with the sat push:**
- Lift **+0.01**, Gain **×1.08** (~+8%) (06:31); Gain **0.99** (slightly under unity) on node 02 (07:00).

**Color-balanced grade node (cool highlights):**
- Lift **−0.03** R/G/B (shadows down), per-channel Gain **R 20.36 / G 25.38 / B 28.48** (blue highest → cool highlights, R<G<B) (08:36, also as Offset 20.36/25.38/28.48 at 09:08).

**WB / exposure push:**
- Temp **−190.0** (cooler), Tint **+6.00**, Contrast **1.006**, all three Gain channels raised equally to **25.00** (scalar highlight/exposure lift) (09:38).

**Curves:**
- Master custom luma curve — control point placed in the **shadow foot (lower-left)** over the RGB histogram to start reshaping tone (10:12).
- **Hue vs Hue** curve: Input Hue **256.00**, Hue Rotate **0.00** (flat, no rotation) — rotate one hue band without a qualifier (10:17).

**Secondaries (toured, not dialed for a final look):**
- **Color Warper** (Hue–Saturation hex mesh): one mesh node dragged off-center to warp a region's hue/sat (10:43).
- **Power Window** (Circle/oval over the face): Size 50, Pan 50, Tilt 50, Aspect 50, Rotate 0, Opacity 100, **Softness Soft 1 = 1.38** (10:50). Window shapes available: Linear / Circle / Polygon / Curve / Gradient, plus Tracker (11:04).

**Scope targets hit:**
- Interview clip Waveform sits **~200–800** of 0–1023 (09:08), spreads **~200–900** after the Gain/Temp push (09:38), **~256–896** post-grade (11:52).
- A different, low-key clip (clip 03, `A004_11171101_C009.mov`) reads heavy shadows **~64–256** — he notes per-shot scope distribution differs and should be read before grading (12:52).

### Save / delivery
- **Grab a still to the Gallery** (right-click viewer) to record the grade — Gallery goes from "No stills created" to **Stills 1**, thumbnail `1.1.1` (11:45 → 11:53). The still = the serialized 4-node grade, re-applicable to similar shots.
- Back on the **Edit page**, graded shots read back on the timeline thumbnails — grade is **non-destructive metadata**, not baked (12:53).

### ENGINE:
- Model the grade as an **ordered serial op list, one purpose per stage**: balance → contrast → saturation → branched secondary; render reads the last stage.
- **Identity defaults to hardcode:** Lift 0 / Gamma 0 / Gain 1.0 / Offset 25 / Sat 50 / Lum Mix 100 / Contrast 1.000 / **Pivot 0.435** — anything else is an applied move.
- **Balance op = Lift/Gamma/Gain**, tunable per-channel; cool-highlight look = **per-channel gain R<G<B** with **lift pulled down (~−0.03)** for a contrast floor. Equal-channel gain bump = scalar exposure/highlight lift; Temp/Tint = WB matrix (e.g. Temp −190 cooler).
- **Keep saturation a separate, independently-toggled knob** (e.g. 50→70 = global boost) so it can be reset without touching the balance pass.
- **Tone curve = monotonic luma spline** with shadow-foot control points; expose **Hue-vs-Hue** as a piecewise hue-remap and **power windows** as elliptical alpha masks (cx,cy,size,aspect,rotate + feather) for local ops.
- **Read the Waveform distribution per shot before grading** — low-key vs bright clips need different lift/gain targets (0–1023 / IRE scale).
- Persist each shot's grade as a **serialized snapshot (still / CDL-style sidecar)** attached as non-destructive metadata for batch re-application.