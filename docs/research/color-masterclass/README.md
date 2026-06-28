# Color-Grading Masterclass Research — index

**Started:** 2026-06-24 (overnight, Elijah's P0 request). **Goal:** give the agent (and Elijah) a
*true, durable* understanding of professional DaVinci Resolve color-grading methodology — the science
and the workflow — by deeply analyzing the best-reviewed YouTube masterclasses (visuals + audio, not
just transcripts), cross-referencing for consensus, and compiling it into:
1. a zero-to-hero teaching guide in the Obsidian vault (`40-Projects/LarpSlop/Color-Grading-Masterclass/`) — for learning + a sellable IG product,
2. an engine-facing best-workflow doc (`COLOR-GRADING-METHODOLOGY.md`, here) that grounds the agentic color pipeline,
3. durable memory files so the knowledge persists across sessions.

## Why this method (no Gemini)
The Gemini API key is quota-exhausted (`limit: 0`, free tier) — so "watch with Gemini" is out. Instead
this is **fully local + quota-free**: `yt-dlp` pulls each video's auto-captions (every spoken second) +
a 720p copy; `ffmpeg` extracts ~50 evenly-spaced frames (UI/scopes/node-trees are fully legible at
1280px — verified); then vision-capable agents (Claude) READ the frames + transcript to extract the
real on-screen methodology. `acquire.py` does the acquisition; `analyze.*` workflow does the analysis.

## Curated curriculum (top-reviewed authorities)
Reddit r/colorists + r/davinciresolve consensus picks: **Darren Mostyn** ("World Class", UK broadcast,
20yr BBC/Netflix) and **Cullen Kelly** (the technical/color-science authority), plus comprehensive,
skin, secondaries, film-emulation, and philosophy sources.

| slug | category | source |
|------|----------|--------|
| mostyn-color-page-intro | fundamentals | Darren Mostyn — NEW to DaVinci? Color Grading |
| beginners-guide-grading | fundamentals | Beginner's Guide to Colour Grading |
| 2hr-beginner-course | fundamentals | How To Color Grade for Beginners (2hr) |
| mostyn-read-scopes | scopes | How Pro Colorists Read Scopes ft Darren Mostyn |
| cullen-master-scopes | scopes | Cullen Kelly — Master Scopes Inside DaVinci |
| mostyn-perfect-node-tree | nodes | Darren Mostyn — My Perfect Node Tree |
| best-node-tree-any-camera | nodes | BEST Node Tree for ANY Camera (BBC pro) |
| grading-too-complicated | color-mgmt | Has Colour Grading Got Too Complicated? (color mgmt) |
| cullen-36-project-settings | color-mgmt | Cullen Kelly — 36 Project Settings |
| cullen-contrast-cinematographer | primaries | Cullen Kelly — contrast secrets for cinematographers |
| qualifier-tricks | secondaries | BEST Pro Colorist Qualifier Tricks |
| frenchie-masterclass | look-design | Frenchie — Pro Colorist Reveals all (MASTERCLASS) |
| mullins-grading-philosophy | look-design | Mitchell Mullins — Color Grading Mastery philosophy |
| film-emulation-16-35mm | look-design | Emulating 16mm/35mm Film |

## Layout
- `raw/<slug>/` — `transcript.txt` (timestamped), `frames/f###.jpg`, `meta.json` per video.
- `raw/manifest.json` — what acquired successfully.
- `per-video/<slug>.md` — the structured analysis of each video (from the workflow).
- `CONSENSUS.md` — universal truths vs disputed vs single-source (cross-referenced).
- `COLOR-GRADING-METHODOLOGY.md` — the engine-facing synthesis (feeds the v2 color pipeline).

## Status — ✅ COMPLETE (2026-06-24)
- [x] Pipeline validated (yt-dlp + ffmpeg frames legible; Gemini ruled out on quota `limit:0`).
- [x] Acquisition: 14/14 videos, 50 frames + transcript each (`acquire.py`, `raw/manifest.json`).
- [x] Per-video deep analysis: 14 vision agents read transcript + ~25 frames each (`analyze-masterclasses.js` + `backfill-studies.js`) → `extracted/studies.all.json`, `per-video/*.md`.
- [x] Consensus + methodology synthesis: `CONSENSUS.md` (15 universal truths, 11-step workflow, 12 scope targets, 6 disputes, 15 engine implications) + `COLOR-GRADING-METHODOLOGY.md` (engine-facing + teaching).
- [x] Obsidian zero-to-hero guide: 12 chapters in `40-Projects/LarpSlop/Color-Grading-Masterclass/` + 95 screenshots in `screens/` (all 33 embeds verified).
- [x] Memory: `reference_color_grading_method.md` + `project_color_engine.md` (durable across sessions).

**Next:** fold the consensus into the v2 engine (color-management/CST-sandwich already partly there via `--input-lut`; validate exposure-to-mid-grey, luma-safe sat, skin-line, film-LUT-needs-log). Then resume the v2 build (looks rebuild, montages, repo extraction).
