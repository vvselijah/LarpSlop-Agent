---
name: auto-clip
description: Turn one long video (10-30 min YouTube, 1-2 hr podcast/interview) into ranked 9:16 vertical shorts using the local auto-clip engine — transcribe, let Claude pick the best self-contained moments, and cut + reframe them to 1080x1920 in out/ for Elijah to review. Use when he says "clip this video", "make shorts/reels from this", "turn this podcast into clips", "auto-clip", "find the best moments", "cut this into shorts", or hands over a long video to repurpose. Stops at files in out/ — NEVER publishes.
---

# Auto-Clip — long video → vertical shorts (local)

Drives the `auto-clip/` engine (entry scripts at `C:\Users\elija\OneDrive\Desktop\ai agent team\auto-clip\`).
**Reuse-first:** ~70% already existed in the hub + `..\abc wrap\`; the engine adds only transcribe,
the highlight "brain", and 9:16 reframe. Full design + caveats: `docs/plans/2026-06-13-auto-clip-pipeline.md`.
The engine **stops at files in `out/`** and prints a manifest — it NEVER publishes (CLAUDE.md rule 1).

## When to run which path
- **Interactive (default, this skill):** Claude is the highlight selector — `--provider agent`. No API key,
  no Ollama, no install. Best quality, and it's free.
- **Unattended/scheduled:** `--provider anthropic` (needs `ANTHROPIC_API_KEY`) or `--provider ollama`
  (needs local Ollama). Only wire these when chaining auto-clip into `Daily Agent Refresh.bat`.

## Steps (run from the `auto-clip/` folder; use PowerShell — `python` is not on the Bash PATH here)

1. **Locate the source video** Elijah names (a file path, or something already in the tree). Confirm it exists.
   Probe it if useful (`mcp__ffmpeg__get-video-info`). Note its aspect ratio — see step 4.

2. **Transcribe** to word-level JSON:
   `python transcribe.py <video> [--model base.en] [--device cpu]`
   → writes `data/<stem>.transcript.json`. CPU/int8 by default (≈12x realtime). Once torch cu128 + cuDNN9
   are installed, add `--device cuda` for a big speedup (GPU fix is a separate, Elijah-gated multi-GB install).

3. **Select highlights — Claude IS the brain** (two-step agent provider, keeps seg→time mapping deterministic):
   - `python highlight.py data/<stem>.transcript.json --provider agent --n 6`
     → writes `data/<stem>.agent-prompt.json` (the numbered transcript + the task) and stops.
   - **Read that brief and make a genuine editorial selection.** Each clip MUST open on a scroll-stopping
     hook, contain exactly ONE complete idea, and stand alone (prefer 20–60s). Favor concrete payoffs —
     numbers, secrets, bold claims. **Lean into Elijah's proven niches** (read `team/stats.md`): Money/Finance
     is his runaway view-leader and AI/Tech is his best save-rate — rank money/AI moments highest.
   - Write your picks to `data/<stem>.picks.json` as a JSON array, each item exactly:
     `{"start_seg": int, "end_seg": int (inclusive), "title": str, "hook": str, "score": 0-100, "reason": str}`.
   - `python highlight.py data/<stem>.transcript.json --provider agent --from-picks data/<stem>.picks.json`
     → validates, snaps to segment boundaries, sorts by score, writes `data/<stem>.highlights.json`.

4. **Reframe + cut** to 9:16 and deliver:
   `python reframe.py <video> data/<stem>.highlights.json [--encoder libx264]`
   → writes `out/<stem>_clip<NN>.mp4` (1080×1920, H.264, AAC) + `out/<stem>.manifest.json`.
   - If the source is already ~9:16 it trims + encodes. If it's wider (16:9 podcast/YouTube) it **center-crops**
     to 9:16 — that's the v1 fallback. **Face/subject-tracking reframe is the documented v2 enhancement**
     (OpenCV/MediaPipe → smoothed crop track); flag it when a wide source would clip a speaker off-center.
   - Swap `--encoder h264_nvenc` only after the GPU (torch cu128) is enabled.

5. **Caption (recommended) — burn word-timed captions:**
   `python caption.py data/<stem>.transcript.json data/<stem>.highlights.json [--group 3] [--marginv 620] [--no-caps]`
   → writes `out/<clip>_cap.mp4` (pure FFmpeg/libass: big bold, lower-third, ~3 words/group; originals kept).
   Needs the transcript's word-level `words[]`. For the premium animated house style instead, use the
   `caption-engine` skill (Remotion, heavier); see `viral-shortform-2026` for hook/caption polish.

6. **Report the manifest** to Elijah: per clip — rank, file, title, hook, duration. These are review files in
   `out/`, NOT posted. Offer the obvious next steps (below) but do not act on them without his go-ahead.

## Next layer (offer, don't auto-run)
- **Captions:** built-in via `caption.py` (step 5, pure-FFmpeg). For the premium animated house style instead,
  wire the word-level transcript into the `caption-engine` skill; see `viral-shortform-2026` for polish.
- **B-roll / platform export:** `broll-inserter` + `platform-exporter` for finishing.
- **Carousel cross-format:** feed a top clip's transcript to the `carousel-builder` skill for a saveable swipe post.

## Rules (CLAUDE.md)
- **Rule 1 — never publish/post without explicit per-action confirmation.** The engine stops at `out/`.
  Any future IG-API publish path must be **voice-only / original-audio** (rule 4) with a
  `get_content_publishing_limit` pre-flight; the per-action confirmation is always Elijah's click.
- **Rule 3 — secrets only in env vars**, never written to files (OneDrive-synced). The agent provider needs none.
- **First engine with third-party deps** (`faster-whisper`, FFmpeg) — `auto-clip/requirements.txt` is the source
  of truth; the agent highlight path itself needs nothing beyond a transcript.
- **Rule 7 — after a real repurposing run, append one dated learning to `team/memory.md`** (which source, which
  niches ranked highest, anything about clip quality).
