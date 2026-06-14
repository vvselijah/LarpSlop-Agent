---
name: content-intel-2026
description: Build Elijah's 2026 content-intelligence briefing — what's actually working by the CORRECT 2026 IG-algorithm signals (skip/share/like/save/repost/comment rates + watch-time/retention), NOT raw likes or views. Use when he asks "what should I post", "what's working", "what's working in 2026 terms", "content briefing", "give me the content intel", "what's my data saying", "score my reels", "what to post more/less of", or wants a data-grounded next-post plan. Runs metrics2026 (2026 rate scoring), watchtime_ideator (retention/arbitrage), and viral-radar (competitor winners), cross-references his profile + stats, and outputs a single briefing with 2-3 concrete next-post ideas in his voice. DRAFT-only — saves an optional vault idea note for his review, NEVER auto-posts.
---

# 2026 Content-Intelligence Briefing

Synthesize Elijah's three NEW 2026 analytics engines + his context files into ONE
briefing: what's working by the *correct* 2026 signals (not raw likes/views), what
to post MORE / LESS of, which competitor reels to study, and 2–3 concrete next-post
ideas grounded in the data and his voice. The vault contract at
`obsidian/Elijah's vault/CLAUDE.md` is law; this skill DRAFTS only — never posts.

**Why this skill exists:** `team/stats.md` and the older skills still rank by VIEWS,
a downstream signal. The 2026 IG algorithm rewards retention/skip-rate first, then
shares > likes > saves > reposts > comments. These three engines compute that
ranking; this skill reads them so a briefing reflects 2026 reality, not vanity counts.

## Steps (workspace root: `C:\Users\elija\OneDrive\Desktop\ai agent team`)

1. **Run the three engines.** Python is NOT on the Bash PATH here — run each via
   **PowerShell** (`python ...`), all read-only over local data / live business_discovery.
   All three already exist and were committed; do not edit them.
   - `python ig-dashboard/metrics2026.py --n 25`
     → prints the top 25 posts by the **2026 composite score** (weighted percentile
     of share/like/save/repost/comment rates, gated on skip-rate). Note: `skip_rate`
     and `repost` are not yet in the store, so the skip gate is NEUTRAL and repost is
     never counted — read like/share/save/comment **rates per reach**, not raw counts.
   - `python ig-dashboard/watchtime_ideator.py --n 3`
     → prints the per-category watch-time (avg hold) table + the arbitrage call, and
     **writes** `ig-dashboard/data/watchtime-ideas.md`. Read that report for the full
     long-form seeds (the top-hold reels per winning category).
   - `python intel/viral-radar.py`
     → competitor leaderboards ranked by VIEWS (business_discovery), over-performer
     suggestions; **writes** `intel/viral-report.md`. This makes ~live API calls and
     can be slow or partially error if the token/endpoint throttles — if it stalls or
     a username errors, note it in the briefing and proceed on the two local engines
     (metrics2026 + watchtime_ideator run purely on local `store.json`).

2. **Read the engine outputs + his context.** After the runs:
   - `ig-dashboard/data/watchtime-ideas.md` — category hold table, the under-posted
     vs skip-risk arbitrage, and the long-form seed reels.
   - `intel/viral-report.md` — competitor winners by views + suggested watchlist adds.
   - `team/profile.md` — Elijah's voice, ranked niches, ventures (an idea can feed a venture).
   - `team/stats.md` — live numbers + category mix (the VIEWS view, for contrast).
   - `team/memory.md` — accumulated learnings; do not re-propose a failed experiment.

3. **Read the data by the CORRECT 2026 signals, not raw likes/views.** Translate:
   - From **metrics2026**: which posts top the 2026 composite, and which RATE drives
     them (share-rate is weighted highest at 40%, then like 25%, save 20%) — call out
     the *rate per reach*, not the headline count. Flag any throttled/`watch`-band
     skip grades if present.
   - From **watchtime_ideator**: the top-hold CATEGORY (his clearest long-form lane),
     the **"lean in"** list (holds attention but under-posted → post MORE), and the
     **"skip-rate risk"** list (rides reach, weak retention → post LESS or tighten the
     middle). This is the watch-time arbitrage — the headline of the briefing.
   - From **viral-radar**: 1–3 competitor reels worth studying, with WHY (the format/
     hook that won), tied to a niche he already over-performs in.

4. **Write the briefing to Elijah** (in chat). Structure it tight:
   - **What's working (2026 terms)** — top 2026-score posts + the rate that carried them.
   - **Post MORE** — the under-posted high-hold category/categories (the arbitrage win).
   - **Post LESS / fix** — the skip-rate-risk categories (reach without retention).
   - **Competitor winners to study** — 1–3 from viral-radar, each with the takeaway.
   - **2–3 next-post ideas** — each in his voice (per `team/profile.md`: high-energy,
     plain-spoken, direct "you", CAPS for emphasis, emoji-forward, disbelief/urgency
     hooks; faith natural never preachy; never corporate). For each idea give: the hook
     line, the format (talking-head / b-roll / AI-generated / carousel), the niche, and
     the **source signal it rides** (which 2026-score post, which arbitrage call, or
     which competitor reel). Ground every idea in a number you pulled — no vibes.

5. **Optionally save ONE keeper as a vault `idea` note (DRAFT, gated).** Only if Elijah
   asks to save it, or you flag a clear standout. Follow the vault contract EXACTLY:
   - Copy the property block from `obsidian/Elijah's vault/_templates/idea.md` verbatim:
     `type: idea`, `domain:`, `stage: raw`, `status: open`, `date_captured:`, `tags: []`.
     Never invent or rename a property; leave unknown fields blank.
   - Save to `obsidian/Elijah's vault/20-Content/Ideas/` with `domain: content`,
     `stage: raw`, `status: open`, `date_captured:` today, a Title-Case filename of the idea.
   - Body: the idea, the hook, the format/niche, the cited source signal (the exact
     metric/category/competitor reel it rode), and a one-line "why it should work in
     2026 terms." Use `[[wikilinks]]` for referenced people/projects/ventures.
   - This is a DRAFT for his review — it is NOT a publish.

6. **Log one dated learning** to `team/memory.md` (newest-first, one line): which 2026
   signal drove the briefing (e.g. the arbitrage category, the top 2026-score rate) and
   the next-post angle proposed — so the next session builds on it.

## Rules

- **Rule 1 (CLAUDE.md): never publish, post, comment, or DM without explicit per-action
  confirmation from Elijah.** This skill stops at the briefing + an optional DRAFT vault
  note. The final publish click is HIS — do not call any `publish_*` / `post_comment` /
  `send_dm` tool here.
- **Read-only engines.** All three engines and their data are read-only inputs; do NOT
  edit `metrics2026.py`, `watchtime_ideator.py`, `viral-radar.py`, `store.json`, or any
  engine file. The skill consumes their output, it does not change them.
- **Run Python via PowerShell, not Bash** — `python` is not on the Bash PATH in this hub.
- **2026 signals over vanity metrics.** Lead with skip/watch-time and the share>like>save
  rate order, NOT raw likes or raw views. Raw views (viral-radar, stats.md) are context
  for *competitor* reach and reach-vs-retention contrast only.
- **Vault property contract is law** (`obsidian/Elijah's vault/CLAUDE.md` + `_templates/idea.md`):
  copy the `idea` block exactly; never add or rename a property; leave unknown fields blank.
- **Rule 3 (CLAUDE.md): secrets only in Windows env vars (`setx`)** — never paste
  `INSTAGRAM_ACCESS_TOKEN` or any token into a vault note or anywhere on disk; this tree
  syncs to OneDrive.
- **Graceful degradation:** if viral-radar's live API is slow/throttled or a username
  errors, note it and proceed on the two local engines — never fabricate competitor data.
- **Rule 7 (CLAUDE.md): after the run, append one dated learning to `team/memory.md`.**
