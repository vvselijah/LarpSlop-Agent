"""Acquire the curated DaVinci color-grading masterclasses for deep local analysis.

For each video: yt-dlp auto-subtitles (full transcript) + a 720p copy, then ffmpeg
extracts ~50 evenly-spaced frames (legible UI/scopes/nodes). Writes raw/<slug>/ with
transcript.txt, frames/f###.jpg, meta.json. Quota-free (no Gemini). Run from this dir.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

YTDLP = r"C:\Users\elija\.local\bin\yt-dlp.exe"
ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

# (id, slug, category, note) -- the curated curriculum from the top-reviewed authorities.
VIDEOS = [
    ("YbDRl_xugJo", "mostyn-color-page-intro", "fundamentals", "Darren Mostyn - NEW to DaVinci? Color Grading"),
    ("rPE1AXKGjgM", "beginners-guide-grading", "fundamentals", "Beginner's Guide to Colour Grading"),
    ("itli8isoXQQ", "2hr-beginner-course", "fundamentals", "How To Color Grade for Beginners (2hr)"),
    ("vt1T9h_vAqY", "mostyn-read-scopes", "scopes", "How Pro Colorists Read Scopes ft Darren Mostyn"),
    ("35wo8eVikqA", "cullen-master-scopes", "scopes", "Cullen Kelly - Master Scopes Inside DaVinci"),
    ("wvPkoL8nx-I", "mostyn-perfect-node-tree", "nodes", "Darren Mostyn - My Perfect Node Tree"),
    ("kdTMRQP_V7E", "best-node-tree-any-camera", "nodes", "BEST Node Tree for ANY Camera (BBC pro)"),
    ("z7PFk8vYSxs", "grading-too-complicated", "color-mgmt", "Has Colour Grading Got Too Complicated? (color mgmt)"),
    ("NnNqjPbfIG8", "cullen-36-project-settings", "color-mgmt", "Cullen Kelly - 36 Project Settings"),
    ("6qJzzwkttrk", "cullen-contrast-cinematographer", "primaries", "Cullen Kelly - contrast secrets for cinematographers"),
    ("-oGA1ayemUY", "qualifier-tricks", "secondaries", "BEST Pro Colorist Qualifier Tricks"),
    ("YRo8b6AJtaM", "frenchie-masterclass", "look-design", "Frenchie - Pro Colorist Reveals all (MASTERCLASS)"),
    ("IBwLq8vtfJ4", "mullins-grading-philosophy", "look-design", "Mitchell Mullins - Color Grading Mastery philosophy"),
    ("45z60vnPOBw", "film-emulation-16-35mm", "look-design", "Emulating 16mm/35mm Film"),
    # --- Pass 1 (2026-06-26): the 11 individual videos from the vault note ---
    ("22mmIgWIcvE", "lenz-most-important-concept", "fundamentals", "Eric Lenz - The MOST IMPORTANT Concept in Colour Grading"),
    ("Zh3QYgCXQGw", "wampus-pro-seminar", "look-design", "Wampus - DaVinci Pro Teaches Me the Color Page (Full Seminar)"),
    ("hvwQIQcXFbI", "euro-pro-level-64min", "fundamentals", "European Filmmaker - Learn PRO-Level Color Grading in 64 Min"),
    ("MCDVcQIA3UM", "faris-full-course-2026", "fundamentals", "Casey Faris - Introduction to DaVinci Resolve Full Course (2026, 5.2hr)"),
    ("3g8TA5n92Bs", "jenkinson-exact-system", "look-design", "Declan Jenkinson - The EXACT SYSTEM To Colour Grade Anything"),
    ("llmycBwcTD4", "qazi-start-here", "fundamentals", "Waqas Qazi - New to DaVinci? Start Color Grading Here"),
    ("SkosqJfzEs0", "batal-conquer-color-page", "fundamentals", "Daniel Batal - CONQUER the COLOR Page"),
    ("pPzhzkPWxkg", "benkabouche-1h-master", "fundamentals", "Zakaria Benkabouche - 1h to Master Color Grading"),
    ("vGrnJeIMyQQ", "neistadt-ultimate-guide", "look-design", "Jason Neistadt - Color Grading: The ULTIMATE GUIDE"),
    ("nSNBtl8cOl8", "editing-explained-2hr", "fundamentals", "Editing Explained - 2 hours: EVERYTHING about Color Grading"),
    ("-MrHvGoq9lY", "content-creators-indepth", "fundamentals", "Content Creators - In Depth DaVinci Resolve Tutorial (2026)"),
]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def clean_vtt(vtt_path: Path) -> str:
    """Convert an auto-caption VTT into deduped, timestamped plain text (~every 15s)."""
    txt = vtt_path.read_text(encoding="utf-8", errors="replace")
    blocks = []
    cur_ts = None
    last = None
    for line in txt.splitlines():
        m = re.match(r"(\d\d:\d\d:\d\d)\.\d\d\d\s*-->", line)
        if m:
            cur_ts = m.group(1)
            continue
        if "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")) or not line.strip():
            continue
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if not clean or clean == last:
            continue
        last = clean
        blocks.append((cur_ts or "00:00:00", clean))
    # collapse to ~1 line per 15s window, joining the words spoken in that window
    out, window, wstart = [], [], None
    def hms_to_s(h):
        a = h.split(":"); return int(a[0]) * 3600 + int(a[1]) * 60 + int(a[2])
    for ts, words in blocks:
        s = hms_to_s(ts)
        if wstart is None:
            wstart = s
        if s - wstart >= 15 and window:
            out.append(f"[{wstart//3600:02d}:{(wstart%3600)//60:02d}:{wstart%60:02d}] " + " ".join(window))
            window, wstart = [], s
        window.append(words)
    if window:
        out.append(f"[{wstart//3600:02d}:{(wstart%3600)//60:02d}:{wstart%60:02d}] " + " ".join(window))
    return "\n".join(out)


def ffprobe_duration(mp4: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(mp4)])
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def acquire(vid, slug, category, note):
    d = RAW / slug
    d.mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={vid}"
    print(f"\n=== {slug} ({vid}) ===", flush=True)

    # metadata
    r = run([YTDLP, "--skip-download", "--print",
             "%(title)s\t%(duration)s\t%(channel)s\t%(view_count)s\t%(like_count)s", url])
    title = dur = channel = views = likes = ""
    if r.returncode == 0 and r.stdout.strip():
        parts = (r.stdout.strip().splitlines()[-1]).split("\t")
        if len(parts) >= 5:
            title, dur, channel, views, likes = parts[:5]
    print(f"  {title} | {dur}s | {channel} | {views} views | {likes} likes", flush=True)

    # subtitles + 720p video in one call (single extraction; gentle on rate limits)
    r = run([YTDLP, "-f", "136/135/18", "--write-auto-subs", "--sub-langs", "en",
             "--sub-format", "vtt", "--convert-subs", "vtt", "--sleep-requests", "1",
             "-o", str(d / "%(id)s.%(ext)s"), url])
    if r.returncode != 0:
        print(f"  yt-dlp FAILED: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '?'}", flush=True)

    mp4 = next(iter(d.glob(f"{vid}*.mp4")), None)
    vtt = next(iter(d.glob(f"{vid}*.vtt")), None)

    transcript_ok = False
    if vtt and vtt.exists():
        try:
            (d / "transcript.txt").write_text(clean_vtt(vtt), encoding="utf-8")
            transcript_ok = True
        except Exception as e:
            print(f"  transcript clean failed: {e}", flush=True)

    # frames: ~50 evenly spaced, 1280 wide, legible
    nframes = 0
    duration = ffprobe_duration(mp4) if mp4 else 0.0
    if mp4 and duration > 0:
        interval = min(150.0, max(8.0, duration / 50.0))
        fdir = d / "frames"
        fdir.mkdir(exist_ok=True)
        rr = run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
                  "-vf", f"fps=1/{interval:.3f},scale=1280:-2", "-q:v", "3",
                  str(fdir / "f%03d.jpg")])
        nframes = len(list(fdir.glob("f*.jpg")))
        print(f"  frames: {nframes} (every {interval:.0f}s)  transcript={transcript_ok}", flush=True)

    meta = {
        "id": vid, "slug": slug, "category": category, "note": note, "url": url,
        "title": title, "duration_s": dur, "channel": channel, "views": views, "likes": likes,
        "frames": nframes, "transcript": transcript_ok,
        "frames_dir": str((d / "frames").resolve()),
        "transcript_path": str((d / "transcript.txt").resolve()) if transcript_ok else None,
    }
    (d / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def main():
    manifest = []
    only = sys.argv[1:] or None  # optionally pass slugs to (re)acquire a subset
    for vid, slug, cat, note in VIDEOS:
        if only and slug not in only and vid not in only:
            continue
        try:
            manifest.append(acquire(vid, slug, cat, note))
        except Exception as e:
            print(f"  ERROR {slug}: {e}", flush=True)
        time.sleep(4)  # be gentle on YouTube rate limits
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    ok = sum(1 for m in manifest if m["frames"] and m["transcript"])
    print(f"\nDONE: {ok}/{len(manifest)} fully acquired. Manifest: {RAW/'manifest.json'}", flush=True)


if __name__ == "__main__":
    main()
