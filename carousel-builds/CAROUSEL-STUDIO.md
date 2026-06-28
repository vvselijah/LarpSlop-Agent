# Carousel Studio — environment & toolchain handoff

Durable reference for the **reel → carousel** + **idea → carousel** render studio built in this folder.
A future session (even on a fresh machine) can run the whole pipeline from this doc.
Session narrative + current pending state: `../SESSION-HANDOFF-2026-06-26-carousel-studio.md`.

---

## What this is

A headless **HTML → PNG** carousel studio. We author slides as HTML/CSS (full design freedom —
gradients, glass, custom type), render them to exact **1080×1350** PNGs with headless Edge, and
preview the whole deck as a contact-sheet "board" PNG. Output is post-ready Instagram carousels.
It produced the Headroom (Frost/Aqua) and AI Builder Cheat Codes (Gold) decks this session.

**Why HTML→PNG, not image-gen:** carousels are text-heavy; AI image-gen mangles copy. HTML gives
pixel-perfect text + a reskinnable theme system. (Image-gen / Higgsfield is still right for
photographic poster/art slides — e.g. the older `tworkflow-vibe` deck.)

---

## The reel-teardown pipeline (remaking someone's reel)

1. **Download:** `yt-dlp` (`C:\Users\elija\.local\bin\yt-dlp.exe`) → `source-reels/<id>.mp4`.
   `& $yt --no-playlist -o "source-reels\%(id)s.%(ext)s" "<reel-url>"`
2. **Watch it:** `video-analyzer` MCP → `analyze_video` (detail `standard` or `detailed`, `ocrLanguage:"eng"`, cap `maxFrames` ~16 to avoid 25k-token truncation).
   - **IG reels have NO caption track** → transcript comes back empty. Read the **burned-in word captions from the FRAMES** + the `ocrResults` (on-screen UI text). That IS the script.
3. **Verify every factual claim** before it goes in Elijah's mouth (he has 100k+ followers; an install rec is a real-world claim). For GitHub tools: `Invoke-RestMethod https://api.github.com/repos/<owner>/<repo>` → real stars/license/dates. Tier the rest (`[[feedback_primary_source_platform_claims]]`): repo's-own-claim vs verified vs mockup-flourish (drop).
4. **Reframe to Elijah:** own series name (not the source's), peer "putting you on" voice (not an ad), his anti-vibe-slop builder stance, current model names.
5. Build the deck (below) + a vault `idea` note + (optionally) a video script.

---

## The build system (`build.py` per deck)

Each deck folder has a self-contained `build.py`. Structure (copy an existing one):

- `STRUCT` — shared CSS: `.slide` (1080×1350, fl... centered, `padding:150px 96px`), `.brand`
  (top-left @handle), `.swipe` (bottom-right), `.eyebrow`, `.h1` (`.xl/.lg/.md`), `.ac` (accent span),
  `.sub`, `.body`, `.cap`, plus component blocks as needed: `.repo` (GitHub card), `.chart/.bar`
  (compression bars), `.list`, `.twocol/.col(.hot)`, `.step/.snum/.steplab` (numbered steps),
  `.prompt/.plabel/.ptext` (prompt cards = save magnets), `.delta`, `.footer`.
- `THEMES` — dict of `{label, fonts, vars}`. **All design lives in `vars` (`:root{…}`)**: `--bg`,
  `--ink`, `--muted`, `--accent`, `--asoft`, `--onac`, `--card`, `--cbd`, `--hair`, `--eye`,
  `--barmute`, `--fh` (display font), `--fb` (body font), `--hw`, `--ht`. Swap a theme = swap colours
  + `--bg`; copy is untouched. Reskinning is nearly free.
- `SLIDES` — list of HTML fragment strings (one per slide). For per-theme copy use a
  `content_for(theme)` helper returning a different list (e.g. `SLIDES_AQUA` for the dark deck).
- Bottom loop writes `theme/slide-N.html` for each slide + a `theme_board.html` contact sheet
  (thumbs scaled `.30556`, 1416px wide).

Fonts load from Google Fonts (`fonts.googleapis.com`). Display font this session = **Plus Jakarta
Sans** (800) + **Inter** body — fresh vs the older decks' Sora / Space Grotesk / Archivo Black.

## The render pipeline (`render.ps1` — generic, reuse it)

`headroom/render.ps1` renders any list of slide/board HTML files to sibling PNGs. Reuse it from
other deck folders: `& ..\headroom\render.ps1 -Files .\<theme>\slide-*.html -W 1080 -H 1350`
(boards: `-W 1416 -H 1420`).

It wraps headless Edge. **The four gotchas that cost time — don't relearn them:**
1. **Edge is a GUI app** → must use `Start-Process -FilePath $edge -ArgumentList $a -Wait` (a bare
   `& $edge …` returns immediately / no exit code / no file).
2. **Fonts:** add `--virtual-time-budget=4500` so Google Fonts finish loading before the screenshot
   (else it falls back to Segoe). Use `--headless` (old) + `--screenshot`.
3. **Spaces in path:** `--screenshot=<path with spaces>` makes Edge throw *"Multiple targets are not
   supported in headless mode"* (the `ai agent team` folder). **Fix: screenshot to a `$env:TEMP`
   no-space path, then `Copy-Item` to the final location.** (render.ps1 already does this.)
4. Encode spaces in the input `file:///` URI as `%20`.
   Edge prints harmless `ERROR …task_manager…` / `…sync…GetUpdates` lines — ignore them.
   Edge path: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.

## Make a new deck (checklist)

1. `mkdir carousel-builds/<deck>/`; copy a `build.py` (Headroom = light/multi-theme; app-idea =
   dark + step/prompt components). Rewrite `SLIDES` (8 slides: hook → value/steps → CTA) + pick/clone a `THEMES` entry.
2. `cd carousel-builds/<deck>; python build.py`
3. Render board → **review at full res** (board thumbnails hide texture/clipping): `& ..\headroom\render.ps1 -Files .\<theme>_board.html -W 1416 -H 1420` then Read the PNG.
4. QA the dense slides (cards/bars/lists) at full res for clipping; fix bar/element widths in `build.py`; re-render only what changed.
5. Render all 8 slides; save a vault `idea` note (property contract: `type: idea, domain: content, stage: raw, status: open, date_captured:, tags: []`).

---

## Design lessons (hard-won this session)

- **Visibility:** background textures at ~.05–.08 opacity are invisible after IG compression
  ("had to zoom all the way in"). Go **bold: ~.30–.40 grid opacity, 2px lines, .25+ glows.** Judge at
  full res, never board scale.
- **Quality bar = depth + premium type + glass cards**, not flat colour blocks. Elijah rejected flat
  thumbnails and the claude-native `visualize` widget previews outright.
- **Each deck its own identity** (colour + bg motif): Frost (light teal, graph-grid + corner glows) ·
  Aqua (dark turquoise, radar-ring arcs) · Gold (dark gold, money — grid / pinstripe / glow / green
  variants). Reuse the *system*, vary the *look*.
- **Save magnets:** exact prompts, step lists, "what it strips" reference rows, repo cards. Put them on their own slides.
- **Voice/framing:** peer cheat-code share, never an ad; CTA = save + send; "be smart be safe be blessed 🙏".

## Standing rules (CLAUDE.md)

DRAFT only — **never post/publish** without Elijah's explicit per-action OK. Secrets only in env vars,
never in files (this tree syncs to OneDrive). Tier every platform/tool claim; verify before recommending.
Run Python/ffmpeg/yt-dlp/Edge via **PowerShell**, not Bash (Bash lacks them here).
