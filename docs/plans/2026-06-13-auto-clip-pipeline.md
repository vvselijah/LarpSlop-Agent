# Plan: auto-clip pipeline — long video → ranked vertical 9:16 shorts

- **Date:** 2026-06-13
- **Branch:** (hub not under git push yet — local commits only; per CLAUDE.md the branch/PR mechanics are aspirational)
- **Size estimate:** large
- **Status:** draft (awaiting Elijah's approval — NO engine code is written until then)

> This is Build C from `docs/plans/2026-06-13-capabilities-research-plan.md`. The research already
> settled the toolchain and the reuse map; this PLAN turns that into a buildable, checkpointed spec.
> Per CLAUDE.md the dev-workflow loop requires a written, premise-verified plan **before** any Python
> engine code. The premises below were verified against the real installed code/libs on 2026-06-13.

---

## 1. Problem

Elijah is ramping long-form (10–30 min YouTube talking-head, 1–2 hr podcast/interview) but has no
local way to turn one long video into a stack of vertical reels. Today that means hand-scrubbing the
whole thing, guessing which 30–60s windows are clip-worthy, then manually reframing each to 9:16 — an
hour-plus of grunt work per source, which is why long-form rarely becomes daily reels. He needs a
local, ~$0 engine that ingests a long file, finds and **ranks** the strongest moments, and emits
ready-to-review vertical shorts — stopping at files on disk for his approval, never publishing.
Crucially, ~70% of the machinery already exists across this hub and the sibling `..\abc wrap\` repo,
so the job is **reuse-first wiring + three genuinely new pieces**, not a from-scratch build.

## 2. Non-goals

- This change will **not** auto-publish, schedule, or upload anything. The engine stops at files in
  `auto-clip/out/` and prints a manifest (CLAUDE.md rule 1 — the publish click is Elijah's).
- This change will **not** add a DM/comment path, a scraper, or any owned-account write.
- This change will **not** rebuild anything that already works: not Whisper, not `build_cutlist.js`,
  not `PodcastEdit.tsx`, not caption-engine / broll-inserter / platform-exporter, not the FFmpeg MCP.
- This change will **not** add speaker diarization (WhisperX) in v1 — single-track Faster-Whisper only.
  Diarization is an explicit v2 add (see Open Questions).
- This change will **not** depend on Remotion for the **default** render path (the sibling's documented
  ~10 GB/bundle disk blowup). Remotion is opt-in, only when stylized output is requested.
- This change will **not** force the GPU reinstall. The engine must run correctly CPU-only (slow);
  the cu128 reinstall is a separate, Elijah-gated speed decision (§ Premise 6, Open Questions).
- This change will **not** be wired into `Daily Agent Refresh.bat` in v1 — it is **on-demand** (a long
  video isn't a daily cron input). Chaining is a later, explicit decision.
- This change will **not** invent vault properties or post to the vault — output is plain files + manifest.

## 3. Premises

Each verified against the **actual** installed code/libraries on this machine on 2026-06-13.

| # | Premise | Verified |
|---|---|---|
| 1 | `transcribe.py` at hub root exists and uses `faster_whisper.WhisperModel("base.en", device="cpu", compute_type="int8")` with `.transcribe(..., vad_filter=True)` — but does **NOT** pass `word_timestamps=True` and only writes segment-level text. So a word-level wrapper is genuinely new, not a dupe. | ✅ Confirmed (read file: lines 1–16; no `word_timestamps`, segment loop only) |
| 2 | `faster-whisper` is installed and importable at a usable version. | ✅ Confirmed `faster_whisper 1.2.1` |
| 3 | House engine convention = `BASE = Path(__file__).resolve().parent`, a `data/` dir, a `log()` helper that prints + appends to a logfile, stdlib-only, run via `python <engine>.py`, chained path-relative in `Daily Agent Refresh.bat`. | ✅ Confirmed in `ig-dashboard/refresh.py` (BASE line 25, `log()` 63–70, `data/`) and `intel/competitor-radar.py` (BASE 22, `log()` 36–37). `.bat` calls each script by `%ROOT%`-relative path. |
| 4 | The sibling `..\abc wrap\` is reachable, and `interview/work/build_cutlist.js` is the editorial cut-list brain (gap-trim/dead-air, same-speaker merge, interjection absorb, min-shot floor, frame-accurate output). | ✅ Confirmed (read full file). Tunables in `P` (lines 13–28): `minShot 1.5`, `trimGap 2.5`, `breath 0.6`, merge logic lines 39–85. This is the boundary logic to port/reuse for pre-filtering highlight candidates. |
| 5 | `..\abc wrap\src\edits\PodcastEdit.tsx` owns a reusable crop transform with a **1.35×-style softness cap + black-edge clamp**: `cropTransform()` clamps translate by `maxT = (s-1)/(2*s)` so the scaled frame always covers the viewport (never reveals black edges). | ✅ Confirmed (read file: `cropTransform` lines 50–62; clamp comment line 53). This is the exact transform the new reframe must feed. |
| 6 | The RTX 5070 (Blackwell sm_120) is present but PyTorch is the **+cpu** build → faster-whisper runs CPU-only; near-instant transcribe + nvenc needs torch cu128 + cuDNN9. | ✅ Confirmed: `torch 2.11.0+cpu`, `torch.cuda.is_available() == False`; `nvidia-smi` → "NVIDIA GeForce RTX 5070" driver 591.86. Multi-GB reinstall required to use the GPU. |
| 7 | The FFmpeg MCP `resize-video` is **fixed-preset** and CANNOT do a 9:16 crop — its only params are `videoPath` + `resolutions` (enum: 360p/480p/720p/1080p), no crop/aspect/filter. So the reframe must be a **direct FFmpeg CLI filtergraph**. | ✅ Confirmed (loaded tool schema: `resolutions` enum only; no crop/aspect/pad/filter param). |
| 8 | A system `ffmpeg` CLI with NVENC is on PATH for a direct filtergraph render (crop/scale/pad + `h264_nvenc`), and `libx264` is available as the CPU fallback. | ✅ Confirmed: `ffmpeg -encoders` lists `h264_nvenc`, `hevc_nvenc`, `av1_nvenc`; libx264 ships with the same build. |
| 9 | Remotion renders blow up disk (~10 GB/bundle) on this setup, so the default render path must be pure-FFmpeg, not Remotion. | ✅ Confirmed in `..\abc wrap\INTERVIEW-HANDOFF.md` ("DISK GOTCHA: ~10GB of %TEMP%\remotion-webpack-bundle-* per render … filled C: to 0.24GB free"). |
| 10 | This is the **first** hub engine to need third-party deps — every existing engine (`refresh.py`, `competitor-radar.py`, `trend-radar.py`) is stdlib-only (+ `curl.exe`). No `requirements.txt` convention exists in the hub yet. | ✅ Confirmed: both read engines import only stdlib (`json/os/subprocess/sys/time/datetime/pathlib/statistics/winreg`); no `requirements.txt` anywhere in the hub root or engine folders. |
| 11 | `opencv` is installed; `mediapipe` is **not**. The face/subject reframe needs a face detector. | ✅ Confirmed: `cv2 4.13.0` imports; `import mediapipe` → `ModuleNotFoundError`. So `mediapipe` is a new dep, and OpenCV's bundled Haar/DNN detector is a zero-extra-dep fallback. |
| 12 | An LLM key is available to the engine for the highlight selector (the one new "brain"). | ⚠️ Unverified at file level — research assumed "just an LLM key." **Open Question for Elijah:** which provider/key, or route via the Claude Code session / local Ollama. Engine must degrade to a heuristic-only ranking if no key is set (see Failure modes). |

## 4. Approach

### Considered alternatives

| Approach | Effort | Key tradeoff |
|---|---|---|
| A. **Reuse-first hybrid (CHOSEN):** new `auto-clip/` engine = thin orchestrator wiring local Whisper + a ported `build_cutlist` boundary filter + an LLM highlight selector + an OpenCV reframe → **pure-FFmpeg** vertical render; Remotion/caption-engine only on request. | Medium (3 new pieces; rest is wiring) | Matches house conventions; ~$0; no platform risk; default render avoids the Remotion disk blowup. Most logic is glue + reuse. |
| B. **Adopt an off-the-shelf repo wholesale** (SamurAIGPT / OpenShorts / KazKozDev). | Medium-High | Drags in Docker/cloud keys (OpenShorts), paid APIs (SamurAIGPT's MuAPI), or Windows-untested stacks (KazKozDev). Throws away the proven `build_cutlist`/`PodcastEdit` brains we already own. Research verdict: **mine for prompts/ideas, don't adopt.** |
| C. **Remotion-only render path** (reuse `PodcastEdit` comp end-to-end for every clip). | High | Re-triggers the documented ~10 GB/bundle disk blowup on every clip; overkill for a plain crop. Right tool only for *stylized* output, not the default. |

### Chosen approach and why

**A.** The research deep-dive (Workflow 1, high confidence) already established that ~70% exists and the
only real gaps are: (1) word-level transcript JSON, (2) the highlight *selector* brain, (3) a
face-aware 9:16 reframe. Everything else is reuse. Building a thin orchestrator that mirrors
`ig-dashboard/`/`intel/` keeps it inside the house pattern Elijah already trusts, costs ~$0, and the
pure-FFmpeg default render sidesteps the one big known landmine (Remotion disk blowup). Stylized
output stays available by routing into the existing Remotion skills only when asked.

## 5. Design

### Engine folder (mirrors `ig-dashboard/` / `intel/`)

```
auto-clip/
  clip.py            # entry orchestrator: probe → transcribe → highlight → reframe → render → manifest
  transcribe.py      # NEW piece (a): word-level Faster-Whisper wrapper → words.json
  highlight.py       # NEW piece (b): boundary pre-filter (ported build_cutlist logic) + LLM selector → clips.json
  reframe.py         # NEW piece (c): face/subject track → smoothed crop track (PodcastEdit clamp math) → FFmpeg filtergraph render
  requirements.txt   # NEW convention for the hub (see §"Dependency departure")
  data/              # cache: words.json, clips.json, crop tracks, run logs (BASE-anchored, like other engines)
  out/               # FINAL deliverables only — vertical .mp4 clips + manifest.json/manifest.md
  README.md          # how-to + GPU note + reuse map (mirrors the other engines' READMEs)
.claude/skills/auto-clip/SKILL.md   # thin skill: "turn this long video into ranked shorts" → calls clip.py
```

### Data flow

```
 long video (mp4/mov/mkv)
        │
        ▼
 [clip.py] ── probe via FFmpeg MCP get-video-info (duration, fps, res, audio) ─┐
        │                                                                       │
        ▼                                                                       │
 extract audio  ── FFmpeg MCP extract-audio (16k wav) ─────────────────────────┘
        │
        ▼
 (a) transcribe.py  faster-whisper word_timestamps=True
        │           → data/words.json  [{text,start,end}, ...]   (flat, matches existing comps)
        ▼
 (b) highlight.py
        │  1. PORT build_cutlist boundary logic over the word stream:
        │     dead-air gap-trim (trimGap 2.5 / breath 0.6), merge, min-shot floor → candidate windows
        │  2. LLM selector pass over transcript+windows
        │     → ranked clips.json: [{start,end,title,hook,score,reason}, ...]
        │     (heuristic-only fallback if no LLM key)
        ▼
 (c) reframe.py   per selected clip:
        │  - sample frames, OpenCV (mediapipe if installed else Haar/DNN) → per-frame subject box
        │  - smooth into a crop track; map to PodcastEdit cropTransform math
        │    (scale cap ~1.35×, black-edge clamp maxT=(s-1)/(2s))
        │  - emit a direct FFmpeg CLI filtergraph: crop=/scale=1080:1920/pad=
        │    encode h264_nvenc if GPU on, else libx264 -crf 18
        ▼
 out/<source>__<rank>_<slug>.mp4  +  out/manifest.{json,md}
        │
        └── (OPTIONAL, on request only) → Remotion edit-video / caption-engine for stylized captions/b-roll
```

### Reuse map — what is NOT rebuilt

| Capability | Reused from | Used for |
|---|---|---|
| Local transcription | faster-whisper 1.2.1 (already installed) + hub-root `transcribe.py` pattern | (a) generalize, don't replace |
| Editorial boundary brain | `..\abc wrap\interview\work\build_cutlist.js` (`P` tunables, gap-trim, merge, min-shot) | (b) port the boundary logic to pre-filter candidates |
| 9:16 crop math | `..\abc wrap\src\edits\PodcastEdit.tsx` `cropTransform` (1.35× cap + black-edge clamp) | (c) the reframe target transform |
| Video probe + audio extract | FFmpeg 8.1 MCP `get-video-info` / `extract-audio` | clip.py ingest |
| Stylized captions / b-roll / platform export | `caption-engine`, `broll-inserter`, `platform-exporter` skills | OPTIONAL post-step, only when asked |
| Stylized render comp | Remotion `edit-video` skill (NOT the default path) | OPTIONAL stylized output only |

> **Why MCP `resize-video` is not used for the crop:** Premise 7 — it is fixed-preset (resolutions enum
> only) and cannot 9:16 crop. The reframe is a direct FFmpeg CLI filtergraph instead. The MCP is used
> only for probe + audio extract.

### Existing helpers/modules this change should reuse (searched the hub)

- `log()` helper pattern — copy the `ig-dashboard/refresh.py` flavor (print + append to `data/clip.log`).
- `BASE = Path(__file__).resolve().parent` anchoring + `data/`/`out/` dirs created with `mkdir(exist_ok=True)`.
- `get_token()`-style winreg fallback is **not** needed (no IG token in this engine).
- Hub-root `transcribe.py` as the literal starting point for `auto-clip/transcribe.py` (generalize args, add `word_timestamps=True`, emit JSON instead of timestamped text).

### Dependency departure — the new `requirements.txt` convention

This is the first hub engine needing third-party deps, so the PLAN proposes a convention (decision for Elijah):

- Each engine that needs deps ships its own `auto-clip/requirements.txt` (engine-local, not a hub-global file), pinned:
  - `faster-whisper==1.2.1` (already satisfied)
  - `opencv-python` (already satisfied: 4.13.0)
  - `mediapipe` (NEW — not installed; optional, with an OpenCV Haar/DNN fallback so the engine still runs without it)
  - **torch is deliberately NOT pinned here** — it's a system/GPU concern (see Premise 6) handled out-of-band, not via this requirements file, to avoid clobbering the working +cpu build by accident.
- README documents `python -m pip install -r auto-clip/requirements.txt`.
- Note the contrast in the engine README: existing engines (`refresh.py`, `competitor-radar.py`, `trend-radar.py`) stay stdlib-only; only `auto-clip/` carries deps.

### GPU prerequisite (decision flagged for Elijah, not auto-done)

- **Current:** torch 2.11.0+cpu, `cuda.is_available()==False` → faster-whisper transcribes on CPU (slow on a 1–2 hr podcast), and nvenc still works for *encode* (it's an ffmpeg feature, independent of torch) but the transcribe stage is the bottleneck.
- **To unlock GPU transcribe:** reinstall `torch --index-url https://download.pytorch.org/whl/cu128` + put cuDNN9/CUDA12 DLLs on PATH. **Multi-GB download.** Risk: a bad reinstall can break the current working +cpu torch.
- **Recommendation:** ship v1 CPU-correct; treat the cu128 reinstall as an explicit, reversible step Elijah approves separately (Open Question). The engine auto-detects `torch.cuda.is_available()` and picks device/compute-type and nvenc-vs-x264 accordingly — no code change needed when the GPU is later enabled.

### Render path (Premise 7/9 — pure FFmpeg default)

- Default: direct `ffmpeg` CLI filtergraph `crop=…:…:x:y, scale=1080:1920, pad=…` →
  `-c:v h264_nvenc -cq 19` when GPU on, else `-c:v libx264 -crf 18 -preset medium`; audio `-c:a aac -b:a 192k`.
- This avoids Remotion's ~10 GB/bundle disk blowup entirely for the common case.
- Stylized output (animated captions, b-roll, branded layout) is an **opt-in** branch that routes the
  clip into the Remotion `edit-video`/`caption-engine` skills — and the README carries the documented
  `%TEMP%\remotion-*` cleanup warning from the sibling INTERVIEW-HANDOFF.

### Standing rules at the engine EXIT

- The engine **stops at files in `out/`** and prints a manifest (ranked list: rank, score, title, hook, in/out, path). It NEVER publishes, schedules, DMs, or posts.
- If an IG-API publish path is **ever** added later, it must be voice-only / original-audio (CLAUDE.md
  rule 4 — API-published reels can't use licensed/trending audio) and pre-flighted with
  `get_content_publishing_limit`. That is explicitly out of scope for this build.

## 6. Failure modes

| Scenario | Expected behavior |
|---|---|
| Partial failure (transcribe OK, highlight LLM fails) | Cache `data/words.json`; highlight stage falls back to **heuristic ranking** (boundary windows scored by length/energy/keyword density) and logs a warning. Resume re-uses cached words.json — never re-transcribes. |
| No LLM key set (Premise 12) | Run in heuristic-only mode end-to-end; manifest flags `selector: heuristic`. Engine still produces clips. |
| Reframe finds no face in a window | Fall back to a static center crop (scale=1080:1920 from center) with the same clamp math; log the clip as `reframe: center-fallback`. Never crash a whole run for one bad clip. |
| mediapipe not installed | Auto-fallback to OpenCV Haar/DNN detector (Premise 11); log `detector: opencv-fallback`. Engine never hard-requires mediapipe. |
| GPU not available (torch +cpu) | Transcribe on CPU int8, encode with libx264; log `device: cpu`. Correct, just slow. No failure. |
| Retry / duplicate run on same source | Idempotent via `data/` cache keyed on source path + mtime + params hash; existing `out/` clips overwritten deterministically, not duplicated. |
| Concurrent access (two runs at once) | Out of scope (single-user, on-demand). README says run one at a time; a lockfile in `data/` is a v2 nicety, not v1. |
| Empty / oversized / malformed input (0-byte, non-video, 3 hr file) | Probe via MCP first; if duration/streams missing or audio absent → clear error + exit non-zero before any heavy work. Oversized (e.g. >2 hr) → warn about CPU transcribe time, proceed. |
| Disk pressure | Default pure-FFmpeg path is light; if the optional Remotion branch is used, README mandates the `%TEMP%\remotion-*` cleanup (sibling gotcha). |

## 7. UI states

No UI. The engine is a CLI that writes files + a manifest; the optional dashboard view is out of scope.
(Section retained per template; nothing to fill.)

## 8. Test plan

| Case | Level | Covers failure mode # |
|---|---|---|
| Short clip (~2 min talking-head) → words.json has word-level `start/end` | unit (transcribe.py) | Premise 1 gap (word timestamps) |
| Known dead-air sample → boundary filter trims it (matches build_cutlist trimGap behavior) | unit (highlight.py) | partial-failure / boundary correctness |
| Heuristic-only mode (LLM key unset) produces a ranked clips.json | integration | no-LLM-key fallback |
| Off-center subject sample → reframe keeps face in frame, never reveals black edges (clamp holds) | unit (reframe.py) | reframe / black-edge clamp (Premise 5) |
| No-face window → center-crop fallback, run completes | unit | reframe no-face |
| mediapipe uninstalled → OpenCV fallback path runs | integration | mediapipe-missing (Premise 11) |
| End-to-end on a real 15–25 min source → N ranked vertical 1080×1920 clips in out/ + manifest | e2e | whole pipeline |
| CPU-only run completes (torch +cpu) and GPU run (if enabled) completes | integration | GPU-absent / device autodetect (Premise 6) |
| Malformed/0-byte/non-video input → clean error, non-zero exit, no partial files | integration | empty/malformed input |
| `out/` contains ONLY deliverables; nothing posted; manifest printed | e2e | standing rule (exit behavior) |

## 9. Steps

Ordered, checkpoint-sized. One commit per step (local). **No step starts until Elijah approves this plan.**

1. **Scaffold** `auto-clip/` (folders `data/`, `out/`), `README.md` stub, `requirements.txt`, and the thin
   `.claude/skills/auto-clip/SKILL.md`. Add `log()` + `BASE` boilerplate to `clip.py`. (No real logic yet.)
2. **Piece (a) — `transcribe.py`:** generalize hub-root `transcribe.py` → take a video/audio path, run
   faster-whisper with `word_timestamps=True`, autodetect device (cuda→cpu) and compute-type, emit
   `data/words.json` as flat `[{text,start,end}]`. Test on a short clip.
3. **Audio extract + probe in `clip.py`:** wire FFmpeg MCP `get-video-info` + `extract-audio`; validate
   input early (malformed-input failure mode); cache by source path+mtime.
4. **Piece (b) — `highlight.py` boundary filter:** port `build_cutlist.js` boundary logic (gap-trim,
   merge, min-shot floor, interjection absorb) to Python over the word stream → candidate windows. Test
   against a dead-air sample.
5. **Piece (b) — LLM selector + heuristic fallback:** LLM pass → ranked `{start,end,title,hook,score,reason}`;
   heuristic ranking when no key. Emit `data/clips.json`. Test both modes.
6. **Piece (c) — `reframe.py` subject track:** OpenCV (mediapipe-if-present) face/subject box per sampled
   frame → smoothed crop track; map to PodcastEdit clamp math; no-face center fallback.
7. **Piece (c) — pure-FFmpeg render:** build the `crop/scale/pad` filtergraph per clip; nvenc-or-x264 by
   device; write to `out/`. Test on an off-center sample (clamp holds, 1080×1920).
8. **Orchestrate + manifest:** `clip.py` runs the full chain, writes `out/manifest.{json,md}`, prints the
   ranked summary, exits at files. End-to-end test on a real 15–25 min source.
9. **Optional stylized branch (flag-gated):** route a chosen clip into Remotion `edit-video`/`caption-engine`;
   document the `%TEMP%\remotion-*` cleanup. (Build only if Elijah wants stylized in v1.)
10. **Docs + handoff:** finish `README.md` (reuse map, GPU note, requirements convention), add the engine
    to the capability quick-map in CLAUDE.md, append a dated learning to `team/memory.md`. (Wiring into
    `Daily Agent Refresh.bat` deliberately deferred — on-demand, not daily.)

## 10. Retro (fill after shipping)

- Premises that turned out wrong:
- Missing from this plan:
- Context-file updates made:

---

## OPEN QUESTIONS for Elijah (gate the build)

1. **LLM for the highlight selector (Premise 12):** which key/provider should the selector use — a hosted
   API key in env, route through the Claude Code session, or a local Ollama model? (Engine ships with a
   heuristic fallback either way, but the LLM pass is the quality lever.)
2. **GPU reinstall (Premise 6):** approve the multi-GB `torch cu128 + cuDNN9` reinstall now (fast transcribe
   + nvenc), or ship v1 CPU-correct and reinstall later? It's reversible but can disrupt the working +cpu torch.
3. **Diarization (v1 non-goal):** single-speaker YouTube talking-head is fine on plain Faster-Whisper. For
   2-speaker podcasts, do you want WhisperX diarization in v1, or accept v1 single-track and add it in v2?
4. **mediapipe:** OK to add `mediapipe` as a dep for better face tracking, or stay on the OpenCV-only
   fallback to keep deps minimal? (Engine runs either way.)
5. **Stylized output in v1:** default to plain pure-FFmpeg vertical crops, or also wire the optional
   Remotion caption/b-roll branch from day one (accepting the disk-cleanup chore)?
6. **`requirements.txt` convention:** approve engine-local `requirements.txt` (proposed here) as the hub
   standard for any future engine that needs third-party deps?
7. **Scheduling:** confirm on-demand only for v1 (NOT chained into `Daily Agent Refresh.bat`) — a long
   video isn't a daily cron input.
