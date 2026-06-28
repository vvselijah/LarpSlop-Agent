# EDIT OUTLINE — "Introducing ClipWith"  ·  SFX + Graphic placement, modeled on the reference

**Purpose:** a beat-by-beat outline of *where graphics land and where sound effects hit*, derived from
how the reference reel actually paces those devices — so our edit borrows its proven rhythm instead of
guessing. Pairs with `assembly-map.md` (the clip EDL), `graphics/SPEC.md`, and `sfx/PROMPTS.md`.

**Reference:** `abc wrap/reference-reels/DNPHHpTAme2.mp4` (@justincgg, 54s, 1080×1920, 30fps, 29.9K likes) —
the AI-*coding* launch-parody our script is built on. Analyzed frame-by-frame 2026-06-27 (video-analyzer:
43 dedup frames + OCR timeline). A second reel, `DSdYvD4jxkd.mp4` (Escrow Bros "grindset rant"), is a
*different* concept (kept for the alt "manic founder" reel — `agentic-grindset-reel-brief.md`), not this edit.

---

## 1. What the reference actually does (its device + SFX rhythm)

Reconstructed device timeline (seconds into the 54s reel):

| t | Device on screen | The SFX that sells it |
|---|---|---|
| 0:00–0:15 | Cold open + deadpan VO, **word-pop captions running continuously** | low **drone** bed under the hook |
| ~0:16 | **Keynote/launch card** ("our smartest, fastest, most useful model") | **riser → soft impact** into the card |
| 0:24–0:29 | **Stacking comedic pain-overlays** ("noo fix my code", "FIX IT CLAUDE", "make it more human") — each new line *adds on top* | light **boing / tick** per line as it pops |
| 0:29–0:37 | **App-UI screenshots** (Cursor/Claude agent, "debug the code", token spend) | **UI clicks / keyboard ticks** |
| 0:38 | **Billing screenshot** ("$9.80 credit balance, Cancel plan") | soft **ding** on the number |
| 0:41–0:44 | **News-headline social-proof cards** ("Base44 → $50M ARR", "Bolt.new → $1M ARR in one weekend") — *the signature credibility device* | **paper-whoosh + ding** per headline |
| 0:47–0:53 | **Follow / CTA** closer | **uplifting outro swell** |

**The three transferable rules:**
1. **Captions never stop; the VO is continuous across every hard cut.** That continuity is the momentum engine — SFX accent the *cuts*, they don't fill silence.
2. **Hard cut every ~2–3s, on the stressed word** → a short **whoosh** rides most cuts (vary 2 whoosh tones so it doesn't get repetitive).
3. **Each on-screen device gets ONE matched hit, not a wall of sound** — slam-in = impact, headline = ding, logo = shing, reveal = whoomp. SFX sit *under* the voice; they're seasoning.

---

## 2. Our placement map (reference rhythm → our 20 clips)

Full clip/source detail is in `assembly-map.md`; this is the **graphic + SFX layer** over it. `G#` = `graphics/`, SFX = `sfx/`.
G1 word-pop captions run the WHOLE piece (built at edit time from the final timeline, caption-engine "Punchy Bold Animated").

| clip | beat | Graphic (track above footage) | SFX hit | mirrors reference |
|---|---|---|---|---|
| 1 | hook ("drug dealer → $1M software co.?") | — (faces) | `hook_drone` bed | 0:00 cold-open drone |
| 2 | "convicted of trafficking [bleep]" | — | `bleep` on the word | (our gag) |
| 3 | "never convicted — never did anything" | — | `comedic_boing` on the smirk | 0:24 boing |
| 4 | "disrupt a **$200 billion** industry—" | **G3a $200B** slam-in | `impact_boom` + `headline_ding` | 0:16 card slam |
| 5 | "the editing industry." | **G3b Editing Industry** | impact tail | — |
| 6 | "everybody wants to be a creator…" | **G4 headlines** (start feed) | `whoosh_a` on cut | 0:41 headline cards |
| 7 | "record everything, download CapCut…" | **G4** cont. + **G2** ("CapCut crashed AGAIN 😭") | `comedic_boing` | 0:24 stacking overlays |
| 8 | "99% of creators can't edit" | **G2** | `whoosh_b` | — |
| 9 | "months learning a new skill" | **G2** ("6 hours for ONE reel 💀") | `whoosh_a` | — |
| 10 | "thousands a month for an editor" | **G2** ("$2,500/mo just to EDIT?!") | `impact_boom` | — |
| 11 | "cheap templates tank their quality" | **G2** | `whoosh_b` | — |
| 12 | "$2,500/mo · ~200 videos/mo" | **G5 stat pop** (count-up) | `stat_tick_rise` | 0:38 billing-number ding |
| 13 | "not everyone has the budget / 100 hrs" | — | — (let it breathe) | the reference's mid-beat dip |
| 14 | "creativity & motivation tank" | — | `hook_drone` dip (callback) | — |
| 15 | "first fully agentic, prompt-to-edit model" | **G6 Introducing** → **G7 logo flash** | `riser_to_card` → `logo_shing` | **0:16 the money beat** |
| 16 | "no menus that take months" | **G8 app UI** ⚑ blocked | `ui_click` | 0:29 app screenshots |
| 17 | "cuts, captions, SFX — you just ask" | **G8** ⚑ blocked | `ui_click` + `done_chime` | 0:31 UI + done |
| 18 | "no editor, no time, no money — excuse gone" | — | `whoosh_a` (snap) | — |
| 19 | "this whole video? edited with ClipWith" | **G9 meta reveal** ⚑ blocked | `reveal_whoomp` | the meta-flex beat |
| 20 | CTA: waitlist / clipwith.ai | **G10 CTA card** | `outro_swell` | 0:47 outro swell |

**Transitions:** hard cuts on the stressed word throughout. Add a quick **dark flash** into clip 15 (G6) to mark
the problem→solution pivot (the reference's hardest gear-change). Optional whip-pan/zoom-punch between the
problem beats (clips 7–11) for energy — but don't overdo it; the cuts already carry it.

---

## 3. Asset status (what exists vs what's blocked)

**Graphics — built (`graphics/*.mov`, ProRes 4444 alpha, drop on a track above footage in Resolve):**
G2 PainPoint (props-driven text) · G3a $200B · G3b Editing Industry · G5 Stat Pop · G6 Introducing · G7 Logo
Flash · G10 CTA · **G4 Headlines ✅ NEW (2026-06-27)** — the reference's signature social-proof device, 3 article
cards (creator economy $480B / CapCut 300M / AI-editing fastest-growing). Preview: `graphics/G4Headlines_preview.png`.
⚠ Sanity-check the G4 stats/sources before publish; tweak copy via the `headlines` prop on the `G4Headlines` comp.

**Graphics — still blocked:** **G8** (app/prompt-to-edit UI) and **G9** ("edited by ClipWith" timeline reveal)
need real ClipWith app screenshots. Drop a logo + 2–3 screenshots into `graphics/brand/` and both build in one pass.

**SFX — BLOCKED on a working key.** All 14 are specced and ready (`sfx/PROMPTS.md`), but the ElevenLabs MCP key
returns 401 (invalid). Options: (a) set a valid `ELEVENLABS_API_KEY` + restart, then fire all 14 (~1–2 min, cheap);
(b) source them free (freesound/Pixabay/YouTube library) — slower, no key; (c) ship caption + graphics first and
add SFX in the IG Edits pass. Nothing here generates until that's resolved.

---

## 4. The order to actually finish (in Resolve)
1. **Graphics** → drop the 8 built `*.mov` onto a video track at the beats above (G4 over clips 6–7; G8/G9 stand-in cards until screenshots land).
2. **SFX** → unblock the key (or go free), generate, place one hit per device per the table.
3. **Captions** → caption-engine word-pop over the whole timeline (G1).
4. **Export** 1080×1920 **voice-only** (`clean-for-instagram.js`) → add trending audio in the IG **Edits** app.
5. Preview in full → **Elijah approves before any final render** → Elijah posts (never auto-publish).
