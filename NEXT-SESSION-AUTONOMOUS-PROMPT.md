# NEXT-SESSION AUTONOMOUS PROMPT — paste this into the fresh session

You are operating **autonomously overnight** while Elijah sleeps. Your job is to **make the color-grading engine
genuinely great and ship it as its own repo** — building, testing, verifying, researching the best next step, and
**looping** without waiting for input. Work in **ultracode** mindset: be exhaustive and correct, use Workflows for
substantive research/fan-out, adversarially verify your own work, and keep going until the mission is done or you hit a
hard Elijah-gate. Do NOT stop after one step — loop.

## 0. Orient (read first, in order)
1. `SESSION-COMPACT-2026-06-24.md` (state + the v2 plan)
2. `docs/plans/2026-06-23-agentic-color-pipeline.md` and `auto-clip/COLOR-BUILD-STATUS.md`
3. `obsidian/Elijah's vault/40-Projects/LarpSlop/Working on.md`
4. The v2 spec: `docs/plans/2026-06-24-color-v2-grading-spec.md`. **If it doesn't exist**, get it first: read the
   `pro-grade-craft-research` workflow output (run id `wf_7107b183-886`) from the task output files, OR re-run that
   workflow (`.../workflows/scripts/pro-grade-craft-research-*.js`), then synthesize the spec into that plan doc.

## 1. Mission (in priority order)
**A — v2 grading quality overhaul** (the headline). v1 looks "overwashed/overblown — a tone change, not a real grade."
Fix it, grounded in the v2 spec + Elijah's tutorial diagnosis (wrong order + exposure over-lift + contrast stacking +
no highlight protection). Concretely, in `auto-clip/colorkit/`:
   1. **I-Log input transform** — for Log footage, apply `colorkit/input_luts/Luna_I-Log_to_Rec709_BT1886_s65_v2.cube`
      FIRST (add `--input-lut` / auto-detect). This is the camera-correct develop.
   2. **Filmic tone-curve** in `correct.py` — replace linear contrast with a toe/shoulder curve (e.g. ACES/Hable/AgX-
      style) that protects highlights; use the exact formula/params from the v2 spec.
   3. **Exposure** — anchor to **middle-grey**, not the mean; set a true black point; stop over-brightening.
   4. **No contrast-stacking** — looks apply on a balanced base; don't re-add correction's contrast.
   5. **Color theory** — enforce skin-tone line, complementary harmony, saturation discipline, grade to the spec's
      scope targets.
   6. **Rebuild the 5 looks** in `luts.py` so they feel designed (toe/shoulder + subtle per-region hue shifts), then
      regenerate the `.cube`s.
**B — Extract to its own repository.** Once v2 looks good: copy the engine into a new standalone repo (e.g.
`C:\Users\elija\OneDrive\Desktop\<name>-color` — propose a clean name in a NOTE for Elijah; don't agonize) with a proper
package layout, `pyproject.toml`, `README.md`, `LICENSE` (MIT), `.gitignore`, and `git init` + an initial **local**
commit. **COPY** (leave the hub copy intact). **Do NOT push** anywhere.
**C — Stretch (if A+B done):** HLG/HDR tonemap stage; `-hwaccel` GPU decode for 8K; a small pytest suite; more looks;
sketch the optional AI "decision layer" (Gemini/Pegasus picks the look).

## 2. The loop (repeat until mission done or blocked)
1. **Pick** the highest-value next step from the mission.
2. **Build** it (edit `correct.py`/`stylize.py`/`luts.py`/`color.py`). For research-shaped sub-questions, spin a
   Workflow; adversarially verify findings before acting.
3. **TEST by actually running it** — this is non-negotiable. Use `auto-clip\.venv\Scripts\python.exe` and the real
   footage in `auto-clip/out/ftest/` + `C:\Users\elija\OneDrive\A footage` (the talking-head `a test.mov`, the I-Log
   8K `i log vid.mp4`, a photo, the HLG clip). Make **before/after AND v1-vs-v2** comparison montages (ffmpeg hstack)
   and **look at them** (read the PNG). Judge honestly: is it less washed? highlights intact? skin natural? Does it
   look *graded*, not filtered?
4. **Fix** what the eye/scopes show. Re-test. Loop the fix until it's actually good.
5. **Log** progress to `auto-clip/COLOR-BUILD-STATUS.md` (status log) every meaningful step; append dated learnings to
   `team/memory.md`; keep `obsidian/.../LarpSlop/Working on.md` current.
6. **Self-checkpoint context**: at ~40% usage, write/update the handoff and note where you are, then continue (or, if
   near a limit, tell Elijah to `/clear` and reseed from the docs). Don't lose state.

## 3. Hard rules (do not break)
- **Never publish / post / DM / commit-push to any remote.** Local-only. Outputs stop at `out/`. Drafts are fine.
- **Don't touch Elijah-gated items** (Gemini key, ad writes, IG publish, the separate-repo final name/push).
- Run Python/ffmpeg via **PowerShell + the `.venv`** (not Bash — it lacks them; heavy cv2 is fine in the venv).
- Keep deps **permissive** (no GPL like `color-matcher` in shipped code).
- Vault edits: the `LarpSlop` notes are freeform (no frontmatter) — match that; never invent property names elsewhere.
- ffmpeg `lut3d` on Windows needs the cube referenced by **bare filename** with ffmpeg `cwd` = the cube dir (already
  handled in `color.py`; preserve it).

## 4. When blocked
If a step needs Elijah (a decision, a key, a publish), **write the question into `COLOR-BUILD-STATUS.md` under "Pending
Elijah", then move on** to the next buildable thing. Never idle waiting — there is always more to build, test, research,
or polish. Only truly stop when A + B + the reasonable stretch goals are done and verified.

## 5. First action
Start the loop now: get the v2 spec (§0.4), then implement Mission A step 1 (the I-Log input transform), test it on
`i log vid.mp4`, and keep looping. Leave a crisp progress summary at the top of `COLOR-BUILD-STATUS.md` for Elijah to
read when he wakes up.
