# OVERNIGHT RUNBOOK — "Introducing ClipWith" video edit-prep

> **This runs AFTER Elijah clears context.** It is self-contained. Read this top-to-bottom, then the inputs below, then execute Phases 1→5 without stopping until done or genuinely blocked. Maintain `clipwith-edit/PROGRESS.md` the whole time.

## Objective
Turn Elijah + Tanner's raw footage of the "Tanner and I" ClipWith launch video into a **fully edit-ready package**: trimmed clips of the correct lines in chronological order + matching motion graphics + sound effects + placement timings, then color grade — so Elijah only has to assemble/refine the final timeline in DaVinci. Quality target = match the reference reel (got hundreds of thousands of likes + investor attention). **This is a strong FIRST PASS, not a published final.**

## Inputs (read ALL of these first)
1. **Footage:** `clipwith-edit/source/` — Elijah's 30–40 raw take files. **May contain duplicates; the better takes are obvious.**
2. **Script + chronological order:** `obsidian/Elijah's vault/20-Content/Scripts/Tanner and I.md` — the $200B "Introducing ClipWith" script PLUS the shot-by-shot **Shooting script** table (= the chronological map: which line → which shot # → what's on screen).
3. **Style / motion-graphics reference:** `abc wrap/reference-reels/DNPHHpTAme2.mp4` + the already-written teardown `abc wrap/reference-reels/clipwith-launch-parody-brief.md` (catalogs the "Introducing" card, logo flash, word captions, jump-cuts).
4. **Color knowledge:** `auto-clip/colorkit/` engine + vault `40-Projects/LarpSlop/Color-Grading-Masterclass/` + auto-memory `reference-insta360-luna-ultra` (I-Log → Rec709 BT1886 LUT for IG).
5. **Tools:** `video-analyzer` MCP, `ffmpeg` (PowerShell), the `auto-clip` engine, Remotion/HyperFrames (in `abc wrap`), `caption-engine` skill, `colorkit`, ElevenLabs MCP (`text_to_sound_effects`).

## ⚠️ CRITICAL heuristics — apply to EVERY clip
- **The keeper take is almost always the VERY LAST one in each file** (after several attempts). **WATCH/ANALYZE EACH FILE ALL THE WAY TO THE END.** The keeper is signaled by Tanner + Elijah **nodding at each other / saying "yeah that's the one" / "that's good"**, or it's the obvious clean full take. Sometimes it's the only take (one try). Never pick an early take just because it appears first.
- **Match each clip to a line/shot** in the shooting script (transcribe → find which scripted line it is → assign shot # + chronological position).
- **NEVER overwrite or re-encode the originals.** All trims are NEW files. Keep originals untouched as masters.

## Phase 1 — Footage triage + clip-down  *(THE PRIORITY — this is the big time-save)*
Fan out: one agent per source file (workflow, `pipeline`/`parallel`). Each agent:
1. **Transcribe + analyze** the file (`video-analyzer` `analyze_video`, detailed). List every take inside it with timestamps.
2. **Find the KEEPER** = the last clean full take. Confirm via the end-signal (nod / "that's the one" / clean delivery). Capture its in/out timecodes.
3. **Match to script** → assign shot # + chronological order index (from `Tanner and I.md` shooting table).
4. **Trim** the keeper to just the needed line **with ~1s handles each side** (editing room). **Re-encode to DNxHR HQ .mov** (frame-accurate + scrubbable — his machine struggles with raw 8K HEVC). ffmpeg: `ffmpeg -ss <in> -to <out> -i <src> -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p -c:a pcm_s16le <out.mov>` (verify exact flags; fall back to `-c copy` rough-cut if DNxHR encode is too slow at 8K).
5. **Name:** `NN_shotNN_<linekeyword>.mov` where NN = chronological order → `clipwith-edit/clips/`.
6. **Log** to `clipwith-edit/assembly-map.md`: order #, source file, in/out TC, the line, shot #, notes (e.g., "2 good takes, used the later one").
- **Flag for Elijah** (don't silently guess on hero shots): duplicates, ambiguous keepers, any file where the end-signal wasn't clear.

## Phase 2 — Motion graphics  *(analysis DONE — build from the spec)*
> ✅ **The frame-by-frame analysis + our-version design + placement timing is already done → `clipwith-edit/graphics/SPEC.md`** (G1–G10 mapped to script beats, with the reference's real device kit: news-headline proof screenshots, product/app screenshots, pain-point overlays, launch card, word captions). **Just BUILD the 10 graphics from that spec** — only re-analyze the reference if something in the spec is unclear.
2. **Design OUR version of each, themed to the ClipWith script + his brand** (cinematic dark/orange, bold sans — match the *vibe*, make it ours, NOT a white Apple card): the **"Introducing ClipWith"** card; a **ClipWith logo flash**; **word-pop captions** (`caption-engine` "Punchy Bold Animated"); emphasis hits on **"$200 billion"** and **"the editing industry"**; the **"this video was edited by ClipWith"** reveal graphic; the **CTA end card** (clipwith.ai / "1,000+ on the waitlist"). **Each graphic must match WHAT'S being said at that moment** and stay consistent with the others.
3. **Build** as Remotion/HyperFrames comps (abc wrap stack) OR transparent overlay assets (PNG/ProRes-4444 with alpha) for DaVinci Fusion. Output → `clipwith-edit/graphics/` + a `graphics/SPEC.md` (what each is, where it goes, in/out timing vs the assembly map).

## Phase 3 — Sound effects + audio
1. From the reference catalog, list the SFX moments (whooshes on cuts, impacts on title cards, a riser into the "edited by ClipWith" reveal, pops on captions).
2. Generate OUR versions via ElevenLabs `text_to_sound_effects` → `clipwith-edit/sfx/` (named to their placement). **⚠️ COSTS CREDITS — see Authorizations.**
3. **Dialogue audio:** if Elijah dropped the **Røde Wireless PRO 32-bit float WAVs**, sync those to the trimmed clips (cleaner than camera scratch). **Music is NOT baked in** — Elijah adds it in the IG Edits app (abc wrap rule: voice-only export).

## Phase 4 — Assembly map + timing sheet
- Finalize `clipwith-edit/assembly-map.md` = the master **edit decision list**: clip order → each clip's line + shot # → the motion graphic overlaid + its in/out timing → the SFX + its timing. This is the sheet Elijah follows in DaVinci.
- **STRETCH:** generate a Resolve-importable **EDL or FCPXML** that lays the trimmed clips on a timeline in order (saves manual dragging). Frame-accurate; note in PROGRESS if attempted/succeeded.

## Phase 5 (LAST) — Color grade
- Run `colorkit` on the trimmed `clips/`: linear-light develop (WB/exposure/contrast) → **shot-match** for inter-shot continuity → a tasteful **look @0.7** that fits the cinematic dark/orange brand (try `clean_pop` or `golden_hour`/`moody_blue` per the footage) → `--height 1920` for IG. Output → `clipwith-edit/graded/`. **LAST step**, so the grade is only on the final selected clips. Correct I-Log/Standard handling (Rec709 BT1886 for SDR/IG).

## Output structure
```
clipwith-edit/
  source/    (Elijah's raw takes — INPUT)
  clips/     (trimmed keeper lines, chronological, DNxHR)
  graphics/  (our motion graphics + SPEC.md)
  sfx/       (our sound effects)
  graded/    (color-graded final clips)
  assembly-map.md   (master edit decision list + all timings)
  PROGRESS.md       (running log: done / flagged-for-Elijah / blockers)
```

## Execution model — DON'T STOP until done
- Run via `agentic-build-loop` + Workflows. Order: **Phase 1 first** (highest value), then 2 + 3 in parallel, then 4, then 5.
- Phase 1 = a Workflow with **one agent per source file** (fan-out); every agent is told **WATCH TO THE END for the keeper take**.
- Keep `PROGRESS.md` updated. If blocked on one thing (missing footage, a paid-gen authorization), **log it and keep going on everything else**. Only stop when all phases are complete or everything remaining is blocked on Elijah.

## ⚠️ AUTHORIZATIONS — Elijah decide BEFORE clearing
- **Paid generation (ElevenLabs SFX, any Higgsfield graphics):** the run will generate SFX + graphic assets as a first pass. **Are you OK with that credit spend?**
  - **YES** → it generates everything.
  - **NO / "specs only"** → it prepares prompts + specs + placement, generates nothing paid, and you fire them later. *(Default if you don't say: SPECS-ONLY for paid gen, but DO all free work — trims, captions via caption-engine, color grade, assembly map.)*
- **OneDrive sync:** the hub syncs to OneDrive; 30–40 large 8K files will thrash sync. **Pause OneDrive sync during the overnight run.**
- **Scope honesty:** output is an edit-READY package (trimmed clips + graphics + SFX + map + grade), not a finished published reel. You still assemble/refine the final timeline in DaVinci; ambiguous keeper picks + graphics are flagged for your eye.
- **Golden rules hold:** never publish; voice-only 1080×1920 export; music added by you in the Edits app.
