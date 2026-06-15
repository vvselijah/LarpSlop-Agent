---
name: live-software-review
description: Prep the recurring "grade my software live with Tanner" segment — Elijah + Tanner publicly grade a software product on a reel/livestream against a fixed 100-point rubric (Quality 25 / Looks 20 / Virality 20 / Pro-fix 20 / Performance 15). Use when he says "grade my software", "grade this app live", "software review prep", "score this product", "prep the Tanner review", "rate my software", "live software grade", or hands over a product/app/URL to review on-camera. Produces DRAFT-only show-prep notes (segment script, the scored rubric card, talking points, the 60-sec recap) for Elijah + Tanner to review — NEVER publishes, posts, DMs, or spends money.
---

# Live Software Review — "Grade My Software Live with Tanner"

Show-prep for the recurring segment where **Elijah + Tanner grade a software product live**
(reel / livestream) against ONE fixed 100-point rubric, so every episode is comparable and
the score is defensible on camera. This skill DRAFTS the prep only — the segment script, the
filled-in rubric card, the talking points, and a 60-second recap script. **It never publishes,
posts, comments, DMs, or spends money** (CLAUDE.md rule 1); the final post is Elijah's call.

**Why a fixed rubric:** a recurring "I grade X" format only builds trust + bingeability when the
scale is consistent. Same five axes, same weights, every episode — so a 78 this week means the
same thing as a 78 next week, and viewers learn to predict (and argue with) the score. That
argument IS the engagement.

## The rubric (100 points, fixed — do NOT re-weight per episode)

| Axis | Pts | What it measures | Grade on |
|---|---|---|---|
| **Quality** | 25 | Does the core thing actually work? Robustness, correctness, no broken flows, edge-case handling, trustworthy output. | The product doing its ONE job well end-to-end. |
| **Looks** | 20 | Visual design, UI polish, brand, typography, consistency, "does it feel premium". | First-impression + a 2-min click-through. |
| **Virality** | 20 | Is it inherently shareable / demo-able? Wow-moment, screenshot-able output, built-in loops, "I have to show someone". | Whether a 15-sec clip of it would stop a scroll. |
| **Pro-fix** | 20 | The pro's fix-list: top 3 concrete changes that would most raise the score, and how cheap/expensive each is. Score = how *fixable* the gaps are (high = small lifts unlock big gains; low = deep rework needed). | The gap between where it is and where one focused sprint could get it. |
| **Performance** | 15 | Speed, load time, responsiveness, reliability under use, no jank/lag/crashes. | Real interaction latency, not a spec sheet. |

- **Total = sum of the five (max 100).** Always show the per-axis breakdown on screen, not just the total — the breakdown is the content.
- **Band labels** (for the on-camera verdict): **90-100 ship-it / category-leader · 75-89 strong, fixable · 60-74 promising but rough · 40-59 needs real work · <40 back to the drawing board.**
- Each axis gets a one-line *why* (the evidence), so the number is never a vibe. No half-credit hand-waving — tie every point to something you saw.

## Steps (workspace root: `C:\Users\elija\OneDrive\Desktop\ai agent team`)

1. **Load context first** (every path relative to the root):
   - `team/profile.md` — Elijah's voice + that Tanner is the technical co-founder/co-host (the rubric leans on his engineering eye; play the Elijah-energy / Tanner-depth dynamic).
   - `team/stats.md` — what his audience responds to (the recap should ride a niche he over-performs in — AI/Tech, Money, Founder).
   - `team/memory.md` — past learnings + any prior episode's score, so this one is comparable and you don't repeat a take.
   - If a product/app is being reviewed and Elijah supplies a URL or build, gather the evidence *non-destructively* (see Rule on tools below): a read-only click-through, screenshots, or a short demo — never sign up for paid tiers, never enter card details, never run write/destructive actions inside someone's product.

2. **Inspect the product against each axis and collect evidence.** For each of the five axes, note 1-2 concrete observations (what worked, what broke, the wow-moment, the lag). Keep receipts (a screenshot path, a timestamp, the exact broken flow) so the on-camera claim is defensible. If you can't verify an axis first-hand, say so and grade conservatively — never invent a result.

3. **Score each axis (integer points, ≤ its cap) with a one-line justification**, then sum to the total and pick the band label. Fill in the rubric card below. The **Pro-fix** axis doubles as the segment's payoff: list the **top 3 fixes**, each tagged *cheap / medium / heavy* lift and *which axis it raises*.

4. **Draft the segment script** (DRAFT — for Elijah + Tanner to review, never auto-posted):
   - **Hook (0-3s):** a scroll-stopper tied to the verdict — a number, a contrarian line, or the wow/fail moment ("this AI app is either a 90 or a 30, watch…"). Use Elijah's voice per `team/profile.md`: high-energy, plain-spoken, direct "you", CAPS for emphasis, disbelief/urgency, faith natural not preachy, never corporate.
   - **The walk-through:** axis by axis, Elijah reacts + Tanner adds the technical read; show the rubric card filling in live.
   - **The fix-list moment (Pro-fix):** the "here's how I'd 10x it" beat — the most shareable/value-dense part; this is what makes it a *pro* grading, not a hot take.
   - **The verdict:** reveal the total + band, then a one-line so-what.
   - **CTA:** ask for engagement (save / "what should we grade next" in comments / follow for the series) — drives the recurring-format flywheel.

5. **Write the on-screen rubric card + a 60-second recap script** so the segment can be cut down to a reel. The recap = hook + the five scores + the verdict + CTA, tight.

6. **Hand the prep to Elijah in chat** (the script, the filled rubric card, the talking points, the 60-sec recap). If — and only if — he asks to keep it, draft it as a vault `idea` note following the contract (see Rules); otherwise leave it in chat. **Stop here. Do not publish.**

7. **Log one dated learning** to `team/memory.md` (newest-first, one line): what was graded, the total + the axis that drove it, and the top fix proposed — so the series stays comparable episode-to-episode.

## Rubric card template (fill this in)

```
GRADE MY SOFTWARE — live with Tanner
Product: __________________            Date: __________
─────────────────────────────────────────────
Quality      __/25   — <why, evidence>
Looks        __/20   — <why, evidence>
Virality     __/20   — <why, evidence>
Pro-fix      __/20   — <why: how fixable the gaps are>
Performance  __/15   — <why, evidence>
─────────────────────────────────────────────
TOTAL        __/100   →  BAND: <ship-it / strong / promising / needs-work / drawing-board>

Top 3 fixes (the Pro-fix payoff):
 1. <fix>  [cheap|medium|heavy] → raises <axis>
 2. <fix>  [cheap|medium|heavy] → raises <axis>
 3. <fix>  [cheap|medium|heavy] → raises <axis>
```

## Rules

- **Rule 1 (CLAUDE.md): never publish, post, comment, or DM without explicit per-action confirmation from Elijah.** This skill stops at DRAFT prep (script, rubric card, recap, optional vault note). The final publish click is HIS — do not call any `publish_*` / `post_comment` / `send_dm` tool.
- **No spending, no signups, no destructive actions inside the reviewed product.** Grade via read-only inspection only — a click-through, screenshots, a short demo (computer-use / Claude-in-Chrome at read tier, or whatever Elijah hands over). Never enter card details, never start a paid trial, never run delete/write/irreversible actions in someone else's app. If an axis needs paid/destructive access to verify, grade it conservatively and flag the gap.
- **The rubric is fixed.** Same five axes, same weights (25/20/20/20/15), every episode — that consistency IS the format's value. Don't re-weight, add, or drop axes per product; if the rubric itself needs tuning, that's a separate proposal to Elijah, not an in-episode change.
- **Evidence over vibes.** Every axis score ties to something observed (a screenshot, a broken flow, a measured lag). If you can't verify it first-hand, say so — never fabricate a product's behavior, score, or screenshot.
- **Voice = Elijah, depth = Tanner.** Write the script in Elijah's voice (`team/profile.md`) and reserve the technical/engineering reads for Tanner's lines — the two-host dynamic is the show.
- **Vault property contract is law** if you save a note (`obsidian/Elijah's vault/CLAUDE.md` + `_templates/idea.md`): copy the `idea` block exactly (`type: idea`, `domain: content`, `stage: raw`, `status: open`, `date_captured:` today, `tags: []`); never invent or rename a property; leave unknown fields blank. The vault is otherwise read-only.
- **Rule 3 (CLAUDE.md): secrets only in Windows env vars (`setx`)** — never paste any token/credential into a note or anywhere on disk; this tree syncs to OneDrive.
- **Rule 7 (CLAUDE.md): after the run, append one dated learning to `team/memory.md`.**
