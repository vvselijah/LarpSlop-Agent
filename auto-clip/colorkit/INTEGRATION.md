# INTEGRATION — wiring `color.py` into the auto-clip pipeline (PROPOSAL, not applied)

**Status:** PROPOSAL · DRAFT-only · **NOT wired into the production `auto-clip` skill.**
**Date:** 2026-06-23 · **Author:** color-engine build run.
**Scope of this doc:** describe the one clean drop point for the headless color engine
(`auto-clip/color.py` + `colorkit/`) inside the existing clip pipeline, the exact command,
the trade-offs, and the env requirement. It proposes; it does **not** change `SKILL.md`,
`reframe.py`, `caption.py`, or any production stage. Wiring it in is **Elijah-gated** (see §6).

Grounding: the engine is BUILT and VERIFIED (stills, single-clip, multi-scene video). See
`auto-clip/COLOR-BUILD-STATUS.md` and the plan `docs/plans/2026-06-23-agentic-color-pipeline.md`.
This doc reflects the verified `color.py` CLI as it exists today, not aspiration.

---

## 1. Where it goes in the pipeline

The current auto-clip chain (from `auto-clip/README.md` and `.claude/skills/auto-clip/SKILL.md`):

```
transcribe → highlight (agent) → reframe | facetrack → [tighten] → caption → manifest
```

Color slots in as **a new OPT-IN stage AFTER `tighten.py` and BEFORE `caption.py`:**

```
transcribe → highlight → reframe|facetrack → [tighten] → [COLOR] → caption → manifest
                                                          ^^^^^^^^^
                                                          proposed new stage (opt-in)
```

**Why this exact position — three reasons, all load-bearing:**

1. **Captions must burn onto the GRADED image, never the reverse.** If you grade after
   captioning, the creative LUT and any WB shift would tint the white caption text and its
   outline, and a teal/orange look would visibly recolor the karaoke highlight. Grade the
   picture first; `caption.py` then burns crisp, untouched text on top. This ordering is the
   whole reason color goes *before* caption.
2. **Grade the final cut, not the raw highlight window.** Running color *after* `tighten.py`
   means the per-shot segmentation and the one-correction-per-shot anti-flicker math operate
   on the actual delivered frames (dead air + um/uh already removed), so no compute is spent
   grading frames that get cut, and shot boundaries line up with what ships.
3. **It is the last *picture* operation.** `caption.py` is a *text+audio* operation (libass
   burn + loudnorm/afftdn cleanup). Color is the final pixel/look pass; captions are an
   overlay on the finished look. Clean separation: color owns the image, caption owns the text.

The canonical color order is internal to `color.py` and unchanged by where it sits in the
chain: **correct → match → stylize** (Stage 1 neutral correction → Stage 2 inter-shot match →
Stage 3 creative look). The pipeline only decides *when* the whole color block runs.

---

## 2. The exact proposed command (and how it threads the filenames)

`color.py` writes a **video** to `out/<stem>_graded.mp4` (stills go to `_before.png`/`_after.png`).
The wiring depends on whether `tighten.py` ran, because that changes both the input filename and
the transcript that `caption.py` consumes.

All commands run **from the `auto-clip/` directory with the venv python** (see §5).

### Path A — clip was tightened (the documented "clip drags" branch)

`tighten.py` emits `out/<name>_tight.mp4` + a 0-based `data/<name>.tight.transcript.json`.
Insert color between them:

```powershell
# (existing) tighten the cut
.venv\Scripts\python.exe tighten.py <source> --transcript data\<stem>.transcript.json `
    --start S --end E --name <clipNN>
#   -> out\<clipNN>_tight.mp4  +  data\<clipNN>.tight.transcript.json

# (PROPOSED, opt-in) grade the tightened cut
.venv\Scripts\python.exe color.py out\<clipNN>_tight.mp4 --look warm_interview --match
#   -> out\<clipNN>_tight_graded.mp4

# (existing) caption the GRADED clip in --clip mode, reusing the 0-based remapped transcript
.venv\Scripts\python.exe caption.py data\<clipNN>.tight.transcript.json `
    --clip out\<clipNN>_tight_graded.mp4
#   -> out\<clipNN>_tight_graded_cap.mp4  (final deliverable)
```

This is the cleanest fit: `tighten.py` already produces a single 0-based clip and its remapped
transcript, and `caption.py --clip` already accepts an explicit clip path. Color just inserts
one `<stem>_graded` rename in between — `caption.py --clip` points at the graded file instead
of the tightened one. **No code change to `caption.py` is needed**; only the path passed to
`--clip` changes.

### Path B — clip was reframed/facetracked but not tightened

`reframe.py` produces `out/<stem>_clip<NN>.mp4` (batch, source-stem named); `facetrack.py`
produces `out/<name>_track.mp4`. Grade that file, then caption the graded result:

```powershell
# (PROPOSED, opt-in) grade one reframed/facetracked clip
.venv\Scripts\python.exe color.py out\<name>_track.mp4 --look kodak_2383_style
#   -> out\<name>_track_graded.mp4

# (existing) caption it
#   - facetrack/tighten single-clip output -> caption.py --clip with the matching 0-based transcript
#   - reframe batch output -> caption.py batch mode matches out\*_clip<NN>.mp4 by glob; because
#     color renames to *_graded.mp4 the batch glob no longer matches, so caption that specific
#     graded clip explicitly via --clip with its transcript window.
.venv\Scripts\python.exe caption.py data\<name>.transcript.json --clip out\<name>_track_graded.mp4
```

**Caveat worth flagging now (so it is not a surprise at wire-up):** `caption.py`'s *batch* mode
finds clips by the glob `out/*_clip<NN>.mp4`. Color's output is `*_graded.mp4`, which that glob
will not match. So when color is enabled, captioning must run in **`--clip` (single-file) mode**
against each `*_graded.mp4`, not batch mode. The tightened branch (Path A) is already single-clip,
so it is unaffected; only the un-tightened batch branch needs this awareness. (A future production
wiring could teach `caption.py`'s batch glob to also accept `*_graded.mp4`, but that is a code
change and out of scope for this proposal.)

---

## 3. Trade-offs (read before enabling)

### 3a. Encode time — the real cost

Color is **not free**: it adds a full extra decode+re-encode pass over the clip, and for video it
re-encodes *per shot* before concat (libx264 `veryfast`/CRF 18). On the verified test footage this
is fast for a single 20–24 s clip, but it scales with clip length and shot count:

- **Correct-only** (`color.py <clip>` with no `--look`, no `--match`): one re-encode pass; cheapest.
- **+ look** (`--look NAME`): same number of passes; the `lut3d` filter adds negligible time.
- **+ `--match`** (video, ≥2 shots): adds a Stage-2 pass that decodes a representative frame per
  shot and bakes a per-shot match LUT — small extra CPU, no extra full-clip pass.
- **+ `--deflicker`**: adds **one more full re-encode** of the concatenated master. Only enable when
  you actually see residual luminance pumping.

Because captioning *also* re-encodes (libass burn), enabling color means the clip is encoded twice
end-to-end (color → caption) instead of once. For a handful of review clips this is fine; for a
large batch it is the main reason color is opt-in, not always-on.

### 3b. When to **correct-only** vs **add a look**

- **Correct-only** (no `--look`): use when the footage just needs to look *right* — fix a white-balance
  cast, lift a flat/underexposed shot, normalize exposure across shots. This is the safe default and
  the highest-confidence part of the engine (per the plan, correction + deterministic looks are
  near-pro and flicker-free). Good for talking-head/interview clips where you want neutral, healthy
  skin and no obvious creative tint.
- **Add a look** (`--look warm_interview | teal_orange | kodak_2383_style | fuji_style | neutral_correct`):
  use when you want a consistent *house* aesthetic on top of the corrected base. The look is applied
  **uniformly across all shots** (Stage 3), so it reads as one cohesive grade. Pick by content:
  `warm_interview` for sit-down/podcast, `teal_orange` or `kodak_2383_style`/`fuji_style` for a
  cinematic/film feel. `neutral_correct` is a gentle technical look (close to correct-only with a
  light filmic touch). Looks are a creative choice — preview one clip before batch-applying.
- **Look-only, skip correction** (`--look NAME --no-correct`): rare. Use only when the footage is
  *already* correctly graded and you just want to stamp a look — e.g. re-styling already-finished
  footage. Note `--match` becomes a no-op here (it needs the corrected domain; the CLI warns and
  proceeds without inter-shot matching).

### 3c. When to use `--match` (and when not to)

`--match` is **video-only, opt-in, and a no-op on single-shot clips.** It reconciles color/exposure
**jumps at cut boundaries** by matching every shot toward a hero shot (constant Reinhard LAB transfer,
baked as a per-shot LUT — still flicker-free because it is constant per shot).

- **Use `--match`** for **multi-shot** clips where cuts are visibly mismatched — e.g. an interview
  intercut between two cameras/lighting, or a montage pulled from different parts of a source. It is
  the difference between "each shot is individually corrected" and "the shots feel like one continuous
  piece."
- **Skip `--match`** for single-shot clips (it does nothing) and when shots are already consistent
  (it adds a small pass for no visible gain). Dial it down with `--match-alpha` (default 0.8; lower =
  gentler) if matching overshoots and pulls a shot too far from its natural look.
- **Requires correction ON** — it matches in the post-correction domain. Combining `--match` with
  `--no-correct` disables it (the CLI tells you).

---

## 4. Default recommendation for the (future) wiring

When/if Elijah greenlights wiring this in, the recommended default posture mirrors the plan's
"correction auto-considered, stylize opt-in" stance:

- **Default offer:** `correct-only` on the final cut — safe, near-pro, flicker-free, one extra pass.
- **Opt-in look:** add `--look <name>` per clip when a house aesthetic is wanted; preview one clip first.
- **Opt-in `--match`:** only for multi-shot clips with visible cut-boundary mismatch.
- **Opt-in `--deflicker`:** only when residual pumping is actually visible (it costs a full extra pass).

Color should be a stage the operator *chooses* per run, not an always-on step — both to control
encode time and because a creative look is an editorial decision, not a mechanical one.

---

## 5. Environment requirement (non-negotiable)

`color.py` and `colorkit/` depend on `opencv-contrib-python`, `numpy`, `scikit-image`,
`colour-science`, and `scenedetect`, which are installed **only in the auto-clip venv** at
`auto-clip/.venv` (Python 3.12.10). They are **not** on the system `python`.

- **Always invoke via the venv python**, from the `auto-clip/` directory:
  `auto-clip\.venv\Scripts\python.exe color.py ...`
  (The other auto-clip stages can run on system python with `faster-whisper`/ffmpeg; color cannot —
  it needs the cv2/scikit-image/colour-science stack in the venv.)
- **Run via PowerShell, not Bash** — per the hub env gotchas, `python`/`ffmpeg` are on the PowerShell
  PATH, not the Bash PATH, and heavy cv2 imports are slow on the OneDrive disk (the engine imports cv2
  lazily and per-image to keep this tolerable).
- **FFmpeg** must be on PATH (already true in this hub and `abc wrap`). The engine stages every `.cube`
  into one temp dir and runs ffmpeg with `cwd` set there, referencing cubes by **bare filename** — this
  is the deliberate workaround for the Windows gotcha where ffmpeg's `lut3d` filtergraph rejects absolute
  Windows paths (drive colon + spaces). Do not "fix" this by passing absolute cube paths; it will break.
- If a look errors as a missing `.cube`, regenerate the LUTs: `python -m colorkit.luts --all`
  (run with the venv python).

---

## 6. Standing-rules compliance (why this stays a proposal)

- **CLAUDE.md rule 1 — never publish without per-action confirmation.** `color.py` stops at `out/`
  and prints a manifest; it never posts. So does the rest of the chain. Wiring color in does not
  change that, but the *decision* to wire it in, and any creative-look choice, is Elijah's.
- **This doc is DRAFT/PROPOSE-only.** It does not edit `SKILL.md` or any production stage. Auto-wiring
  the engine into the skill without Elijah's go would (a) silently add encode time to every run and
  (b) make an editorial look choice on his behalf — both of which the hub's golden rule reserves for him.
- **To actually enable it**, the minimal change would be: add an opt-in step 4.5 in
  `.claude/skills/auto-clip/SKILL.md` ("Color grade (optional)") with the §2 commands, and add the
  color deps to `auto-clip/requirements.txt` (or document the venv). Leave it OFF by default. That edit
  is intentionally **not made here** — it is the Elijah-gated next action.

---

## 7. Quick reference — the proposed stage in one block

```powershell
# OPT-IN color stage, AFTER tighten/reframe, BEFORE caption. Run from auto-clip\ with the venv python.

# correct-only (safe default):
.venv\Scripts\python.exe color.py out\<clip>.mp4

# correct + house look:
.venv\Scripts\python.exe color.py out\<clip>.mp4 --look warm_interview

# multi-shot clip with mismatched cuts -> add inter-shot matching:
.venv\Scripts\python.exe color.py out\<clip>.mp4 --look kodak_2383_style --match

#   -> out\<clip>_graded.mp4   (then caption that file via caption.py --clip)

# looks available: neutral_correct · warm_interview · teal_orange · kodak_2383_style · fuji_style
```

Outputs land in `out/` as review files only. Nothing is published.
