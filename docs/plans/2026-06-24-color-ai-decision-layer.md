# SPEC / SKETCH — Color Engine: the AI "pick-the-look" decision layer

**Date:** 2026-06-24 · **Status:** SKETCH (design + a working deterministic fallback already shipped).
**Scope:** the optional layer that chooses *which creative look* to apply automatically, so a clip can be
graded with no human look-choice. Companion to `2026-06-24-color-v2-grading-spec.md` (the develop) and
`2026-06-23-agentic-color-pipeline.md` (the v1 architecture). Tracker: `auto-clip/COLOR-BUILD-STATUS.md`.

> **DRAFT / PROPOSE-only.** A wired AI provider makes an external model call (cost / network), which is
> Elijah-gated per the hub's golden rule. What ships *now* is the deterministic brain + the interface;
> the AI brain is a documented stub that falls back to deterministic.

---

## 1. Why a decision layer

The engine deliberately splits **measurement** (deterministic pixel-math: white-balance, exposure,
black point, tone — always safe to apply) from **decision** (which *creative look* — `warm_interview`,
`teal_orange`, `kodak_2383_style`, `fuji_style`, `neutral_correct`). Correction is mechanical; the look
is editorial. Until now the look has been the operator's call (`--look NAME`).

The build-status backlog flagged the gap: *"non-portrait clips shouldn't get a skin look by default."*
A decision layer closes it — pick the look from what's actually in the frame, the way a colorist first
reads a shot before reaching for a look.

This is the same "Claude IS the brain" pattern `auto-clip` already uses for highlight selection
(`--provider agent`): cheap deterministic signal first, optional model intelligence on top.

---

## 2. What shipped now — the deterministic brain (`colorkit/decide.py`)

`measure.scene_stats(bgr)` extracts six cheap signals from a representative frame (pure cv2/numpy):

| signal | meaning | how |
|--------|---------|-----|
| `skin_frac` | fraction of skin-tone pixels (portrait/talking-head) | YCrCb rule: Cr∈[133,173], Cb∈[77,127], luma-gated |
| `green_frac` | fraction of foliage-green (nature/outdoor) | HSV hue 35–85, S≥60, V≥40 |
| `warmth` | warm vs cool cast, −1..1 | mean (R−B)/255 |
| `saturation` | mean HSV S, 0..1 | |
| `brightness` | mean luma (BT.601), 0..1 | |
| `contrast` | luma std-dev, 0..1 | |

`decide.suggest_look(stats)` maps them onto a look with ordered, first-match rules (grounded in the
masterclass color-theory: skin is decided by skin, not background):

1. `skin_frac ≥ 0.08` → **warm_interview** (flattering talking-head; opacity eased to 0.6 on tight
   close-ups so skin stays natural — never key skin hard).
2. `green_frac ≥ 0.18` (low skin) → **fuji_style** (Fuji greens).
3. `warmth ≥ 0.06` (low skin) → **kodak_2383_style** (warm print density; golden-hour/interior).
4. `warmth ≤ −0.02` or (high contrast + saturation) → **teal_orange** (cinematic complementary).
5. else → **neutral_correct** (let the develop speak).

Returns a `LookChoice` = `{look, opacity, reason, confidence, stats}`. Wired into the CLI as
**`--look auto`** (`color.py` grabs a representative frame — tonemapped if HDR, de-logged if I-Log —
measures it, logs the pick + the human-readable reason, then grades with it).

**Verified (2026-06-24):** real talking-head (`a test.mov`, skin 0.14) → `warm_interview`; a cool still
(`warmth −0.13`) → `teal_orange`; `--look auto` runs end-to-end through `color.py`.

### Known limitation (the reason the AI brain exists)
YCrCb skin detection fires on warm non-skin surfaces (tan asphalt, beige car interiors read as "skin").
The deterministic brain is *conservative* — that false-positive still yields `warm_interview`, a safe,
flattering, low-risk look — but it is not *understanding the scene*. That is exactly what the model layer
upgrades.

---

## 3. The AI brain (the sketch) — `decide.suggest_look_ai(...)`

Same interface, same `LookChoice` return shape; swaps the heuristic for a vision model that classifies
**content + mood + genre** and picks a look with a written rationale. The stub ships now and falls back
to `suggest_look`; wiring a provider is the Elijah-gated step.

### 3.1 Providers (in hub-preference order)
1. **`agent` — a Claude vision sub-agent (RECOMMENDED, no API key, "Claude IS the brain").**
   Mirrors `auto-clip --provider agent`. Pass 3–5 representative frames (one per shot, or a contact
   sheet) + the `scene_stats` + the look catalog (name → one-line character) to a sub-agent; it returns
   `{look, opacity, reason}` as structured output. Cheap, no external paid call, already the hub pattern.
2. **`pegasus` — TwelveLabs Pegasus via the `video-analyzer` MCP.** It already analyzes whole clips for
   `auto-clip`; ask it to classify scene/mood/setting/lighting, then map its taxonomy → look. Best when
   the *temporal* read (not just a frame) matters (e.g. "moody night drive" vs "bright vlog").
3. **`gemini` — Gemini video.** Currently quota-blocked in this hub (`limit:0`); slot in when a working
   key exists.

### 3.2 Contract the provider must honor
- Input: `video_path` and/or representative frames + `scene_stats` + the look catalog.
- Output: a `LookChoice` — `look ∈ VALID_LOOKS`, `opacity ∈ [0,1]`, a model-written `reason`,
  `confidence ∈ [0,1]`, `ai: true`.
- **Must fall back to `suggest_look` on any model error / low confidence / invalid look** (robustness-first;
  the grade must never fail because a model call did).
- **Never** lets the model invent a look outside the catalog or push opacity to a filter-y 1.0
  (cap at ~0.85; the masterclass "tasteful, not a filter" rule still governs).
- Side-effect-free + DRAFT-only: it returns a recommendation; `color.py` decides to apply it; nothing is
  published.

### 3.3 Future: model-*authored* looks (beyond picking)
The current looks are a fixed catalog of 5. A later layer could have the model emit look *parameters*
(per-region hue offsets, density curve, vibrance) that `luts.py` bakes into a fresh `.cube` — moving from
"pick one of five" to "design a look for this clip." Out of scope here; flagged as the natural extension.

---

## 4. Implementation status & follow-ups

- [x] `measure.scene_stats` — six signals (shipped, verified).
- [x] `decide.suggest_look` — deterministic brain (shipped, verified).
- [x] `decide.suggest_look_ai` — stub + fallback (shipped).
- [x] `color.py --look auto` — wired, HDR/Log-aware rep frame (shipped, verified).
- [ ] Wire a real provider (`agent` first) — **Elijah-gated** (external call / cost).
- [ ] Multi-frame / per-shot decisioning (currently one rep frame ~40% into the clip).
- [ ] Improve skin detection (LAB + face-presence) to cut warm-surface false positives — or let the
      `agent` provider supersede it.
- [ ] Model-authored looks (`luts.py` bake from model params).

**Golden-rule note:** picking a look is an editorial choice. `--look auto` makes a *defensible default*
the operator can always override (`--look NAME`); it never publishes, and the AI path stays gated.
