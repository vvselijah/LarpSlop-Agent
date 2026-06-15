---
name: artifacial-ad-ideator
description: Draft analytics-grounded ad CONCEPTS for Artifacial (Elijah's AI Character & Video Studio venture) — one ad idea per Artifacial tool (Face Swap, Image-to-Video, Lip Sync, etc.), each grounded in what's actually working on his Instagram by 2026 signals. Use when he says "ad ideas for Artifacial", "draft Artifacial ads", "promote Artifacial", "ad concepts for my video studio", "what ads should I run for Artifacial", "ideate ads per tool", or wants a per-tool creative brief for the Artifacial product. Fans over intel/artifacial-tools.json and DRAFTS each concept as a vault idea note for his review. DRAFT-ONLY — never creates a campaign, never publishes, ZERO ad spend; the publish/spend click is always Elijah's.
---

# Artifacial Ad Ideator

Fan over the Artifacial tool catalog and DRAFT **one analytics-grounded ad concept
per tool** — each tied to a real signal from Elijah's own Instagram performance, each
saved as a vault `idea` note for his review. Artifacial is one of Elijah's ventures
(an AI Character & Video Studio — face-swap / image-to-video; see active ventures in
`obsidian/Elijah's vault/CLAUDE.md`), so promoting it is on-mission.

**Hard stop:** this skill produces DRAFTS only. It NEVER creates a Meta campaign/ad/ad
set, NEVER publishes a post, and spends ZERO dollars. Per CLAUDE.md Rule 1 + Rule 2, the
final publish click and any ad write are Elijah's, per-action. Do not call any
`ads_create_*`, `ads_update_*`, `publish_*`, `post_comment`, or `send_dm` tool here.

## Inputs (workspace root: `C:\Users\elija\OneDrive\Desktop\ai agent team`)

- **`intel/artifacial-tools.json`** — the tool catalog you fan over. `tools[]` each have
  `name`, `slug`, `what`, `ad_angle`, `verified`. This is the loop's source of truth.
- **Analytics grounding (use what's available; degrade gracefully):**
  - `python ig-dashboard/metrics2026.py --n 25` (via **PowerShell** — Python is NOT on the
    Bash PATH here) → top posts by the 2026 composite score; note WHICH rate carries them
    (share-rate weighted highest, then like, then save). Read-only.
  - `ig-dashboard/data/watchtime-ideas.md` if present (from `watchtime_ideator.py`) → the
    high-hold categories = the formats worth pointing an ad at.
  - `team/profile.md` — Elijah's voice + ranked niches (so each ad sounds like him).
  - `team/stats.md` — live category mix / top formats, for contrast.
  - `team/memory.md` — accumulated learnings; don't re-propose a dead angle.
  - If an engine throttles, errors, or a file is missing, note it and proceed on whatever
    grounding you DO have (even just `profile.md` + `stats.md`). Never fabricate a metric.

## Steps

1. **Load the catalog.** Read `intel/artifacial-tools.json`. Validate it parses and that
   `tools` is a non-empty list. If a tool is marked `"verified": "_unverified"`, keep it but
   flag the resulting draft as `[UNVERIFIED TOOL — confirm on artifacial.io before running]`.

2. **Pull the analytics grounding.** Run `metrics2026.py` (PowerShell) and read the context
   files above. Identify: (a) the 1–3 hooks/formats currently WORKING by 2026 signals (the
   top-composite posts + the rate that carried them), and (b) Elijah's strongest niches. These
   are the proof each ad concept must ride — every concept cites a real signal, not a vibe.

3. **Fan over the tools — one concept per tool.** For EACH entry in `tools[]`, draft an ad
   concept that maps the tool's `ad_angle` onto a working signal. Each concept = :
   - **Hook line** — in Elijah's voice (per `profile.md`: high-energy, plain-spoken, direct
     "you", CAPS for emphasis, emoji-forward, disbelief/urgency; faith natural, never preachy;
     never corporate).
   - **Format** — talking-head demo / screen-capture demo / before→after / b-roll, chosen to
     match a high-hold format from the analytics, not at random.
   - **The signal it rides** — the EXACT metric/post/category it's grounded in (e.g. "rides the
     share-rate winner [post X], a before→after reveal that holds attention").
   - **CTA** — soft, on-brand, pointing to the free tier (sign-up gives free generations); no
     spend, no urgency-pressure dark patterns.
   - **Why it should work (2026 terms)** — one line tying the tool to the retention/share logic.

4. **Save each concept as a vault `idea` note (DRAFT).** Follow the vault property contract
   in `obsidian/Elijah's vault/CLAUDE.md` EXACTLY — copy the block from
   `obsidian/Elijah's vault/_templates/idea.md` verbatim and fill values only:
   - `type: idea` · `domain: content` · `stage: raw` · `status: open` ·
     `date_captured:` today (YYYY-MM-DD) · `tags: []` (leave `[]` or add at most a sparse
     theme like `artifacial`, `ad` — never invent a NEW property name).
   - Save to `obsidian/Elijah's vault/20-Content/Ideas/` with a Title-Case filename like
     `Artifacial Ad - Face Swap.md` (one note per tool).
   - Body: use the template's `## The idea` / `## Why it might work` / `## Why it might not`
     / `## Next step (if any)` sections. Put the hook + format + CTA under "The idea"; the
     cited signal + "why it should work in 2026 terms" under "Why it might work"; the obvious
     risk (e.g. demo fatigue, weak proof) under "Why it might not"; and "Next step" = a
     DRAFT-only line such as "Elijah reviews → if approved, record the demo; no spend yet."
   - Use `[[wikilinks]]` for `[[Artifacial]]` and any referenced post/person/project.
   - These are DRAFTS for his review — NOT a publish, NOT a campaign.

5. **Summarize in chat.** A tight table: tool → hook → format → signal it rides → vault note
   path. Lead with the 1–2 strongest concepts (the ones riding the best signal). End with the
   explicit reminder: these are drafts, zero spend, the publish/ad-create click is Elijah's.

6. **Log one dated learning** to `team/memory.md` (newest-first, one line): which Artifacial
   tools got concepts, which working signal anchored them, and any tool that lacked grounding.

## Rules

- **DRAFT-ONLY, ZERO SPEND (CLAUDE.md Rule 1 + Rule 2).** Never create/edit/pause a Meta
  campaign, ad set, ad, audience, or budget; never publish a post or DM. Stop at vault `idea`
  notes + the chat summary. Any ad write or publish is Elijah's per-action confirmation.
- **Ground every concept in a real number.** Each ad must cite a specific metric/post/category
  from the analytics. If you have NO grounding for a tool, say so in that draft ("Why it might
  not": "no direct signal yet — test small") rather than inventing one.
- **Run Python via PowerShell, not Bash** — `python` is not on the Bash PATH in this hub. The
  analytics engines are READ-ONLY inputs; do not edit `metrics2026.py` or any engine file.
- **Vault property contract is law** (`obsidian/Elijah's vault/CLAUDE.md` + `_templates/idea.md`):
  copy the `idea` block exactly; never add or rename a property; leave unknown fields blank.
- **One concept per tool** — the catalog (`intel/artifacial-tools.json`) is the loop; don't
  skip tools and don't bolt on tools that aren't in the JSON (re-fetch + edit the JSON first).
- **Voice is Elijah's, not corporate** (`team/profile.md`). The ad is for HIS product; it
  should sound like his reels, not a SaaS landing page.
- **Graceful degradation:** if an engine throttles or a file is missing, proceed on whatever
  grounding remains and flag the gap — never fabricate a metric or a tool.
- **Secrets stay in env vars (CLAUDE.md Rule 3)** — never write a token into a vault note; this
  tree syncs to OneDrive.
- **Rule 7 (CLAUDE.md): after the run, append one dated learning to `team/memory.md`.**
