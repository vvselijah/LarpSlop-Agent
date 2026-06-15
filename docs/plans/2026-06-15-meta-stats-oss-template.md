# Plan: extract `ig-dashboard/` into an MIT OSS template — 2026-06-15 (Wave 3, id=meta-stats-oss)

> **What this is.** A concrete, ready-to-execute extraction plan for sub-product **A** of the
> `meta-stats-opensource-app` candidate (verdict **ADD-LATER / Phase-0**, per
> `docs/plans/2026-06-14-meta-stats-opensource-app-research.md`), plus **slice B**: a draft of the
> in-vault Obsidian dashboard note that sub-product B would emit.
>
> **This is docs-only — by explicit instruction nothing is extracted, copied, or built tonight.**
> No code moved, no new repo created, no file written inside `obsidian/` (the vault is READ-ONLY).
> Execution stays **gated on Elijah deciding he wants a public repo** (the research's Phase-1 gate).
>
> **Grounding (all read this run):** `ig-dashboard/README.md`, the real `data/data.js` + `data/store.json`
> headers (confirmed to contain live account data), `obsidian/Elijah's vault/CLAUDE.md` (property
> contract), `obsidian/Elijah's vault/_templates/` (the full template set — and the gap it reveals),
> and the prior research doc above.

---

## Slice A — the OSS extraction plan

### A.0 Scope and non-goals (read first)

**In scope (sub-product A only):** de-personalize the three engine files + the single-file viewer into a
public repo a *stranger* can clone and run **on their own Instagram account**, MIT-licensed, with a
README that walks them from "make a Meta app" to "open the dashboard." No App Review needed — each user
runs it on their own account in their app's **Development mode** (research §"Risks").

**Explicitly NOT in scope (do not let scope creep pull these in):**
- **Sub-product C (multi-tenant SaaS)** — OAuth login, hosted server, DB, per-user token vault, Meta App
  Review + Business Verification. That is a separate company, not a hub extraction. SKIP (research verdict).
- **A framework rewrite** (React/Next/DB). The engine's whole virtue is stdlib + `curl.exe` + one HTML
  file. A rewrite destroys the property that makes it shippable and pushes toward C. Keep the stack.
- **Any unofficial-API / scraper "feature parity"** with the IGBlade-based OSS repos. Official-API-only
  is the differentiator and a hub standing rule. Hold the line.

### A.1 Source inventory — what the hub has today (verified this run)

| File | Role | Personalization to strip | Heavy deps |
|---|---|---|---|
| `ig-dashboard/refresh.py` | Graph-API sync → `store.json` + `data.js`; daily history; categories | Hardcoded `ACCOUNT_ID`; Elijah-specific `CATEGORIES` keyword rules; `POST_LIMIT`/`REFETCH_DAYS` defaults | none (stdlib + `curl.exe`) |
| `ig-dashboard/metrics2026.py` | The 2026 scoring contract (skip/share/like/save/repost/comment rates, skip-gate) | none structural — already account-agnostic (ranks against whatever store it's given) | none (stdlib) |
| `ig-dashboard/watchtime_ideator.py` | Watch-time arbitrage ideator | none structural; may echo category names | none (stdlib) |
| `ig-dashboard/dashboard.html` | Single-file viewer (Overview/Posts/Strategy/Compare) | none — reads `data.js`; renders whatever account's data it's handed | none |
| `ig-dashboard/vendor/chart.umd.min.js` | Chart.js (bundled) | **LICENSE AUDIT REQUIRED** before shipping (see A.4) | n/a |
| `ig-dashboard/Open Dashboard.bat` | double-click runner | hardcoded paths likely | none |
| `ig-dashboard/data/*` | `store.json`, `data.js`, `refresh.log`, `watchtime-ideas.md` | **REAL ACCOUNT DATA — MUST NEVER SHIP** | n/a |

**Reuse note:** `metrics2026.py` and `watchtime_ideator.py` are already effectively account-agnostic —
they operate on whatever `store.json` they're handed. The de-personalization work is almost entirely in
`refresh.py` (the one file that hardcodes identity) + the `data/` scrub + docs. That keeps slice A genuinely ~1 day.

### A.2 Target repo structure (`meta-stats-tracker/`, separate public repo)

```
meta-stats-tracker/                 (NEW public repo, MIT — NOT a folder in this hub)
├── refresh.py                      # de-hardcoded: reads IG_ACCOUNT_ID + IG_ACCESS_TOKEN from env
├── metrics2026.py                  # the 2026 scoring contract, unchanged (already generic)
├── watchtime_ideator.py            # watch-time arbitrage, unchanged
├── dashboard.html                  # single-file viewer, unchanged
├── vendor/
│   └── chart.umd.min.js            # ONLY if license audit (A.4) clears it; else CDN <script> + note
├── config.example.json             # categories + POST_LIMIT + REFETCH_DAYS sample (copy to config.json)
├── refresh-token.py                # NEW small helper: long-lived token refresh (the 50–55-day treadmill)
├── .gitignore                      # excludes ALL real data + secrets (see A.3 — this is load-bearing)
├── LICENSE                         # MIT
├── README.md                       # the stranger walkthrough (see A.5)
└── data/
    └── .gitkeep                    # keep the empty dir; everything else in data/ is gitignored
```

**Why `config.json` (gitignored) + `config.example.json` (committed):** today `refresh.py` hardcodes
`ACCOUNT_ID` and bakes Elijah's category keywords inline. For a stranger those must become editable
config. The *example* ships (so people know the shape); the *real* one is gitignored (so no one's account
id or niche leaks). `IG_ACCESS_TOKEN` stays an **env var, never a file** — inheriting the hub's secret rule.

### A.3 `.gitignore` — exactly what must NOT ship (the one non-negotiable section)

The pre-publish data-hygiene chore is the single highest-risk step: `data/data.js` and `data/store.json`
were inspected this run and **both contain live account data** — username `elijahaifl`, real follower
count, full post captions, profile-picture URLs, and IG media IDs. Shipping either would leak Elijah's
account wholesale. The `.gitignore` MUST therefore exclude:

```gitignore
# --- real account data: NEVER COMMIT (this block is the whole point) ---
data/*               # store.json, data.js, refresh.log, watchtime-ideas.md — all real metrics/captions
!data/.gitkeep       # keep the empty directory so a fresh clone has somewhere to write

# --- local config carrying account identity ---
config.json          # contains the user's IG_ACCOUNT_ID + their niche category keywords
*.local.*

# --- secrets (defense in depth — tokens should be env vars, never files, but belt-and-suspenders) ---
.env
*.token
secrets*

# --- runtime / OS noise ---
__pycache__/
*.pyc
*.log
.DS_Store
Thumbs.db
```

**Verification gate before the first `git push` (all must pass):**
1. `git status --porcelain` shows **nothing** under `data/` except `data/.gitkeep`.
2. `git log -p` / `git show` of the *initial* commit contains **no** real username, follower count,
   caption text, media id, profile-picture URL, or access token. (Grep the packed objects, not just the
   working tree — a file added then gitignored still lives in history.)
3. Because history is the trap: **start the public repo from a fresh `git init`**, copying only the
   de-personalized files in — do NOT `git filter-branch` the hub's history (the hub isn't even public yet,
   and a fresh init guarantees zero leaked objects). This sidesteps the "added-then-ignored stays in
   history" footgun entirely.
4. Manual eyeball of `config.example.json` + README screenshots/examples for any real numbers.

### A.4 `vendor/` license audit (blocking pre-publish task)

`vendor/chart.umd.min.js` is a bundled third-party (Chart.js). Before publishing:
- Confirm its license (Chart.js is **MIT** as of current releases — verify the exact bundled version's
  header). MIT is compatible with shipping inside an MIT repo *with attribution*.
- If it clears: keep it vendored and add the upstream license/attribution (NOTICE or a `vendor/README`).
- If any vendored asset is GPL/AGPL or unclear: **do not vendor it** — switch `dashboard.html` to a
  pinned CDN `<script>` tag and document the swap. (Research §"License" flags this as the one thing to
  confirm before MIT-publishing.)

### A.5 README outline (the "bring your own IG token" setup)

```
# Meta Stats Tracker
> A local, official-API Instagram analytics dashboard. No scraper, no paid key, no server.
> Clone it, point it at YOUR account, run one Python file, open one HTML file.

## What you get
- 300-post history, per-post insights with velocity, daily account metrics, follower demographics
- A single-file dashboard (Overview / Posts / Strategy / Compare)
- The 2026 IG-signal scoring contract (skip/share/like/save/repost/comment rates, skip-gated score)
- 100% Python standard library + curl + one HTML file. Runs on Windows/Mac/Linux. No install.

## Why this over the other "IG analytics" repos
- Uses the **official Instagram Graph API** with YOUR consent — not IGBlade (paid 3rd-party) or a
  scraper (ToS-violating, ban-risky). Your data never leaves your machine.

## Prerequisites
- An Instagram **Professional** account (Business or Creator) linked to a Facebook Page.
- Python 3.10+ and `curl` (preinstalled on modern Windows/Mac/Linux).

## Setup (≈15 min, one time)
1. **Create a Meta app** at developers.facebook.com → "Business" type. Keep it in **Development mode**
   (running on your own account needs NO App Review).
2. **Add the Instagram Graph API product**, connect your Professional account + its Page.
3. **Get a long-lived access token** (~60 days). [step-by-step + the exact Graph API Explorer flow]
4. **Find your IG account id** (the `instagram_business_account` id on your Page). [one Graph call shown]
5. **Set two environment variables** (never put the token in a file):
   - `IG_ACCESS_TOKEN` = your long-lived token
   - `IG_ACCOUNT_ID`   = your numeric account id
   (Windows: `setx`. Mac/Linux: export in your shell profile.)
6. `cp config.example.json config.json` and edit your post-category keywords (optional).

## Run
- `python refresh.py`            # pulls your data → data/store.json → data/data.js
- open `dashboard.html`          # double-click; it reads data/data.js
- `python refresh.py --full`     # re-pull ALL posts' insights (run ~monthly)

## Keep it alive: the token treadmill (READ THIS or it dies in 60 days)
Long-lived tokens last ~60 days and DO NOT auto-renew. Run `python refresh-token.py` every 50–55 days
(or automate it). The dashboard shows a warning banner as expiry approaches. [refresh flow explained]

## Automate (optional)
- Windows Task Scheduler / cron snippet to run refresh.py daily. [example]

## Rate limits
- 200 requests/hour per Instagram account — far above one creator's daily refresh. Fine for personal use.

## License
MIT. Chart.js (vendored) is MIT — see vendor/ attribution.

## NOT included / NOT a goal
- Multi-account / multi-user / hosted SaaS (that needs Meta App Review + a server + a DB — out of scope).
- Any scraping or unofficial-API access. Official Graph API only, on your own account, with your consent.
```

### A.6 De-personalization checklist (the actual ~1-day execution, when un-gated)

1. `refresh.py`: `ACCOUNT_ID` → `os.environ["IG_ACCOUNT_ID"]`; `CATEGORIES`/`POST_LIMIT`/`REFETCH_DAYS`
   → loaded from `config.json` with `config.example.json` defaults. (Keep `INSTAGRAM_ACCESS_TOKEN`
   env-var pattern, but rename to the documented `IG_ACCESS_TOKEN`, or accept both for back-compat.)
2. Strip Elijah-specific category keywords out of the committed default into `config.example.json`.
3. Write `refresh-token.py` (the 50–55-day refresh helper the README promises).
4. Add `LICENSE` (MIT), `.gitignore` (A.3), `config.example.json`, `data/.gitkeep`.
5. Run the A.4 vendor license audit; vendor-or-CDN decision.
6. Fresh `git init` in the new repo dir, copy de-personalized files in, run the A.3 verification gate,
   then publish.
7. **(Optional, demand-gated, research Phase 2)** a `--demo` synthetic-data mode so people see the
   dashboard before wiring a token. Only if the repo gets real traction.

### A.7 Honest costs / risks carried from the research

- **Two-copy maintenance tax.** The hub keeps its personalized copy; the public repo is a parallel
  fork-point. Every future hub engine improvement must be *consciously* back-ported or not. Mitigation:
  keep the public repo deliberately minimal; don't back-port hub-specific features.
- **Weak market pull.** The legitimate official-API OSS niche is nearly empty (closest comparable repo:
  4★, last touched 2023). Differentiation is real (official API, no scraper, no paid key) but demand is
  unproven — treat this as a **credibility/content artifact + portfolio piece**, not a revenue bet.
- **The data scrub is the only thing that can actually hurt.** Everything else is reversible; a leaked
  initial commit is not. A.3's fresh-init + grep-history gate is mandatory, not optional.

---

## Slice B — Obsidian dashboard-note draft

### B.0 The blocking finding (must surface before any vault write)

The vault property contract (`obsidian/Elijah's vault/CLAUDE.md` §"The property contract") is explicit:
the canonical property names for a `type` are **defined in `_templates/`**, and *"Do not invent new
property names without explicit permission from Elijah."* `dashboard` is a **listed `type` value** (line
33 of the contract) — **but there is NO `_templates/dashboard.md` file.** The template set is:
daily, hook, post, script, person, sponsor-deal, project, task, decision, meeting, bug, prompt, book,
idea, ad-campaign. **No dashboard template exists.**

**Consequence:** sub-product B cannot define a real `dashboard` frontmatter schema tonight without
**inventing property names**, which the contract forbids. So the draft below is built **only from
properties that already exist in shipped templates** (so it never violates the contract), and the
**actual schema is logged as an explicit Elijah decision**, not guessed. This is the correct,
contract-respecting move — the research doc's Wire-2 assumed a `dashboard` template the vault doesn't
actually carry.

### B.1 What the dashboard note would contain (concept)

A single nightly-refreshed note that mirrors the `team/stats.md` writer pattern (`refresh.py`'s existing
`write_stats_md()` is the exact idiom to clone): top-line `metrics2026` numbers as machine-refreshable
**frontmatter**, a human-readable body, rendered into charts by an existing community plugin (Charts
View / Dataview) — no custom plugin. The body is human-written analysis; only the YAML refreshes (the
vault's standing ingestion rule: *never overwrite the prose body, only update property fields*).

### B.2 Draft note — using ONLY existing/safe properties (placeholder values)

> **Location (proposed):** `20-Content/IG Dashboard.md` (NOT written tonight — draft only).
> Frontmatter uses `type`, `status`, `tags` (all canonical, contract-safe) and intentionally does
> NOT add metric properties, because no `dashboard` template defines their names yet (see B.0/B.3).
> Numbers below are **illustrative placeholders**, not Elijah's real data.

```markdown
---
type: dashboard
status: live
tags: [analytics, ig, metrics2026]
---

# IG Dashboard — @<account>

> Auto-refreshed nightly from `ig-dashboard/` (metrics2026 contract). Body below is human analysis;
> properties refresh automatically. Last refresh: <YYYY-MM-DD HH:MM>.

## 2026 signal snapshot (skip-gated scoring)
| Metric (rate) | Last 30d | Prior 30d | Trend |
|---|---|---|---|
| Skip rate (gate)   | <12.3%> | <14.1%> | ▲ better |
| Share rate         | <2.1%>  | <1.7%>  | ▲ |
| Save rate          | <3.4%>  | <3.6%>  | ▼ |
| Like rate          | <8.9%>  | <8.5%>  | ▲ |
| Comment rate       | <0.9%>  | <1.0%>  | ▼ |
| Repost rate        | <0.4%>  | <0.3%>  | ▲ |
| **metrics2026 score** | **<71>** | **<64>** | ▲ |

## Top posts by 2026 score (last 30d)
1. <caption slug> — score <88>, skip <8%>, share <4.1%>
2. <caption slug> — score <82>, skip <10%>, share <3.0%>
3. <caption slug> — score <79>, skip <11%>, share <2.8%>

## Category breakdown
- <Money>: <n posts>, median score <74>
- <Motivation>: <n posts>, median score <69>
- <AI/Tech>: <n posts>, median score <66>

## Watch-time arbitrage (from watchtime_ideator)
- Highest watch-time, lowest supply: <category> → make more long-form here.

## Notes (human — never overwritten by the refresh)
-
```

### B.3 The one decision this slice needs from Elijah (do not guess it)

To actually emit a `dashboard` note that respects the contract, **one of these must happen first**, and
it is Elijah's call (it touches the vault schema, which is his to define):

1. **Create `_templates/dashboard.md`** with an approved property block (e.g. `type`, `status`,
   `refreshed_at`, and whatever metric fields he wants as properties). Then the writer copies it exactly.
   — *Preferred: it makes `dashboard` a real, first-class type and lets Charts View/Dataview query the
   metric properties.*
2. **Keep metrics in the body only** (tables, as drafted above), with frontmatter limited to the three
   already-canonical properties (`type`, `status`, `tags`). — *No schema change needed; charts come from
   Dataview reading the markdown table or from a `_bases/` query, not from frontmatter.* This is the
   **zero-permission-needed** path and is what the B.2 draft uses.

Until he picks, the safe default is **option 2** (the draft above) — it introduces **no new property
names** and therefore violates nothing. Building the `write_dashboard_note()` engine is a separate
~30-min job (Phase 0 in the research) and is **not done tonight** (docs-only instruction; vault is
read-only).

---

## Status / next step

- **Slice A:** complete, executable extraction plan — gated on Elijah wanting a public repo. The data
  scrub (A.3) and vendor license audit (A.4) are the two blocking pre-publish chores; the fresh-`git
  init` approach is the safe way to guarantee no real data enters history.
- **Slice B:** draft delivered using only contract-safe properties; surfaced the missing
  `_templates/dashboard.md` as the real blocker and framed it as an explicit Elijah decision rather than
  inventing a schema.
- **Nothing was extracted, copied, built, or written into `obsidian/` tonight** — per instruction.
