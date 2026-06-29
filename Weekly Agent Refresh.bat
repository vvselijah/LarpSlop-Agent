@echo off
REM ============================================================================
REM  Weekly Agent Refresh -- activates the "orphaned" 2026 engines that the
REM  DAILY refresh does not run. Proposed by the 2026-06-15 level-up pass
REM  (finding #1: 7 validated engines run on NO schedule = pure activation gap).
REM
REM  INSTALL (Elijah-gated): create a Windows Task Scheduler task ->
REM    Program:  <your python.exe path or just "cmd">
REM    Argument: /c "<this folder>\Weekly Agent Refresh.bat"
REM    Trigger:  weekly, Sunday ~7:00 AM
REM    Options:  [x] Run task as soon as possible after a missed start
REM  This .bat is the proposal artifact; the scheduled task is yours to create.
REM
REM  Each step is INDEPENDENT -- a failure in one engine does not stop the rest
REM  (same pattern as Daily Agent Refresh.bat). All steps are READ-ONLY: API
REM  GETs + scraper reads only, never publish/comment/DM.
REM ============================================================================

set ROOT=%~dp0
echo [%date% %time%] Weekly Agent Refresh starting...

REM ---- THE VIRAL DISCOVERY PIPELINE (discover -> track -> tear down) ----

echo --- 1/6 Niche radar (hashtag DISCOVERY via scraper) ---
REM Needs APIFY_TOKEN (set via: setx APIFY_TOKEN "...") -- skips itself cleanly
REM if the key is absent, so the rest of the chain still runs.
python "%ROOT%intel\niche-radar.py"

echo --- 2/6 Viral radar (true-view tracking of watchlist accounts) ---
python "%ROOT%intel\viral-radar.py"

echo --- 3/6 Viral teardown (WHY the winners win; reads BOTH leaderboards) ---
python "%ROOT%intel\viral_teardown.py"

REM ---- OTHER ORPHANED WEEKLY ENGINES (level-up activation set) ----

echo --- 4/6 News radar (AI-news -> content ideas) ---
python "%ROOT%intel\news-radar.py"

echo --- 5/6 Watch-time ideator (long-form watch-time arbitrage) ---
python "%ROOT%ig-dashboard\watchtime_ideator.py"

echo --- 6/6 Self-improve grader (model vs realized outcomes; self-monitor) ---
python "%ROOT%self-improve\grade.py"

echo [%date% %time%] Weekly Agent Refresh complete.
