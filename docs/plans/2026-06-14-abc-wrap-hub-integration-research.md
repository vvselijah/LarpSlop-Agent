---
title: "abc wrap (ClipWith) ↔ hub integration — feasibility research"
date: 2026-06-14
candidate_id: abc-wrap-hub-integration
type: research
verdict: add-later
confidence: high
build_effort: M (Phase 0 is S; full vision is L)
source: "vault 40-Projects/LarpSlop/What I need to do or start with the ai agent team.md (line 13: 'Integrate the ABC wrap repo into my ai agent team for specific use cases needed with it like ad and post creation')"
---

# abc wrap (ClipWith) ↔ hub integration — should we wire them together?

## Headline verdict: **ADD-LATER** (one small ADD-NOW slice). Confidence: HIGH.

**The premise is half-right in a way that changes the build.** The roadmap's framing — "engine
exists, packaging missing," same shape that made `clipping-campaign-folder` a strong ADD-NOW — is
true for the *render engine* but **the heaviest integration is already done and was never the gap.**

The two repos **already share their entire skill suite and MCP stack** — not by copying, but because
both resolve from the same user-level install:

- **41 skills live at `C:\Users\elija\.claude\skills\`** (user scope), including the whole video
  suite: `edit-video`, `caption-engine`, `broll-inserter`, `platform-exporter`, `robthebank-style`,
  `viral-shortform-2026`, the `higgsfield-*` set, `video-intake`, `template-creator`, etc. Both the
  hub and abc wrap see these identically. `comm -12` of the two repos' local `.claude/skills/`
  folders returns **zero** — they don't duplicate skills, they each just carry their own *native*
  ones (hub: auto-clip/carousel/comment-triage/etc.; abc: none local, all inherited from user scope).
- **MCPs are near-identical** in both `.mcp.json` files (meta-ads, instagram, figma, lottiefiles,
  gemini-video, video-analyzer, elevenlabs, fal, ffmpeg). The hub adds exa/tavily on top.

So "deeper wiring so both share skills/MCPs" is **already a solved problem.** What is *genuinely*
missing is a **clean data/asset handoff seam** so the hub's brain (analytics, ad insights, content
plans, picked moments) can *drive* abc wrap's Remotion render farm and get finished files back —
without a human manually carrying JSON and MP4s between two Desktop folders.

That seam is real, modest, and worth building **incrementally** — but it is **not** a strong
ADD-NOW the way clipping-campaign-folder was, because (a) the highest-value clip path (`auto-clip`,
pure Python/FFmpeg) already lives *in the hub* and needs none of abc wrap, and (b) the ad pipeline
it would unlock depends on assets that don't exist yet (no current ad client/brand in flight; the
ad `.tsx` comps are bespoke per-sponsor, not a reusable template).

---

## What each repo actually is (verified, not assumed)

| | **Hub** (`ai agent team`) | **abc wrap** (`ClipWith` R&D) |
|---|---|---|
| Nature | Python + docs + data hub | Remotion (React/TS/Node) render farm |
| Has `package.json` / `node_modules`? | **No** — no Node project at root | Yes — Remotion 4.0.475, full deps |
| Core engines | `ig-dashboard/` (analytics), `intel/` (competitor+trend radar), `auto-clip/` (long→9:16, pure FFmpeg/whisper) | `src/edits/*.tsx` (24 comps incl. 7 ad comps), `src/twelvelabs/` pipeline, `src/components/` style suites |
| Render path | FFmpeg subprocess only (no React) | `remotion render <Comp> --props=… --public-dir=…` |
| "Stops at" | `auto-clip/out/` | `out/<Comp>.mp4` → `clean-for-instagram.js` → `-ig.mp4` |
| Brain | Claude + IG/Meta data + vault context | Claude + TwelveLabs video understanding |

**abc wrap's ad assets that already exist** (`src/edits/`): `BioFlowAd.tsx` (41 KB),
`BioFlowBreathAd.tsx`, `FlowFuelAd.tsx` (40 KB), `FlowFuelDropsAd.tsx`, `FlowFuelSleepAd.tsx`,
`FlowFuelShashaEdit.tsx`, `JamieMentzerAd.tsx` (45 KB), `ClipWithPitch.tsx`. These are **hand-built,
per-sponsor compositions**, not a parameterized "ad template" — important for effort estimates below.

**The injection seam already exists.** `render:podcast` runs
`remotion render PodcastEdit … --props=render-props.json --public-dir=render-public`. Remotion's
`--props=<file.json>` is the standard, documented way to inject external data into a composition at
render time. **This is the entire technical basis for hub→abc wrap automation** — the hub writes a
props JSON + drops assets, abc wrap renders against them.

## Why he wants it (and the honest read)

Roadmap intent: "ad and post creation." Force-multiplier on shared assets. The honest read:

- **The clip half of the vision is already delivered** — by `auto-clip` *inside the hub*, which the
  SKILL.md notes reused ~70% from the hub + abc wrap but then went its own pure-Python way. It does
  **not** call into abc wrap at runtime. So "auto-clip already reuses the sibling repo" is true at
  *build* time (borrowed ideas/snippets) but **not** at *run* time (no live dependency). The premise
  slightly overstates the existing coupling.
- **The ad/post half is the actual unmet need** — and it's gated on inputs that don't exist:
  there's no live ad campaign, and the ad comps are bespoke. Wiring a pipeline now would be building
  a road to a destination not yet under construction.

## External landscape (for buy-vs-build sanity)

- **Remotion license**: free for individuals and orgs ≤3 employees, **commercial use allowed**,
  local + self-hosted Lambda rendering included. Elijah is a solo creator → **$0, no license
  concern.** Paid only kicks in at 4+ employees. ([license](https://www.remotion.dev/docs/license),
  [LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md))
- **gethookd.ai** (the tool he bookmarked in the same note): an **ad-research/intelligence SaaS**
  ($29–$129/mo) — 23M-ad library, competitor "Brand Spy," AI script gen from winning ads. It is a
  *research* product, **not** a render pipeline — orthogonal to this integration. The hub's `intel/`
  radars + `meta-ads ads_library_search` already cover the free-and-legal slice of that; gethookd is
  a separate buy-vs-build decision, not part of this seam. ([gethookd.ai](https://www.gethookd.ai/))
- **OSS alternatives** (Twick MIT, YumCut, Gemini+Remotion demos): all point back to the same stack
  Elijah already owns — Remotion + FFmpeg + an LLM. **No new tool beats "use the render farm you
  already built."** ([Remotion vs Twick vs CE.SDK](https://dev.to/neeru_jaroliya/remotion-vs-twick-vs-cesdk-best-react-sdks-for-ai-powered-video-editors-709))

**Net:** nothing to install, nothing to buy. The whole value is in a thin, reliable seam.

---

## Integration sketch — how it composes with the hub

**The seam is a shared "job folder" + a props-JSON contract.** No new dependency, no new MCP.

```
HUB (brain)                              SHARED SEAM                    ABC WRAP (render farm)
───────────                              ──────────                     ─────────────────────
weekly-content-plan / niche-intel ─┐
reel-analytics (what's working)    ├──► writes  jobs/<slug>/spec.json ──► Remotion comp reads it
auto-clip picks / carousel-builder │     (+ assets/ : voiceover, b-roll)   via --props=spec.json
meta-ads ad insights ──────────────┘                                       │
                                                                           ▼
                                          ◄── reads  jobs/<slug>/out/  ◄── render → clean-for-instagram
review (NEVER auto-publish) ◄──────────────────────────────────────────── *-ig.mp4 (1080x1920, voice-only)
```

- **Which engine/skill/MCP:**
  - Source of truth for *what to make*: hub's `reel-analytics` + `niche-intel` + vault `20-Content/`
    ideas (props say "render THIS hook/script in THIS style").
  - Render executor: abc wrap's existing `remotion render <Comp> --props=jobs/<slug>/spec.json`.
  - Voice/assets: `elevenlabs` MCP (TTS) or Higgsfield (b-roll) write into `jobs/<slug>/assets/`.
  - Finishing: abc wrap's `clean-for-instagram.js` (already enforces voice-only 1080×1920).
  - Distribution-readiness only: `instagram` MCP `get_content_publishing_limit` pre-flight; the
    publish click stays Elijah's (rule 1).
- **Data shapes (the contract):**
  ```jsonc
  // jobs/<slug>/spec.json  — hub writes, abc wrap's comp reads via --props
  {
    "kind": "post" | "ad",
    "comp": "RobTemplateEdit",          // a PARAMETERIZED comp (see Phase 1)
    "niche": "money" | "ai" | ...,       // drives caption color / pacing presets
    "hook": "Nobody tells you this about…",
    "script": [ { "t": 0.0, "text": "…" }, … ],   // word/line timing
    "assets": { "voiceover": "assets/vo.wav", "broll": ["assets/b1.mp4"] },
    "export": { "w": 1080, "h": 1920, "audio": "voice-only" }  // rule 4 baked in
  }
  ```
  ```jsonc
  // jobs/<slug>/out/manifest.json  — abc wrap writes back
  { "file": "out/<slug>-ig.mp4", "duration": 31.2, "rendered_at": "…", "approved": false }
  ```
- **Where the seam physically lives:** a `jobs/` folder. Cleanest is **inside abc wrap** (it has the
  renderer + `out/` convention already) with the hub writing to `..\abc wrap\jobs\`. Keep large
  media OFF git via the existing `.gitignore` patterns; the hub references abc wrap by relative path
  exactly as CLAUDE.md already documents the sibling.

---

## Phased build sketch

**Phase 0 — the smallest safe thing (ADD-NOW, ~1 focused session, S).**
Document the seam; don't automate anything yet. Deliver:
1. A one-page `docs/abc-wrap-bridge.md` in the hub: the `jobs/<slug>/spec.json` contract above, the
   exact `remotion render … --props=…` command, and the golden rules copied verbatim (no render
   until previewed+approved; voice-only 1080×1920; never auto-publish; confirm before any Higgsfield
   gen that costs credits).
2. One **manual** end-to-end dry run on an EXISTING comp (e.g. `MoneyTestEdit` or `PercentEdit`):
   hub picks a hook from `reel-analytics`, hand-writes a `spec.json`, a human runs the render in abc
   wrap, file lands in `out/`. Proves the contract with zero new code.
This de-risks everything and is genuinely useful even if Phases 1–3 never happen.

**Phase 1 — one parameterized "post" comp (S–M).**
Build ONE data-driven Remotion comp in abc wrap (`HubPostEdit.tsx`) that reads `spec.json` via
`getInputProps()` and renders Elijah's proven house style (lean on `robthebank-style` +
`viral-shortform-2026` + `caption-engine`). This is the missing reusable template the 7 bespoke ad
comps never were. Test: hub writes spec → render → preview → approve.

**Phase 2 — a hub `render-bridge` skill (M).**
A thin hub skill that: takes a vault idea or auto-clip pick → assembles `spec.json` (+ optional
ElevenLabs VO into `assets/`) → prints the exact render command for Elijah to run (does NOT auto-run
renders; render is credit/CPU-heavy and rule-gated). Closes the loop without crossing a golden rule.

**Phase 3 — ad path + Higgsfield (L, only when a real ad client exists).**
Generalize `HubPostEdit` into `HubAdEdit` (product shot slot, CTA, Marketing-Studio avatar via
Higgsfield). Pull winning-ad structure from `meta-ads ads_library_search`. Gate behind an actual
sponsor/campaign — do NOT speculative-build.

---

## Windows + OneDrive feasibility & dependency weight

- **Dependency weight: essentially zero NEW.** Both repos already have their toolchains installed.
  No torch/cv2/cloud/paid additions. Remotion + FFmpeg are already in abc wrap.
- **OneDrive / sync risk: LOW but real.** Renders write multi-hundred-MB MP4s; a `jobs/` folder of
  active renders inside the OneDrive tree will churn sync. **Mitigation:** keep `jobs/*/out/` and
  `assets/` gitignored AND consider a OneDrive "always keep on this device / exclude folder" for
  active render scratch, or stage renders to a non-synced scratch dir and copy only the final
  `-ig.mp4` back. Heavy Remotion renders already run as `node`/Chromium subprocesses (the known-good
  pattern), so the "heavy import hangs on the synced disk" gotcha (torch/cv2) does **not** apply here.
- **Two-repo path coupling.** The seam hardcodes a relative hop to `..\abc wrap\`. CLAUDE.md already
  documents the sibling at that path, so this is consistent — but it's a brittleness to note if
  either folder ever moves (the HANDOFF bring-up checklist already flags absolute-path fixups).

## Risks / compliance / ToS

- **Golden-rule collision (the #1 risk).** abc wrap's rules (never render until previewed+approved;
  Higgsfield costs credits) and the hub's rules (never publish without per-action confirmation;
  voice-only IG export) must BOTH hold across the seam. The contract bakes `"audio":"voice-only"`
  and the bridge **stops at a file + a render command** — it must never auto-render or auto-publish.
  This is a discipline risk, not a technical one; Phase 0's doc is what enforces it.
- **Remotion license: no risk** (solo creator, free, commercial OK).
- **FFmpeg/whisper licensing: no risk** (already in use across both repos).
- **Secrets / rule 3 — INCIDENTAL FINDING (flag, not part of this build):** abc wrap's
  `.mcp.json` contains a **hardcoded `GEMINI_API_KEY`** (`AIzaSy…d8e4`) in plaintext. It is
  **gitignored** (not committed — verified via `git check-ignore`), so it's not on GitHub, but it
  **is** sitting in cleartext inside the OneDrive-synced tree, which violates hub rule 3 ("secrets
  only in env vars, never in files"). Recommend rotating that Gemini key and switching the entry to
  `${GEMINI_API_KEY}` env-var interpolation like every other key. (Logged here for visibility; a
  separate spawned task will track the fix so it isn't lost.)
- **Platform ToS: none triggered.** Pipeline produces local files only; no scraping, no auto-posting.

## Bottom line

Build **Phase 0 now** (a documented seam + one manual dry-run on an existing comp — cheap, useful,
de-risking). Treat **Phases 1–2** as ADD-LATER, pulled forward the moment Elijah wants repeatable
"idea → finished reel in my house style" without leaving the hub. Hold **Phase 3 (ads)** until a
real sponsor exists. Do **not** re-build the clip path — `auto-clip` already owns it. The integration
is worth doing, but its value is packaging/discipline, not new capability, so it doesn't out-rank
work that unlocks capability the hub doesn't already have.

## Sources
- Remotion License & Pricing — https://www.remotion.dev/docs/license
- Remotion LICENSE.md (GitHub) — https://github.com/remotion-dev/remotion/blob/main/LICENSE.md
- Remotion company licensing — https://www.remotion.pro/license
- GetHookd (ad-research SaaS, the bookmarked tool) — https://www.gethookd.ai/
- Remotion vs Twick vs CE.SDK (React video SDK landscape, 2026) — https://dev.to/neeru_jaroliya/remotion-vs-twick-vs-cesdk-best-react-sdks-for-ai-powered-video-editors-709
- Repo evidence (local): `..\abc wrap\package.json` (render:podcast `--props` seam), `..\abc wrap\src\edits\*Ad.tsx`, `C:\Users\elija\.claude\skills\` (41 shared user-level skills), both `.mcp.json` files
