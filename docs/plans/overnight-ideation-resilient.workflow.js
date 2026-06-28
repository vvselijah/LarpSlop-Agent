// Resilient overnight IDEATION + COMPILE workflow.
// Launch with:  Workflow({ scriptPath: "docs/plans/overnight-ideation-resilient.workflow.js" })
// Optionally prefix your message with a token budget (e.g. "+600k") so the loop self-throttles.
//
// WHY THIS EXISTS: the first deep run (wf_c9ab2d30-b37) hit the ACCOUNT session limit mid-ideation
// because it re-did 5 rounds of web research (~271 agents). The research is now DONE and saved to
// team/state-of-play.md, so this run SKIPS research entirely and only ideates + compiles = far fewer
// agents, no slow web fetches, fits under the cap.
//
// RESILIENCE BUILT IN:
//  - budget-gated loop: if a token target is set ("+Nk"), it stops before the cap; else fixed round cap.
//  - FULL-DRAFT checkpoint to disk EVERY round (deterministic markdown -> low-effort Write), so the
//    on-disk file is always a usable deliverable, never just titles.
//  - returns ALL ideas in the result (nothing is lost even if the final compile fails).
//  - compile wrapped in try/catch -> falls back to the live draft.
//  - per-agent failures already tolerated (.filter(Boolean)).
// NOTE: account session caps reset on a clock (was 7:10am ET) and resume is SAME-SESSION-ONLY, so the
// durable continuity is these disk checkpoints + this lean design. Run it when budget is fresh.

export const meta = {
  name: 'overnight-ideation-compile',
  description: 'Rate-limit-resilient ideation + compile over the finished research: loop-until-dry idea generation with ruthless critique + per-idea vetting, full-draft checkpoints every round, returns all ideas',
  phases: [
    { title: 'Ground' },
    { title: 'Ideate' },
    { title: 'Critique' },
    { title: 'Verify-ideas' },
    { title: 'Compile' },
  ],
}

const IDEAS = { type:'object', properties:{ category:{type:'string'}, ideas:{type:'array',items:{type:'object',properties:{ title:{type:'string'}, hook:{type:'string'}, format:{type:'string'}, why:{type:'string'}, niche:{type:'string'}, effort:{type:'string'} }, required:['title','hook','format','why']}} }, required:['category','ideas'] }
const RANK = { type:'object', properties:{ category:{type:'string'}, top:{type:'array',items:{type:'object',properties:{title:{type:'string'},why:{type:'string'}},required:['title','why']}}, cut:{type:'array',items:{type:'string'}}, missing:{type:'array',items:{type:'object',properties:{title:{type:'string'},hook:{type:'string'},why:{type:'string'},format:{type:'string'},niche:{type:'string'}},required:['title','hook']}} }, required:['category','top'] }

const RESERVE = 80000
function roomLeft() { return budget.total ? budget.remaining() > RESERVE : true }
const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 40)

phase('Ground')
const ground = await agent(`Read these repo files and return a tight but COMPLETE creator brief that will ground all ideation:\n- team/state-of-play.md  (THE finished, verified 2026 content research: ~520 lines, sections 0-29, every claim tier-tagged platform-official / well-documented / marketer-claim — this is the source of truth)\n- team/profile.md and team/stats.md  (his voice, ventures, real performance numbers)\nReturn markdown covering: his voice in 2-3 sentences; ranked niches with real numbers (and the AI/Tech execution gap); what wins for him (formats, hooks, signals — share/watch-driven); the format strategy (carousel = #1 untapped saves engine, reels = reach, long-form = revenue); the verified trending THEMES worth riding right now (with their tiers); and hard constraints (never auto-post; API reels = voice/original audio only; tier every claim, no marketer numbers as fact). Be specific and faithful to state-of-play.md.`, { phase:'Ground', label:'ground:read-research' })
log('Grounded on finished research (state-of-play.md).')

phase('Ideate')
const CATS = [
  { key:'carousel-ai-tech', niche:'AI/tech value, NO product CTA' },
  { key:'carousel-money', niche:'money/finance/investing value, NO product CTA' },
  { key:'carousel-business-founder', niche:'business/startup/founder/build-in-public value, NO product CTA' },
  { key:'carousel-broad', niche:'psychology/productivity/frameworks/things-nobody-tells-you, NO product CTA' },
  { key:'carousel-contrarian', niche:'contrarian takes + storytelling carousels, NO product CTA' },
  { key:'shortform-talking', niche:'reels where Elijah talks to camera' },
  { key:'shortform-nontalking', niche:'text-on-screen / show-dont-tell / skits / faceless-friendly reels' },
  { key:'shortform-reactive', niche:'reels riding current 2026 trends/news/debates (the verified themes in the brief)' },
  { key:'longform-talking', niche:'long-form YouTube video essays / deep dives / documentary-build' },
  { key:'series-formats', niche:'recurring named series concepts across formats (high compounding)' },
]
let allIdeas = []
const seen = new Set()
let dry = 0
let rankCumulative = []
const MAX_ROUNDS = 6

function draftDoc(tag) {
  const byCat = {}
  for (const i of allIdeas) { (byCat[i.category] = byCat[i.category] || []).push(i) }
  let md = '# 2026 Content Idea Bank — LIVE DRAFT (' + (tag || '') + ')\n\n_' + allIdeas.length + ' ideas, auto-checkpointed each round. Value/info ideas, no repo or product CTA unless noted._\n\n'
  for (const c of Object.keys(byCat)) {
    md += '## ' + c + ' (' + byCat[c].length + ')\n'
    for (const i of byCat[c]) { md += '- **' + i.title + '** — ' + i.hook + (i.why ? '  _(' + i.why + ')_' : '') + '\n' }
    md += '\n'
  }
  return md
}

for (let r = 1; r <= MAX_ROUNDS && dry < 2 && roomLeft(); r++) {
  log('Ideation round ' + r + ' (' + allIdeas.length + ' ideas, spent ' + Math.round(budget.spent() / 1000) + 'k)')
  const existingByCat = {}
  for (const it of allIdeas) { (existingByCat[it.category] = existingByCat[it.category] || []).push(it.title) }
  const banks = (await parallel(CATS.map(c => () =>
    agent('Generate 8 NEW, specific content ideas for category "' + c.key + '" (' + c.niche + '). Round ' + r + '.\nGROUND (finished research + creator brief):\n' + ground + '\nDo NOT repeat or lightly reword any of these already-generated titles:\n' + JSON.stringify((existingByCat[c.key] || []).slice(0, 90)) + '\nGo deeper and fresher each round: new angles, the verified 2026 hooks/themes from the brief, contrarian or hyper-specific takes. NO generic filler. For each: title, exact HOOK (first line / slide-1 text), format, WHY it works (tie to a verified 2026 signal or his data), niche, effort (low/med/high). Distinct from one another.', { schema: IDEAS, phase:'Ideate', label:'ideate:r' + r + ':' + c.key })
  ))).filter(Boolean)
  let fresh = 0
  for (const b of banks) { for (const idea of (b.ideas || [])) { const k = norm(idea.title); if (k && !seen.has(k)) { seen.add(k); allIdeas.push(Object.assign({ category: b.category }, idea)); fresh++ } } }
  const ranks = (await parallel(CATS.map(c => () => {
    const ci = allIdeas.filter(i => i.category === c.key)
    return agent('You are a ruthless content editor. Category "' + c.key + '". Ideas:\n' + JSON.stringify(ci) + '\nGROUND:\n' + ground + '\nRank the TOP ideas (most likely to save/share/perform for Elijah, one-line why each), name weak/generic ones to CUT, and add any MISSING high-potential ideas (with hook + format + niche). Be honest and specific.', { schema: RANK, phase:'Critique', label:'critique:r' + r + ':' + c.key, effort:'medium' })
  }))).filter(Boolean)
  rankCumulative = ranks
  for (const rk of ranks) { for (const m of (rk.missing || [])) { const k = norm(m.title); if (k && !seen.has(k)) { seen.add(k); allIdeas.push({ category: rk.category, title: m.title, hook: m.hook, format: m.format || '', why: m.why || '', niche: m.niche || '', effort: '' }); fresh++ } } }
  if (fresh < 8) dry++; else dry = 0
  log('Round ' + r + ': +' + fresh + ' fresh (total ' + allIdeas.length + ')')
  await agent('Use the Write tool to overwrite the file "docs/plans/2026-06-24-content-idea-bank.md" with EXACTLY the following content (verbatim, do not summarize), then return just "ok":\n\n' + draftDoc('round ' + r), { phase:'Ideate', label:'checkpoint:r' + r, effort:'low' })
}
log('Ideation done: ' + allIdeas.length + ' ideas.')

phase('Verify-ideas')
const topTitles = new Set()
for (const rk of rankCumulative) { for (const t of (rk.top || [])) topTitles.add(norm(t.title)) }
const topIdeas = allIdeas.filter(i => topTitles.has(norm(i.title)))
const chunk = (arr, n) => { const o = []; for (let i = 0; i < arr.length; i += n) o.push(arr.slice(i, i + n)); return o }
let verdicts = []
if (topIdeas.length && roomLeft()) {
  verdicts = (await parallel(chunk(topIdeas, 5).map((grp, gi) => () =>
    agent('Adversarially vet these ' + grp.length + ' content ideas for Elijah. For EACH: is it genuinely strong + fresh (not generic), does it fit his voice + proven niches + a real 2026 signal, and is the HOOK sharp? Kill or fix the weak ones. Ideas:\n' + JSON.stringify(grp) + '\nGROUND:\n' + ground + '\nReturn a markdown list: each idea = KEEP or CUT, one-line reason, improved hook where useful.', { phase:'Verify-ideas', label:'vet:' + (gi + 1), effort:'medium' })
  ))).filter(Boolean)
}
log('Vetted ' + topIdeas.length + ' top ideas.')

phase('Compile')
let compiled = ''
try {
  compiled = await agent('Compile the FINAL content idea-bank deliverable for Elijah.\nGROUND:\n' + ground + '\nALL IDEAS (' + allIdeas.length + '):\n' + JSON.stringify(allIdeas) + '\nEDITOR RANKINGS / CUTS / GAPS:\n' + JSON.stringify(rankCumulative) + '\nTOP-IDEA ADVERSARIAL VERDICTS:\n' + verdicts.join('\n\n') + '\nProduce ONE clean, skimmable markdown doc:\n1. TL;DR — 5 biggest takeaways + a DO-THESE-FIRST shortlist (~10 ideas across formats).\n2. FORMAT STRATEGY — carousel vs short-form vs long-form: when/why each (from the ground brief, tier-tagged).\n3. TRENDING NOW — the verified themes worth riding this month.\n4. CAROUSEL IDEA BANK — curated best, grouped by niche, hook + one-line why (value/info, NO repo/product CTA).\n5. SHORT-FORM IDEA BANK — talking + non-talking + reactive, curated, hook + why.\n6. LONG-FORM + SERIES IDEA BANK — curated, angle + why.\nFavor editor-top + adversarially-kept ideas; drop the cut ones. Every idea concrete with its hook. Return ONLY the markdown.', { phase:'Compile', label:'compile:final', effort:'high' })
} catch (e) {
  compiled = draftDoc('compile-fallback')
}
return { brief: ground, compiled, ideas: allIdeas, rankings: rankCumulative, verdicts, stats: { ideas: allIdeas.length, top: topIdeas.length } }
