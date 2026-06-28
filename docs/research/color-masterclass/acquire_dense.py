r"""Dense, fused re-acquisition of the color-grading masterclasses (the "watch every frame
against everything they said" pass).

The first pass (``acquire.py``) took 50 evenly-spaced frames per video (1 frame every ~8-128s on
the long ones) and collapsed the transcript to 15s windows -- it read every WORD but only glanced at
the SCREEN, and never aligned the two. For color grading that misses the whole demonstration: the
exact scope readings, wheel/curve values, and node structure shown at the moment a technique is
described.

This pass fixes that. Per video, for the local 720p copy + the WORD-LEVEL ``.vtt``:
  1. Extract frames at ``--fps`` (default 1 fps) -- one look per second, not per two minutes.
  2. Perceptual-dedup (dHash + Hamming): collapse static UI stretches, KEEP every frame where the
     screen meaningfully changed (a wheel moved, a scope shifted, a node was added). That keeps the
     *moments of demonstrated action* and drops redundant holds -- the right density for vision review.
  3. Parse the per-word timestamps out of the auto-caption ``.vtt`` and, for each KEPT frame at time
     T, attach the words spoken in ``[T-win, T+win]`` -> a fused record: "at MM:SS the screen shows
     <frame> while the colorist says <words>".

Output per video under ``raw/<slug>/dense/``:
  - ``frames/f####_<mmss>.jpg``  -- the kept (distinct) frames, named by timestamp
  - ``fused.jsonl``              -- one JSON record per kept frame {idx, t, mmss, frame, said}
  - ``summary.json``             -- counts (raw frames, kept frames, dedup ratio, duration)

Stdlib + cv2 + numpy only (no OCR dependency: the vision agents read the frames directly). Run with
the auto-clip venv python from this directory:

    ..\..\..\auto-clip\.venv\Scripts\python.exe acquire_dense.py [--fps 1] [--hamming 10] [slug ...]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"

_TS = re.compile(r"<(\d\d):(\d\d):(\d\d)\.(\d\d\d)>")
_CUE = re.compile(r"^(\d\d):(\d\d):(\d\d)\.(\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d)\.(\d\d\d)")
_TAG = re.compile(r"<[^>]+>")


def _hms(h: int, m: int, s: int, ms: int = 0) -> float:
    return h * 3600 + m * 60 + s + ms / 1000.0


def parse_vtt_words(vtt_path: Path) -> list[tuple[float, str]]:
    """Return a clean, de-duplicated, time-ordered ``[(t_seconds, word), ...]`` stream.

    YouTube auto-captions ROLL: each cue redisplays the tail of the previous line plus a little new
    text, so a naive word dump triples every phrase. We parse cues (start time + tag-stripped displayed
    text) in order and run the canonical **overlap merge**: for each cue, find the largest k where the
    last k words already emitted equal the first k words of this cue, and append only the non-overlapping
    suffix (each new word stamped with the cue's start time). That yields every spoken word exactly once,
    in order, timed within ~1-2s -- ample for the +/- 2.5s frame-alignment window.
    """
    txt = vtt_path.read_text(encoding="utf-8", errors="replace")
    cues: list[tuple[float, str]] = []  # (start_s, displayed_text)
    cur_start: float | None = None
    buf: list[str] = []
    for line in txt.splitlines():
        m = _CUE.match(line)
        if m:
            if cur_start is not None:
                cues.append((cur_start, _TAG.sub("", " ".join(buf))))
            cur_start = _hms(int(m[1]), int(m[2]), int(m[3]), int(m[4]))
            buf = []
        elif line.strip() and not line.startswith(("WEBVTT", "Kind:", "Language:")):
            buf.append(line)
    if cur_start is not None:
        cues.append((cur_start, _TAG.sub("", " ".join(buf))))

    out: list[tuple[float, str]] = []
    prev_words: list[str] = []
    for start, text in cues:
        cw = re.sub(r"\s+", " ", text).strip().split()
        if not cw:
            continue
        maxk = min(len(prev_words), len(cw))
        k = 0
        for kk in range(maxk, 0, -1):
            if prev_words[-kk:] == cw[:kk]:
                k = kk
                break
        for w in cw[k:]:
            out.append((start, w))
        prev_words = (prev_words + cw[k:])[-40:]  # bounded tail for overlap test
    return out


def words_in_window(words: list[tuple[float, str]], t: float, win: float) -> str:
    seg = [w for (wt, w) in words if (t - win) <= wt <= (t + win)]
    return " ".join(seg).strip()


def dhash(gray: np.ndarray, size: int = 8) -> int:
    """64-bit difference hash of a grayscale image (resize to (size+1)x size, compare columns)."""
    small = cv2.resize(gray, (size + 1, size), interpolation=cv2.INTER_AREA)
    diff = small[:, 1:] > small[:, :-1]
    bits = 0
    for b in diff.flatten():
        bits = (bits << 1) | int(b)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def extract_frames(mp4: Path, out_dir: Path, fps: float) -> list[tuple[int, float, Path]]:
    """ffmpeg-extract at ``fps`` into a temp dir; return ``[(idx, t_seconds, path), ...]``."""
    tmp = out_dir / "_all"
    tmp.mkdir(parents=True, exist_ok=True)
    for old in tmp.glob("*.jpg"):
        old.unlink()
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
         "-vf", f"fps={fps},scale=1100:-2", "-q:v", "3", str(tmp / "a%05d.jpg")],
        check=False,
    )
    frames = sorted(tmp.glob("a*.jpg"))
    return [(i + 1, i / fps, p) for i, p in enumerate(frames)]


def process(slug: str, fps: float, ham_thresh: int, win: float) -> dict:
    d = RAW / slug
    mp4 = next((p for p in d.glob("*.mp4")), None)
    vtt = next((p for p in d.glob("*.vtt")), None)
    if not mp4 or not vtt:
        print(f"  SKIP {slug}: mp4={bool(mp4)} vtt={bool(vtt)}", flush=True)
        return {"slug": slug, "ok": False}

    dense = d / "dense"
    fdir = dense / "frames"
    fdir.mkdir(parents=True, exist_ok=True)
    for old in fdir.glob("*.jpg"):
        old.unlink()

    words = parse_vtt_words(vtt)
    allframes = extract_frames(mp4, dense, fps)

    kept: list[tuple[int, float, Path]] = []
    prev_hash: int | None = None
    for idx, t, p in allframes:
        img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        h = dhash(img)
        if prev_hash is None or hamming(prev_hash, h) >= ham_thresh:
            kept.append((idx, t, p))
            prev_hash = h

    records = []
    for k, (idx, t, p) in enumerate(kept, 1):
        mm, ss = int(t // 60), int(t % 60)
        mmss = f"{mm:02d}{ss:02d}"
        dst = fdir / f"f{k:04d}_{mmss}.jpg"
        cv2.imwrite(str(dst), cv2.imread(str(p)))
        records.append({
            "idx": k, "t": round(t, 1), "mmss": f"{mm:02d}:{ss:02d}",
            "frame": dst.name, "said": words_in_window(words, t, win),
        })

    (dense / "fused.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")

    # cleanup the temp full-rate dump (keep only the deduped set)
    for old in (dense / "_all").glob("*.jpg"):
        old.unlink()
    try:
        (dense / "_all").rmdir()
    except OSError:
        pass

    dur = allframes[-1][1] if allframes else 0.0
    summary = {
        "slug": slug, "ok": True, "fps": fps, "hamming": ham_thresh,
        "duration_s": round(dur, 1), "raw_frames": len(allframes),
        "kept_frames": len(kept),
        "dedup_ratio": round(len(kept) / max(1, len(allframes)), 3),
        "words": len(words),
    }
    (dense / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"  {slug}: {len(allframes)} raw -> {len(kept)} kept "
          f"({summary['dedup_ratio']*100:.0f}%), {len(words)} words, {dur/60:.1f} min", flush=True)
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*", help="video slugs to process (default: all in raw/)")
    ap.add_argument("--fps", type=float, default=1.0)
    ap.add_argument("--hamming", type=int, default=10, help="min dHash distance to keep a new frame")
    ap.add_argument("--win", type=float, default=2.5, help="+/- seconds of transcript per frame")
    args = ap.parse_args()

    slugs = args.slugs or sorted(p.name for p in RAW.iterdir()
                                 if p.is_dir() and not p.name.startswith("_"))
    out = []
    for slug in slugs:
        print(f"=== {slug} ===", flush=True)
        out.append(process(slug, args.fps, args.hamming, args.win))
    (RAW / "dense_manifest.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    ok = sum(1 for s in out if s.get("ok"))
    tot_kept = sum(s.get("kept_frames", 0) for s in out)
    print(f"\nDONE: {ok}/{len(out)} processed, {tot_kept} total kept frames.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
