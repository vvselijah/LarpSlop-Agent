# SESSION COMPACT & HANDOFF — 2026-06-29

> **READ FIRST on resume.** Baton for the 2026-06-29 session. ✅ done+pushed · ⏳ pending · ⚑ needs Elijah.
> Two big threads this session: (1) **finished the viral scraper pipeline** (now LIVE), and (2) **deep-research
> plan for Elijah+Tanner's personal online SEO / Google Knowledge Panel**. Detail in the linked docs.

## 0. ENVIRONMENT NOTE (important)
This work was done in a **git worktree off the 2026-06-15 `main`** (`7dd1f9f`), branch
**`claude/objective-greider-1516e5`**, at `C:\Users\elija\OneDrive\Desktop\ai agent team\.claude\worktrees\objective-greider-1516e5`.
**All 2026-06-29 commits are PUSHED to `origin` on that branch** but **NOT merged to main** and **NOT yet a PR**
(gh CLI isn't installed — open the PR by clicking the URL in §4). The hub's "live" main may be a different/newer
tree (memory references a 2026-06-28 env-move); **verify these files exist / rebase before relying on the live main.**

## 1. THREAD A — VIRAL SCRAPER PIPELINE (✅ finished + live)
The pipeline is now end-to-end: **discover → track → tear down.**
- **`intel/niche-radar.py`** *(NEW)* — hashtag DISCOVERY via the **Apify `instagram-hashtag-scraper`**. The
  official Graph API hashtag endpoints are **App-Review-gated for this app** (`ig_hashtag_search` →
  `OAuthException #10`, live-probed 2026-06-29 — confirms HANDOFF §7), so a scraper is the only path to true
  view counts on arbitrary posts. Ranks per niche by views, auto-suggests winning NEW accounts into
  `watchlist.json`. Budget guards: `--dry-run`, `--results` clamp, no-408-retry, graceful skip if
  `APIFY_TOKEN` unset. Self-test imports the REAL `viral_teardown.POST_RE`.
- **`intel/niche-hashtags.json`** *(NEW)* — niche→hashtags config; seeded to Elijah's AI/founder niche
  (`ai,claude,aiagents,aitools,founder,startup,buildinpublic,indiehackers,vibecoding,saasfounder`).
- **`intel/viral_teardown.py`** *(modified)* — now reads BOTH `viral-report.md` + `niche-report.md` (deduped).
- **`Weekly Agent Refresh.bat`** *(NEW)* — wires niche-radar → viral-radar → viral_teardown + the other
  orphaned weekly engines (the level-up "activation gap" fix). ⚑ Scheduled-task install is Elijah's.
- **LIVE-VERIFIED:** real run = 297 reels scraped → 243 ranked → 24 suggested AI/founder accounts (e.g.
  @sabrina_ramonov, @rollins.io, @brycent, @seb.ai, @bennettx.ai), ~$0.77 (inside the $5/mo Apify free tier).

### Commits (all pushed to origin/claude/objective-greider-1516e5)
`922ff3d` engine + wiring · `9d0f727` memory · `73bf446` UTF-8 fix + real hashtags · `4b67560` refined
hashtags · `f3ca95e` memory live-run.

## 2. THREAD B — PERSONAL SEO / KNOWLEDGE PANEL (deep-research plan)
Elijah's ask: searching his/Tanner's NAMES should surface a real story (history, accolades, what they built)
+ ideally a Google Knowledge Panel — done the **cheapest legitimate way**. They have real credibility, ~zero
online footprint. **Full plan:** `docs/plans/2026-06-29-personal-seo-knowledge-panel.md` *(written from the
`personal-seo-knowledge-panel` research workflow — see that doc for the phased plan, cost ladder, and
start-here checklist).*

**Core findings (corrects the common myths):**
- A Knowledge Panel **can't be bought or "claimed into existence"** — it's the visible OUTPUT of Google
  becoming confident it understands you as an **entity**. Engineer the entity; the panel follows.
- **No fame bar in Google's Knowledge Graph** (unlike Wikipedia, ~87.6% of person-entities have no Wikipedia
  page). The gate is **data clarity + consistency across ~20 corroborating sources**, not celebrity — they
  qualify on substance, they're just invisible to the machine.
- **Path:** Phase 0 = own an **"Entity Home"** (a person page on `claritydigital.dev/team/...` + `schema.org/Person`
  + `sameAs`; identical name/bio/headshot everywhere) → Phase 1 = free structured entities (Crunchbase, Gravatar,
  About.me; **Wikidata only once you have independent references to cite**) → Phase 2 = cheap earned mentions
  (free journalist stack HARO/Featured/Qwoted, guest bylines, podcast guesting) → Phase 3 = notability / claim.
- **Cost:** the whole core is **~$10–20/yr** + time; everything that moves the needle is free. **AVOID** guaranteed-
  panel agencies, paid Wikipedia (deleted + backfires), pay-to-play "news", fake credibility — *more* dangerous
  for them precisely because they have real credibility to protect. **Timeline** ~3 weeks–3 months after the
  corroboration work (slower because "Elijah Sullivan"/"Tanner Carlson" have namesakes already ranking).
- The plan §7 holds a **substance bank** of their real, public-verifiable ventures for bios/articles, and
  explicitly flags the sensitive private beats to keep OUT of credibility material.

## 3. KEY GOTCHAS / LEARNINGS (don't relearn)
- **Official IG hashtag API is DEAD for this app:** `ig_hashtag_search` → `OAuthException #10` ("Instagram
  Public Content Access" needs App Review). Hashtag discovery REQUIRES a scraper. Don't re-attempt the
  official path.
- **`subprocess.run(curl, text=True)` decodes as cp1252 → crashes on UTF-8 emoji bytes (0x8d) → empty stdout.**
  Fix = `encoding="utf-8", errors="replace"`. Fixed in niche-radar; the SAME latent bug is in
  `intel/{viral,competitor}-radar.py` (a background-task chip was filed to fix them).
- **Hashtag TOPIC-collisions are real:** `#saas` = Hindi "mother-in-law" (saas-bahu comedy), `#ceo/#software/
  #developer` pull multilingual noise. View counts can't filter wrong-topic — only tag choice can.
- **Cost:** no safe FREE/LOCAL scraper path (OSS needs a login = ban risk to @elijahaifl). Apify ~$0.77/run,
  inside the $5/mo free credit. `apidojo/instagram-scraper` ~5× cheaper if the list scales (not wired).
  Bright Data has CONTRADICTORY hub-doc verdicts (protocol "Winner/5k free" vs blueprint "Tier C skip") — unresolved.
- Run Python via **PowerShell** (not Bash — no python on Bash PATH). `gh` CLI NOT installed.

## 4. NEXT STEPS (⚑ = needs Elijah)
1. ⚑ **Open the viral-pipeline PR** (1 click): https://github.com/vvselijah/LarpSlop-Agent/pull/new/claude/objective-greider-1516e5
2. ⚑ **Rotate the APIFY_TOKEN** — it was pasted in plaintext chat (this tree is OneDrive-synced). Regenerate
   in Apify Console → Settings → API; then `setx APIFY_TOKEN "<new>"`. (Current one works; it's stored in the
   User registry, not a file.)
3. ⚑ **Review/merge the background-task chip** fixing the cp1252 bug in viral/competitor-radar.
4. **Add discovered accounts to `watchlist.json`** (@sabrina_ramonov, @rollins.io, @brycent, @seb.ai…) so
   viral-radar tracks them with true official-API numbers.
5. ⚑ **Install the Weekly Agent Refresh scheduled task** (Sunday) to activate the orphaned engines.
6. **Personal SEO:** execute the START-HERE checklist in `docs/plans/2026-06-29-personal-seo-knowledge-panel.md`.
7. *(carried)* ⚑ revoke the OLD Gemini key (leaked in abc-wrap history) — see SESSION-COMPACT-2026-06-15 §4.

## 5. ARTIFACT MAP
- Viral pipeline: `intel/niche-radar.py`, `intel/niche-hashtags.json`, `intel/viral_teardown.py`,
  `intel/viral-radar.py`, `Weekly Agent Refresh.bat`, `intel/README.md` (§C). Generated (gitignored):
  `intel/niche-report.md`, `intel/viral-report.md`, `intel/viral-teardown.md`, `intel/data/`.
- Personal SEO: `docs/plans/2026-06-29-personal-seo-knowledge-panel.md`.
- Memory: `team/memory.md` (2026-06-29 entry); cross-session memory updated (automation-roadmap, env gotchas).
- Prior baton: `SESSION-COMPACT-2026-06-15.md`.
