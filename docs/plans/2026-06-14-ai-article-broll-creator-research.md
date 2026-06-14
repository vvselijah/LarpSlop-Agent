# AI Article B-Roll Creator — Build / Feasibility Research

**Candidate id:** `ai-article-broll-creator`
**Date:** 2026-06-14
**Source of request:** `docs/plans/2026-06-14-overnight-roadmap.md` (STILL-TO-RESEARCH → Video) · vault `40-Projects/LarpSlop/What I have so far.md` ("viral help creation pipeline")
**Roadmap status:** STILL-TO-RESEARCH (Video)

---

## Headline verdict: ADD-LATER (Phase 0 buildable now), confidence MEDIUM-HIGH

Build the **Phase-0 brain** (a `broll-plan.json` planner) now — it's cheap, OneDrive-safe, and a near-clone
of the `auto-clip/highlight.py` agent pattern this hub already runs. **Defer the full automated
fetch+assemble engine to ADD-LATER**, because (a) it's only worth wiring once `news-update-system`
is producing the article/idea-notes that feed it (that's the upstream half of the "story→reel" chain,
and it's still itself a Phase-0 plan, not built), and (b) the genuinely *hard* part isn't code — it's
that auto-fetched generic stock b-roll is the lowest-leverage visual on the 2026 algorithm. Elijah's
winners are face-to-camera + custom motion graphics (the `carson-raps-style` / `robthebank-style`
lane), not stock-clip slideshows. A text→stock-slideshow tool risks *manufacturing* the exact
low-retention, high-skip-rate format the rest of the hub is built to avoid.

So: the **planner** (article → ranked list of scene beats + per-beat search queries / generation
prompts) is high-leverage and reusable. The **auto-assembled stock slideshow** is low-leverage and
should stay an optional, clearly-labeled output, never the default. Build the brain; gate the body.

**Rough effort:** Phase 0 (the planner, agent-as-brain, ~150 lines stdlib) ~half a day. Phase 1
(Pexels/Pixabay fetch into a footage folder for `broll-inserter`) ~half a day. Phase 2 (FFmpeg
auto-assemble slideshow) ~1 day — optional, demand-gated.

**The one honest caveat:** this only "completes the story→reel chain" if the chain is one Elijah
actually wants. He has no text→reel product live today; the gap is real but unproven as a *need*.
Ship the planner (independently useful, feeds the editing skills he already uses) and let real usage
decide whether the auto-assembler is ever worth building.

---

## What it is / what it actually does

The ask: **turn an article (or an idea/story note) into matching b-roll automatically** — close the
gap that `broll-inserter` (the Remotion skill) leaves open, because that skill *places* b-roll but
needs the footage to already exist in a folder. There is currently **no path from text → visuals** in
the hub.

Decomposed, the candidate is three separable stages:

1. **Plan (the brain).** Read article/script text → segment it into visual "beats" (one idea per beat)
   → for each beat emit: a short on-screen concept, a *stock-search query*, an *AI-generation prompt*,
   and a rough duration. This is pure language work — exactly the `highlight.py` "agent picks → JSON"
   move, no media touched.
2. **Source (the body).** For each beat, either (a) **fetch** a matching stock clip from a free video
   API, or (b) **generate** one via the installed Higgsfield MCP (Seedance / Soul). Output = a folder
   of clips + a manifest mapping beat→file.
3. **Assemble (optional).** Concatenate the clips (+ optional Ken-Burns on stills, captions, VO) into a
   rough 9:16 cut with FFmpeg. This is where it overlaps most with the existing editing skills and is
   the lowest-value, highest-taste-risk stage.

**Critical framing:** stages 1–2 produce *inputs to the editing skills Elijah already has*
(`broll-inserter`, `edit-video`, `caption-engine`). Stage 3 tries to *replace* them with an automated
slideshow. The valuable product is "fill the footage folder + hand `broll-inserter` a plan," **not**
"render the whole reel."

---

## Prior art (what's out there, 2026) + license

| Tool | What it does | Approach | Deps / cost | License | Fit |
|---|---|---|---|---|---|
| **[Anil-matcha/AI-B-roll](https://github.com/Anil-matcha/AI-B-roll)** | Adds AI b-roll to a video | Jupyter notebook; transcript → b-roll; ties to a paid SaaS (vadoo.tv) for the polished path | Python notebook; specifics undocumented; SaaS upsell | MIT | Reference only — pattern, not a dependency |
| **[sasoder/stockpile](https://github.com/sasoder/stockpile)** | "Drop a clip, get b-roll" | Transcribe → topics → **search YouTube** → Gemini scores relevance → categorized folders | Python, FFmpeg, **Gemini API key**; optional GDrive/Gmail | unspecified | Good *architecture* match; **YouTube-sourcing = ToS/copyright risk (reject)**; Gemini replaceable by our agent |
| **[eshaan-mehta/B-Roller](https://github.com/eshaan-mehta/B-Roller)** | Auto-places b-roll on a timeline | DaVinci Resolve scripting; varies clip duration | Requires **DaVinci Resolve 16+** | n/a | Wrong host app (we're FFmpeg/Remotion) |
| **OpenShorts / Open-Sora / invideo / OpusClip / Fliki / VideoGen** | Full text→video platforms | Script → scene split → stock/AI per scene → VO + captions | Heavy (Open-Sora = torch/diffusion); or paid SaaS | mixed | **Confirms the pattern is mainstream**; none is OneDrive-safe or free to self-host cheaply |

**Takeaway:** the pattern (text → beats → per-beat stock/AI → assemble) is completely standard in 2026
and commoditized. **There is no must-clone repo** — every OSS one either needs a cloud LLM key (replace
with our agent), sources from YouTube (copyright risk — reject), or hosts in the wrong app. The hub
should **build a thin native version** that reuses what's already installed, exactly as it did for
`auto-clip`. The real IP is the *prompt/curation*, not the plumbing.

---

## Footage sourcing: the decisive sub-decision

The whole feasibility hinges on **where the visuals come from**. Three paths, ranked:

1. **Free stock video API — RECOMMENDED for Phase 1.**
   - **[Pixabay API](https://pixabay.com/api/docs/)** — **best first choice.** Content License (CC0-style):
     **no attribution required**, commercial use OK, modify/redistribute OK. Video search endpoint,
     ~100 req/60s. One free API key (a secret → Windows env var, per Rule 3). Light HTTP/JSON via
     `curl.exe` — zero heavy deps, OneDrive-safe.
   - **[Pexels API](https://www.pexels.com/api/documentation/)** — strong fallback / supplement.
     `GET https://api.pexels.com/v1/videos/search?query=…&orientation=portrait&size=medium&per_page=…`
     returns `video_files` with direct download links per resolution. Free, 200 req/hr & 20k/mo (free
     unlimited tier on request). **Attribution requested** ("prominent link to Pexels," credit the
     videographer) and it **does not explicitly bless heavy re-editing** in the API docs — so for a
     no-friction, attribution-free, modify-freely pipeline, **prefer Pixabay; use Pexels to widen
     coverage** and keep a credits line in the manifest.
   - Both are `orientation=portrait` capable → native 9:16, no reframe needed.

2. **AI generation via the installed Higgsfield MCP — RECOMMENDED for "no stock match" beats.**
   Seedance 2.0 (video), Soul/Nano-Banana (image), Marketing Studio. **Already installed, ~1.9k credits,
   zero new deps.** Per-beat generation prompt from stage 1 → `mcp__…__generate_video` /
   `generate_image`. This is the on-brand path (custom visuals beat generic stock on retention) but
   costs credits → keep it agent-selected per beat, not blanket.

3. **YouTube scraping (stockpile's path) — REJECT.** Copyright/ToS risk, exactly the kind of paid-scraper
   /grey-area sourcing the hub avoids. Do not build.

**Net:** Pixabay (free, CC0, light) for the bulk + Higgsfield (installed) for the hero/custom beats.
No torch, no cv2, no cloud LLM key, no paid scraper. Fully OneDrive-safe.

---

## How it composes with the hub (integration sketch)

This is a **sibling engine to `auto-clip`**, the mirror image: `auto-clip` goes *video → text-ranked
clips*; this goes *text → visual beats → clips*. It reuses the same two proven patterns.

**Proposed location:** new `broll-creator/` engine dir (parallel to `auto-clip/`), + a `broll-creator`
skill that drives the agent loop. New secret: `PIXABAY_API_KEY` (and optionally `PEXELS_API_KEY`) via
`setx`, never in files.

**Data flow + shapes:**

```
article.md / vault idea-note (from news-update-system)
        │
        ▼  [Stage 1: plan.py  — clone of highlight.py's agent two-step]
broll-plan.json
  [{ beat, text, concept, duration_s,
     stock_query: "<2-4 words>", gen_prompt: "<image/video prompt>",
     source: "stock"|"generate" }]          ← Claude (the agent) IS the planner; no API key
        │
        ├─► [Stage 2a: fetch.py] Pixabay/Pexels portrait search per stock_query
        │       → footage/<slug>/beatNN.mp4   + footage/<slug>/manifest.json (incl. Pexels credits)
        │
        └─► [Stage 2b] Higgsfield MCP generate_video/image per gen_prompt
                → footage/<slug>/beatNN.mp4
        │
        ▼
footage/<slug>/   ◄── EXACTLY the "pre-existing footage folder" broll-inserter needs
        │
        ├─► broll-inserter / edit-video (Remotion) — the GOOD path: human-curated, on-brand
        └─► [Stage 3 OPTIONAL: assemble.py] FFmpeg concat + Ken-Burns + caption-engine
                → out/<slug>_rough.mp4   ← clearly labeled ROUGH; engine STOPS here, never publishes
```

**Pattern reuse (verified against the real code):**
- **Agent-as-brain:** `auto-clip/highlight.py` already implements the exact `--provider agent`
  two-step (emit `*.agent-prompt.json` → agent writes `*.picks.json` → re-run `--from-picks`). Stage 1
  is a structural copy with a different SYSTEM prompt and pick schema. **No ANTHROPIC_API_KEY, no
  Ollama** — Claude Code is the planner.
- **FFmpeg subprocess:** `auto-clip/reframe.py` already shells `ffprobe`/`ffmpeg` (the hub's FFmpeg 8.1
  build) with the Windows-cp1252-safe `log()` and the **"stop at `out/`, never publish" exit rule**
  (CLAUDE.md Rule 1). Stage 3 reuses both verbatim.
- **Engine+skill split:** mirrors `auto-clip` (engine in a dir, `auto-clip` skill orchestrates).
- **Upstream feeder:** `news-update-system` (the just-researched ADD-NOW) writes article/idea-notes to
  `20-Content/Ideas/` → those are the *input* to Stage 1. This candidate is the **production half** of
  that loop; `news-update-system` is the **intake half**. Neither is fully built yet, so this stays
  ADD-LATER until the intake half ships.

---

## Phased build sketch

**Phase 0 — the planner (smallest safe thing; build now). ~half day, GREEN deps.**
`broll-creator/plan.py`: read a `.md`/`.txt` article → segment into beats → agent two-step → write
`broll-plan.json` (beats + stock queries + gen prompts + source hint). Pure stdlib, no media touched,
no new secret, no network. **Independently useful immediately:** hand the plan to `edit-video` /
`broll-inserter` / `higgsfield-generate` by hand. This alone delivers the literal "turn an article into
matching b-roll [plan]" ask with zero risk.

**Phase 1 — stock fetch into a footage folder. ~half day, GREEN deps.**
`broll-creator/fetch.py`: for each `source:"stock"` beat, Pixabay (then Pexels) portrait search via
`curl.exe`, download top match → `footage/<slug>/beatNN.mp4` + manifest (with Pexels credit line).
Needs `PIXABAY_API_KEY` env var. Output is exactly what `broll-inserter` consumes — **this is the
candidate's true unlock.** Add a `--generate` flag that routes `source:"generate"` beats to a printed
Higgsfield MCP call list for the agent to execute (credits-gated).

**Phase 2 — optional rough auto-assemble. ~1 day, demand-gated, low value.**
`broll-creator/assemble.py`: FFmpeg concat beats → 9:16 rough cut, optional Ken-Burns on stills, hand
off to `caption-engine`/ElevenLabs VO. Clearly labeled `_rough.mp4`. **Only build if Phase-1 footage
folders prove genuinely useful** — otherwise the editing skills already do this better with taste.

**Phase 3 — scheduled "story→reel draft" chain. Gated on news-update-system shipping.**
`news-update-system` writes idea-note → `plan.py` → `fetch.py` fills a footage folder → vault note links
it for Elijah to open in `edit-video`. Unattended drafting, **stops at a footage folder + plan**, never
renders-and-publishes. Same gate as `always-on-content-research-agent`: prove he acts on the drafts first.

---

## Risks / honesty

- **Taste/retention risk (the real one).** Auto-assembled generic stock slideshows are the *opposite*
  of what wins for @elijahaifl in 2026 (skip-rate is the #1 negative signal; face-cam + custom motion
  graphics retain, stock montages don't). The candidate is valuable as a **footage-folder filler for the
  human-in-the-loop editing skills**, not as an autopilot reel maker. Keep Stage 3 (auto-assemble) off
  by default and labeled ROUGH.
- **Generic-visual sameness.** Free stock pulls look like every other AI slideshow → erodes the
  original-content edge IG's Apr-2026 originality policy rewards. Mitigate by **biasing toward
  Higgsfield-generated** (on-brand, original) over stock for hero beats, stock only for filler.
- **Pexels attribution + re-edit ambiguity.** Pexels asks for credit and its API docs don't explicitly
  bless heavy re-editing. **Mitigation: default to Pixabay (CC0, no attribution, modify-freely);** use
  Pexels only to widen coverage and always write a credits block into the manifest.
- **Unproven need.** No text→reel product is live; the "completes the chain" rationale assumes a chain
  he wants. Phase 0 (the planner) is independently useful regardless, which is why it's safe to build now
  while the rest waits on demand.
- **Secrets.** One/two new API keys → Windows env vars via `setx` only (Rule 3); never in files (tree
  syncs to OneDrive).
- **Publishing.** Engine stops at a footage folder / `out/` rough cut. Never posts (Rule 1). No new
  surface area here.
- **Ban/ToS:** Pixabay & Pexels APIs are sanctioned for exactly this use (download + modify). The only
  ToS-risky path is YouTube scraping (stockpile's approach) — **explicitly rejected.**

---

## Recommendation

**Build Phase 0 (the planner) as part of the next video-tooling pass — it's a cheap, OneDrive-safe clone
of `highlight.py` and is useful on its own.** Tier the whole candidate **ADD-LATER**: Phase 1 (stock
fetch → footage folder for `broll-inserter`) is the real unlock and should follow once
`news-update-system` is actually producing idea-notes to feed it. Keep the auto-assembler (Phase 2)
optional and demand-gated — it's the lowest-value, highest-taste-risk stage and the existing editing
skills already do it with judgment. Sourcing: **Pixabay (CC0) for bulk + Higgsfield MCP (installed) for
hero/custom beats; never YouTube.** No new heavy deps, no torch/cv2/cloud-LLM/paid-scraper.

---

## Sources

- Anil-matcha/AI-B-roll (MIT) — https://github.com/Anil-matcha/AI-B-roll
- sasoder/stockpile (YouTube-sourced b-roll finder, Gemini) — https://github.com/sasoder/stockpile
- eshaan-mehta/B-Roller (DaVinci Resolve b-roll script) — https://github.com/eshaan-mehta/B-Roller
- Pixabay API docs (CC0 content license, video search, no attribution) — https://pixabay.com/api/docs/
- Pixabay Content License summary — https://pixabay.com/service/license-summary/
- Pexels API video search docs (params, video_files, attribution, rate limits) — https://www.pexels.com/api/documentation/
- OpusClip — Best AI B-Roll Generators for Short-Form Video 2026 (market context) — https://www.opus.pro/blog/best-ai-b-roll-generators-short-form-video
- Digen — Best Open Source AI Video Generators 2026 (Open-Sora context) — https://resource.digen.ai/best-open-source-ai-video-generators/
- Hub code verified: `auto-clip/highlight.py` (agent-as-brain two-step), `auto-clip/reframe.py` (FFmpeg subprocess + stop-at-out/ rule)
