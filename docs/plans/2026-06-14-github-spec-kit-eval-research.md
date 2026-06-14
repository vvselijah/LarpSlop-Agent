# github/spec-kit eval — graft, don't install

- **Candidate id:** `github-spec-kit-eval`
- **Date:** 2026-06-14
- **Source:** vault `Cool repos to checkout.md` → roadmap STILL-TO-RESEARCH → Infra
- **Verdict:** **SKIP installing it; GRAFT 1-2 ideas into the existing dev-workflow.** (Same shape as the addyosmani verdict.)
- **Confidence:** High
- **Build effort:** ~30-60 min if Elijah wants the optional graft (one template tweak + one skill line). Zero if we just pin this decision.

---

## Headline verdict

spec-kit is a **real, serious, well-built tool** (GitHub-official, MIT, ~112k stars as of mid-2026) that does **almost exactly what this hub's `dev-workflow` + `docs/templates/` already do** — turn a vague request into spec → plan → tasks → implement, with a project "constitution" for standing rules. It is genuinely good. It is also **redundant here**, and installing it would *fragment* the hub's working method into two parallel systems (its `.specify/` tree + slash commands vs. our `docs/` + `.claude/skills/`). The hub already won this battle once: CLAUDE.md explicitly says "don't re-litigate" the working method.

**Do not install `specify` into this repo.** Instead, steal its two best ideas that we're genuinely missing:
1. **The "constitution" pattern** — a single standing-principles file the planner is forced to read every run. We have this *de facto* (CLAUDE.md "Standing rules", vault property contract) but it isn't wired into the PLAN template as a checked premise.
2. **An explicit `/clarify` step** — a structured "ask N questions before writing the spec" gate. Our skill has the adversarial questions but no hard clarify-before-plan checkpoint.

Both are decision-support grafts with near-zero build/runtime risk. Everything else spec-kit offers, we have.

---

## What it actually is

**Spec-Driven Development (SDD)** toolkit. You install a Python CLI (`specify`), run `specify init` in a repo, and it drops a workflow scaffold plus agent slash-commands. The loop:

| spec-kit command | Produces | Our equivalent |
|---|---|---|
| `/speckit.constitution` | `.specify/memory/constitution.md` (project governing principles) | CLAUDE.md "Standing rules" + vault CLAUDE.md property contract |
| `/speckit.specify` | `specs/<feat>/spec.md` (what/why, user stories) | PLAN.md §1 Problem + §2 Non-goals |
| `/speckit.clarify` *(optional)* | clarifying Q&A baked into the spec | **gap** — we do this ad-hoc, not as a gate |
| `/speckit.plan` | `specs/<feat>/plan.md` + `research.md`, `data-model.md`, `api-spec.json`, `quickstart.md` | PLAN.md §3-§8 (premises, approach, design, failure modes, test plan) |
| `/speckit.tasks` | `specs/<feat>/tasks.md` (ordered task list) | PLAN.md §9 Steps |
| `/speckit.analyze` *(optional)* | cross-artifact consistency check | our 3-lens REVIEW pass (broader than this) |
| `/speckit.implement` | executes the tasks | dev-workflow Phase 2 + commit discipline |

**Stack:** Python 3.11+, installed via `uv tool install` / `uvx` / `pipx`; needs Git; integrates with 30+ agents incl. Claude Code. Fully **local — no cloud, no API key** for the workflow itself (the agent you point it at does the LLM calls).

**Claude Code integration:** writes prompt files into `.claude/commands/` (slash-command mode) or a skills variant via `--integration-options="--skills"`. So it would literally add a `/speckit.*` command family alongside our existing skills.

Sources confirm it's the fastest-growing AI-coding methodology of 2026 and GitHub-official — this is not vaporware. The question is purely **redundancy**, not quality.

---

## How it compares to what we already have

Our `dev-workflow` skill + `docs/workflow/00-08` + `docs/templates/{PLAN,REVIEW-CHECKLIST,QA-REPORT,SESSION-HANDOFF}.md` is **a superset of spec-kit's core loop for this hub's needs**, and is *better adapted* in three ways spec-kit can't match:

- **It already encodes hub-specific law** — the 40% context-hygiene rule, OneDrive/torch hazards, "never publish without confirmation", the vault property contract, model routing. spec-kit's generic constitution would have to re-derive all of this.
- **It has a real QA phase with visual screenshots** (`scripts/qa-screenshots.js` at 375/768/1440px) and a 3-lens security/correctness/conformance review. spec-kit's `/analyze` is a lighter cross-doc consistency check, not a security pass.
- **It's prose-first and human-readable**, which fits a hub whose continuity *is* session handoffs. spec-kit fragments one plan into 5-6 files per feature (`spec.md`, `plan.md`, `tasks.md`, `research.md`, `data-model.md`, `api-spec.json`) — overkill for the small Python engines and skill edits this hub actually ships.

What spec-kit has that we genuinely lack (the only real findings):
- A **named, enforced constitution gate** the planner must consult every run.
- A **clarify-before-spec** checkpoint as an explicit phase, not just "ask good questions."

---

## Windows + OneDrive feasibility (if installed anyway)

- **Dependency weight: LIGHT.** Pure-Python CLI; no torch/cv2/cloud/paid. `uv`/`pipx` install. No heavy models. Would not hang the OneDrive disk on import.
- **PowerShell: SUPPORTED.** Every automation script ships both `.sh` and `.ps1` variants; select with `specify init --script ps`. So the hub's "run Python/ffmpeg via PowerShell" rule is satisfiable — no WSL/Git-Bash dependency.
- **Known Windows friction (flag this):** open bug [#2179](https://github.com/github/spec-kit/issues/2179) — `specify init --here` on Windows failing while hunting for a `spec-kit-template-claude-ps` release asset ("No matching release asset found for claude", also [#2185](https://github.com/github/spec-kit/issues/2185)). The CLI also churned its own flags recently (`--ai claude` deprecated → `--integration claude`), i.e. moving target.
- **OneDrive-sync hazard:** installing would scatter a `.specify/` tree + `specs/<feat>/` doc-explosion + `.claude/commands/` files **inside the synced tree**, plus a CLI whose templates update out-of-band. More surface area to sync and to drift against our existing `docs/` system. This is the real cost, and it's an argument *against* installing.

Net: technically installable on this box, but the payoff is negative — it duplicates our system and adds a second, churning source of truth inside OneDrive.

---

## Integration sketch (the graft we actually recommend)

No engine, MCP, or new dependency. Two surgical edits to the *existing* working method:

**Graft A — "Constitution check" premise in the PLAN template.**
Add one row to `docs/templates/PLAN.md` §3 Premises (and mirror in `.claude/skills/dev-workflow/templates/PLAN.md`): a fixed first premise the planner must verify every run —
> "This plan honors the standing law: CLAUDE.md Standing Rules + (if vault is touched) the vault property contract + (if it publishes) the no-publish-without-confirmation rule. ✅/❌"

This is spec-kit's constitution idea, expressed as a checked premise instead of a separate file — fits our prose-first system and costs one table row. Data shape: a markdown row; no code.

**Graft B — explicit Clarify gate in `dev-workflow` Phase 1.**
Add one line to `SKILL.md` Phase 1, step 0: *"If the request is underspecified, ask 2-3 clarifying questions and fold the answers into the plan before writing premises."* (This is exactly what the `deep-research`/`research-lean` skills already do for research — we'd be making the dev loop consistent with them.)

That's the whole integration. Both are reversible one-liners, both pinnable so this never gets re-litigated.

---

## Phased build sketch

- **Phase 0 (smallest safe thing — DONE by this doc):** Pin the decision. spec-kit = quality tool, redundant here, do-not-install. Cost: this file. No code, no install, no risk.
- **Phase 1 (optional, ~30-60 min, only if Elijah wants it):** Apply Graft A + Graft B above to the two PLAN templates and the dev-workflow SKILL.md. Run the existing dev-workflow's own lighter-touch path (docs edit = one-line plan inline). Append one dated learning to `team/memory.md`.
- **Phase 2 (not recommended):** *If* a future need ever arises to drive an external agent (Copilot/Gemini) on a non-hub repo with a heavy multi-file spec process, revisit `specify` then — install it in *that* repo, off the OneDrive tree, never here. No action now.

---

## Risks / compliance

- **ToS / ban risk: NONE.** Local dev tooling, MIT license, no platform automation, touches no IG/Meta surface. Irrelevant to the publish/ban rules.
- **Main risk is organizational, not technical:** installing it would create **two competing working-method systems** inside one OneDrive-synced hub — the exact fragmentation CLAUDE.md's "don't re-litigate the working method" rule exists to prevent. The graft avoids this; the install causes it.
- **Moving-target risk:** spec-kit's CLI flags and release-asset handling are still churning (deprecated `--ai`, Windows asset bug). Another reason to copy the *idea*, not bind to the *tool*.
- **Honest low-value note:** even the recommended graft is marginal. The hub's working method is already strong and battle-tested; A and B are polish, not a force-multiplier. If Elijah's attention is scarce, "pin the skip and move on" is a perfectly good final answer — the grafts are nice-to-have, not needed.

---

## Sources

- spec-kit repo: https://github.com/github/spec-kit
- spec-kit docs (home): https://github.github.com/spec-kit/
- spec-kit installation guide: https://github.github.com/spec-kit/installation.html
- Microsoft for Developers — diving into SDD with Spec Kit: https://developer.microsoft.com/blog/spec-driven-development-spec-kit
- MarkTechPost overview (2026-05): https://www.marktechpost.com/2026/05/08/meet-github-spec-kit-an-open-source-toolkit-for-spec-driven-development-with-ai-coding-agents/
- Windows `--here` init bug #2179: https://github.com/github/spec-kit/issues/2179
- Release-asset bug #2185: https://github.com/github/spec-kit/issues/2185
- Spec Kit + Claude Code walkthrough: https://rajeevpentyala.com/2026/02/22/github-spec-kit-with-claude-code-build-a-react-app-using-spec-driven-ai/

---

## Hub artifacts this was compared against

- `.claude/skills/dev-workflow/SKILL.md` (Plan→Implement→Review→QA→Ship→Retro)
- `docs/templates/PLAN.md`, `REVIEW-CHECKLIST.md`, `QA-REPORT.md`, `SESSION-HANDOFF.md`
- `docs/workflow/00-principles.md` … `08-failure-modes.md`
- CLAUDE.md "Standing rules" + "Working method" sections
