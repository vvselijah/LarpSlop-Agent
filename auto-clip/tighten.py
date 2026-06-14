"""
auto-clip/tighten.py -- remove dead air + disfluencies from a clip window, using the word-level
transcript (we have exact word times, so this is cleaner than FFmpeg silencedetect).

Trims any inter-word silence longer than --max-gap down to --max-gap, and drops filler/disfluency
words (conservative default: um/uh/er/... NOT like/so/you-know, which are too risky). Emits:
  1) a tightened video clip, and
  2) a 0-based remapped transcript so caption.py --clip can caption the tightened clip IN SYNC.

Pipeline: highlight -> tighten (optional) -> caption.py --clip ...  (reframe/facetrack can run on the
tightened clip too if it's wide). Use when a clip drags. Stops at out/ (CLAUDE.md rule 1).

Usage:
  python tighten.py <source-video> --transcript data/<stem>.transcript.json --start S --end E
                    [--name N] [--max-gap 0.35] [--lead 0.1] [--fillers um,uh,er,...] [--encoder libx264]
Writes:
  out/<name>_tight.mp4
  data/<name>.tight.transcript.json   ({media, words:[{word,start,end}]}, 0-based)
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DEFAULT_FILLERS = "um,umm,uh,uhh,uhm,er,erm,ah,mhm,hmm,uhhuh"


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def norm(w):
    return re.sub(r"[^a-z]", "", w.lower())


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        log("FATAL: usage: python tighten.py <source-video> --transcript <t.json> --start S --end E "
            "[--name N] [--max-gap 0.35] [--fillers um,uh,...]")
        sys.exit(1)

    src = Path(args[0]).resolve()
    if not src.exists():
        log(f"FATAL: source not found: {src}")
        sys.exit(1)

    def opt(f, d):
        return args[args.index(f) + 1] if f in args else d

    tpath = opt("--transcript", None)
    if not tpath:
        log("FATAL: --transcript data/<stem>.transcript.json is required")
        sys.exit(1)
    tpath = Path(tpath).resolve()
    S = float(opt("--start", "0"))
    E = float(opt("--end", "0"))
    if E <= S:
        log("FATAL: need --end > --start")
        sys.exit(1)
    name = opt("--name", src.stem.replace(" ", "_"))
    max_gap = float(opt("--max-gap", "0.35"))
    lead = float(opt("--lead", "0.1"))
    fillers = {norm(f) for f in opt("--fillers", DEFAULT_FILLERS).split(",")}
    encoder = opt("--encoder", "libx264")
    out_dir = BASE / opt("--out", "out")
    out_dir.mkdir(parents=True, exist_ok=True)

    all_words = json.loads(tpath.read_text(encoding="utf-8")).get("words") or []
    win = [w for w in all_words if float(w["start"]) >= S - 1e-3 and float(w["start"]) < E]
    kept = [(float(w["start"]) - S, float(w["end"]) - S, w["word"]) for w in win]
    if not kept:
        log(f"FATAL: no words in [{S},{E}]")
        sys.exit(1)

    # Build keep-intervals (window-time): drop fillers; trim silences > max_gap down to max_gap.
    intervals, prev_end, dropped = [], None, 0
    for (w0, w1, word) in kept:
        if norm(word) in fillers:
            dropped += 1
            continue
        if prev_end is None:
            a = max(0.0, w0 - lead)
        else:
            gap = w0 - prev_end
            a = prev_end if gap <= max_gap else max(prev_end, w0 - max_gap)
        intervals.append((a, w1))
        prev_end = w1
    # merge adjacent/overlapping
    intervals.sort()
    merged = []
    for (a, b) in intervals:
        if merged and a <= merged[-1][1] + 1e-3:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))

    window = E - S
    keep_dur = sum(b - a for a, b in merged)
    log(f"window {window:.1f}s -> tightened {keep_dur:.1f}s (removed {window-keep_dur:.1f}s; "
        f"{dropped} filler word(s), {len(merged)} keep-segments)")

    # remap kept words to the tightened 0-based timeline
    cum, acc = [], 0.0
    for (a, b) in merged:
        cum.append((a, b, acc))
        acc += b - a

    def to_new(t):
        for (a, b, base) in cum:
            if a - 1e-3 <= t <= b + 1e-3:
                return base + (t - a)
        return None

    new_words = []
    for (w0, w1, word) in kept:
        if norm(word) in fillers:
            continue
        ns, ne = to_new(w0), to_new(w1)
        if ns is None or ne is None:
            continue
        new_words.append({"word": word, "start": round(ns, 3), "end": round(max(ne, ns + 0.04), 3)})

    dst = out_dir / f"{name}_tight.mp4"
    sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for (a, b) in merged)
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(S), "-to", str(E), "-i", str(src),
        "-vf", f"select='{sel}',setpts=N/FRAME_RATE/TB", "-af", f"aselect='{sel}',asetpts=N/SR/TB",
        "-c:v", encoder, "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", str(dst),
    ]
    log(f"rendering -> {dst.name}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        tail = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error"
        log(f"FAILED: {tail}")
        sys.exit(1)

    twords = out_dir.parent / "data" / f"{name}.tight.transcript.json"
    twords.write_text(json.dumps({"media": str(dst), "words": new_words}, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    log(f"DONE -> {dst}  + remapped transcript {twords.name} ({len(new_words)} words). "
        f"Caption it: python caption.py {twords.name} --clip {dst.name}. NOT published (rule 1).")


if __name__ == "__main__":
    main()
