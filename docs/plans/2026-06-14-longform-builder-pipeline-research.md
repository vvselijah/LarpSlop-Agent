# Longform Builder Pipeline — Build/Feasibility Research

- **id:** `longform-builder-pipeline`
- **Date:** 2026-06-14
- **Source of request:** `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md`, line 6 — *"I need to get it to essentially build me out full structure for longform videos and be able to edit them and publish them in a fully finalized and polished manner."*
- **Verdict:** **ADD-LATER** (build the *structure/assembly brain* as a thin local skill; do NOT adopt a new heavyweight OSS tool). Rough effort: **multi-day** (1 strong day for a v0 storyboard-only skill; 2–4 days for assembled rough-cut).
- **Confidence:** medium-high on the design (it cleanly inverts the proven auto-clip pattern); medium on payoff (depends on whether Elijah actually produces long-form, which his account today does not lean on).

---

## Headline verdict

This is the **inverse of `auto-clip`**: auto-clip takes ONE long video and *subtracts* (cuts the best self-contained 9:16 moments out). The longform-builder *assembles* — it builds a full narrative **structure** (hook → sections → payoff → CTA), then edits raw footage/assets into a finished long-form (16:9 or 9:16 multi-minute) master.

The honest finding: **the hub already owns ~80% of the machinery, and there is no OSS tool worth importing for the missing 20%.** The right move is the SAME move that made auto-clip cheap and good — **Claude IS the brain**, a tiny Python harness keeps the timing deterministic, and the render goes through Remotion (already wired in `..\abc wrap\`). The missing piece is a single "structure planner + assembler" skill, not a new dependency.

What does NOT change the verdict:
- **StoryToolkitAI** (the closest direct OSS match) is real and capable but a **wrong-shape** dependency for this hub (GUI desktop app, GPL-3.0, tied to DaVinci Resolve, heavy ML stack). Details below.
- **GetHookd.ai** (referenced in the source note) is a **paid SaaS for short-form *ad* generation** (competitor-ad scraping → hooks/angles), not a long-form structure/edit tool. It belongs to the *viral-scraper / ad-creative* idea on that same note, not this one.

I'd rate this candidate **medium value, not high**: the building blocks are done, the inversion is straightforward, but Elijah's account (@elijahaifl, ~100k, vertical Reels-first) does not currently live on long-form. Build it when there's a concrete long-form deliverable to make, not speculatively.

---

## What it actually is / does

A 4-stage pipeline, mirroring auto-clip's stage shape:

1. **STRUCTURE (the new brain).** Input = a topic/brief, OR a script, OR a pile of raw clips + their transcripts. Claude produces a **structured outline**: title, target length, an ordered list of *sections* each with a purpose (hook / context / point / proof / CTA), the spoken/script line(s) for that section, and a b-roll/visual intent per section. This is a storyboard, not a render.
2. **SOURCE.** Resolve each section to real media: existing footage spans (via transcript word-timestamps, exactly like auto-clip), TTS voiceover (ElevenLabs MCP / hyperframes-media Kokoro), b-roll (Pexels via `broll-inserter`, or Higgsfield-generated), title cards/graphics (Remotion).
3. **ASSEMBLE.** Turn the storyboard into a deterministic **edit timeline** — an ordered cut-list of `(source, in, out, layer, transition)` rows. Two render targets: (a) **Remotion composition** (the polished house style — captions, b-roll layering, grade — already built in `abc wrap`), or (b) a fast **FFmpeg concat** rough-cut for a same-day preview.
4. **POLISH + DELIVER.** Captions (`caption-engine` / auto-clip `caption.py`), color grade (`color-grade-system`), platform export (`platform-exporter`). **Stops at a file in `out/` — never publishes** (CLAUDE.md rule 1). Publish stays Elijah's per-action click.

The defining new artifact is the **storyboard JSON** between stage 1 and stage 3 — that's the "full structure" Elijah is asking for, and it's the only genuinely new code.

---

## OSS landscape (real research)

| Tool | What it is | License | Fit for this hub |
|---|---|---|---|
| **StoryToolkitAI** ([repo](https://github.com/octimot/StoryToolkitAI)) | Transcribe footage → searchable index → **Story Editor** that composes a screenplay from transcript lines → export **EDL / FCPXML / Fountain**; deep DaVinci Resolve 18+ integration; chat-with-content via GPT-4 / ollama / LM Studio. | **GPL-3.0** | **Closest match, but wrong shape.** It's a CustomTkinter **GUI desktop app** built for a human editor + DaVinci, not a headless skill. Heavy ML deps (Whisper, **Sentence-Transformers**, **pyannote.audio**, **spaCy**) = exactly the torch-class weight that hangs on the OneDrive disk. GPL-3.0 is copyleft. **Mine it for IDEAS** (its "screenplay from transcript → EDL" flow validates the design) but **do not import it.** |
| **OpenTimelineIO (OTIO)** ([PyPI](https://pypi.org/project/OpenTimelineIO/), [docs](https://opentimelineio.readthedocs.io/en/stable/)) | ASF-backed Python API + interchange format for editorial timelines; adapters to **FCPXML, CMX3600 EDL, AAF**. Build a timeline from scratch in Python and export to any NLE. | Apache-2.0 (permissive) | **The one OSS piece actually worth considering**, and it's a *library*, not an app. **Pure-Python, no torch/cv2.** IF Elijah ever wants the agent's storyboard to open in DaVinci/Premiere for human finishing, OTIO is the clean export bridge. **Optional/Phase-3**, not core — for an all-in-agent render, Remotion + FFmpeg already cover it without adding OTIO. |
| **OpenCut-AI / OpenReelio / openshorts** | Prompt/text-driven editors (edit-by-deleting-text, NL edit commands). | mixed | Either web/desktop apps or short-form-focused; overlap with existing `auto-editor`/`edit-video`. No reason to import. |
| **GetHookd.ai** ([site](https://www.gethookd.ai/), [G2](https://www.g2.com/products/gethookd-ai/reviews)) | **Paid SaaS.** Scrapes 65M+ Meta ads, extracts winning hooks/angles/CTAs, generates short-form **ad** creative. Launched Mar 2026. | Commercial | **Not this candidate.** It's a short-form *ad* tool — maps to the note's "viral scraper / ad-creative" idea, not long-form structure. Conflicts with hub principle (prefer local + official MCPs over paid scrapers). |

**Net:** no OSS tool to adopt for the core. One permissive library (OTIO) is a nice-to-have export bridge for a later phase. The brain is Claude; the renderer is Remotion (already present).

---

## How it composes with the hub (concrete integration sketch)

Build it as a new local engine `longform/` + skill `longform-builder`, **structurally cloning `auto-clip/`** (same agent-provider, same deterministic-Python-around-an-LLM-pick pattern from `auto-clip/highlight.py`).

**Reuse (already in the tree — do NOT rebuild):**
- **Transcription:** `auto-clip/transcribe.py` (faster-whisper, word-level JSON) — verbatim.
- **Editing primitives:** `abc wrap/.claude/skills/auto-editor` (cut-list: silence/filler removal, segment grouping, transition placement) and `edit-video` (full Remotion pipeline). The longform-builder *calls* these rather than reimplementing.
- **Render:** Remotion comps in `abc wrap/src/` + `remotion-longform` skill (proxies for smooth multi-minute preview/fast render) + `podcast-interview-editor` (already does multicam long-form 16:9 masters).
- **Assets:** ElevenLabs MCP (TTS), `broll-inserter` (Pexels), Higgsfield MCP (generated b-roll/title visuals).
- **Finish:** `caption-engine` / `auto-clip/caption.py`, `color-grade-system`, `platform-exporter`.

**New code (the only genuinely new ~20%):** the **storyboard brain** — invert `highlight.py`.

Data shapes (mirroring auto-clip's two-step agent provider so seg→time mapping stays in Python):
```
# 1) plan.py emits a brief and stops (like highlight.py --provider agent)
data/<stem>.structure-prompt.json   # brief + (optional) numbered transcript segments

# 2) Claude (the agent) writes the storyboard — the "full structure":
data/<stem>.storyboard.json
[
  { "section": 1, "role": "hook",   "script": "...", "visual": "talking-head",
    "source": {"type":"footage","start_seg":12,"end_seg":15} | {"type":"tts"} | {"type":"broll","query":"..."},
    "duration_hint_s": 8 },
  ...
]

# 3) assemble.py validates + snaps footage spans to segment boundaries (reusing highlight.py's
#    snap logic), resolves TTS/b-roll, and emits a deterministic timeline:
data/<stem>.timeline.json
[ { "src": "...", "in": 0.0, "out": 8.3, "layer": "A|broll|caption", "transition": "cut|crossfade" } ]

# 4) render: either -> Remotion props (render-props.json shape abc wrap already uses)
#    or -> FFmpeg concat for a fast rough-cut. Output to out/, NEVER published.
```
`team/stats.md` + `team/profile.md` feed the brain (lean structure toward Money/Finance + AI/Tech, his proven niches), exactly as the auto-clip skill already instructs for ranking.

**Niches/format note:** his account is vertical-Reels-first. The most *useful* first target is probably a **long vertical talking-head (2–5 min, 9:16)** assembled from a brief + TTS + b-roll, not a 16:9 YouTube cut — that's closer to what actually performs for him. `podcast-interview-editor` already covers the 16:9 multicam case if/when needed.

---

## Phased build sketch

- **Phase 0 — storyboard-only (≈ half-day to 1 day). HIGHEST leverage, lowest risk.**
  Just the brain: `plan.py` (emits brief) + the agent writing `storyboard.json` + a validator. Output = a structured outline (hook/sections/payoff/CTA with script + visual intent) saved as a vault `idea`/`script` note (respect the property contract). **This alone delivers "build me out full structure for longform" with ZERO new heavy deps** and is independently useful even if no render ever follows.
- **Phase 1 — FFmpeg rough-cut assembler (≈ 1 day).** `assemble.py` resolves footage spans (reuse `highlight.py` snapping) + TTS, emits `timeline.json`, FFmpeg-concats a watchable rough draft to `out/`. No Remotion yet — fast feedback loop.
- **Phase 2 — Remotion polished render (≈ 1–2 days).** Map `timeline.json` → the `render-props.json` shape `abc wrap` already consumes; route through `edit-video` / `podcast-interview-editor` for captions, b-roll layering, grade. This is where it becomes "finalized and polished."
- **Phase 3 (optional) — OTIO/EDL export + Higgsfield b-roll.** Add OpenTimelineIO export so the storyboard can open in DaVinci/Premiere for human finishing; wire Higgsfield for generated visuals where Pexels has no match.

Ship Phase 0 first and stop there until Elijah confirms he wants assembled output — don't gold-plate a render path for content he may not make.

---

## Windows + OneDrive feasibility / dependency weight

- **Phase 0:** **zero new deps** — Claude + a few lines of Python. Trivially safe.
- **Phase 1:** FFmpeg (already used everywhere) + faster-whisper (already installed). Safe.
- **Phase 2:** Remotion/Node (already installed in `abc wrap`). Heavy renders run as Node subprocesses, off the synced hot path. Use `remotion-longform` proxies to keep multi-minute preview smooth.
- **OneDrive landmines (known):** keep big models / scratch renders OFF the synced disk; run heavy steps as subprocesses (don't `import torch/cv2` inline — it hangs on the synced volume, per hub env notes). The design needs **no torch/cv2 of its own** — face-tracking etc. is only relevant to the short-form reframe path, not long-form assembly.
- **StoryToolkitAI's stack (pyannote/sentence-transformers/spaCy)** is exactly the weight to AVOID — another reason not to import it.
- **Secrets:** only ElevenLabs/Higgsfield/Pexels keys touch this, all already env-var-managed (CLAUDE.md rule 3). The agent brain itself needs none.

---

## Risks / honest caveats

- **Demand risk (biggest).** Elijah's growth engine is short-form. This is speculative until there's a real long-form piece to make. Phase 0 is cheap enough to justify regardless; Phases 2–3 should be demand-gated.
- **Overlap risk.** `auto-editor` + `edit-video` + `podcast-interview-editor` already cover a lot of "assemble/edit." The ONLY non-redundant new thing is the **structure/storyboard brain**. If that's all that ships, scope is honest; if it balloons into re-doing the editors, it's wasted effort. Build the brain; call the existing editors.
- **Quality ceiling.** Agent-assembled long-form from a brief (TTS + stock b-roll) reads as "AI content" unless there's real footage/voice. For *talking-head* long-form (his own footage + voice) the result can be genuinely good; for fully-synthetic it's mediocre. Set expectations accordingly.
- **Determinism.** Long-form has many more cuts than a 30s short — keep ALL timing in Python (the agent only emits semantic structure + segment indices, never raw timestamps), exactly as `highlight.py` does, or drift compounds.
- **GPL contamination.** Do not vendor StoryToolkitAI code (GPL-3.0). OTIO (Apache-2.0) is safe if/when used.

---

## Sources

- Request origin: `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md` (line 6)
- StoryToolkitAI — https://github.com/octimot/StoryToolkitAI (GPL-3.0; transcript→screenplay→EDL/FCPXML/Fountain, DaVinci integration)
- OpenTimelineIO — https://pypi.org/project/OpenTimelineIO/ · docs https://opentimelineio.readthedocs.io/en/stable/ (Apache-2.0 timeline API + EDL/FCPXML adapters)
- OTIO YouTube example (URL+description → OTIO timeline w/ markers) — https://github.com/OpenTimelineIO/otio-youtube-example
- ai-video-editor topic survey (OpenCut-AI, OpenReelio, openshorts, StoryToolkitAI) — https://github.com/topics/ai-video-editor
- GetHookd.ai — https://www.gethookd.ai/ · reviews https://www.g2.com/products/gethookd-ai/reviews (paid short-form *ad* SaaS; not long-form)
- Existing hub assets cross-referenced: `auto-clip/highlight.py`, `auto-clip/transcribe.py`, `.claude/skills/auto-clip/SKILL.md`, `..\abc wrap\.claude\skills\{auto-editor,edit-video,podcast-interview-editor,remotion-longform}`, `..\abc wrap\package.json` (Remotion 4.0.475).
