# SESSION-COMPACT — 2026-06-24 (color engine: built → footage-tested → v2 quality pivot)

**READ THIS FIRST on resume.** Then `docs/plans/2026-06-23-agentic-color-pipeline.md`,
`auto-clip/COLOR-BUILD-STATUS.md`, and (when present) `docs/plans/2026-06-24-color-v2-grading-spec.md`.
Autonomous overnight driver: **`NEXT-SESSION-AUTONOMOUS-PROMPT.md`** (paste it into the fresh session).

## 1. HEADLINE / STATE
Built our **own headless agentic color-grading engine** (`auto-clip/color.py` + `auto-clip/colorkit/`) — the exact
"headless + single-file shot-segmentation + per-shot anti-flicker correction + shot-match + creative grade" combo that
prior-art research found **nobody ships**. It is **BUILT + VERIFIED** on real footage (stills, single-clip, multi-scene
video, 8K, I-Log, HLG). **BUT** Elijah judged v1's *look* "overwashed/overblown — a tone change like IG's Edits app, not
a real grade." So the work pivoted to a **v2 quality overhaul** grounded in real grading craft, and the engine will be
**extracted into its own separate repository**. DRAFT-only throughout — nothing published, nothing committed.

## 2. WHAT THIS SESSION DID
1. **Research** (4 workflows): agentic-DaVinci verdict (Studio-only, skip) → build our own; the full pixel-math vs
   semantic-AI architecture; prior-art ("nobody ships this exact combo"; closest = MIT `perbhat/agentic-color-grader`);
   and the **grade-craft v2 spec** research (`pro-grade-craft-research`, run `wf_7107b183-886`).
2. **Built the engine** via parallel author → adversarial review → fix workflows + live testing. Bugs caught/fixed:
   critical R/B LUT-write-order, gamma-sign, WB still/video parity, and an ffmpeg-Windows lut3d path bug (drive
   colon/spaces → fixed via cwd + bare-filename staging). Re-verified after each fix.
3. **Footage-tested** on `OneDrive\A footage` (Luna Ultra): added the **`--height`** delivery-downscale flag (8K →
   1080×1920 IG-ready, rotation-aware). Proofs in `auto-clip/out/ftest/`.
4. **v2 diagnosis** (from Elijah's own color tutorial + research): washed look = wrong **order of operations** +
   exposure **over-lift** + **contrast stacking** + **no highlight protection** → clipped dynamic range.
5. **Official Insta360 I-Log LUTs** copied to `auto-clip/colorkit/input_luts/` (Rec709 BT1886 = SDR input transform).
6. **Wired Obsidian as durable project memory**: `40-Projects/LarpSlop/Completed/` + `Working on.md`.

## 3. THE ENGINE (verified v1)
- Run: `auto-clip\.venv\Scripts\python.exe auto-clip\color.py <file> --look teal_orange --match --height 1920`
- Modules: `colorkit/{io_utils,measure,correct,stylize,segment,match,luts}.py`; looks in `colorkit/luts/*.cube`
  (neutral_correct, warm_interview, teal_orange, kodak_2383_style, fuji_style); deps in `auto-clip/.venv`.
- Pipeline: router → PySceneDetect shots → ONE constant correction per shot (anti-flicker) → shot-match → uniform look
  → concat → `out/`. NEVER publishes. Docs: `colorkit/README.md`, `colorkit/INTEGRATION.md`.

## 4. v2 BUILD PLAN (the overnight target)
Make the *look* genuinely pro, not a filter. In priority order:
1. **I-Log input transform**: for Log footage apply `colorkit/input_luts/Luna_I-Log_to_Rec709_BT1886_s65_v2.cube` FIRST.
2. **Filmic tone-curve** replacing naive linear contrast in `correct.py` (toe/shoulder, protect highlights, no clip).
3. **Middle-grey exposure anchor** (stop pushing the mean to 0.46 → over-bright); set a real black point.
4. **Stop contrast-stacking**: looks sit on a balanced base; don't re-add the contrast correction already did.
5. **Color-theory looks + scope targets** (skin-tone line, complementary harmony, saturation discipline).
6. **Rebuild the 5 `.cube` looks** so they feel designed (toe/shoulder + subtle per-region hue shifts).
7. **Extract to its own repo** (proper package/pyproject/README/LICENSE/git init; COPY first; NO push).
→ The exact filmic formulas / params / scope numbers come from the v2 research → write them to
   `docs/plans/2026-06-24-color-v2-grading-spec.md`. If that file is absent, read the research output (run id
   `wf_7107b183-886`) or re-run the `pro-grade-craft-research` workflow.

## 5. PENDING ELIJAH (gates — don't proceed without him)
- Revoke OLD Gemini API key (new one set + validated). · Telegram bridge blocked on Anthropic API credit.
- Commit/push the engine? · Finalize the separate-repo NAME.

## 6. GIT
Hub repo `vvselijah/LarpSlop-Agent`. The color engine + this session's work are **uncommitted** in the working tree
(Elijah's call to commit). The color engine will move to its OWN repo after v2.

## 7. STANDING RULES (unchanged)
Never publish/post without per-action OK. DRAFT/propose only. Stops at `out/`. Run Python/ffmpeg via PowerShell (not
Bash). Vault: follow the property contract (but the LarpSlop folder notes are freeform — match that). 40% context rule.
