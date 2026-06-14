# addyosmani/agent-skills — Cherry-Pick Evaluation (Research & Recommendation)

**Date:** 2026-06-14
**Candidate id:** `addyosmani-agent-skills-eval`
**Source:** `obsidian/Elijah's vault/40-Projects/LarpSlop/Cool repos to checkout.md` ("agent skills repo → See if any benefit us")
**Type:** Pure decision-support research (the doc IS the deliverable — a vetted shortlist). No build required to act.

---

## Headline verdict: SKIP the plugin install / ADD-LATER for 2–3 cherry-picked *patterns*

**Do not install the marketplace plugin.** The vault note guessed this repo might be a content/IG/infra
force-multiplier. It is not. `addyosmani/agent-skills` is a **software-engineering workflow** skill pack —
24 skills covering spec-driven dev, TDD, code review, CI/CD, security hardening, observability, git
workflow, etc. It is built for product engineering teams shipping application code, not for a solo
Instagram creator running analytics/clip/vault automations.

The reason to skip is not quality — the repo is excellent (49.9k stars, MIT, no heavy deps, Claude Code
native). The reason is **near-total overlap with capabilities the hub already has and already validated**:

- The hub's **`dev-workflow`** skill (Tanner's tworkflow: Plan→Implement→Review→QA→Ship→Retro) already
  covers spec/plan/implement/review/QA/ship.
- **`agentic-build-loop`** covers decompose-fan-out-verify-loop.
- **`context-checkpoint`** covers the 40% context-hygiene rule.
- Built-in **`code-review`, `simplify`, `verify`, `security-review`** cover the review/cleanup/QA/security axes.
- The **`AGENT-TEAM-BLUEPRINT.md`** explicitly ruled against marketplace plugin packs (Tier C):
  *"too rigid, token burn, fighting the format… editable files + skills do the same job and stay
  correctable (3-0 verified)."* Installing a 24-skill plugin is exactly the pattern the blueprint warns off.

**What IS worth doing (add-later, low effort):** read 2–3 specific SKILL.md files and fold their best ideas
into the hub's *existing* skills as plain-markdown edits — not as an installed dependency. Top candidates:
`doubt-driven-development`, `source-driven-development`, and `interview-me`. See the integration sketch.

**Effort to act on the recommendation:** ~30 min (read 3 files, decide whether to graft any one paragraph
into `dev-workflow`/`research`). The decision itself — don't install — is free.

---

## What it actually is

**Repo:** https://github.com/addyosmani/agent-skills — "Production-grade engineering skills for AI coding
agents." MIT license, ~49.9k stars (Feb 2026 launch, fast-growing). Currently the most-installed skills
marketplace for Claude Code.

**Structure:** Each skill is a folder with a `SKILL.md` (YAML frontmatter + workflow steps + a
"rationalizations" table + red flags + verification requirements). Pure markdown — **zero runtime code,
zero Python, no torch/cv2, no API keys, no cloud calls.** Two skills reference an external MCP
(`browser-testing-with-devtools` → Chrome DevTools MCP; `observability-and-instrumentation` →
OpenTelemetry), but those are optional and only matter for app code.

**Targets:** Claude Code (plugin marketplace), plus Cursor / Gemini CLI / Windsurf / OpenCode / Copilot /
Kiro / Antigravity. Install path for Claude Code:
```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```
Ships 7 slash commands: `/spec /plan /build /test /review /code-simplify /ship` (plus `/build auto`).

**The 24 skills** (all dependency-free unless noted):

| Skill | What it does | Hub overlap |
|---|---|---|
| using-agent-skills | Meta-router: maps a task to the right skill | `agentic-build-loop` + CLAUDE.md routing |
| interview-me | Q&A loop to extract real requirements | **partial gap** — borrowable |
| idea-refine | Rough concept → concrete proposal | `dev-workflow` PLAN phase |
| spec-driven-development | Writes a PRD before coding | `dev-workflow` PLAN template |
| planning-and-task-breakdown | Spec → small verifiable tasks | `dev-workflow` + `agentic-build-loop` |
| incremental-implementation | Thin vertical slices, feature flags | `dev-workflow` Implement |
| test-driven-development | Red-Green-Refactor, test pyramid | partial — hub leans "evidence-before-done" not formal TDD |
| context-engineering | Rules files + MCP context feeding | CLAUDE.md system + `context-checkpoint` |
| source-driven-development | Ground decisions in official docs | **partial gap** — borrowable for `research` |
| doubt-driven-development | Fresh-context adversarial review | `code-review` + `research-lean` verify; **borrowable framing** |
| frontend-ui-engineering | Component arch, a11y (WCAG) | N/A (no app UI here) |
| api-and-interface-design | Contract-first API design | N/A |
| browser-testing-with-devtools | Chrome DevTools MCP runtime checks | overlaps Claude-in-Chrome (wired) |
| debugging-and-error-recovery | 5-step triage | generic; `dev-workflow` covers enough |
| code-review-and-quality | Five-axis review, ~100-line sizing | built-in `code-review` |
| code-simplification | Reduce complexity (Rule of 500) | built-in `simplify` |
| security-and-hardening | OWASP Top 10, secrets mgmt | built-in `security-review` |
| performance-optimization | Core Web Vitals, measure-first | N/A (no web app) |
| git-workflow-and-versioning | Trunk-based, atomic commits | hub git discipline already in CLAUDE.md |
| ci-cd-and-automation | Shift-left, quality-gate pipelines | N/A (no CI here) |
| deprecation-and-migration | Migration patterns | rarely relevant |
| documentation-and-adrs | ADRs, API docs | vault already does decision logs |
| observability-and-instrumentation | Structured logging, OpenTelemetry | N/A |
| shipping-and-launch | Pre-launch checklist, rollback | `dev-workflow` Ship |

**Honest read:** ~18 of 24 skills are about shipping production *application code* (frontend, API, CI/CD,
observability, performance, migration). Those are irrelevant to a hub whose "code" is a handful of local
Python engines (`refresh.py`, `intel/*.py`, `auto-clip/`) and markdown. The 6 that *are* relevant to the
hub's small-Python work are already covered by the hub's own `dev-workflow` + built-in code skills.

---

## How it composes with the hub (integration sketch)

There is **no MCP and no data shape** here — this is pure prompt/markdown context. "Integration" means:
do we graft any of its best paragraphs into the hub's *existing* skills? Three are worth a look, grafted as
plain-markdown edits (NOT as an installed plugin, to respect the blueprint's no-plugin-packs rule):

- **`doubt-driven-development` → `.claude/skills/dev-workflow/` review lens.** Its 5-step CLAIM → EXTRACT →
  DOUBT (fresh-context reviewer, gets *only* artifact + contract, never the reasoning) → RECONCILE → STOP
  is a crisp, bounded formalization of the hub's existing "three fresh-context review lenses." If
  `dev-workflow`'s review section feels loose, lift the "reviewer sees only the artifact, never your
  reasoning, to avoid bias" rule and the ≤3-cycle stop condition. **One paragraph, high signal.**
- **`source-driven-development` → `docs/RESEARCH-PROTOCOL.md` / `research` skill.** "Ground framework/API
  decisions in the official docs you actually fetched, and cite them" reinforces the hub's existing
  WebFetch-the-primary-source discipline. Mostly already practiced; worth a one-line reinforcement at most.
- **`interview-me` → planning skills.** A short requirements-interrogation loop before a build. The hub's
  `dev-workflow` already verifies premises against real code; `interview-me`'s "ask 2-3 clarifying questions
  when the request is ambiguous" is a useful habit but is also already baked into `deep-research`'s
  pre-flight. Lowest incremental value of the three.

Everything else (spec/plan/build/test/review/ship, code-review, simplify, security) **duplicates** existing
hub skills and would create two competing conventions — actively harmful. Do not graft those.

**What it does NOT touch:** none of the hub's actual force-multipliers — IG/Meta MCPs, `ig-dashboard`,
`intel/`, `auto-clip`, the vault, content skills. The vault note's hope ("infra force-multiplier across the
whole hub") does not materialize; this repo has no bearing on content, analytics, ads, or video.

---

## Phased build sketch

This is decision-support, so the "build" is just an optional 30-minute graft. No software.

- **Phase 0 (smallest safe thing — 0 min):** Decision is made above: **do not install the plugin.** Record
  the verdict; that alone closes the vault roadmap item.
- **Phase 1 (optional, ~30 min, no spend, no deps):** Read three SKILL.md files directly via raw GitHub
  (no install): `doubt-driven-development`, `source-driven-development`, `interview-me`. If any paragraph
  sharpens an existing hub skill, paste a 1–3 line adaptation into `.claude/skills/dev-workflow/SKILL.md`
  or `docs/RESEARCH-PROTOCOL.md`. Attribute the source inline. **No new skill files; edit existing ones.**
- **Phase 2 (only if a real product-code repo enters the hub):** If Elijah ever pulls a genuine application
  codebase into this environment (e.g. working on Cruncrr/ClipWith source here rather than in its own repo),
  re-evaluate installing the full plugin *into that repo's scope only* — it would earn its keep there. Not
  applicable to the content/analytics hub as it exists today.

There is no Phase 3 — the upside ceiling of this candidate for *this* hub is the Phase-1 graft.

---

## Risks / Windows + OneDrive feasibility / ToS

- **Dependency weight: none.** Pure markdown, no torch/cv2/cloud/paid. Trivially OneDrive-safe and
  Windows-safe — it is text. (The only flagged deps, Chrome DevTools MCP and OpenTelemetry, attach to
  skills the hub would never use.)
- **License: MIT** — fully permissive; grafting a paragraph with attribution is clean.
- **No ToS / ban / compliance risk.** No platform API, no scraping, no auto-publish — it never touches IG,
  Meta, or any account. Orthogonal to the standing publish-confirmation rules.
- **The real risk is convention collision + context bloat (this is why SKIP, not ADD).** Installing 24
  skills + 7 slash commands that overlap `dev-workflow`, `agentic-build-loop`, `code-review`, `simplify`,
  `security-review`, and `verify` would (a) burn context with always-loaded duplicate descriptions, (b)
  create two competing "how we ship" conventions in one workspace, and (c) violate the blueprint's
  3-0-verified Tier-C ruling against marketplace plugin packs. The hub's whole thesis is *editable
  markdown + a few first-party MCPs*, not plugin packs.
- **Honest low-value caveat:** even the 3 borrowable skills are *marginal* upgrades to things the hub
  already does well. This is a "read it once, maybe lift one paragraph" item, not a capability gap. If the
  30 minutes are better spent on a content or revenue task, skipping entirely is fully defensible.
- **Stale-guess caveat:** the vault note's premise was wrong about what this repo is. Worth correcting the
  note so it isn't re-researched as an "infra" lead later.

---

## Sources

- Repo (license, structure, 24 skills, install): https://github.com/addyosmani/agent-skills
- `doubt-driven-development` SKILL.md (workflow, fresh-context reviewer): https://github.com/addyosmani/agent-skills/blob/main/skills/doubt-driven-development/SKILL.md
- Plugin manifest: https://github.com/addyosmani/agent-skills/tree/main/.claude-plugin
- Addy Osmani's write-up (intent, philosophy): https://addyosmani.com/blog/agent-skills/
- 2026 review / "engineering process not prompt collection": https://knightli.com/en/2026/06/14/addyosmani-agent-skills-engineering-workflows/
- DEV community overview (49k stars, hidden uses): https://dev.to/_cbd692d476c5faf3b61bcf/addy-osmanis-agent-skills-5-hidden-uses-in-49k-stars-of-workflow-magic-37c8
- Claude Plugin Hub listing: https://www.claudepluginhub.com/plugins/addyosmani-agent-skills
- Hub blueprint (Tier-C: skip marketplace plugin packs): `AGENT-TEAM-BLUEPRINT.md`
- Hub existing equivalents: `.claude/skills/dev-workflow/SKILL.md`, `context-checkpoint`, built-in `code-review`/`simplify`/`verify`/`security-review`, `agentic-build-loop`
- Format precedent (decision-support doc): `docs/plans/2026-06-14-clipping-agency-research-research.md`
