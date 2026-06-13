---
name: carousel-builder
description: Turn an idea OR a proven high-performing reel/transcript into an Instagram carousel (hook slide + body slides + caption) and an optional text thread, saved as a vault idea note for Elijah to review/post — his highest-leverage untapped format (he runs ZERO carousels today). Use when he says "make a carousel", "turn this reel into a carousel", "carousel idea", "swipe post", "build a thread from this", or wants a saveable reference post. Optimizes for SAVES first; enforces the vault property contract in obsidian/Elijah's vault/CLAUDE.md and the standing rules in CLAUDE.md.
---

# Carousel Builder

Turn an idea or a proven reel into a saveable Instagram carousel (+ optional thread), drafted as a vault `idea` note for Elijah to approve — never auto-posted. Authoritative voice/niche/contract docs are referenced below by relative path; the vault contract at `obsidian/Elijah's vault/CLAUDE.md` is law.

## Steps

1. **Pin the workspace root and load context** (every path below is relative to `C:\Users\elija\OneDrive\Desktop\ai agent team`):
   - `team/profile.md` — Elijah's voice, ranked niches, ventures (carousel CTAs can feed a venture).
   - `team/stats.md` — live numbers, auto-fed daily; read the "Category mix" to pick the topic.
   - `team/memory.md` — accumulated learnings; do not repeat a failed experiment.
   - `obsidian/Elijah's vault/CLAUDE.md` — the property contract; read before writing any note.
   - `obsidian/Elijah's vault/_templates/idea.md` — copy its property block EXACTLY. The canonical keys are `type: idea`, `domain:`, `stage: raw`, `status: open`, `date_captured:`, `tags: []`. Never invent or rename a property.

2. **Choose the source signal (idea OR proven reel).** Two plays:
   - *Repurpose play (preferred):* pick a PROVEN winner from `team/stats.md` "Top posts" or via the `reel-analytics` skill / `instagram` MCP (`get_media_insights`), and reuse the reel's proven hook verbatim on slide 1. If a transcript is supplied, mine it for the body slides.
   - *Fresh-idea play:* take Elijah's idea and shape it into the same structure.
   In both cases record WHICH reel/idea it rode and WHY it should save well.

3. **Pick the topic for SAVES, then shares.** Carousels win on saveable, reference-style value. Prioritize **AI / Tech UTILITY** (his best save-rate, ~3.6%) and **Money / Finance** (his runaway view-leader, ~207k views/post — ~25x his Motivation niche). Avoid the oversupplied, weak Motivation/Life niche unless he asks.

4. **Write the slide deck in Elijah's voice** (per `team/profile.md`: high-energy, plain-spoken, direct "you", CAPS for emphasis, emoji-forward, hooks built on disbelief/urgency; faith natural never preachy; never corporate):
   - **Slide 1 = scroll-stopping hook** — a big claim, a number, or a contrarian line (reuse the proven reel hook when repurposing).
   - **Slides 2..n = one idea each** — punchy, swipeable, a single takeaway per slide so each is screenshot-worthy.
   - **Final slide = CTA** — explicitly ask to SAVE (primary) and share/follow, plus a soft faith or brand line where it lands naturally.

5. **Write the caption + the optional thread version:**
   - Caption: opening line that re-states the hook, a short value tease, then the CTA, then a tight hashtag set tuned to the chosen niche.
   - Optional thread: the same beats compressed into a tweet/X-style numbered thread (slide 1 = post 1, etc.) for cross-posting.

6. **Save it as a vault `idea` note** in `obsidian/Elijah's vault/20-Content/Ideas/` with `domain: content`, `stage: raw`, `status: open`, `date_captured:` today (`type: idea`, `tags: []` from the template). Title in Title Case with the carousel topic. In the body include: the full slide copy (numbered), the caption with hashtags, the optional thread, the cited source signal (which reel/idea it rode), and a one-line "why it should save well." Use `[[wikilinks]]` for any referenced people/projects. Follow the vault CLAUDE.md contract exactly — never add or rename a property.

7. **Optional publish path is GATED.** The skill DRAFTS only. Publishing a carousel uses `publish_carousel` via the `instagram` MCP and may only run AFTER Elijah's explicit, per-action confirmation for that specific post. (The voice-only/original-audio API constraint applies to API-published reels, not image carousels — but the per-action confirmation rule always applies.)

8. **Log one dated learning** to `team/memory.md` (newest-first, one line): which signal you rode, the topic, and the save-first rationale.

## Rules

- **Rule 1 (CLAUDE.md): never publish, post, comment, or DM without explicit per-action confirmation from Elijah.** Drafting the deck, caption, thread, and vault note is fine; creating the carousel container is fine; the final publish click is HIS. Do not call `publish_carousel` until he confirms that specific post.
- **Rule 3 (CLAUDE.md): secrets only in Windows env vars (`setx`), never written into files** — this whole tree syncs to OneDrive. Never paste tokens (e.g. `INSTAGRAM_ACCESS_TOKEN`) into the vault note or anywhere on disk.
- **Vault property contract is law** (`obsidian/Elijah's vault/CLAUDE.md` + `_templates/idea.md`): copy the `idea` property block exactly; never invent or rename a property; leave unknown fields blank rather than fabricating.
- **Rule 7 (CLAUDE.md): after the run, append one dated learning to `team/memory.md`.**
