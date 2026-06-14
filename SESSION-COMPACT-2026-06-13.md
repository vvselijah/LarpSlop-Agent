# SESSION COMPACT & AUDIT — 2026-06-13 (auto-clip completion)

> **Doc precedence (read in this order):** **THIS FILE** (newest, verified state) → `HANDOFF.md`
> (master ops/bring-up) → `docs/plans/2026-06-13-SESSION-HANDOFF.md` (long historical baton).
> Written for a competent stranger with zero prior context. Every claim carries a confidence tag and
> the check that backs it. Author: Claude (Opus 4.8). Audit run before writing — see §8.

---

## 1. HEADLINE / CURRENT STATE
This is **Elijah Sullivan's AI-agent hub** (`C:\Users\elija\OneDrive\Desktop\ai agent team`) — a Claude
Code workspace that runs his Instagram analytics, competitive intel, content tooling, and Meta ads for
**@elijahaifl (100,324 followers, live-verified)**. This session **finished the `auto-clip` engine's
missing "brain"**: a no-API-key, no-install highlight selector where **Claude itself picks the clips**,
plus an orchestration skill. The full pipeline (transcribe → agent-highlight → reframe) was run
end-to-end and produced **6/6 valid 1080×1920 shorts**. Committed as **`7e0b9a5` on `main`**.
**Single most important fact: that commit is NOT yet pushed** (local `main` is 1 ahead of `origin/main`).

---

## 2. WHAT'S DONE (tagged + how verified)

### This session (auto-clip)
| Item | Tag | Verified how |
|---|---|---|
| `auto-clip/highlight.py` gains `--provider agent` (Claude is the selector; 2-step: emit brief → agent writes `picks.json` → Python maps seg→time) | ✅ DONE+VERIFIED | Ran both steps live; logs show brief written + 6 clips mapped/ranked |
| New `.claude/skills/auto-clip/SKILL.md` orchestration skill | ✅ DONE+VERIFIED | File exists (Glob); skill appears in the live skill registry |
| End-to-end pipeline on `source.mp4` → 6 vertical clips | ✅ DONE+VERIFIED | `ffprobe` on all 6: every one `1080,1920`, `aac` audio, durations 13–53s |
| `auto-clip/README.md` status + `CLAUDE.md` capability map + `team/memory.md` learning updated | ✅ DONE+VERIFIED | Edits applied; included in commit `7e0b9a5` (5 files, +183/-38) |
| Commit `7e0b9a5` on `main`, worktree clean, artifacts gitignored | ✅ DONE+VERIFIED | `git log`, `git status --short` (clean), `git check-ignore` on data/out |
| `transcribe.py` (faster-whisper word-level) | 🟡 BUILT, prior-tested | Built+tested in commit `cbc0851`; artifact `data/audio.transcript.json` (77 seg/1182 words) exists. **NOT re-run this session** — `import faster_whisper` hung on this OneDrive disk (see §6) |

### Pre-existing platform (spot-verified live this session)
| Subsystem | Tag | Verified how |
|---|---|---|
| Instagram MCP + token | ✅ DONE+VERIFIED | `validate_access_token`→`{valid:true}`; `get_profile_info`→@elijahaifl, id `17841400159953101`, 100,324 followers, 583 media |
| IG token expiry **2026-08-11** | ✅ DONE+VERIFIED | `team/stats.md` line 23 (auto-written by refresh.py) |
| Meta Ads MCP | ✅ DONE+VERIFIED | `ads_get_ad_accounts`→ acct `661339332628311`, ACTIVE, USD, queryable, has payment method |
| Daily refresh pipeline is firing | ✅ DONE+VERIFIED | `team/stats.md` "Updated: 2026-06-13 11:39 UTC" (today); `refresh.log` shows repeated "refresh complete" |
| 8 local skills present | ✅ DONE+VERIFIED | Glob `.claude/skills/*/SKILL.md`: weekly-content-plan, niche-intel, context-checkpoint, dev-workflow, research, carousel-builder, comment-triage, auto-clip |
| Engines + both PLAN docs present | ✅ DONE+VERIFIED | Glob: `ig-dashboard/refresh.py`, `intel/{competitor,trend}-radar.py`, `auto-clip/*.py`, `docs/plans/2026-06-13-{auto-clip,audience-sim}-pipeline.md` |
| GitHub repo pushed through `096062e` | ⚠️ ASSUMED (last fetch) | `origin/main` tracking ref = `096062e`; not freshly fetched this session |
| Scheduled-task repoint (action=`Daily Agent Refresh.bat`, run-when-missed, LogonType Interactive) | ⚠️ ASSUMED | Per `HANDOFF` UPDATE 6 (Elijah ran it); **live `Get-ScheduledTask` hung** (§6) — not re-verified this session |

---

## 3. DECISIONS LOCKED (+ WHY)
- **Claude is the auto-clip highlight brain (`--provider agent`)** — the hub has no `ANTHROPIC_API_KEY`
  and no local Ollama; requiring either (or a multi-GB model) is wrong for an interactive Claude-Code hub.
  The 2-step design keeps the **deterministic seg→time mapping/sort in Python** so the agent only does the
  creative selection. `anthropic`/`ollama` providers remain for unattended/scheduled runs only.
- **auto-clip ranks for SAVES/MONEY/AI** — `team/stats.md` shows Money/Finance ≈4.1M views/19 posts is the
  runaway leader and AI/Tech his best save niche; the skill tells the selector to rank those highest.
- **Engine stops at `out/`, never publishes** (CLAUDE.md rule 1). Any future IG publish = voice-only/
  original-audio (rule 4) + `get_content_publishing_limit` pre-flight + Elijah's per-action click.
- **Pure-FFmpeg reframe, not Remotion** — avoids the ~10GB/bundle disk blowup documented in `..\abc wrap\`.
- **Research-key 401 is NOT a bad key** — do NOT re-issue (see §6); fix is a full app restart.
- **Both auto-clip + audience-sim PLANs already APPROVED** by Elijah (HANDOFF UPDATE 6). auto-clip = build;
  audience-sim = cheap R&D spike, treat as unproven for IG until backtested.

---

## 4. NEXT STEPS (prioritized; ⚑ = needs the operator/Elijah)
1. **⚑ Push the commit:** `git push origin main` (local `main` is 1 ahead — `7e0b9a5`). Browser/GCM auth.
2. **Pick the next auto-clip layer** (Elijah deferred the choice — all three are open):
   - **Captions** (recommended first; biggest short-form lever): burn karaoke captions onto the 6 clips.
     Cheapest path = pure-FFmpeg/ASS from the word-level transcript (no install); premium path = the
     `caption-engine` skill (Remotion, heavier).
   - **Face-track reframe v2:** ⚑ needs `pip install opencv-python mediapipe` **and a 16:9 test source**
     (the sample is already vertical, so it can't exercise tracking).
   - **audience-sim Phase 0:** ⚑ `pip install camel-oasis`, seed ~100 personas, spike on one past reel,
     **backtest vs the 300-post history before trusting** (`docs/plans/2026-06-13-audience-sim-pipeline.md`).
3. **⚑ Research keys (Exa/Tavily/Firecrawl):** do a TRUE full quit + relaunch of the Claude Code desktop
   app (tray Quit / end process — a window close is NOT enough), then test one `mcp__exa__web_search_exa`
   call. Keys are valid; do not re-issue. (Not blocking — all research deep-dives are already done.)
4. **⚑ GPU `torch-cu128`** (optional, multi-GB): reinstall torch `--index-url .../cu128` + cuDNN9 → near-
   instant transcribe + `h264_nvenc` encodes. Only worth it if long-form clipping volume ramps.
5. **⚑ Verify the scheduled task** once (env was too slow this session): run
   `Get-ScheduledTask 'IG Dashboard Daily Refresh'` in an interactive PowerShell; confirm action =
   `Daily Agent Refresh.bat` and `StartWhenAvailable=True`.
6. **Recurring:** renew the IG token by ~2026-08-11 (HANDOFF §4).

---

## 5. ARTIFACT MAP (paths + commands)
**Auto-clip engine** — `auto-clip/`
- `transcribe.py` → `python transcribe.py <video> [--model base.en] [--device cpu]` → `data/<stem>.transcript.json`
- `highlight.py` → **agent path (interactive, default):**
  `python highlight.py data/<stem>.transcript.json --provider agent --n 6` (writes `data/<stem>.agent-prompt.json`),
  then the agent writes `data/<stem>.picks.json`, then
  `python highlight.py data/<stem>.transcript.json --provider agent --from-picks data/<stem>.picks.json` → `data/<stem>.highlights.json`
- `reframe.py` → `python reframe.py <video> data/<stem>.highlights.json` → `out/<stem>_clip<NN>.mp4` + `out/<stem>.manifest.json`
- **Skill (one-shot):** invoke the `auto-clip` skill ("clip this video"). Orchestrates all of the above.
- Outputs this session: `auto-clip/out/source_clip01..06.mp4` (gitignored). Source: `source.mp4` (94 MB, repo root, already 9:16).
- ⚠️ **Run Python via the PowerShell tool, NOT Bash** (Bash has no `python` on PATH here — see §6).

**Platform** — `ig-dashboard/refresh.py` (+`dashboard.html`, `Open Dashboard.bat`) · `intel/competitor-radar.py`,
`intel/trend-radar.py` · `Daily Agent Refresh.bat` (runs all three) · `team/{profile,stats,memory}.md` (context brain).

**Docs/index** — `HANDOFF.md` (master) · `docs/plans/2026-06-13-SESSION-HANDOFF.md` (long baton) ·
`docs/plans/2026-06-13-{auto-clip,audience-sim}-pipeline.md` (approved PLANs) · `docs/RESEARCH-PROTOCOL.md`.

**Git** — repo `https://github.com/vvselijah/LarpSlop-Agent.git` (private, framework-only). HEAD `7e0b9a5` (main).

---

## 6. GOTCHAS & ENVIRONMENT (hard-won; don't relearn)
- **`python` & `ffmpeg` resolve only in the PowerShell tool, NOT the Bash tool.** Bash here also lacks
  `head`/`tail`. Use **PowerShell for all Python/ffmpeg runs**; use Bash for `git`.
- **Heavy Python imports hang on this OneDrive-synced disk.** `import faster_whisper`/`import cv2` did not
  return in 90s+ this session (torch/DLL load + disk contention). For dep *existence* checks use
  `python -m pip show <pkg>` (metadata, no import), not `python -c "import ..."`. Even `Get-ScheduledTask`
  was slow this session — the box was contended. Long PowerShell calls auto-background; use `TaskOutput`/
  `TaskStop` to manage them.
- **Research keys 401 = process-env absence, NOT bad keys.** Verified: `EXA/TAVILY/FIRECRAWL_API_KEY` are
  present & valid at **User** scope (len 36/57/35) but **empty in the Claude process**, while
  `INSTAGRAM_ACCESS_TOKEN` IS in-process. Cause: the app launched before those keys were set, so the MCP
  servers spawned with empty values. **Fix = full app quit+relaunch.** A `/clear` or window-close does NOT
  reload env vars. Do not rotate the keys.
- **Secrets only in Windows env vars (`setx`)** — the whole tree is OneDrive-synced; never write tokens to files.
- **`.gitignore` comments must be on their OWN line** — a trailing `# comment` becomes part of the pattern
  (it nearly staged the whole vault once). The `auto-clip/data/` + `out/` + `*.mp4` ignores are confirmed working.
- **PowerShell → `graph.facebook.com` hangs** — repo scripts use Git-Bash `curl` for Graph reads.
- **DMs blocked by Meta App Review** (app capability, error #3), not the token. Comments work today.

---

## 7. RISKS / OPEN QUESTIONS / TECH DEBT
- **Unpushed commit `7e0b9a5`** — if this machine dies before a push, the auto-clip brain work is local-only.
- **transcribe.py not re-verified this session** — relies on faster-whisper, which couldn't be re-imported
  (disk hang). High confidence it works (prior commit + existing transcript artifact), but unconfirmed today.
- **Scheduled-task state unconfirmed this session** (env too slow). If the repoint silently regressed, the
  daily competitor/trend radars wouldn't refresh — though `stats.md`'s fresh timestamp shows the dashboard leg runs.
- **auto-clip face-track is v1 center-crop only** — a wide (16:9) source with an off-center speaker will get
  clipped poorly until v2 (OpenCV/MediaPipe) lands. The vertical sample never exercised this path.
- **audience-sim is unbuilt + unproven for IG** — simulates X/Reddit, ~30% RMSE; qualitative-only until backtested.
- **Open questions for Elijah:** caption style (quick FFmpeg/ASS vs premium Remotion `caption-engine`)?
  Greenlight the multi-GB GPU `torch-cu128` reinstall? Greenlight `camel-oasis` install for the audience-sim spike?

---

## 8. VERIFICATION LOG (what was actually run)
| Check | Command/tool | Result |
|---|---|---|
| Auto-clip highlight agent path | `python highlight.py … --provider agent` (emit + `--from-picks`) | ✅ brief written; 6 clips mapped/sorted/ranked |
| Auto-clip render | `python reframe.py ..\source.mp4 data/audio.highlights.json` | ✅ 6/6 clips written to `out/` |
| Clip validity | `ffprobe` width,height,duration,audio on all 6 | ✅ all `1080,1920`, `aac`, 13–53s |
| Commit | `git add … && git commit` → `git log` | ✅ `7e0b9a5`, 5 files, +183/-38 |
| Worktree clean / ignores | `git status --short`, `git check-ignore` | ✅ clean; data/out/*.mp4 ignored |
| Push state | `git rev-list --left-right --count origin/main...main` | ⚠️ `0  1` → local 1 ahead (unpushed) |
| IG token | `mcp__instagram__validate_access_token` | ✅ `{valid:true}` |
| IG profile | `mcp__instagram__get_profile_info` | ✅ @elijahaifl, 100,324 followers, 583 media |
| Meta Ads | `mcp__meta-ads__ads_get_ad_accounts` | ✅ `661339332628311` ACTIVE/USD/queryable |
| Daily pipeline | Read `team/stats.md` + grep `refresh.log` | ✅ stats updated 2026-06-13 11:39 UTC; multiple "refresh complete" |
| Env keys (process vs user) | PowerShell `[Environment]::GetEnvironmentVariable(...,'Process'/'User')` | ✅ research keys User-only; absent in process |
| Exa MCP (symptom) | `mcp__exa__web_search_exa` | ✅ confirms 401 "Invalid API key" (process-env cause) |
| Skills + engines + PLANs | Glob | ✅ 8 skills, all engines, both PLAN docs present |
| Deps re-import / scheduled task live | PowerShell `import …` / `Get-ScheduledTask` | ❌ hung (disk/CPU contention) — tagged ⚠️/🟡 above |
