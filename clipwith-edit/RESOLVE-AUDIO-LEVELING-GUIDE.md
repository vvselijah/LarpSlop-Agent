# Resolve Audio Leveling — total-beginner click guide ("Introducing ClipWith")

Goal: make every clip's voice sit at the same, even level despite the handheld Røde + different rooms.
Order matters — do the sections top to bottom. (Resolve Studio 21.)

**Orientation:** the 7 buttons along the very bottom = "pages." **Fairlight** = the audio page (do most of this there).
Panels are toggled by buttons in the **top toolbar** of the Fairlight page: **Effects** (top-left), **Mixer** + **Meters** (top-right).

---

## STEP 0 — Make sure you're on the Røde audio (not the camera)
If you imported the separate Røde `_backup.wav` files, your good audio is those. If your timeline clips are
playing the camera's audio, swap to the Røde. (If you only have the camera audio, just continue — the steps
still work, the Røde just sounds better.)

## STEP 1 — Normalize all clips to the same loudness (the big evener)
1. Go to the **Edit** page (bottom toolbar) — easiest place to select clips.
2. Click the **first** audio clip in the timeline, then **Shift-click the last** (or press **Ctrl+A**) to select them all. They turn red-outlined.
3. **Right-click** any selected clip → **Normalize Audio Levels…**
4. In the dialog:
   - **Normalization Mode:** choose **ITU-R BS.1770-4** (a loudness standard, NOT "Sample Peak").
   - **Target Loudness Level:** type **-16** (LUFS).
   - **Set Level:** click **Independent** ← this is the key one; it levels each clip on its own to the same target.
5. Click **Normalize.** Every clip is now at matched loudness. Play through — already way more even.

## STEP 2 — Open the audio page + mixer
1. Click **Fairlight** (bottom toolbar).
2. Top-right, click **Mixer** if it isn't already showing. The Mixer = vertical "channel strips," one per track, plus a **Bus 1 / Main** strip on the far right.
3. Your dialogue is probably all on track **A1**. You'll add the next effects to the **A1 strip** so they apply to every clip on it at once. (If your audio is split across A1, A2… repeat Steps 3–6 on each, or ask me about buses.)

## STEP 3 — High-pass filter (kills handheld rumble) via the track EQ
1. On the **A1** channel strip in the Mixer, find the small **EQ** box (a little curve graph, upper area of the strip). **Double-click** it → the **Equalizer** window opens.
2. Make sure the EQ is **ON** (the power/enable button in that window is lit).
3. Click **Band 1** (far-left band). Change its **shape** to **High Pass** (the icon that's a downward ramp on the left). 
4. Set its **Frequency** to about **80–100 Hz.** (Drag the band's dot, or type the value.) This removes the low "thump/handling" noise from gripping the mic without touching the voice.
5. Close the window.

## STEP 4 — Compressor + Limiter (evens the in-clip swings) via Dynamics
1. On the **A1** strip, find the **Dynamics** box (just below EQ, another little graph). **Double-click** it → the **Dynamics** window opens. It has sections: Expander/Gate · **Compressor** · **Limiter**.
2. **Compressor:** turn it **ON** (click its enable/power button).
   - **Ratio:** ~**3:1**
   - **Threshold:** drag down to about **-24 to -18 dB** until, while playing, the **gain-reduction meter** dips ~**3–6 dB** on the louder words. That's it working.
3. **Limiter:** turn it **ON.**
   - **Threshold/Level:** **-1.0 dB** (a safety ceiling so nothing peaks/clips).
4. Close the window.

## STEP 5 — Dialogue Leveler (auto-evens the close/far handheld variation) — Studio FX
1. Top-left, click **Effects** to open the **Effects Library** panel.
2. Expand **Audio FX → FairlightFX.** Find **Dialogue Leveler.**
3. **Drag** "Dialogue Leveler" onto the **A1 track header** (the name area at the left end of the A1 track in the timeline) — OR drop it into the **Inserts** area at the **top of the A1 mixer strip.** Its control window pops open.
4. Leave it on default to start; if clips are still uneven, raise its amount/strength. This rides the level up and down automatically — the main fix for handheld distance changes.

## STEP 6 — Voice Isolation (matches the different room tones) — Studio FX
1. Still in **Effects Library → FairlightFX**, find **Voice Isolation.**
2. **Drag** it onto the **A1 track** (same as Step 5) — put it **above/before** the others ideally (it cleans first).
3. In its window, raise the **amount** until the background room differences fade but the voice still sounds natural (don't overdo it — too much sounds robotic). This makes all the rooms sound like one space.

## STEP 7 — Check the final loudness
1. Top-right, click **Meters** (or look at the **Bus 1 / Main** strip).
2. Find the **Loudness** meter and watch the **Integrated (LUFS)** number while playing the whole thing.
3. Aim for about **-14 to -16 LUFS** integrated. (Instagram re-normalizes anyway, so *evenness between clips* matters more than the exact number.)

---

### Quick recap (the order)
Røde audio → **Normalize (Independent, -16 LUFS)** → **EQ High-Pass 80–100 Hz** → **Compressor 3:1 + Limiter -1 dB** → **Dialogue Leveler** → **Voice Isolation** → check **LUFS ~-14 to -16.**
Steps 1, 4, and 5 do 90% of the evening-out. If you only do three things, do those.

### If an effect window vanishes
Effects you added live in the strip's **Inserts** area (top of the A1 mixer strip) — **double-click the effect's name** there to reopen its controls. Right-click an insert → **Remove** to delete it.
