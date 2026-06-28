export const meta = {
  name: 'color-masterclass-merge-only',
  description: 'CHEAP finish: merge already-written per-video sheets into synthesis_v2.md + engine_gap_map (ONE agent, no re-extraction). Use when the sheets exist on disk but the merge did not run.',
  whenToUse: 'Finishing a pass whose per-video-v2/<slug>.md sheets are already written but synthesis/gap-map were not merged (e.g. the vision run hit a cap on the merge step).',
  phases: [{ title: 'Merge', detail: 'fold the named sheets into synthesis_v2.md + engine_gap_map.(json|md), cleaning prior bookkeeping' }],
}

// args = { base: "<abs path to docs/research/color-masterclass>", new_slugs: ["slug1", ...] }
let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const base = A.base
const newSlugs = A.new_slugs || []
if (!base || !newSlugs.length) {
  throw new Error('args.base/args.new_slugs missing — got: ' + (typeof args) + ' ' + JSON.stringify(args).slice(0, 200))
}
const EXTRACTED = base + '\\extracted'
const PERVID = base + '\\per-video-v2'

phase('Merge')

const mergePrompt = `You are MERGING new frame-by-frame color-grading evidence into an existing engine-spec corpus. This is additive and must be loss-free.

Files (absolute paths):
- Existing methodology:  ${EXTRACTED}\\synthesis_v2.md
- Existing gap map JSON:  ${EXTRACTED}\\engine_gap_map.json
- New per-video sheets to fold in (READ each):
${newSlugs.map((s) => '  - ' + PERVID + '\\' + s + '.md').join('\n')}

TASK:
0. CLEANUP prior incomplete-run bookkeeping FIRST: in engine_gap_map.json delete any gap_map row whose id is "pending-vision-analysis-10-videos" or whose technique starts with "MERGE BOOKKEEPING", and delete any flagged_claims entry starting with "MERGE-PROCESS FLAG"; in synthesis_v2.md remove any pending-work / "pending vision analysis" placeholder note left by a prior failed merge. Then do the real merge below.
1. Read synthesis_v2.md and engine_gap_map.json and ALL the new sheets above.
2. Produce an UPDATED synthesis_v2.md that folds the new demonstrated parameters/techniques into the existing sections where they corroborate or extend (add the new citations like "${newSlugs[0]} 12:34" alongside existing ones). Add a NEW numbered section only for a genuinely new technique not covered. Update the top COVERAGE note to include the newly-analyzed videos and their count. PRESERVE every existing section, citation, and the §"Disputes preserved as tunable knobs" structure — do NOT delete or weaken prior evidence; only add/extend.
3. Produce an UPDATED engine_gap_map.json = {"gap_map":[...], "flagged_claims":[...]}: keep all existing rows; append new corroborating evidence to each row's "evidence" where relevant; ADD new rows for newly-demonstrated techniques (fields: technique, module, status[missing|partial|present], priority[P0|P1|P2|P3], engine_change, evidence); append genuinely-new ambiguous numbers to flagged_claims (dedup).
4. Regenerate engine_gap_map.md from the merged JSON, grouped by priority (P0->P3), each row: "- **[status] technique** (\`module\`) — engine_change  _ev: evidence_", then a "## Flagged for human re-check" section. Update header counts + date.

WRITE the three files in place:
- ${EXTRACTED}\\synthesis_v2.md
- ${EXTRACTED}\\engine_gap_map.json
- ${EXTRACTED}\\engine_gap_map.md

VERIFY after writing: synthesis_v2.md still contains the original section headings and is LONGER than before; engine_gap_map.json is valid JSON with >= the original gap_map row count.

Reply with a compact JSON summary ONLY: {"new_sections":[...],"gap_rows_added":N,"gap_rows_total":N,"flagged_total":N,"synthesis_chars":N,"sheets_merged":N,"sanity":"<one line>"}`

const mergeSummary = await agent(mergePrompt, {
  label: 'merge-only:synthesis+gapmap',
  phase: 'Merge',
  agentType: 'general-purpose',
  effort: 'high',
})

return { merged_slugs: newSlugs, merge: mergeSummary }
