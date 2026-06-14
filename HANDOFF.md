# AI AGENT TEAM — MASTER HANDOFF

**Owner:** Elijah Sullivan (FB id `1718785869259383`, IG `@elijahaifl` ≈ 99.7k followers)
**Collaborator:** Tanner Carlson (co-founder on multiple ventures)
**Workspace:** `C:\Users\elija\OneDrive\Desktop\ai agent team` (Windows 11, user `elija`)
**Vault:** `…\ai agent team\obsidian\Elijah's vault`
**Prereqs present on the old machine:** Python 3.12.10 ✓ · Node v22.16 + npx ✓ · uv/uvx ✓ · Git-Bash curl ✓ · `claude` is the **desktop app** (not on PATH).

> ⚠ **This whole tree is inside OneDrive (cloud-synced). NEVER put secrets in files — use `setx` (Windows env vars).**
> **New session: read this file first, then the workspace `CLAUDE.md`, then the vault's `CLAUDE.md`.**
> ⏩ **LATEST VERIFIED SNAPSHOT (2026-06-13): `SESSION-COMPACT-2026-06-13.md` (repo root)** — read it before this file; it audits actual state (auto-clip "brain" done + committed `7e0b9a5`, unpushed) and supersedes the long baton `docs/plans/2026-06-13-SESSION-HANDOFF.md`.

---

## 0. What this is — and current status

A single Claude Code hub that consolidates Elijah's content, analytics, ads, competitive
intelligence, and business ops. Everything below is **built and working** as of 2026-06-12.

| Subsystem | What it does | Status |
|---|---|---|
| **Meta Ads MCP** | official connector, ad acct `661339332628311` (USD) | ✅ connected |
| **Instagram MCP** | mcpware, `@elijahaifl` insights/comments/publish/DMs | ✅ connected (token → **~2026-08-11**) |
| **`team/`** | file-based context: profile / stats (auto-fed) / memory | ✅ live |
| **`ig-dashboard/`** | own-account analytics over 300 posts, daily 7 AM refresh | ✅ live |
| **`intel/`** | competitor radar + virality trend radar (free, keyless) | ✅ live |
| **Obsidian vault** | structured second brain, 15 templates / 14 Bases | ✅ built, frontmatter retrofit done |
| **Skills** | `weekly-content-plan`, `niche-intel`, `dev-workflow`, `context-checkpoint` (+ video suite) | ✅ live |
| **Working method** | Tanner's `tworkflow` in `docs/` — 40% context rule (hook in `.claude/settings.json`) + dev loop for code | ✅ integrated 2026-06-12 |
| **Research docs** | `AGENT-TEAM-BLUEPRINT.md`, `CONTENT-INTEL-PROTOCOL.md` | ✅ done |

There is no half-finished work blocking anything. Open items are **enhancements + Elijah-actions**, all in §6.

---

## 1. ⭐ BRING-UP CHECKLIST FOR A NEW ENVIRONMENT

Do these in order on the new machine. ~20–30 min.

1. **Place the folder.** Put the `ai agent team` tree at a path and update any absolute
   paths if it differs from `C:\Users\elija\OneDrive\Desktop\ai agent team`. Absolute paths
   live in: the scheduled task, `ig-dashboard/refresh.py` is path-relative (fine), `intel/*.py`
   are path-relative (fine). **Recommendation:** if the new env is for heavy git/code work,
   put it OUTSIDE OneDrive (e.g. `C:\dev\`) to avoid sync churn; OneDrive is fine for this docs/data hub.
2. **Install prereqs:** Python 3.12+, Node 20+ (for `npx`), `uv` (for `uvx` — elevenlabs MCP),
   and ensure `curl.exe` exists (ships with Windows 10+). Confirm `python`, `npx`, `uvx` on PATH.
3. **Set the secrets via `setx`** (see §3 table). The two that MUST be set for the core to work:
   ```
   setx INSTAGRAM_ACCESS_TOKEN "<EAA… token>"
   setx INSTAGRAM_ACCOUNT_ID  "17841400159953101"
   ```
   Then set whichever optional API keys you want the media MCPs to actually authenticate with
   (GEMINI/ELEVENLABS/FAL — see the ⚠ in §3; they are currently **unset**).
4. **MCP servers** load from the two `.mcp.json` files already in the tree (workspace + vault) —
   no action needed beyond having the env vars set, EXCEPT: **app-level connectors are NOT in these
   files** (Meta Ads, Higgsfield, computer-use, Claude-in-Chrome, scheduled-tasks, etc. are added
   through the Claude Code desktop app's connector UI / OAuth). Re-add those in the new app install:
   for **Meta Ads**, just ask *"list my Meta ad accounts"* → complete the browser OAuth.
5. **Recreate the daily refresh task** (Windows Task Scheduler):
   - Program: the new machine's `python.exe` · Argument: `"…\ig-dashboard\refresh.py"`
   - Trigger: daily 7:00 AM · ✔ **"Run task as soon as possible after a scheduled start is missed"**
     ✔ ideally **"Run whether user is logged on or not."** (The old task lacked these — see §6 P1.)
6. **Restart Claude Code** (env vars only load on a fresh start), then run the verification in §1a.

### 1a. Verification (run after bring-up)
- `INSTAGRAM_ACCESS_TOKEN` / `INSTAGRAM_ACCOUNT_ID` set? → `[Environment]::GetEnvironmentVariable('INSTAGRAM_ACCOUNT_ID','User')`
- Meta Ads: ask *"list my Meta ad accounts"* → expect acct `661339332628311`.
- Instagram: `validate_access_token` / `get_profile_info` → expect `@elijahaifl`.
- Dashboard: `python ig-dashboard/refresh.py` → `refresh complete` + fresh `team/stats.md`.
- Intel: `python intel/competitor-radar.py` and `python intel/trend-radar.py` → reports written.

---

## 2. SYSTEM MAP

```
ai agent team/
├─ CLAUDE.md ................ auto-loads every session; rules + capability map + routing
├─ HANDOFF.md .............. this file (ops state + bring-up)
├─ AGENT-TEAM-BLUEPRINT.md . researched tool roadmap (what to add / skip; don't re-litigate)
├─ CONTENT-INTEL-PROTOCOL.md  competitive-intel + virality strategy (3 deep-research runs)
├─ team/ ................... THE CONTEXT BRAIN — read before any planning
│   ├─ profile.md .......... who Elijah is, voice, ventures (HE edits this)
│   ├─ stats.md ........... live IG numbers, auto-rewritten daily by refresh.py (don't hand-edit)
│   └─ memory.md .......... dated learnings, newest first (agents append after planning runs)
├─ ig-dashboard/ ........... own-account analytics
│   ├─ refresh.py ......... sync engine (token from env; /debug_token auto-expiry; writes stats.md)
│   ├─ dashboard.html ..... local UI (Chart.js vendored at vendor/ for offline)
│   ├─ Open Dashboard.bat . refresh + open
│   └─ data/ ............. store.json (full state) · data.js · refresh.log
├─ intel/ ................. COMPETITIVE INTEL + VIRALITY RADAR (free, keyless)
│   ├─ competitor-radar.py  competitor reels WITH view counts via business_discovery (no scraping)
│   ├─ watchlist.json ..... niche → IG usernames (HE edits; verified handles seeded)
│   ├─ trend-radar.py ..... virality early-warning: Wikipedia + GDELT + Hacker News
│   ├─ trend-watchlist.json  niche → entities/terms/keywords (HE edits)
│   └─ data/ ............. competitors.json · trend-history.json (persistence needs ≥2 days)
├─ obsidian/Elijah's vault/  structured second brain — OWN CLAUDE.md is law (property contract)
├─ .claude/
│   ├─ skills/ ........... weekly-content-plan · niche-intel · dev-workflow · context-checkpoint (+ video suite)
│   ├─ settings.json ..... portable: the 40%-context hook (UserPromptSubmit → context_hook.py)
│   └─ settings.local.json  personal permission allowlist
├─ docs/ .................. WORKING METHOD (Tanner's tworkflow): workflow/ reference + templates/ (PLAN/REVIEW/QA/SESSION-HANDOFF)
├─ here/ .................. Claude's personal space — read here/about.md, NEVER tidy
└─ archive: fromtheinside/, frames/, tiktok-analysis.md, source.mp4/audio.wav (~119MB, see §6 P2)
```

**Sibling repo:** `..\abc wrap\` — ClipWith.AI video R&D (Remotion edits, the baby-reveal reel,
Derwin Scott podcast edit). Same skills/MCPs wired in both. Before video work, read its
`SESSION-COMPACT-2026-06-12.md` + `CLAUDE.md`. Per the journal: Higgsfield is live (~1,887 credits);
the baby reel is blocked only on Elijah's ultrasound files.

---

## 3. CREDENTIALS & ENV VARS (no secrets in this file)

| Var | Scope | Status (2026-06-12) | Needed for | Where the value lives |
|---|---|---|---|---|
| `INSTAGRAM_ACCESS_TOKEN` | User | ✅ set (len 217) | instagram MCP, dashboard, intel | renew per §4 (expires ~2026-08-11) |
| `INSTAGRAM_ACCOUNT_ID` | User | ✅ set = `17841400159953101` | same | non-secret (it's @elijahaifl's id) |
| `GEMINI_API_KEY` | — | ⚠ **NOT set** any scope | `gemini-video` MCP | Google AI Studio |
| `ELEVENLABS_API_KEY` | — | ⚠ **NOT set** any scope | `elevenlabs` MCP | ElevenLabs dashboard |
| `FAL_KEY` | — | ⚠ **NOT set** any scope | `fal` MCP | fal.ai dashboard |

⚠ **The 3 media-MCP keys are absent at every scope** — those servers will start but fail real API
calls until the keys are supplied. Set them if/when those tools are needed (none are core to the hub).

**Non-secret IDs (safe to keep here):** Meta App `mybrain` ID `4345934765671734` · App Secret is
**not stored locally** (only Meta → App → Settings → Basic → Show; never needed it) · FB user
`1718785869259383` · Ad account `661339332628311` · FB Page "Di$trobaby" `107148982346936` ·
IG business account `17841400159953101`.

---

## 4. CONNECTORS + TOKEN RENEWAL

**Meta Ads** — official MCP `https://mcp.facebook.com/ads` (app-level, browser-OAuth; Meta manages the
token, nothing stored). Scopes: ads_management/ads_read/business_management/pages_show_list. Read freely;
**confirm before any write.** Tools: `mcp__meta-ads__ads_*`. Re-auth = just complete the browser login.
Bonus: `ads_library_search` returns **all active US commercial ads** (not just EU) but **no archive** —
save winning creatives on sight. `ads_get_user_pages` is the escape hatch that surfaced the New-Pages page.

**Instagram** — `npx -y @mcpware/instagram-mcp`, env = `INSTAGRAM_ACCESS_TOKEN` + `INSTAGRAM_ACCOUNT_ID`
+ `INSTAGRAM_API_VERSION=v22.0`. The package reads exactly those two vars (NOT the `*_BUSINESS_*`/app-secret
set the original spec wrongly used). `business_discovery` gives any public Business/Creator account's
views/likes/comments — but NOT their reach/saves/watch-time (owner-token only).

**IG TOKEN RENEWAL (do by ~2026-08-11):**
1. Open this URL in Chrome (already granted → instant redirect to Graph Explorer):
   ```
   https://www.facebook.com/v25.0/dialog/oauth?client_id=4345934765671734&redirect_uri=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2Fcallback&response_type=token&scope=instagram_basic%2Cinstagram_manage_insights%2Cinstagram_manage_comments%2Cinstagram_content_publish%2Cpages_show_list%2Cpages_read_engagement%2Cbusiness_management
   ```
2. Copy Token → paste into https://developers.facebook.com/tools/debug/accesstoken/ → **Extend Access Token** → copy the extended (60-day) token.
3. **Verify it's the live one** (Explorer can show stale): `curl "https://graph.facebook.com/v22.0/me?access_token=<TOK>"` (use Git-Bash curl — PowerShell→graph.facebook.com hangs).
4. `setx INSTAGRAM_ACCESS_TOKEN "<token>"` → restart Claude Code → `validate_access_token`.
   The dashboard needs **no code edit** — `refresh.py` auto-detects the new expiry via `/debug_token`.

**Other project MCPs** (in workspace `.mcp.json`): `lottiefiles`, `video-analyzer`, `ffmpeg` (no keys);
`gemini-video`, `elevenlabs`, `fal` (need the keys in §3); `figma` (http). Vault `.mcp.json` adds
`obsidian` (`mcp-remote http://localhost:22360/sse` — only works while Obsidian is open with its REST plugin).
**App-level connectors** (not in any file; re-add via the desktop app): Meta Ads, Higgsfield, computer-use,
Claude-in-Chrome, scheduled-tasks, TwelveLabs/video-intake.

---

## 5. STANDING RULES (non-negotiable)

1. **Never publish, post, comment, or DM on any platform without explicit per-action confirmation.** Drafts/containers fine; the publish click is Elijah's.
2. **Meta Ads:** read/report freely; confirm before ANY write (create/edit/pause/budget).
3. **Secrets only in `setx`** — never in files (OneDrive-synced).
4. **IG API publishing:** voice-only / original-audio reels only (API reels can't use licensed audio); pre-flight `get_content_publishing_limit`.
5. **Vault:** follow its property contract exactly; never invent property names; `_templates/` is the schema.
6. **`here/`** is Claude's own space — read it, never tidy it.
7. After a planning run/experiment, append one dated learning to `team/memory.md`.

---

## 6. NEXT STEPS — prioritized to-do for the next Claude Code

**P0 — quick wins, no blockers**
- [x] **Wrapper built — `Daily Agent Refresh.bat`** runs all three engines (dashboard + competitor +
      trend) in sequence. **Remaining (Elijah/next-Claude):** repoint the "IG Dashboard Daily Refresh"
      scheduled task from `refresh.py` to this `.bat` so competitor + trend reports refresh every morning.
      Trend persistence needs this daily cadence to start firing STRONG alerts. (I'm permission-gated from
      editing Task Scheduler; one repoint in the task's Action does it.)
- [ ] **Fix the scheduled task's reliability flags** (Elijah, ~2 min in Task Scheduler): enable
      "Run task as soon as possible after a scheduled start is missed" + "Run whether user is logged on
      or not." Without these, missed mornings permanently lose `online_followers` data (API serves ~2 days only).

**P1 — high-value enhancements**
- [ ] **Wikipedia "top-views discovery" feed for `trend-radar.py`** — the current radar only tracks
      *named* entities; pop-culture/news breakouts you didn't name in advance are missed. Add the
      `/metrics/pageviews/top/en.wikipedia.org/all-access/{Y}/{M}/{D}` endpoint to surface day-over-day
      risers from the top-1000. This makes the `pop-culture-events` niche actually work.
- [ ] **Let Elijah tune both watchlists** — `intel/watchlist.json` (his real niche competitors; AI niche
      only has `thejustinwelsh` — needs his actual AI-creator targets, which mostly aren't Business accounts)
      and `intel/trend-watchlist.json` (his specific topics).
- [ ] **Run `niche-intel` after ≥2 days of history** — by then the trend radar has persistence and the
      competitor radar has follower-delta history; the synthesis gets much stronger.

**P2 — Elijah-decisions / optional adds (all researched in the two roadmap docs)**
- [ ] **Metricool MCP** (AGENT-TEAM-BLUEPRINT Tier A) — needs Elijah to create the account (~30 min);
      unlocks TikTok/YouTube scheduling + analytics (TikTok can't be self-published — audited scheduler only).
- [ ] **Bright Data MCP** (5k free credits) — one install covers TikTok/YouTube/non-business-IG scraping
      gaps; **zero risk to the IG token** (vendor infra, no login). Add when a specific gap bites.
- [ ] **Whop MCP** at Kajabi-migration decision; **beehiiv MCP** at newsletter launch; **Foreplay** ($59/mo) if ad-creative testing scales.
- [ ] **Cleanup:** ~119 MB of May-14 TikTok media (`source.mp4`, `audio.wav`, `frames/`, `transcript.txt`,
      `transcribe.py`) is dead OneDrive weight — delete/archive pending Elijah's OK (keep `tiktok-analysis.md`).
- [ ] **Belt-and-braces security:** purge OneDrive version history of `Ai agent team handoff.md` (it held a
      now-redacted, expired short-lived token in an old version).
- [ ] **Supply media-MCP keys** (`GEMINI_API_KEY`/`ELEVENLABS_API_KEY`/`FAL_KEY`) only if those tools are needed.

**Recurring maintenance:** renew the IG token by ~2026-08-11 (§4).

---

## 7. GOTCHAS / LEARNINGS (carry these forward)

- **PowerShell → `graph.facebook.com` hangs.** Use Git-Bash `curl` for Graph reads. The repo's Python
  scripts call `curl.exe` and feed the token via `--config -` (stdin) so it never hits the process argv;
  multi-param Graph URLs need `curl -g` + URL-encoded `fields` (PowerShell otherwise mangles `{}` `()`).
- **Chrome extension dies on `developers.facebook.com`** — `navigate`/`get_page_text` work; `read_page`/`find`/`javascript_tool` hang 300s and kill the service worker. Drive OAuth via the manual URL on `www.facebook.com`, never DOM-tools on that domain.
- **`computer-use` request_access** times out (300s) if nobody's at the screen — don't attempt unattended.
- **Env vars load only on a fresh Claude Code start** (after `setx`).
- **IG hashtag/top-media API is App-Review-gated** (this app lacks it) → that surface needs the Layer-3 scraper (Apify), not the official API. See CONTENT-INTEL-PROTOCOL.
- **Bases syntax** is `property:` (not `column:`) with unquoted view names — correct for Elijah's Obsidian version; do NOT revert.
- **MCP split:** project `.mcp.json` servers vs app-level connectors are configured in different places — the bring-up checklist (§1 step 4) is the reason this matters on a new machine.

---

## 8. ARCHIVE — how Instagram got connected (historical, compressed)

The blocker that ate two early sessions: `GET /me/accounts` returned **empty** across fresh tokens because
Elijah's Page is a **"New Pages Experience"** page the classic flow can't surface — so the FB-login path
couldn't reach the IG Business account. **The break (2026-06-11):** the official Meta Ads MCP (server-side
OAuth, immune to the bug) surfaced the Page id `107148982346936` via `ads_get_user_pages`; a **direct node
read** `GET /107148982346936?fields=instagram_business_account` then returned the IG account id — `/me/accounts`
being empty never blocked direct reads. mcpware was kept (no connector swap needed); only its
`get_account_pages` tool stays broken, which is fine. Token prefixes: `EAA…` = Facebook-Login (what mcpware
uses); `IG…` = Instagram-Login (an abandoned alt path). Full saga is recoverable from `Ai agent team handoff.md`
(the raw 2026-06-11 transcript) and the `here/journal/` entries if ever needed.
