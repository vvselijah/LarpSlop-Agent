# auto-clip — long video → vertical shorts (local)

Turns one long video (10–30 min YouTube, 1–2 hr podcast/interview) into ranked 9:16 shorts.
**Reuse-first:** ~70% already exists in the hub + `..\abc wrap\`; this engine adds only the 3
genuinely-missing pieces. Full design + caveats: `docs/plans/2026-06-13-auto-clip-pipeline.md`.

## Status (2026-06-13)
- ✅ **`transcribe.py`** — local word-level transcription (faster-whisper). **Built + tested.**
- ⏳ `highlight.py` — LLM moment selector → ranked `{start,end,title,hook,score}` (per PLAN; needs an LLM key or local Ollama).
- ⏳ `reframe.py` — face/subject-aware 9:16 auto-reframe (OpenCV/MediaPipe track → FFmpeg crop or the existing PodcastEdit transform).
- ⏳ `sim`/orchestrator + `Daily Agent Refresh.bat` wiring — after the above validate.

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
