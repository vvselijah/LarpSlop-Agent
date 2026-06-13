# Session Handoff: product-vision + DM/comment feasibility + dashboard-v2 direction

- **Date:** 2026-06-13 (~1:30 AM)
- **Strategy doc:** `docs/PRODUCT-VISION.md` (the main artifact — read it first)
- **Not under git** (no branch/commit; OneDrive-synced workspace)

## Where things stand

Elijah wants to grow the hub's dashboard into a real product (open-source core + hosted app)
that beats Meta Business Suite / the IG Professional Dashboard, with deep analysis (viral-post
reverse-engineering, comment mining, content strategy), AND wants to know if we can handle his
3,000–5,000 DMs/month without hiring a VA.

**Done this session:**
- Confirmed no stuck tasks (the "2 running tasks" counter = harness tracking background shells / MCP servers; nothing hung).
- **Live-tested the messaging/comment feasibility (the key finding):** token has `instagram_manage_messages` scope, BUT DM conversations endpoint returns **error #3 "Application does not have the capability"** → the app `mybrain` needs **Meta App Review for messaging**; scope ≠ capability. **Comments DO work today** (read verified live; reply/hide same granted capability). Full table in `docs/PRODUCT-VISION.md`.
- Wrote `docs/PRODUCT-VISION.md` capturing thesis, head-start, grounded feasibility, OSS/app direction, next steps.
- **Launched 2 background research runs** (still running — will notify):
  - DM automation feasibility + compliant architecture: run `wf_a74e9756-f2b`, task `wz1zamux1`.
  - Product strategy / OSS-vs-app / competitive gaps / architecture: run `wf_5ddc3f07-8ec`, task `wu6ij7zga`.

## Next action (for the fresh session)

1. Read the two research outputs when their task-notifications arrive (or read their `.output` files under `…/tasks/`).
2. Append their synthesis into `docs/PRODUCT-VISION.md`.
3. Write a PLAN (`docs/plans/<date>-comment-triage.md`) and build the **comment-triage/draft skill** — it works on the API TODAY and is the highest near-term value (most "how do I get put on" volume is in comments). Approval-gated: triage → draft in Elijah's voice → human approves → API replies. Never auto-send (standing rule 1).
4. Then PLAN the dashboard-v2 / OSS-repo extraction from the product research.

## Open questions / landmines

- **DMs are gated on Meta App Review for messaging** (business verification + use-case). Likely slow / uncertain for a personal dev app — the DM research run is mapping the exact requirements. Treat as an Elijah action with lead time, NOT a quick unblock.
- Comment **reply** is a write action → per-action confirmation required; don't bulk-send.
- Context was at ~48% (1M window) at handoff — this note exists because the `context-checkpoint` 40% rule (installed this same session) fired. Reseed the new session by pointing it at `docs/PRODUCT-VISION.md` + this handoff.
- The 2 research runs may hit the session compute limit mid-verify (happened earlier today); they're resumable via their run IDs, and they return vote-confirmed claims even if the final synthesis step is skipped.
