# Reel 1 — the live one-prompt (rebuild our real site)

**The reel:** clipwith.ai is already live. On camera you say *"watch me rebuild our entire landing
page with one prompt"* — paste ONE prompt into Claude Code, hit enter, and a full page that mirrors
clipwith.ai builds itself. Honest: the real site is the reference; the AI build is the flex.

## Setup (off camera, 60 sec before record)
1. Have **clipwith.ai open in a browser** (this is the "before" you show first).
2. Empty folder open in Claude Code; a second browser window ready for the reveal.
3. Record -> show the real site -> paste the prompt -> let it build -> open the file -> compare.

> Reference build already exists at `carousel-builds/reel1/landing/index.html` (this is what the
> prompt produces — a clean rebuild of clipwith.ai). Screenshots: `landing/_hero.png` (the AI build),
> `landing/_real_hero.png` (the live site, for the before/after).

---

## PASTE THIS (one prompt)

```
Rebuild my company's landing page as a single self-contained `index.html`. It's "ClipWith.ai", an
agentic AI video editor whose assistant is named "Clippy" — you upload footage (or paste a Twitch/Kick
VOD link), tell Clippy how you want it cut in plain English, and get a professional, post-ready edit
back in multiple formats.

Style: premium dark mode, near-black (#050505) background, orange accent (#f5a623 -> #e8760a gradient)
with gold (#caa54a) stat numbers, subtle radial orange glow. Fonts via Google: Syne (800) for headings,
Outfit for body, JetBrains Mono for small labels.

Sections, top to bottom:
1. Sticky blurred nav: play-triangle logo "clipwith.ai", links (Features, How it works, The difference,
   FAQ), "Sign in", and an orange "Try free" button.
2. Hero (two columns): left = pill eyebrow "The agentic AI video editor" with a live green dot, huge
   headline "Edit to post in minutes." with "in" in orange, the subhead above, a primary "Try free, no
   card required ->" button + a "How it works" text link. Right = a friendly orange retro ROBOT mascot
   on a pedestal labelled "CLIPPY" with a glowing halo.
3. A 4-up stat row: "60s / First render", "14x / Faster than Premiere / CapCut", "4K / Export quality",
   "3x / Formats per prompt" — big gradient numbers in cards.
4. Features section titled "Tools that no other editor ships." — 7 cards: "Visual AI, not just
   transcripts" (watches every frame, not the transcript), "Paste a stream URL, get clips" (Twitch/Kick
   VODs), "Eye contact correction" (redirects teleprompter gaze to camera), "Color grading from a
   prompt", "Full AI audio stack" (VO, SFX, music), "Background removal + lip-sync dub (20+ languages)",
   and a wide "Remembers your style" card with a CTA button.
5. "How it works": 3 cards — Upload or paste a link / Tell Clippy the edit / Get it back, ready to post.
6. Pricing titled "Fire your editor.": two cards — a human editor "$1,500/mo" (struck through) vs
   ClipWith "$49/mo flat", with a green "Save $17,400/yr" badge.
7. FAQ titled "Good questions. Real answers." with these rows: difference vs Descript/CapCut, how
   pricing works, formats & resolutions, the OrganicTrafficFunnel partnership, running out of credits
   mid-edit, what a credit buys.
8. Final CTA card (glowing): "Edit to post in minutes." + email input + orange "Try free ->".
9. Footer with logo + links.

Make it genuinely premium: generous spacing, rounded glassy cards with 1px hairline borders, soft
gradients, big bold display type, deep shadows and orange glow on the hero + CTA. Desktop-first,
~1180px max width. No frameworks — HTML + CSS only (Google Fonts via <link>), inline SVG icons.
Output the complete file.
```

---

## On-camera tips
- Open on the REAL clipwith.ai for ~1s ("this is our actual site") — then cut to pasting the prompt.
- Let the code stream as it builds — that motion is the b-roll. Speed-ramp it.
- Reveal beat: open the generated file, then put it side-by-side with the live site.
- Narrate the outcome, never the code: "one prompt rebuilt our whole page."
