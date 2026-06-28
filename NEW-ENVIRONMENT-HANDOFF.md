# NEW-ENVIRONMENT HANDOFF — Color-Grading Masterclass Deep Analysis (2026-06-26)

**For:** continuing this work in a DIFFERENT environment / DIFFERENT Claude account (the original account is
about to hit its weekly usage limit). This doc is **self-contained** — a fresh session can execute it cold.

**One-line status:** Pass 1 (11 individual masterclasses) is **fully extracted, all 11 per-video sheets written
to disk**; only the final *merge* into the master synthesis is left (one cheap step). Passes 2 & 3 (71 playlist
videos) are **downloaded + dense-extracted + batched and ready for vision** (245 batches). Nothing is lost.

---

## 0. WHERE I WAS WHEN CUT OFF
Running the Pass-1 vision workflow (resume). It re-ran the full extraction and **wrote all 11 per-video sheets to
`docs/research/color-masterclass/per-video-v2/`** (2,977 techniques, 0 batches failed). The **only** thing that
failed was the very last step — the single `merge` agent that folds those 11 sheets into `synthesis_v2.md` +
`engine_gap_map.*` — which hit the account session cap. So: extraction ✅, sheets ✅, **merge ❌ (1 step left)**.

---

## 1. WHAT THIS PROJECT IS
Complete the frame-by-frame analysis of Elijah's FULL color-grading source list (vault note
`60-Life/Personal masterclasses/Color grading, color correction, and color theory.md`) and MERGE the demonstrated
techniques into the master methodology that grounds the **colorkit** auto-grading engine
(`auto-clip/colorkit/`). Output lives in `docs/research/color-masterclass/`:
- `extracted/synthesis_v2.md` — the demonstrated-evidence methodology (engine spec).
- `extracted/engine_gap_map.(md|json)` — techniques mapped to engine modules (P0–P3) + flagged claims.
- `per-video-v2/<slug>.md` — one demonstrated-technique sheet per video (exact values + `mm:ss` cites).
- `raw/<slug>/dense/` — kept frames + fused transcript + batch briefs per video.

Elijah's decision for scope: **"full everything" (all 82 videos), paced across usage windows.**

---

## 2. CURRENT STATE (counts are exact)

### DONE & DURABLE ON DISK
- **14 original masterclasses** — analyzed + already in `synthesis_v2.md` (Mostyn ×3, Cullen ×3, Frenchie, Mullins,
  film-emulation, qualifier, 2 beginner courses, BBC node-tree).
- **11 individual videos (Pass 1)** — acquired → dense (7,723 kept frames, 393 batches) → **vision-extracted
  (2,977 techniques) → all 11 sheets WRITTEN** to `per-video-v2/`:
  `lenz-most-important-concept, wampus-pro-seminar, euro-pro-level-64min, faris-full-course-2026,
  jenkinson-exact-system, qazi-start-here, batal-conquer-color-page, benkabouche-1h-master,
  neistadt-ultimate-guide, content-creators-indepth, editing-explained-2hr`.
- **71 playlist videos (Pass 2 + 3)** — downloaded + dense-extracted + batched, in `raw/pl2-cNN/` and
  `raw/pl1-cNN/`, indexed in `raw/batches_index.json`:
  - **PL2 (Hindi color course, 25 classes)** = `pl2-c01..pl2-c25` → 1,110 frames, **66 batches** (Pass 2).
  - **PL1 (DaVinci Resolve 20 course, 46 classes)** = `pl1-c01..pl1-c46` → 3,159 frames, **179 batches** (Pass 3).

### PENDING (3 steps, in order)
1. **Pass 1 MERGE** — fold the 11 written sheets into `synthesis_v2.md` + `engine_gap_map`. CHEAP (1 agent). The
   sheets already exist; **do NOT re-extract**.
2. **Pass 2 vision** — `pl2-*` (66 batches): extract → sheets → merge.
3. **Pass 3 vision** — `pl1-*` (179 batches): extract → sheets → merge (may need 2 sub-passes / a resume).

### KNOWN POLLUTION TO CLEAN (handled automatically by the merge prompt's "step 0")
`synthesis_v2.md` (~19,831 chars) + `engine_gap_map.*` still carry bookkeeping from an earlier failed merge:
a gap row id `pending-vision-analysis-10-videos` + a `MERGE-PROCESS FLAG` flagged_claim + a "pending work" note in
the synthesis. The merge step removes these (it's instructed to).

---

## 3. HOW TO CONTINUE IN THE NEW ENVIRONMENT

### Prereqs
- The project folder synced/copied, **including `docs/research/color-masterclass/raw/<slug>/dense/`** (the frames
  the vision agents read). The big `.mp4` files are NOT needed for vision (frames + batch briefs are) — only
  needed if you must RE-dense (see §5).
- Python venv with `opencv-python` + `numpy` (this repo uses `auto-clip/.venv`); `ffmpeg`/`ffprobe` on PATH.
- Claude Code with the **Workflow** tool (this is multi-agent; the workflow fans vision agents per batch).
- For re-downloading only (§5): `yt-dlp` + `curl_cffi` (impersonation) + `node` (JS runtime for nsig). Install:
  `pip install -U yt-dlp curl_cffi` into the venv; Node.js on PATH.

> Let `$py = <venv python>`. On the original machine that was
> `C:\Users\elija\OneDrive\Desktop\ai agent team\auto-clip\.venv\Scripts\python.exe`. Adjust for the new machine.

### STEP 0 — regenerate batch briefs with LOCAL paths (REQUIRED if the folder moved/synced)
The batch briefs (`raw/<slug>/dense/batches/*.md`) and `raw/batches_index.json` contain ABSOLUTE frame paths from
the original machine. Re-run to rewrite them for THIS machine (reads `dense/fused.jsonl`, cheap, no model):
```
cd docs/research/color-masterclass
$py build_batches.py --batch 20
```

### STEP 1 — finish Pass 1's merge (cheap, ONE agent — do NOT re-extract)
Run the **merge-only** workflow over the 11 already-written sheets:
```
Workflow({
  scriptPath: "<...>/docs/research/color-masterclass/merge-only.workflow.js",
  args: { base: "<abs path to docs/research/color-masterclass>",
          new_slugs: ["lenz-most-important-concept","wampus-pro-seminar","euro-pro-level-64min",
            "faris-full-course-2026","jenkinson-exact-system","qazi-start-here","batal-conquer-color-page",
            "benkabouche-1h-master","neistadt-ultimate-guide","content-creators-indepth","editing-explained-2hr"] }
})
```
Verify: `synthesis_v2.md` grew, still has its original numbered sections + the "Disputes…" section; the bookkeeping
row/flag are gone; `engine_gap_map.json` has ≥17 rows.

### STEP 2 — Pass 2 (PL2 Hindi, 66 batches)
Get the args, then run the full vision workflow (extract → sheet → merge):
```
$py make_args.py pl2     # prints the args JSON (portable; recomputes local paths)
Workflow({ scriptPath: "<...>/docs/research/color-masterclass/color-deep.workflow.js", args: <paste pl2 args> })
```

### STEP 3 — Pass 3 (PL1 DR20, 179 batches)
```
$py make_args.py pl1
Workflow({ scriptPath: "<...>/docs/research/color-masterclass/color-deep.workflow.js", args: <paste pl1 args> })
```
179 batches may exceed one usage window. If it stops mid-run with sheets written but merge unfinished, finish with
`merge-only.workflow.js` (new_slugs = the pl1 slugs whose sheets exist). If it stops mid-extraction, the cleanest
recovery in a fresh env is to re-run the workflow (it re-extracts; cross-session resume cache is NOT portable —
see §6). To keep within a window, you can split: `make_args.py` then hand-trim the `videos` array to ~half.

**Run order matters:** do STEP 1 before STEP 2 before STEP 3, so each pass's merge folds into the
already-updated synthesis (the merge reads the current synthesis + only its own new sheets).

---

## 4. THE ARTIFACTS (all under `docs/research/color-masterclass/`)
- `color-deep.workflow.js` — the reusable vision pass (extract per batch → per-video sheet → additive MERGE).
  args = `{base, videos:[{slug,note,batches_dir,n_batches}]}`. Self-corrects if args arrive as a JSON string.
- `merge-only.workflow.js` — NEW: cheap merge of already-written sheets (args = `{base, new_slugs:[]}`).
- `make_args.py` — NEW: prints portable `args` JSON for `pl1` / `pl2` / `individuals`.
- `acquire.py` — downloads the 14 + 11 individuals (VIDEOS list). `acquire_playlists.py` — downloads PL1+PL2 with
  yt-dlp `--impersonate chrome --js-runtimes node` (beats the 429/403s). `acquire_dense.py` — 1fps → dHash dedup →
  word-level transcript fusion. `build_batches.py` — chunks fused.jsonl into ≤20-frame vision briefs.
- `persist_results.py` — LEGACY; it **overwrites** (clobbers sheets + synthesis). **Do not use for incremental
  merges** — the workflows write/merge directly instead.
- `RESUME-PASS1-BATON.md` — the earlier same-session resume baton (now superseded by this doc for cross-env).

---

## 5. IF `raw/<slug>/dense/` DID NOT SYNC (must re-acquire)
Everything is re-derivable from YouTube with the scripts (no model tokens for this part):
```
cd docs/research/color-masterclass
$py acquire.py <the 11 individual slugs>     # or omit args to (re)do all in acquire.py VIDEOS
$py acquire_playlists.py                      # PL1 + PL2 (idempotent; skips dirs that already have an mp4)
# dense-extract (tier fps for the long ones): individuals as before, playlists at fps 1
$py acquire_dense.py --fps 1  <short slugs>
$py acquire_dense.py --fps 0.5 wampus-pro-seminar content-creators-indepth editing-explained-2hr
$py acquire_dense.py --fps 0.33 faris-full-course-2026
$py build_batches.py --batch 20
```
Frame-only caveat: `editing-explained-2hr` + ~17 playlist classes have NO transcript (YouTube sub 429s; no local
Whisper). They were analyzed FRAMES-ONLY via a minimal stub `.vtt`. PL2 is Hindi audio anyway (frames carry the
demo). This is acceptable; transcripts are supporting context, not required for technique extraction.

---

## 6. COST / OPERATIONAL LESSONS (learned the hard way this session)
- **Each big vision pass ≈ a full usage window.** Pass 1 (393 batches) = ~24–27M subagent tokens / 416 agents /
  ~42 min and exhausted the session cap. The playlists are cheaper: Pass 2 (66) + Pass 3 (179) = 245 batches
  combined < Pass 1, so they may fit in ~1–2 windows. **Plan one large pass per usage window.**
- **Cross-session resume cache is NOT portable.** `Workflow({resumeFromRunId})` only works in the SAME session on
  the SAME machine (journal under `~/.claude/projects/.../subagents/workflows/<runId>`). In a NEW env you cannot
  resume — but you don't need to, because the valuable output (the per-video sheets) is on disk. Re-run or
  merge-only from the sheets instead.
- **Resume cache also missed on the concurrent pipeline** even same-session (it re-extracted rather than reusing).
  So: prefer letting a pass finish; if it dies after sheets are written, use `merge-only` (don't re-extract).
- **Vision agents read images = the dominant cost** (≈ total kept frames). To cut cost: raise dedup `--hamming`
  (fewer near-dup frames) — batch size only changes agent count, not image-token cost.
- **YouTube download hardening:** the standalone `yt-dlp.exe` lacked impersonation (persistent sub 429s) and a JS
  runtime (video-data 403s). Fix that paid off: `pip install yt-dlp curl_cffi` in the venv + Node on PATH, then
  `--impersonate chrome --js-runtimes node`, and DECOUPLE video from subs (a sub 429 shouldn't cost the video).
- **`acquire_dense.py` picks the first `*.mp4` in a dir** — don't leave stray audio-only `.mp4`/`.m4a` next to the
  real video (it'll extract 0 frames from the audio file).

---

## 7. WHY THIS MATTERS / WHERE IT LANDS
Feeds the **colorkit engine gap map** — esp. still-open items **G3 film texture (halation/grain/vignette)** (PL1
Classes 37 Halation / 39 Film Grain are direct demos) and **G4 wide-gamut/CST** (PL2 Class 25 CST; Qazi's CST
sandwich already captured). Also doubles as Elijah's DaVinci Resolve Studio hand-grading reference (vault
`40-Projects/LarpSlop/Color-Grading-Masterclass/`). New demonstrated params → new/updated gap-map rows → engine work.
Engine state + this research are summarized in the auto-memory `project-color-engine`.

---

## 8. BROADER PROJECT CONTEXT (so a fresh env can pick up the WHOLE hub, not just this thread)
This color-masterclass work is ONE active thread inside Elijah's "AI Agent Team" hub. On opening the folder in a
new environment, read these (all present in the synced project folder):
- **`CLAUDE.md`** (repo root) — the read-first routing map for the entire hub (content, analytics, ads, vault,
  engines, skills, standing rules). START HERE.
- **`HANDOFF.md`** (repo root) — master ops state + history + token-renewal (§4).
- **`team/profile.md` / `team/stats.md` / `team/memory.md`** — the context system (who Elijah is, live numbers,
  accumulated learnings; newest learning = this session's color/cap/yt-dlp lessons).
- **Auto-memory** at `<user>/.claude/projects/.../memory/MEMORY.md` + files (e.g. `project-color-engine`,
  `project-agent-team-hub`) — NOTE: auto-memory is per-account/machine and will NOT travel to a new account; the
  in-folder docs above are the portable record. Re-seed memory in the new env from `team/memory.md` + this doc.
- **The colorkit engine itself:** `auto-clip/colorkit/` (+ hub-root `colorkit/`), tracker
  `auto-clip/COLOR-BUILD-STATUS.md`. Recent engine work (G1 skin-solve, G3 look-stack) is logged in the
  `project-color-engine` memory + `SESSION-COMPACT-2026-06-26-g1-resolve.md`.
- **Standing rules (non-negotiable, from CLAUDE.md):** never publish/post/DM without per-action OK; secrets only
  in Windows env vars (this tree syncs to OneDrive); DRAFT-only by default.

**STATUS OF THIS SESSION'S OTHER SIDE-EFFECTS:** installed `yt-dlp` + `curl_cffi` into `auto-clip/.venv` (new
deps; harmless, used for downloads). No production engine code changed. No git commits made. No publishing. The
only corpus files still mid-update are `synthesis_v2.md` + `engine_gap_map.*` (awaiting the Pass-1 merge in §3).
