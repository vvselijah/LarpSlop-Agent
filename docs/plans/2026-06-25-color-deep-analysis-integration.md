# Plan — Color engine: deep frame-by-frame re-analysis → iterate & integrate (2026-06-25)

**Owner:** agent (autonomous, DRAFT-only) · **Trigger:** Elijah — *"the color grading agentic workflow is not
fully finished. Did you actually watch every single video and look at every frame vs everything they said?
Create a plan of how you can iterate and integrate."*

**Honest answer to his question: NO, the first pass did not.** This plan fixes that, then closes the loop into
the engine. Rules from the autonomous charter still bind: local-only, stops at `out/`, never publishes/commits-push,
run via `auto-clip\.venv`, permissive deps. Gemini/AI-provider wiring stays Elijah-gated.

---

## 1. The honest verdict (why it's not finished)

The masterclass research (`docs/research/color-masterclass/`) was a **transcript-led survey with sparse visual
spot-checks**, not an exhaustive watch:

- **Frames: 50 evenly-spaced per video, regardless of length** (`acquire.py`). On the 107-min course that's **1 frame
  every ~128 s**; ~700 frames across **7.7 hours**. A colorist makes dozens of scope/wheel/node moves per minute — at
  1 frame / 2 min you miss virtually all of the *demonstrated* technique.
- **Transcript collapsed to 15-second windows** (not word-level), then handed to each agent as "transcript + ~25 frames
  → write a summary." So it read **every word but only glanced at the screen**, and **never fused** "at this second they
  said X while the scope showed Y and the wheel sat at Z."
- Result: `synthesis.md` is strong **consensus *theory*** — but its numbers (skin 40-50 IRE, pivot 0.336, blacks ~0) are
  **textbook values the model already knew**, not parameters *read off the colorists' actual demonstrations*. (It even
  leaked an agent preamble on line 1.) We have the philosophy; we're missing the **demonstrated, parameter-level craft.**

**Proof it's recoverable:** the 16 source videos (~1.4 GB) and the word-level `.vtt`s are still on disk. A single
densely-sampled frame (`qualifier-tricks` @ 02:09) is fully legible: node tree **EX→WB→LUT**, Log-wheels **Contrast
1.104 / Pivot 0.435 / Offset 16.05 / Sat 50.00**, live waveform — exactly the craft the sparse pass couldn't see.

---

## 2. The fix — a validated dense-fusion pipeline (DONE, de-risked)

`docs/research/color-masterclass/acquire_dense.py` (stdlib + cv2, no OCR dep — vision agents read frames directly):

1. **Dense sample** at 1 fps (one look per second, not per 2 min).
2. **Perceptual dedup** (dHash + Hamming ≥ 10): collapse static UI holds, **keep every frame where the screen
   meaningfully changed** — the moments of demonstrated action.
3. **Word-level fusion**: canonical overlap-merge of the rolling `.vtt` → each spoken word once, at its real time;
   attach the words in `[t−2.5s, t+2.5s]` to each kept frame.

Output per video: `dense/frames/f####_<mmss>.jpg` + `dense/fused.jsonl` (`{idx,t,mmss,frame,said}`) + `summary.json`.

**Validated on `qualifier-tricks`:** 423 raw → **64 distinct timestamped states (15%)**, 1,318 clean time-aligned words.
Full 14-video extraction is **running in the background now**.

---

## 3. Phase 1 — Deep re-analysis (the genuine "watch everything" pass)

A **Workflow** (pipeline, one lane per video; fan vision agents over ~5-min segments so each reads a tractable batch):

- **Stage A — per-segment extraction:** each agent gets a segment's deduped frames + the exact `said` text and returns
  **structured, frame-evidenced findings**: every technique shown, with the *demonstrated* params (node label/order,
  wheel/curve/qualifier values, scope readings, pivot/offset/sat numbers, the exact on-screen state). Schema-forced JSON.
  Each claim cites `mmss` + frame.
- **Stage B — per-video synthesis:** merge a video's segments into one technique sheet (what THIS authority does, with
  numbers), flagging anything that contradicts or refines `synthesis.md`.
- **Stage C — corpus synthesis + adversarial pass:** merge all 14; for each "new/contradictory" claim, an independent
  verifier re-reads the cited frame to confirm it's really shown (kill hallucinated params). Produce:
  - `extracted/synthesis_v2.md` — the consensus, now backed by **demonstrated** numbers + dispute knobs.
  - `extracted/engine_gap_map.json` — every technique mapped to: *already in engine / partial / missing*, with the
    concrete `colorkit` change and a priority.

**Scale guard:** `log()` any video/segment dropped; no silent truncation.

---

## 4. Phase 2 — Engine gap-map (pre-identified; Phase 1 confirms/extends)

From reading the current engine against `synthesis.md` §4. Priority = value for a **talking-head AI/money creator**.

| # | Gap | Where | Priority |
|---|---|---|---|
| **G1** | **Skin-tone solver** — measure the skin cluster's angle vs the **~123° I-line** + IRE, drive WB so skin lands on/just-under, **minimise cross-clip variance**. Today: generic Shades-of-Gray WB (`correct.py`), `scene_stats` only counts `skin_frac`. | `correct.py` + `measure.py` | **P0 (headline)** |
| **G2** | **Scope self-validation harness** — headless waveform / parade / vectorscope; assert the §4.10 checklist (neutrals→equal RGB, no 0/1023 clip, **mean-luma-unchanged after sat**, skin angle/IRE variance < threshold). Makes the engine *provably* correct + is the QA rig for every other gap. | new `scopes.py` | **P0** |
| **G3** | **Look = stacked effects** — add **halation** (red-weighted highlight blur, ADD in linear), **grain** (shadows/mids), **vignette**, **density** as composable toggles; feed print-emulation looks **log, not Rec.709**. Today: looks are split-tone + curve only. | `luts.py` / `stylize.py` | **P1** |
| **G4** | **Wide working-space transform** — do the develop in a DWG/ACES-analog wide gamut w/ highlight gamut-compression, not linear-sRGB. Matters most for the **Insta360 I-Log** path. | `correct.py` / `tonemap.py` | **P1** |
| **G5** | **Parade / skin-consistency shot matching** — upgrade beyond global Reinhard mean/std to per-tone-band (shadow/mid/high) alignment + a skin-consistency objective. | `match.py` | **P2** |
| **G6** | **Luma-safe saturation assertion** — prove (and fail closed) that vibrance/sat doesn't raise mean luma. | `correct.py` + `scopes.py` | **P2** |
| **G7** | **Contrast judged at sat=0 / pivot reconciliation** — auto-tune contrast on a desaturated copy; reconcile 0.18-linear vs 0.336-DWG / 0.435-Rec709. | `correct.py` | **P3** |

---

## 5. Phase 3 — Integration loop (per gap, highest-value first)

For each gap, run the hub's CODE loop (dev-workflow): one-line plan → build the slice → **TEST by actually grading
Elijah's real footage** (`a test.mov`, the I-Log `i log vid.mp4`, an HLG clip, a photo) → make before/after + v2-vs-new
montages and **read the PNG**; check the new `scopes.py` targets → fix → loop until genuinely better. Regression-guard:
the **approved well-exposed look stays byte-stable** unless a gap intends to change it. Order: **G1 → G2 → G3 → G4 → G5
→ G6 → G7.** G2 lands early so G1/G3/G4 are validated against real scope numbers, not just the eye.

---

## 6. Phase 4 — QA, docs, memory

- Full pytest pass + a new regression test pinning the approved develop.
- Rewrite `synthesis_v2.md` into the engine spec + refresh the vault zero-to-hero guide with the **demonstrated**
  findings (and a "demonstrated vs textbook" column).
- Update `COLOR-BUILD-STATUS.md`, `[[project-color-engine]]`, append one dated learning to `team/memory.md`.
- **Sync decision (Elijah-gated):** fold the result into `Desktop\colorkit` + commit? — still his call.

---

## 7. Optional follow-on — the AI decision layer

The deep technique sheets are the ideal grounding for `decide.suggest_look_ai` (still a sketch). Wiring a real
provider (Claude-vision agent → Pegasus → Gemini) is **Elijah-gated** (external call/cost) and stays out of scope here.

---

## 8. Scope / honesty

Phase 1 is one background Workflow (hours of agent time, no gates). Phase 3 is the real work — **multi-session**, one
verified gap at a time. Nothing here publishes, commits-push, or spends. Success = the engine demonstrably grades
Elijah's footage better (skin on the line + consistent across clips, scopes pass, looks read *filmic* not *tinted*),
proven on his real footage, not asserted.
