"""
auto-clip/caption.py -- burn word-timed captions onto the 9:16 clips (pure FFmpeg/libass, no Remotion).

Reads the word-level transcript + the highlights, slices the words for each clip's time window, offsets
them to the clip's own 0-based timeline, builds a styled ASS subtitle (punchy: big bold, thick outline,
lower-third, ~3 words per group with a quick fade), and burns it onto the matching rendered clip. Pure
FFmpeg/libass keeps us off Remotion's ~10GB/bundle disk blowup (per the auto-clip PLAN). Stops at out/.

Clips are matched by GLOB (out/*_clip<NN>.mp4), because reframe.py names them with the SOURCE-video stem
while the transcript/highlights use the audio stem -- the highlights rank is the reliable link.

Usage:
  python caption.py data/<stem>.transcript.json data/<stem>.highlights.json
                    [--in out] [--group 3] [--fontsize 96] [--marginv 620]
                    [--font Arial] [--no-caps] [--encoder libx264]
Writes:
  out/<clip-stem>_cap.mp4   (one per existing out/*_clip<NN>.mp4; originals untouched)
"""
import glob
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


def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"  # H:MM:SS.cc


def ass_header(font, fontsize, marginv):
    # Alignment 2 = bottom-center; MarginV lifts it into the lower third (above the IG UI).
    # Colours are &HAABBGGRR: white fill, black outline. Bold on, thick outline + shadow for punch.
    return (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "WrapStyle: 2\n"
        "ScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{font},{fontsize},&H00FFFFFF,&H000000FF,&H00000000,&H64000000,"
        f"-1,0,0,0,100,100,0,0,1,6,3,2,60,60,{marginv},1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )


def esc(text):
    return text.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", " ").strip()


def build_ass(words, group, font, fontsize, marginv, caps):
    """words: [{word,start_off,end_off}] already offset to clip-0. Returns ASS file text."""
    groups = [words[i:i + group] for i in range(0, len(words), group)]
    out = [ass_header(font, fontsize, marginv)]
    for gi, grp in enumerate(groups):
        txt = " ".join(w["word"].strip() for w in grp).strip()
        if not txt:
            continue
        if caps:
            txt = txt.upper()
        start = grp[0]["start_off"]
        end = groups[gi + 1][0]["start_off"] if gi + 1 < len(groups) else grp[-1]["end_off"]
        end = max(end, start + 0.3)
        out.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,"
            f"{{\\fad(50,30)}}{esc(txt)}\n"
        )
    return "".join(out)


def find_clip(out_dir, rank):
    hits = sorted(glob.glob(str(out_dir / f"*_clip{rank:02d}.mp4")))
    hits = [h for h in hits if not h.endswith("_cap.mp4")]
    return Path(hits[0]) if hits else None


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        log("FATAL: usage: python caption.py data/<stem>.transcript.json data/<stem>.highlights.json "
            "[--in out] [--group 3] [--fontsize 96] [--marginv 620] [--font Arial] [--no-caps]")
        sys.exit(1)

    tpath = Path(args[0]).resolve()
    hpath = Path(args[1]).resolve()
    for p in (tpath, hpath):
        if not p.exists():
            log(f"FATAL: not found: {p}")
            sys.exit(1)

    def opt(flag, d):
        return args[args.index(flag) + 1] if flag in args else d

    out_dir = BASE / opt("--in", "out")
    group = int(opt("--group", "3"))
    fontsize = int(opt("--fontsize", "96"))
    marginv = int(opt("--marginv", "620"))
    font = opt("--font", "Arial")
    caps = "--no-caps" not in args
    encoder = opt("--encoder", "libx264")

    tdata = json.loads(tpath.read_text(encoding="utf-8"))
    words_all = tdata.get("words") or []
    if not words_all:
        log("FATAL: transcript has no word-level 'words' array -- re-run transcribe.py with word timestamps")
        sys.exit(1)
    clips = json.loads(hpath.read_text(encoding="utf-8"))

    done = 0
    for c in clips:
        rank, cs, ce = c["rank"], float(c["start"]), float(c["end"])
        src = find_clip(out_dir, rank)
        if not src:
            log(f"clip #{rank}: no rendered out/*_clip{rank:02d}.mp4 -- run reframe.py first; skipping")
            continue
        # slice words in [cs, ce), offset to clip-0
        ws = []
        for w in words_all:
            st = float(w["start"])
            if st >= cs - 0.15 and st < ce:
                ws.append({"word": w["word"], "start_off": st - cs, "end_off": float(w["end"]) - cs})
        if not ws:
            log(f"clip #{rank}: no words in [{cs:.0f},{ce:.0f}]s; skipping")
            continue

        ass_text = build_ass(ws, group, font, fontsize, marginv, caps)
        ass_path = out_dir / f"{src.stem}.ass"
        ass_path.write_text(ass_text, encoding="utf-8")

        dst = out_dir / f"{src.stem}_cap.mp4"
        # cwd=out_dir + relative paths sidesteps libass's Windows colon-escaping pain.
        cmd = [
            "ffmpeg", "-y", "-i", src.name, "-vf", f"ass={ass_path.name}",
            "-c:v", encoder, "-preset", "veryfast", "-crf", "20", "-c:a", "copy", dst.name,
        ]
        log(f"clip #{rank}: burning {len(ws)} words -> {dst.name}")
        r = subprocess.run(cmd, cwd=str(out_dir), capture_output=True, text=True)
        if r.returncode != 0:
            tail = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error"
            log(f"  FAILED: {tail}")
            continue
        done += 1

    log(f"DONE -- {done}/{len(clips)} captioned clips in {out_dir} (originals kept). NOT published (rule 1).")


if __name__ == "__main__":
    main()
