# SFX generation prompts — "Introducing ClipWith"  (Phase 3)

**Status: SPECS-ONLY (default).** These are ElevenLabs `text_to_sound_effects`-ready prompts.
Nothing here is generated yet — generating costs credits and is gated on Elijah's OK.
**To fire them:** say "generate the SFX" and I'll run each prompt → `clipwith-edit/sfx/<name>.wav`.

Mapping is to `graphics/SPEC.md` (G#) + `assembly-map.md` (shot #). Keep them subtle — these sit
UNDER continuous voice + (later) trending audio added in the IG Edits app, so they're accents, not a bed.

| File to generate | Lands on | ElevenLabs prompt | duration_seconds | prompt_influence |
|---|---|---|---|---|
| `hook_drone.wav` | shots 1–3 (hook/intros) | "subtle deep cinematic sub-bass drone, ominous tension, no melody, clean low-end, dead air room tone" | 4 | 0.3 |
| `bleep.wav` | shot 2 ("trafficking [bleep]") | "single short censor bleep, 1000 Hz beep, clean, broadcast TV style, 0.4 seconds" | 1 | 0.6 |
| `whoosh_a.wav` | jump-cuts (problem beats) | "fast clean transition whoosh, short air swoosh, modern punchy, subtle" | 1 | 0.4 |
| `whoosh_b.wav` | jump-cuts (variant) | "quick reverse whoosh into a soft tick, tight, hi-fi, no reverb tail" | 1 | 0.4 |
| `impact_boom.wav` | shot 4–5 ("$200 billion / editing industry") G3 | "deep cinematic impact boom, trailer hit, weighty sub drop, tight punchy, no long tail" | 2 | 0.5 |
| `headline_ding.wav` | shots 4–7 G4 (headlines pop) | "paper-swish into a soft notification ding, light, UI-style, crisp" | 1 | 0.5 |
| `comedic_boing.wav` | shots 7–11 G2 (pain-point overlays) | "light comedic cartoon boing pop, playful, short, dry" | 1 | 0.5 |
| `stat_tick_rise.wav` | shot 12 G5 ($2,500 · ~200 count-up) | "rising digital tick counter, numbers counting up, light electronic blips accelerating then a soft landing thud" | 2 | 0.5 |
| `riser_to_card.wav` | shot 15→16 (into G6 Introducing card) | "cinematic riser swell building tension over 3 seconds into a clean impact, uplifting, modern trailer" | 4 | 0.4 |
| `logo_shing.wav` | shot 16 G7 (logo flash) | "sharp bright metallic shing, quick magical sparkle accent, premium logo sting, 0.4 seconds" | 1 | 0.6 |
| `ui_click.wav` | shots 17–18 G8 (app UI demo) | "soft modern UI click and keyboard key tick, clean app interface tap, subtle" | 1 | 0.5 |
| `done_chime.wav` | shot 18 (\"just ask\" → done) | "soft satisfying completion chime, two-note positive app success sound, gentle, premium" | 1 | 0.5 |
| `reveal_whoomp.wav` | shot 20 G9 (\"edited by ClipWith\") | "big riser into a satisfying deep whoomp reveal, cinematic curtain-drop moment, weighty, clean" | 3 | 0.5 |
| `outro_swell.wav` | shots 21–23 G10 (CTA) | "uplifting cinematic outro swell, warm hopeful synth pad rising to a gentle peak, motivating, modern" | 5 | 0.4 |

## Notes
- ElevenLabs `text_to_sound_effects` caps at ~22s; all here are ≤5s. `prompt_influence` 0.3–0.6 (lower = more creative/natural, higher = literal).
- Generate 1–2 takes of the hero hits (`impact_boom`, `riser_to_card`, `reveal_whoomp`) and keep the best.
- **Dialogue audio:** the trimmed clips keep their own camera audio by default. The cleaner **Røde 32-bit-float `_backup.wav`** for each take is per-clip aligned (verified) — substitute it on the hero lines if the camera scratch is noisy (Phase 3 task, free).
- **No music** is baked — Elijah adds trending audio in the IG Edits app (voice-only export rule).
