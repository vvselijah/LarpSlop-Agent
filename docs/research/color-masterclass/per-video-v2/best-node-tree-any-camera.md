## best-node-tree-any-camera — BEST Node Tree for ANY Camera (BBC pro)

A fixed, reusable "broadcast notary" node tree the author runs on every BBC / Amazon / ITV job. Built once, saved as a PowerGrade/still, applied to any camera — and the *only* node that changes per camera is the input CST. Everything is graded inside a CST sandwich (camera→working space at the head, working→Rec.709 at the tail). DaVinci Resolve Studio 18.5.

### Project color management (set ONCE, before building) — 01:05–02:07
- Color science: **DaVinci YRGB → switched to DaVinci WRGB (Wide Gamut)** (01:26 → 01:51).
- Timeline color space: **Rec.709 (Scene) default → changed to DaVinci WG/Intermediate** (01:51).
- Output color space: **Rec.709 (Scene) → changed to Rec.709 Gamma 2.4** ("that's what my monitor is calibrated to / what my delivery is", 01:51).
- Deliberately **NOT** using automatic color management — uses manual CST nodes instead so camera profiles are switchable (01:05).
- Dolby Vision 4.0, mastering display 4000-nit P3 D65 ST2084; all LUTs = No LUT; 3D LUT interp = Trilinear; broadcast-safe IRE −20–120. Press **Save** to lock (02:07).

### The node tree (left → right, on-screen labels + numbers) — full reveal 12:42 / 16:05
```
01 CAM>DWG → 03 BAL/EXP → 04 CONTRAST → 05 SAT
   → [parallel mixer #1: 06 TEMP / 08 HDR / 09 WARPER / 10 CURVES]
   → 11 TRIM
   → [parallel mixer #2: 12 PW1 / 14 PW2 / 15 PW3]   (power-window secondaries)
   → 16 Texture → 17 SPARE
   → 02 DWG>709 → 18 KODAK (film-look LUT) → 19 (output/timeline node)
```
- Serial spine first (balance→contrast→sat), then two parallel banks each recombined via a **layer/parallel mixer** (07:07–09:29).
- Build order: node 01 from scratch (02:21), drop CST on it (02:51), build output CST node 02 next (04:12), then add serial nodes via **Option/Alt+S** (06:19, 06:30).
- Empty nodes are intentional scaffold — "you don't have to use the node just because it's there" (08:55); trailing PW nodes left empty for per-clip local work (16:29).

### Input CST — node 01 "CAM>DWG" (the ONLY per-camera change)
- Maps camera gamut/log → **DaVinci Wide Gamut / DaVinci Intermediate** working space. Resolve FX Color → **Color Space Transform** (02:51).
- Fixed CST settings: **Tone Mapping = DaVinci, Adaptation = 9.00, Gamut Mapping = None, Use White Point Adaptation = ON, Forward/Inverse OOTF = OFF** (05:12–05:56). Large-space→large-space ⇒ Resolve auto-sets the correct OOTF/white-point boxes (05:12).
- Per-camera input values demonstrated:
  - **Canon: Canon Cinema Gamut / Canon Log 3** (05:26, 05:56) — (read as Log 2 in earlier frames 05:01/05:12/19:53).
  - **Sony: S-Gamut3.Cine / S-Log3** (19:26).
  - **ARRI: ARRI Wide Gamut 3 / ARRI LogC3** (21:06).
  - **iPhone / consumer & non-log Canon: Rec.709 / Rec.709** — treat as already display-referred, skip the log path (16:36, 17:36, 21:18, 21:53).
  - "Blank" option = set input to **Use Timeline** to inherit project CM (19:56).

### Output CST — node 02 "DWG>709" — 04:39, 10:45
- Input DaVinci Wide Gamut / DaVinci Intermediate → **Output Rec.709 / Gamma 2.4**; Tone Mapping = DaVinci, Adaptation 9.00, Gamut Mapping None; **Apply Forward OOTF = ON**, White Point Adaptation ON.
- Grade lives **between** the two CSTs so you always work in display-referred Rec.709 space, not log (04:39, 07:07).
- Applying the output CST visibly **stretches the parade to fill 0–1023** (restores contrast from flat log) (04:13).

### Film look — node 18 "KODAK" (compound) — 09:57–12:42
- Classic **Kodak 2383 print-emulation LUT** (LUTs → Film Looks → **Rec709 Kodak 2383 D65**) (09:57, 12:42).
- KEY trick: a plain DWG>709 (Gamma 2.4) output is **wrong** to feed a film LUT. Add a **second CST** set **Input Rec.709 / Gamma 2.4 → Output Rec.709 / Cineon Film Log** (Apply Inverse OOTF ON) so the LUT receives the log encoding it was authored for — "now that Kodak emulation looks a lot more usable" (10:45–11:36).
- Package the feeder-CST + LUT as one **compound node** named "KODAK" (right-click → Show Compound Node; interior = 01 CST → 02 LUT). Swap LUT inside to change film stock (12:11–12:20).
- **LUT strength = Key Output Gain**: 0 = off, 1.0 = full strength (12:00, 12:05).
- Alt look layer seen later: **Dehancer Pro 7.0.1** film emulation as the named look (20:35, 20:59).

### Neutral starting baseline (Resolve defaults the grader perturbs from)
Lift 0.00 / Gamma 0.00 / **Gain 1.00 / Offset 25.00**; **Contrast 1.000, Pivot 0.435**; **Sat 50.00, Hue 50.00, Lum Mix 100.00**; Temp 0.0, Tint 0.00 (00:25, 04:39, 13:32).

### Demonstrated grade moves & tools
- **TRIM (11)** = global "trim the overall look" corrector after the look, before secondaries; e.g. **lift shadows slightly with the Lift wheel** (15:47–15:52).
- **SAT (05)** value seen at **45** (down from 50 default) on a graded read (14:54).
- **Secondaries** = per-hue + windowed: **Hue-vs-Sat / Hue-vs-Hue custom curves** (Input Hue 256.00, Sat 1.00) for per-hue targeting (15:53–15:58).
- **Power windows (PW1–3)**: elliptical/feathered masks for spatial isolation. Demonstrated: circle shape, **Soft 1 = 2.07 → 7.83, Size 5.92, Angle 42.21, Pan ~52.6, Tilt 48.4, Opacity 100** over a subject; A/B toggle on/off to confirm improvement (16:07–16:20).

### Scope targets he hits (Parade + Vectorscope)
- Flat log before CST = compressed/low parade (~200–700 of 0–1023), tight central vectorscope blob (06:04, 19:53).
- After CST/grade target = **balanced RGB parade spanning ~0/128 up to ~768–896, no channel clipped at 1023**, green typically peaks highest; **vectorscope skin lobe sitting on the skin/I-line**, tight, not over-saturated (13:04–13:32).
- Daylight sanity: blue sky drives the blue parade trace high + a long cyan/blue vectorscope arm — confirm no clip after the look (21:53).
- Discipline: get balance/contrast/sat neutral and **pass the scope check BEFORE branching** into any creative secondary (14:44).

### Distinctive opinions
- One fixed node order, every job — "the secret to my grading being very consistent." Manual CSTs over auto color management *specifically* so any camera profile is a one-node swap.
- Always grade *under* the output CST (and under any film look) so every move is judged in final display space.
- Reuse mechanism: save the whole tree as a Gallery still/PowerGrade ("FIXED NODE TREE"), then **right-click → Apply Grade** (or drag-drop) onto a new clip; it looks wrong until you fix node 01 — that's the expected workflow (16:46–16:57, 19:05, 19:44).

### ENGINE
- **Adopt the fixed stage order verbatim:** input-CST → balance/exposure → contrast → saturation → [temp / HDR / warp / curves parallel layer] → trim → [power-window secondaries] → texture → output-CST → film-LUT. Map each to a discrete op.
- **CST sandwich = the transform contract:** decode camera log/gamut → DaVinci Wide Gamut/Intermediate working space, grade there, then transform to Rec.709 Gamma 2.4 for delivery.
- **Per-clip, change only the input transform:** keep a camera→(gamut,gamma) lookup — Canon Cinema Gamut/CLog3, Sony S-Gamut3.Cine/S-Log3, ARRI AWG3/LogC3, BMD Film Gen, iPhone/consumer = Rec.709/Rec.709 (no log decode). Everything downstream is camera-agnostic.
- **CST defaults:** Tone Mapping DaVinci, Adaptation 9.0, Gamut Mapping None, White Point Adaptation ON; OOTF flags auto by large-vs-display classification.
- **Film LUT needs a log re-encode first:** before a Cineon-authored print LUT (Kodak 2383 D65), apply Rec.709/G2.4 → Cineon Film Log, then the .cube; expose LUT-name + strength (mix 0→1) as parameters.
- **Neutral identity baseline:** Gain 1.0, Offset 25, Contrast 1.000, Pivot 0.435, Sat 50, Lum Mix 100 — perturb deltas from here.
- **Scope gate before look:** full-range luma (shadows off 0, no clip at 1023), channels balanced/neutral, skin lobe on the skin-line — verify before applying the creative look.