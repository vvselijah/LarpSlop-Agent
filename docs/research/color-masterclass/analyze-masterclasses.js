export const meta = {
  name: 'analyze-masterclasses',
  description: 'Deeply analyze the acquired DaVinci color-grading masterclasses (read each video\'s transcript + ~50 on-screen frames), extract the real methodology, cross-reference for consensus, and synthesize an engine-facing best-workflow + a zero-to-hero teaching outline.',
  phases: [
    { title: 'Study', detail: 'one vision agent per video: read transcript + frames' },
    { title: 'Consensus', detail: 'cross-reference: universal truths vs disputed' },
    { title: 'Synthesize', detail: 'engine methodology + teaching guide outline' },
  ],
}

// Self-contained: paths derived from slug (no args dependency). Forward slashes (Read/Glob accept them on Windows).
const BASE = 'C:/Users/elija/OneDrive/Desktop/ai agent team/docs/research/color-masterclass/raw'
const VIDEOS = [
  { slug: 'mostyn-color-page-intro', note: 'Darren Mostyn - NEW to DaVinci? Color Grading', category: 'fundamentals', authority: 'Darren Mostyn, 545K views (HIGH)' },
  { slug: 'beginners-guide-grading', note: "Beginner's Guide to Colour Grading", category: 'fundamentals', authority: 'Bill Blakely, 250 views (LOW - weight lightly)' },
  { slug: '2hr-beginner-course', note: 'How To Color Grade for Beginners (2hr)', category: 'fundamentals', authority: 'Ragib Choudhury, 159K views' },
  { slug: 'mostyn-read-scopes', note: 'How Pro Colorists Read Scopes ft Darren Mostyn', category: 'scopes', authority: 'ft Darren Mostyn, 7K views' },
  { slug: 'cullen-master-scopes', note: 'Cullen Kelly - Master Scopes Inside DaVinci', category: 'scopes', authority: 'Cullen Kelly, 31K views (HIGH authority)' },
  { slug: 'mostyn-perfect-node-tree', note: 'Darren Mostyn - My Perfect Node Tree (ResolveCon)', category: 'nodes', authority: 'Darren Mostyn, 13K views (HIGH authority)' },
  { slug: 'best-node-tree-any-camera', note: 'BEST Node Tree for ANY Camera (BBC pro)', category: 'nodes', authority: 'Darren Mostyn, 561K views (HIGH)' },
  { slug: 'grading-too-complicated', note: 'Has Colour Grading Got Too Complicated? 5 PRO Fundamentals', category: 'color-mgmt', authority: 'Darren Mostyn, 36K views (HIGH authority)' },
  { slug: 'cullen-36-project-settings', note: 'Cullen Kelly - 36 Project Settings', category: 'color-mgmt', authority: 'Cullen Kelly, 38K views (HIGH authority)' },
  { slug: 'cullen-contrast-cinematographer', note: 'Cullen Kelly - contrast secrets for cinematographers', category: 'primaries', authority: 'Cullen Kelly, 40K views (HIGH authority)' },
  { slug: 'qualifier-tricks', note: 'BEST Pro Colorist Qualifier Tricks', category: 'secondaries', authority: 'Edou Hoekstra, 3K views' },
  { slug: 'frenchie-masterclass', note: 'Frenchie - Pro Colorist Reveals all (MASTERCLASS)', category: 'look-design', authority: 'Frenchie, 7K views' },
  { slug: 'mullins-grading-philosophy', note: 'Mitchell Mullins - Color Grading Mastery philosophy', category: 'look-design', authority: 'Mitchell Mullins, 137K views' },
  { slug: 'film-emulation-16-35mm', note: 'Emulating 16mm/35mm Film', category: 'look-design', authority: 'serr, 836K views (HIGH)' },
].map(v => ({ ...v, transcriptPath: `${BASE}/${v.slug}/transcript.txt`, framesDir: `${BASE}/${v.slug}/frames` }))

const VIDEO_SCHEMA = {
  type: 'object',
  required: ['source', 'overview', 'orderOfOperations', 'scopes', 'primaries', 'teachingPoints'],
  properties: {
    source: { type: 'string' },
    framesRead: { type: 'number', description: 'how many of the ~50 frames you actually opened with Read' },
    authorityNote: { type: 'string' },
    overview: { type: 'string' },
    orderOfOperations: { type: 'array', items: { type: 'string' }, description: 'the staged grading workflow shown, in order' },
    nodeTree: { type: 'string', description: 'node structure: how many nodes, serial/parallel/layer, what each node does' },
    scopes: { type: 'array', items: { type: 'object', properties: {
      scope: { type: 'string' }, howRead: { type: 'string' }, targets: { type: 'string' } } } },
    primaries: { type: 'string', description: 'lift/gamma/gain/offset, contrast+pivot, log vs primary wheels, technique + any on-screen values' },
    secondaries: { type: 'string', description: 'qualifier, power windows, HSL, tracking; skin isolation' },
    skinTone: { type: 'string', description: 'vectorscope skin line, target hue/angle, technique' },
    colorManagement: { type: 'string', description: 'RCM / ACES / CST, working color space, project settings, input/output transforms' },
    lookDesign: { type: 'string', description: 'creative look: LUTs, film emulation, split-tone, hue-vs-hue, saturation discipline' },
    numericSettings: { type: 'array', items: { type: 'string' }, description: 'concrete numeric values SEEN ON SCREEN (e.g. "Pivot 0.435", "Contrast 1.15", "Lift -0.01")' },
    keyFrames: { type: 'array', items: { type: 'object', properties: {
      frame: { type: 'string', description: 'the frame filename, e.g. f021.jpg' }, shows: { type: 'string' } } },
      description: 'the 3-8 most teaching-valuable screenshots and what each shows' },
    teachingPoints: { type: 'array', items: { type: 'string' }, description: 'zero-to-hero pedagogy: how a beginner should understand each concept' },
    quotableClaims: { type: 'array', items: { type: 'object', properties: {
      claim: { type: 'string' }, timestamp: { type: 'string' } } } },
  },
}

const CONSENSUS_SCHEMA = {
  type: 'object',
  required: ['universalTruths', 'canonicalWorkflow', 'disputed', 'engineImplications'],
  properties: {
    universalTruths: { type: 'array', items: { type: 'object', required: ['principle', 'sourceCount'], properties: {
      principle: { type: 'string' }, sourceCount: { type: 'number' }, sources: { type: 'array', items: { type: 'string' } },
      detail: { type: 'string' } } }, description: 'principles >=2 independent sources agree on, with how-many' },
    canonicalWorkflow: { type: 'array', items: { type: 'object', properties: {
      step: { type: 'string' }, does: { type: 'string' }, scopeCheck: { type: 'string' }, nodeOrTool: { type: 'string' } } },
      description: 'the consensus end-to-end grading order, stage by stage' },
    nodeTreeConsensus: { type: 'string', description: 'the consensus node-tree structure (and where authorities differ)' },
    scopeTargets: { type: 'array', items: { type: 'object', properties: {
      metric: { type: 'string' }, target: { type: 'string' }, source: { type: 'string' } } } },
    disputed: { type: 'array', items: { type: 'string' }, description: 'where authorities genuinely disagree' },
    singleSource: { type: 'array', items: { type: 'string' }, description: 'interesting but only one source — treat as opinion' },
    engineImplications: { type: 'array', items: { type: 'string' }, description: 'what each consensus truth means for our headless Python/ffmpeg color engine' },
  },
}

phase('Study')
log(`Studying ${VIDEOS.length} masterclasses (transcript + on-screen frames each)`)
function studyPrompt(v) {
  const fdir = v.framesDir || ''
  return (
    `You are a senior colorist + film-color scientist studying a DaVinci Resolve color-grading masterclass to extract its COMPLETE methodology for a knowledge base. ` +
    `Source: "${v.note}" (category: ${v.category}; authority: ${v.authority}).\n\n` +
    `STEP 1 — Read the transcript (what is said). It may be long; if so, read it in a few chunks via Read offset/limit rather than many tiny reads:\n${v.transcriptPath}\n\n` +
    `STEP 2 — Actually LOOK at the on-screen frames (this is the load-bearing step — the visuals carry the real teaching). The folder has ~50 JPGs (f001.jpg ... f050.jpg):\n${fdir}\n` +
    `Use Glob("${fdir}/f*.jpg") to list them, then Read a broad, well-distributed set across the whole video (aim for ~25-40 of them; you do NOT have to open all 50, but cover beginning/middle/end and any frame where the UI/scopes/node-graph changes). Read the DaVinci UI: node graph, scopes (waveform/parade/vectorscope/histogram), color wheels & values, curves, qualifier. Report framesRead = how many you opened.\n\n` +
    `STEP 3 — Synthesize what is TAUGHT (combine audio + what you SEE on screen). Be concrete and numeric: order of operations, node tree structure, which scopes are used and how they're read (with target numbers), primaries technique (lift/gamma/gain/offset, contrast, pivot, log vs primary wheels — read actual values off the wheels/sliders), secondaries (qualifier/windows/skin), skin-tone-line method, color management (RCM/ACES/CST + project settings), look design (LUTs/film emulation/split-tone). ` +
    `For keyFrames, name the 3-8 specific frame files (e.g. f021.jpg) that best teach a concept and say what each shows. numericSettings = only values you actually saw on screen. Distinguish demonstrated vs generic talk.\n\nStructured output only.`
  )
}
const studies = (await parallel(VIDEOS.map(v => () =>
  agent(studyPrompt(v), { label: 'study:' + v.slug, phase: 'Study', schema: VIDEO_SCHEMA })
    .then(r => r ? { ...r, slug: v.slug, authority: v.authority } : null)
))).filter(Boolean)
log(`Studied ${studies.length}/${VIDEOS.length} (framesRead avg ${studies.length ? Math.round(studies.reduce((a, s) => a + (s.framesRead || 0), 0) / studies.length) : 0})`)
if (!studies.length) { return { error: 'no studies produced', requested: VIDEOS.length } }

phase('Consensus')
const digest = studies.map(s =>
  `### ${s.slug} (${s.authorityNote || s.authority || ''}) [framesRead=${s.framesRead || '?'}]\n` +
  `OVERVIEW: ${s.overview}\n` +
  `ORDER: ${(s.orderOfOperations || []).join(' -> ')}\n` +
  `NODES: ${s.nodeTree || ''}\n` +
  `SCOPES: ${(s.scopes || []).map(x => `${x.scope}: ${x.howRead} [${x.targets || ''}]`).join(' | ')}\n` +
  `PRIMARIES: ${s.primaries || ''}\n` +
  `SECONDARIES: ${s.secondaries || ''}\n` +
  `SKIN: ${s.skinTone || ''}\n` +
  `COLOR MGMT: ${s.colorManagement || ''}\n` +
  `LOOK: ${s.lookDesign || ''}\n` +
  `NUMBERS: ${(s.numericSettings || []).join('; ')}\n`
).join('\n\n')
log('Cross-referencing for consensus (what >=2 authorities agree on)')
const consensus = await agent(
  `You are the lead colorist consolidating ${studies.length} analyzed DaVinci color-grading masterclasses into the authoritative consensus. ` +
  `Weight by authority (Darren Mostyn + Cullen Kelly are the top references; a 250-view video is low-weight). ` +
  `Find what MULTIPLE independent sources agree on (the load-bearing truths), the canonical end-to-end workflow with scope checks, the consensus node-tree, the numeric scope targets, where authorities genuinely DISAGREE, and single-source opinions. ` +
  `Then translate each consensus truth into an implication for a HEADLESS Python + ffmpeg auto-color engine (no DaVinci at runtime) that auto-corrects + grades footage. \n\nANALYSES:\n${digest}\n\nStructured output only.`,
  { label: 'consensus', phase: 'Consensus', schema: CONSENSUS_SCHEMA, effort: 'high' })
log(`Consensus: ${(consensus.universalTruths || []).length} universal truths, ${(consensus.canonicalWorkflow || []).length} workflow steps`)

phase('Synthesize')
const synth = await agent(
  `You are writing two things from the consensus below, for (a) an autonomous color-grading AGENT and (b) a human learner going zero-to-hero.\n\n` +
  `CONSENSUS:\n${JSON.stringify(consensus, null, 2)}\n\n` +
  `Produce a detailed markdown document with these sections: \n` +
  `1. "The professional color-grading method (consensus)" — the definitive end-to-end workflow, stage by stage, with the scope checks and target numbers, written so an engineer could implement it.\n` +
  `2. "Node tree + why" — the consensus structure and the reasoning.\n` +
  `3. "Scopes — how pros actually read them" — waveform/parade/vectorscope/histogram, with target numbers.\n` +
  `4. "What this means for our headless engine" — concrete changes/validations for a Python+ffmpeg auto-grader (map each principle to code: WB, exposure to mid-grey, filmic tone/contrast, skin line, saturation discipline, look design, color management/log handling).\n` +
  `5. "Zero-to-hero teaching outline" — the chapter list for a sellable masterclass (beginner setup -> scopes -> primaries -> secondaries -> skin -> look -> film emulation -> delivery), each chapter with its key teaching points.\n` +
  `Be concrete, numeric, and faithful to the consensus. Return the FULL markdown as the message (not a schema).`,
  { label: 'synthesize', phase: 'Synthesize', effort: 'high' })

return { consensus, studies, synthesisMarkdown: synth, stats: { studied: studies.length, requested: VIDEOS.length } }
