# Research + Build Plan — DM triage that routes Archetype-Index leads (sales layer on the DM responder)

**Candidate id:** `dm-routing-va-or-agent`
**Date:** 2026-06-14
**Source:** roadmap STILL-TO-RESEARCH → Automation (`docs/plans/2026-06-14-overnight-roadmap.md` line 79) + vault `40-Projects/Archetype-Index/To do.md` ("Go ahead and hire a VA to go through our DMs and route potential archetype clients to the index").
**Why he wants it:** highest-leverage remaining automation. Sits directly on top of `manychat-alt-dm-responder` (Wave-2), whose finding — *DMing his own account is Standard Access, no App Review* — unblocked it. It attacks his stated #1 pain at 100k (DM volume) AND adds the monetization layer: routing/qualifying Archetype-Index sales leads, turning triage into revenue.

---

## HEADLINE VERDICT: ADD-LATER → a thin lead-routing layer on top of the (gated) `dm-triage` skill. Confidence: high. Build effort: S (one extra bucket + a vault lead-note writer; ~½-day once `dm-triage` Phase 0 clears).

**The honest core:** this is **not a new system** — it is **one classification bucket and one vault-note side-effect added to the `dm-triage` skill** that `manychat-alt-dm-responder` already specs. The vault To-do literally says "hire a VA to route potential archetype clients to the index." Strip the human VA and that is: detect lead-intent in a DM thread → qualify it → draft the routing reply (in-thread, never cold) → log the lead as a vault note so it doesn't fall through the cracks. The hard parts (DM read/send, voice drafting, the draft→approve→send loop, the 24h-window logic) are **all already designed in the `dm-triage` plan**. This candidate adds the *sales semantics* on top.

**Why ADD-LATER, not ADD-NOW:** it is **strictly gated on `dm-triage` Phase 0** — the one live human-approved DM send must succeed first (Elijah-actioned Meta-dashboard config + a single send). Until DMs send at all, a routing layer has nothing to route *on*. The moment that gate clears, this is a small, high-value follow-on build, not a separate project.

**One sharp correction to the framing:** "routing" must mean **drafting a reply inside an existing conversation**, never **proactively DMing a sales link to someone**. The 2026 Meta rules are unambiguous: you may only message someone who messaged/commented/replied first; sending the first message or pushing promo to a non-engager is **cold DMing = a bannable integrity violation** (see Risks). So the routing layer rides the *same* inbound-only, 24h-window, human-approved rails as `dm-triage`. It qualifies and drafts; it never prospects.

---

## WHAT IT IS / WHAT IT DOES

A **sales-qualification + routing layer** on the `dm-triage` skill. Same draft→approve→send loop; the new work is what happens to the **`lead`** bucket:

1. `dm-triage` already classifies each thread FAQ / **lead** / spam / needs-human.
2. **New: qualify the `lead` bucket.** When a thread shows Archetype-Index buying intent ("how do I get on the index", "what's the cost", "I want a report", "how does the archetype thing work"), score it:
   - **intent** (curious vs ready-to-buy), **fit** (is this an Archetype-Index prospect vs a generic biz inquiry), **stage** (cold question / warm / asked-about-price-or-link), and **next action** (answer + soft-route, send the Index link, or hand to Elijah/Tanner for a high-value close).
3. **Draft the routing reply in-thread, in Elijah's voice** — answer the question, then route: explain the Archetype Index briefly and (only when it fits) include the canonical link/next step. Drafted with merge fields, never a blasted template.
4. **Write a vault lead note** (`type: idea` or a lightweight per-lead record) so the prospect is tracked even if the conversation goes cold — this is the "don't let leads fall through" job the VA would do.
5. **Present the review table** — bucket, qualification score, draft reply, and "log as lead? y/n." Nothing sent, nothing written, without Elijah's per-item OK.
6. On approval → `send_dm` the reply + write the vault note. Log the outcome to `team/memory.md`.

**It is a sales setter that drafts, not a closer that acts.** The 2026 SaaS that does this auto-magically (SetSmart, TailorTalk, FlowGent, Inrō — all "GPT-powered, qualifies leads, books appointments, routes by intent") is exactly the category — but every one of them **auto-sends**, which Standing Rule 1 forbids. Inrō even names the precise feature ("AI Agent qualifies leads, captures contact data mid-conversation, and routes by intent"), validating that the pattern is real and worth building — just not the auto-send mechanism. We build the human-in-the-loop subset they do worst.

---

## BEST 2026 OSS / APPROACH + LICENSE

**Recommendation: build the routing semantics in-skill (Claude-as-qualifier) + a vault note as the lead store. Adopt NOTHING.** Two adoption paths were evaluated and both rejected:

| Option | License | Stack / weight | Verdict for this hub |
|---|---|---|---|
| **DM-automation SaaS** — SetSmart, TailorTalk, FlowGent, **Inrō** (€12.99/mo+), Chatfuel ($14.99/mo), respond.io ($79/mo) | Proprietary SaaS | Hosted GPT bots over the Graph API | **SKIP — they auto-send.** Their core (real-time AI conversations, auto-qualify, auto-route, auto-book) is auto-send by design → violates Standing Rule 1. respond.io is the only one with real human-handoff/routing, but it's a $79/mo team helpdesk — wrong shape for one creator. Useful only as a **feature spec** of what "good routing" looks like. |
| **OSS CRM as the lead store** — SuiteCRM, Twenty, X2CRM, Frappe CRM | varied (mostly free self-host) | **Heavy**: MySQL/Postgres + Docker/Node server | **SKIP — OneDrive-hostile + overkill.** The CRM survey was explicit: "most require traditional databases (MySQL, PostgreSQL) rather than JSON-based local storage… If you specifically need a JSON-based, database-free solution, you may need to explore simpler alternatives or custom development." Running a Rails/Node CRM + DB on the OneDrive-synced Windows box is exactly the weight the hub avoids. The vault **is** his single-user CRM already. |
| **Lead-scoring ML model** (per the "build a proper lead scoring agent" pattern) | n/a | Supervised model trained on closed deals | **SKIP for now — wrong scale.** That pattern argues (correctly) that *LLMs are unreliable scorers over large structured datasets* and you should train on historical conversions. But Elijah has **no labeled lead/close dataset** and **low DM volume per day** of *unstructured conversational text* — the exact regime where the other finding holds: "LLM semantic understanding dramatically outstrips keyword-based intent detection." So **Claude-as-qualifier is the right call**, not a trained model. Revisit ML scoring only if/when a meaningful labeled lead→close history accumulates. |

**Why build-not-adopt (same logic as `dm-triage`):** the hub already owns every hard part — the `instagram` MCP (auth via env var), the `team/` voice system, the vault (the CRM), and the proven draft→approve→send loop. The lead-routing layer is **a prompt (qualification rubric) + a vault-note writer**, both of which are in-skill text. Adopting any external tool would add a server, a second auth path, a paid subscription, or an auto-send mechanism — all net-negative here.

**License note:** nothing adopted → no license obligation. If a routing-rubric idea is lifted from a SaaS feature page, it's a concept, not code.

---

## WINDOWS + ONEDRIVE FEASIBILITY + DEPENDENCY WEIGHT

**Green across the board — even lighter than `dm-triage`, because it adds *zero* new I/O surface:**

- **No torch / cv2 / transformers / cloud / paid SaaS.** The "qualifier" is Claude reasoning in-session (the `comment-triage` / auto-clip `--provider agent` pattern). No model download, nothing off the synced disk.
- **No new server, no new MCP, no new secret.** Reuses `dm-triage`'s `instagram` MCP calls (`get_conversations`/`get_conversation_messages`/`send_dm`) and `INSTAGRAM_ACCESS_TOKEN`. (Rule 3 safe.)
- **Lead store = a vault note**, not a database. Tiny markdown, no sync thrash. **Must obey the vault property contract** (`obsidian/Elijah's vault/CLAUDE.md`): use an existing `type` and copy `_templates/` verbatim — do **not** invent a `lead` type or new properties without Elijah's say-so. Safest v1: write to `20-Content/Ideas/` or a per-lead note under `40-Projects/Archetype-Index/` using the existing `idea`/`task` template, with the qualification detail in the BODY, not new YAML keys.
- **OneDrive:** only artifacts are the skill `SKILL.md` text, the lead vault notes, and `team/memory.md` log lines. All tiny.

The **only** real dependency is inherited, not new: `dm-triage` Phase 0 (Meta-app messaging config + one live send) must clear. This candidate adds no dependency of its own.

---

## HOW IT COMPOSES WITH THE HUB (integration sketch)

**Shape: extend the (planned) `dm-triage` skill — do NOT make a separate skill.** Folding routing into `dm-triage` keeps one DM loop, one window-logic implementation, one review table.

```
inbound DMs                                            Elijah
   │ instagram MCP                                       │ per-item OK
   ▼                                                     ▼
get_conversations ─► get_conversation_messages ─► [classify FAQ/lead/spam/needs-human]
   (poll, daily/on-demand)                                  │
                                                            ▼ (lead bucket only)
                                              [QUALIFY: intent · fit · stage · next-action]
                                                            │  team/profile.md (voice + offer)
                                                            │  Archetype-Index FAQ/offer KB
                                                            ▼
                                       [draft in-thread routing reply]  +  [draft vault lead note]
                                                            │                       │
                                                            ▼ on explicit OK        ▼ on explicit OK
                                                         send_dm            write idea/task note
                                                            │              (vault property contract)
                                                            └────────► team/memory.md (approve/edit/reject loop)
```

- **Engine/skill:** the `.claude/skills/dm-triage/SKILL.md` planned in `manychat-alt-dm-responder` — add (a) the qualification rubric for the `lead` bucket, (b) the in-thread routing-draft step, (c) the optional vault lead-note write. No new skill folder.
- **MCP:** `instagram` (`get_conversations`, `get_conversation_messages` read; `send_dm` write, confirmation-gated). Vault writes via the Obsidian MCP or direct file write, **template-conformant**.
- **Knowledge base:** a small **Archetype-Index offer/FAQ KB** (what the Index is, who it's for, price, the canonical link, common objections) so routing replies are accurate. One markdown file; can be the same shared FAQ KB `dm-triage` reads, with an Archetype section.
- **Data shapes:**
  - Inherited: `get_conversations` → `[{id, participants[{id: IGSID}], updated_time}]`; `get_conversation_messages(id)` → `[{from{id}, message, created_time}]`; `send_dm(recipient_id=IGSID, message)`.
  - New in-session record: `{ conversation_id, igsid, intent: low|med|high, fit: archetype|generic|none, stage: cold|warm|price_link, next_action: answer|route|handoff, draft_reply, log_as_lead: bool, within_24h: bool }`.
  - Vault lead note: existing `idea`/`task` template; lead context (handle, what they asked, qualification, suggested next step, link to the IG thread) in the BODY.
- **Context system:** `team/profile.md` (voice + the Archetype offer), `team/memory.md` (which routings converted / were edited / rejected — the learning loop that improves the rubric).
- **Scheduling:** optional later — the same morning poll `dm-triage` proposes ("N DMs waiting, M leads detected, K inside 24h"). **Queue-only, never auto-send, never auto-route.**

---

## PHASED BUILD SKETCH

### Phase 0 — INHERITED GATE (not new work): `dm-triage` Phase 0 must clear first
- The single live human-approved DM send (`manychat-alt-dm-responder` Phase 0): Elijah enables the messaging product + `messages` webhook on the `mybrain` app, then one approved `send_dm` lands in the 24h window. **Until this succeeds, there is nothing to route on — do not start the routing layer.**
- **Exit:** one DM successfully sent → `dm-triage` Phase 1 becomes buildable → this layer becomes buildable.

### Phase 1 — Qualification + in-thread routing draft (smallest safe thing) — **S, no new deps**
- In `dm-triage`, extend the `lead` bucket: add the intent/fit/stage/next-action rubric (Claude-as-qualifier, no model).
- Draft the **in-thread routing reply** in Elijah's voice from the Archetype-Index offer/FAQ KB. Include the Index link **only** when stage = warm/price_link and fit = archetype — never as an opener.
- Surface qualification + draft in the existing review table. **Nothing sent.**
- **Exit:** Elijah runs "triage my DMs," sees lead threads scored with a drafted routing reply, approves a couple, they send within the 24h window.

### Phase 2 — Vault lead capture (the "don't lose the lead" job the VA did) — **S**
- On approval, write a **template-conformant** vault lead note (existing `idea`/`task` type; qualification in the body; `[[wikilink]]` to `Archetype-Index`). De-dupe by IGSID/handle so re-runs don't duplicate a lead.
- Optional: a tiny rollup ("open leads this week, by stage") for Elijah/Tanner — read from the vault, not a new store.
- **Exit:** every approved lead becomes a tracked vault note; no prospect silently drops.

### Phase 3 — ADD-LATER ergonomics + (much later) real scoring
- Volume ergonomics: batch the lead review, pace sends, the morning queue-only poll.
- **Only if a labeled lead→close history accumulates:** revisit data-driven scoring (the supervised-model pattern) instead of pure LLM qualification. Not before — there's no dataset today, and at his volume the LLM-semantic approach is the right tool.
- Beyond-24h routing inherits `dm-triage` Phase 3's `human_agent`-tag gate (App Review + Business Verification) — same Elijah-gated decision, not part of this layer.

---

## RISKS / ToS / BAN RISK

- **COLD-DM = the headline ban risk, and it's specific to *routing*.** 2026 Meta rules: you may only message someone who messaged/commented/replied first; **sending the first message, or pushing a sales link to a non-engager, triggers restrictions/bans.** "Routing a lead" must therefore mean **a drafted reply inside a conversation the prospect started**, inside the 24h window — never an outbound prospecting blast. Bake this into the skill as a hard rule: the routing draft is only ever a *reply*.
- **Standing Rule 1 (never auto-send/auto-route):** the whole design is draft→approve→send + draft→approve→write-note, per-item OK. A scheduled poll queues only. This is load-bearing — copy it verbatim from `comment-triage`/`dm-triage`.
- **Over-selling / spam integrity:** routing every faint question to a sales link on a 100k account reads as spammy and trips behavioral spam heuristics even with approval. Mitigation: qualify honestly — most leads get an *answer* first and a route only when fit+stage warrant it; vary drafts (real per-thread context, merge fields); pace sends. The 2026 guidance to **disclose AI assistance** is worth honoring where natural.
- **Wrong-voice / wrong-offer to a real prospect:** a mis-qualified or off-message routing reply to a genuine buyer is worse than a slow human reply. Mitigation: high-value or ambiguous leads → `needs-human` (no draft), handed to Elijah/Tanner to close personally. Same rule as comments/DMs.
- **24h-window violation:** routing reply outside the window without the `human_agent` tag → API error / integrity flag. Mitigation: the inherited `within_24h` flag gates the send; closed-window leads are surfaced for in-app manual reply, not API send.
- **Vault contract violation:** inventing a `lead` type or new YAML properties breaks the property contract (vault CLAUDE.md). Mitigation: reuse an existing template, keep qualification detail in the note BODY, get Elijah's OK before any schema change.
- **PII handling:** lead notes may contain a follower's handle / stated details. They live only in the local OneDrive-synced vault (no third party), and **no token/secret ever goes in a file** (Rule 3). Don't paste a prospect's private message verbatim beyond what's needed to act.
- **No paid-SaaS / scraper risk:** official Graph API + official MCP only. No Manychat/Inrō/scraping, no ToS gray area on access.

---

## HONEST BOTTOM LINE

This is a **small, high-leverage follow-on, not a new project** — one qualification bucket + an in-thread routing draft + a vault lead note, all bolted onto the `dm-triage` skill that `manychat-alt-dm-responder` already specs. It turns DM triage (cost-saving) into lead routing (revenue) — the exact "VA routes archetype clients to the index" job from the vault, minus the VA. It adds **zero new dependencies** beyond the inherited DM gate, is OneDrive-safe, and reuses the proven human-in-the-loop loop. The verdict is **ADD-LATER** purely because it is gated on `dm-triage` Phase 0 (one Elijah-actioned live DM send); the instant that send succeeds, this is a ~½-day build. **Do not adopt any DM SaaS (all auto-send) or any OSS CRM (DB-heavy, OneDrive-hostile) — the vault is already his CRM and Claude is already the qualifier.** The one rule that must not be missed: **routing is a reply, never a cold outbound** — get that wrong and it's a ban risk; get it right and it's pure upside.

---

## SOURCES

- [7 Best ManyChat Alternatives in 2026 — SetSmart](https://setsmart.io/blog/manychat-alternative) (GPT-powered lead qualification + appointment booking for coaches/creators; "real conversations not pre-built flows")
- [ManyChat Alternatives for Instagram DM Automation (2026) — Inrō](https://www.inro.social/blog/manychat-competitors-alternatives-2026) (Inrō "AI Agent qualifies leads, captures contact data mid-conversation, and routes by intent"; respond.io = human handoff/routing at $79/mo; pricing for each)
- [Best ManyChat Alternative for Instagram DM Automation (2026) — FlowGent](https://flowgent.ai/manychat-alternative) (real-AI DM handling: qualify leads, book appointments)
- [How To Build A Proper Lead Scoring Agent — Rani Urbis, Medium (Mar 2026)](https://medium.com/@raniurbis/how-to-build-a-proper-lead-scoring-agent-2f083d2d56e3) (LLMs unreliable as scorers over large structured data → use supervised model trained on closed deals; LLM is the explanation/ranking layer — argues *against* pure-LLM scoring at scale, which is why Claude-qualifier fits Elijah's *small unstructured* regime instead)
- [LLM Lead Conversion-Propensity Scoring — Vadim's blog](https://vadim.blog/llm-lead-conversion-propensity-scoring-for-b2b-lead-prioritization) ("LLM semantic understanding dramatically outstrips keyword-based intent detection" — context/urgency/sentiment from unstructured text)
- [Instagram DM Automation Policy in 2026: What Is Allowed and What Gets Banned — AppBrewers](https://appbrewers.com/blog/instagram-dm-automation-policy-2026) (only reply to user-initiated triggers; cold DMs to non-engagers → bans; ≤200 automated DMs/hr; 24h window)
- [Instagram DM Compliance 2026: Meta's Allowed vs Banned — CreatorFlow](https://creatorflow.so/blog/instagram-dm-compliance-meta-rules/) (allowed vs banned actions; disclose AI assistance)
- [Instagram Auto Reply: How It Works, What's Allowed & Best Practices 2026 — InstantDM](https://instantdm.com/blog/instagram-auto-reply-how-it-works-whats-allowed-best-practices-2026) (comment→DM lead-magnet keyword flow mechanics; you cannot send the first message)
- [Best Open Source CRM Software for 2026 — CRM.org](https://crm.org/crmland/open-source-crm) and [Top 20 Open-Source Self-Hosted CRMs 2026 — GrowCRM](https://growcrm.io/2026/01/04/top-20-open-source-self-hosted-crms-in-2025/) (SuiteCRM/Twenty/X2CRM/Frappe all need MySQL/Postgres + server; no good JSON/DB-free single-user option → "custom development" — i.e., use the vault)
- Internal: `docs/plans/2026-06-14-manychat-alt-dm-responder-research.md` (the `dm-triage` skill + DM access findings this builds on), `.claude/skills/comment-triage/SKILL.md` (the draft→approve→send pattern + four-bucket classifier reused), `obsidian/Elijah's vault/40-Projects/Archetype-Index/To do.md` ("route potential archetype clients to the index"), `obsidian/Elijah's vault/CLAUDE.md` (property contract the lead notes must obey)
</content>
</invoke>
