# SESSION HANDOFF — 2026-06-13 (the long one)

**Read this first on resume**, then the master `HANDOFF.md` and workspace `CLAUDE.md`.
This is the baton for everything built in the 2026-06-13 session.

---
## ⏩ UPDATE — Workflow 1 (recon + research) landed; build phase is next
**Resume here.** A throttle-safe 6-agent workflow (`wf_646cdd8c-80a`) completed clean. Full results +
the **build spec** are in `docs/plans/2026-06-13-capabilities-research-plan.md` → section
"DEEP-DIVE RESULTS — Workflow 1". Read that; it's the implementation brief. Highlights:

- **FIRST THING ON RESUME — fix the research keys:** Exa/Tavily/Firecrawl 401 because their keys, though
  correctly set at User level (valid prefixes), were NOT in this session's process env. **A full quit +
  relaunch of Claude Code loads them** (`/clear` does NOT — same process). After relaunch, verify with one
  `mcp__exa__web_search_exa` call. Keys are valid — do NOT rotate.
- **Build order (locked by content mix — short-form now, ramping long-form):**
  1. `carousel-builder` skill (leverage now; he runs zero carousels; optimize SAVES first, Money/Finance + AI/Tech).
  2. `comment-triage` skill (comment-only v1 works TODAY via instagram MCP; draft→approve→reply, never auto-send).
  3. `auto-clip` engine — **write a PLAN first** (dev-workflow). ~70% already exists in hub + `..\abc wrap\`;
     build only: local-transcribe wrapper, LLM highlight selector, face-track 9:16 reframe. GPU fix (torch cu128) gates speed.
- **Intel = ADD NOW:** free `business_discovery` (already wired) + optional Apify pay-per-result (never touches his token); Bright Data SKIP.
- **Task list (in-session):** #2 carousel, #3 comment-triage, #4 auto-clip PLAN, #5 housekeeping (repoint task), #6 save-back. (#1 done.)
- **Open Qs for Elijah** (don't block builds; ask at the relevant step): Meta app Advanced vs Standard access?
  Competitor comment TEXT vs COUNTS + volume? Do the torch-cu128 GPU reinstall (multi-GB)? Webhook host vs polling for DM-triage v1?
- **Housekeeping recon done:** scheduled task "IG Dashboard Daily Refresh" still points at `refresh.py` with
  `StartWhenAvailable=False`; repoint to `Daily Agent Refresh.bat` + set run-when-missed AFTER validating the .bat
  (confirm bare `python` resolves in task context). Deferred during the run to avoid IG-API contention — now clear.

---
## ⏩ UPDATE 2 — build phase DONE; restart recommended (fixes keys + context)
**Workflow 2 (`wf_9d2a41e9-019`) complete — all 3 items adversarially verified PASS (zero must-fix):**
- ✅ **`carousel-builder` skill** — `.claude/skills/carousel-builder/SKILL.md` (live in registry). Optimizes
  SAVES-first, Money/Finance + AI/Tech, slide-1 hook, vault idea-note output, publish gated. **One tiny cleanup:**
  step 7 has a garbled sentence ("and only voice-only/original-audio constraints don't apply…") — rewrite cleanly
  (FIRST quick task next session; content is correct, grammar is broken).
- ✅ **`comment-triage` skill** — `.claude/skills/comment-triage/SKILL.md` (live). Comment-only DRAFT→approve→reply,
  never auto-send, hide-over-delete, DM/Advanced-Access caveat encoded.
- ✅ **auto-clip PLAN** — `docs/plans/2026-06-13-auto-clip-pipeline.md` — **PLAN ONLY (no engine code), awaiting
  Elijah's approval** before building the `auto-clip/` engine.
- ⏳ **Scheduled-task repoint** submitted (`Set-ScheduledTask`, bg `bz28nsb3a`) but **completion NOT confirmed** —
  VERIFY first: `Get-ScheduledTask "IG Dashboard Daily Refresh"` action should be `Daily Agent Refresh.bat`,
  `StartWhenAvailable=True`. Then a one-shot `.bat` validation run + **diagnose 06/12 `LastResult 0x800710E0`**
  (the refresh.py run errored — daily pipeline may have been failing).

**NEW research queued (Elijah req 2026-06-13) — see capabilities-plan items #6 & #7:**
- #6 **OASIS (camel-ai) / BettaFish / MiroFish** — agent-based audience-reaction SIMULATION → predict how his
  audience reacts to the next post/hook pre-publish; compare/mix; integration sketch.
- #7 **Composio** — managed multi-app agent toolkit; validity + use vs existing MCP stack + the env-var/OneDrive
  secret constraint. Fire via `research-lean`, ONE at a time, AFTER restart (so Exa/Tavily/Firecrawl work).

**➡️ RECOMMENDED NOW: full quit + relaunch Claude Code.** Reasons converge: (a) loads the research keys into the
process (fixes the Exa/Tavily/Firecrawl 401 — needed for the new research), (b) clears a near-full context window.
Nothing is lost — all state is in this handoff + `docs/plans/2026-06-13-capabilities-research-plan.md`. On resume:
verify the repoint → fix the carousel typo → review the auto-clip PLAN with Elijah → fire research #6 then #7 →
finish save-back (task #6: CLAUDE.md capability map + AGENT-TEAM-BLUEPRINT tiers) → GitHub push when URL given.

---
## ⏩ UPDATE 3 — sim/Composio research DONE (report on disk); RESTART NOW is safe
Workflow 3 (`wf_d83c9e71-06a`) complete → full report: `docs/plans/2026-06-13-simulation-composio-research.md` (high confidence). Verdicts:
- **OASIS (camel-ai, Apache-2.0) = the pick.** Build a small self-hosted `audience-sim/` engine seeded from real
  @elijahaifl audience data as a QUALITATIVE pre-publish hook-ranker that PAIRS with Higgsfield (OASIS gates the
  idea/hook, Higgsfield gates the edit). Caveats: simulates X/Reddit not IG (directional proxy), NO shipped
  persona-seeder (build it), ~30% RMSE → qualitative only. Plan: 2-3h spike on ONE past reel → backtest vs the
  300-post ig-dashboard history BEFORE trusting output. (Becomes a new PLAN doc + `audience-sim/` engine.)
- **BettaFish = SKIP** (China public-opinion analysis, GPL-2.0, overlaps owned tools; cherry-pick only its ForumEngine debate pattern).
- **MiroFish = investigate-later toy** (polished OASIS wrapper, China-cloud Qwen/Zep/GraphRAG, AGPL-3.0).
- **Composio = add-later, SCOPED** (MIT SDK, free 20k-call tier, one-line Claude Code MCP add) BUT its default cloud
  vault stores OAuth/API tokens OFF-machine → conflicts with secrets-local; self-host is Enterprise-only. OK for
  low-stakes Notion/Calendar/Sheets; **NEVER route IG/Meta tokens through it**; skip GitHub (redundant), use beehiiv's
  native MCP. UNVERIFIED: an alleged Composio token-security incident couldn't be confirmed — check before high-privilege use.
- **#8 Playwright MCP = NOT yet researched** (queued in capabilities-plan; fire next pass, one workflow at a time).

**➡️ FULL RESTART NOW is the move — and finally safe (no workflow running).** Fixes the Exa/Tavily/Firecrawl 401
(loads keys into the process) + clears an overflowing context window. RESUME ORDER on next session:
1. Playwright MCP research pass (#8). 2. Verify the scheduled-task repoint + one-shot `.bat` validation run +
diagnose 06/12 `0x800710E0`. 3. Fix the carousel-builder step-7 grammar. 4. Review the auto-clip PLAN + draft the
`audience-sim` (OASIS) PLAN with Elijah. 5. Save-back: CLAUDE.md capability map + AGENT-TEAM-BLUEPRINT tiers + a
memory learning. 6. GitHub push when Elijah gives the repo URL.

---
## ⏩ UPDATE 4 — "DO EVERYTHING" pass (post-restart)
- ✅ Carousel-builder step-7 grammar fixed · ✅ Playwright MCP verdict (**SKIP-now**, `docs/plans/2026-06-13-playwright-mcp-verdict.md`) · ✅ OASIS **audience-sim PLAN** drafted (`docs/plans/2026-06-13-audience-sim-pipeline.md`, draft — awaiting approval).
- ✅ Save-back: CLAUDE.md capability map (2 new skills + queued PLANs); AGENT-TEAM-BLUEPRINT round-2 tier verdicts; team/memory.md (2 dated blocks).
- ⚠️ **RESEARCH KEYS STILL 401** — the restart did NOT reload Exa/Tavily/Firecrawl (closing the window ≠ a full app quit, OR the keys are invalid). They ARE set at User level w/ valid prefixes. Action: do a TRUE full quit+relaunch, then test one `mcp__exa__web_search_exa` call; if STILL 401, the key VALUES need re-checking/re-issuing.
- 🔒 **SCHEDULED-TASK REPOINT BLOCKED (interactive password).** The task runs with STORED CREDENTIALS, so every modify (`Set-ScheduledTask` AND `schtasks /Change`) hangs on `"Please enter the run as password for elija:"` — non-interactive can't answer. **Task is UNCHANGED/intact** (daily refresh.py still runs). FIX (Elijah, one-time): in Task Scheduler GUI set the action to `Daily Agent Refresh.bat`, tick "Run task as soon as possible after a scheduled start is missed"; OR run the `Register-ScheduledTask` snippet (in chat) in an interactive PowerShell and type your password. Set LogonType Interactive to avoid the password entirely.
- 🔁 **refresh.py validation** run to diagnose the 06/12 `LastResult 0x800710E0` — check `ig-dashboard/data/refresh.log` for the result.
- ⏳ **PENDING ELIJAH:** (1) approve the **auto-clip** + **audience-sim** PLANs → I build the engines; (2) the scheduled-task fix above; (3) the **private repo URL** for the GitHub push; (4) a true full restart for the research keys.

## Current state (what's live)
- **Deep-research stack is LIVE** — `exa`, `tavily`, `firecrawl` MCPs all connected (confirmed
  post-restart). Keys in Windows env vars (valid; Firecrawl had 1025 credits). Use them.
- **IG token** valid → expires **2026-08-11** (auto-detected by refresh.py).
- **GitHub repo** — framework committed **locally** (`f364ef4`, 52 files, clean, framework-only).
  NOT pushed yet (see Next Actions #1).
- All prior systems intact: ig-dashboard, intel radars, vault, skills, Meta/IG MCPs.

## What this session built (newest-relevant first)
1. **Research efficiency overhaul** — diagnosed the built-in `deep-research` throttle (its Verify
   phase bursts ~75 agents → Anthropic load-shed → abstentions → "synthesis skipped"). Built the
   throttle-safe **`.claude/workflows/research-lean.js`** (≤6 concurrent verify) + **`docs/RESEARCH-PROTOCOL.md`**
   (direct-first → research-lean → ONE workflow at a time). research-lean has now run clean 3×.
2. **Deep-research stack wired** — Exa + Tavily + Firecrawl in `.mcp.json` (`${VAR}` placeholders);
   `research-lean` prefers them; `docs/RESEARCH-STACK-SETUP.md` documents it.
3. **GitHub repo prep** — `.gitignore` (framework-only; caught a trailing-comment bug that would
   have leaked the vault — see Landmines), README + MIT LICENSE, clean local commit.
4. **Capabilities research** — broad survey done; results + 5 queued deep-dives in
   `docs/plans/2026-06-13-capabilities-research-plan.md`.
5. **Product direction + feasibility** — `docs/PRODUCT-VISION.md`: comments work via API TODAY;
   **DMs are blocked by Meta App Review** (app capability, NOT the token — error #3).
6. **Tanner's tworkflow integrated** (earlier) — `dev-workflow` + `context-checkpoint` skills,
   `docs/workflow/` + `docs/templates/`, the 40% hook in `.claude/settings.json`.
7. **New `research` skill** (this handoff) — auto-routes research requests through the protocol.

## Next actions (priority order)
1. **Push the GitHub repo** — Elijah creates an empty PRIVATE repo `ai-agent-team` on github.com,
   pastes the URL → `git remote add origin <url>; git push -u origin main` (GCM browser auth) →
   add Tanner as collaborator. (gh CLI failed to install — needs admin/UAC; the no-gh path above works.)
2. **Build the auto-clipping + local-transcription pipeline** (top capability pick — Faster-Whisper +
   LLM highlight + FFmpeg reframe; turns his podcast/long video → daily shorts + diarized notes).
   First ask Elijah his content mix (long-form vs short reels) — it sets build order. Write a PLAN first.
3. **Build the comment-triage skill** (works on the instagram MCP TODAY; draft→approve→reply).
4. **Fire the 5 queued research deep-dives** one-at-a-time (capabilities plan).
5. **Repoint the scheduled task** from `refresh.py` to `Daily Agent Refresh.bat` + enable
   "run when missed" / "run whether logged on or not" (HANDOFF §6).
6. **IG token renewal** by ~2026-08-11 (HANDOFF §4).

## Landmines (do NOT relearn these)
- **Research:** never run two workflows at once (throttle); use `research-lean`, not built-in `deep-research`;
  try direct WebFetch/live-API FIRST (it gave every decisive answer this session for ~free).
- **Secrets:** never in files (OneDrive-synced); env vars only. **`.gitignore` comments must be on their
  OWN line** — a trailing `# comment` becomes part of the pattern and silently fails (it nearly staged the
  whole vault; the dry-run `git status` leak-check caught it before any commit).
- **Restart required:** env vars, new `.mcp.json` servers, and PATH changes load only on a FULL Claude
  Code quit + relaunch (not a window reopen).
- **DMs:** blocked by Meta App Review (app capability), not the token. Comments work today.
- **gh CLI:** not installed (winget hit UAC 1602). Use the no-gh push path or install with admin.

## Open questions (need Elijah)
- Content mix (long-form podcast vs short reels)? → sets the build priority.
- Speaker diarization (WhisperX) needed, or single-speaker Faster-Whisper enough?
- Brand-deal volume enough for a Notion MCP sponsor pipeline, or local CSV for now?
