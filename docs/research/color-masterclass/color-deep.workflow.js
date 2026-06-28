export const meta = {
  name: 'color-masterclass-deep',
  description: 'Frame-by-frame vision analysis of color-grading masterclasses → per-video technique sheets → MERGE into synthesis_v2.md + engine_gap_map. Pass-agnostic: processes whatever slugs are in args.videos; never overwrites prior evidence.',
  whenToUse: 'Continuing the color-grading masterclass deep analysis for a new batch of videos (individuals or a playlist subset).',
  phases: [
    { title: 'Extract', detail: 'one vision agent per ~20-frame batch — read frames + aligned transcript, pull frame-cited demonstrated techniques with EXACT on-screen values' },
    { title: 'Sheet', detail: 'one agent per video synthesizes the per-video technique sheet (self-rechecks surprising numbers against the cited frame)' },
    { title: 'WriteSheet', detail: 'persist each new per-video-v2/<slug>.md (additive — never deletes existing sheets)' },
    { title: 'Merge', detail: 'fold new demonstrated evidence into synthesis_v2.md + engine_gap_map.(json|md), preserving every prior section/citation and the disputes-as-knobs structure' },
  ],
}

// args = { base: "<abs path to docs/research/color-masterclass>", videos: [ {slug, note, batches_dir, n_batches} ... ] }
// Defensive: the harness can deliver args as a JSON STRING rather than an object — parse if so.
let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const base = A.base
const videos = A.videos || []
if (!base || !videos.length) {
  throw new Error('args.base/args.videos missing — got: ' + (typeof args) + ' ' + JSON.stringify(args).slice(0, 200))
}
const EXTRACTED = base + '\\extracted'
const PERVID = base + '\\per-video-v2'

const pad2 = (n) => (n < 10 ? '0' + n : '' + n)

const TECH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    tool: { type: 'string', description: 'App/version/project/footage context visible in these frames (e.g. "DaVinci Resolve 19, color-managed, ARRI source").' },
    techniques: {
      type: 'array',
      description: 'One entry per distinct demonstrated technique or parameter visible in THIS batch. Cite the frame.',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          mmss: { type: 'string', description: 'Timestamp MM:SS from the frame header.' },
          frame: { type: 'string', description: 'Frame filename (e.g. f0042_1234.jpg).' },
          technique: { type: 'string', description: 'What is being done (concise).' },
          demonstrated_values: { type: 'string', description: 'EXACT on-screen numbers WITH their UI context (which control, which scale). e.g. "Offset wheel master 25.00 (Resolve neutral = 25, NOT a lift)", "Pivot 0.435", "Contrast 1.104", "Lift Y -0.02". Never invent a number; if unreadable say so.' },
          scope_reading: { type: 'string', description: 'Any scope/waveform/vectorscope/parade reading shown (values, where the trace sits). Empty if none.' },
          node_context: { type: 'string', description: 'Node tree / node label / stage order if visible. Empty if none.' },
          surprising: { type: 'boolean', description: 'True if the number looks scale-confused or contradicts the technique (e.g. a wheel value on a 0-100 vs -1..1 vs 1.0-centered scale) and needs a recheck.' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
        required: ['mmss', 'technique', 'demonstrated_values', 'surprising', 'confidence'],
      },
    },
  },
  required: ['techniques'],
}

const extractPrompt = (slug, note, mdPath, bi, nb) => `You are doing a rigorous frame-by-frame extraction of a DaVinci Resolve color-grading tutorial for an engine-spec corpus. Quality bar is non-negotiable: capture EXACT on-screen demonstrated values, never invent one.

Video: ${slug} — ${note}
Batch ${bi + 1}/${nb}.

STEP 1: Read this batch brief file (it lists, per kept frame: the timestamp, the absolute frame image path, and the transcript words spoken around that moment):
${mdPath}

STEP 2: Read EVERY frame image the brief lists (use the Read tool on each absolute path — they are .jpg, you will see them). Cross-reference what the screen shows against the "said:" transcript for that frame.

STEP 3: Extract the demonstrated techniques. For each, record the EXACT numbers visible on screen WITH the control + scale they belong to.

CRITICAL scale-confusion guard (this corpus has been burned by it): DaVinci's Primary wheels read **Offset neutral = 25.00**, Gain neutral = 1.00, Lift/Gamma neutral = 0.00; the wheel COLOR coordinates are a different -1..1 scale than the 0-100 numeric readouts. If you see "Offset 25" that is NEUTRAL, not a black lift. If a number's scale is ambiguous or the value seems impossible for the described move, set surprising=true and say which scale you think it is. Read scope values off the visible scale (0-1023 / IRE / %).

Only report what is actually visible/demonstrated in THESE frames. If a frame is just a talking head with no UI, skip it. Return the structured techniques.`

const sheetPrompt = (slug, note, payload) => `You are writing the per-video DEMONSTRATED-TECHNIQUE SHEET for a color-grading engine corpus, from frame-cited extractions of the video "${slug} — ${note}".

Below is the JSON of every technique extracted across all batches (each has mmss, frame, demonstrated_values, scope_reading, node_context, surprising, confidence):

${payload}

Produce a single Markdown sheet in EXACTLY this structure (match the existing corpus format):

## ${slug} — ${note}

**Tool:** <app/version/project/footage context if known>

### Workflow order
<the node-tree / stage order the colorist uses, numbered; only if demonstrated>

### Demonstrated parameters (number @ mm:ss)
- **<param>**: <exact value with control+scale> (mm:ss)
<every concrete demonstrated number, each cited mm:ss. Group sensibly.>

### Distinctive techniques / opinions
- <notable methods, rules of thumb, opinions — cited mm:ss>

### ENGINE: what a headless auto-grader should adopt
- <concrete, implementable takeaways for colorkit (correct.py / measure.py / scopes / stylize.py / match.py / tonemap.py / luts.py)>

RULES:
- Cite mm:ss on every concrete claim. Never invent a value not in the extractions.
- For any technique flagged surprising=true, you have the frame name — if you cannot confirm the value is plausible, KEEP it but append " [flag: <which scale ambiguity>]" so it is captured for human recheck rather than silently trusted or dropped.
- Be concise but complete. This sheet is the durable evidence record.

Return ONLY the markdown sheet (starting with the "## ${slug} —" line). After your reasoning, your final message IS the file content.`

phase('Extract')

const perVideo = await pipeline(
  videos,
  // STAGE 1 — fan a vision agent per batch (parallel within the video)
  async (v) => {
    const tasks = []
    for (let i = 0; i < v.n_batches; i++) {
      const mdPath = v.batches_dir + '\\b' + pad2(i) + '.md'
      tasks.push(() =>
        agent(extractPrompt(v.slug, v.note, mdPath, i, v.n_batches), {
          label: `extract:${v.slug}:b${pad2(i)}`,
          phase: 'Extract',
          schema: TECH_SCHEMA,
        })
      )
    }
    const results = await parallel(tasks)
    const ok = results.filter(Boolean)
    const techniques = ok.flatMap((r) => (r && r.techniques) ? r.techniques : [])
    const tools = ok.map((r) => r && r.tool).filter(Boolean)
    return {
      slug: v.slug,
      note: v.note,
      n_batches: v.n_batches,
      n_failed: v.n_batches - ok.length,
      tool: tools.length ? tools[0] : '',
      techniques,
    }
  },
  // STAGE 2 — synthesize the per-video sheet markdown
  async (ex) => {
    const payload = JSON.stringify({ tool: ex.tool, techniques: ex.techniques }, null, 0).slice(0, 120000)
    const sheet_md = await agent(sheetPrompt(ex.slug, ex.note, payload), {
      label: `sheet:${ex.slug}`,
      phase: 'Sheet',
    })
    const surprising = ex.techniques.filter((t) => t && t.surprising)
      .map((t) => `${ex.slug} ${t.mmss}: ${t.technique} — ${t.demonstrated_values}`)
    return { slug: ex.slug, note: ex.note, n_tech: ex.techniques.length, n_batches: ex.n_batches, n_failed: ex.n_failed, sheet_md, surprising }
  },
  // STAGE 3 — write the sheet to disk (additive; never deletes other sheets)
  async (s) => {
    const path = PERVID + '\\' + s.slug + '.md'
    const writeRes = await agent(
      `Write the following Markdown to the file ${path} (create it / overwrite only this one file). Do not modify any other file. After writing, reply with just "WROTE ${s.slug}".\n\n----- BEGIN CONTENT -----\n${s.sheet_md}\n----- END CONTENT -----`,
      { label: `write:${s.slug}`, phase: 'WriteSheet', agentType: 'general-purpose' }
    )
    return { slug: s.slug, n_tech: s.n_tech, n_batches: s.n_batches, n_failed: s.n_failed, surprising: s.surprising, wrote: !!writeRes }
  }
)

const done = perVideo.filter(Boolean)
const newSlugs = done.map((d) => d.slug)
const allSurprising = done.flatMap((d) => d.surprising || [])
const totalFailed = done.reduce((a, d) => a + (d.n_failed || 0), 0)
log(`Extracted ${done.length}/${videos.length} videos · ${done.reduce((a, d) => a + d.n_tech, 0)} techniques · ${totalFailed} batches failed · ${allSurprising.length} surprising claims`)

phase('Merge')

const mergePrompt = `You are MERGING new frame-by-frame color-grading evidence into an existing engine-spec corpus. This is additive and must be loss-free.

Files (absolute paths):
- Existing methodology:  ${EXTRACTED}\\synthesis_v2.md
- Existing gap map JSON:  ${EXTRACTED}\\engine_gap_map.json
- New per-video sheets just written (READ each):
${newSlugs.map((s) => '  - ' + PERVID + '\\' + s + '.md').join('\n')}

Newly-flagged surprising/ambiguous values to consider for the flagged_claims list:
${allSurprising.length ? allSurprising.map((x) => '  - ' + x).join('\n') : '  (none)'}

TASK:
0. CLEANUP prior incomplete-run bookkeeping FIRST: in engine_gap_map.json delete any gap_map row whose id is "pending-vision-analysis-10-videos" or whose technique starts with "MERGE BOOKKEEPING", and delete any flagged_claims entry starting with "MERGE-PROCESS FLAG"; in synthesis_v2.md remove any pending-work / "pending vision analysis" placeholder note left by a prior failed merge. Then do the real merge below.
1. Read synthesis_v2.md and engine_gap_map.json and ALL the new sheets above.
2. Produce an UPDATED synthesis_v2.md that folds the new demonstrated parameters/techniques into the existing sections where they corroborate or extend (add the new citations like "${newSlugs[0] || 'slug'} 12:34" alongside existing ones). Add a NEW numbered section only for a genuinely new technique not covered. Update the top COVERAGE note to include the newly-analyzed videos and their count. PRESERVE every existing section, citation, and the §"Disputes preserved as tunable knobs" structure — do NOT delete or weaken prior evidence; only add/extend. Keep the engine-grounding accurate.
3. Produce an UPDATED engine_gap_map.json = {"gap_map":[...], "flagged_claims":[...]}: keep all existing rows; for each, append new corroborating evidence to its "evidence" string where relevant; ADD new rows for newly-demonstrated techniques not yet mapped (fields: technique, module, status[missing|partial|present], priority[P0|P1|P2|P3], engine_change, evidence); append genuinely-new ambiguous numbers to flagged_claims (dedup against existing).
4. Regenerate engine_gap_map.md from the merged JSON, grouped by priority (P0→P3), each row: "- **[status] technique** (\`module\`) — engine_change  _ev: evidence_", then a "## Flagged for human re-check" section listing flagged_claims. Update the header counts and date to 2026-06-26.

WRITE the three files in place:
- ${EXTRACTED}\\synthesis_v2.md
- ${EXTRACTED}\\engine_gap_map.json
- ${EXTRACTED}\\engine_gap_map.md

VERIFY after writing: synthesis_v2.md must still contain the original section headings and be LONGER than before; engine_gap_map.json must be valid JSON with >= the original number of gap_map rows.

Reply with a compact JSON summary ONLY: {"new_sections":[...titles...],"gap_rows_added":N,"gap_rows_total":N,"flagged_added":N,"flagged_total":N,"synthesis_chars":N,"sheets_merged":N,"sanity":"<one line: did old headings survive + file longer? yes/no>"}`

const mergeSummary = await agent(mergePrompt, {
  label: 'merge:synthesis+gapmap',
  phase: 'Merge',
  agentType: 'general-purpose',
  effort: 'high',
})

return {
  pass_videos: videos.length,
  videos_done: done.length,
  total_techniques: done.reduce((a, d) => a + d.n_tech, 0),
  batches_failed: totalFailed,
  per_video: done.map((d) => ({ slug: d.slug, n_tech: d.n_tech, n_batches: d.n_batches, n_failed: d.n_failed })),
  surprising_count: allSurprising.length,
  merge: mergeSummary,
}
