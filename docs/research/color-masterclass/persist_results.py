"""Split the color-masterclass-deep workflow result into durable files on disk.

Reads the task-output JSON (a wrapper around the workflow's return value) and writes:
  - extracted/synthesis_v2.md          (the upgraded, demonstrated-evidence methodology)
  - extracted/engine_gap_map.json      (gap_map + flagged_claims)
  - extracted/engine_gap_map.md        (human-readable gap table, grouped by priority)
  - per-video-v2/<slug>.md             (each authority's demonstrated technique sheet)
Then prints a coverage + priority summary.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = sys.argv[1] if len(sys.argv) > 1 else None
EXTRACTED = ROOT / "extracted"
PERVID = ROOT / "per-video-v2"


def find_result(obj):
    """Locate the workflow return value ({n_batches, sheets, gapmap}) inside the wrapper."""
    if isinstance(obj, dict):
        if "gapmap" in obj and "sheets" in obj:
            return obj
        for k in ("result", "return", "value", "output", "data"):
            if k in obj and isinstance(obj[k], dict):
                r = find_result(obj[k])
                if r:
                    return r
        # last resort: scan all dict values
        for v in obj.values():
            if isinstance(v, dict):
                r = find_result(v)
                if r:
                    return r
    return None


def slug_from_sheet(md: str, i: int) -> str:
    m = re.search(r"##\s*([a-z0-9\-]+)\s*[—-]", md)
    return m.group(1) if m else f"sheet-{i:02d}"


def main() -> int:
    raw = Path(OUT).read_text(encoding="utf-8")
    try:
        wrapper = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}", file=sys.stderr)
        return 2
    res = find_result(wrapper)
    if not res:
        print(f"Could not find result; top-level keys = {list(wrapper)}", file=sys.stderr)
        return 3

    EXTRACTED.mkdir(exist_ok=True)
    PERVID.mkdir(exist_ok=True)

    gm = res.get("gapmap") or {}
    synthesis = gm.get("synthesis_md", "")
    gap_map = gm.get("gap_map", [])
    flagged = gm.get("flagged_claims", [])
    sheets = res.get("sheets", [])

    (EXTRACTED / "synthesis_v2.md").write_text(synthesis, encoding="utf-8")
    (EXTRACTED / "engine_gap_map.json").write_text(
        json.dumps({"gap_map": gap_map, "flagged_claims": flagged}, indent=2), encoding="utf-8")

    # human-readable gap table grouped by priority
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    rows = sorted(gap_map, key=lambda g: (order.get(str(g.get("priority", "")).upper(), 9),
                                          str(g.get("module", ""))))
    lines = ["# colorkit engine gap map (from demonstrated-evidence analysis, 2026-06-25)", "",
             f"{len(gap_map)} mapped techniques · {len(flagged)} flagged-for-recheck", ""]
    cur = None
    for g in rows:
        pri = str(g.get("priority", "?")).upper()
        if pri != cur:
            cur = pri
            lines.append(f"\n## {pri}\n")
        lines.append(f"- **[{g.get('status','?')}] {g.get('technique','?')}** "
                     f"(`{g.get('module','?')}`) — {g.get('engine_change','')}  "
                     f"_ev: {g.get('evidence','')}_")
    if flagged:
        lines.append("\n## Flagged for human re-check\n")
        lines += [f"- {c}" for c in flagged]
    (EXTRACTED / "engine_gap_map.md").write_text("\n".join(lines), encoding="utf-8")

    for old in PERVID.glob("*.md"):
        old.unlink()
    for i, md in enumerate(sheets):
        slug = slug_from_sheet(md, i)
        (PERVID / f"{slug}.md").write_text(md, encoding="utf-8")

    # summary
    by_pri: dict[str, int] = {}
    for g in gap_map:
        by_pri[str(g.get("priority", "?")).upper()] = by_pri.get(str(g.get("priority", "?")).upper(), 0) + 1
    print(f"n_batches={res.get('n_batches')} extracted={res.get('n_extracted')} "
          f"techniques={res.get('n_techniques')} sheets={len(sheets)}")
    print(f"gap_map={len(gap_map)} by_priority={dict(sorted(by_pri.items()))} flagged={len(flagged)}")
    print(f"wrote: extracted/synthesis_v2.md ({len(synthesis)} chars), engine_gap_map.(json|md), "
          f"per-video-v2/*.md ({len(sheets)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
