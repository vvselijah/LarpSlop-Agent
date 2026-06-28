# PROGRESS — "Introducing ClipWith" overnight edit-prep

_Running log. Started 2026-06-25 (overnight run). Maintained continuously per the runbook._

> **▶ RESUMING (esp. new session/account)? Read [`SESSION-HANDOFF.md`](SESSION-HANDOFF.md) first.** As of 2026-06-26: Elijah assembled the 20 clips + color-corrected them in DaVinci Resolve Studio. **Next = motion graphics (`graphics/*.mov`) + SFX (gated) into his Resolve timeline → captions → export.**

## ⚑ FLAGS FOR ELIJAH (read these first)

1. **Footage was in the WRONG folder — handled, not a blocker.** You dropped the 24 raw takes into **`clipwithedit/`** (no hyphen, at hub root), but the runbook expected **`clipwith-edit/source/`**. I'm reading them in place from `clipwithedit/` and writing all trims to `clipwith-edit/clips/`. **Originals are never touched.** (If those `clipwithedit/*.mp4` are NOT the right footage, stop me.)
2. **~~Mixed orientation~~ — CORRECTED, NOT a problem.** The "3840×2160" files actually carry a **rotation flag** → they are **portrait 2160×3840 (9:16)**; ffmpeg bakes the rotation on trim. So **every delivered clip is correctly-oriented 9:16 portrait** (verified on frame grabs). The only real difference is **resolution**: clips 1,2,4–15 are 2160×3840 (sharper); clips 3,16–20 are 1728×3072 (softer). Both downscale cleanly to 1080×1920. No reframe needed.
3. **Paid generation = SPECS-ONLY (default).** You didn't leave a YES on the ElevenLabs/Higgsfield credit spend, so per the runbook default I'm doing ALL free work and only PREPARING the paid SFX/graphic prompts — generating nothing paid until you OK it.
4. **No ClipWith logo / app screenshots exist anywhere in the hub.** G7 (logo flash), G8 (app UI), G9 (timeline reveal) can't be built faithfully without them. I'll build typographic stand-ins and flag — drop a logo PNG/SVG + a couple app screenshots into `clipwith-edit/graphics/brand/` to upgrade them.
5. **Pause OneDrive sync** for the run — trims write new files into this OneDrive tree.

## Footage inventory (24 takes, `clipwithedit/`, all HEVC 29.97fps, ~8 min total)

| File (VID_20260624_…) | Dur | Orientation | Size | Likely role |
|---|---|---|---|---|
| _154429_174 | 13.5s | landscape 4K | 128 MB | short (line × takes) |
| _154802_175 | 10.0s | landscape 4K | 93 MB | short |
| _154848_176 | 9.3s | landscape 4K | 86 MB | short |
| _155034_177 | 22.8s | **vertical 9:16** | 170 MB | medium |
| _155108_178 | 22.4s | **vertical 9:16** | 169 MB | medium |
| _155511_179 | 8.7s | landscape 4K | 81 MB | short |
| _160014_180 | 15.0s | landscape 4K | 138 MB | short/med |
| _160142_181 | 2.3s | landscape 4K | 21 MB | very short (1 take) |
| _160453_182 | 4.8s | landscape 4K | 45 MB | short |
| _160512_183 | 8.6s | landscape 4K | 81 MB | short |
| _160647_184 | 8.1s | landscape 4K | 75 MB | short |
| _160854_185 | 8.9s | landscape 4K | 84 MB | short |
| _161053_186 | 5.6s | landscape 4K | 46 MB | short |
| _161335_187 | 6.7s | landscape 4K | 63 MB | short |
| _161435_188 | 7.7s | landscape 4K | 72 MB | short |
| _161509_189 | 10.2s | landscape 4K | 96 MB | short/med |
| _161801_190 | 4.7s | landscape 4K | 45 MB | short (NO backup wav) |
| _162203_197 | 9.0s | landscape 4K | 85 MB | short |
| _162604_201 | 52.2s | landscape 4K | 486 MB | **long run-through** |
| _163236_204 | 61.9s | **vertical 9:16** | 447 MB | **long run-through** |
| _163635_206 | 50.0s | **vertical 9:16** | 371 MB | **long run-through** |
| _163908_207 | 24.3s | **vertical 9:16** | 183 MB | medium |
| _164047_208 | 6.4s | **vertical 9:16** | 48 MB | short |
| _164253_209 | 110.9s | **vertical 9:16** | 810 MB | **longest — full script run?** |

23 of 24 have a per-clip-aligned **Røde Wireless PRO 32-bit-float backup WAV** (48 kHz, exact same duration as the video → timestamps map 1:1). File 190 has none (use its own mp4 audio).

## Pipeline decisions

- **Transcription (Phase 0):** local **whisper.cpp `base.en`** via abc wrap's `@remotion/install-whisper-cpp` (free, offline). The video-analyzer MCP's Whisper fallback is NOT configured (returned empty), so we use whisper.cpp directly on the clean Røde WAVs. whisper.cpp must install to a **space-free path** (`C:/Users/elija/.cache/whisper-clipwith`) — `Expand-Archive` and whisper-cli both break on the spaces in "abc wrap"/"ai agent team". Batch script: `abc wrap/scripts/batch-transcribe-clipwith.ts` → `clipwith-edit/transcripts/<stem>.json`.
- **Trims (Phase 1):** ffmpeg, new files only, `clipwith-edit/clips/NN_shotNN_keyword.mov`. Originals untouched.
- **Graphics (Phase 2):** Remotion 4.0.475 (installed in abc wrap) → transparent overlays; cinematic dark/orange brand from `graphics/SPEC.md`.
- **Color (Phase 5, last):** `auto-clip/colorkit` — coordinate with the parallel color session (don't clobber).

## Phase status

- **Phase 0 — Transcribe:** ✅ DONE. All 24 takes → word-level JSON in `transcripts/` (whisper.cpp base.en on the Røde WAVs). 4 false starts fixed (log-dir, space-path Expand-Archive ×2, merge bug).
- **Phase 1 — Keeper takes + trim:** ✅ DONE. 20 keeper clips → `clips/NN_shotNN_keyword.mp4` (frame-accurate H.264 CRF18, native res). Decisions in `cut-list.json`. Verified content + orientation on frame grabs.
- **Phase 2 — Motion graphics:** ✅ DONE. 7 graphics built on the real ClipWith brand (G6 Introducing, G7 logo flash, G3a $200B, G3b editing-industry, G5 stat pop, G10 CTA, G2 pain-point) → `graphics/*.png` (preview) + `graphics/*.mov` (**ProRes 4444, alpha verified yuva444p12le**). G8/G9 (app UI) asset-blocked → specced (need ClipWith app screenshots). Render fix saga (CRF config / 2.5GB public dir / png image-format / browser-timeout) solved → Node-API render in `abc wrap/scripts/render-clipwith-graphics.mjs`.
- **Phase 3 — SFX + audio:** ✅ specs done (`sfx/PROMPTS.md`, 14 ElevenLabs prompts, SPECS-ONLY/gated). Røde WAV dialogue-sub documented (free, optional).
- **Phase 4 — Assembly map + EDL:** ✅ DONE. `assembly-map.md` (master EDL) + `Introducing-ClipWith.fcpxml` (Resolve-importable timeline in order).
- **Phase 5 — Color grade:** ✅ look-test DONE. Graded clips 01 + 16 with **clean_pop** @0.7 → `graded/` (1080×1920 IG-ready). Verified: brighter/cleaner whites, natural skin, punchy — not over-cooked. Full batch = `bash grade_clips.sh clean_pop` (or swap the look). Elijah picks the final look.

## Log
- 2026-06-25 — Resumed overnight run. Found footage in `clipwithedit/` (not `clipwith-edit/source/`). Inventoried 24 takes (ffprobe). Confirmed Røde WAVs per-clip aligned. Built + debugged batch whisper transcriber.
- 2026-06-25 — Transcribed all 24. Built precise take map (global dedup across files). Trimmed 20 keepers + FCPXML + assembly map. **Corrected a false "orientation split" flag** — the 3840×2160 files carry a rotation flag → bake to 9:16 portrait; ALL clips are vertical. Built 6 brand motion graphics on abc wrap's existing ClipWith brand system.
