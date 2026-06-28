# SESSION COMPACT & HANDOFF — 2026-06-16

> **READ FIRST on resume.** Baton for the 2026-06-16 session. Supersedes `SESSION-COMPACT-2026-06-15.md`
> for current state. ✅ done · ⚑ needs Elijah · 🔨 next build. Personal single-user use only ([[project-personal-use-scope]]).

## 1. STATE
Elijah's hub (`C:\Users\elija\OneDrive\Desktop\ai agent team`, IG @elijahaifl). This session was almost
entirely **net-new building**, not pushed to git yet (the bridge lives in `telegram-bridge/`, untracked).
Headline: **built a working Telegram→Claude bridge so Elijah can run the hub from his phone.** It's running
but blocked on Claude billing (see §4). Big late finding: there's a **near-free way to run it on his Claude
subscription** instead of buying API credit (§5).

## 2. WHAT SHIPPED THIS SESSION
- ✅ **Podcast-editor skill packaged for Tanner / ClipWith.AI.** Polished `~/.claude/skills/podcast-interview-editor/`
  (folded the orphaned `playbook-v2.json` into SKILL.md), wrote **`INTEGRATION-FOR-CLIPWITH.md`** (pipeline DAG,
  JSON data contracts, what's hardcoded-to-the-Derwin-shoot to parameterize, deps, golden rules), and zipped the
  whole thing to **`C:\Users\elija\OneDrive\Desktop\podcast-interview-editor-skill.zip`** (82 KB) for Elijah to send.
  ⚑ Offered to also drop it into the `..\abc wrap\` repo — HELD (that repo has leaked keys + is 28 behind; needs his OK).
- ✅ **Answered IG-capability questions** (live-checked the token): trial reels — API supports creation via a
  `trial_params` field (`graduation_strategy: MANUAL|SS_PERFORMANCE`) but there's **no API field to READ whether a
  posted reel is a trial**, and the connected `@mcpware/instagram-mcp` doesn't expose `trial_params` at all.
  Posting works (`publish_reel`/`publish_carousel`, voice-only, per-action confirm). **Saved posts/collections are
  NOT in the Graph API** → his "carousel copy" folder can't be read; workaround = he sends permalinks. `business_discovery`
  = any public account's public data (no private insights). `get_account_pages` shows **only ONE** account under the
  current token: page "Di$trobaby" → IG `17841400159953101`.
- ✅ **Telegram bridge BUILT + RUNNING** — `telegram-bridge/` (bot.py, bridge_settings.json, requirements.txt,
  run-bot.bat, README.md, .gitignore). Bot **@Elijahclaudebot**, whitelisted to Elijah (**TG user id 2008524722**).
  Installed the **Claude Code CLI** (`npm i -g @anthropic-ai/claude-code` → native `bin/claude.exe`) + `python-telegram-bot`.
  Each message → headless `claude -p` with cwd=hub → inherits `.mcp.json`+skills+CLAUDE.md. Golden rule enforced via
  `permissions.deny` (publish/DM/comment/ads-writes blocked). Media in (inbox/) + out (outbox/ + `SEND_FILE:` marker).
  Hardened with a **pidfile self-replace** after a multi-instance 409 debugging saga (see §6).
- ✅ **Memories written:** `project-telegram-bridge`, `project-personal-use-scope` (+ MEMORY.md index lines).

## 3. SECRETS (set via setx, User env vars)
`TELEGRAM_BOT_TOKEN`, `ANTHROPIC_API_KEY`, `BRIDGE_ALLOWED_USER_IDS=2008524722`.
⚑ **ROTATE the Telegram + Anthropic secrets** — both were pasted in chat → in the OneDrive-synced transcript.
(BotFather `/revoke` → new token; console.anthropic.com → roll key.) Going forward, Elijah `setx` secrets himself
and tells me only the VAR NAME. Old **Gemini key** from prior sessions still needs revoking too.

## 4. ⚑ BLOCKER: Claude billing (what stops the bot from actually replying)
Headless `claude -p` is NOT covered by the interactive Pro/Max plan the way the desktop app is. We wired the bot to
use `ANTHROPIC_API_KEY` → its account has **$0 API credit** → every real prompt returns *"Credit balance is too low."*
`/start` `/id` `/help` `/new` work without credit; real answers don't. **Two ways forward — see §5.**
Pricing if he funds the API: **Sonnet 4.6 $3/$15 per 1M** (cache-read $0.30, write $3.75); **Opus 4.8 $5/$25**.
Per simple message ≈ $0.02–0.08 on Sonnet; heavy task $0.10–0.50; the bot prints the exact `$` per message (`BRIDGE_SHOW_COST`).

## 5. 💡 THE (NEAR-)FREE PATH — run the bot on his subscription, no separate API funding
The bot SOFTWARE is already free/open-source (ours is). The only thing that costs money is Claude inference. As of the
**June 15 2026** billing change, **headless `claude -p` draws on a monthly headless credit pool INCLUDED with a
Pro/Max subscription — $20 (Pro) / $100 (Max 5x) / $200 (Max 20x), no API key required.** Interactive use is unaffected.
Sources: [techtimes](https://www.techtimes.com/articles/317625/20260602/anthropic-ends-subscription-subsidy-agents-june-15-credit-pool-replaces-flat-rate-access.htm), [tygartmedia](https://tygartmedia.com/claude-code-billing-credit-pool-2026/).
- **To switch the bot to this path:** (1) run **`claude /login`** ONCE in a normal terminal on the npm CLI (its login is
  SEPARATE from the desktop app's); (2) make the bot's process **NOT set `ANTHROPIC_API_KEY`** — currently `run_claude()`
  injects it; change to `env.pop("ANTHROPIC_API_KEY", None)` (and don't pass it in run-bot.bat). Don't use `--bare` (it skips the keychain/subscription read).
- **CAVEATS (be honest):** (a) capped at that monthly pool, then it stops or spills to paid credits; light personal use
  likely fits in Pro's $20. (b) The June-15 change was reported as possibly **paused/in flux** ([digitalapplied](https://www.digitalapplied.com/blog/anthropic-claude-credit-overhaul-june-15-2026)) — verify current behavior. (c) one claude-code-guide pass read older policy as "headless-on-subscription discouraged," but the current credit-pool model is the official mechanism — confirm on his account.
- **Net:** likely no need to prepay API at all for personal use — switch to subscription auth and watch the headless-credit usage.

## 6. GOTCHAS (hard-won — don't relearn) — full detail in [[project-telegram-bridge]]
- Bot runs as **`python3.12.exe`** (the WindowsApps `python` alias's real interpreter), and its `Win32_Process.CommandLine`
  is **null** (Store-app isolation). Find/kill by **Name=`python3.12.exe` + ExecutablePath under `…WindowsApps\PythonSoftwareFoundation.Python.3.12…`** — NOT `python.exe` and NOT by command-line match (both silently miss it).
- **python-telegram-bot retries FOREVER on a 409 Conflict** → two pollers fight endlessly. Fixed with a `bot.pid`
  self-replace (`ensure_single_instance()` kills the prior PID on startup). Never run two instances.
- **Don't kill-all-python** as a fallback — the session's own MCP servers (elevenlabs via uv) are `python.exe` too; I killed this session's elevenlabs MCP that way once.
- Claude Code **v2.1.178 ships a native `bin/claude.exe`** (no cli.js) → invoke the exe directly. CLI is NOT on PATH in spawned shells; it's at `%APPDATA%\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe`.
- `claude -p` with no piped stdin waits 3s → pass `stdin=DEVNULL` (done). Calling `claude` from inside this Claude session hangs — avoid nested invocations.
- IG Graph API has no trial-reel READ field and no saved-posts endpoint (§2).

## 7. 🔨 NEXT — in order (after billing is sorted via §5 or §4)
1. **Confirm the bot end-to-end:** Elijah sends `/start` (welcome ✓), then a real prompt (e.g. "what's working this week") → a real hub answer with IG data. This validates the whole architecture.
2. **Trial-reel MCP patch (Phase 2):** vendor `@mcpware/instagram-mcp` into `hub/mcp-servers/instagram-mcp/`, patch `publishReel` (in `dist/client.js`) to accept + send `trial_params`, `npm install` its deps, re-point `.mcp.json` from `npx -y …` to the local fork (keep original line commented = 1-line revert). Test the fork launches before re-pointing.
3. **Multi-account:** add a SECOND instagram MCP instance in `.mcp.json` for infinetAI.org (own token/account-id env vars) — blocked until that account is connected.
4. **infinetAI.org carousel engine (Phase 3):** daily AI/tech/security/uncensored-AI news → `carousel-builder` skill → render slide images → `publish_carousel` (per-OK) → daily task. NEW infra needed: the account connected (below) + public image hosting for slides.
5. **Saved-carousel reference doc:** Elijah pastes his "carousel copy" permalinks → I pull each via `business_discovery`/permalink → build a "winning carousel patterns" reference that feeds the infinetAI engine.

## 8. ⚑ infinetAI.org account connection (Elijah's move, needed for #3/#4 above)
Create the IG account → switch to Business/Creator → link to a Facebook **Page** he admins → regenerate a long-lived
token covering BOTH Pages → give me the new account ID. (Accounts aren't visible just by sharing a Facebook login — the
link is Page + token permissions.) `business_discovery` works with zero setup but is public-data-only.

## 9. ARTIFACT MAP
- Bridge: `telegram-bridge/` (README has setup/run/security). Zip for Tanner: `…\Desktop\podcast-interview-editor-skill.zip`.
- Skill source: `C:\Users\elija\.claude\skills\podcast-interview-editor\` (+ `INTEGRATION-FOR-CLIPWITH.md`).
- Memories: `…\.claude\projects\…\memory\{project-telegram-bridge,project-personal-use-scope}.md` + MEMORY.md.
- Prior baton (still useful for the 2026 analytics engines + level-up/self-improve state): `SESSION-COMPACT-2026-06-15.md`.
