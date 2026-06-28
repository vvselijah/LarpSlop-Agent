#!/usr/bin/env bash
# Build a single ROUGH-CUT review video: all 20 keeper clips, in script order,
# normalized to 1080x1920, each labeled with its clip # + line keyword so you can
# verify the takes in one ~2.5-min watch and tell me precisely which (if any) are wrong.
set -u
HUB="C:/Users/elija/OneDrive/Desktop/ai agent team/clipwith-edit"
CLIPS="$HUB/clips"
TMP="$HUB/_review_tmp"
OUT="$HUB/_ROUGH-CUT-review.mp4"
rm -rf "$TMP"; mkdir -p "$TMP"

# does this ffmpeg have drawtext (libfreetype)?
if ffmpeg -hide_banner -filters 2>/dev/null | grep -q "drawtext"; then DT=1; else DT=0; fi
FONT="C\\:/Windows/Fonts/arialbd.ttf"
[ -f "C:/Windows/Fonts/arialbd.ttf" ] || DT=0
echo "drawtext labels: $DT"

> "$TMP/list.txt"
for f in "$CLIPS"/[0-9][0-9]_*.mp4; do
  base=$(basename "$f" .mp4)               # e.g. 12_shot12_2500-200videos
  seg="$TMP/seg_$base.mp4"
  norm="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1"
  if [ "$DT" -eq 1 ]; then
    vf="$norm,drawtext=fontfile='$FONT':text='$base':x=24:y=28:fontsize=46:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=14"
  else
    vf="$norm"
  fi
  echo "  segment: $base"
  ffmpeg -y -i "$f" -vf "$vf" -r 30 -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p \
    -c:a aac -ar 48000 -ac 2 "$seg" 2>"$TMP/err_$base.txt" \
    && echo "file '$seg'" >> "$TMP/list.txt" \
    || { echo "  !! failed $base"; tail -3 "$TMP/err_$base.txt"; }
done

echo "=== concatenating ==="
ffmpeg -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT" 2>"$TMP/concat_err.txt" \
  || ffmpeg -y -f concat -safe 0 -i "$TMP/list.txt" -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p -c:a aac "$OUT" 2>>"$TMP/concat_err.txt"
echo "=== ROUGH CUT -> $OUT ==="
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null | xargs -I{} echo "duration: {}s"
