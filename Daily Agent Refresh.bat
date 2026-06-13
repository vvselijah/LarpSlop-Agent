@echo off
REM Daily Agent Refresh — runs all three intelligence engines in sequence.
REM Point the Windows scheduled task ("IG Dashboard Daily Refresh") at THIS file
REM instead of refresh.py to refresh own-stats + competitor radar + trend radar
REM every morning. Each script is path-relative and safe to run from any cwd.
REM Logs go to each engine's own data\ folder (refresh.log / report .md files).

set ROOT=%~dp0
echo [%date% %time%] Daily Agent Refresh starting...

echo --- IG dashboard (own account) ---
python "%ROOT%ig-dashboard\refresh.py"

echo --- Competitor radar ---
python "%ROOT%intel\competitor-radar.py"

echo --- Trend radar (virality early-warning) ---
python "%ROOT%intel\trend-radar.py"

echo [%date% %time%] Daily Agent Refresh complete.
