# memory.md — what the agent team has learned (self-updating)

> The agent appends dated learnings here after planning runs, post-mortems, and
> experiments. Newest first. Humans may edit/prune freely. Keep entries short:
> one finding, one line of evidence, one implication.

## 2026-06-13 — auto-clip "brain" completed: Claude IS the highlight selector

- **The missing "brain" is solved without any new dependency:** `highlight.py` gained a `--provider agent`
  path where the Claude Code agent makes the editorial clip selection (two-step: emit a brief → agent writes
  `picks.json` → Python does the deterministic seg→time mapping/sort). No `ANTHROPIC_API_KEY`, no Ollama (not
  installed), no install. Evidence: ran transcribe → agent-highlight → reframe end-to-end on `source.mp4` →
  6/6 valid 1080×1920 H.264/AAC clips. Implication: auto-clip is **usable interactively today** via the new
  `auto-clip` skill; the anthropic/ollama providers are only for unattended/scheduled runs.
- **Pattern worth reusing:** for a "local agent hub," the cheapest, highest-quality LLM step is often the agent
  itself — wire a `--provider agent` mode instead of requiring a paid key or a multi-GB local model.
- **Research keys (Exa/Tavily/Firecrawl) 401 is NOT a bad-key problem:** they're valid at User scope (len
  36/57/35) but absent from the Claude *process* env (INSTAGRAM token IS present). The MCP servers spawned with
  empty keys. Fix = a true full quit + relaunch of the desktop app (not a window close). Do NOT re-issue them.

## 2026-06-13 — business-ops + productivity research (round 3) + a throttle lesson

- **Scheduling:** Metricool stays the cross-platform pick — but its MCP needs the **Advanced ~$54/mo** plan (blueprint said "any plan" — stale), and IG licensed-audio auto-publish is now **partially** unlocked (needs Facebook-Login auth; trending-sound catalog may be narrow). TikTok still MUST go through an audited client (never a self-built MCP). Full report: `docs/plans/2026-06-13-business-ops-productivity-research.md`.
- **Course platform:** migrate Archetype Index → **Whop** (verified: official `@whop/mcp` + native Courses + lowest fees, no monthly). Skool only if it's community-first. Tie-breaker O3 in the report.
- **Payments/CRM/newsletter:** **Stripe official MCP** (restricted key in env var — NOT Composio's cloud vault); sponsor CRM = a **vault `sponsors/` folder**, no SaaS; **beehiiv** MCP is read-only V1 + Send API is Enterprise-beta (later/at-launch).
- **Productivity:** nothing new to buy — reuse `auto-clip/transcribe.py` + the vault + the 7AM scheduled task for podcast→notes + a daily briefing.
- **THROTTLE LESSON:** even a single 5-agent workflow partial-throttled (3/4 research agents rate-limited) when Anthropic was load-shedding. Recovered per protocol: did NOT relaunch the fan-out; spot-verified the load-bearing claims with direct WebSearch instead. Reinforces: keep research fan-outs small, and verify-don't-relaunch on a throttle.

## 2026-06-13 — capability research round 2 (audience-sim / Composio / Playwright)

- **Pre-publish audience simulation is viable & novel:** camel-ai/OASIS (Apache-2.0, local) is the pick — a QUALITATIVE hook-ranker seeded from his audience that PAIRS with Higgsfield (OASIS gates the hook, Higgsfield gates the edit). Caveat: simulates X/Reddit not IG, ~30% RMSE → must backtest vs the 300-post history before trusting. PLAN: `docs/plans/2026-06-13-audience-sim-pipeline.md`.
- **BettaFish/MiroFish = not for us:** China-platform public-opinion analysis, restrictive licenses (GPL/AGPL), overlap owned tools. Cherry-pick only BettaFish's multi-agent "debate" pattern.
- **Composio = add-later, scoped:** powerful 500+ toolkit MCP gateway, but its cloud vault stores tokens OFF-machine → conflicts with the secrets-local rule. OK for low-stakes Notion/Calendar/Sheets; NEVER route IG/Meta tokens through it. Self-host is Enterprise-only.
- **Playwright MCP = skip now:** overlaps the already-wired Claude-in-Chrome + Firecrawl; only wedge is headless unattended scheduled browser jobs (not a need). Logged-in IG/TikTok browser scraping = ToS/ban — public pages only.

## 2026-06-13 — capabilities recon + research (Workflow 1)

- **Auto-clipping is ~70% already built, not a from-scratch project.** Local transcription (faster-whisper 1.2.1 installed), the editorial cut-list brain (`abc wrap/interview/work/build_cutlist.js`), and a data-driven crop comp (`abc wrap/src/edits/PodcastEdit.tsx`) all exist. Only 3 new pieces needed: local-transcribe JSON wrapper, an LLM highlight/moment **selector** (the true missing brain), and face-track 9:16 reframe. Implication: build small + reuse; don't rebuild captions/b-roll/export.
- **GPU is idle:** RTX 5070 (Blackwell sm_120) present but torch is the +cpu build → faster-whisper runs CPU-only. Needs the `cu128` torch wheels + cuDNN9. Highest-leverage perf fix before any clipping work.
- **Carousels are pure untested upside:** he runs zero today. Optimize a carousel skill for SAVES first (his live save-rate peaks ~3.6% on AI/Tech utility); Money/Finance remains the view-leader (~25× Motivation).
- **Competitor intel = two layers:** free `business_discovery` (own token, zero ban risk, counts-not-text) + Apify pay-per-result for comment TEXT/TikTok/YouTube (never touches his token). Bright Data is enterprise-overkill ($250 min). Do sentiment in-house with Claude, not a paid actor.
- **DMs at scale need Meta App Review (Advanced Access).** Error #3 = Standard Access only. Comments (read/reply/hide) work today; DM replies only inside the 24h reactive window; cap ~200 business-initiated msgs/hr. HUMAN_AGENT tag must never be auto-applied (revocation risk). Triage must be webhook-driven + draft→human-approve→send.
- **Env-var landmine recurred:** research keys (Exa/Tavily/Firecrawl) were set correctly at User level but absent from the running process → 401. Only a FULL Claude restart loads new env vars; `/clear` keeps the same process. Verify MCP keys with one live call after any session that added env vars.

## 2026-06-12 — seeded at system creation

- **Category arbitrage detected:** last 30d — Money/Finance: 4.15M views from 20 posts (~207k/post) vs Motivation/Life: 554k views from 66 posts (~8.4k/post). Implication: shift volume from Motivation toward Money/Finance and AI/Tech until the data says otherwise.
- **Publishing quota is a non-issue:** live check shows 0/100 daily API publishes used. The real IG API constraint is no licensed/trending audio on API-published reels.
- **TikTok cannot be self-automated** (unaudited apps post private-only). Route TikTok through an audited scheduler (Metricool) or skip.
- **Infrastructure:** IG token auto-renews its expiry display (real expiry 2026-08-11); dashboard self-feeds stats.md daily at 7:00 AM.
