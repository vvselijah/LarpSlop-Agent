# Meet Your Cofounder — Game-Show Franchise Production/Asset Pipeline — Research & Build Plan

**Candidate id:** `meet-your-cofounder-event-series`
**Date:** 2026-06-14
**Source:** vault `me and tanner cooking/Meet your cofounder.md` (roadmap: STILL-TO-RESEARCH → Content-ops, `docs/plans/2026-06-14-overnight-roadmap.md` line 143)
**Sibling already-researched:** `live-software-review-format` (ADD-NOW skill, `docs/plans/2026-06-14-live-software-review-format-research.md`) — the same "Tanner + Elijah on camera, agent-as-brain prep skill, draft-to-vault" shape. This candidate is its event/series cousin and should reuse that pattern, not invent a new one.

---

## Headline verdict: ADD-LATER (Phase 0 doc now is OK) — build effort: SMALL (~1–2 hrs if/when built)

Scope it down hard, exactly as the Wave-5 lesson predicted. The right hub artifact is a **format-bible series note + a thin `cofounder-show-prep` skill** — NOT a new engine, NOT a "production/asset pipeline." Every media need this idea has (announce reel, contestant intros, lower-thirds, title cards, confessional captions, clip repurposing) is **already 100% covered** by the existing generation + edit suite. There is nothing left to build on the asset side; the only missing piece is a planning document and a prep checklist, both of which are pure Markdown.

It's **ADD-LATER rather than ADD-NOW** for one honest reason: unlike `live-software-review` (a low-friction recurring reel format that can start this week), this is an **in-person, multi-person event** that hasn't been scheduled, cast, or even fully outlined (the vault note's "episode 2" is blank). Building the prep kit before the event has a date is building scaffolding for a show that may not happen on any near horizon. The format bible has real value as a *thinking tool* for Elijah + Tanner to actually design the thing — so writing the **bible note now is fine and cheap** — but the prep *skill* should wait until there's a real shoot date. Do not stand up any pipeline.

**One-line call:** Write the format-bible vault note now if Elijah wants a planning doc; defer the prep-skill until the event is real; build ZERO new engine/dependency. The "asset pipeline" framing is the trap — reject it.

---

## What it actually is

From the vault note (`Meet your cofounder.md`, captured 2026-06-11) + its parent (`Hosting In person events.md`, 2026-06-10):

A recurring **in-person event** where people come to find their **technical cofounder** or **creative cofounder** — advertising and reproducing the exact Elijah (creative) + Tanner (technical) dynamic for the attendees — captured and cut into an **"early 2000s game-show-style 3-episode trilogy."** Concrete mechanics already sketched:

- **Episode 1** — speed cofounder-matching: 60-second self-intros; Tanner grills the techs on stack/workflow, Elijah grills the creatives; **Big-Brother-style confessional-room** cutaways of the hosts; 2–3 min speed-dating swaps over hard business problems; a **"time-capsule pitch"** where the room *attacks* (not praises) each idea and the sharpest critic earns a stake; everyone ranks 3 picks; pairs formed by end; **homework** assigned (cofounders pick an idea, creatives ship 7 posts, techs ship an MVP/repo).
- **Episodes 2–3** — not yet written (the note's episode-2 body is empty). The trilogy arc presumably follows the formed teams through building and a finale.

So the deliverable Elijah is reaching for is **a repeatable production format + the media to promote/document it.** Decomposed, that is exactly two things, and only one is missing:

1. **Format mechanics / "show bible"** (MISSING as an artifact) — the run-of-show, the segment list, the confessional prompts, the casting brief, the scoring/matching rules, the homework spec, the episode-to-episode arc. This is a standard, well-documented document type (a "show bible" / "format bible"): typically 10–50 pages, sections for premise/tone, format mechanics, contestant/cast types, episode breakdown, and forward planning ([No Film School](https://nofilmschool.com/show-bible-template), [AIScriptReader](https://aiscriptreader.com/blog/screenwriting/tv-show-bible-format-template-and-examples)). For an unscripted/competition format you swap "character arcs" for **format mechanics + contestant types + competitive structure**. Markdown is the ideal medium; a vault note IS a show bible.
2. **The media** (ALREADY FULLY COVERED — see integration sketch) — announce reel, contestant lower-thirds, confessional captions, title cards, episode cut, and clip/carousel repurposing. Nothing new is needed here.

### Reality check on the "asset pipeline" framing
"Production/asset pipeline" implies a new engine that ingests event footage and emits show assets. **That engine already exists in pieces and the pieces are better than anything bespoke would be:** HyperFrames' registry (lower-thirds, title cards, caption styles), Higgsfield (contestant-intro stylization, game-show-graphic generation), `auto-clip` + `caption-engine` (announce + clip pass), `carousel-builder` (recap swipe post). Web research on 2026 game-show graphics tooling (ChatCut, Vegas Pro Continuum, brand-kit generators — [OpusClip](https://www.opus.pro/blog/best-lower-thirds-generators-template-packs), [ChatCut](https://chatcut.io/blog/how-to-add-motion-graphics-templates-no-after-effects)) confirms the category is commoditized motion-graphics templating — which the hub already owns via HyperFrames/Remotion. There is **no OSS tool worth adding**; building one would duplicate the suite.

---

## Integration sketch (how it composes with the hub)

The whole point of the scope-down: this is a **connective document + a thin orchestration skill over the existing suite**, with near-zero new surface area.

- **New artifact 1 — the format-bible vault note** (`type: idea` per contract, in `obsidian/Elijah's vault/me and tanner cooking/` alongside the source, or `20-Content/Ideas/`). Body = the run-of-show, segment list, confessional prompts, casting brief, matching/scoring rules, homework spec, episode arc. `[[Tanner]]` wikilink. This is the single highest-value deliverable and it's just Markdown.
- **New artifact 2 (DEFER) — `.claude/skills/cofounder-show-prep/SKILL.md`**, modeled on `carousel-builder/SKILL.md` and the planned `live-software-review` skill (agent-as-brain, draft-to-vault, gated-publish). Given an episode + a cast list, it drafts: the announce reel script, the per-contestant lower-third copy, the confessional question bank, the run sheet, and the post-event recap. No Python, no deps. Only build once a shoot date exists.
- **Media composition (all existing, no new build):**
  - **Announce reel** ("come find your cofounder") → script in the skill → `auto-clip` (if cut from B-roll) + **`caption-engine`** / `viral-shortform-2026` for the hook + captions. Elijah approves before posting (Rule 1).
  - **Contestant intros / game-show stylization** → **Higgsfield** (`higgsfield-generate`, Marketing Studio) for stylized intro cards; **HyperFrames `hyperframes-registry`** for lower-thirds + title cards + "early-2000s game-show" motion graphics.
  - **Confessional-room captions + episode cut** → **`edit-video`** / `robthebank-style` / `podcast-interview-editor` (multicam confessional) + `caption-engine`.
  - **Announce/clip path is ALREADY covered** (the task's open question, answered): the announce video and per-episode highlights ride **`auto-clip` + `caption-engine`**, and a recap rides **`carousel-builder`** — no gap to fill.
- **Data shapes (if/when the skill is built):**
  - Episode object: `{episode:int, title:str, segments:[{name,duration,host,mechanic}], cast:[contestant], confessional_prompts:[str], homework:str}`
  - Contestant object: `{name, role:"technical"|"creative", one_liner, stack_or_portfolio, lower_third_copy}`
  - Output: a vault `idea` note (exact property block) + draft scripts; **stops at the note — never publishes.**
- **Niche fit:** lands in Elijah's #2 niche (AI/Tech) and the founder/build-in-public lane; pulls double duty as a top-of-funnel for his ventures (`team/profile.md`). Reasonable content fit; the bottleneck is logistics (a real event), not media.

---

## Phased build sketch

- **Phase 0 (optional, ~1 hr) — write the format-bible note.** A vault `idea` note that turns the raw `Meet your cofounder.md` into a structured show bible: premise/tone, the Episode-1 run-of-show (already ~80% specified in the raw note), confessional prompts, casting brief, matching + "time-capsule attack" scoring rules, homework spec, and a stubbed Episode 2–3 arc to force the blank to get filled. **This is the only piece worth doing on a near horizon** — it's the thinking tool that makes the event designable. Pure Markdown, contract-compliant, zero risk.
- **Phase 1 (DEFER until a shoot date exists) — the `cofounder-show-prep` skill.** Clone `carousel-builder` structure; wire the announce-script + lower-third + confessional-bank + run-sheet drafting; output to the vault note. ~1–2 hrs. Acceptance test: feed it a mock 6-person cast, confirm it emits a sane run sheet + per-contestant lower-thirds + a valid `idea` note. Nothing posts.
- **Phase 2 (only if the series actually recurs) — a reusable HyperFrames "game-show pack."** A registry block set (early-2000s lower-third, contestant scorecard, confessional name-plate, episode title card) so each episode looks consistent. Pure templating on the existing engine; no new deps. Do NOT build until ≥1 episode has shot and the format has proven it recurs.

**Stop rule:** if the event never gets a date, this stays at the Phase-0 bible note (a planning doc) and costs nothing further. No engine, ever, unless the suite genuinely can't produce a needed asset (it can).

---

## Windows + OneDrive feasibility / dependency weight

**Cleanest possible profile — no flags.**
- **Dependencies:** ZERO new ones. Phase 0 is a Markdown note; the deferred skill is a Markdown file; all media rides existing skills/MCPs (HyperFrames, Higgsfield MCP, `auto-clip`, `caption-engine`, `carousel-builder`).
- **No torch / cv2 / heavy / cloud / paid** introduced by this candidate. (Higgsfield is a hosted MCP already wired and credit-funded; `auto-clip` runs locally as today.) None of the OneDrive heavy-import hang risks apply.
- **Windows/PowerShell:** nothing new to run; existing engines already handle the platform gotchas.
- **Cost:** $0 beyond normal Claude/Higgsfield-credit usage that the suite already incurs.

---

## Risks & compliance

- **Standing Rule 1 — draft-only, never auto-publish/post/DM.** The bible note and any drafted scripts stop in the vault; the "post the announce reel" click and any DM to a contestant are Elijah's, per-action. Same gate as `carousel-builder`. ✅
- **Vault property contract is law.** The bible note must copy the `idea` template's property block exactly (`type: idea`, `domain:`, `stage: raw`, `status: open`, `date_captured:`, `tags:`); never invent a property. Place under `me and tanner cooking/` or `20-Content/Ideas/` per the layout.
- **Real-people / event risk (the actual risk surface — not a software one):** filming attendees requires **on-camera consent / release forms**; the "time-capsule pitch" segment exposes attendees' startup ideas publicly (IP/embarrassment) — disclose the format and get explicit opt-in before rolling. Confessional "we grill them" content must stay critique-of-work, not personal mockery (same honesty/anti-bullying gate as the `live-software-review` plan: lead with a strength, critique the work not the person, opinion-frame subjective takes). These are event-production responsibilities, flagged here but outside what any hub artifact controls.
- **No platform ToS/ban risk** from the format itself — documenting an in-person event and posting clips is ordinary creator activity. The only adjacent line is harassment in the "grilling" footage, mitigated above.
- **Honest low-value note / why ADD-LATER not ADD-NOW:** the media side has **nothing to build** (already covered), and the planning side is **one Markdown note**. The bottleneck is entirely logistical — venue, date, casting an influencer + ~20 cofounders, release forms — none of which a hub skill solves. Building a "pipeline" now would be solving a problem the suite already solved, for an event with no date. The bible note is a genuinely useful thinking tool; the skill is premature. That's the whole verdict.

---

## Sources

- [No Film School — Learn to Write a TV Show Bible (template)](https://nofilmschool.com/show-bible-template)
- [AIScriptReader — TV Show Bible Format: Template + 7 Examples (2026)](https://aiscriptreader.com/blog/screenwriting/tv-show-bible-format-template-and-examples)
- [ScriptReaderPro — TV Show Bible Examples](https://www.scriptreaderpro.com/tv-show-bible-examples/)
- [Wikipedia — Bible (screenwriting)](https://en.wikipedia.org/wiki/Bible_(screenwriting))
- [OpusClip — 10 Best Lower-Thirds Generators & Template Packs (2026)](https://www.opus.pro/blog/best-lower-thirds-generators-template-packs)
- [ChatCut — How to Make Animated Lower Thirds Without After Effects](https://chatcut.io/blog/how-to-add-motion-graphics-templates-no-after-effects)
- [Hashmeta — Generative AI Gaming: 2026 Guide](https://www.hashmeta.ai/en/generative-ai/generative-ai-gaming)
- Internal: `docs/plans/2026-06-14-live-software-review-format-research.md` (the sibling ADD-NOW prep-skill pattern this reuses)
