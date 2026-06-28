r"""Acquire BOTH DaVinci course playlists for the deep color analysis, using the venv yt-dlp +
curl_cffi impersonation to dodge the auto-sub 429s the standalone yt-dlp hit.

  PL1 = PLNLA7EsgTsU5lzs9Fy-OhsybeY_uXZRfx  (DaVinci Resolve 20 full course, 46 classes)  slug pl1-cNN
  PL2 = PL2HeOArLswsUmXRtQe9tk_utN2UX46Nm1  (Hindi color course, 25 classes)               slug pl2-cNN

Per video: metadata + 720p video + en auto-subs (vtt) + ~50 nav frames + meta.json + transcript.txt,
mirroring acquire.py's raw/<slug>/ layout so acquire_dense.py / build_batches.py pick them up unchanged.

IDEMPOTENT: skips any slug that already has an .mp4 (re-runnable after a crash/429). Run with the
auto-clip venv python from this dir:  ..\..\..\auto-clip\.venv\Scripts\python.exe acquire_playlists.py [pl1|pl2]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

from acquire import clean_vtt, ffprobe_duration  # reuse the proven helpers

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)
PYEXE = sys.executable  # the venv python running this script (has yt_dlp + curl_cffi)

PLAYLISTS = {
    "pl1": ("PLNLA7EsgTsU5lzs9Fy-OhsybeY_uXZRfx", "playlist-dr20"),
    "pl2": ("PL2HeOArLswsUmXRtQe9tk_utN2UX46Nm1", "playlist-hindi"),
}


def ytdlp(*args, timeout=900):
    # --impersonate chrome (curl_cffi) dodges 429s; --js-runtimes node fixes nsig 403s on video data
    return subprocess.run([PYEXE, "-m", "yt_dlp", "--impersonate", "chrome", "--js-runtimes", "node", *args],
                          capture_output=True, text=True, timeout=timeout)


def enumerate_playlist(pid: str):
    r = ytdlp("--flat-playlist", "--print", "%(id)s\t%(title)s",
              f"https://www.youtube.com/playlist?list={pid}")
    out = []
    for line in r.stdout.splitlines():
        if "\t" in line:
            vid, title = line.split("\t", 1)
            if vid.strip():
                out.append((vid.strip(), title.strip()))
    return out


def class_num(title: str):
    m = re.search(r"Class\s*0*(\d+)", title, re.I)
    return int(m.group(1)) if m else None


def acquire_one(vid: str, slug: str, category: str, note: str) -> dict:
    d = RAW / slug
    d.mkdir(parents=True, exist_ok=True)
    if any(d.glob("*.mp4")):
        print(f"  SKIP {slug} (mp4 exists)", flush=True)
        return {"slug": slug, "id": vid, "skipped": True}
    url = f"https://www.youtube.com/watch?v={vid}"
    print(f"\n=== {slug} ({vid}) ===\n  {note}", flush=True)

    # 1) VIDEO ONLY first — decoupled so a subtitle 429 never costs us the video (frames-only fallback)
    rv = ytdlp("-f", "136/135/18", "--sleep-requests", "1", "-o", str(d / "%(id)s.%(ext)s"), url)
    if rv.returncode != 0:
        tail = rv.stderr.strip().splitlines()[-1] if rv.stderr.strip() else "?"
        print(f"  yt-dlp(video) rc={rv.returncode}: {tail}", flush=True)
    # 2) SUBS best-effort (if 429, this video is analyzed frames-only)
    rs = ytdlp("--skip-download", "--write-auto-subs", "--sub-langs", "en", "--sub-format", "vtt",
               "--convert-subs", "vtt", "--sleep-requests", "2", "-o", str(d / "%(id)s.%(ext)s"), url)
    if rs.returncode != 0:
        tail = rs.stderr.strip().splitlines()[-1] if rs.stderr.strip() else "?"
        print(f"  yt-dlp(subs) rc={rs.returncode}: {tail}", flush=True)

    mp4 = next(iter(d.glob(f"{vid}*.mp4")), None) or next(iter(d.glob("*.mp4")), None)
    vtt = next(iter(d.glob(f"{vid}*.vtt")), None) or next(iter(d.glob("*.vtt")), None)

    transcript_ok = False
    if vtt and vtt.exists():
        try:
            (d / "transcript.txt").write_text(clean_vtt(vtt), encoding="utf-8")
            transcript_ok = True
        except Exception as e:
            print(f"  transcript clean failed: {e}", flush=True)

    nframes = 0
    duration = ffprobe_duration(mp4) if mp4 else 0.0
    if mp4 and duration > 0:
        interval = min(150.0, max(8.0, duration / 50.0))
        fdir = d / "frames"
        fdir.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
                        "-vf", f"fps=1/{interval:.3f},scale=1280:-2", "-q:v", "3",
                        str(fdir / "f%03d.jpg")], check=False)
        nframes = len(list(fdir.glob("f*.jpg")))
    print(f"  mp4={bool(mp4)} frames={nframes} transcript={transcript_ok} ({duration/60:.1f} min)", flush=True)

    meta = {
        "id": vid, "slug": slug, "category": category, "note": note, "url": url,
        "frames": nframes, "transcript": transcript_ok,
        "frames_dir": str((d / "frames").resolve()),
        "transcript_path": str((d / "transcript.txt").resolve()) if transcript_ok else None,
    }
    (d / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def main() -> int:
    which = [a for a in sys.argv[1:] if a in PLAYLISTS] or list(PLAYLISTS)
    manifest = []
    for key in which:
        pid, category = PLAYLISTS[key]
        print(f"\n########## {key} ({pid}) ##########", flush=True)
        vids = enumerate_playlist(pid)
        print(f"  {len(vids)} videos enumerated", flush=True)
        for vid, title in vids:
            cn = class_num(title)
            slug = f"{key}-c{cn:02d}" if cn else f"{key}-{vid}"
            try:
                manifest.append(acquire_one(vid, slug, category, title))
            except Exception as e:
                print(f"  ERROR {slug}: {e}", flush=True)
            time.sleep(3)
    (RAW / f"playlists_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    got = sum(1 for m in manifest if m and m.get("frames"))
    print(f"\nDONE: {got} acquired (+{sum(1 for m in manifest if m and m.get('skipped'))} skipped). "
          f"Manifest: {RAW / 'playlists_manifest.json'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
