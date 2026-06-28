# Introducing ClipWith — edit-ready package

Overnight-prepped from your 24 raw takes. This is a **strong first pass**, not a published final —
you still assemble/refine the timeline in DaVinci and make the calls flagged below.

> **▶ Resuming / new session or account? Read [`SESSION-HANDOFF.md`](SESSION-HANDOFF.md) first** — it has the
> current state (clips assembled + color-corrected in Resolve; next = graphics + SFX) and how to continue cold.

## Start here
1. **Import `Introducing-ClipWith.fcpxml`** into DaVinci Resolve → the 20 keeper clips drop onto a
   timeline in script order automatically. (File → Import → Timeline. If Resolve is fussy about the
   FCPXML, just drag the numbered clips from `clips/` — they sort in order.)
2. **Read `assembly-map.md`** — the master edit-decision-list: every line → which clip → which graphic
   (G#) → which SFX, with the beats to tighten.
3. **Skim the ⚑ flags** in `assembly-map.md` and `PROGRESS.md` — the few things only you should decide.

## What's in here
| Folder / file | What it is |
|---|---|
| `clips/` | **20 trimmed keeper takes** (the last clean take of each line), chronological, frame-accurate H.264, native res. All 9:16 portrait. |
| `Introducing-ClipWith.fcpxml` | Resolve-importable timeline — clips pre-laid in order. |
| `assembly-map.md` | Master EDL: line → clip → graphic → SFX + timings + decisions for you. |
| `cut-list.json` | Machine-readable source of truth (re-run `build_clips.py` to rebuild clips). |
| `graphics/` | **6 on-brand motion graphics** (Introducing card, logo flash, $200B, editing-industry, stat pop, CTA) as PNG + ProRes 4444 (alpha). Built on your real ClipWith brand. `SPEC.md` maps them to beats. |
| `sfx/PROMPTS.md` | 14 ElevenLabs SFX prompts, ready to fire — **not generated yet** (credit spend, your call). |
| `transcripts/` | Word-level transcripts of all 24 raw takes (whisper.cpp). |
| `graded/` | Color-graded clips (colorkit) — a look-test sample; full batch via `grade_clips.sh`. |
| `verify/` | Frame grabs I used to confirm content + orientation. |

## The decisions only you should make (don't let me guess)
1. **Missing beats:** no clean standalone "so we built something to fix it" / "ClipWith.ai" name-drop —
   they merged into clip 15. Want a quick VO pickup, or lean on the **G6 "Introducing ClipWith"** card?
2. **Pauses to tighten:** clip 1 (hook, ~5s mid-line gap), clip 4 (very slow $200B delivery).
3. **SFX + extra graphics = credit spend** — say the word and I'll generate the SFX (`sfx/PROMPTS.md`)
   and the asset-blocked graphics (G8/G9 app-UI — drop ClipWith app screenshots into `graphics/brand/`).
4. **Look:** pick a color look (`grade_clips.sh <look>`) — I sampled one as a starting point.

## Re-run anything
- Rebuild clips: `auto-clip/.venv/Scripts/python.exe clipwith-edit/build_clips.py`
- Re-grade (your look): `bash clipwith-edit/grade_clips.sh golden_hour`
- Re-render graphics: `cd "abc wrap" && bash scripts/render-clipwith-graphics.sh all`

## Standing rules honored
DRAFT only · never published · voice-only (music added by you in the IG Edits app) · no paid generation
without your OK · originals in `clipwithedit/` never modified.
