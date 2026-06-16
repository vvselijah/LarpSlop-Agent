export const meta = {
  name: 'level-up',
  description: 'Recurring project-wide improvement pass: recall prior decisions, scan the external frontier (viral/content/business strategy + new tools/MCPs/repos/agent practices), re-evaluate our own built assets, then synthesize ONE dated, prioritized DRAFT improvement plan. Context-rot-safe (all work in subagents -> disk).',
  whenToUse: 'Invoked by the level-up skill (or directly) to refresh the project with current best practices. Pass args.date = today YYYY-MM-DD (scripts cannot read the clock). Optional args.focus narrows the frontier sweep.',
  phases: [
    { title: 'Recall', detail: 'read last level-up + memory + roadmap + live model state; assemble the do-not-repeat list + asset inventory' },
    { title: 'Frontier research', detail: '5 parallel domain sweeps of what is NEW since last pass' },
    { title: 'Asset re-eval', detail: 're-score every built engine/skill: value delivered + how to extract more + what is underused' },
    { title: 'Synthesize', detail: 'one dated DRAFT improvement plan + log + memory learning' },
  ],
}

const REPO = "C:\\Users\\elija\\OneDrive\\Desktop\\ai agent team"
const DATE = (args && args.date) || 'undated'
const FOCUS = (args && args.focus) || 'all areas (viral, content, business, tools, agent practices)'

const GUARD = `You are an agent in Elijah's AI-agent-team hub at ${REPO} (@elijahaifl, ~100k IG followers; niches: AI/tech, founder/business, motivation, money/finance, child-safety). HARD RULES:
- READ-ONLY everywhere except the ONE doc your task tells you to write. NEVER edit a production engine (ig-dashboard/*.py, intel/*.py) or the Obsidian vault (obsidian/ is read-only). Improvements are PROPOSED in the plan doc, never applied.
- NEVER publish/post/DM, spend money, install multi-GB deps, or put secrets in files. Do NOT git (the orchestrator handles git).
- Run python via the PowerShell tool, NOT Bash (python isn't on Bash PATH).
- RESEARCH: prefer firecrawl_search (load via ToolSearch query "firecrawl" if its schema isn't loaded) for rich extraction; WebSearch/WebFetch are the always-available baseline. exa/tavily keys are dead in-process. CITE every external claim with a URL and a date; flag anything you can't date. Distinguish "genuinely new since ~mid-2026" from evergreen.
- Your final message is DATA for the orchestrator, not a human note: concise, lead with the result.`

// ----------------------------------------------------------------- Recall
phase('Recall')
const recall = await agent(`${GUARD}

TASK (Recall — so this pass BUILDS on prior ones and doesn't repeat them). Do all of:
1. Find the most recent PRIOR level-up doc: glob docs/plans/*-level-up.md (exclude ${DATE}). If one exists, read it and extract what was already recommended + its tiers, so we don't re-propose the same things.
2. Read team/memory.md (the dated learnings, newest-first) + docs/plans/2026-06-15-MORNING-BRIEFING.md + docs/plans/2026-06-15-overnight-roadmap-v2.md + docs/plans/2026-06-14-overnight-roadmap.md — capture every verdict already locked (ADD-NOW/LATER/SKIP) and every "needs-Elijah" gate, so the frontier sweep knows what's settled.
3. Inventory the hub's CURRENT built assets: list every engine (ig-dashboard/*.py, intel/*.py, auto-clip/*.py, self-improve/grade.py) and every skill (.claude/skills/*/) with a 1-line "what it does + is it wired into the daily 7AM Daily Agent Refresh.bat or on-demand only".
4. Capture LIVE data state: run "python self-improve/grade.py" via PowerShell and read self-improve/data/grade-report.md (the model's current held-out correlations + skip-gate + top proposals). Summarize the 3 headline numbers.

RETURN a structured brief: (A) DO-NOT-REPEAT list (already-decided items w/ verdict), (B) ASSET INVENTORY (engine/skill | one-liner | wired-daily? | obviously underused?), (C) LIVE DATA STATE (grade headlines + the open self-improve proposals), (D) GAPS you already notice. This brief is fed to every later agent.`, { label: 'recall', phase: 'Recall' })

// ----------------------------------------------------------------- Frontier research
phase('Frontier research')
const domains = [
  { id: 'viral-shortform', q: `Short-form VIRAL strategy as of ${DATE}. What's genuinely NEW/changed in the IG Reels + TikTok algorithms and in winning-reel tactics (hooks, retention, skip-rate, shares, watch-time, posting cadence, trial reels, carousels-vs-reels) since ~mid-2026? Tie each to whether the hub's engines already capture it (metrics2026 uses skip>share>like>save>repost>comment + watch-time).` },
  { id: 'content-strategy', q: `CONTENT strategy + formats breaking out for creators in AI/tech, founder/business, and motivation niches as of ${DATE}. New series formats, narrative structures, carousel patterns, longform-from-shortform, repurposing loops. What should a ~100k creator add to their format mix? Cite creators/examples.` },
  { id: 'business-monetization', q: `Creator BUSINESS + MONETIZATION strategy as of ${DATE} for a ~100k-follower technical creator with multiple ventures (AI video studio, uncensored-LLM platform, AI video editor, personality classifier). What monetization models, agency plays, products, community/course platforms (Whop/Skool vs build), and AGENT-ECONOMY product opportunities are working now? Cite.` },
  { id: 'tools-mcps-repos', q: `New AI TOOLS / apps / MCP servers / Claude-Code skills / open-source repos worth ADOPTING into a content+analytics+video agent hub, released or notably updated since ~mid-2026. For each: what it does, the concrete value to THIS hub, license/cost, and integration friction. Return an ADD/WATCH/SKIP shortlist, cited. (Hub already has: Higgsfield, ElevenLabs, TwelveLabs, Remotion/HyperFrames, Meta-ads + IG MCPs, faster-whisper.)` },
  { id: 'agent-practices', q: `New AGENT / automation / self-improving-agent engineering practices as of ${DATE} — agent memory systems, eval/grading loops, orchestration patterns, context-rot mitigation, reflexion/self-improvement, scheduled autonomous runs. What concretely would upgrade this hub's architecture (it already has: a self-improve grader, dated session handoffs, a 40%-context rule, workflow orchestration, team/memory.md)? Cite.` },
]
const frontier = await parallel(domains.map(d => () => agent(`${GUARD}

PRIOR-PASS BRIEF (do NOT re-surface things already decided here):
${(recall || '(recall unavailable)').slice(0, 3500)}

TASK (Frontier research — domain: ${d.id}). Focus area for this run: ${FOCUS}. ${d.q}
Use firecrawl_search / WebSearch / WebFetch. RETURN: 5-10 findings, each = {what's new, why it matters to THIS hub, cheapest way to act on it, source URL+date}. Lead with the 3 highest-leverage. Mark anything that updates/contradicts an existing hub assumption.`, { label: `frontier:${d.id}`, phase: 'Frontier research' })))

// ----------------------------------------------------------------- Asset re-eval
phase('Asset re-eval')
const assetEval = await agent(`${GUARD}

PRIOR-PASS BRIEF (asset inventory + live data are in here):
${(recall || '(recall unavailable)').slice(0, 4000)}

TASK (Asset re-evaluation). For EVERY built engine + skill in the hub, judge: is it delivering value? how do we extract MORE from it? is it UNDERUSED (built but rarely run / not wired into the daily refresh / no outputs consumed)? Cross-reference the live grade data. Specifically assess the things built for Elijah recently: metrics2026, watchtime_ideator, viral-radar, news-radar, content-intel-2026, self-improve, auto-clip (+ library/facetrack/tighten/caption), trial_ab, viral_teardown, broll_planner, artifacial-ad-ideator, live-software-review, carousel-builder, comment-triage, niche-intel, weekly-content-plan. You may RUN a read-only engine via PowerShell to see its current output if useful.
RETURN: (A) ASSET-VALUE TABLE: asset | value delivered (high/med/low/unknown) | how to get MORE from it | underused? (B) "ACTIVATE THESE" — the top 5 already-built things that are underused and would pay off if wired into the daily routine or actually run. (C) "RETIRE/MERGE?" — anything redundant or not worth maintaining.`, { label: 'asset-reeval', phase: 'Asset re-eval' })

// ----------------------------------------------------------------- Synthesize
phase('Synthesize')
const synthesis = await agent(`${GUARD}

TASK (Synthesize the level-up pass into ONE dated DRAFT plan). Inputs below: the recall brief, 5 frontier-research results, and the asset re-eval. Write docs/plans/${DATE}-level-up.md (UTF-8). Structure:
- "# Level-Up Pass — ${DATE}" + a 6-line TL;DR (the single highest-leverage move + the 3 themes).
- "## 1. New things to TRY" — net-new practices/strategies/formats from the frontier sweep. Table: Idea | Why now (cited) | Cheapest first slice | Tier {Do-now / Later / Skip} | Composes-with existing asset.
- "## 2. BETTER use of what we already have" — from the asset re-eval: the underused assets to activate + how to extract more. Table: Asset | Current value | Lever to get more | Effort.
- "## 3. New TOOLS / repos / MCPs to add" — ADD/WATCH/SKIP table with license/cost/friction + cheapest integration path.
- "## 4. Architecture / anti-rot upgrades" — agent-practice improvements for the hub itself.
- "## Suggested order (leverage / effort)" — numbered 1..N, with the ⚑ Elijah-gated ones separated.
- "## Sources" — the key cited URLs+dates.
Apply the hub's lessons: cheapest-slice over grand build; propose-only (NEVER apply to a production engine); split at the measure/generate seam; verify an API exposes a named field before promising it. Don't re-propose anything in the recall's DO-NOT-REPEAT list (note it as "still pending" instead).
THEN: (a) append/create docs/LEVEL-UP-LOG.md — a one-line dated index entry linking this pass + its top recommendation; (b) prepend ONE dated learning to team/memory.md (match its "## YYYY-MM-DD — title" newest-first format).
RETURN: the TL;DR + the numbered suggested-order list (this is what the user sees first).

=== RECALL BRIEF ===
${(recall || '(none)').slice(0, 2500)}

=== FRONTIER FINDINGS ===
${domains.map((d, i) => `--- ${d.id} ---\n${(frontier[i] || '(none)').slice(0, 1800)}`).join('\n\n')}

=== ASSET RE-EVAL ===
${(assetEval || '(none)').slice(0, 2500)}`, { label: 'synthesize', phase: 'Synthesize' })

return {
  date: DATE,
  recall_summary: (recall || '').slice(0, 600),
  frontier: domains.map((d, i) => ({ id: d.id, top: (frontier[i] || 'NULL').slice(0, 350) })),
  asset_reeval: (assetEval || '').slice(0, 700),
  synthesis: (synthesis || '').slice(0, 1600),
}
