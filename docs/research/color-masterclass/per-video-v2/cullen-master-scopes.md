## cullen-master-scopes — Cullen Kelly - Master Scopes Inside DaVinci

**Tool:** DaVinci Resolve 18, color-managed project "Working with Scopes". Mixed-camera timeline: Apple ProRes 422 HQ / RED / ARRIRAW per source (07:44). Scopes used: RGB Histogram (stacked), Vectorscope, RGB Parade.

### Workflow order (timeline-level, then clip-level)
1. **Step 0 — color management + look LUT at the timeline level** before any primary grade. LUT browser shows a custom CUBE pack (ACES, Arri, CKC Dev, Elements LE1/LE2/PRE/Utility, Essentials, Pro Pack, etc.); a `LOOK` node sits at timeline level above per-clip corrections (01:31, 01:55).
2. **Per-clip node tree** (the recurring serial chain seen all session):
   `EXPOSURE (01) → RATIO (03) → BAL (05)` across the top, with a **lower parallel branch (nodes 02 / 04)** feeding a **parallel-mixer** node → output (02:01).
   - Named-stage mapping: EXPOSURE = exposure normalize · RATIO = contrast/tone · BAL = white-balance/neutralize · parallel branch = isolated secondary mixed back.
   - Secondary work lives in the lower branch as a **compound / qualified node labeled "ADJ Y"** (node 04), e.g. shot 6 portrait and shot 7 cityscape (15:43, 17:02).

### Demonstrated parameters (number @ mm:ss)
- **Default neutral primary state** (the baseline he measures against): Color Boost 0.00, Shadows 0.00, Highlights 0.00, **Saturation 50.00, Hue 50.00, Lum Mix 100.00** (01:55).
- **Primaries-Color Bars header** at baseline: **Temp 0.0, Tint 0.00, Contrast 1.000, Pivot 0.435**, Mid/Detail 0.00 (03:10).
- **Wheel master values** at baseline: **Lift 0.00 / Gamma 0.00 / Gain 1.00 / Offset 25.00** (per channel) (03:10, also confirmed 03:20).
- **Project rate:** ~23.976 fps (07:48, 08:21).
- **Vectorscope skin target:** skin trace runs center → upper-right (R/Yl, ~11→1 o'clock), modest saturation well inside the targets — skin sits along the I-line / skin-tone line (~123°) (03:20, 15:43).

### Distinctive techniques / opinions
- **Scopes as objective arbiter, not decoration** — "am I actually seeing an imbalance or am I crazy"; scope math is ground truth that guards against eye-only bias (08:25). Repeat playback to build a diagnosis: "show this to me enough times and I could give you a decent diagnosis" — i.e. temporally average several frames before correcting (08:18).
- **Vectorscope signal-mass overlap = the shot-match metric.** Rule of thumb: "the more you can get their signal masses to stack up and overlap, generally the more flow" between a cut (08:52, 08:55). Verifies a match by the masses overlapping *more* than before the correction (11:07).
- **Anchor/hero-shot workflow:** set the hero first, grab a **still**, then move shot-to-shot and match each to it (09:14, 10:03).
- **Directional cast diagnosis off the vectorscope lobe angle:** one shot "skewing pinky-magenta" vs neighbor "greeny-yellow" → correct each toward neutral on the green↔magenta (tint) axis (09:05, 09:09).
- **Restraint:** match is feel, not maxing the move — "I feel like I could go a little bit less"; ease the correction (11:22).
- **Saturated set-dressing is a trap:** red flowers / red costumes throw big vectorscope excursions independent of skin — judge balance on the skin lobe, not the overall spread (07:44, 07:48).
- **Continuity anchors:** track a stable highlight (the sky cluster at the histogram's right edge) across cuts as a match reference (07:49, 07:57).
- **Global daylight balance read:** histogram channel-means aligned + vectorscope centroid near neutral (12:06).

### ENGINE: what a headless auto-grader should adopt
- **Order passes as EXPOSURE → RATIO(contrast/tone) → BAL(white-balance)**, with secondaries in an isolated parallel branch mixed back — mirror this node-stage decomposition.
- **Baseline contrast pivot ≈ 0.435 with contrast 1.0**; treat Offset (~25) as the exposure/lift trim knob and per-channel Parade comparison as the white-balance driver.
- **Skin-line steering:** measure mean chroma angle of skin pixels, steer toward the ~123° I-line; ignore/mask saturated set-dressing so it doesn't bias the balance.
- **Shot-match objective = maximize 2D vectorscope hue-mass overlap** (hue-cluster centroid alignment) between adjacent shots — not just per-channel mean match. Score cut continuity by mass-distribution distance.
- **Pick a hero frame per scene**, store its scope signature (histogram + 2D hue mass), and grade every other shot to minimize distance to it.
- **Temporal averaging:** accumulate scope reads over several frames before committing a correction (reduces single-frame noise).
- **Damping factor < 1.0** on auto-match moves — target partial convergence, not exact, to avoid over-correction.
- **Per-camera input transform** (ProRes vs RED vs ARRIRAW) before any matching.
- **Match diagnostics:** classify per-shot bias by vectorscope lobe angle on the green↔magenta axis; track a highlight anchor (sky) via histogram top-end clustering across cuts.