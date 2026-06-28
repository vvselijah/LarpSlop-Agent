export const meta = {
  name: 'write-guide',
  description: 'Author the zero-to-hero DaVinci color-grading masterclass chapters (vault notes) from the analyzed methodology + consensus + per-video studies, each grounded with embedded screenshots.',
  phases: [{ title: 'Write', detail: 'one teaching agent per chapter' }],
}

const RES = 'C:/Users/elija/OneDrive/Desktop/ai agent team/docs/research/color-masterclass'
const METH = `${RES}/COLOR-GRADING-METHODOLOGY.md`
const CONS = `${RES}/CONSENSUS.md`
const PV = `${RES}/per-video`

const CHAPTERS = [
  { file: '01 - What Color Grading Is (and Correction vs Grading)', title: 'What Color Grading Is — Correction vs Look, and the Mindset', sources: ['mullins-grading-philosophy', 'cullen-master-scopes', 'cullen-contrast-cinematographer'], focus: 'the mindset; correction vs look-development (two buckets); macro beats micro; scopes guide / eyes + client decide; why order matters. Set the tone for a total beginner.' },
  { file: '05 - Project Setup & Color Management', title: 'Project Setup & Color Management (the foundation everyone skips)', sources: ['cullen-36-project-settings', 'grading-too-complicated', 'best-node-tree-any-camera'], focus: 'DaVinci YRGB vs Color Managed; working space = DaVinci Wide Gamut/Intermediate; the input transform per camera (table); project-settings gems set BEFORE node creation (tetrahedral LUT interp, luminance-mix-defaults-to-zero, broadcast-safe off, timeline res).' },
  { file: '10 - The Professional Workflow', title: 'The Professional Workflow (the canonical order, end to end)', sources: ['mullins-grading-philosophy', 'best-node-tree-any-camera', 'grading-too-complicated'], focus: 'the full stage-by-stage order (color mgmt -> CST sandwich -> balance/exposure -> contrast -> saturation -> match -> secondaries -> look -> film -> texture -> QC/delivery), each with the scope check. This is the spine chapter.' },
  { file: '15 - Node Trees', title: 'Node Trees — how pros structure the grade', sources: ['mostyn-perfect-node-tree', 'best-node-tree-any-camera', 'mullins-grading-philosophy', 'grading-too-complicated'], focus: 'the CST sandwich; fixed labeled serial skeleton built empty-first; one idea per node; toggling (Ctrl+D / Shift+D); save as Still/PowerGrade; re-point node 01 per camera; serial vs parallel; where authorities differ.' },
  { file: '20 - Primaries', title: 'Primaries — Balance, Exposure, Contrast & Saturation', sources: ['cullen-contrast-cinematographer', 'best-node-tree-any-camera', 'mostyn-color-page-intro', 'mullins-grading-philosophy'], focus: 'offset/HDR wheels over lift-gamma-gain (and the gamma=linear + gain variant); neutralize casts on parade; contrast + pivot (0.435 Rec709 / 0.336 DWG) judged at sat=0; luma-safe saturation (HDR/Color Slice, leave primary Sat at 50); the S-curve debate.' },
  { file: '30 - Scopes & Targets', title: 'Scopes & Targets — reading like a pro', sources: ['cullen-master-scopes', 'mostyn-read-scopes', 'beginners-guide-grading'], focus: 'waveform (0-1023, black near 0 no crush, highlights under clip), parade (neutrals overlap = white; THE matching scope), vectorscope (skin line ~123 deg, on/under/over, consistency), histogram (log spike -> spread); scopes as measurement device not target; the numeric target table.' },
  { file: '40 - Secondaries', title: 'Secondaries — qualifiers, windows, tracking', sources: ['qualifier-tricks', 'mullins-grading-philosophy', 'frenchie-masterclass'], focus: 'HSL qualifiers (feather/roll-off), Power Windows + tracker, Color Warper, curves; key NON-skin only; the qualifier-as-noise-reduction-mask pro trick; when NOT to use secondaries.' },
  { file: '45 - Skin Tones', title: 'Skin Tones — the chapter that matters most', sources: ['mostyn-read-scopes', 'grading-too-complicated', 'cullen-master-scopes', 'qualifier-tricks'], focus: 'the skin-tone line debate (Mostyn vectorscope yes vs Kelly/Mullins by-eye); on/under/over + consistency-beats-position; skin IRE ~40-50; fix skin in BALANCE globally, never key skin; the exposure heatmap.' },
  { file: '50 - Building a Look', title: 'Building a Look — color theory, harmony, split-toning', sources: ['frenchie-masterclass', 'mullins-grading-philosophy', 'cullen-contrast-cinematographer'], focus: 'color theory + harmony; teal-orange / complementary; split-tone via curves with Lum Mix 0 (cool shadows/warm highlights); narrative color arc; run grade UNDER the look at ~50% mix; saturation discipline.' },
  { file: '55 - Film Emulation', title: 'Film Emulation — the filmic look done right', sources: ['film-emulation-16-35mm', 'mullins-grading-philosophy', 'best-node-tree-any-camera'], focus: 'film look = STACKED effects not a LUT flip; print LUTs (Kodak 2383) need Cineon film-log input (pre-CST), compounded for keyable strength, restore washed blacks; halation recipe (red-weighted highlight blur, ADD in linear); grain in shadows/mids; vignette; density.' },
  { file: '60 - Delivery', title: 'Delivery — output transforms, render, broadcast-safe', sources: ['mullins-grading-philosophy', 'cullen-36-project-settings', 'frenchie-masterclass'], focus: 'output transform 2.4 (broadcast) vs 2.2 (web/IG/phone); Light Box QC for consistency; PowerGrade reuse; export bitrate high enough that grain survives social recompression (~100 Mbps 4K masters); render cache.' },
  { file: '90 - The One-Page Cheat Sheet', title: 'The One-Page Cheat Sheet', sources: ['grading-too-complicated', 'best-node-tree-any-camera', 'cullen-36-project-settings'], focus: 'the entire method compressed to one scannable page: the node tree, the order, the scope targets table, the disputed knobs, the do/dont list. Dense and practical.' },
]

phase('Write')
log(`Authoring ${CHAPTERS.length} masterclass chapters`)
function prompt(c) {
  const pvFiles = c.sources.map(s => `${PV}/${s}.md`).join('\n')
  return (
    `You are an expert colorist AND a gifted teacher writing one chapter of a polished, SELLABLE "zero-to-hero" DaVinci Resolve color-grading masterclass for a smart beginner (the reader has Resolve open but has never graded). ` +
    `Chapter: "${c.title}".\nFocus: ${c.focus}\n\n` +
    `GROUND YOURSELF FIRST — read these (they are the distilled consensus of 14 analyzed masterclasses):\n- ${METH}\n- ${CONS}\nAnd these specific source analyses most relevant to this chapter:\n${pvFiles}\n\n` +
    `Then WRITE the chapter as a clean Obsidian markdown note (freeform, NO YAML frontmatter). Requirements:\n` +
    `- Start with an H1 title and a one-paragraph "what you'll learn".\n` +
    `- Teach concretely and NUMERICALLY (real values, scope targets, exact settings) — a beginner should be able to DO it, and an engineer could implement it.\n` +
    `- Where the authorities genuinely disagree, teach it as a knob ("depends on deliverable/taste"), citing who takes which side — don't paper over it.\n` +
    `- Embed 2-4 screenshots that genuinely illustrate the point using Obsidian embed syntax: ![[screens/<filename>]]. Choose filenames ONLY from the "Key frames" sections of the per-video source files you read; the actual files are named "<slug>__fXXX.jpg" (e.g. ![[screens/cullen-master-scopes__f021.jpg]]). Add a one-line caption under each.\n` +
    `- End with a short "Key takeaways" bullet list and a "Try it yourself" mini-exercise.\n` +
    `- Keep it tight and high-signal (~600-1100 words). Sound like a confident pro teacher, not a textbook.\n\n` +
    `Return ONLY the finished markdown of the chapter as your message (no preamble, no code fences around the whole thing).`
  )
}
const chapters = await parallel(CHAPTERS.map((c, i) => () =>
  agent(prompt(c), { label: 'chapter:' + c.file.slice(0, 14), phase: 'Write', effort: 'high' })
    .then(md => ({ file: c.file, title: c.title, markdown: md }))
))
log(`Wrote ${chapters.filter(c => c.markdown).length}/${CHAPTERS.length} chapters`)
return { chapters }
