"""
auto-clip/library.py -- package auto-clip output into a niche-split clip library for agency hand-off.

This is the Phase-0 "stage what already exists" layer from
docs/plans/2026-06-14-clipping-campaign-folder-research.md. It sits AFTER the auto-clip engine:
auto-clip writes loose 9:16 MP4s to out/ plus out/<stem>.manifest.json (rank/file/title/hook/duration)
and data/<stem>.highlights.json (adds score/reason). This script COPIES those clips (never moves --
out/ stays the working dir) into a library tree split by NICHE, with descriptive filenames, then writes:
  - _index.csv  : flat catalog (title, hook, duration, source, niche, score, ...)
  - _index.md   : human-skimmable, grouped by niche, for the agency
  - README-for-agency.md : one-pager (naming scheme, niche breakdown, delivery guidance)
  - library.manifest.json : machine record so re-runs are idempotent and the library ACCUMULATES.

Niche comes from --niche (applies to the whole batch) and/or a per-clip "niche" field in the
manifest/highlights if present; default is "other". The library accumulates across many source videos.

ENGINE EXIT RULE (CLAUDE.md rule 1): stages files into a folder. NEVER uploads, shares, or publishes --
Elijah creates/sends the share link himself. Delivery = clean FILES into a cloud folder (Dropbox/Drive),
never chat/DM media (which transcodes). Default --dest is OUTSIDE the OneDrive tree to avoid double-sync.

Usage:
  python library.py [--out out] [--dest <library-path>] [--niche finance-motivation]
                    [--source <stem>] [--prefer raw|captioned] [--brief "..."] [--dry-run]
Examples:
  # Stage the 6 existing test clips into a throwaway local library, tagged finance-motivation:
  python library.py --niche finance-motivation --dest _library_test
  # Stage one specific source's manifest into the real (configurable) library:
  python library.py --source source --niche software --dest "D:/Dropbox/clip-library"
"""
import argparse
import csv
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent

# The known niches (split decision from the plan). "other" is the safe default bucket.
KNOWN_NICHES = ["finance-motivation", "software", "ads", "viral-funny", "other"]

# Default real destination: OUTSIDE the OneDrive tree (avoids double-sync of large MP4s). This is a
# DOCUMENTED default only -- the real target is Elijah's choice (his Dropbox/Drive sync path) and the
# script never creates it unless he points --dest at it. Relative --dest values resolve inside auto-clip/.
DEFAULT_DEST = r"C:\Users\elija\clip-library"


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:  # Windows cp1252 console chokes on emoji/smart-quotes/arrows
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def slug(text, maxlen=48):
    """Slugify a title for a filename: ascii-safe, lowercase, hyphenated, length-capped."""
    out = []
    for ch in (text or "").lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_":
            out.append("-")
        # everything else (smart quotes, $, emoji, punctuation) is dropped -> cp1252/path safe
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    s = s.strip("-")
    return (s[:maxlen].strip("-")) or "clip"


def norm_niche(value):
    """Normalize a niche string to one of KNOWN_NICHES; unknown -> 'other'."""
    if not value:
        return "other"
    v = str(value).strip().lower().replace("_", "-").replace(" ", "-")
    if v in KNOWN_NICHES:
        return v
    # a few friendly aliases
    aliases = {
        "finance": "finance-motivation", "money": "finance-motivation",
        "motivation": "finance-motivation", "finance-money": "finance-motivation",
        "ai": "software", "tech": "software", "ai-tech": "software", "code": "software",
        "saas": "software", "tool": "software", "ad": "ads", "advertising": "ads",
        "funny": "viral-funny", "viral": "viral-funny", "meme": "viral-funny",
    }
    return aliases.get(v, "other")


def load_manifests(out_dir, source):
    """Yield (stem, manifest_entries) for each <stem>.manifest.json in out/, optionally one source."""
    if source:
        names = [out_dir / f"{source}.manifest.json"]
    else:
        names = sorted(out_dir.glob("*.manifest.json"))
    for mpath in names:
        if not mpath.exists():
            log(f"  WARN: manifest not found, skipping: {mpath.name}")
            continue
        stem = mpath.name[: -len(".manifest.json")]
        try:
            entries = json.loads(mpath.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            log(f"  WARN: could not read {mpath.name}: {e}")
            continue
        if isinstance(entries, list) and entries:
            yield stem, entries


def load_highlights(out_dir, stem):
    """Return {rank: highlight_entry} from data/<stem>.highlights.json (adds score/reason/niche)."""
    hpath = BASE / "data" / f"{stem}.highlights.json"
    if not hpath.exists():
        return {}
    try:
        data = json.loads(hpath.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}
    by_rank = {}
    for h in data if isinstance(data, list) else []:
        if "rank" in h:
            by_rank[h["rank"]] = h
    return by_rank


def pick_variant(out_dir, stem, rank, prefer):
    """Resolve the actual source file to copy.
    prefer='raw' (default) -> <stem>_clip<NN>.mp4 ; prefer='captioned' -> _cap.mp4 if it exists.
    Falls back to whichever exists. Returns (Path, captioned_bool) or (None, False).
    """
    base = out_dir / f"{stem}_clip{rank:02d}.mp4"
    cap = out_dir / f"{stem}_clip{rank:02d}_cap.mp4"
    if prefer == "captioned":
        if cap.exists():
            return cap, True
        if base.exists():
            return base, False
    else:  # raw
        if base.exists():
            return base, False
        if cap.exists():
            return cap, True
    return None, False


def build_readme(dest, counts, total, niche_flag, brief, generated_at):
    """Author the agency one-pager. Plain ascii so it survives any console / editor."""
    lines = []
    lines.append("# Clip Library -- Agency Hand-off")
    lines.append("")
    lines.append(f"Generated: {generated_at}")
    lines.append(f"Total clips staged: {total}")
    lines.append("")
    if brief:
        lines.append("## Brief")
        lines.append("")
        lines.append(brief.strip())
        lines.append("")
    lines.append("## What's in here")
    lines.append("")
    lines.append("Vertical 9:16 (1080x1920) short-form source clips, pre-cut from longer videos and")
    lines.append("ranked by hook strength. Each clip is a self-contained moment ready to re-edit.")
    lines.append("Clips are split into niche subfolders -- each niche is its own brief / footage set.")
    lines.append("")
    lines.append("## Niche breakdown")
    lines.append("")
    for niche in KNOWN_NICHES:
        n = counts.get(niche, 0)
        if n:
            lines.append(f"- **{niche}/** -- {n} clip(s)")
    lines.append("")
    lines.append("## Naming scheme")
    lines.append("")
    lines.append("`<source-slug>__clip<NN>__<short-title>.mp4`")
    lines.append("")
    lines.append("- `<source-slug>` = the original long video this came from")
    lines.append("- `clip<NN>` = rank within that source (01 = strongest hook)")
    lines.append("- `<short-title>` = a human label for the moment")
    lines.append("")
    lines.append("Full per-clip detail (title, hook line, duration, score) is in `_index.csv` and")
    lines.append("`_index.md`. Pick by hook + niche; the index is sortable in any spreadsheet tool.")
    lines.append("")
    lines.append("## Delivery / quality guidance")
    lines.append("")
    lines.append("- These are the **original 1080x1920 H.264 files** -- bit-identical, no re-compression.")
    lines.append("- Pull them as **FILES from this folder** (Dropbox / Google Drive share link).")
    lines.append("- **Never** send or receive these as chat/DM media (iMessage, WhatsApp, Slack inline,")
    lines.append("  platform DMs) -- those apps transcode and degrade quality. Folder files stay clean.")
    lines.append("- Default deliverable is **uncaptioned** source -- clippers re-caption / re-edit anyway.")
    lines.append("  (Captioned variants can be staged on request via `--prefer captioned`.)")
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Stage auto-clip output into a niche-split clip library.")
    ap.add_argument("--out", default="out", help="auto-clip output dir to read from (default: out)")
    ap.add_argument("--dest", default=DEFAULT_DEST,
                    help=f"library destination (default documented OUTSIDE OneDrive: {DEFAULT_DEST})")
    ap.add_argument("--niche", default=None,
                    help="niche for the whole batch (overrides per-clip niche). One of: "
                         + ", ".join(KNOWN_NICHES))
    ap.add_argument("--source", default=None,
                    help="only stage this one source stem's manifest (default: all *.manifest.json)")
    ap.add_argument("--prefer", choices=["raw", "captioned"], default="raw",
                    help="which variant to copy (default: raw = uncaptioned source)")
    ap.add_argument("--brief", default=None, help="optional brief text embedded in the agency README")
    ap.add_argument("--dry-run", action="store_true", help="report what would be staged; copy nothing")
    args = ap.parse_args()

    out_dir = (BASE / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    dest = Path(args.dest)
    dest = (BASE / dest).resolve() if not dest.is_absolute() else dest

    if not out_dir.exists():
        log(f"FATAL: out dir not found: {out_dir}")
        sys.exit(1)

    batch_niche = norm_niche(args.niche) if args.niche else None
    if args.niche and batch_niche == "other" and norm_niche(args.niche) != norm_niche("other"):
        log(f"WARN: unrecognized --niche '{args.niche}' -> filed under 'other'")

    # OneDrive double-sync guard (plan risk): warn (don't block) if dest is inside the OneDrive tree.
    if "onedrive" in str(dest).lower():
        log("WARN: --dest is inside the OneDrive tree -- large MP4s may double-sync. "
            "Prefer a Dropbox/Drive folder outside OneDrive for the real library.")

    log(f"reading clips from: {out_dir}")
    log(f"library dest:       {dest}{'  (DRY RUN -- nothing copied)' if args.dry_run else ''}")
    if batch_niche:
        log(f"batch niche:        {batch_niche} (applied to all clips)")

    # Load any existing library manifest so re-runs accumulate / skip duplicates (idempotent).
    lib_manifest_path = dest / "library.manifest.json"
    existing = {"clips": []}
    if lib_manifest_path.exists():
        try:
            existing = json.loads(lib_manifest_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing = {"clips": []}
    seen = {c.get("file") for c in existing.get("clips", [])}

    rows = []          # full records for this run + carried-over existing
    rows.extend(existing.get("clips", []))
    new_count = 0
    skipped = 0

    for stem, entries in load_manifests(out_dir, args.source):
        highlights = load_highlights(out_dir, stem)
        log(f"source '{stem}': {len(entries)} manifest entr{'y' if len(entries)==1 else 'ies'}")
        for m in entries:
            rank = m.get("rank")
            hl = highlights.get(rank, {})
            # niche precedence: --niche flag > manifest field > highlights field > default 'other'
            niche = batch_niche or norm_niche(m.get("niche") or hl.get("niche"))
            src_file, captioned = pick_variant(out_dir, stem, rank, args.prefer)
            if src_file is None:
                log(f"  WARN: no clip file on disk for {stem} rank {rank}; skipping")
                continue

            title = m.get("title") or hl.get("title") or f"clip{rank:02d}"
            hook = m.get("hook") or hl.get("hook") or ""
            duration = m.get("duration") or hl.get("duration") or ""
            score = hl.get("score", "")
            reason = hl.get("reason", "")

            new_name = f"{slug(stem, 32)}__clip{rank:02d}__{slug(title)}.mp4"
            rel = f"{niche}/{new_name}"
            target = dest / niche / new_name

            if rel in seen:
                skipped += 1
                continue

            rows.append({
                "niche": niche, "file": rel, "source": stem, "clip_no": rank,
                "title": title, "hook": hook, "duration_s": duration,
                "score": score, "reason": reason, "captioned": "y" if captioned else "n",
            })
            seen.add(rel)
            new_count += 1

            if args.dry_run:
                log(f"  [dry] {src_file.name} -> {rel}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, target)  # copy (preserve mtime), NEVER move -- out/ stays intact
            log(f"  staged {src_file.name} -> {rel}")

    if not rows:
        log("nothing to stage (no manifests / no clip files found).")
        sys.exit(0)

    # Counts by niche across the full (accumulated) library.
    counts = {}
    for r in rows:
        counts[r["niche"]] = counts.get(r["niche"], 0) + 1
    total = len(rows)

    if args.dry_run:
        log(f"DRY RUN -- would stage {new_count} new clip(s); {skipped} already present.")
        for niche in KNOWN_NICHES:
            if counts.get(niche):
                log(f"  {niche}: {counts[niche]}")
        return

    dest.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # _index.csv -- flat, sortable catalog.
    csv_cols = ["niche", "file", "source", "clip_no", "title", "hook",
                "duration_s", "score", "reason", "captioned"]
    csv_path = dest / "_index.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig: Excel-friendly
        w = csv.DictWriter(f, fieldnames=csv_cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x["niche"], -float(x["score"] or 0), x["source"], x["clip_no"])):
            w.writerow(r)

    # _index.md -- human-skimmable, grouped by niche.
    md = [f"# Clip Library Index\n", f"Generated: {generated_at}  |  Total clips: {total}\n"]
    for niche in KNOWN_NICHES:
        group = [r for r in rows if r["niche"] == niche]
        if not group:
            continue
        md.append(f"\n## {niche} ({len(group)})\n")
        md.append("| title | hook | duration | source | niche | score |")
        md.append("|---|---|---|---|---|---|")
        for r in sorted(group, key=lambda x: -float(x["score"] or 0)):
            hook = str(r["hook"]).replace("|", "/").replace("\n", " ")
            title = str(r["title"]).replace("|", "/")
            dur = f"{r['duration_s']}s" if r["duration_s"] != "" else ""
            md.append(f"| {title} | {hook} | {dur} | {r['source']} | {r['niche']} | {r['score']} |")
    md_path = dest / "_index.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    # README-for-agency.md
    readme = build_readme(dest, counts, total, batch_niche, args.brief, generated_at)
    (dest / "README-for-agency.md").write_text(readme, encoding="utf-8")

    # library.manifest.json -- machine record (idempotent accumulation).
    lib_manifest = {
        "generated_at": generated_at,
        "dest": str(dest),
        "counts_by_niche": counts,
        "total": total,
        "clips": rows,
    }
    lib_manifest_path.write_text(json.dumps(lib_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"DONE -- staged {new_count} new clip(s) ({skipped} already present); library total {total}.")
    log("Counts by niche:")
    for niche in KNOWN_NICHES:
        if counts.get(niche):
            log(f"  {niche}: {counts[niche]}")
    log(f"Index: {csv_path.name}, {md_path.name}  |  README-for-agency.md  |  library.manifest.json")
    log("STAGED ONLY -- not uploaded/shared/published (CLAUDE.md rule 1). "
        "Elijah creates/sends the share link himself; deliver FILES in a folder, never chat media.")


if __name__ == "__main__":
    main()
