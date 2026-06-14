"""
auto-clip/caption.py -- burn word-timed captions onto the 9:16 clips (pure FFmpeg/libass, no Remotion).

Reads the word-level transcript + the highlights, slices the words for each clip's time window, offsets
them to the clip's 0-based timeline, builds a styled ASS subtitle, and burns it onto the matching
rendered clip. Pure FFmpeg/libass keeps us off Remotion's ~10GB/bundle disk blowup. Stops at out/.

Styles:
  word-pop (default) -- karaoke: ~3 words on screen, the CURRENTLY-SPOKEN word highlighted (bright colour).
  block              -- the older look: a word-group shown together with a quick fade.

Also does **audio cleanup** on the final render (loudnorm + gentle afftdn) -- the biggest amateur-vs-pro
tell -- on by default; pass --no-clean-audio to copy the audio untouched.

Two modes:
  batch (default) -- caption every out/*_clip<NN>.mp4 from a highlights file (clips matched by GLOB,
                     since reframe names them with the SOURCE stem while the transcript uses the audio stem).
  --clip <file>   -- caption ONE explicit clip whose transcript words are already 0-based (e.g. a
                     tighten.py output). Pass the remapped transcript as the first arg; no highlights needed.

Usage:
  python caption.py data/<stem>.transcript.json data/<stem>.highlights.json [options]
  python caption.py data/<name>.tight.transcript.json --clip out/<name>_tight.mp4 [options]
Options:
  [--in out] [--style word-pop|block] [--group 3] [--fontsize 96] [--marginv 620]
  [--font Arial] [--hi 00FFFF] [--no-caps] [--no-clean-audio] [--encoder libx264]
Writes:
  out/<clip-stem>_cap.mp4
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
    return f"{h}:{m:02d}:{t % 60:05.2f}"  # H:MM:SS.cc


def ass_header(font, fontsize, marginv):
    return (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n"
        "WrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
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


def _word(w, caps):
    s = w["word"].strip()
    return esc(s.upper() if caps else s)


def _sanitize(words):
    """Sort by start + force monotonic non-decreasing starts (whisper word times can slightly overlap),
    so caption events end exactly at the next word's start and never overlap/stack."""
    ws = sorted(words, key=lambda w: w["start_off"])
    prev = -1.0
    for w in ws:
        if w["start_off"] < prev:
            w["start_off"] = prev
        prev = w["start_off"]
    return ws


def build_block(words, group, caps):
    words = _sanitize(words)
    groups = [words[i:i + group] for i in range(0, len(words), group)]
    rows = []
    for gi, grp in enumerate(groups):
        txt = " ".join(_word(w, caps) for w in grp).strip()
        if not txt:
            continue
        start = grp[0]["start_off"]
        end = groups[gi + 1][0]["start_off"] if gi + 1 < len(groups) else max(grp[-1]["end_off"], start + 0.3)
        if end > start + 1e-3:
            rows.append((start, end, "{\\fad(50,30)}" + txt))
    return rows


def build_wordpop(words, group, caps, hi):
    """~`group` words on screen; the active (currently-spoken) word recoloured. Events = [start, next-start]
    so they never overlap; zero-width events (words sharing a start) are skipped."""
    words = _sanitize(words)
    groups = [words[i:i + group] for i in range(0, len(words), group)]
    flat = [(gi, wi, grp, w) for gi, grp in enumerate(groups) for wi, w in enumerate(grp)]
    rows = []
    for k, (gi, wi, grp, w) in enumerate(flat):
        start = w["start_off"]
        end = flat[k + 1][3]["start_off"] if k + 1 < len(flat) else max(w["end_off"], start + 0.3)
        if end <= start + 1e-3:
            continue
        parts = [f"{{\\c&H{hi}&}}{_word(gw, caps)}{{\\r}}" if j == wi else _word(gw, caps)
                 for j, gw in enumerate(grp)]
        fade = "{\\fad(60,0)}" if wi == 0 else ""
        rows.append((start, end, fade + " ".join(parts)))
    return rows


def build_ass(words, p):
    rows = (build_wordpop(words, p["group"], p["caps"], p["hi"]) if p["style"] == "word-pop"
            else build_block(words, p["group"], p["caps"]))
    out = [ass_header(p["font"], p["fontsize"], p["marginv"])]
    for (start, end, text) in rows:
        out.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{text}\n")
    return "".join(out)


def render(src, ws, out_dir, p):
    """Burn captions onto one clip file `src` using clip-local words `ws`. Returns True on success."""
    ass_path = out_dir / f"{src.stem}.ass"
    ass_path.write_text(build_ass(ws, p), encoding="utf-8")
    dst = out_dir / f"{src.stem}_cap.mp4"
    src_arg = src.name if src.parent == out_dir else str(src)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", src_arg,
           "-vf", f"ass={ass_path.name}", "-c:v", p["encoder"], "-preset", "veryfast", "-crf", "20"] \
        + p["audio"] + ["-movflags", "+faststart", dst.name]
    r = subprocess.run(cmd, cwd=str(out_dir), capture_output=True, text=True)
    if r.returncode != 0:
        tail = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error"
        log(f"  FAILED: {tail}")
        return False
    return True


def find_clip(out_dir, rank):
    hits = sorted(h for h in glob.glob(str(out_dir / f"*_clip{rank:02d}.mp4")) if not h.endswith("_cap.mp4"))
    return Path(hits[0]) if hits else None


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        log("FATAL: usage: python caption.py <transcript.json> [<highlights.json> | --clip <file>] [options]")
        sys.exit(1)
    tpath = Path(args[0]).resolve()
    if not tpath.exists():
        log(f"FATAL: transcript not found: {tpath}")
        sys.exit(1)

    def opt(flag, d):
        return args[args.index(flag) + 1] if flag in args else d

    out_dir = BASE / opt("--in", "out")
    p = {
        "style": opt("--style", "word-pop"), "group": int(opt("--group", "3")),
        "fontsize": int(opt("--fontsize", "96")), "marginv": int(opt("--marginv", "620")),
        "font": opt("--font", "Arial"), "hi": opt("--hi", "00FFFF"),
        "caps": "--no-caps" not in args, "encoder": opt("--encoder", "libx264"),
    }
    clean = "--no-clean-audio" not in args
    p["audio"] = (["-af", "loudnorm=I=-16:TP=-1.5:LRA=11,afftdn=nf=-20", "-c:a", "aac", "-b:a", "160k"]
                  if clean else ["-c:a", "copy"])

    words_all = json.loads(tpath.read_text(encoding="utf-8")).get("words") or []
    if not words_all:
        log("FATAL: transcript has no word-level 'words' array")
        sys.exit(1)

    # --- single explicit clip (e.g. a tighten.py output; words already 0-based) ---
    clip = opt("--clip", None)
    if clip:
        if Path(clip).is_absolute():
            src = Path(clip).resolve()
        else:  # try as-given (cwd-relative), then out_dir/<as-given>, then out_dir/<basename>
            cands = [Path(clip).resolve(), (out_dir / clip).resolve(), (out_dir / Path(clip).name).resolve()]
            src = next((c for c in cands if c.exists()), cands[0])
        if not src.exists():
            log(f"FATAL: --clip not found: {src}")
            sys.exit(1)
        ws = [{"word": w["word"], "start_off": float(w["start"]), "end_off": float(w["end"])} for w in words_all]
        log(f"--clip {src.name}: {p['style']} captions, {len(ws)} words, clean_audio={clean}")
        ok = render(src, ws, out_dir, p)
        log(f"{'DONE -- captioned ' + src.stem + '_cap.mp4' if ok else 'FAILED'}. NOT published (rule 1).")
        sys.exit(0 if ok else 1)

    # --- batch over highlights ---
    if len(args) < 2 or args[1].startswith("--"):
        log("FATAL: need a highlights.json (or use --clip <file>)")
        sys.exit(1)
    hpath = Path(args[1]).resolve()
    if not hpath.exists():
        log(f"FATAL: highlights not found: {hpath}")
        sys.exit(1)
    clips = json.loads(hpath.read_text(encoding="utf-8"))

    done = 0
    for c in clips:
        rank, cs, ce = c["rank"], float(c["start"]), float(c["end"])
        src = find_clip(out_dir, rank)
        if not src:
            log(f"clip #{rank}: no rendered out/*_clip{rank:02d}.mp4 -- run reframe/facetrack first; skipping")
            continue
        ws = [{"word": w["word"], "start_off": float(w["start"]) - cs, "end_off": float(w["end"]) - cs}
              for w in words_all if cs - 0.15 <= float(w["start"]) < ce]
        if not ws:
            log(f"clip #{rank}: no words in [{cs:.0f},{ce:.0f}]s; skipping")
            continue
        log(f"clip #{rank}: {p['style']} captions, {len(ws)} words, clean_audio={clean} -> {src.stem}_cap.mp4")
        if render(src, ws, out_dir, p):
            done += 1

    log(f"DONE -- {done}/{len(clips)} captioned clips in {out_dir} (originals kept). NOT published (rule 1).")


if __name__ == "__main__":
    main()
