r"""Emit the `args` JSON object to paste into the Workflow tool for a color-deep vision pass.

PORTABLE: recomputes the absolute `base` + per-video `batches_dir` from THIS machine's location of
the color-masterclass folder, so it is correct even after the project syncs to a different path/account.

Usage (from this dir, any python):
    python make_args.py pl2          # Pass 2 args (all pl2-* slugs)
    python make_args.py pl1          # Pass 3 args (all pl1-* slugs)
    python make_args.py individuals  # the 11 individual slugs (only needed to RE-extract; normally use merge-only)

Reads raw/batches_index.json for slugs + n_batches. If a slug is missing there, re-run build_batches.py first.
Prints a single-line JSON {base, videos:[{slug,note,batches_dir,n_batches}]} — copy it into Workflow(args=...).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent           # ...\docs\research\color-masterclass  (portable)
RAW = ROOT / "raw"
INDEX = RAW / "batches_index.json"

INDIVIDUALS = [
    "lenz-most-important-concept", "wampus-pro-seminar", "euro-pro-level-64min",
    "faris-full-course-2026", "jenkinson-exact-system", "qazi-start-here",
    "batal-conquer-color-page", "benkabouche-1h-master", "neistadt-ultimate-guide",
    "content-creators-indepth", "editing-explained-2hr",
]


def main() -> int:
    sel = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if sel not in ("pl1", "pl2", "individuals"):
        print("usage: python make_args.py [pl1|pl2|individuals]", file=sys.stderr)
        return 2
    if not INDEX.exists():
        print(f"missing {INDEX} — run build_batches.py first", file=sys.stderr)
        return 3
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    by_slug = {x["slug"]: x for x in idx}

    if sel == "individuals":
        slugs = [s for s in INDIVIDUALS if s in by_slug]
    else:
        slugs = sorted(s for s in by_slug if s.startswith(sel + "-"))

    videos = []
    for s in slugs:
        x = by_slug[s]
        videos.append({
            "slug": s,
            "note": x.get("note", ""),
            # recompute from THIS machine's ROOT (portable; ignore any stored absolute path)
            "batches_dir": str((RAW / s / "dense" / "batches").resolve()),
            "n_batches": x.get("n_batches", 0),
        })
    out = {"base": str(ROOT), "videos": videos}
    print(json.dumps(out))
    print(f"\n# {len(videos)} videos, {sum(v['n_batches'] for v in videos)} batches", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
