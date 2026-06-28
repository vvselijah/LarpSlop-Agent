# mostyn-perfect-node-tree — analysis

*Source: Darren Mostyn, 13K views (HIGH authority) · framesRead: 18*

## Overview
Mostyn's thesis: a colorist grading 300-500 (sometimes ~1000) shots a day needs SPEED, CONSISTENCY, and PROTECTED IMAGE QUALITY, and a single FIXED, reusable node tree delivers all three. The whole philosophy is "send everything UP to a big working color space (DaVinci Wide Gamut/Intermediate), do all the work there, and bring it back DOWN to the delivery space (Rec.709 2.4)" — bookended by two Color Space Transform (CST) nodes. The grade is built so the three foundation nodes (exposure/balance, contrast, saturation) are nailed FIRST, then every subsequent tool is fed from that clean point via PARALLEL nodes, so secondaries never dirty each other or the foundation. He builds it live, then strips all settings and saves it as a reusable still/template node graph that drops onto any clip with one middle-mouse click; only the input CST changes per camera. The same tree handles ARRI, Canon, Sony, Blackmagic, even plain Rec.709 and unknown sources. Key discipline: only move forward if the image looks better; check scopes constantly (he manually QCs, never trusts auto Broadcast Safe); don't crush blacks; clipped highlights are acceptable. He also shows a Film Look Creator (Rochester/Kodak emulation) placed at the END so you "grade under" the look, a per-node HSV-saturation trick, a glow texture node, and where noise reduction goes (very early, before/just after the first CST).

## Order of operations
1. 1. Set project color management FIRST: Color science = DaVinci YRGB (NOT a managed mode); Timeline color space = DaVinci Wide Gamut/Intermediate; Output = Rec.709 Gamma 2.4 (2.2 for web). Monitor gamma MUST match output.
2. 2. Node 01 — Input CST: camera color space/gamma (e.g. Canon Cinema Gamut / Canon Log 3) -> DaVinci Wide Gamut / DaVinci Intermediate. This is the ONLY node that changes per camera.
3. 3. LAST node — Output CST: DaVinci Wide Gamut/Intermediate -> Rec.709 / Gamma 2.4. Built early and kept ON so you grade WYSIWYG on a Rec.709 display (displays can't show DWG).
4. 4. Now grade UNDER the output CST. Foundation, in strict order: exposure/balance (offset, check vectorscope) -> contrast (contrast/pivot, lift up shadows, don't crush) -> saturation. Get these three '99% right' before anything else.
5. 5. Branch into a PARALLEL bank off saturation so each secondary gets its own clean feed from the foundation: highlights, shadows, density (Color Slice), warper (Color Warper hue/sat on sky), curves (Hue-vs-Hue/Hue-vs-Sat).
6. 6. Add a 'trim' node after the parallels for any global after-the-fact tweak that must NOT alter the feed going to the secondaries.
7. 7. Second PARALLEL bank = power windows, pre-built and labelled: PW left, PW right, PW top, PW bottom (all with softness, shapes pre-drawn).
8. 8. Texture/look nodes near the END: Film Look Creator (Clean Slate + a stock like 'Rochester', mix pulled back), optional Glow/Halation/Film Grain/Sharpen.
9. 9. Place the Film Look Creator BEFORE finalizing foundation values, because it changes them — revisit exposure/contrast/balance with the film look ON.
10. 10. Strip all per-shot settings, reset wheels, leave CSTs + labelled empty nodes, save as a still/template node graph (save it sitting on the exposure node so it reopens there). Apply to a clip, set camera CST, grade. Copy/ripple across the scene, then refine shot-by-shot.
11. 11. Workflow ordering for whole job: grade a hero shot -> copy to whole scene (group level) -> balance each shot -> then do secondaries -> copy secondaries across similar shots -> shot-by-shot polish. Optionally use Groups (pre-clip CST per camera) instead of per-camera trees.

## Node tree
A two-CST 'sandwich' with two parallel banks. SERIAL SPINE (left to right): [01 >DWG: input CST cam->DaVinci WG/Int] -> [02 exp/bal] -> [03 con (contrast)] -> [04 sat (saturation)] -> then SPLIT into PARALLEL BANK 1, all fed from sat: {highlights, shadows, density (Color Slice), warper (Color Warper), curves} -> recombine into [trim] -> SPLIT into PARALLEL BANK 2 (power windows): {PW left, PW right, PW top, PW bottom} -> recombine -> [FLC: Film Look Creator] -> [>709: output CST DaVinci WG/Int->Rec.709/2.4]. On the real broadcast job the tail also carries a Dehancer/film node, a Halation+Bloom node, and an 'HSV' node (RGB->HSV color space at node level with channels 1 and 3 disabled, for subtractive saturation). Foundation = first 3 grade nodes; everything downstream is parallel-fed so secondaries never compound onto each other. Empty labelled nodes are harmless when bypassed ('not dirtying the feed').

## Scopes
- **Vectorscope** — Watch the trace spread/center for neutrality; check skin lands toward the I (skin-tone) line; judge saturation by how far the trace reaches the targets. · targets: Used while setting exposure/balance and saturation. Neutralize casts to center; on the warm music-video grade the trace pushes into the orange/skin quadrant. He says music videos can deliberately sit 'everything in the warm quadrants'.
- **Waveform** — Reads the trace top-to-bottom for black point (don't crush), mids, and highlight clipping; uses it to verify the film look's effect on highlights/shadows (highlights 'go creamier', shadows 'go bluer'). · targets: Primary tool for exposure/contrast. Scale shown ~0-1023 (10-bit). He lifts shadows OFF the floor (no crushing — references Daria's filmic talk), is comfortable letting highlights clip ('I don't mind clipping highlights... looks better without it sometimes'), but keeps an eye on legal levels.
- **RGB Parade / Histogram** — Manual eyeballing against legal limits; he is the QC, no automated safe. · targets: Used implicitly for balance, but he leans on vectorscope+waveform. Manual QC throughout — explicitly says do NOT use Resolve's Broadcast Safe (IRE -20..120) clamp, it 'clips everything... absolute garbage'.

## Primaries
Foundation done on standard Color Wheels (Lift/Gamma/Gain/Offset) in DaVinci Wide Gamut timeline space. On-screen Primaries panel during the build showed Contrast 1.000, Pivot 0.435, Saturation 50.00 (default), Hue 50.00, Lum Mix 100.0 as the reset baseline; Offset wheel numerically ~25.00/25.00/25.00 default, nudged to e.g. 24.20/25.04/25.83 and 24.24/25.32/26.49 for warm balance moves; Saturation raised to ~57.80 on one shot. Exposure done primarily with OFFSET (his preferred 'really useful' balance tool) plus the HDR palette (Dark/Shadow/Light/Global wheels) which is color-space-aware and works in the DWG timeline space. Contrast via the Contrast/Pivot control and via Lift (lifted up to avoid crushing). Rule he repeats: nail exposure -> contrast -> saturation in that order and get them 'bang on' before branching.

## Secondaries
Each secondary lives in its OWN parallel node fed from the clean foundation, so they're independent. Tools shown: (1) Color Slice (new v19) for DENSITY — six-vector wheel (Red/Yellow/Green/Cyan/Blue/Magenta + Skin), he pushes Density up specifically on the Skin vector; panel showed Density/Dem.Depth 0.00, Saturation 1.00, Sat.Balance/Sat.Depth/Hue fields. (2) Color Warper (Hue-Saturation grid) on the SKY — samples the sky, nudges hue/saturation (panel Hue ~0.35, Sat ~0.23-0.37, Luma 0.50, Auto Lock on), careful 'not to break it too much'. (3) Curves for Hue-vs-Hue / Hue-vs-Sat. (4) Power Windows as a second parallel bank — left/right/top/bottom pre-built WITH softness always on (he 'can't remember working a window without softness'), top window drawn with the pencil/wonky shape; used to relight/shape faces and darken sky/backgrounds. (5) HSV node trick: change a node's color space RGB->HSV, disable channel 1 (H) and channel 3 (V) so saturation edits become subtractive — pre-baked into a preset so it's one drag. (6) Log wheels to cool shadows.

## Skin tone
Skin is protected and enriched, not hand-painted onto a line. His main skin move is DENSITY via the Color Slice 'Skin' vector (push density up on skin specifically), plus watching skin on the vectorscope so it stays toward the skin-tone (I) line while he adjusts exposure/saturation. He repeatedly 'checks the skin tones stay good' while balancing exposure and adding saturation, and warns against over-saturating ('probably a little bit hot here, let's bring that down'). For interview/hero subjects (documentary key subjects appearing ~30x) he spends far more time and uses many more power windows on the face than on b-roll. No explicit RGB skin-line numbers were stated; the discipline is scope-checking + Color Slice skin density + restraint.

## Color management
DaVinci YRGB (non-managed) + manual CST workflow — his deliberate choice over RCM/ACES. Project: Color science DaVinci YRGB; Timeline color space DaVinci Wide Gamut / DaVinci Intermediate (the big working space — 'send everything up to a larger color space and bring it back down'); Output Rec.709 Gamma 2.4 for broadcast (2.2 for web), and the grading monitor MUST match that gamma. Node 01 input CST maps source->DWG/Intermediate; final node CST maps DWG->Rec.709 2.4 and OVERRIDES the project output setting. Key clarifications he gave in Q&A: the project Timeline color space sets default behavior of color-space-aware tools (HDR palette, Film Look Creator, many ResolveFX); the project Output color space, when using CSTs, does nothing visually BUT controls the export's color-space TAG (so apps know 2.4 vs 2.2, i.e. TV vs web). Even unknown/Rec.709 footage is still sent up to DWG and back to stay disciplined and protect quality. Prefers DWG over ACES purely from 14 years of muscle memory and tool behavior; doesn't need ACES for BBC docs (not Netflix). Works in Groups (pre-clip CST per camera) on real jobs, or alternatively one fixed tree per camera.

## Look design
Look is applied at the END so you 'grade under it': Film Look Creator (Resolve Studio, v19) on its own node — click 'Clean Slate' to strip the heavy default preset, choose a stock emulation (he favors 'Rochester' = Kodak/Rochester HQ reference), then pull the Mix/blend back because it's strong. The look shifts highlights creamier and shadows bluer, so he re-checks the foundation with it on. On real broadcast work the look engine is Dehancer (replaced here by FLC), plus a separate Halation + Bloom node and optional Film Grain. Other texture: a preset Glow node (Composite mode Screen/Overlay, Saturation 1.000, Gain 0.500, Opacity 0.500, threshold pulled back, global blend back) and a Sharpen node, both saved as single-node stills. Look philosophy by genre: factual-crime docs go dark/cold ('how dark do we want to go', body-cam/TikTok footage 'breaks really quick — barely touch it'); art docs stay faithful to the artwork; music videos are 'much more fun' — opposing color contrast or fully warm. He tests the big look on several scene shots before committing.

## Numeric settings seen on screen
- Project color science: DaVinci YRGB (non-color-managed)
- Timeline color space: DaVinci Wide Gamut / DaVinci Intermediate
- Output color space: Rec.709 Gamma 2.4 (broadcast); Gamma 2.2 for web — monitor must match
- Input CST examples: Canon Cinema Gamut + Canon Log 3; Canon Log 2; Sony S-Gamut3.Cine + S-Log3; Blackmagic Design Film Gen 5; ARRI LogC3 -> all to DaVinci WG/Intermediate
- Output CST: DaVinci WG/Intermediate -> Rec.709 / Gamma 2.4; Tone Mapping = DaVinci; White Point Adaptation ON
- Primaries reset baseline: Contrast 1.000, Pivot 0.435, Saturation 50.00, Hue 50.00, Lum Mix 100.0
- Offset wheel default ~25.00/25.00/25.00; warm nudges e.g. 24.20/25.04/25.83 and 24.24/25.32/26.49
- Saturation raised to ~57.80 on one shot; HDR-palette saturation used sparingly
- Color Slice: push Density up on the Skin vector (Saturation 1.00 default)
- Color Warper on sky: Hue ~0.35, Sat ~0.23-0.37, Luma 0.50, Auto Lock ON
- Film Look Creator: Clean Slate, stock 'Rochester' (Kodak), Mix pulled back
- Glow preset: Composite Screen/Overlay, Saturation 1.000, Gain 0.500, Opacity 0.500, threshold + global blend pulled back
- HSV node: node color space RGB->HSV, disable channel 1 (H) and channel 3 (V)
- Broadcast Safe IRE -20..120 = DO NOT USE
- Waveform scale 0-1023 (10-bit); workload 300-500 (up to ~1000) shots/day

## Teaching points
- A FIXED node tree buys speed, consistency, discipline and protected quality — build it once, reuse forever across every project.
- Sandwich the grade between two CSTs: go UP to DaVinci Wide Gamut/Intermediate, do ALL work there, come back DOWN to Rec.709 2.4. The output CST stays ON so you grade WYSIWYG (displays can't show DWG).
- Only the INPUT CST changes per camera — same tree grades Canon, Sony, Blackmagic, ARRI, even Rec.709 or unknown footage.
- Nail the first three nodes (exposure/balance -> contrast -> saturation), IN THAT ORDER, to ~99% before doing anything else.
- Use PARALLEL nodes for secondaries so each pulls a clean feed from the foundation — serial stacking makes every node compound onto the last and 'dirties the feed'.
- Add a 'trim' node after the foundation for later global tweaks that must not change the feed going to your secondaries.
- Golden rule: only move forward if the image looks BETTER than before — otherwise undo.
- Pre-build power windows WITH softness always on, labelled left/right/top/bottom, so you never draw from scratch on 400 shots.
- Put the film look (Film Look Creator 'Clean Slate' + a stock, blend pulled back) near the END and 'grade under' it — then revisit exposure/contrast because the look shifts highlights/shadows.
- Save the stripped tree as a still/template node graph (sitting on the exposure node so it reopens there); also keep single-node FX presets (CSTs, NR, HSV, Glow, Sharpen, windows) to drag on individually.
- Don't crush blacks; clipped highlights are usually fine. Manually QC on scopes — NEVER use Resolve's Broadcast Safe clamp ('garbage').
- Project Output color space, under a CST workflow, only sets the export TAG (2.4 TV vs 2.2 web); the visible transform is the CST. Timeline color space sets default behavior of color-space-aware tools (HDR palette, FLC, ResolveFX).
- If you don't know the camera source: try a generic wide log (ARRI LogC3, then Sony/Blackmagic); if nothing fits, use Rec.709 SOURCE (no display gamma) and just start grading.
- Noise reduction goes EARLY — before, or just after, the first CST (NR after the grade flattens the image); keep one pre-built NR node and use it sparingly.
- Per-node HSV color space with channels 1 and 3 disabled gives a subtractive saturation look — bake it into a preset to avoid fiddling on 400 shots.
- On real jobs, group by camera+scene so the input CST is set once per group, or keep one fixed tree per camera; spend the time budget on hero/interview subjects.

## Quotable claims
- "As a documentary colorist I have to grade something like three, four, even 500 shots a day — this needs speed, and the fixed node tree gives me that." (00:06:01)
- "The theory behind my fixed node tree is we send everything up to a larger color space, work in that color space, and bring it back down again." (00:09:44)
- "These first three nodes — exposure/balance, contrast and saturation — should be absolutely bang on before we move forward; all the secondaries get their own separate clean feed from this point." (00:22:28)
- "One rule I've got is I always check that the image looks better when I've done something — as I move forward it should always look a bit better, otherwise don't move forward." (00:13:49)
- "Do not use that Broadcast Safe — it's absolute garbage, it's just going to clip everything. I'm manually QC-ing on my scopes the whole time." (00:52:47)
- "I don't mind clipping highlights — I think it looks better without it sometimes — but certainly not crushing my blacks." (00:53:02)
- "The output color space being set in the project, under a CST workflow, doesn't change the image — it determines the tag of the clip on export, i.e. 2.4 for TV versus 2.2 for web." (00:51:31)
- "Noise reduction — normally I'd put this before even my CST, early in the pipeline; certainly not after, it's going to really flatten your image." (00:46:50)
- "The nodes are there already ready for me to switch on if I need them; invariably I get what I want with the first three nodes — the others aren't doing any harm, they're not dirtying the feed." (00:45:30)
- "I prefer to grade in DaVinci Wide Gamut because I like this CST workflow; I'm not doing Netflix shows, the BBC documentaries don't need an ACES workflow." (00:43:25)

## Key frames
- `f008` — The complete 'perfect node tree' revealed up front: serial spine cst->exp/bal->contrast->sat, then the highlights/shadows/density/warper/curves parallel bank into 'trim', then PW left/right/top/bottom power-window bank, ending at output. Color Slice panel + Waveform scope (0-1023) visible. The whole talk's blueprint in one image.
- `f019` — Both parallel banks clearly laid out — bank 1 (highlights, shadows, density, warper, curves) recombining, then bank 2 of power windows — proving every secondary gets its own clean feed. Window/softness panel open below.
- `f012` — Color Space Transform node panel fully expanded: Input DaVinci Wide Gamut / DaVinci Intermediate, Output Rec.709 / Gamma 2.4, Tone Mapping = DaVinci, Gamut Mapping, 'Use White Point Adaptation' checked — the exact output-CST settings.
- `f009` — Project Settings > Color Management: DaVinci YRGB color science, Timeline = DaVinci WG/Intermediate, Output = Rec.709 Gamma 2.4, and the Broadcast Safe IRE -20..120 control at the bottom that he tells you NOT to use.
- `f029` — Camera-agnostic proof — a Blackmagic 'MOTEL' desert shot on the SAME tree with the input CST switched to Blackmagic Design Film Gen 5 -> DaVinci Wide Gamut; only node 01 changed.
- `f031` — Rec.709 source (London street) on the same tree with input CST = Rec.709 -> DaVinci Wide Gamut, demonstrating 'even Rec.709 goes up to DWG and back down' for discipline and clean transforms.
- `f046` — HDR color-wheel palette (Dark/Shadow/Light/Global) AND the CST gamma dropdown open (Canon Log 2/3, Cineon Film Log, DaVinci Intermediate, DCI, DJI D-Log, Fujifilm F-Log, Gamma 2.2, Gamma 2.4) — the 'if you don't know the source, pick a generic wide log' and 2.2-vs-2.4 teaching.
- `f035` — Real ITV broadcast job: same node structure plus the gallery of single-node FX presets in the left bin — 'ARRI LOG C3 to DWG', 'SLOG3 GAMUT3 CINE to DWG', 'DWG to REC 709 2.4', 'NR 01' (noise reduction), 'HSV' — the reusable building blocks he drags onto nodes.
