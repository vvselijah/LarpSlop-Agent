# IG Dashboard — @elijahaifl Content Command Center

**To use: double-click `Open Dashboard.bat`.** It pulls everything new since last
open (new posts, updated engagement on recent posts, daily account metrics),
then opens the dashboard in your browser.

## What's inside

- **Overview** — KPI cards with vs-prior-period deltas, daily reach / profile
  visits / bio-link taps, the reach→profile→link funnel, post timeline,
  follower growth.
- **Posts** — all 300 tracked posts; sort by any metric, filter by category /
  format / time range, search captions, click a row for the full stat breakdown.
- **Strategy** — category performance, posts-vs-results bubbles (find
  undersupplied winners), best day/hour heatmap, views-vs-ER scatter,
  top/bottom 10, most-saved, most-shared.
- **Compare** — any time period + category vs any other, with a verdict.

## How data flows

- `refresh.py` syncs from the Instagram Graph API into `data/store.json`,
  then writes `data/data.js` for the dashboard. Old posts' insights are cached;
  posts younger than 14 days are re-fetched (their numbers still move).
- A Windows scheduled task ("IG Dashboard Daily Refresh", 7:00 AM daily) keeps
  daily history accruing even if you don't open it — Meta only serves ~30 days
  of account metrics, but the dashboard never forgets what it has seen.
- `python refresh.py --full` re-pulls insights for ALL posts (run monthly-ish).

## Token

Reads `INSTAGRAM_ACCESS_TOKEN` from Windows env vars (never stored in this
folder — it's OneDrive-synced). Current token expires **2026-08-10**; the
dashboard shows a warning banner when it's close. Renewal: HANDOFF.md §4.

## Tweaks

- Post categories: keyword rules at the top of `refresh.py` (`CATEGORIES`).
- Tracked post count: `POST_LIMIT` in `refresh.py`.
- Re-fetch window for fresh posts: `REFETCH_DAYS`.
