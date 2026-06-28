#!/usr/bin/env bash
# Phase 5 — color grade the trimmed clips with colorkit.
# Usage:  bash grade_clips.sh [look] [clip-glob]
#   look       a colorkit look (default: clean_pop). Options: clean_pop golden_hour
#              moody_blue warm_interview teal_orange kodak_2383_style fuji_style
#              portra_style bleach_bypass neutral_correct  (or 'auto' to let colorkit pick per clip)
#   clip-glob  which clips to grade (default: all). e.g. "01_*" for just the hook.
# Outputs graded 1080x1920 mp4s to clipwith-edit/graded/.
set -u
HUB="C:/Users/elija/OneDrive/Desktop/ai agent team"
PY="$HUB/auto-clip/.venv/Scripts/python.exe"
COLOR="$HUB/auto-clip/color.py"
CLIPS="$HUB/clipwith-edit/clips"
OUT="$HUB/clipwith-edit/graded"
LOOK="${1:-clean_pop}"
GLOB="${2:-*}"
mkdir -p "$OUT"
echo "=== grading $CLIPS/$GLOB.mp4 with look=$LOOK -> $OUT ==="
for f in "$CLIPS"/$GLOB.mp4; do
  [ -e "$f" ] || { echo "no clips match $GLOB"; break; }
  base=$(basename "$f")
  echo "--- $base ---"
  # single-shot clips => --match is a no-op; --height 1920 for IG; look @0.7 (colorkit default).
  "$PY" "$COLOR" "$f" --look "$LOOK" --height 1920 --hwaccel auto --out "$OUT" 2>&1 | tail -3
done
echo "=== grade done -> $OUT ==="
