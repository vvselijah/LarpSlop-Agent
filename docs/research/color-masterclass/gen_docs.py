"""Generate per-video analysis MDs + copy hero screenshots into the vault, from the studies.

Usage: python gen_docs.py            (uses extracted/studies.all.json if present, else studies.json)
Produces: per-video/<slug>.md, and copies each study's keyFrames into the vault attachments.
"""
import json
import os
import shutil
from pathlib import Path

RES = Path(__file__).resolve().parent
RAW = RES / "raw"
PV = RES / "per-video"
PV.mkdir(exist_ok=True)
VAULT_IMG = Path(r"C:\Users\elija\OneDrive\Desktop\ai agent team\obsidian\Elijah's vault\40-Projects\LarpSlop\Color-Grading-Masterclass\screens")
VAULT_IMG.mkdir(parents=True, exist_ok=True)

studies_path = RES / "extracted" / "studies.all.json"
if not studies_path.exists():
    studies_path = RES / "extracted" / "studies.json"
studies = json.load(open(studies_path, encoding="utf-8"))


def md_for(s):
    g = lambda k, d="": s.get(k, d)
    out = [f"# {g('slug')} — analysis\n",
           f"*Source: {g('authority', g('authorityNote',''))} · framesRead: {g('framesRead','?')}*\n",
           f"## Overview\n{g('overview')}\n",
           "## Order of operations\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(g('orderOfOperations', []))) + "\n",
           f"## Node tree\n{g('nodeTree')}\n",
           "## Scopes\n" + "\n".join(f"- **{x.get('scope','')}** — {x.get('howRead','')}" + (f" · targets: {x.get('targets')}" if x.get('targets') else "") for x in g('scopes', [])) + "\n",
           f"## Primaries\n{g('primaries')}\n",
           f"## Secondaries\n{g('secondaries')}\n",
           f"## Skin tone\n{g('skinTone')}\n",
           f"## Color management\n{g('colorManagement')}\n",
           f"## Look design\n{g('lookDesign')}\n",
           "## Numeric settings seen on screen\n" + "\n".join(f"- {x}" for x in g('numericSettings', [])) + "\n",
           "## Teaching points\n" + "\n".join(f"- {x}" for x in g('teachingPoints', [])) + "\n",
           "## Quotable claims\n" + "\n".join(f"- \"{x.get('claim','')}\"" + (f" ({x.get('timestamp')})" if x.get('timestamp') else "") for x in g('quotableClaims', [])) + "\n",
           "## Key frames\n" + "\n".join(f"- `{x.get('frame','')}` — {x.get('shows','')}" for x in g('keyFrames', [])) + "\n"]
    return "\n".join(out)


copied = []
for s in studies:
    slug = s.get("slug")
    (PV / f"{slug}.md").write_text(md_for(s), encoding="utf-8")
    # copy hero screenshots into the vault, prefixed by slug
    for kf in s.get("keyFrames", []):
        fr = kf.get("frame", "")
        if not fr.endswith(".jpg"):
            continue
        src = RAW / slug / "frames" / fr
        if src.exists():
            dst = VAULT_IMG / f"{slug}__{fr}"
            try:
                shutil.copyfile(src, dst)
                copied.append((f"{slug}__{fr}", kf.get("shows", "")))
            except OSError:
                pass

# write a screenshot index for the guide
idx = ["# Screenshot index (hero frames the analysts flagged)\n"]
for name, shows in copied:
    idx.append(f"- `screens/{name}` — {shows}")
(VAULT_IMG.parent / "Screenshot index.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
print(f"wrote {len(studies)} per-video MDs; copied {len(copied)} hero screenshots to vault.")
