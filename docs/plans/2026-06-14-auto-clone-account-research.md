---
type: research
status: complete
date: 2026-06-14
candidate_id: auto-clone-account
verdict: add-later
confidence: high
build_effort: multi-day (real build is weeks once you count a second IG account + token infra)
source_note: "[[What I need to do or start with the ai agent team]]"
---

# Research: Fully-automated clone account ("auto-clone-account")

**Verdict: ADD-LATER (lean toward SKIP the literal version).** Build the *generation + scheduling* engine — it's reusable and high-value. Do **not** build the literal "clone my viral content and re-post near-copies" account: Instagram's **April 2026 originality policy** makes that the single worst-positioned strategy on the platform right now. The honest move is to keep the human-in-the-loop, *transform* (not clone), and gate the whole thing behind the existing "never publish without per-action confirmation" rule until a fresh second account has proven its first 20-30 posts by hand.

---

## What the candidate actually is

From `40-Projects/LarpSlop/What I need to do...md` (line 4):

> "Figure out a way to create another entirely automated account that basically **clones all of my most viral content and iterates upon it** in a better way and post more educational niche specific content towards **one category**."

Decomposed, that's **four** distinct capabilities, only one of which is new:

| # | Capability | Hub status |
|---|---|---|
| 1 | Pick his best-performing content (which reels to remix) | **Already have it** — `ig-dashboard/` ranks 300 posts; `reel-analytics` skill reads it |
| 2 | Turn a proven piece into a *new* asset (new script/voice/visuals on the same idea) | **Mostly have it** — Higgsfield (img/video), ElevenLabs (TTS/voice), `caption-engine`, `auto-clip` reframe/caption. Missing: an *idea→new-script* generator aimed at ONE niche |
| 3 | Schedule + auto-publish to a **separate** account on a cadence | **Do NOT have it** — no second IG account, no second token, no scheduler that publishes (current scheduled task only *refreshes analytics*) |
| 4 | Run unattended ("entirely automated") | **Conflicts with the hub's #1 standing rule** (no publish without per-action confirmation) |

So "auto-clone-account" is really **#2 (a niche generation engine) + #3 (a publish scheduler) + a brand-new second IG account**, wearing the word "clone." #1 is solved and #4 is a policy non-starter as literally stated.

### The referenced tool: gethookd.ai — not relevant
The source note links `gethookd.ai`. Researched it: it is an **e-commerce / dropshipping ad-research tool** ("copy winning products and ads with 1 click," scaling-brand intel, AI image-ad generation) — [G2](https://www.g2.com/products/gethookd-ai/reviews), [IG](https://www.instagram.com/gethookd.ai/). It is **not** an Instagram content-cloning/autoposting platform and has no bearing on this build. Disregard.

---

## The decisive finding: Instagram's 2026 originality policy kills the literal "clone" thesis

The growth premise of a clone account is "post content the algorithm pushes to *new* (non-follower) audiences." That is exactly what Instagram restricted in **April 2026**:

- Accounts where "most of what you post is someone else's content" become **"no longer recommendable."** Originality is evaluated **monthly**, not per-post — so one bad month flips the whole account off recommendations. ([PetaPixel, 2026-04-30](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/))
- "**Watermarks, minor crops, or basic reposts are unlikely to qualify as 'original.'**" Meaningful **transformation** (commentary, remix, creative reinterpretation) is required to keep recommendation eligibility. ([PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/), [ALM Corp](https://almcorp.com/blog/instagram-restricts-reach-content-aggregators/))
- Penalty = "we're no longer gonna show your posts to people who don't follow your account" (Mosseri). Followers keep seeing you; **discovery/growth stops** — which is the *entire point* of a new account that has no followers yet.
- Separately, cross-posting near-duplicates draws **duplicate-content** down-ranking ([Socialync](https://www.socialync.io/blog/avoid-content-duplication-penalties-cross-posting-2026)), and aggressive automation risks an **80-95% reach shadowban** ([SocialzAI](https://socialz.ai/blog/how-to-fix-instagram-shadowban)).

**Nuance in his favor:** he wants to clone *his own* content, not strangers'. Reusing your own ideas isn't "aggregation," and re-shooting/re-scripting an idea into a different niche *can* be the "meaningful transformation" the policy explicitly allows. **But** the line is bright: if the clone account outputs near-copies (same VO, same edit, light crop), it trips the same signal and dies in its first monthly evaluation with zero followers to fall back on. The strategy only survives if each post is a genuine *new* asset on a proven *idea* — which is generation, not cloning.

**Honest takeaway:** the valuable, policy-safe product is *"mine my own winners for proven IDEAS, then generate brand-new niche assets from them."* The word "clone" should be retired from the spec.

---

## Tools / approach surveyed (2026 OSS + the honest "you already own most of this")

| Option | What it is | License | Fit |
|---|---|---|---|
| **Hub's own stack** (auto-clip + Higgsfield MCP + ElevenLabs MCP + caption-engine + ig-dashboard) | Already wired in both this hub and `abc wrap` | n/a (owned) | **Best.** The generation + reframe + caption + ranking halves exist. Build the thin glue. |
| [Reels-AutoPilot (Avnsh1111)](https://github.com/Avnsh1111/Instagram-Reels-Scraper-Auto-Poster) | Scrapes others' reels, auto-reposts | GPL-3.0 | **Avoid.** Literal aggregator; pure repost = exactly what the 2026 policy nukes; unofficial/browser posting = ban risk; **last release Aug 2023** (stale). GPL also infects. |
| [FullyAutomatedRedditVideoMakerBot (raga70)](https://github.com/raga70/FullyAutomatedRedditVideoMakerBot) | Reddit→short, posts to TikTok/IG/YT | GPL-3.0 | **Avoid.** IG path uses **instagrapi (unofficial)** → ban risk; **Vosk needs ~9GB RAM**, torch-class weight on OneDrive; **no longer maintained**. Useful only as a reference for the *YouTube-official* path. |
| [ReelsMaker (steinathan)](https://github.com/steinathan/reelsmaker) | Streamlit faceless-video generator (script→VO→subs→render) | check repo | Reference only. The hub's Higgsfield+ElevenLabs+caption-engine already cover this with better assets. |
| **n8n template #8918** (Heygen→Submagic→**Blotato**→IG) | No-code script→avatar→captions→auto-post | template free, **services paid** | Architecture reference. Posts via **Blotato** (3rd-party publisher), not official Graph API — extra cost + another ToS surface. Skip the SaaS chain; copy the *shape*. |

**Decision: build on the hub's own stack. No new OSS dependency, no scraper, no torch/cv2 added.** The one genuinely missing piece (idea→niche-script) is a Claude prompt + the existing analytics, not a library.

---

## Windows + OneDrive feasibility & dependency weight

- **No new heavy deps required.** Generation = Higgsfield/ElevenLabs **MCPs (cloud)**; transcribe/reframe/caption = the existing `auto-clip` engine (faster-whisper already vetted, runs as a subprocess). No new torch/cv2/Vosk. **Green** on the hub's "light deps / heavy models off the synced disk / heavy steps as subprocess" rule.
- **Avoid all unofficial-API libs** (instagrapi, Selenium reposters). They violate the hub's official-MCP-only posture and risk both accounts. The new account must publish via the **official Graph API** path the hub already uses.
- **OneDrive:** render scratch + any model cache must stay in a non-synced temp dir (same pattern auto-clip already follows). The scheduler's state file (queue) is small and fine on the synced tree.

---

## The real cost is account infrastructure, not code

A *second* account is not free in API terms ([Meta content-publishing docs](https://developers.facebook.com/docs/instagram-platform/content-publishing/), confirmed by [search synthesis](https://www.getphyllo.com/post/a-complete-guide-to-the-instagram-reels-api)):

- Needs its **own IG Business account**, linked to a FB Page, with its **own access token** (no shared token across accounts) → a **second `INSTAGRAM_ACCESS_TOKEN_CLONE` / `INSTAGRAM_ACCOUNT_ID_CLONE`** in Windows env vars, plus a **second 60-day token renewal** on the HANDOFF §4 cadence. Token sprawl is the real maintenance tax.
- **API publish constraints (apply to the clone account too):** **9:16, 5-90s, H.264/HEVC**; **~25-50 published/24h** per account ([InstantDM](https://instantdm.com/blog/instagram-api-rate-limits-explained-2026-developer-guide), [Postproxy](https://postproxy.dev/blog/instagram-reels-api-publishing-guide/)); **original-audio/voice-only only** — API-published reels **cannot** use trending/licensed audio (already a known hub constraint, and a real growth handicap for a from-zero account that leans on trending sound).

---

## Integration sketch — how it composes with the hub (if/when built)

Reuse, don't rebuild. New surface area is ONE skill + ONE small scheduler script + ONE config.

```
ig-dashboard/  ──(ranked winners JSON)──►  [niche-clone skill]
                                              │  1. pick top-N proven IDEAS in chosen category
                                              │     (reel-analytics reads ig-dashboard history)
                                              │  2. Claude rewrites each idea → NEW script (one niche, his voice)
                                              ▼
   ElevenLabs MCP (VO)  +  Higgsfield MCP (visuals)  +  auto-clip (reframe/caption/tighten)
                                              │  → finished 1080x1920 asset in  clone-out/
                                              ▼
                          docs/plans review note  ──►  ELIJAH APPROVES (per-asset)
                                              ▼
   [clone-scheduler.py]  → publish via official Graph API to the SECOND account
                            (INSTAGRAM_ACCESS_TOKEN_CLONE), pre-flight get_content_publishing_limit,
                            log permalink + ingest back into ig-dashboard for the feedback loop
```

**Data shapes (keep it boring/JSON):**
- `clone_queue.json`: `[{ source_permalink, idea, niche, script, asset_path, status: draft|approved|published, scheduled_for, published_permalink }]`
- The skill writes a **vault idea note** per asset (reuse the `idea` template + property contract) so review happens in Obsidian, mirroring how `carousel-builder` already drafts to the vault.
- Publish step reuses the **same instagram MCP** publish path (`publish_reel`) but parameterized by the clone account's id/token — so it inherits `get_content_publishing_limit` pre-flight and the voice-only rule for free.

**Where it plugs in:** new `niche-clone` skill (sibling to `carousel-builder`/`auto-clip`); `clone-scheduler.py` wired into `Daily Agent Refresh.bat` **as a draft-generator only** (never as an auto-publisher). It is `auto-clip`'s downstream sibling: auto-clip makes clips from a long video; this makes *net-new niche assets from proven ideas* and queues them.

---

## Phased build sketch

- **Phase 0 — manual proof (no code, do this first).** Stand up the second IG account by hand. Hand-make 15-20 niche posts by running existing skills (reel-analytics → pick idea → Higgsfield/ElevenLabs/auto-clip) and publishing manually. **Gate:** does a from-zero niche account actually grow under the 2026 originality regime? If it doesn't, stop — no engine fixes a dead strategy.
- **Phase 1 — generation skill.** `niche-clone` skill: ranked-winners → Claude idea-rewrite → new script → draft asset → vault idea note. Human approves. **No publishing yet.** (Days, mostly prompt + glue.)
- **Phase 2 — second-account publish path.** Provision `INSTAGRAM_*_CLONE` env vars + token; parameterize the instagram MCP publish; pre-flight limits; ingest result back to ig-dashboard. Still **per-asset confirmation.**
- **Phase 3 (optional, gated) — scheduler.** `clone-scheduler.py` queues approved assets on a cadence and surfaces a daily approval batch. **Never** a true auto-publish loop while the hub's #1 rule stands.

---

## Risks / honest assessment

1. **Strategy risk > build risk.** The 2026 originality policy means "clone" is the wrong word and the wrong plan. The build is easy; the *premise* is the thing most likely to fail. Phase-0 manual proof is non-negotiable.
2. **"Entirely automated" contradicts the hub's #1 standing rule.** Either he relaxes that rule for this one account (his call, explicit), or this is a *draft-generator with a human publish click* — which is what I'd ship.
3. **Token/account sprawl.** A second 60-day token renewal on the HANDOFF cadence; a second account to keep warm and un-shadowbanned.
4. **Voice-only API ceiling** handicaps a from-zero account that would otherwise lean on trending audio for reach.
5. **Brand/dilution risk.** A near-clone of @elijahaifl in one niche competes with the main account for the same audience and the same ideas; the upside over just posting that content on the main account is unproven.
6. **Cannibalization of effort.** Every asset the engine makes for the clone is an asset it could have made for the main 100k account. The opportunity cost is real.

**Where the value actually is:** Phase 1's **idea→niche-script generator** is genuinely useful *for the main account too* — it's the missing top-of-funnel for `auto-clip`/`carousel-builder`. Build that; treat the "separate automated account" as an experiment you run by hand first and only automate if Phase 0 proves it.

---

## Sources

- [PetaPixel — New Instagram Policies Target Reposted Content (2026-04-30)](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/) — the decisive originality policy
- [ALM Corp — Instagram Restricts Reach for Content Aggregators](https://almcorp.com/blog/instagram-restricts-reach-content-aggregators/)
- [Socialync — Avoid Content Duplication Penalties When Cross-Posting (2026)](https://www.socialync.io/blog/avoid-content-duplication-penalties-cross-posting-2026)
- [SocialzAI — How to Fix Instagram Shadowban (2026)](https://socialz.ai/blog/how-to-fix-instagram-shadowban)
- [Meta — Publish Content using the Instagram Platform](https://developers.facebook.com/docs/instagram-platform/content-publishing/)
- [InstantDM — Instagram API Rate Limits Explained (2026)](https://instantdm.com/blog/instagram-api-rate-limits-explained-2026-developer-guide)
- [Postproxy — Instagram Reels API Publishing Guide (2026)](https://postproxy.dev/blog/instagram-reels-api-publishing-guide/)
- [Phyllo — Complete Guide to the Instagram Reels API (2026)](https://www.getphyllo.com/post/a-complete-guide-to-the-instagram-reels-api)
- [Reels-AutoPilot (Avnsh1111) — GPL-3.0, last release Aug 2023](https://github.com/Avnsh1111/Instagram-Reels-Scraper-Auto-Poster)
- [FullyAutomatedRedditVideoMakerBot (raga70) — GPL-3.0, unmaintained, instagrapi+Vosk](https://github.com/raga70/FullyAutomatedRedditVideoMakerBot)
- [ReelsMaker (steinathan)](https://github.com/steinathan/reelsmaker)
- [n8n template #8918 — Heygen→Submagic→Blotato IG auto-post](https://n8n.io/workflows/8918-create-and-auto-post-instagram-reels-with-ai-clones-script-to-post-heygen-submagic-blotato/)
- [Gethookd.AI — G2 reviews (confirms it's e-commerce ad research, not relevant)](https://www.g2.com/products/gethookd-ai/reviews)
