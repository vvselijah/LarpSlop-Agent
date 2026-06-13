"""
auto-clip/transcribe.py -- local word-level transcription for the auto-clip pipeline.

Wraps faster-whisper to turn a video/audio file into a flat, time-coded JSON transcript
(segments + word-level timestamps + full text) that the highlight selector (highlight.py)
and the existing caption-engine skill consume. Runs FULLY LOCALLY -- no API key, no upload.

CPU/int8 by default. Once the torch cu128 build + cuDNN9 are installed (see
docs/plans/2026-06-13-auto-clip-pipeline.md), pass --device cuda for a large speedup;
compute_type auto-bumps to float16 on cuda.

Usage:
  python transcribe.py <media-file> [--model base.en] [--device cpu] [--compute int8] [--lang en]
  python transcribe.py ../source.mp4
  python transcribe.py ../audio.wav --model small.en

Writes:
  data/<stem>.transcript.json
    { media, model, device, language, duration, transcribed_in_s, realtime_factor,
      text, segments:[{start,end,text}], words:[{word,start,end}] }
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:  # Windows cp1252 console chokes on emoji/smart-quotes/arrows
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def main():
    args = sys.argv[1:]
    model_name, device, compute, lang, media = "base.en", "cpu", "int8", "en", None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--model" and i + 1 < len(args):
            model_name = args[i + 1]; i += 2
        elif a == "--device" and i + 1 < len(args):
            device = args[i + 1]; i += 2
        elif a == "--compute" and i + 1 < len(args):
            compute = args[i + 1]; i += 2
        elif a == "--lang" and i + 1 < len(args):
            lang = args[i + 1]; i += 2
        else:
            media = a; i += 1

    if not media:
        log("FATAL: no media file given. Usage: python transcribe.py <media-file> [--model base.en]")
        sys.exit(1)

    media_path = Path(media).resolve()
    if not media_path.exists():
        log(f"FATAL: media not found: {media_path}")
        sys.exit(1)

    if device == "cuda" and compute == "int8":
        compute = "float16"  # int8 is a CPU path; cuda wants float16

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        log("FATAL: faster-whisper not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    log(f"loading model '{model_name}' ({device}/{compute}) ...")
    model = WhisperModel(model_name, device=device, compute_type=compute)

    log(f"transcribing {media_path.name} ...")
    t0 = time.time()
    seg_iter, info = model.transcribe(
        str(media_path), beam_size=5, vad_filter=True, word_timestamps=True, language=lang
    )

    segments, words, full = [], [], []
    for s in seg_iter:
        text = s.text.strip()
        segments.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": text})
        full.append(text)
        for w in (s.words or []):
            words.append({"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
        log(f"  [{s.start:6.1f}s] {text[:72]}")

    elapsed = time.time() - t0
    out = {
        "media": str(media_path),
        "model": model_name,
        "device": device,
        "language": info.language,
        "duration": round(info.duration, 3),
        "transcribed_in_s": round(elapsed, 1),
        "realtime_factor": round(info.duration / elapsed, 1) if elapsed else None,
        "text": " ".join(full).strip(),
        "segments": segments,
        "words": words,
    }

    DATA.mkdir(exist_ok=True)
    out_path = DATA / f"{media_path.stem}.transcript.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    log(
        f"wrote {out_path}  ({len(segments)} segments, {len(words)} words, "
        f"{info.duration:.0f}s audio, {out['realtime_factor']}x realtime)"
    )


if __name__ == "__main__":
    main()
