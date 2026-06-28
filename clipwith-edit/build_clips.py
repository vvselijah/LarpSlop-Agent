#!/usr/bin/env python3
"""
Phase 1 builder for "Introducing ClipWith".
Reads cut-list.json -> trims each keeper take (frame-accurate H.264 proxy at native
resolution) -> clips/NN_shotNN_keyword.mp4 -> generates a Resolve-importable FCPXML
that lays the trimmed clips end-to-end in chronological order.

stdlib only. Run with any python (ffmpeg/ffprobe must be on PATH).
"""
import json, os, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.join(ROOT, "cut-list.json")

def ffprobe_dur_dims(path):
    out = subprocess.run(
        ["ffprobe","-v","error","-select_streams","v:0",
         "-show_entries","stream=width,height","-show_entries","format=duration",
         "-of","json", path],
        capture_output=True, text=True)
    j = json.loads(out.stdout)
    w = int(j["streams"][0]["width"]); h = int(j["streams"][0]["height"])
    d = float(j["format"]["duration"])
    return d, w, h

def main():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("!! ffmpeg/ffprobe not on PATH"); sys.exit(1)
    cfg = json.load(open(CUT, encoding="utf-8"))
    clips_dir = cfg["clipsDir"]; os.makedirs(clips_dir, exist_ok=True)
    src_dir = cfg["sourceDir"]
    built = []
    for c in cfg["clips"]:
        src = os.path.join(src_dir, c["src"])
        if not os.path.exists(src):
            print(f"!! MISSING SOURCE {src}"); continue
        name = f"{c['order']:02d}_shot{c['shot']}_{c['keyword']}.mp4"
        out = os.path.join(clips_dir, name)
        tin = float(c["in"]); tout = float(c["out"]); dur = max(0.05, tout - tin)
        A = max(0.0, tin - 2.0); B = tin - A   # fast seek to A, accurate seek B more
        cmd = ["ffmpeg","-y",
               "-ss", f"{A:.3f}", "-i", src, "-ss", f"{B:.3f}", "-t", f"{dur:.3f}",
               "-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p",
               "-c:a","aac","-b:a","192k","-movflags","+faststart", out]
        print(f"[{c['order']:02d}] {name}  ({tin:.2f}-{tout:.2f}, {dur:.2f}s)  <- {c['src']}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            print("   !! ffmpeg failed:\n", r.stderr[-600:]); continue
        d, w, h = ffprobe_dur_dims(out)
        built.append({**c, "file": name, "path": out, "dur": d, "w": w, "h": h})
        print(f"   -> {w}x{h}  {d:.2f}s")
    write_fcpxml(cfg, built, os.path.join(ROOT, "Introducing-ClipWith.fcpxml"))
    json.dump(built, open(os.path.join(ROOT,"clips","_built.json"),"w",encoding="utf-8"), indent=2)
    print(f"\n=== built {len(built)}/{len(cfg['clips'])} clips ===")

# ---- FCPXML (v1.9) ----
FD_NUM, FD_DEN = 1001, 30000  # 29.97 frame duration = 1001/30000 s

def frames(sec): return max(1, round(sec * FD_DEN / FD_NUM))
def rtime(fr):   return f"{fr*FD_NUM}/{FD_DEN}s"

def write_fcpxml(cfg, built, path):
    seqW, seqH = 1080, 1920  # IG target timeline
    res = ['  <resources>',
           f'    <format id="r0" name="FFVideoFormatRateUndefined" frameDuration="{FD_NUM}/{FD_DEN}s" width="{seqW}" height="{seqH}" colorSpace="1-1-1 (Rec. 709)"/>']
    fmt_ids = {}
    for i, b in enumerate(built):
        fid = f"rf{i}"
        wh = (b["w"], b["h"])
        if wh not in fmt_ids:
            fmt_ids[wh] = fid
            res.append(f'    <format id="{fid}" name="FF_{b["w"]}x{b["h"]}" frameDuration="{FD_NUM}/{FD_DEN}s" width="{b["w"]}" height="{b["h"]}" colorSpace="1-1-1 (Rec. 709)"/>')
    for i, b in enumerate(built):
        aid = f"a{i}"; b["_aid"] = aid
        fid = fmt_ids[(b["w"], b["h"])]
        dfr = frames(b["dur"])
        src_uri = "file:///" + b["path"].replace("\\","/").replace(" ", "%20")
        res.append(f'    <asset id="{aid}" name="{b["file"]}" start="0s" hasVideo="1" hasAudio="1" '
                   f'format="{fid}" duration="{rtime(dfr)}" audioSources="1" audioChannels="2">')
        res.append(f'      <media-rep kind="original-media" src="{src_uri}"/>')
        res.append(f'    </asset>')
    res.append('  </resources>')

    spine = []; off = 0
    for b in built:
        dfr = frames(b["dur"])
        spine.append(f'          <asset-clip ref="{b["_aid"]}" offset="{rtime(off)}" '
                     f'name="{b["file"]}" duration="{rtime(dfr)}" start="0s" tcFormat="NDF"/>')
        off += dfr
    seq_dur = rtime(off)
    body = ['<?xml version="1.0" encoding="UTF-8"?>','<!DOCTYPE fcpxml>','<fcpxml version="1.9">',
            *res,
            '  <library>',
            f'    <event name="{cfg["project"]}">',
            f'      <project name="{cfg["project"]} - rough assembly">',
            f'        <sequence format="r0" duration="{seq_dur}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">',
            '          <spine>',
            *spine,
            '          </spine>',
            '        </sequence>',
            '      </project>',
            '    </event>',
            '  </library>',
            '</fcpxml>']
    open(path,"w",encoding="utf-8").write("\n".join(body))
    print(f"FCPXML -> {path}  ({len(built)} clips, {off} frames = {off*FD_NUM/FD_DEN:.1f}s)")

if __name__ == "__main__":
    main()
