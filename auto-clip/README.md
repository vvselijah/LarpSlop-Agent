# auto-clip — long video → vertical shorts (local)

Turns one long video (10–30 min YouTube, 1–2 hr podcast/interview) into ranked 9:16 shorts.
**Reuse-first:** ~70% already exists in the hub + `..\abc wrap\`; this engine adds only the 3
genuinely-missing pieces. Full design + caveats: `docs/plans/2026-06-13-auto-clip-pipeline.md`.

## Status (2026-06-13)
- ✅ **`transcribe.py`** — local word-level transcription (faster-whisper). **Built + tested** (77 seg / 1182 words, ~12x realtime CPU).
- ✅ **`highlight.py`** — moment selector → ranked `{rank,start,end,title,hook,score,reason}`. **Built + tested.** Three providers:
  `anthropic` (needs `ANTHROPIC_API_KEY`), `ollama` (local), and **`agent`** — the Claude Code agent IS the selector, **no key/install needed** (the default for interactive runs; see the `auto-clip` skill).
- ✅ **`reframe.py`** — simple 9:16 cut + reframe. **Built + tested** (6/6 clips, 1080×1920 H.264/AAC). Already-9:16 → trim+encode; single-subject wide → center-crop.
- ✅ **`facetrack.py`** — face-tracking 9:16 reframe for WIDE/multi-person sources (interviews). OpenCV Haar (frontal+profile, bundled — no download) **detection only**; locks onto one chosen speaker (largest/left/right, lock-and-hold through profile turns); FFmpeg `sendcmd` crop (audio kept). **Built + tested** on the Elijah/Derwin interview — both speakers, framing verified on-frame. v2 = LR-ASD active-speaker auto-switch.
- ✅ **`caption.py`** — burn word-timed captions (pure FFmpeg/libass): **word-pop** karaoke (active word highlighted yellow) or `block` style, big bold lower-third, all-caps, **+ audio cleanup** (loudnorm/afftdn, on by default). **Built + tested** (6/6 `_cap.mp4`; word-pop highlight tracking speech + cleaned audio verified). Premium animated house style via `caption-engine` is the optional alternative.
- ✅ **`auto-clip` skill** (`.claude/skills/auto-clip/`) — orchestrates the full interactive pipeline (transcribe → agent-highlight → reframe → **caption** → manifest).
- ⏳ **Remaining (roadmap in `docs/plans/2026-06-14-interview-clip-enhancements-research.md`):** pure-FFmpeg silence/filler cut + audio cleanup (loudnorm/afftdn) + punch-in & emoji/word-pop captions (DO FIRST — no new deps); **LR-ASD active-speaker auto-switch + multicam** (the real v2 brain — torch, gated, keep models OFF OneDrive); PySceneDetect shot cuts; background blur (MediaPipe Selfie, add-later); GPU torch-cu128 (Elijah-gated); `Daily Agent Refresh.bat` wiring.

## The 3 new pieces (everything else is reused)
1. **Transcribe** (done) — word-level JSON the caption-engine + highlight selector consume.
2. **Highlight select** — the true missing "brain": rank transcript spans for standalone-short quality.
3. **Reframe** — track the speaker, crop to 9:16 (the existing reframe is geometry-only; tracking is what's new).

Reused (do NOT rebuild): caption-engine, broll-inserter, platform-exporter, `build_cutlist.js`
(editorial brain) + `PodcastEdit.tsx` (crop comp) from `..\abc wrap\`, and the FFmpeg 8.1 MCP for probe/audio.

## Transcribe usage
```
python transcribe.py <media-file> [--model base.en] [--device cpu] [--lang en]
```
Writes `data/<stem>.transcript.json` (`text`, `segments[]`, word-level `words[]`).
CPU/int8 by default; once torch cu128 + cuDNN9 are installed, add `--device cuda` for a big speedup.

## Hard rules (CLAUDE.md)
Engine **stops at files in `out/`** and prints a manifest — it NEVER publishes. Any future IG-API
publish path must be voice-only/original-audio (rule 4) with `get_content_publishing_limit` pre-flight.
