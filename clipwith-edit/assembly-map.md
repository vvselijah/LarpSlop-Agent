# Assembly Map — "Introducing ClipWith"  (master EDIT DECISION LIST)

Built from word-level transcripts of all 24 raw takes (`transcripts/`) + the shooting script
(`Tanner and I.md`) + `graphics/SPEC.md`. Each row = the **keeper take** (last clean delivery),
trimmed to `clips/NN_shotNN_keyword.mp4`, in timeline order. Source in/out are seconds into the
original file in `clipwithedit/` (also in `cut-list.json`). **Import `Introducing-ClipWith.fcpxml`
into DaVinci to get all clips on a timeline in this order automatically.**

Legend: **G#** = graphic from `graphics/SPEC.md` · **SFX** from `sfx/PROMPTS.md` · G1 word-captions run over
the whole piece. The **orient** column now means resolution mode: **L** = 2160×3840 portrait (sharper camera
mode) · **V** = 1728×3072 portrait (softer mode). **Both are already 9:16 vertical — no reframe needed.** (The
'L' files store as 3840×2160 + a rotation flag; ffmpeg bakes the rotation on trim, so every clip is portrait.)

| # | shot | clip file | src | in–out | orient | Line (keeper) | Graphic | SFX |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | `01_shot1_hook` | 174 | 0.0–13.0 | L | "Do you think a drug dealer could build a software company to $1M in a year?" | — (faces) | hook_drone |
| 2 | 2 | `02_shot2_tanner-intro` | 176 | 0.0–9.2 | L | "My name's Tanner — and I was convicted of trafficking [bleep]." | — | bleep |
| 3 | 3 | `03_shot3_elijah-intro` | 178 | 12.8–17.5 | V | "My name's Elijah… I've never been convicted — because I've never done anything." | — | comedic_boing (smirk) |
| 4 | 4 | `04_shot4_disrupt-200b` | 180 | 0.0–14.5 | L | "But we decided to disrupt a $200 billion industry—" | **G3** + **G4** | impact_boom + headline_ding |
| 5 | 5 | `05_shot5_editing-industry` | 181 | 0.0–1.5 | L | "the editing industry." | **G3** | impact tail |
| 6 | 6 | `06_shot6_everybody-creator` | 182 | 0.0–4.4 | L | "Everybody wants to be a creator — influencer, streamer, YouTuber, TikToker." | **G4** | whoosh_a |
| 7 | 7 | `07_shot7_record-capcut` | 183 | 1.5–8.3 | L | "So they record everything, download CapCut, and dream of pro edits." | **G2** ("CapCut crashed AGAIN") | comedic_boing |
| 8 | 8 | `08_shot8_99pct-cant-edit` | 184 | 0.0–7.5 | L | "The reality? 99% of creators don't know how to edit." | **G2** | whoosh_b |
| 9 | 9 | `09_shot9_months-learning` | 185 | 3.1–7.7 | L | "So they spend months learning a whole new skill—" | **G2** ("6 hours for ONE reel") | whoosh_a |
| 10 | 10 | `10_shot10_thousands-editor` | 186 | 0.0–5.6 | L | "—pay thousands a month for an editor—" | **G2** ("$2,500/mo just to EDIT?!") | impact_boom |
| 11 | 11 | `11_shot11_cheap-templates` | 187 | 0.0–6.0 | L | "—or settle for cheap templates that tank their quality." | **G2** | whoosh_b |
| 12 | 12 | `12_shot12_2500-200videos` | 189 | 0.0–9.8 | L | "I was about to pay over $2,500 a month, because I post almost 200 videos a month." | **G5** (stat pop) | stat_tick_rise |
| 13 | 13 | `13_shot13_no-budget-100hrs` | 190 | 0.0–4.6 | L | "Not everyone has the budget. Not everyone has 100 hours to learn it." | — | — |
| 14 | 14 | `14_shot14_motivation-tanking` | 197 | 3.0–8.7 | L | "And while you stress over editing… your creativity and motivation tank." | — | hook_drone (dip) |
| 15 | 17 | `15_shot17_agentic-model` | 201 | 48.4–51.6 | L | "So we built the first fully agentic, prompt-to-edit model." | **G6** + **G7** | riser_to_card → logo_shing |
| 16 | 18a | `16_shot18a_no-more-menus` | 204 | 46.0–53.2 | V | "No menus that take months to master." | **G8** (app UI) | ui_click |
| 17 | 18b | `17_shot18b_handles-everything` | 206 | 37.9–46.8 | V | "Cuts, captions, SFX — everything. You just ask." | **G8** | ui_click + done_chime |
| 18 | 19 | `18_shot19_eliminated-excuse` | 207 | 11.8–22.8 | V | "No editor, no time, no money? We just eliminated that excuse." | — | whoosh_a (snap) |
| 19 | 20 | `19_shot20_edited-by-clipwith` | 208 | 0.0–6.0 | V | "Oh — and this whole video? Edited with ClipWith. A few simple prompts." | **G9** (meta reveal) | reveal_whoomp |
| 20 | 21-23 | `20_shot21-23_cta-outro` | 209 | 92.0–105.0 | V | "Building in public… launch end of month… 1,000+ on the waitlist — clipwith.ai." | **G10** (CTA card) | outro_swell |

**Rough assembled runtime ≈ 2.5 min** (before tightening internal pauses) → target ~70s after you cut
the flagged dead air (clip 1's mid-pause, clip 4's slow gaps) and pace the jump-cuts.

## ⚑ Decisions for Elijah (don't let me guess these)
1. **Missing beats:** no clean standalone "So we built something to fix it" (shot 15) or "ClipWith.ai" name-drop
   (shot 16) — they were merged into clip 15. Want a quick VO pickup, or lean on the **G6 "Introducing ClipWith"** card?
2. **Hero beats to eyeball:** clip 1 (hook, internal ~5s pause to tighten), clip 15 (product reveal),
   clip 19 (meta flex), clip 20 (CTA). These carry the reel.
3. **Resolution mix (minor):** clips 1,2,4–15 are 2160×3840 (sharper); clips 3,16–20 are 1728×3072 (softer,
   a different camera mode). Both are 9:16 and both downscale fine to 1080×1920 — but you may notice a slight
   sharpness/look shift at clip 16. Colorkit's shot-by-shot develop will help even them out.
4. **Pauses to tighten:** clip 1 (hook, ~5s mid-line gap 4.8–9.7), clip 4 (very slow $200B delivery).
5. **Alternates** kept in source if you prefer them: 175 (Tanner), 179 (disrupt), 188 ($2,500 w/ throat-clear).

> ~~Earlier I flagged a landscape/vertical "orientation split" as the #1 call — that was WRONG.~~ The early
> files store as 3840×2160 + a rotation flag; ffmpeg bakes the rotation on trim, so **every delivered clip is
> correctly-oriented 9:16 portrait.** No reframe needed. (Verified on frame grabs.)

## Build artifacts
- `clips/` — 20 trimmed keeper proxies (H.264 CRF18, native res, frame-accurate).
- `Introducing-ClipWith.fcpxml` — import into DaVinci → timeline pre-laid in order.
- `cut-list.json` — machine-readable source of truth (re-run `build_clips.py` to rebuild).
