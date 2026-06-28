# REFERENCE TEARDOWN — DNPHHpTAme2 (the reel we're matching)

**Source:** instagram.com/reel/DNPHHpTAme2 (@justincgg, 54s, 1080×1920, 30fps, 29.9K likes).
Local: `abc wrap/reference-reels/DNPHHpTAme2.mp4`. Analyzed 2026-06-27 from extracted frames
(contact sheets every 1.5s), the audio waveform (transient = SFX hit), and ffmpeg scene-cut detection.
This supersedes the lighter OCR pass — read alongside `EDIT-OUTLINE.md`.

---

## 1. PACING (measured, not estimated)
- **54.0s total.** 17 hard cuts at scene>0.18: `4.1, 13.1, 14.4, 20.0, 20.8, 21.7, 23.0, 23.8, 27.3, 34.8, 36.7, 37.9, 38.8, 44.1, 44.8, 49.4, 51.6`s. (Plus subtler jump-cuts under that threshold.)
- **Avg shot ≈ 2–2.5s.** Not uniform — that's the craft:
  - **Machine-gun cluster 0:20–0:24** → 5 cuts in ~4s (the pain/escalation). Fastest section.
  - **Deliberate quiet micro-pause ~0:19** → a near-silent gap in the waveform = a held beat ("but how?") before the slam back in. The ONE place it breathes.
  - Opening hook 0:00–0:13 is slower (one long-ish couch shot) to land the premise, then it accelerates.
- **VO is continuous across every cut.** The sentence never stops while the room/angle changes. Copy this exactly — it's the whole momentum trick.

## 2. THE GRAPHIC / POP-UP KIT (what's on screen, with timing + quality notes)
| t | Element | Quality detail to match |
|---|---|---|
| whole reel | **Word-by-word captions** | Bold, centered, **pop-in per word**. NOT all-white — **key words get an emphasis color** (the stressed word changes color). Thin dark stroke for legibility over footage. |
| whole reel | **Prop-mic gag** | Both hold a slabbed Pokémon card up like a mic the entire time — recurring absurd visual. (Ours = a camera/SSD/clapperboard.) |
| ~0:10–0:13 | **"$50 BILLION DOLLAR INDUSTRY" slam card** | Huge **condensed bold** type, dark bg, the figure emphasized, **slam/scale-in** with a shake. Their biggest type moment. → our **G3**. |
| ~0:15–0:16 | **White rounded card / screenshot popups** | Clean white rounded cards (launch-card + app screenshots) — composited over frame. |
| ~0:24 | **Giant "99" stat number** | One massive colored number popping full-frame ("99% of…"). → our **G5** stat pop. |
| ~0:25–0:29 | **Stacking pain-text overlays** | Quote-style lines that **ADD ON TOP of each other** as he rants ("noo fix my code" → "FIX IT CLAUDE" → "CLAUDE U F*** FIX MY CODE"). The stacking IS the joke. → our **G2** (run 3–4 in sequence, let them accumulate). |
| ~0:30 & ~0:38 | **Dark app + billing screenshots** | Real Cursor/Claude chat UI; a real billing screen ("Pay as you go · Credit balance **$9.80** · Cancel plan"). Authenticity device. → our **G8**. |
| ~0:41–0:44 | **News-headline article cards** ⭐ | THE social-proof device: real article screenshots ("Supersonic Growth: Base44 → **$50M ARR**", "Bolt.new → **$1M ARR** in one weekend") with a **marker-highlight (yellow/green) swept across the key stat**. This is the "real, exploding market" beat. → our **G4 (built 2026-06-27)** — we use an orange underline-sweep; a yellow marker-block variant would match even closer. |
| ~0:51–0:53 | **End card** | Wide two-shot + a colorful logo/wordmark reveal (their "BIG ___" gag). → our **G10 CTA**. |

**Quality throughline:** lo-fi native (phone, natural light, real rooms) BUT the graphics are crisp and punchy — condensed bold type, spring/slam-ins, emphasis color, marker highlights, real screenshots. The contrast (scrappy footage + polished overlays) is what reads as "authentic but legit."

## 3. THE SFX MAP (inferred from waveform transients + cut points + on-screen device)
The waveform shows a continuous voice bed with sharp transient spikes riding on top — those spikes are the SFX. They cluster on cuts and on graphic pops; one heavier spike on the $50B slam; a clear silence dip at ~0:19.
| beat | SFX | evidence |
|---|---|---|
| 0:00–0:04 hook | low **drone** bed | smooth low envelope under the open |
| every cut (~2–3s) | short **whoosh** (vary 2 tones) | transient on each cut timestamp |
| ~0:11 $50B slam | deep **impact/boom** | tallest early spike, on the slam |
| 0:19 "but how?" | **(silence)** — hold the beat | waveform gap |
| 0:25–0:29 pain stack | **boing / tick** per line | rapid small spikes during the stack |
| 0:30 / 0:38 screenshots | **UI click / keyboard tick** | spikes on the app/billing frames |
| 0:38 "$9.80" | soft **ding** on the number | — |
| 0:41–0:44 headlines | **paper-whoosh + ding** per card | spike cluster on the headline region |
| 0:51–0:53 end card | **uplifting outro swell** | rising tail at the end |

→ Maps 1:1 onto our 14 specced SFX in `sfx/PROMPTS.md`. The new precision: **whoosh-per-cut at ~2–2.5s cadence**, a **real held silence at the "but how?" equivalent (our clips 13–14)**, and the **fast 5-in-4s cluster on our problem stack (clips 7–11)**.

## 4. WHAT THIS CHANGES FOR OUR EDIT
1. **Captions must use emphasis COLOR**, not flat white — our `ClipCaptions` already does gold/red/yellow; keep it, that matches.
2. **Stack the G2 pain-overlays** (run 3–4 in sequence so they accumulate) rather than one-at-a-time.
3. **Pace the problem stack FAST** (clips 7–11 ≈ 5 cuts in ~4s) and **hold a real silent beat** at clips 13–14.
4. **G4 marker-highlight:** consider a yellow marker-block sweep variant (closer to the reference) in addition to the orange underline.
5. **Keep the prop-mic** consistent across all shots; **keep VO continuous** across every cut.
