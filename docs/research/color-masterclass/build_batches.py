"""Chunk each video's dense/fused.jsonl into vision-agent batch briefs.

Workflow scripts can't touch the filesystem, so we pre-write a markdown "brief" per batch (absolute
frame paths + the aligned transcript for each frame). A Phase-1 vision agent Reads one brief, then
Reads the frames it lists, and extracts frame-cited techniques. Writes:
  - raw/<slug>/dense/batches/b##.md     -- the briefs
  - raw/batches_index.json              -- [{slug, note, batches_dir, n_batches, n_frames}] (small;
                                           passed to the Workflow as `args`)

Run with the auto-clip venv python from this dir:  python build_batches.py [--batch 20]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"


def build(batch: int) -> None:
    index = []
    for d in sorted(p for p in RAW.iterdir() if p.is_dir() and not p.name.startswith("_")):
        fused = d / "dense" / "fused.jsonl"
        if not fused.exists():
            continue
        note = ""
        meta = d / "meta.json"
        if meta.exists():
            try:
                note = json.loads(meta.read_text(encoding="utf-8")).get("note", "")
            except Exception:
                note = ""
        recs = [json.loads(ln) for ln in fused.read_text(encoding="utf-8").splitlines() if ln.strip()]
        frames_dir = d / "dense" / "frames"
        bdir = d / "dense" / "batches"
        bdir.mkdir(parents=True, exist_ok=True)
        for old in bdir.glob("*.md"):
            old.unlink()

        chunks = [recs[i:i + batch] for i in range(0, len(recs), batch)]
        for bi, chunk in enumerate(chunks):
            t0, t1 = chunk[0]["mmss"], chunk[-1]["mmss"]
            lines = [f"# {d.name} — {note}",
                     f"# batch {bi + 1}/{len(chunks)} · {t0}–{t1} · {len(chunk)} frames", ""]
            for r in chunk:
                abspath = (frames_dir / r["frame"]).resolve()
                lines.append(f"## {r['mmss']}  frame: {abspath}")
                lines.append(f"said: {r['said']}")
                lines.append("")
            (bdir / f"b{bi:02d}.md").write_text("\n".join(lines), encoding="utf-8")

        index.append({
            "slug": d.name, "note": note,
            "batches_dir": str(bdir.resolve()),
            "n_batches": len(chunks), "n_frames": len(recs),
        })
        print(f"  {d.name}: {len(recs)} frames -> {len(chunks)} batches", flush=True)

    (RAW / "batches_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    total = sum(x["n_batches"] for x in index)
    print(f"\nDONE: {len(index)} videos -> {total} batches. Index: {RAW / 'batches_index.json'}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=20)
    build(ap.parse_args().batch)
