export const meta = {
  name: 'research-lean',
  description: 'Throttle-safe deep research: fan-out search + extract, then LIGHT batched verification (≤6 concurrent verify agents, not 75). Use instead of the built-in deep-research for most surveys; reserve the heavy 3-vote version for genuinely adversarial questions. See docs/RESEARCH-PROTOCOL.md.',
  phases: [
    { title: 'Scope', detail: 'decompose into 4 angles' },
    { title: 'Search', detail: '4 parallel searchers' },
    { title: 'Fetch', detail: 'batched extract (≤4 concurrent)' },
    { title: 'Verify', detail: 'top 8 claims × 2 votes, batched ≤6 concurrent' },
    { title: 'Synthesize', detail: 'merge + cite' },
  ],
}

// ── Tuning (the fix): far smaller verify burst than deep-research's 25×3=75 ──
const ANGLES = 4
const MAX_FETCH = 14
const MAX_VERIFY_CLAIMS = 8
const VOTES = 2
const VERIFY_BATCH = 3          // claims per batch → ≤ VERIFY_BATCH*VOTES = 6 concurrent
const FETCH_BATCH = 4

// ── Helpers ──
// Retry-once safety net: a null usually means a transient throttle; give it
// one more attempt after sibling work has drained.
async function tryAgent(prompt, opts) {
  const r = await agent(prompt, opts)
  if (r !== null && r !== undefined) return r
  return await agent(prompt, opts)
}
// Run items in SEQUENTIAL batches of `size`, each batch in parallel. This caps
// sustained concurrency (the throttle trigger) without losing throughput.
async function batched(items, size, fn) {
  const out = []
  for (let i = 0; i < items.length; i += size) {
    const res = await parallel(items.slice(i, i + size).map((it, j) => () => fn(it, i + j)))
    out.push(...res)
  }
  return out
}

const SCOPE_SCHEMA = {
  type: 'object', required: ['angles'],
  properties: { angles: { type: 'array', minItems: 3, maxItems: 5, items: {
    type: 'object', required: ['label', 'query'],
    properties: { label: { type: 'string' }, query: { type: 'string' } } } } },
}
const SEARCH_SCHEMA = {
  type: 'object', required: ['results'],
  properties: { results: { type: 'array', maxItems: 5, items: {
    type: 'object', required: ['url', 'title'],
    properties: { url: { type: 'string' }, title: { type: 'string' },
      relevance: { enum: ['high', 'medium', 'low'] } } } } },
}
const EXTRACT_SCHEMA = {
  type: 'object', required: ['claims', 'sourceQuality'],
  properties: { sourceQuality: { enum: ['primary', 'secondary', 'blog', 'forum', 'unreliable'] },
    claims: { type: 'array', maxItems: 5, items: {
      type: 'object', required: ['claim', 'quote'],
      properties: { claim: { type: 'string' }, quote: { type: 'string' },
        importance: { enum: ['central', 'supporting', 'tangential'] } } } } },
}
const VERDICT_SCHEMA = {
  type: 'object', required: ['refuted', 'evidence'],
  properties: { refuted: { type: 'boolean' }, evidence: { type: 'string' },
    confidence: { enum: ['high', 'medium', 'low'] } },
}
const REPORT_SCHEMA = {
  type: 'object', required: ['summary', 'findings'],
  properties: { summary: { type: 'string' },
    findings: { type: 'array', items: {
      type: 'object', required: ['claim', 'confidence', 'sources'],
      properties: { claim: { type: 'string' }, confidence: { enum: ['high', 'medium', 'low'] },
        sources: { type: 'array', items: { type: 'string' } }, evidence: { type: 'string' } } } },
    caveats: { type: 'string' }, openQuestions: { type: 'array', items: { type: 'string' } } },
}

const QUESTION = (typeof args === 'string' && args.trim()) || ''
if (!QUESTION) return { error: "Pass the question as args: Workflow({scriptPath, args: '<question>'})." }

// ── Scope ──
phase('Scope')
const scope = await tryAgent(
  `Decompose this research question into ${ANGLES} complementary web-search angles ` +
  `(e.g. primary/official · practitioner · contrarian · recent). Make each query specific.\n\n` +
  `Question: ${QUESTION}\n\nStructured output only.`,
  { label: 'scope', schema: SCOPE_SCHEMA })
if (!scope) return { error: 'Scope failed (likely throttle). Try again solo or use targeted WebFetches.' }
log('Angles: ' + scope.angles.map(a => a.label).join(', '))

// ── Search (parallel over angles — only ~4 agents, safe) ──
phase('Search')
const searched = (await parallel(scope.angles.map(a => () =>
  tryAgent(
    `Web Searcher — angle "${a.label}". Question: "${QUESTION}". Search for: ${a.query}\n` +
    `TOOL PREFERENCE: if an Exa or Tavily MCP search tool is available (find via ToolSearch keyword "exa" or "tavily"), use it — higher-signal, AI-tuned results; else use WebSearch.\n` +
    `Return the top 3-5 results most relevant to the ORIGINAL question. Skip SEO spam.\n\nStructured output only.`,
    { label: 'search:' + a.label, phase: 'Search', schema: SEARCH_SCHEMA })
    .then(r => r ? { angle: a.label, results: r.results } : null)
))).filter(Boolean)

// dedup by normalized URL, cap to MAX_FETCH
const seen = new Set()
const sources = []
for (const s of searched) {
  for (const r of (s.results || [])) {
    let key = r.url.toLowerCase()
    try { const u = new URL(r.url); key = (u.hostname.replace(/^www\./, '') + u.pathname.replace(/\/$/, '')).toLowerCase() } catch {}
    if (seen.has(key) || sources.length >= MAX_FETCH) continue
    seen.add(key); sources.push({ ...r, angle: s.angle })
  }
}
log('Fetching ' + sources.length + ' unique sources (batched ' + FETCH_BATCH + ')')

// ── Fetch + extract (batched ≤4 concurrent) ──
phase('Fetch')
const fetched = (await batched(sources, FETCH_BATCH, src => {
  let host = 'src'; try { host = new URL(src.url).hostname.replace(/^www\./, '') } catch {}
  return tryAgent(
    `Source Extractor. Question: "${QUESTION}". Retrieve this URL and extract 2-5 FALSIFIABLE claims ` +
    `that bear on the question, each with a direct supporting quote; rate source quality.\n` +
    `FETCH PREFERENCE: for JS-heavy/blocked/deep pages, prefer a Firecrawl MCP tool if available (ToolSearch "firecrawl"), or get clean free text by WebFetching "https://r.jina.ai/${src.url}" (Jina reader); else plain WebFetch.\n` +
    `If fetch fails/irrelevant, return claims:[] sourceQuality:"unreliable".\n**URL:** ${src.url}\n\nStructured output only.`,
    { label: 'fetch:' + host, phase: 'Fetch', schema: EXTRACT_SCHEMA })
    .then(ext => ext ? { url: src.url, quality: ext.sourceQuality,
      claims: ext.claims.map(c => ({ ...c, sourceUrl: src.url, sourceQuality: ext.sourceQuality })) } : null)
})).filter(Boolean)

const impRank = { central: 0, supporting: 1, tangential: 2 }
const qualRank = { primary: 0, secondary: 1, blog: 2, forum: 3, unreliable: 4 }
const claims = fetched.flatMap(s => s.claims)
  .sort((a, b) => (impRank[a.importance] ?? 1) - (impRank[b.importance] ?? 1) || (qualRank[a.sourceQuality] - qualRank[b.sourceQuality]))
  .slice(0, MAX_VERIFY_CLAIMS)
log('Extracted ' + fetched.flatMap(s => s.claims).length + ' claims → verifying top ' + claims.length)

if (!claims.length) return { question: QUESTION, summary: 'No claims extracted.', findings: [],
  sources: fetched.map(s => ({ url: s.url, quality: s.quality })) }

// ── Verify (THE FIX: batched, ≤6 concurrent, 2 votes) ──
phase('Verify')
const voted = await batched(claims, VERIFY_BATCH, claim =>
  parallel(Array.from({ length: VOTES }, (_, v) => () =>
    tryAgent(
      `Adversarial Verifier (${v + 1}/${VOTES}). Be skeptical; try to REFUTE.\nQuestion: ${QUESTION}\n` +
      `Claim: "${claim.claim}"\nSource: ${claim.sourceUrl} (${claim.sourceQuality})\nQuote: "${claim.quote}"\n` +
      `WebSearch for contradicting evidence. refuted=true if unsupported/contradicted/low-quality-for-strength/outdated/marketing. ` +
      `Default refuted=true if uncertain.\n\nStructured output only.`,
      { label: 'v' + v + ':' + claim.claim.slice(0, 32), phase: 'Verify', schema: VERDICT_SCHEMA })
  )).then(vs => {
    const valid = vs.filter(Boolean)
    const refuted = valid.filter(x => x.refuted).length
    const survives = valid.length >= 1 && refuted < VOTES   // killed only if ALL valid votes refute
    log('"' + claim.claim.slice(0, 46) + '…": ' + (valid.length - refuted) + '-' + refuted + (survives ? ' ✓' : ' ✗'))
    return { ...claim, valid, refuted, survives }
  }))

const confirmed = voted.filter(c => c.survives)
const killed = voted.filter(c => !c.survives)
log('Verify done: ' + confirmed.length + ' confirmed, ' + killed.length + ' killed')

// ── Synthesize ──
phase('Synthesize')
const block = confirmed.map((c, i) =>
  `### [${i}] ${c.claim}\nSource: ${c.sourceUrl} (${c.sourceQuality}) · vote ${c.valid.length - c.refuted}-${c.refuted}\nQuote: "${c.quote}"`).join('\n\n')
const report = await tryAgent(
  `Synthesize a research report answering: ${QUESTION}\n\n${confirmed.length} claims passed light verification:\n${block}\n\n` +
  `Merge duplicates, group into findings (each with confidence + sources), write a 3-5 sentence summary, ` +
  `note caveats and 2-4 open questions.\n\nStructured output only.`,
  { label: 'synthesize', schema: REPORT_SCHEMA })

return report
  ? { question: QUESTION, ...report,
      refuted: killed.map(c => ({ claim: c.claim, source: c.sourceUrl })),
      sources: fetched.map(s => ({ url: s.url, quality: s.quality })),
      stats: { angles: scope.angles.length, sources: fetched.length, verified: voted.length, confirmed: confirmed.length } }
  : { question: QUESTION, summary: 'Synthesis skipped — returning confirmed claims raw.',
      findings: [], confirmed: confirmed.map(c => ({ claim: c.claim, source: c.sourceUrl, quote: c.quote })),
      sources: fetched.map(s => ({ url: s.url, quality: s.quality })) }
