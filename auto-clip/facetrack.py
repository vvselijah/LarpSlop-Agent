"""
auto-clip/facetrack.py -- face-tracking 9:16 reframe (v1): the crop FOLLOWS a chosen speaker.

For a 16:9 / wide / two-shot source, OpenCV (Haar frontal + profile cascades, both bundled with cv2 --
no model download) detects faces at sampled times, locks onto ONE target speaker (largest / left / right
with a temporal lock so it doesn't jump people), builds a smoothed horizontal crop track, and FFmpeg
applies it via `sendcmd` -> a vertical 1080x1920 clip with audio preserved. This is v1 of the auto-clip
PLAN's "face/subject-aware reframe" (center-crop was v0). Active-speaker auto-SWITCHING between two people
is the v2 follow-up (see docs/plans/2026-06-14-interview-clip-enhancements-research.md).

Detection runs OpenCV; the encode is pure FFmpeg (no slow per-frame cv2 VideoWriter, audio kept).

Usage:
  python facetrack.py <source-video> [--start S] [--end E] [--target largest|left|right]
                      [--out out] [--name <stem>] [--sample 0.2] [--smooth 0.18] [--encoder libx264]
Writes:
  out/<name>_track.mp4   (+ a debug out/<name>_track.cmd sendcmd file)
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import cv2

BASE = Path(__file__).resolve().parent


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def detect_faces(gray, frontal, profile, inv_scale):
    """gray = downscaled grayscale frame. Returns full-res [(cx, area)] candidate face centers."""
    out = []
    found = frontal.detectMultiScale(gray, 1.1, 5, minSize=(36, 36))
    for (x, y, w, h) in found:
        out.append(((x + w / 2) * inv_scale, w * h))
    found = profile.detectMultiScale(gray, 1.1, 5, minSize=(36, 36))  # left-facing profiles
    for (x, y, w, h) in found:
        out.append(((x + w / 2) * inv_scale, w * h))
    flip = cv2.flip(gray, 1)                                          # right-facing profiles
    gw = gray.shape[1]
    found = profile.detectMultiScale(flip, 1.1, 5, minSize=(36, 36))
    for (x, y, w, h) in found:
        out.append(((gw - (x + w / 2)) * inv_scale, w * h))
    return out


def strat_pick(boxes, target):
    """Initial lock target from candidate boxes [(cx, area)]: largest / leftmost / rightmost."""
    if not boxes:
        return None
    if target == "left":
        return min(boxes, key=lambda b: b[0])[0]
    if target == "right":
        return max(boxes, key=lambda b: b[0])[0]
    return max(boxes, key=lambda b: b[1])[0]          # largest (most prominent)


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        log("FATAL: usage: python facetrack.py <source-video> [--start S] [--end E] "
            "[--target largest|left|right] [--name <stem>] [--sample 0.2] [--smooth 0.18]")
        sys.exit(1)

    src = Path(args[0]).resolve()
    if not src.exists():
        log(f"FATAL: source not found: {src}")
        sys.exit(1)

    def opt(f, d):
        return args[args.index(f) + 1] if f in args else d

    out_dir = BASE / opt("--out", "out")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = opt("--target", "largest")
    name = opt("--name", src.stem.replace(" ", "_"))
    sample = float(opt("--sample", "0.2"))
    alpha = float(opt("--smooth", "0.18"))
    encoder = opt("--encoder", "libx264")

    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        log(f"FATAL: cv2 could not open {src}")
        sys.exit(1)
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dur = (cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0) / (cap.get(cv2.CAP_PROP_FPS) or 30)
    start = float(opt("--start", "0"))
    end = float(opt("--end", str(round(dur, 2)) if dur else "0"))
    if end <= start:
        log("FATAL: need --end > --start (and a readable duration)")
        sys.exit(1)

    crop_w = (round(H * 9 / 16)) // 2 * 2          # even
    crop_h = H
    cdir = cv2.data.haarcascades
    frontal = cv2.CascadeClassifier(cdir + "haarcascade_frontalface_default.xml")
    profile = cv2.CascadeClassifier(cdir + "haarcascade_profileface.xml")

    det_w = 960                                     # detect on a downscaled frame for speed
    scale = det_w / W
    inv_scale = 1.0 / scale
    det_h = int(H * scale)

    log(f"{src.name} {W}x{H} -> crop {crop_w}x{crop_h} -> 1080x1920 | target={target} "
        f"window {start:.0f}-{end:.0f}s @ {sample}s")

    lock_band = W * float(opt("--band", "0.18"))      # only follow faces within this of the locked x
    track, prev = [], None
    t = start
    n = 0
    while t < end:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.cvtColor(cv2.resize(frame, (det_w, det_h)), cv2.COLOR_BGR2GRAY)
        boxes = detect_faces(small, frontal, profile, inv_scale)
        if prev is None:                              # acquire the initial lock
            prev = strat_pick(boxes, target)
        else:                                         # lock-and-hold: never switch speakers
            near = [b for b in boxes if abs(b[0] - prev) < lock_band]
            if near:
                prev = max(near, key=lambda b: b[1])[0]
            # else: hold prev through profile turns / dropouts
        track.append((t, prev))
        t += sample
        n += 1
    cap.release()

    if not track:
        log("FATAL: no frames sampled")
        sys.exit(1)
    hits = sum(1 for _, c in track if c is not None)
    log(f"sampled {n} frames, {hits} with a locked face ({100*hits//max(1,n)}%)")

    # EMA smooth + clamp -> sendcmd (0-based timeline; crop x driven over time)
    s = None
    lines = []
    for (tt, cx) in track:
        cx = W / 2 if cx is None else cx
        s = cx if s is None else alpha * cx + (1 - alpha) * s
        x = min(max(s - crop_w / 2, 0), W - crop_w)
        lines.append(f"{max(0.0, tt - start):.3f} crop x {int(round(x))};")
    cmd_path = out_dir / f"{name}_track.cmd"
    cmd_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    dst = out_dir / f"{name}_track.mp4"
    vf = f"sendcmd=f={cmd_path.name},crop={crop_w}:{crop_h}:0:0,scale=1080:1920"
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", str(start), "-to", str(end), "-i", str(src),
        "-vf", vf, "-c:v", encoder, "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", dst.name,
    ]
    log(f"rendering -> {dst.name}")
    r = subprocess.run(cmd, cwd=str(out_dir), capture_output=True, text=True)
    if r.returncode != 0:
        tail = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error"
        log(f"FAILED: {tail}")
        sys.exit(1)
    log(f"DONE -> {dst}  (sendcmd: {cmd_path.name}). NOT published (rule 1).")


if __name__ == "__main__":
    main()
