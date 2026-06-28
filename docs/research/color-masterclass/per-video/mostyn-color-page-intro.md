# mostyn-color-page-intro — analysis

*Source: Darren Mostyn, 545K views (HIGH) · framesRead: 24*

## Overview
This is an absolute-beginner orientation to the Resolve 18 Color page, NOT a deep technique lesson. Mostyn explicitly says up front he is "not going to color management, anything deep" and is just demystifying the page so newcomers "are not scared of it." The teaching value is in the LAYOUT and the WORKING MODEL, not in numeric grade recipes. The demo footage is a graded interview ("FINISHED_WTTP_New_Interview_RADIO_EDIT", 11 shots, Apple ProRes 422 Proxy) of a woman in a cafe with a red/floral headscarf — a deliberately easy skin-tone + memory-color subject. Core message, repeated: the pages all talk to each other (an edit-page trim updates live in color); the node graph is just a left-to-right signal chain you build look in switchable layers; primaries (whole-image) come first, secondaries (isolated color/luma/area) come second; and a grabbed Still in the Gallery is a portable container of the whole node tree you drag onto other clips. He never opens Project Settings, never shows RCM/ACES/CST, never reads a vectorscope, and never does a skin-tone-line pass — so several schema fields are 'not demonstrated' and I mark them as such rather than inventing them. His one concrete beginner prescription, stated twice: start in Primaries > Color Wheels, drive brightness and color with OFFSET first, then add a little saturation and maybe contrast.

## Order of operations
1. 1. Understand the page is live-linked: an edit-page trim/adjustment auto-updates in the Color page (shown by trimming a clip).
2. 2. Pick the timeline/sequence to grade (Timeline dropdown or Edit page > Sequences); the 11-shot 'FINISHED' edit is loaded.
3. 3. Select a shot via the clip thumbnails strip at the bottom of the node area.
4. 4. Node 01 (primary, whole-image): set overall BRIGHTNESS and COLOR using the wheels — Mostyn's prescribed beginner move is to use OFFSET first (master ring for color cast, master wheel/Y for brightness).
5. 5. Refine tonal range on the same or a new node with Lift (shadows), Gamma/Gain demo (highlights), pulling Lift down to deepen blacks toward 0.
6. 6. Add a NEW SERIAL node (right-click > Add Node > Add Serial, or Option/Alt+S) for SATURATION so it can be toggled independently of the level work.
7. 7. Add further serial nodes as 'thinking space' — one idea per node so each can be switched on/off; reset a node (right-click > Reset Node) if you dislike an idea without losing earlier nodes.
8. 8. Move to SECONDARIES on a later node: Curves (Custom, Hue vs Sat, etc.), qualifier/keyer, Power Windows (shapes), tracker, Color Warper.
9. 9. Optionally add an OpenFX/ResolveFX effect (e.g. Blur) by dragging from the Effects/Library onto a node.
10. 10. GRAB A STILL (right-click viewer > Grab Still) — it stores the entire node tree in the Gallery.
11. 11. APPLY the look to other same/similar shots by dragging the still onto them, or middle-mouse-click the still onto a selected clip.
12. 12. Toggle grades for before/after: Cmd/Ctrl+D disables a single node; Shift+D disables the whole clip grade; the grade persists back on the Edit page because the pages are linked.

## Node tree
"Serial node chain, built left-to-right, ending at 4 nodes (f034/f037). Structure taught explicitly via the connecting wires (f034 narration): the GREEN dot on the far left = the original ungraded image (source); it feeds Node 01; Node 01's output feeds Node 02; Node 02 feeds Node 03; Node 03 feeds Node 04; Node 04's output goes to the far-right node = the DISPLAY / final render output. He stresses moving nodes around does NOT change order — order is defined by the wires, not screen position. Add-node methods shown: right-click > Add Node > Add Serial (submenu also lists Add Serial Before, Add Parallel, Add Layer, Add Outside — f021), or Option/Alt+S. Per-node roles in his demo: Node 01 = primary offset/lift level + cast correction; Node 02 = saturation (deliberately separated so it can be toggled without losing level work — his stated MAIN reason for using nodes); Node 03/04 = empty 'idea' nodes / placeholder for a window or FX. Toggles: click a node's NUMBER to disable just that node; Cmd/Ctrl+D disable single node; Shift+D disable whole-clip grade. Housekeeping: right-click > Clean Up Node Graph to auto-arrange; middle-mouse-drag to reposition a node."

## Scopes
- **Waveform (RGB parade-style, the default he uses)** — Opened from the Scopes panel (top-right 'Scopes > Waveform'). He reads it as vertical brightness: bottom of the graph is black at 0, top is white at 1023 (10-bit). He explicitly narrates 'zero is black, 1023 is white' and watches the WHOLE trace move up/down together when he drags Offset (proving Offset is a whole-image lift), versus Gain pulling the TOP (highlights) more than the bottom, and Lift pushing the BOTTOM (shadow/black level) down. · targets: No numeric target values given (beginner scope-reading only). Implicit targets: blacks sit near 0 and whites near the top without clipping; he uses it to confirm which control affects which tonal region, not to hit a spec.
- **Histogram (per-channel RGB)** — Visible in the wide overview shots of his hardware monitor (the broadcast scope wall with three color wheels + waveform + histograms + vectorscope). Not driven numerically in the tutorial — present as part of the 'scopes exist to measure objectively' message. · targets: Not demonstrated numerically.
- **Vectorscope** — Visible only on his background broadcast monitor wall (cutaway frames f001/f013/f039/f048); never brought into the on-screen Resolve UI and never used to set color. No skin-tone-line read. · targets: Not demonstrated — no I/Q skin line, no hue angle target given.

## Primaries
"He teaches the four-wheel primaries bank (Primaries > Color Wheels) as the beginner's home base and shows the SAME controls in two interchangeable forms: the circular Color Wheels and the 'Primaries - Color Bars' slider view (f029) — pressing the panel icon swaps between them, doing 'exactly the same thing.' The four wheels are LIFT (shadows), GAMMA (mids), GAIN (highlights), OFFSET (whole image). Mechanic taught: the small color ring in the center of each wheel shifts hue/cast (push toward red = warmer, toward blue/cyan = cooler); the slider/Y under each wheel is brightness for that tonal zone. KEY PRESCRIPTION (stated twice): beginners should drive the grade with OFFSET first — color ring for the overall cast, master slider for overall brightness — because it moves the whole image cleanly. Demonstrated correction on the cafe shot: it 'looked a bit warm,' so he pulled OFFSET away from warm into the cool/blue side and pulled Shadows/Lift down slightly, instantly 'smartening up' the image. Seen-on-screen values: default wheels read Lift/Gamma/Gain 0.00 (×4 each) and Offset 25.00/25.00/25.00; during the cool correction Offset moved to roughly 20.36/25.38/28.48 and 23.82/24.61/25.60 (red lowered, blue raised = cooler) with Lift nudged to -0.02/-0.03; a Gain demo nudged Gain to 1.11 (×4) and 1.08 (×4); the Color Bars view showed Offset bars at 16.40/16.40/16.40. Top-bar primaries also shown: Temp 0.0, Tint 0.00, Contrast 1.000, Pivot 0.435, Mid/Detail 0.00, Color Boost 0.00, Shadows 0.00, Highlights 0.00, Sat 50.00 (default) raised to 70.00, Hue 50.00, Lum Mix 100.00. He name-checks Temperature and Tint (green/magenta) and Contrast/Pivot as 'tools to play with' but does not teach pivot theory."

## Secondaries
"Secondaries are framed as 'isolating either colors, or luminance/brightness values, or an area' to focus the grade. Three secondary tools are demonstrated, all on a later node: (1) CURVES — he opens the Curves panel which defaults to Custom (the diagonal luma curve over a histogram, f004/f013) and explicitly switches to HUE vs SAT (f039), then clicks the woman's RED headscarf with the picker and pulls down saturation only in the reds — honestly noting it 'also affects her face and her lips' because red skin shares the hue (a real lesson in qualifier spill). The Hue-vs-Sat panel shows Input Hue and Saturation readouts at the bottom (e.g. Input Hue 256.00 / Sat 1.00). (2) POWER WINDOWS — he opens the Window palette and draws a CIRCLE/oval over the subject's face (f041), with Transform Size 50.00, Pan/Tilt 50.00, and Softness 1.38, so 'everything I do only affects inside or outside that window'; he notes a Tracker exists to follow it. (3) He name-checks the keyer/qualifier and the Color Warper (says he has a dedicated episode on it) but does not operate them. No HSL qualifier pull or skin isolation is actually completed."

## Skin tone
"Not demonstrated. There is no vectorscope skin-tone-line pass, no targeting of the ~11 o'clock I-line, and no hue-angle number given. The closest skin-relevant moment is the inverse lesson: when he desaturates reds via Hue-vs-Sat, the subject's face and lips desaturate too because facial skin and the red headscarf occupy overlapping hues — i.e. he teaches that red-channel secondaries spill into skin, but he never sets or protects a skin target. Mark skinTone as out-of-scope for this beginner video."

## Color management
"Not demonstrated and explicitly excluded. In the first minute he says 'we're not going to color management, anything deep — this is just an absolute beginner's guide.' He never opens Project Settings, never shows RCM (DaVinci YRGB Color Managed), never shows ACES, and never adds a CST (Color Space Transform) node — though a 'Color Space' submenu is visible in the node right-click menu (f021) and 'ACES Transform' / 'Color Space Transform' appear in the ResolveFX Color list (f042), they are pointed at as things that exist, not used. The project is plain DaVinci YRGB with proxy media (Apple ProRes 422 Proxy). Working space / input-output transforms: not shown. Treat color management as NOT covered by this source."

## Look design
"No LUT, film-emulation, or split-tone look is built — this video is corrective/structural, not stylistic. Look 'design' here = the node-stacking philosophy and the Gallery Still as a reusable look container. He builds a 4-node serial chain (Node1 level/offset correction, Node2 saturation, Node3/4 'thinking-space'/empty or a windowed/FX node), grabs a Still (right-click viewer > Grab Still) which appears in the Gallery under 'Stills 1' / 'PowerGrade 1' (f048), and shows that right-clicking the still > 'Display Node Graph' proves it holds all four nodes. He then DRAGS that still onto other identical/similar shots (or middle-mouse-clicks it) to instantly replicate the whole grade — his framing: 'the still is basically a record of the grade.' He also demonstrates a non-look creative FX: dragging a Blur (ResolveFX Blur > Gaussian, Horizontal/Vertical Strength ~0.40, Border Type Reflect) onto a node from the Effects Library, then resetting it. Effects he flags as 'fun to play with' early on: the ResolveFX/OpenFX list (f042/f044)."

## Numeric settings seen on screen
- Primaries default — Lift 0.00/0.00/0.00/0.00, Gamma 0.00 ×4, Gain 1.00 ×4, Offset 25.00/25.00/25.00 (f004, f010)
- Top primaries bar defaults — Temp 0.0, Tint 0.00, Contrast 1.000, Pivot 0.435, Mid/Detail 0.00 (f004)
- Bottom primaries bar — Color Boost 0.00, Shadows 0.00, Highlights 0.00, Hue 50.00, Lum Mix 100.00 (f004/f010)
- Saturation 50.00 default, raised to 70.00 on the saturation node (f010)
- Gain demo nudge — Gain 1.11/1.11/1.11/1.11 with Lift 0.01 ×3 (f019)
- Gain demo nudge — Gain 1.08/1.08/1.08/1.08 (f023/f027)
- Cool correction — Offset 20.36/25.38/28.48 (red down, blue up = cooler) (f013/f015)
- Cool correction — Offset 23.82/24.61/25.60 with Lift -0.02 (f016/f030)
- Cool correction — Lift -0.02/-0.02/-0.02 then -0.03/-0.03/-0.03 (f031/f032)
- Final shot wheels — Gain 25.37/24.23/25.03 region on Color Bars / Offset back near 25 (f050)
- Color Bars (slider) view — Offset bars 16.40/16.40/16.40, Gain 1.00 ×4 (f029)
- Waveform scale markers — 0 (black) to 1023 (white), gridlines at 128/256/384/512/640/768/896 (f017/f019)
- Hue vs Sat panel readout — Input Hue 256.00, Saturation 1.00 (f039)
- Power Window (circle) — Transform Size 50.00, Pan 50.00, Tilt 50.00, Softness 1.38 (f041)
- ResolveFX Gaussian Blur — Horizontal/Vertical Strength 0.400, Border Type Reflect (f044)
- Viewer zoom 72%, Resolve version 18 (status bar, multiple frames)

## Teaching points
- The pages are ONE project, live-linked: a trim or grade made on the Edit page instantly appears in the Color page and vice-versa — there is no 'export to color', it is the same media. Beginners panic that color is a separate app; it is not.
- The node graph is just a signal flowing left-to-right: a green source dot enters node 01, each node passes its result to the next, and the last node feeds the display/render. Node order is set by the WIRES, not by where boxes sit on screen.
- Primaries = whole image; Secondaries = isolated (a color via curves/qualifier, a luma range, or an area via a window). Do primaries first, then secondaries.
- Offset is the beginner's best friend: its color ring sets overall cast (toward red=warm, toward blue=cool) and its master controls overall brightness, moving the whole image cleanly. Mostyn's literal starter recipe: Offset for color + brightness, then a touch of saturation, then maybe contrast.
- Lift = shadows, Gamma = mids, Gain = highlights, Offset = everything. Watch the WAVEFORM to learn which is which: Gain pulls the top (highlights), Lift pushes the bottom (blacks toward 0), Offset slides the whole graph.
- Read the waveform as brightness: 0 is black at the bottom, 1023 is white at the top (10-bit). You don't need numbers yet — just confirm which control moves which part of the trace, and keep blacks near 0 and whites near the top without crushing/clipping.
- Put each idea on its OWN serial node (Alt/Option+S or right-click > Add Serial) so you can toggle it independently — e.g. saturation on a separate node lets you preview the look with and without color without destroying your level work. This is the single biggest reason to use nodes.
- Nodes are cheap thinking-space: if you're unsure, add a node, try the idea, and if you dislike it right-click > Reset Node — you keep every earlier node. Toggle a node by clicking its number; Cmd/Ctrl+D toggles one node, Shift+D toggles the whole clip grade for instant before/after.
- The wheels and the 'Color Bars' sliders are the SAME controls drawn two ways — switching views doesn't change your grade. Don't be thrown when the panel looks different.
- Secondaries spill: pulling saturation out of 'red' also hits red skin and lips because they share the hue. Isolation is never perfectly clean — which is exactly why qualifiers, windows, and trackers exist.
- A grabbed Still in the Gallery is a CONTAINER for the entire node tree, not just a picture. Right-click > Display Node Graph to verify, then drag it (or middle-mouse-click it) onto matching shots to copy the whole grade in one move — the fastest way to grade a multi-shot scene consistently.
- This video deliberately skips color management, vectorscope skin-line work, LUTs, and ACES/CST — so don't treat it as a complete grading method. It is the map of the room; the actual disciplined workflow (color management, shot-matching on scopes, skin line) is a separate, deeper study.

## Quotable claims
- "We're not going to color management, anything deep — this is just an absolute beginner's guide to what is going on in the color page." (00:00:45)
- "These pages all talk to each other — so the edit that's sitting here, if I make an edit adjustment to it... that has updated automatically for me in the color page." (00:01:06)
- "With offsets we're adjusting the whole image." (00:03:53)
- "Zero is black, 1023 is white." (00:04:39)
- "This node now contains offset information, lift, gain and the saturation information — that's a lot of information in just one node, so for me I like to separate it out into separate things." (00:06:13)
- "I suggest you work with your offset first — so this shot is looking a little bit warm, so if I use my offset and literally pull that down away from the warm colors and into these cooler colors, very quickly we've smartened that image up." (00:07:47)
- "This green dot here represents the original image without a grade; it goes into the first node... and this here is my display, this is my output, my final render." (00:08:50)
- "Secondary basically means that you can isolate either colors, or luminance values, brightness values, and start really focusing the grade into a more specialized area." (00:09:52)
- "If I click on her red headscarf I can pull down the saturation just in the red — you can see it's also affecting her face and her lips." (00:10:23)
- "This still contains all the color grading information from these four nodes... it's basically a record of the grade." (00:12:12)
- "If you're new to the color page I suggest just start in the primary color wheels tab and work with offset — use this for your brightness, this for your overall color, and maybe play with a bit of saturation and a bit of contrast." (00:13:00)

## Key frames
- `f004.jpg` — The clean Color-page anatomy on the first shot: main viewer (woman, headscarf), empty Gallery saying 'No stills created', a single node 01 in the graph, and the full Primaries Color Wheels (Lift/Gamma/Gain/Offset at defaults 0/0/1.00/25.00) with the Custom curve panel — the baseline layout he orients the beginner around.
- `f017.jpg` — The Waveform scope open (Scopes > Waveform) reading 0=black to 1023=white, used to prove Offset moves the whole trace while Gain lifts highlights and Lift drops the black level — his core 'how to read brightness on a scope' lesson.
- `f021.jpg` — The right-click node context menu open on node 01 with Add Node > submenu (Add Serial / Add Serial Before / Add Parallel / Add Layer / Add Outside) — exactly how to build the serial chain; also shows Color Space / Gamma / LUT submenus that exist but are left untouched.
- `f029.jpg` — The 'Primaries - Color Bars' slider representation (RGB bars under Lift/Gamma/Gain/Offset, Offset bars at 16.40) — proving the wheels and bars are the same controls in two forms, a frequent beginner confusion.
- `f032.jpg` — The cool correction landed: Offset pulled toward blue and Lift at -0.03, the warm cafe shot now neutralized — his demonstrated 'use Offset first to fix a warm image' move with the matching wheel values visible.
- `f039.jpg` — Curves switched to Hue vs Sat with the hue spectrum strip; he picks the red headscarf and pulls red saturation down — the secondaries lesson, including the honest caveat that it spills onto skin/lips (Input Hue 256 / Sat readout visible).
- `f041.jpg` — A circular Power Window drawn over the subject's face with the Window/Transform/Softness palette (Size 50, Softness 1.38) — demonstrating area-isolated (inside/outside) secondary grading and mentioning the tracker.
- `f048.jpg` — End state: the grabbed Still in the Gallery ('Stills 1' + 'PowerGrade 1' thumbnail) and the completed 4-node tree arranged as source>01>02>03>04>display, with the still being dragged/applied to other clips — the 'a still is a portable record of the whole grade' payoff.
