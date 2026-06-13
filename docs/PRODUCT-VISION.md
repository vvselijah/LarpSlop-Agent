# PRODUCT VISION — from local dashboard to a real creator-analytics product

*Started 2026-06-13. Living strategy doc. The competitive/architecture detail will be
appended when the two background research runs land (IDs at the bottom). Specific build
phases each get their own `docs/plans/<date>-<slug>.md` per the dev-workflow.*

## The thesis (Elijah's, sharpened)

Meta Business Suite and the Instagram Professional Dashboard are genuinely bad analytics
UX — shallow, slow, ~90-day memory, awful on mobile and desktop. Meta's official Ads MCP
+ Instagram Graph API matured recently and **most creators don't know how to use them.**
We already have a working engine that beats the native experience on depth. If we structure
it right — **open-source core for trust + a hosted app for non-technical creators** — it's a
real product. The differentiators we believe in: *find your most-viral posts and reverse-engineer
why they worked, mine the comments for what people actually want, and turn that into a content
strategy* — none of the incumbents nail this.

## What we already have (the unfair head start)

- `ig-dashboard/` — Python Graph-API sync engine (`refresh.py`) + self-contained HTML dashboard
  over 300 posts, daily history accrual past Meta's 30-day window, token auto-expiry, offline Chart.js.
- `intel/` — competitor radar (others' reels WITH view counts, official API) + virality trend radar
  (Wikipedia + GDELT + Hacker News, keyless).
- `team/` context system + `weekly-content-plan` / `niche-intel` skills (the "what to make next" layer).
- A working, scoped Instagram token and the Meta Ads MCP. This is already 80% of a v1 backend.

## GROUNDED FEASIBILITY — what the API actually allows (live-tested 2026-06-13)

Token `@elijahaifl` granted scopes (verified via `/debug_token`): `instagram_basic,
instagram_manage_comments, instagram_manage_insights, instagram_content_publish,
instagram_manage_messages, instagram_manage_contents, instagram_manage_engagement,
instagram_branded_content_brand, pages_show_list, pages_read_engagement, business_management`.

| Capability | Status (live-tested) | Note |
|---|---|---|
| Read media + insights (own) | ✅ works | the dashboard's foundation |
| Read **comments** on own posts | ✅ **works today** (live-verified) | `instagram_manage_comments` is an approved capability |
| Reply to / hide comments | ✅ scope granted (write — gate behind confirmation) | not yet tested; same capability |
| Competitor `business_discovery` | ✅ works | views/likes/comments on any public Business acct |
| **DM conversations (read OR send)** | ❌ **BLOCKED** | endpoint returns error **#3 "Application does not have the capability to make this API call"** — the **app `mybrain` has not passed Meta App Review for messaging**, even though the token has `instagram_manage_messages`. Granting the scope ≠ the app having the approved capability. |

### DM messaging rules — confirmed from Meta's primary docs (2026-06-13)
- **Reply-to-inbound only:** the API can send a DM to a user *only after that user has messaged
  the account first.* No proactive/unsolicited outbound. (Fine — the use case IS replying to incoming.)
- **24-hour window:** you have 24h to respond to a user's message via the API.
- **Human-agent tag:** a human-agent response can be tagged to reply *outside* the 24h window
  (commonly up to 7 days) — this is exactly what legitimizes the approval-queue architecture.
- **Permissions:** read = `instagram_manage_messages`; send (IG-login config) =
  `instagram_business_basic` + `instagram_business_manage_messages`.
- (App-Review/dev-mode-tester-limit specifics were rate-limited mid-verification — re-confirm when building.)

### What this means for the 3,000–5,000 DMs/month problem
- **DMs cannot be touched today** through the official API. The blocker is **Meta App Review
  for the messaging capability** (requires a business use-case submission + Business Verification;
  a personal dev app may struggle to get it). The running DM research (ID below) is mapping the
  exact path, the policy windows (24h standard / 7-day human-agent tag), and what's compliant.
- **Comments are the win available NOW.** A large share of "how do I get put on" / questions
  arrives as comments, which we CAN read and reply to today. **Highest-leverage near-term build:
  an AI comment-triage + draft-reply workflow** (categorize → draft in Elijah's voice → human
  approves → API replies), under the standing never-send-without-confirmation rule. This delivers
  most of the "respond to people at scale without a VA" value before the DM gate is cleared.
- When/if messaging App Review is approved, the SAME approval-gated architecture (triage → draft →
  approve-queue → send) extends from comments to DMs with the 24h/7-day window handling.

## Product direction (to be finalized with the research)

- **Open-core**: open-source the engine + Graph-API plumbing + dashboard (trust, distribution,
  "the tool that finally makes IG analytics good"); gate the hosted multi-account version, the AI
  strategist, comment-AI, and alerts. (PostHog / Plausible / Cal.com pattern — the running product
  research is validating this.)
- **Path**: local-first OSS (BYO-token, like today) → hosted app (needs Meta App Review + business
  verification + per-user OAuth). Ship OSS-local first; it needs no review and builds the audience.

## OPEN — answered by the two background research runs (resume from these)

1. **DM feasibility + compliant architecture** — run `wf_a74e9756-f2b` (task `wz1zamux1`).
2. **Product strategy / OSS-vs-app / competitive gaps / architecture** — run `wf_5ddc3f07-8ec` (task `wu6ij7zga`).

When they land: append their synthesis here, then write `docs/plans/` PLAN docs for (a) the
comment-triage workflow [buildable now] and (b) the dashboard v2 / OSS-repo extraction.

## Immediate next steps (for the next session)

1. Read the two research outputs (they'll arrive as task-notifications).
2. PLAN + build the **comment-triage/draft skill** — works today, highest near-term value.
3. PLAN the **dashboard v2 + OSS extraction** (what's open vs gated) from the product research.
4. Flag the **Meta App Review for messaging** as an Elijah action (it has lead time) once the
   research confirms the exact submission requirements.
