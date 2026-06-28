# Color-grading research — HANDOFF (continue in a fresh conversation)

**Purpose:** complete the frame-by-frame analysis of the FULL color-grading source list (Elijah's vault note
`60-Life/Personal masterclasses/Color grading, color correction, and color theory.md`) and merge it into the
master methodology. This doc is self-contained — a new conversation/environment can execute it without prior
context.

**Last updated:** 2026-06-26.

---

## 1. What is DONE (do NOT re-analyze)

**14 named-colorist masterclasses** fully analyzed frame-by-frame (1 fps → perceptual-dedup → word-level
transcript fusion → vision-agent technique extraction). Output already produced:
- `extracted/synthesis_v2.md` — the demonstrated-evidence methodology (the engine spec).
- `extracted/engine_gap_map.(md|json)` — 17 techniques mapped to the colorkit engine (P0–P3) + 5 flagged claims.
- `extracted/studies.json` / `per-video-v2/*.md` — per-video technique sheets.
- Raw + dense frames live under `raw/<slug>/` and `raw/<slug>/dense/` (2,498 kept frames, 1,363 techniques).

**The 14 done (YouTube IDs — dedup new downloads against these):**
`YbDRl_xugJo, rPE1AXKGjgM, itli8isoXQQ, vt1T9h_vAqY, 35wo8eVikqA, wvPkoL8nx-I, kdTMRQP_V7E, z7PFk8vYSxs,
NnNqjPbfIG8, 6qJzzwkttrk, -oGA1ayemUY, YRo8b6AJtaM, IBwLq8vtfJ4, 45z60vnPOBw`
(= Mostyn ×3, Cullen Kelly ×3, Frenchie, Mullins, film-emulation, qualifier-tricks, 2 beginner courses, BBC node-tree.)

> Of the vault note's *individual* links, only `itli8isoXQQ` and `IBwLq8vtfJ4` were in the done set. Everything
> else below is NEW.

---

## 2. What REMAINS (the work)

### 2a. Individual videos from the note — 11 unique, NOT analyzed (highest priority; likely named-colorist)
```
https://www.youtube.com/watch?v=22mmIgWIcvE
https://youtu.be/Zh3QYgCXQGw
https://youtu.be/hvwQIQcXFbI
https://www.youtube.com/watch?v=MCDVcQIA3UM
https://youtu.be/3g8TA5n92Bs
https://youtu.be/llmycBwcTD4
https://youtu.be/SkosqJfzEs0
https://youtu.be/pPzhzkPWxkg
https://youtu.be/vGrnJeIMyQQ
https://youtu.be/nSNBtl8cOl8
https://youtu.be/-MrHvGoq9lY
```

### 2b. Playlist 1 — `PLNLA7EsgTsU5lzs9Fy-OhsybeY_uXZRfx` — 46 videos ("DaVinci Resolve 20" full course)
- **Color-relevant subset (recommended): Classes 24–39** = color overview, node tree, color-correction basics,
  curves, qualifier, color slice, windows, keyframing, LUTs, LOG grading, film-look LUTs, PowerGrade, Magic Mask,
  **Halation Tool (Class 37)**, Noise Reduction, **Film Grain (Class 39)**. *(Class 37 Halation + Class 39 Film
  Grain directly feed engine gap G3 — texture stack.)*
- **Skip for color research:** Classes 1–23 (editing/UI/media/audio/subtitles) and 40–46 (Fusion/green-screen/maps)
  — not color grading. Analyze only if Elijah wants *literally* every video.

### 2c. Playlist 2 — `PL2HeOArLswsUmXRtQe9tk_utN2UX46Nm1` — 25 videos (Hindi DaVinci color course, Classes 01–25)
- **All 25 are color-grading** (nodes, primaries, curves, Hue-vs-Hue/Sat/Lum, power windows, tracker, Magic Mask,
  layer/parallel/key/shared mixers, stills/PowerGrade, versions, groups, local-vs-remote, **CST/Color Space
  Transform**). Strong on node mixers + CST (gap G4).
- **CAVEAT: audio is Hindi.** The visual demonstrations (UI/scopes/values) are the signal anyway — the vision pass
  reads those. Word-level transcript fusion may be Hindi (yt-dlp auto-subs); set `--sub-langs en` to try the
  English auto-translation track, else rely on the frames. Flag any technique where the spoken context was unclear.

**Re-enumerate any playlist anytime:**
`yt-dlp --flat-playlist --print "%(id)s | %(title)s" "https://www.youtube.com/playlist?list=<ID>"`

**Recommended scope (decide with Elijah):** all 11 individuals + Playlist-2 (25) + Playlist-1 color subset (~16)
≈ **~52 new videos**. "Literally every video" adds Playlist-1's ~30 non-color classes (low value for grading).

---

## 3. The METHOD (exact pipeline — already built, reuse it)

Run from `docs/research/color-masterclass/` with the auto-clip venv:
`$py = "C:\Users\elija\OneDrive\Desktop\ai agent team\auto-clip\.venv\Scripts\python.exe"`

1. **Add the new IDs** to the `VIDEOS` list in `acquire.py` (give each a `slug`, `category`, `note`). Then
   download transcripts + 720p copies + 50 nav frames:
   `& $py acquire.py <slug1> <slug2> ...`  (it skips nothing; pass slugs to limit). Dedup: don't re-add the §1 IDs.
2. **Dense extract** (1 fps → dHash dedup → word-level fusion) — the real analysis frames:
   `& $py acquire_dense.py --fps 1 --hamming 10`  (processes every `raw/<slug>/` lacking `dense/`; safe to re-run).
3. **Build vision batches** (≤20 frames each):
   `& $py build_batches.py --batch 20`  → writes `raw/<slug>/dense/batches/*.md` + `raw/batches_index.json`.
4. **Run the vision workflow** (the parent `Workflow` tool, ultracode). Reuse the saved script
   `color-masterclass-deep` (run id `wf_015b4b41-129`) — update its inline `VIDEOS` array to the NEW slugs +
   their `n_batches` (from step 3's index). It fans a vision agent per batch → per-video sheets → corpus
   synthesis + gap map. **Gotcha:** last run lost 7/130 batches to transient API rate-limits — re-run those
   batches or resume; pace the fan-out.
5. **Persist + MERGE:** `& $py persist_results.py <workflow-output.json>` writes `extracted/synthesis_v2.md`,
   `engine_gap_map.*`, `per-video-v2/*.md`. **Do not overwrite — MERGE**: fold new demonstrated params into the
   existing `synthesis_v2.md` and add new gap-map rows; keep the disputes-as-knobs structure.

**Quality bar (non-negotiable):** capture EXACT on-screen demonstrated values (node order, wheel/curve/pivot/sat
numbers, scope readings), cite `mm:ss` + frame; never invent a value; adversarially re-check surprising claims
against the cited frame (the 5 `flagged_claims` in `engine_gap_map.json` are the pattern — Resolve's Offset wheel
reads "25 = neutral", so several "demonstrated" numbers are scale-confusions).

---

## 4. Why this matters / where it lands
The output feeds the **colorkit engine gap map** (see `extracted/engine_gap_map.md`) — especially the still-open
P1/P2 items: **G3 film texture (halation/grain/vignette)** (Playlist-1 Classes 37/39 are direct demos) and
**G4 wide-gamut/CST** (Playlist-2 Class 25). New techniques → new/updated gap-map rows → engine work.
**Also now relevant:** Elijah owns **DaVinci Resolve Studio** — this corpus IS DaVinci technique, so it doubles as
his hand-grading reference (the vault `40-Projects/LarpSlop/Color-Grading-Masterclass/` teaching guide).
