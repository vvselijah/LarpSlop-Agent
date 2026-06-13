# RESEARCH-STACK-SETUP — exactly what Elijah does to enable the deep-research stack

*Created 2026-06-13. The stack is being validated by a `research-lean` run; this list covers the
near-certain core (search + fetch). Reranker + vector-cache specifics get appended once research
confirms them. Claude wires all the plumbing — your only job is the 3 free signups + `setx`.*

## Your part: get 3 free API keys (~2 min each), then `setx` them

| # | Tool | Sign up at | Free tier | After signup |
|---|---|---|---|---|
| 1 | **Exa** (semantic search) | exa.ai → Dashboard → API Keys | free trial credits | copy the API key |
| 2 | **Tavily** (LLM search) | tavily.com → Dashboard → API Keys | ~1,000 credits/mo free | copy the API key (starts `tvly-`) |
| 3 | **Firecrawl** (deep crawl/JS) | firecrawl.dev → Dashboard → API Keys | 1,000 pages/mo free | copy the API key (starts `fc-`) |

**Jina Reader (free fetch workhorse) needs NO key** to start — Claude wires it key-free. (Optional: a free jina.ai key raises rate limits; add later if needed.)

### Then run these (one per key you got) in PowerShell:
```powershell
setx EXA_API_KEY        "your_exa_key_here"
setx TAVILY_API_KEY     "your_tavily_key_here"
setx FIRECRAWL_API_KEY  "your_firecrawl_key_here"
```
Then **fully restart Claude Code** (env vars only load on a fresh start — same as the Instagram token).

## Claude's part (after you have the keys)
1. Fetch each tool's *current* official MCP config (verify-first — no guessing) and add `exa`, `tavily`,
   `firecrawl` to workspace `.mcp.json` with `${EXA_API_KEY}` / `${TAVILY_API_KEY}` / `${FIRECRAWL_API_KEY}` placeholders + the keyless Jina reader.
2. Wire `research-lean.js` to PREFER Exa/Tavily search + Firecrawl/Jina fetch, with WebSearch/WebFetch as graceful fallback (never hard-breaks).
3. Add the reranker + local vector-cache (the force-multipliers) once the research confirms which — likely a small Python module in the hub + one more key (Cohere or Jina rerank) or fully local (LanceDB, no key).
4. Test live on a real question and show you it's actually going deeper.

## Research verdict (research-lean run wf_7efc13c4, 2026-06-13 — and the throttle fix WORKED: 36 agents, clean full synthesis, zero rate-limit failures)

- **Exa + Tavily are complementary, not redundant** — run both. Exa = neural-embedding semantic discovery; Tavily = AI-agent/RAG with pre-cleaned summarized results. Both ~1,000 free units/mo. (Tavily was acquired by Nebius Feb 2026; still operational.)
- **Fetch: Firecrawl (paid, JS/multi-page/anti-bot) + Jina (free, 10M tokens, single-page, no anti-bot bypass) is cost-optimal** — confirmed.
- **Official MCP servers confirmed for Exa, Brave, Firecrawl.** Tavily has its own MCP too (`tavily-mcp`). Jina is keyless via `r.jina.ai` (wired in the research scripts, not as an MCP).
- **Brave Search API** topped one agent benchmark but **removed its free tier for new users** (~$5/mo) → **skip for now**, optional later.
- **Reranker + local vector cache = add LAST, and they're optional here.** Confirmed as good general practice, BUT an open question the research raised is sharp: *with Claude's 1M context, a reranker matters less* than in small-context RAG (Claude can just read more sources directly). So: **LanceDB local cache = yes** (free, no key, compounding memory); **reranker = measure first, add only if token efficiency demands it.**
- **Unified alternative considered:** `mcp-omnisearch` (one server, Exa+Tavily+Brave+Firecrawl behind 4 tools, runs with any subset of keys) — elegant, but needs a local `pnpm` build vs the hub's all-`npx` pattern. **Decision: official npx MCPs** (more robust, no build step); omnisearch is the fallback if one-server is preferred.

**Final stack:** Exa MCP + Tavily MCP (search) · Firecrawl MCP + keyless Jina (fetch) · LanceDB local cache (memory) · reranker only if measured-worthwhile. **Your 3 keys unchanged: Exa, Tavily, Firecrawl.**

## Status (updated 2026-06-13)
- [x] Elijah: provided Exa / Tavily / Firecrawl keys → Claude stored them via `setx` (User env)
- [x] Claude: wired `.mcp.json` — `exa` (`exa-mcp-server` v3.2.1), `tavily` (`tavily-mcp` v0.2.20), `firecrawl` (`firecrawl-mcp` v3.20.4), all via `npx -y` with `${VAR}` placeholders
- [x] Claude: wired `research-lean.js` to PREFER Exa/Tavily search + Firecrawl/Jina(`r.jina.ai`) fetch, WebSearch/WebFetch fallback
- [ ] **Elijah: RESTART Claude Code** — MCP servers + env vars only load on a fresh start (the 3 new servers are inert until then)
- [ ] Claude: after restart, TEST live (confirm `mcp__exa__*` / `mcp__tavily__*` / `mcp__firecrawl__*` tools appear and work) + add **LanceDB** local cache (free, no key — the "remember it forever" layer)
- [ ] reranker: **deferred** — optional given Claude's 1M context; add only if measured worthwhile
