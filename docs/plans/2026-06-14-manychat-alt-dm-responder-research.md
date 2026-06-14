# Research + Build Plan — Local on-brand DM-drafting responder (Manychat alternative)

**Candidate id:** `manychat-alt-dm-responder`
**Date:** 2026-06-14
**Source:** vault `Brainstorming/In the moment ideas.md` ("figure out Manychat alternative or create my own local version") + roadmap STILL-TO-RESEARCH (Automation), program jump-queue.
**Why he wants it:** Elijah's stated #1 pain at 100k followers — *"personally and accurately respond to all of my DMs as if it was me, in an extremely efficient manner considering the volume… only gonna grow."*

---

## HEADLINE VERDICT: ADD-LATER → with a buildable ADD-NOW Phase 0

**Confidence: high. Build effort: M (Phase 0: S).**

The research overturns the pessimistic assumption baked into `docs/PRODUCT-VISION.md`. That doc concluded DMs are "BLOCKED" behind Meta App Review (error `#3`). That conclusion is **half-wrong**:

- **Sending DMs to an account you OWN (`@elijahaifl`) is _Standard Access_ — which needs NO App Review.** Confirmed against Meta's own access-tier definition and three independent 2026 references. The only requirements are: the `instagram_business_manage_messages` permission (already on the token), the messaging *capability* enabled on the app, and a `messages` webhook subscription. The earlier `#3` "does not have the capability" error is an **app-configuration gap** (messaging product not added / webhook not subscribed on the `mybrain` app), **not** an App-Review wall.
- **App Review IS still the gate for the _7-day human_agent extension_ and for Business Verification** — but that only matters if Elijah needs to reply to a DM more than 24h after the follower's last message. Inside the rolling 24h window (which every new follower DM re-opens), no review is needed.

So the honest framing: **the proven `comment-triage` draft→approve→send pattern extends to DMs _now_, for the 24h window, with zero App Review** — pending one app-config fix Elijah does in the Meta dashboard. The full "answer every DM no matter how old" version needs App Review + Business Verification and is the ADD-LATER piece.

This is a high-value, on-pattern, mostly-already-built capability. The only reason it is not a clean ADD-NOW is the **app-config + live-send verification gate** (Phase 0 below) must clear first, and that depends on an Elijah action in the Meta dashboard.

---

## WHAT IT IS / WHAT IT DOES

A **local, human-in-the-loop DM responder** that mirrors `comment-triage` exactly, one channel over:

1. Pull the DM inbox (`get_conversations` → `get_conversation_messages`).
2. Classify each thread: **FAQ** / **lead** / **spam** / **needs-human**.
3. Draft a reply *in Elijah's voice* using `team/profile.md` + the FAQ knowledge base + thread context.
4. Present a review table — nothing sent.
5. On Elijah's explicit per-thread OK → `send_dm(recipient_id, message)`.
6. Log outcomes to `team/memory.md` (the same approve/edit/reject learning loop).

It is **not** a Manychat-style auto-responder. Manychat's core value (keyword auto-replies, comment→DM funnels, drip flows, link-in-bio bots) is mostly *auto-send*, which Standing Rule 1 forbids. What Elijah actually asked for ("respond as if it was me… at volume") is **AI-assisted drafting with his approval** — which is the higher-quality, lower-risk subset Manychat does *worst*. We're not cloning Manychat; we're building the human-in-the-loop responder it can't be.

### Live-tested state (2026-06-14)
- `instagram` MCP exposes `get_conversations`, `get_conversation_messages`, `send_dm` (all gated on `instagram_manage_messages`).
- Token `validate_access_token` → `valid: true`; scopes include `instagram_manage_messages` / `instagram_manage_messages`.
- `get_conversations` returned **"An unknown error has occurred"** (not the old `#3`). This is the Phase-0 blocker to diagnose — most likely the messaging product/webhook isn't fully configured on the `mybrain` app, or the conversations edge needs the linked Page. **Re-confirm before building.**

---

## BEST 2026 OSS / APPROACH + LICENSE

**Recommendation: do NOT adopt a third-party OSS DM platform. Extend the hub's own pattern.** Reference the OSS tools for ideas only.

| Tool | License | Stack / weight | Fit for this hub |
|---|---|---|---|
| **Chatwoot** (github.com/chatwoot/chatwoot) | MIT | Rails + Postgres + Redis + Sidekiq — **heavy**, multi-service server app | Overkill. It's a team helpdesk; we need a single-creator drafting skill. Self-hosting a Rails stack on a OneDrive-synced Windows box is exactly the kind of weight the hub avoids. **Skip.** |
| **insta-p8 / InstaAuto** (github.com/ayuuxh2/insta-p8) | MIT | Next.js 16 + Supabase + Groq/OpenAI proxy. Uses official Graph API v24. ~18 stars, modest. | Closest conceptual match (own Meta app, official API, MIT). But it **auto-sends on keyword triggers** — violates Standing Rule 1 — and pulls in Supabase + Vercel + a hosted LLM proxy we don't want. Good as a **reference for the webhook/scope wiring**, not as a dependency. |
| **ZernFlow** | MIT | Multi-platform flow builder | Auto-flow oriented (same auto-send problem). Reference only. |
| Botpress / Typebot / Chaskiq | MIT/AGPL | Bot-builder servers | Wrong shape (flow bots, not draft-and-approve). |

**Why build-not-adopt:** the hub already owns the hard parts — the official `instagram` MCP (auth via Windows env var, the secrets rule), the `team/` voice + memory system, and the proven `comment-triage` draft→approve→send loop. A DM responder is **~90% a copy of `comment-triage` with the `send_dm` edge swapped in.** Adopting Chatwoot/insta-p8 would *add* a heavy server, *add* a second auth path, and *fight* the never-auto-send rule. Net negative.

**License note:** nothing to adopt, so no license obligation. If we lift a snippet from insta-p8 (MIT) for webhook wiring, attribute it.

---

## WINDOWS + ONEDRIVE FEASIBILITY + DEPENDENCY WEIGHT

**Green across the board.** This is a *light* build:

- **No torch / cv2 / transformers / cloud / paid SaaS.** The "AI" is Claude itself drafting in-session (same as `comment-triage` and the auto-clip `--provider agent` pattern). No local model, no big download off the synced disk.
- **No new server.** It's a skill (markdown + MCP calls), not a service. Nothing to keep running, nothing to sync-thrash.
- **Secrets:** reuses the existing `INSTAGRAM_ACCESS_TOKEN` Windows env var via the `instagram` MCP. No new secret, no file writes (Rule 3 safe).
- **OneDrive:** only artifacts are a skill `SKILL.md`, an optional FAQ knowledge-base markdown, and `team/memory.md` log lines — all tiny text. No sync risk.

The **only** non-trivial dependency is the **Meta app configuration** (add the messaging product, subscribe the `messages` webhook) — and webhooks need a public HTTPS callback. For a draft→approve workflow we can **poll `get_conversations` on a schedule instead of running a webhook listener**, sidestepping the public-endpoint requirement entirely on a local Windows box. (Webhook = optional later optimization, not a Phase-0 requirement.)

---

## HOW IT COMPOSES WITH THE HUB (integration sketch)

**Shape: a new skill `dm-triage`, sibling to `comment-triage`.** Reuses the exact same scaffolding.

```
inbound DMs                                 Elijah
   │  instagram MCP                            │ per-thread OK
   ▼                                           ▼
get_conversations ──► get_conversation_messages ──► [classify] ──► [draft in voice] ──► review table ──► send_dm
   (poll, daily/on-demand)                         │  team/profile.md (voice + niches)        │
                                                   │  FAQ knowledge base (merge fields)       │ only on explicit OK
                                                   └─ team/memory.md (approve/edit/reject loop)┘
```

- **Engine/skill:** new `.claude/skills/dm-triage/SKILL.md` — copy `comment-triage/SKILL.md`, swap the edges.
- **MCP:** `instagram` MCP — `get_conversations`, `get_conversation_messages` (read), `send_dm` (write, gated on confirmation).
- **Data shapes:**
  - `get_conversations` → `[{ id (conversation_id), participants[{ id: IGSID }], updated_time }]`
  - `get_conversation_messages(conversation_id)` → `[{ from{id}, message, created_time }]`
  - `send_dm(recipient_id = IGSID, message ≤1000 chars)`
  - Classification record (in-session, not persisted): `{ conversation_id, igsid, bucket, draft_text, last_inbound_ts, within_24h: bool }`
- **Context system:** `team/profile.md` (voice), `team/memory.md` (learning loop), shared FAQ knowledge base (could be one markdown file reused by both comment- and DM-triage so the FAQ answers stay in sync).
- **Scheduling:** optional later — chain a poll into `Daily Agent Refresh.bat` to surface "X DMs waiting, Y inside the 24h window" each morning. **Do not auto-send from the scheduled run** — it only queues; Elijah approves interactively.
- **24h-window awareness is a first-class field.** The skill must compute `within_24h` per thread from `last_inbound_ts` and **visually flag** threads where the window has closed (those need the human_agent tag → App Review → Phase 3, or Elijah replies in-app manually). This is the one real difference from `comment-triage`.

---

## PHASED BUILD SKETCH

### Phase 0 — Unblock + verify the send path (smallest safe thing) — **Elijah-gated, ~30 min**
1. Diagnose the `get_conversations` "unknown error." Most likely fix: in the Meta App Dashboard for the `mybrain` app, **add the Instagram messaging product** and ensure the linked Page/Instagram account and `messages` webhook field are subscribed. (Elijah action — config, not code.)
2. Confirm read works: `get_conversations` → `get_conversation_messages` return real threads.
3. **Single live send test:** Elijah DMs the account from a second handle (opens the 24h window), then we `send_dm` one approved reply to that IGSID. If it lands → the whole architecture is unblocked with **zero App Review**.
- **Exit:** one human-approved DM successfully sent within the 24h window. If this fails with a capability error, the gate really is App Review and we drop to ADD-LATER-only.

### Phase 1 — `dm-triage` skill (draft→approve→send, 24h window only) — **S/M, no new deps**
- Copy `comment-triage/SKILL.md` → `dm-triage/SKILL.md`. Swap: queue source (`get_conversations`/`get_conversation_messages`), send edge (`send_dm`), add the `within_24h` flag + "window closed" handling, drop the hide/delete logic (no DM equivalent).
- Same four buckets, same voice drafting, same review table, same `team/memory.md` loop.
- Reuse/extract a shared FAQ knowledge base both triage skills read.
- **Exit:** Elijah runs "triage my DMs," gets a review table, approves a few, they send, outcomes logged.

### Phase 2 — Volume ergonomics — **S**
- Pagination over many conversations; batch the review table; pace under limits (Conversations API 2/s, sends 100/s — generous, but throttle politely).
- Optional morning poll wired into `Daily Agent Refresh.bat`: "N DMs waiting, M inside 24h." Queue-only, never auto-send.
- FAQ knowledge-base tuning from `memory.md` patterns (the recurring "how do I get put on" etc.).

### Phase 3 — ADD-LATER: beyond-24h via human_agent tag — **needs Elijah + Meta App Review + Business Verification**
- For threads where the window closed, the `human_agent` tag extends to 7 days — but it **requires App Review + Business Verification**, and Meta frames it as *for live human agents, not automation.* Our draft→**human-approves**→send is arguably exactly that, but it's a real submission with lead time and rejection risk.
- **Treat as a separate Elijah-gated decision.** Phases 0–2 deliver most of the value (the bulk of inbound DMs get answered within 24h if he runs triage daily). Only pursue Phase 3 if the closed-window backlog proves material.

---

## RISKS / ToS / BAN RISK

- **Standing Rule 1 (never auto-send):** the entire design is draft→approve→send, per-thread explicit OK. The scheduled poll must **queue only**. This is the load-bearing constraint — bake it into the skill rules verbatim, as `comment-triage` does.
- **24h-window violations:** sending outside the window without the human_agent tag → API error and, if abused, integrity flags. Mitigation: the `within_24h` flag *gates* the send button; closed-window threads are surfaced for in-app manual reply, not API send.
- **Rate / spam integrity:** even with human approval, blasting many near-identical DMs fast can trip Meta's spam heuristics on a 100k account. Mitigation: pace sends, vary drafts (merge fields, real per-thread context), don't bulk-send templated text. Limits are generous (100 text/s) but *behavioral* spam detection is the real risk, not the rate cap.
- **"Respond as if it was me" quality risk:** a wrong-voiced or factually-off auto-draft sent to a real follower/lead is worse than a late reply. Mitigation: the `needs-human` bucket (emotional / faith-sensitive / ambiguous / high-value lead) gets **no draft** — handed to Elijah. Same rule as comments.
- **App-config dependency:** Phase 0 hinges on an Elijah action in the Meta dashboard (and possibly Business Verification even for Standard Access on a Page-linked account — re-confirm during Phase 0). If that stalls, the whole thing stalls. Honest: this is the single biggest schedule risk.
- **No paid-SaaS / scraper risk:** we use only the official Graph API + official MCP. No Manychat, no unofficial scraping, no ToS gray area on access.

---

## HONEST BOTTOM LINE

This is one of the **highest-value, lowest-weight** candidates in the queue: it's Elijah's literal #1 pain, it's ~90% a copy of an already-proven skill, it adds **zero heavy dependencies**, and — contrary to the hub's prior assumption — the core 24h-window version needs **no App Review**. The verdict is ADD-LATER *only* because of the Phase-0 app-config/live-send gate that needs an Elijah action and one verification pass; the moment that single DM send succeeds, promote Phase 1 to build-now. Do **not** adopt Chatwoot/insta-p8 — they'd add weight and fight the never-auto-send rule. Build the `dm-triage` skill instead.

---

## SOURCES

- Meta official — [Instagram API with Instagram Login: Messaging API](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api) (Advanced vs Standard Access; 24h window; human_agent tag; `instagram_business_manage_messages`)
- Meta official — [Send Messages using the Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/)
- [Instagram Official APIs — Comprehensive Reference (April 2026)](https://gist.github.com/jameschapman2c/65eff9f54a2d350b17a6ce5127b9fe42) (Standard Access own-account needs no review; human_agent → 7 days needs App Review + Business Verification; rate limits 100 text/s, Conversations API 2/s)
- [Instagram Messaging API 24-Hour Window Policy: The Complete Guide (2026) — keyapi.ai](https://www.keyapi.ai/blog/instagram-messaging-api-policy/) (24h window mechanics; human_agent 7-day support window; 200 automated msg/hr cap noted as of Oct 2024)
- [How to Integrate the Instagram Messaging API: 2 ways in 2026 — zernio.com](https://zernio.com/blog/instagram-messaging-api) (App Review weeks-to-months for serving accounts you don't own; 25 test users in dev)
- [6 Best Open Source Manychat Alternatives in 2026 — openalternative.co](https://openalternative.co/alternatives/manychat)
- [Chatwoot (MIT) — github.com/chatwoot/chatwoot](https://github.com/chatwoot/chatwoot)
- [insta-p8 / InstaAuto (MIT) — github.com/ayuuxh2/insta-p8](https://github.com/ayuuxh2/insta-p8) (Next.js+Supabase, official Graph API, auto-sends on keyword triggers)
- Internal: `docs/PRODUCT-VISION.md` (prior live-tested DM/App-Review findings — partially corrected here), `.claude/skills/comment-triage/SKILL.md` (the pattern this extends), vault `Brainstorming/In the moment ideas.md` (the original ask)
