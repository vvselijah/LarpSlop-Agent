"""
auto-clip/reframe.py -- cut highlight windows out of the source video and deliver 9:16 shorts.

Takes the source VIDEO + a highlights.json (from highlight.py) and writes one MP4 per clip to out/.
- If the source is already ~9:16 it trims + re-encodes to H.264 (IG/TikTok friendly).
- If the source is wider, it center-crops to 9:16. (FACE/subject TRACKING is the planned enhancement --
  see docs/plans/2026-06-13-auto-clip-pipeline.md; center-crop is the v1 fallback.)
Uses the system ffmpeg (the hub's FFmpeg 8.1 build). Swap --encoder h264_nvenc once the GPU is enabled.

ENGINE EXIT RULE (CLAUDE.md rule 1): stops at files in out/ and prints a manifest. NEVER publishes.

Usage:
  python reframe.py <source-video> data/<stem>.highlights.json [--out out] [--encoder libx264]
Writes:
  out/<stem>_clip<NN>.mp4  +  out/<stem>.manifest.json
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:  # Windows cp1252 console chokes on emoji/smart-quotes/arrows
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def probe_wh(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        capture_output=True, text=True,
    )
    w, h = r.stdout.strip().split("x")
    return int(w), int(h)


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        log("FATAL: usage: python reframe.py <source-video> data/<stem>.highlights.json [--out out] [--encoder libx264]")
        sys.exit(1)

    src = Path(args[0]).resolve()
    hl = Path(args[1]).resolve()

    def opt(f, d):
        return args[args.index(f) + 1] if f in args else d

    out_dir = BASE / opt("--out", "out")
    out_dir.mkdir(parents=True, exist_ok=True)
    encoder = opt("--encoder", "libx264")

    if not src.exists():
        log(f"FATAL: source not found: {src}")
        sys.exit(1)
    if not hl.exists():
        log(f"FATAL: highlights not found: {hl}")
        sys.exit(1)

    w, h = probe_wh(src)
    if abs(w / h - 9 / 16) < 0.01:
        vf = "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
        note = "already 9:16 (trim + encode)"
    else:
        vf = "crop='min(iw,ih*9/16)':ih:(iw-min(iw,ih*9/16))/2:0,scale=1080:1920"
        note = "center-crop to 9:16 (v1; face-track is the enhancement)"
    log(f"source {w}x{h} -> {note}")

    clips = json.loads(hl.read_text(encoding="utf-8"))
    manifest = []
    for c in clips:
        name = f"{src.stem}_clip{c['rank']:02d}.mp4"
        dst = out_dir / name
        cmd = [
            "ffmpeg", "-y", "-ss", str(c["start"]), "-to", str(c["end"]), "-i", str(src),
            "-vf", vf, "-c:v", encoder, "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(dst),
        ]
        log(f"clip #{c['rank']} [{c['start']:.0f}-{c['end']:.0f}s] -> {name}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            tail = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error"
            log(f"  FAILED: {tail}")
            continue
        manifest.append({
            "rank": c["rank"], "file": str(dst), "title": c["title"],
            "hook": c["hook"], "duration": c["duration"],
        })

    mpath = out_dir / f"{src.stem}.manifest.json"
    mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"DONE -- {len(manifest)}/{len(clips)} clips written to {out_dir}")
    log("MANIFEST (review only -- NOT published, per CLAUDE.md rule 1):")
    for m in manifest:
        log(f"  #{m['rank']}  {Path(m['file']).name}  -- {m['title']}")


if __name__ == "__main__":
    main()
