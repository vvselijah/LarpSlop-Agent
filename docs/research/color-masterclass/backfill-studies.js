export const meta = {
  name: 'backfill-studies',
  description: 'Backfill the 3 masterclass studies that failed on transient rate-limits (read transcript + frames, structured output).',
  phases: [{ title: 'Study', detail: '3 vision agents' }],
}

const BASE = 'C:/Users/elija/OneDrive/Desktop/ai agent team/docs/research/color-masterclass/raw'
const VIDEOS = [
  { slug: 'cullen-master-scopes', note: 'Cullen Kelly - Master Scopes Inside DaVinci', category: 'scopes', authority: 'Cullen Kelly, 31K views (HIGH authority)' },
  { slug: 'mostyn-perfect-node-tree', note: 'Darren Mostyn - My Perfect Node Tree (ResolveCon)', category: 'nodes', authority: 'Darren Mostyn, 13K views (HIGH authority)' },
  { slug: '2hr-beginner-course', note: 'How To Color Grade for Beginners (2hr)', category: 'fundamentals', authority: 'Ragib Choudhury, 159K views' },
].map(v => ({ ...v, transcriptPath: `${BASE}/${v.slug}/transcript.txt`, framesDir: `${BASE}/${v.slug}/frames` }))

const VIDEO_SCHEMA = {
  type: 'object',
  required: ['source', 'overview', 'orderOfOperations', 'scopes', 'primaries', 'teachingPoints'],
  properties: {
    source: { type: 'string' }, framesRead: { type: 'number' }, authorityNote: { type: 'string' }, overview: { type: 'string' },
    orderOfOperations: { type: 'array', items: { type: 'string' } },
    nodeTree: { type: 'string' },
    scopes: { type: 'array', items: { type: 'object', properties: { scope: { type: 'string' }, howRead: { type: 'string' }, targets: { type: 'string' } } } },
    primaries: { type: 'string' }, secondaries: { type: 'string' }, skinTone: { type: 'string' }, colorManagement: { type: 'string' }, lookDesign: { type: 'string' },
    numericSettings: { type: 'array', items: { type: 'string' } },
    keyFrames: { type: 'array', items: { type: 'object', properties: { frame: { type: 'string' }, shows: { type: 'string' } } } },
    teachingPoints: { type: 'array', items: { type: 'string' } },
    quotableClaims: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, timestamp: { type: 'string' } } } },
  },
}

phase('Study')
function studyPrompt(v) {
  const fdir = v.framesDir
  return (
    `You are a senior colorist studying a DaVinci Resolve color-grading masterclass to extract its COMPLETE methodology. Source: "${v.note}" (authority: ${v.authority}).\n\n` +
    `STEP 1 — Read the transcript (chunked via offset/limit if long):\n${v.transcriptPath}\n\n` +
    `STEP 2 — LOOK at the on-screen frames (load-bearing). Glob("${fdir}/f*.jpg"), then Read ~25-35 well-distributed frames (beginning/middle/end + any UI/scope/node change). Read the DaVinci UI: node graph, scopes, color wheels & values, curves, qualifier. Report framesRead.\n\n` +
    `STEP 3 — Synthesize what is TAUGHT (audio + what you SEE): order of ops, node tree, scopes + target numbers, primaries (with on-screen values), secondaries, skin-tone line, color management, look design. keyFrames = 3-8 best teaching frames + what each shows. numericSettings = values actually seen. Structured output only.`
  )
}
const studies = (await parallel(VIDEOS.map(v => () =>
  agent(studyPrompt(v), { label: 'study:' + v.slug, phase: 'Study', schema: VIDEO_SCHEMA })
    .then(r => r ? { ...r, slug: v.slug, authority: v.authority } : null)
))).filter(Boolean)
log(`Backfilled ${studies.length}/${VIDEOS.length}`)
return { studies }
