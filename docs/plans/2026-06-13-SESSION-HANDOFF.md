# SESSION HANDOFF — 2026-06-13 (the long one)

**Read this first on resume**, then the master `HANDOFF.md` and workspace `CLAUDE.md`.
This is the baton for everything built in the 2026-06-13 session.

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
