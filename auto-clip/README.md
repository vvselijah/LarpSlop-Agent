# auto-clip — long video → vertical shorts (local)

Turns one long video (10–30 min YouTube, 1–2 hr podcast/interview) into ranked 9:16 shorts.
**Reuse-first:** ~70% already exists in the hub + `..\abc wrap\`; this engine adds only the 3
genuinely-missing pieces. Full design + caveats: `docs/plans/2026-06-13-auto-clip-pipeline.md`.

## Status (2026-06-13)
- ✅ **`transcribe.py`** — local word-level transcription (faster-whisper). **Built + tested** (77 seg / 1182 words, ~12x realtime CPU).
- ✅ **`highlight.py`** — moment selector → ranked `{rank,start,end,title,hook,score,reason}`. **Built + tested.** Three providers:
  `anthropic` (needs `ANTHROPIC_API_KEY`), `ollama` (local), and **`agent`** — the Claude Code agent IS the selector, **no key/install needed** (the default for interactive runs; see the `auto-clip` skill).
- ✅ **`reframe.py`** — 9:16 cut + reframe. **Built + tested** (6/6 clips, 1080×1920 H.264/AAC). Already-9:16 → trim+encode; wider → center-crop (v1). **Face/subject-tracking reframe is the v2 enhancement.**
- ✅ **`caption.py`** — burn word-timed captions (pure FFmpeg/libass; big bold, lower-third, ~3 words/group, all-caps). **Built + tested** (6/6 `_cap.mp4`; captions verified on-frame). Premium animated house style via `caption-engine` is the optional alternative.
- ✅ **`auto-clip` skill** (`.claude/skills/auto-clip/`) — orchestrates the full interactive pipeline (transcribe → agent-highlight → reframe → **caption** → manifest).
- ⏳ **Remaining:** face-track reframe (v2, OpenCV/MediaPipe), GPU torch-cu128 (Elijah-gated multi-GB; near-instant transcribe + `h264_nvenc`), `Daily Agent Refresh.bat` wiring (on-demand first).

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
