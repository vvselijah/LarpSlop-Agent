---
name: comment-triage
description: Triage incoming Instagram comments and DRAFT on-brand replies (plus reversible hide actions for spam) for Elijah's one-click approval, then reply only on his explicit per-item OK — never auto-send. Use when he says "triage my comments", "draft comment replies", "answer my comments", "deal with the spam in my comments", "clear the comment queue", or "what should I reply to". Enforces the comment-only DRAFT→approve→reply workflow documented in docs/PRODUCT-VISION.md.
---

# Comment Triage And Draft-Reply Workflow

Pull recent Instagram comments, classify them, draft replies in Elijah's voice, and present
them for his approval — nothing leaves draft state without his explicit per-item click.
Why comments and not DMs, and what the API actually allows: `docs/PRODUCT-VISION.md`.

## Steps (workspace root: `C:\Users\elija\OneDrive\Desktop\ai agent team`)

1. **Pin the workspace.** All paths below are relative to
   `C:\Users\elija\OneDrive\Desktop\ai agent team`. Read `team/profile.md` (voice + niches)
   and the newest entries in `team/memory.md` (past approve/edit/reject outcomes — the
   knowledge-base loop) before drafting anything.
2. **Pull the queue.** Use the `instagram` MCP: `get_media_posts` to pick recent posts, then
   `get_comments` per post to read incoming comments. Read-only so far — no writes yet. This
   works today on his owned account under the `instagram_business_manage_comments` permission.
3. **Classify each comment** into exactly one bucket: **FAQ** (a known repeatable question),
   **lead** (real interest / "how do I get put on" / business inquiry), **spam** (bots, drop
   links, scams, repeated junk), or **needs-human** (nuanced, emotional, faith-sensitive, or
   anything you're unsure about — never guess on these; flag for Elijah to handle himself).
4. **Draft the action** per bucket:
   - FAQ / lead → draft a `reply_to_comment` text in Elijah's voice using the FAQ knowledge
     base (templates with merge fields like `{first_name}`); high-energy, plain-spoken, direct
     "you", faith natural-not-preachy (per `team/profile.md`).
   - spam / abuse → draft a `hide_comment` (REVERSIBLE — unhide is available). Never draft a
     delete; `delete_comment` is IRREVERSIBLE and only valid on his own comments anyway.
   - needs-human → no draft; surface it with a one-line "why" so Elijah can answer directly.
5. **Present the review table** — columns: comment text + author, classification, proposed
   action (reply / hide / hand-off), and the full draft. One row per item. State clearly that
   nothing has been sent.
6. **Act ONLY on explicit per-item approval.** For each item Elijah OKs by hand, call
   `reply_to_comment` (FAQ/lead) or `hide_comment` (spam). Skip every item he doesn't approve.
   Stay well under the limits (~750 private comment-replies/hr, ~2 calls/sec) — pace, don't
   blast; there is no reason to rush a batch.
7. **Close the loop.** Log this run's outcomes (which drafts were approved, edited, or
   rejected, and any edit text) back to `team/memory.md` so the FAQ knowledge base and voice
   improve over time. Append one dated learning, newest-first (CLAUDE.md rule 7).

## Rules

- **Never send a reply, hide, or any write without Elijah's explicit per-item confirmation.**
  Drafting and presenting are fine; the final click is his (CLAUDE.md rule 1). This is a
  comment-only workflow.
- **Spam = draft a HIDE (reversible), never auto-delete.** Hide/unhide is recoverable;
  `delete_comment` is irreversible and only applies to his own comments — do not use it for
  moderation.
- **No secrets in files.** The `instagram` MCP reads its token from Windows env vars
  (`INSTAGRAM_ACCESS_TOKEN`); never write tokens, IDs, or credentials into any file — this
  tree syncs to OneDrive (CLAUDE.md rule 3).
- **DMs are out of scope for v1.** `send_dm` only works inside the 24-hour window the user
  opens by messaging first; outside it, sends fail, and acting on real (non-app-role)
  followers at scale needs Advanced Access via Meta App Review (error `#3` = Standard Access
  only). DM auto-reply is a separate gated track — see `docs/PRODUCT-VISION.md`; don't attempt it here.
- **When unsure, hand it to Elijah.** Anything emotional, faith-sensitive, or ambiguous goes
  to the needs-human bucket — never draft a guess on his behalf.
