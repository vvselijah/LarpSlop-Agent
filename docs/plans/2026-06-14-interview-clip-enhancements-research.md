# Interview-Clip Enhancements — Research (2026-06-14)

**Context:** Local pipeline turns long 2-person interview/podcast footage (16:9, often TWO camera
angles of the same conversation) into captioned vertical 9:16 clips. Already have:
faster-whisper word-level transcription → Claude highlight picker → FFmpeg 9:16 reframe →
FFmpeg/libass burned captions. We are NOW adding **face-tracking reframe** (crop follows the
active speaker). Question: what to add **alongside** face-tracking + captions to make these great.

**Constraints that shaped every verdict:**
- Windows-friendly, Python/FFmpeg-compatible, permissive license (MIT/Apache/BSD/Unlicense).
- **OneDrive-synced disk hazard:** heavy native imports (`torch`, `opencv`/`cv2`, large model
  checkpoints) have been observed to HANG or load very slowly here. Anything torch/CUDA-heavy is
  flagged. Prefer ONNXRuntime-CPU and pure-FFmpeg paths; if a torch tool is worth it, install the
  CPU-only wheel and keep the package + checkpoints OFF the synced path (a local `C:\models`
  cache, `HF_HOME` / `TORCH_HOME` redirected) so OneDrive never touches them mid-run.

---

## Verdict table (prioritized)

| # | Enhancement | OSS tool | License | Dep weight / OneDrive risk | Verdict |
|---|---|---|---|---|---|
| 1 | **Active-speaker detection** (which face is talking; multicam angle pick) | **LR-ASD** (2025, successor to Light-ASD) | MIT | torch + cv2 + S3FD — **HEAVY, OneDrive risk** | **ADD-NOW (gated)** — this IS the face-tracking brain |
| 2 | **Auto punch-in / dynamic zoom** on the talker | Pure FFmpeg `scale`/`crop`/`zoompan` driven by our own data | n/a | **Zero new deps** | **ADD-NOW** |
| 3 | **Silence / dead-air auto-cut** | **auto-editor** | Unlicense (public domain) | Pure Python + FFmpeg, **no torch** | **ADD-NOW** |
| 3b | **Filler-word removal** ("um/uh/like") | Our own transcript + FFmpeg | n/a | Zero new deps | **ADD-NOW** |
| 4 | **Scene/shot-change detection** (multicam cut points, b-roll timing) | **PySceneDetect** | BSD-3 | cv2 + numpy — moderate (cv2 = OneDrive risk) | **ADD-NOW** |
| 5 | **Emoji / keyword pop-ups, word-pop captions, zoom-on-emphasis** | libass/ASS (already have) + drawtext | n/a (FFmpeg) | Zero new deps | **ADD-NOW** |
| 6 | **Background blur / segmentation** | MediaPipe Selfie/Image Segmenter | Apache 2.0 | mediapipe wheel (~bundles deps) — moderate | **ADD-LATER** |
| 6b | rembg background removal | rembg (U²-Net/BiRefNet) | MIT | ONNXRuntime, CPU-slow 3-8 s/img | **ADD-LATER** |
| 6c | SAM2 video segmentation | facebookresearch/sam2 | Apache 2.0 | **torch + CUDA, very heavy** | **SKIP** (for now) |
| 7 | **Audio cleanup** (denoise / loudness normalize) | FFmpeg `loudnorm` + `arnndn`/`afftdn` | n/a | Zero new deps | **ADD-NOW (cheap win)** |
| 8 | **Beat-synced cuts** | librosa beat-track OR FFmpeg | ISC/MIT | librosa pulls numpy/scipy/numba — moderate | **ADD-LATER** |
| 9 | **PyAutoFlip** (saliency reframing) | pyautoflip | MIT | InsightFace + ONNX + mediapipe (~57 MB) | **SKIP** — overlaps #1/#2 |
| 10 | **Whisper-level VAD turn segmentation** (cheap speaker turns) | Silero-VAD | MIT | torchaudio (small) OR onnx | **ADD-LATER** (alt to #1 for multicam) |

---

## Per-item detail + how it composes with our engine

### 1. Active-speaker detection (ASD) — the face-tracking brain — ADD-NOW (gated)
**What it does:** Per-frame, scores each detected face for "is this person talking right now" using
audio-visual sync (lip motion vs. audio). Output is exactly what face-tracking reframe needs: a
track ID + bounding box for the *active* speaker over time, so the 9:16 crop locks onto whoever is
talking and switches when the turn changes. For our **two-angle** case it also tells us which camera
angle to use at each moment (multicam switching = pick the angle whose active face is the talker, or
just always frame the talker).

**Tool:** **[LR-ASD](https://github.com/Junhua-Liao/LR-ASD)** (Springer IJCV 2025) — the maintained,
lighter, more robust successor to **[Light-ASD](https://github.com/Junhua-Liao/Light-ASD)** (CVPR
2023). MIT licensed. It ships a **Columbia-style demo** (`Columbia_test.py --videoName X
--videoFolder demo`) that runs end-to-end on an arbitrary `.mp4`: S3FD face detect → track faces →
ASD score per track → annotated output (green = active, red = inactive). This demo scaffold *is* the
reference pipeline OpusClip-class tools use. LR-ASD's design explicitly minimizes per-inference
memory (single candidate face seq, split 2D/3D convs, GRU temporal). Reports ~94% mAP on
AVA-ActiveSpeaker; "lightweight" is relative to its peers (LoCoNet/TalkNet), **not** to FFmpeg.

**Dep weight / OneDrive risk:** **HEAVY and a OneDrive hazard.** Pulls **torch**, **opencv (cv2)**,
S3FD weights, `python_speech_features`, `scenedetect`, `scipy`. Both `torch` and `cv2` are the exact
imports flagged as hanging on the synced disk. **Mitigation (required):** install the **CPU-only**
torch wheel (`pip install torch --index-url https://download.pytorch.org/whl/cpu`), put the LR-ASD
checkout + checkpoints under a **local non-OneDrive path** (e.g. `C:\models\lr-asd`), and run it as a
**one-shot subprocess** that writes a small JSON (per-frame: track_id, bbox, asd_score) — never
import torch into the long-lived agent process. We only need the JSON; torch never touches our
filtergraph.

**How it composes:** Run LR-ASD once per source angle → JSON of active-speaker tracks. Feed that to
our reframe step: the crop center = active face bbox center (smoothed); the highlight list from
Claude tells us *which spans* to cut, ASD tells us *where to point the crop* and *when to switch
angle/speaker* inside each span. Captions are unaffected (still word-level from whisper). This is the
single highest-value add — it's what makes "crop follows the active speaker" actually work instead of
a static center crop.

**Alternatives considered:** TalkNet-ASD (ACM MM 2021, MIT) — same family, heavier; LoCoNet — SOTA but
heaviest. LR-ASD is the right pick: lightest of the family, 2025, maintained, MIT, ships the demo.

---

### 2. Auto punch-in / dynamic zoom on the talker — ADD-NOW (zero new deps)
**What it does:** Periodic/triggered zoom-ins (102–115%) on the talking head to add visual rhythm,
emphasize a line, and break up a static crop. 2026 best practice: a visible change every ~0.5–1 s;
zooms placed at emphasis / audio peaks / scene changes — exactly the data we already have.

**Tool:** **No new dependency.** Pure FFmpeg `crop`+`scale` (or `zoompan` for animated push) with the
zoom amount/timing driven by *our own signals*: word timestamps (zoom on emphasized keyword),
audio RMS peaks (FFmpeg `astats`/`silencedetect`), and scene cuts from #4. Animate via the `scale`
filter with a `t`-based expression, or pre-compute keyframes and use `sendcmd`/`zoompan`.

**How it composes:** After face-tracking gives the crop window (#1), apply a second multiplier:
`zoom(t)` that pushes in on chosen beats. Trigger list = {highlight-clip start (open on a punch),
keyword timestamps from whisper, audio-peak times}. Lives entirely in the existing FFmpeg
filtergraph — no import-hang risk, deterministic, free.

---

### 3. Silence / dead-air auto-cut — ADD-NOW (no torch)
**What it does:** Detects and removes silent/dead gaps so the clip is tight (kills dead air → higher
completion %, the 2026 retention lever). Critical for raw interview footage with pauses.

**Tool:** **[auto-editor](https://pypi.org/project/auto-editor/)** — **Unlicense (public domain)**,
Python ≥3.9, wraps FFmpeg, **no torch / no ML**, "available on all major platforms" (Windows fine).
Analyzes audio loudness (and optional motion) and cuts below-threshold sections. Note: it does NOT do
transcript/filler-word detection itself and does NOT emit a bare timestamp EDL (it renders or exports
to NLE project formats), so for our pipeline prefer to use its *detection logic* or run our own
silence detection.

**Lighter alternative (recommended for our stack):** FFmpeg's own **`silencedetect`** filter →
parse the silence intervals → build a keep-list → cut with the `select`/`atrim` filters or concat.
Zero new dependency, fully inside our existing FFmpeg usage, and it composes cleanly with word
timestamps so we never cut mid-word.

**How it composes:** Run silence detection on the *highlight span* (not the whole 2 hr file — cheaper
and avoids cutting across Claude's chosen boundaries). Subtract silent intervals, then re-anchor the
whisper word timestamps to the new timeline so captions stay in sync. Do silence-cut BEFORE caption
burn-in and BEFORE reframe so the crop/zoom timing matches the final cut.

### 3b. Filler-word removal — ADD-NOW (zero new deps, we already have the data)
**What it does:** Removes "um, uh, like, you know" — we already have **word-level timestamps** from
faster-whisper, so this is nearly free: regex the filler tokens, take their `[start,end]`, add to the
silence cut-list. No new tool. Big perceived-quality jump for interview clips. (SilenceTrimmer, MIT,
exists for this but is redundant given our transcript.)

---

### 4. Scene / shot-change detection — ADD-NOW (moderate)
**What it does:** Finds hard cuts / camera-angle changes / fade points. Two uses for us:
(a) **multicam:** if our two angles are pre-edited into one file, scene detection finds the existing
cut points; (b) **b-roll / overlay timing:** detected shot boundaries are the natural, non-jarring
moments to drop a b-roll insert, an emoji pop, or a punch-in.

**Tool:** **[PySceneDetect](https://www.scenedetect.com/)** v0.6.6 (Mar 2025, actively maintained),
**BSD-3-Clause**. `ContentDetector` (HSV content), `AdaptiveDetector` (handles camera movement),
`ThresholdDetector` (fades). Exports cut points as `HH:MM:SS.nnn` ready to paste into FFmpeg.

**Dep weight / OneDrive risk:** Pulls **opencv (cv2)** + numpy — **cv2 is on the OneDrive
slow-import list.** Moderate. Mitigation: run it as a one-shot subprocess that emits a cut-list JSON;
don't keep cv2 imported. (Lighter no-cv2 fallback: FFmpeg's `select='gt(scene,0.4)'` +
`showinfo`/`metadata` to dump scene scores — less accurate but zero new dep.)

**How it composes:** Cut-list JSON feeds the b-roll/overlay scheduler and the punch-in trigger list
(#2). Combined with ASD (#1), a scene cut + active-speaker change = a clean place to switch the crop
target or insert an overlay without a jump-cut feel.

---

### 5. Emoji / keyword pop-ups, word-pop captions, zoom-on-emphasis — ADD-NOW (we already have libass)
**What it does:** The 2026 caption meta: word-by-word "karaoke" highlight, animated keyword
emphasis (scale-bounce on the punch word), and contextual emoji/keyword pop-ups beside the caption.
Text changes in rapid succession + emojis = the documented engagement driver.

**Tool:** **Already in our stack** — libass/ASS (we burn captions with it). ASS supports per-word
karaoke timing (`\k`), inline animation (`\t` transforms: scale/pos/color), and emoji glyphs (with an
emoji-capable font, e.g. Noto Color Emoji). For pop-ups that need to fly in/out we can also use
FFmpeg `drawtext`/`overlay` with `t`-based enable windows.

**How it composes:** We already have word-level timestamps → generate ASS `\k`/`\t` tags per word for
the karaoke highlight and a scale-bounce on emphasized words. For emoji/keyword pops, have **Claude**
(already the highlight brain) tag a handful of keywords per clip with an emoji + timestamp; emit them
as extra ASS events or `drawtext` overlays. The "zoom-on-emphasis" visual (#2) is triggered on the
same keyword timestamps — captions and punch-ins fire together. Pure FFmpeg, no new deps, no hang
risk. This is the cheapest "make it look pro" lever.

---

### 6. Background blur / person segmentation — ADD-LATER
**What it does:** Blur or replace the background behind the speaker for a cleaner, more "designed"
vertical (especially when the crop still shows a messy room).

**Options (ranked for our constraints):**
- **[MediaPipe Selfie / Image Segmenter](https://developers.google.com/mediapipe/solutions/vision/image_segmenter/python)**
  — **Apache 2.0**, `pip install mediapipe`. Selfie model is tiny (~454 KB, 106K params),
  **real-time on CPU**, designed for person-near-camera (our exact case). Deps: mediapipe wheel +
  numpy + opencv. **Moderate OneDrive risk** (mediapipe bundles native libs; opencv import). Best
  speed/size/license trade for us. → **the ADD-LATER pick.**
- **[rembg](https://github.com/danielgatis/rembg)** — **MIT**, U²-Net/BiRefNet via ONNXRuntime.
  CPU-slow (**3–8 s/image** → ~too slow for video frame-by-frame without GPU). Good for one-off, bad
  for clips.
- **[SAM2](https://github.com/facebookresearch/sam2)** — **Apache 2.0**, best-in-class video
  segmentation, BUT **torch + CUDA, very heavy** (38.9M–224.4M params; ~30–47 fps on an **A100**).
  On CPU + OneDrive this is a non-starter. **SKIP for now.**

**Why ADD-LATER not ADD-NOW:** background work is a polish layer, not a retention driver, and even
the light MediaPipe path adds an opencv/mediapipe import to a per-frame loop. Ship face-tracking +
captions + cuts first; add MediaPipe selfie-blur as a v2 toggle (run as subprocess writing an alpha
matte / pre-blurred frames, then `overlay` in FFmpeg).

**How it composes (when added):** MediaPipe emits a per-frame person mask → FFmpeg `alphamerge` +
`boxblur`/`gblur` on the background layer, composited under the burned captions. Runs after reframe.

---

### 7. Audio cleanup (denoise + loudness) — ADD-NOW (cheap, zero new deps)
**What it does:** Normalizes loudness across clips and knocks down hiss/room noise — interview audio
is the #1 thing that reads as "amateur." Easy win, often overlooked.
**Tool:** Pure FFmpeg: `loudnorm` (EBU R128, the streaming standard) + `afftdn` or `arnndn` (RNN
denoise). No new dependency.
**How it composes:** Apply on the audio leg of the existing filtergraph before mux. Free quality bump
on every clip.

---

### 8. Beat-synced cuts — ADD-LATER
**What it does:** Align cuts/zoom-pushes to a background music beat for that "edited" feel.
**Tool:** **librosa** (`beat_track`) — **ISC license**, but pulls numpy/scipy/**numba** (moderate
weight, numba JIT can be slow to warm). Or do it manually if we set the track's BPM.
**How it composes:** Beat timestamps merge into the punch-in/cut trigger list (#2/#4). Defer — only
matters once we add background music; for talking-head interview clips, dialogue-driven cuts (#3/#4)
matter more.

---

### 9. PyAutoFlip (saliency reframing) — SKIP (overlaps #1+#2)
**[pyautoflip](https://pypi.org/project/pyautoflip/)** (MIT) is a maintained Python port of Google's
**[AutoFlip](https://research.google/blog/autoflip-an-open-source-framework-for-intelligent-video-reframing/)**
(original is abandoned). It does saliency-aware crop to 9:16 using InsightFace + UNISAL(ONNX) +
mediapipe + PySceneDetect (~57 MB). It's a credible *generic* reframer, but for a **2-person talking
interview**, ASD-driven crop (#1) is more correct (it follows the *speaker*, not generic saliency),
and we get punch-in from #2. Skipping avoids a second face-detection stack. Keep as a fallback if
LR-ASD proves too heavy to tame on this disk.

### 10. Silero-VAD turn segmentation — ADD-LATER (cheap multicam alt)
**[Silero-VAD](https://github.com/snakers4/silero-vad)** (MIT, tiny, ONNX option = no big torch) gives
speech/no-speech intervals very cheaply. Combined with our **two camera angles**, a *poor-man's*
multicam: if each angle has one mic-dominant speaker, VAD + simple energy can pick the talking angle
without full ASD. Lighter than LR-ASD but coarser (no lip-sync, struggles on fast turns/crosstalk).
Worth it only if LR-ASD's torch/cv2 weight proves unworkable on the OneDrive disk — then VAD-based
angle switching is the lightweight fallback. (Full **pyannote** diarization is heavier and torch-bound
— not worth it here.)

---

## Recommended build order

1. **Audio cleanup (#7)** + **silence/filler cut (#3/#3b)** — pure FFmpeg + our transcript, zero new
   deps, immediate quality jump. Do first; re-anchor whisper timestamps after cutting.
2. **Punch-in/zoom (#2)** + **emoji/keyword pops & word-pop captions (#5)** — pure FFmpeg + libass we
   already have; Claude tags the keywords. Big "looks pro" lever, no hang risk.
3. **LR-ASD face-tracking (#1)** — the real prize, but **gated**: CPU-only torch wheel, checkout +
   checkpoints on a **local non-OneDrive path**, run as a one-shot subprocess → JSON. This drives both
   crop-follows-speaker and (for two angles) multicam switching.
4. **PySceneDetect (#4)** — subprocess → cut-list JSON for b-roll/overlay timing and angle-cut points.
5. **v2 polish:** MediaPipe selfie background blur (#6), beat-sync (#8) once music is in the mix.

## OneDrive-disk hang warnings (call-outs)
- **LR-ASD (#1):** torch + cv2 + S3FD — **will hang/slow-import on the synced disk.** Mandatory:
  CPU-only torch, models on `C:\models\...`, run as isolated subprocess, redirect `HF_HOME`/
  `TORCH_HOME` off OneDrive. Never import torch into the agent's long-lived process.
- **PySceneDetect (#4):** pulls **cv2** — moderate slow-import; isolate as subprocess. FFmpeg
  `select='gt(scene,..)'` is the zero-dep fallback.
- **SAM2 (#6c):** torch + CUDA, needs A100-class GPU for real-time — **SKIP**, would be unusable
  here.
- **rembg (#6b):** ONNXRuntime CPU is 3–8 s/image — too slow per-frame for video on this machine.
- **Safe (no hang risk):** auto-editor (no torch), FFmpeg `silencedetect`/`loudnorm`/`zoompan`/
  `drawtext`, libass/ASS — all already proven in our stack.

---

## Sources
- LR-ASD (2025, MIT, the face-tracking brain): https://github.com/Junhua-Liao/LR-ASD
- Light-ASD (CVPR 2023, predecessor): https://github.com/Junhua-Liao/Light-ASD
- TalkNet-ASD (ACM MM 2021): https://github.com/TaoRuijie/TalkNet-ASD
- auto-editor (Unlicense): https://pypi.org/project/auto-editor/
- PySceneDetect (BSD-3, v0.6.6 Mar 2025): https://www.scenedetect.com/ · https://github.com/Breakthrough/PySceneDetect
- MediaPipe Image Segmenter (Apache 2.0): https://developers.google.com/mediapipe/solutions/vision/image_segmenter/python
- MediaPipe Selfie Segmentation: https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/selfie_segmentation.md
- rembg (MIT): https://github.com/danielgatis/rembg
- SAM2 (Apache 2.0, torch/CUDA): https://github.com/facebookresearch/sam2
- pyautoflip (MIT) / Google AutoFlip: https://pypi.org/project/pyautoflip/ · https://research.google/blog/autoflip-an-open-source-framework-for-intelligent-video-reframing/
- Silero-VAD (MIT): https://github.com/snakers4/silero-vad
- pyannote-audio (diarization, heavier): https://github.com/pyannote/pyannote-audio
- FFmpeg burn-subtitles/libass: https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo
- Auto zoom / punch-in 2026 practice: https://www.opus.pro/blog/best-auto-zoom-in-tools
- Viral Shorts 2026 (cut cadence, length, captions): https://prapermedia.com/blog/make-viral-youtube-shorts/
