# Live "Drop Your Software, We Grade It" Format — Research & Build Plan

**Candidate id:** `live-software-review-format`
**Date:** 2026-06-14
**Source:** vault `me and tanner cooking/ideas for us going live.md` (roadmap: STILL-TO-RESEARCH → Content-ops, `docs/plans/2026-06-14-overnight-roadmap.md` line 125)

---

## Headline verdict: ADD-NOW (Phase 0 only) — build effort: SMALL (~1.5–2.5 hrs)

Build the **rubric + a `live-software-review` skill** now. It is the cleanest possible hub addition:
**agent-as-brain, zero new dependencies, zero cloud/paid, draft-only, stops at a vault note** — the exact
shape of the already-proven `carousel-builder` / `comment-triage` / `auto-clip --provider agent` skills. The
underlying content format ("roast my product / landing page") is a **validated, established genre**, not a bet.
This is one Markdown skill file + one vault rubric note; it touches no Python engine and carries no OneDrive
or dependency risk.

The honest caveat: this is **content scaffolding, not a moat**. The skill does NOT make the live show happen,
attract submissions, or guarantee views — those are Elijah + Tanner's job on camera. What it *does* remove is
the recurring friction of every episode: a consistent scorecard, a pre-filled prep checklist, an on-brand
scoring honesty gate, and a saved archive note per session. That friction-removal is real and it compounds
across a recurring series, which is why it clears the ADD-NOW bar. It would be wrong to oversell it as more.

---

## What it actually is

The vault idea (verbatim, 2026-06-09): *"make a video telling people to drop their software's in the comments
because tanner and i will be going live and reviewing peoples projects and grading them for overall quality,
performance, virality, looks, and our professional opinion on how to make it better."*

So the deliverable is **not a video tool** — it is a **scoring system + repeatable show-prep kit** for a
recurring live format in Elijah's AI/Tech niche, co-hosted with his named collaborator Tanner. Two artifacts:

1. **A scoring rubric** — fixed dimensions, a 1–10 scale, weights, and an honesty gate, so grades are
   consistent episode-to-episode and across two hosts (the classic two-judge consistency problem).
2. **A hub skill** (`live-software-review`) that, given one or more submitted projects (a URL, a repo, an app
   store link, or a description from the comments), produces a **draft scorecard + improvement notes + an
   episode prep checklist**, saved as a vault `idea` note for Elijah/Tanner to use live. Claude is the brain;
   it reads the submission (WebFetch on the URL/repo), applies the rubric, and writes the note. No model, no
   API key, no install.

### Format reality check (it's a proven genre, not a gamble)
"Roast my landing page / roast my product" is an established build-in-public content format with multiple
standing products and a documented track record (Roast My Landing Page, Roastd.io, the Indie Hackers/Twitter
roast culture). That de-risks the *format*; the rubric just makes Elijah + Tanner's version repeatable and
on-brand. Sources below.

### Rubric dimensions (pinned)
Elijah's five raw dimensions map cleanly onto the converged best-practice criteria, with one rename for
honesty. Research consensus across academic rubric design and startup/hackathon judging: **4–6 criteria max**
(past ~5–6, judges lose track), each scored **1–10**, with explicit weights, and grading must reflect only the
work shown (not host bias). The recommended rubric:

| # | Dimension (Elijah's word) | What it scores | Weight | How Claude/host reads it |
|---|---|---|---|---|
| 1 | **Quality** (build quality) | Does it work? Stability, completeness, technical execution, no obvious bugs | 25% | WebFetch the live URL / skim the repo README + structure; load on device if demoed live |
| 2 | **Performance** | Speed, responsiveness, load time, mobile behavior | 15% | Page-load feel; note heavy assets; honest "couldn't fully test live" when true |
| 3 | **Looks** (design/UX) | Visual polish, hierarchy, clarity, does the value prop land in 5s | 20% | Screenshot/first-impression read of landing + key screens |
| 4 | **Virality** | Shareability, hook, "would this spread / is it screenshot-able", positioning | 20% | The host's own niche instinct (Elijah's 2026 view-rank lens), NOT a fabricated metric |
| 5 | **Pro opinion** (the improve note) | The single highest-leverage change to make it better | 20% | One concrete, specific, actionable fix — the part the audience actually came for |
|   | **Overall** | Weighted 0–100 + a one-line verdict | — | Weighted sum, then a plain-English grade band |

Grade bands (holistic top-line on top of the analytic score): **90+ ship it / 70–89 strong, here's the gap /
50–69 real but rough / <50 back to the drawing board.** Two hosts → each scores independently, then average
(or note the split on camera — disagreement is good TV). This mirrors the "no more than five criteria, score
1–10, give each a weight, be specific about what each means" guidance from pitch-competition judging.

### The scoring honesty gate (the part that protects Elijah)
The format's value AND its risk both come from honest grading. The gate, baked into the skill:
- **Grade the work shown, never the person.** Critique the product, not the builder. (Reduces both bias and
  IG harassment-guideline exposure.)
- **Opinion-frame everything subjective.** "In my opinion / the way I'd do it" — opinion is legally protected;
  a false statement of fact is not. Never assert a factual claim about the product you haven't verified.
- **Every low score must carry a fix.** No naked dunk; the "pro opinion" dimension is mandatory and must be
  specific and actionable. This is what separates a *grading show* from a *pile-on*.
- **Lead with one genuine strength** before the gaps. Keeps it constructive and re-watchable.
- **No fabricated metrics.** "Virality" is the host's instinct, labelled as such — never a made-up number.

---

## Integration sketch (how it composes with the hub)

This is the strongest part of the case: it slots into the existing pattern with near-zero new surface area.

- **Engine/skill:** a new **`.claude/skills/live-software-review/SKILL.md`**, modeled directly on
  `carousel-builder/SKILL.md` (same agent-as-brain, draft-to-vault, gated-publish shape). No Python.
- **Brain:** Claude, applying the rubric — same `--provider agent` philosophy as `auto-clip`. Zero deps.
- **Reading submissions:** **WebFetch** for a submitted URL/landing page; **WebFetch / `gh`** for a GitHub
  repo (read the README + structure); the `instagram` MCP `get_comments` to *pull the actual "dropped"
  submissions* from the announcement reel's comments. (exa/tavily/firecrawl keys are dead — WebFetch only.)
- **Niche lens:** read `team/stats.md` so "virality" scoring reflects Elijah's real 2026 view-rank instincts
  (AI/Tech is his #3 category by views, ~960k/30d — this format lives squarely in a proven niche).
- **Output (data shapes):**
  - A per-submission **scorecard object**:
    `{project, url, scores:{quality,performance,looks,virality}, pro_opinion:str, overall:0-100, grade_band:str, one_strength:str}`
  - A vault **`idea` note** in `obsidian/Elijah's vault/20-Content/Ideas/` using the `idea` template's exact
    property block (`type: idea`, `domain: content`, `stage: raw`, `status: open`, `date_captured:`,
    `tags: [tanner]`), body = the announcement-reel script + per-submission scorecards + the episode prep
    checklist. Title Case filename. `[[Tanner]]` wikilink.
- **Composes outward:** the announcement video can be cut/captioned via `auto-clip` + `caption-engine`; a top
  episode can be repurposed into a saveable `carousel-builder` swipe post; `niche-intel` can suggest which
  tools to invite. The skill is the connective rubric; the existing suite does the media.

### Reusable live-prep checklist (ships inside the skill)
1. **Announce** (script the "drop your software in the comments" reel; Elijah approves before posting — Rule 1).
2. **Harvest** submissions from the reel comments (`instagram` MCP `get_comments`).
3. **Pre-score** each submission offline with the rubric (so live time = reaction + the "how to fix it", not
   first-discovery fumbling). Flag any that won't load / can't be tested.
4. **Safety pass** — drop anything sketchy (NSFW, scam-looking, a minor's project, a direct competitor it'd be
   unfair to grade). Note conflicts of interest (a friend's product → disclose on camera).
5. **Run sheet** — order submissions worst→best or by theme; pre-write each "one genuine strength."
6. **Live** — score on the rubric, hosts compare, deliver the fix. (Going live = Elijah's action, not Claude's.)
7. **Archive** — save the filled scorecards back to the vault note; log one learning to `team/memory.md`.

---

## Phased build sketch

- **Phase 0 (build now, ~1.5–2.5 hrs) — the rubric + skill, draft-only.**
  Write `.claude/skills/live-software-review/SKILL.md` (clone `carousel-builder`'s structure + rules block) and
  a canonical **rubric note** in the vault. Wire the WebFetch + `get_comments` submission-reading steps and the
  vault-note output. Acceptance test: feed it 1–2 real public SaaS landing-page URLs, confirm it produces a
  sane scorecard + a specific fix + a valid `idea` note that passes the property contract. **Nothing posts.**
  This is the entire safe, high-value core.

- **Phase 1 (after one real episode, optional) — capture loop.**
  Add a post-episode step that writes the *actual* grades given on the live back into the vault note and appends
  a `team/memory.md` learning (which tools graded well, which fixes landed, recurring weak spots → future
  content angles). Turns the series into a compounding idea-mine.

- **Phase 2 (only if the series sticks, optional) — light automation.**
  A `score-sheet` HTML overlay (transparent, OBS-friendly) the rubric can populate for on-screen scoring, OR a
  one-command "build next episode prep pack from the latest announcement reel's comments." Pure templating; no
  new heavy deps. Do NOT build until Phase 0 has run live ≥2–3 times and proven demand. Risk of over-building a
  format that may not recur.

**Stop rule:** if Elijah + Tanner don't actually go live with it within a couple weeks, this stays at Phase 0
(a rubric + skill that cost ~2 hrs) and that's fine — no sunk cost.

---

## Windows + OneDrive feasibility / dependency weight

**Cleanest possible profile — no flags.**
- **Dependencies:** ZERO new ones. No torch, no cv2, no heavy install, no model download, no cloud, no paid
  service. The skill is a Markdown file; the brain is Claude; reading uses WebFetch + the already-wired
  `instagram` MCP. (`gh` for repo reads is already present.)
- **OneDrive:** no heavy imports, no big files on the synced disk — it only writes small Markdown notes. None
  of the torch/cv2 hang risks apply.
- **Windows/PowerShell:** nothing to run; WebFetch and MCP calls are platform-agnostic. No subprocess, no PATH
  gotchas.
- **Cost:** $0 beyond normal Claude usage.

---

## Risks & compliance

- **Standing Rule 1 (the one that matters): draft-only, never auto-publish/post/comment/DM.** The skill DRAFTS
  the announcement reel script and the scorecards; **the "go live" click and any reply to a submitter is
  Elijah's**, per-action. The skill must never `post_comment` / `send_dm` / publish — same gate as
  `carousel-builder`. Verified: the deliverable stops at a vault note. ✅
- **Defamation:** honest, opinion-framed critique is legally protected; a *false statement of fact* is not. The
  honesty gate ("opinion-frame, never assert unverified facts, grade the work not the person") directly
  mitigates this. Low risk if the gate is followed. (Minc Law / RM Warner Law sources below.)
- **IG harassment/bullying guideline:** grading strangers' work on a live *can* tip into bullying if it becomes
  a dunk. Mitigation is baked in: lead with a strength, every low score carries a fix, critique product-not-
  person, drop minors'/sketchy submissions. This keeps it on the "constructive critique" side of the line.
- **Consent / fairness:** people who "drop their software in the comments" are opting in to being reviewed —
  that's the format's premise and reduces the harm surface. Still: skip a submission if it looks like a minor's
  project or could embarrass a real business unfairly; disclose any conflict of interest (friend's product).
- **No ban/ToS risk to the account** from the format itself — reviewing third-party products on camera is
  ordinary creator activity. The only ToS-adjacent line is harassment, handled above.
- **Honest low-value note:** this does not move the needle by itself. It's a force-multiplier on a format whose
  success depends entirely on the hosts' on-camera chemistry and the quality of submissions. Worth building
  because it's nearly free and removes real recurring friction — not because it's transformative.

---

## Sources

- [TAIKAI — Hackathon judging: 6 criteria](https://taikai.network/en/blog/hackathon-judging)
- [ScoreJudge — How to Judge a Startup Pitch Competition](https://scorejudge.com/blog/posts/how-to-judge-a-startup-pitch-competition/)
- [FasterCapital — Understanding Judging Criteria in Pitch Competitions](https://fastercapital.com/content/Understanding-Judging-Criteria-in-Pitch-Competitions.html)
- [DoraHacks — How to Design a Hackathon Judging Plan](https://dorahacks.io/blog/guides/hackathon-judging-plan)
- [Brown University — Designing Grading Rubrics](https://sheridan.brown.edu/resources/course-design/feedback-student-learning/grading-criteria-rubrics/designing-grading)
- [Statsig — Rubric design: effective grading criteria](https://www.statsig.com/perspectives/rubric-design-effective-grading)
- [SaaS Landing Page — Where to Get Your Landing Page Roasted](https://saaslandingpage.com/articles/where-to-get-your-landing-page-roasted-the-top-5-websites/)
- [Roast My Landing Page (Indie Hackers)](https://www.indiehackers.com/product/roast-my-landing-page/roast-my-landing-page-passed-20-000-new-design--MXVtO0xnSOI2Kp7Ujj-)
- [Roastd.io — AI website audit / roast](https://www.roastd.io/)
- [Minc Law — Defamation on Instagram (opinion vs. false fact)](https://www.minclaw.com/instagram-libel-defamation/)
- [RM Warner Law — Instagram's Terms of Service](https://rmwarnerlaw.com/blog/instagrams-terms-of-service-what-youre-really-agreeing-to/)
