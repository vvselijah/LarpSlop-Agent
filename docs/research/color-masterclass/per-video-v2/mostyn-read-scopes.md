## mostyn-read-scopes — How Pro Colorists Read Scopes ft Darren Mostyn

**Authority:** Darren Mostyn — 20-year broadcast colorist. Grading in DaVinci Resolve from an Advanced/Mini panel, but reading on a third-party **Nobe OmniScope** suite on a dedicated 32" ultra-wide scope monitor (separate from the image). FSI (Flanders Scientific) reference monitor. This is a **scope-reading masterclass**, not a node-tree build — almost all moves are read/diagnose, then small corrective trims.

### Suite / read environment (setup)
- Scopes live on a **separate, smaller, dimmed** monitor so bright traces don't pollute dark-adapted image evaluation; enlarged here only for teaching (00:58, 01:02). Dim via scope **Settings → gain** (display-only, doesn't touch signal) — values shown: trace gain field `4.384`, peak-level color R:255/G:64/B:64, channel spacing `10`, top/bottom margin `20.000`, left margin `0.158` (08:21, 08:25).
- Saved as a reusable **preset / layout** — the read surface is a deliberate persisted config (00:51).
- **Cross-validation principle:** "the trace from DaVinci Resolve is true" — OmniScope gives the identical reading with more customization. Software-computed scopes = ground truth (00:24).
- **10-bit code-value scale throughout:** parade Y-axis labeled `0,128,256,384,512,640,768,896,1023`; hue histogram X-axis in degrees `0,36,72,108,144,180,216,252,288,324,360` (00:29, 01:05, 09:33).
- Scope vocabulary (context menu, 08:19): Source Signal, Waveform, Vectorscope, Sat/Luma, Channel Plot, **Twin Peaks**, RGB Plot, Histogram, **False Color**, **Skin Tone**, Gamut, 3D Color Cube, Min/Max, Timecode.

### Grading tools seen (nodes/wheels)
- DaVinci color page on the right monitor: **primary color wheels Lift / Gamma / Gain / Offset**, plus the **Log** page (panel labels: `MASTER OFFSET`, `RED/GREEN/BLUE OFFSET`, `MASTER SHADOW`, `RED/GREEN/BLUE SHADOW`) used for range-gated shadow work (05:44, 08:33).
- No node-tree labels exposed; corrections are single-node primary trims driven by the scope read.

### Demonstrated workflow ORDER (his stated method)
1. **Expose first, color second.** Use **False Color** to get exposure in the right ballpark, *then* the **skin-tone vectorscope** for hue (02:57, 03:36). "I've got the exposure sitting where it should be. Now I can [make creative moves]."
2. **Scopes are a guide, not a target.** "I'm using them as a guide only… it's a creative decision at this point" (03:34). "Using the two to start with, but I'm **not grading by scopes**" — scopes seed the balance, the eye finishes (03:42).

### Concrete demonstrated parameters (number @ mm:ss)
**Skin exposure (False Color / waveform), IRE:**
- Skin floor **~35 IRE**, top **~55–60 IRE** (02:21).
- Brightest forehead/specular ceiling **~70 IRE — do not exceed**; a highlight band appears on the forehead at 70 (02:40, 04:13).
- Bulk of face should sit in the **green (mid) band**; only specular pokes above (02:43, 02:45). Target band is the one rendered **gray on this particular false-color chart** (02:27) — band→color mapping is **user-customizable**, not fixed (02:45, 02:53).
- Subject skin majority **~50 IRE, a touch under** (03:49).
- Top Gun (Cruise): brightest cheek "**into 60, doesn't go up to 70**"; bulk **~40–50 IRE on the line, down to ~30** on the shadow side (04:13, 04:14).
- Connelly still: false color reads skin **mid-50s IRE** (both agree "lower") despite a visually bright frame — trust measured skin ROI over perceived brightness; bright background fools the eye (04:22, 04:27, 04:31).
- **Two-band skin model:** midtone bulk **40–50 IRE**; **highlights 55–65 IRE** (a distinct band) (04:35, 04:38).
- Working clamp restated: skin "**between 40, not getting anywhere past 65**" (~40–65 IRE) (05:21).
- **Highlight discipline:** always "sit a little bit less" than the ceiling; "Her" reference highlights **don't even hit 55 IRE** — cap below clip, not at 100/1023 (04:40, 04:45).

**Skin hue (vectorscope skin-tone / I-line):**
- Skin-tone line ≈ **123° I-line** (upper-left lobe). Push the skin centroid toward it (00:42, 01:35).
- **Distinctive opinion:** skin does **NOT** have to sit *on* the line — under/on/over are all fine "**as long as it's consistent**" across the project (05:37, 05:39, 05:42).
- Film references trend **slightly GREEN of the I-line** (CCW/under it) and still read natural — demonstrated on Top Gun: Maverick (04:04) and "Her" (04:46, 04:55). "Slightly greener" ≠ looks green; it means skin sits balanced under the line (04:55).
- **Debunks the "50% gray skin" myth** — don't force skin into the mid/gray region (04:33).

**Shadow / black-point work (Log page, custom shadow scope):**
- Custom **"black-guide" scope** = a waveform/parade **windowed to the bottom 10/15/20% IRE** so only blacks are analyzed — his most-used favorite tool, absent from stock Resolve (00:35, 07:50, 08:12, 09:33).
- Read per-channel floor in the shadow band; on "her top" clip the **green channel sits slightly higher** in the bottom 15% = green shadow cast (08:58).
- **Correction:** go to **Log tool → bring green shadows down** until the three channel baselines converge (R=G=B at the floor) = neutral black (09:05, 09:07, 09:11).
- Also demoed: **pull red down in lift/shadows** for "slightly cooler shadows," watching the scope live for clipping (09:26).
- **Per-channel clip catch:** parade flags the **green channel clipping** first as one channel is pushed (08:42).

**White balance / temp:**
- Warm the shot via primary offset/temp to rotate skin off green toward yellow/amber — "working temp + tint, the two together" (03:22, 03:26).

### Distinctive scopes / opinions
- **Split shadow / midtone / highlight vectorscopes** — judge color casts tonal-zone by tonal-zone, not on one combined plot (00:32).
- **False Color as a permanent on-screen tone indicator** ("it's there all the time") with an IRE legend strip 10→90 (00:46, 02:09).
- **Solo / isolate-an-area / isolate-just-skin** — right-click a scope to mask the read down to only skin pixels before judging hue (assignable to Stream Deck) (01:29, 01:33, 01:35).
- **Twin Peaks scope** (third-party, hourglass/double-diamond CIE-style): folds **brightness (vertical) + hue + saturation** into one display; specialist, not run full-time (05:52, 05:56, 06:00, 09:52).
- **3D Vectorscope** axis convention: **vertical = luminance, radial = saturation, angular = hue**; black at center, peak white at top vertex (06:22, 06:33, 06:38). Zero saturation collapses the cloud to a single vertical line on the neutral axis (06:26). Global warm/cast = whole cloud shifts off the neutral axis toward a corner; "tipping it back onto the axis = white balance" (06:15, 06:51). Hue is **hard to read in 3D** (rotation-ambiguous) — prefer the 2D vectorscope for hue (07:13).
- **Tool-to-task:** "saturation work → vectorscope" (radial extent vs 75%/100% targets); "I need them all" (09:48, 10:13).

### ENGINE: what a headless auto-grader should adopt
- **Compute the standard triplet per frame** on a 10-bit (0–1023) scale: RGB **parade** (per-channel balance/clip), luma **waveform** (range/clip), **vectorscope** (hue/sat) — plus a luma **histogram** and a hue-degree (0–360) histogram. Trust software scopes as ground truth.
- **Order = expose then color:** Pass 1 drive **face-mask luma** into the IRE target window, Pass 2 steer skin hue. Treat scope targets as **soft constraints** (initialize, then stop) — not an objective to optimize to.
- **Two-band skin-luma model:** midtone bulk **40–50 IRE**, highlights **55–65 IRE**, hard ceiling **~70 IRE** (flag above as over-exposed); never force skin to 50% gray.
- **Skin hue:** measure the masked-skin cluster angle vs the **~123° I-line**; allow an offset band (on-line *or* slightly green/CCW for a filmic look) rather than snapping; enforce **one consistent offset across a shot batch** (match pass).
- **Measure the skin ROI, not the whole frame** — a bright background must not raise the face-exposure estimate.
- **Windowed black-guide:** restrict histogram/parade to the **bottom 10–20% IRE**; compute per-channel shadow means and drive **min(R)=min(G)=min(B)** to a common floor (neutralize via range-gated Log/lift offset); flag any single channel piling at the 1023 ceiling.
- **False color = luma→IRE-band LUT** (configurable band colors) for a per-pixel exposure-zone check before grading.
- **White-balance via cloud geometry:** mean chroma offset (Lab a*,b* / 3D-scope lean) names the cast; correction = translate the neutral/highlight cluster back to the achromatic axis. Use `atan2(b*,a*)` for hue (angular), radius for saturation, vertical for luma.
- **Saturation health = radial spread**: keep within gamut/75–100% targets, flag over-saturation when chroma radius exceeds threshold.
- Separate **display gain from signal gain** — trace-brightness/scope-dimming knobs are visualization-only and must not alter measured values.