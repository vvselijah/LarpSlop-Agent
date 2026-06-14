# Pocket (heypocket.com) — research + DIY verdict (2026-06-13)

**Question (Elijah):** what is Pocket, what's inside, is it dropshipped, can it be reverse-engineered into
something better at home, can it feed Obsidian (button → voice note → transcription → vault note)?
**Real goal:** frictionlessly speak ideas into Obsidian without pulling out the phone or typing.

## What Pocket actually is (✅ verified: official site + YC + docs.heypocketai.com)
- **Hardware + app + cloud.** A 52g "card" recorder (3.4×2.2×0.2 in): 2 studio mics + 1 **contact mic**
  (captures phone-call audio), 64GB, **4-day battery**, USB-C (1.5h charge), MagSafe, **BLE + Wi-Fi**.
- **Flow:** press side button → records offline on-device → opens app → **syncs to Pocket's cloud** → AI does
  transcription (120+ langs), summaries, **mind maps**, action items; "Ask Pocket" Q&A. **Model-agnostic**
  (GPT-5, Claude, Gemini).
- **Price:** $99 launch ($199 reg) + **Pro $19.99/mo** (speaker labels, custom templates, unlimited history).
  Free tier = lifetime transcription + 90-day cloud history.
- **Company:** YC **W2026**, founded 2024, **team of 6**.

## Is it "dropshipped"? (🟡 strong inference)
The hardware is a **commodity ODM "AI recorder card,"** the same device class as **Mobvoi TicNote, Plaud
Note/NotePin, FoCase REC** — a crowded category of near-identical Chinese-ODM recorders (a "Plaud vs FoCase
vs TicNote" showdown exists). Pocket is **not literally a rebadged TicNote** (TicNote = 71g, aluminum, OLED,
3 MEMS mics, GPT-4o "Shadow"; Pocket = 52g, 2+1 mics, model-agnostic) — but a 6-person YC team did **not**
fab custom silicon; they **spec/brand a reference recorder** and put their app+cloud on top. **So: the
hardware is white-label/commodity; the actual product is the software.** (❌ exact chip/teardown not public.)

## Developer surface — can you change the button / build apps? (✅ from docs.heypocketai.com)
- **Real API:** Recordings (search, create-upload-URL, **get audio download URL**, list, details), Tags,
  Users, Org (API keys, templates, analytics, members), **Webhooks**, and notably a **"Pocket MCP Server"**.
- **You CANNOT:** reprogram the device button (no firmware/button-mapping endpoint), install on-device
  plugins, or use a native Obsidian/Notion connector (none exist).
- **You CAN:** pull recordings/transcripts programmatically (API + webhooks + their MCP) and route them
  anywhere yourself. So "apps" live **downstream of the button**, not on the device.

## Can it feed Obsidian? Two paths
1. **Buy Pocket, bridge it yourself:** Pocket button → its cloud transcribes → **webhook / Pocket MCP** →
   the hub's **Obsidian MCP** writes a templated vault note. Works, but you still pay $99 + $19.99/mo and
   your audio goes through Pocket's cloud.
2. **DIY (recommended) — you already own every hard part:** the hub has **faster-whisper installed** (local,
   free, 99 langs) and the vault has the **Obsidian MCP** wired. The only missing piece is a capture trigger.

## DIY build plan (the "tool nobody has," tuned to his vault) — phased
- **Phase 0 (no hardware, ~hours):** desktop hotkey / phone Shortcut → record a memo → `faster-whisper`
  transcribe → Claude cleans+titles+tags → **Obsidian MCP** writes an `idea`/`daily` note per the property
  contract. Frictionless capture from phone or desk, **$0, fully local/private, your schema.**
- **Phase 1 (~$5–15):** a cheap **BLE button** (or iOS Action Button / Apple Watch) fires the Phase-0 flow
  hands-free.
- **Phase 2 (~$15–30):** **XIAO ESP32-S3 Sense** (mic + BLE/Wi-Fi) = a true DIY always-on pocket recorder —
  this IS the reverse-engineered Pocket, but it dumps to **local Whisper + your vault**, no subscription/cloud.

## Verdict
- **For ambient/always-on capture of meetings & calls** (hands-free, 4-day battery, contact mic), Pocket's
  *hardware UX* is genuinely nice and hard to beat cheaply — but its **value is the polished app, not the chip.**
- **For Elijah's actual goal (speak ideas → Obsidian),** the **DIY pipeline wins**: native Obsidian, local
  +private (no cloud, no $19.99/mo), your templates, infinitely scriptable. The capture hardware is the only
  thing Pocket does that we don't already have — and a phone Shortcut or a $15 ESP32-S3 closes that gap.
- **Recommendation:** build **Phase 0 first** (proves the value with zero spend), then decide on a $15 button
  vs buying Pocket only if you want true away-from-everything ambient capture.

## Contact mic vs. iPhone native call recording (the both-ends question)
- **Pocket's trick:** the contact mic is a **vibration/bone-conduction pickup** against the phone body — it
  acoustically hears the earpiece (their voice) + your voice. Not a software call-tap; it sidesteps iOS by
  literally listening to the phone vibrate.
- **iPhone already does both ends natively:** **iOS 18.1+ Call Recording** (Settings → Apps → Phone → Call
  Recording) records **both ends** of a regular Phone-app call → saves **audio + transcript to Notes**, with a
  "This call will be recorded" announcement (two-party-consent compliance). Free, iPhone XS→17. (✅ verified.)
- **FaceTime/VoIP:** native recording is Phone-app only; use **Screen Recording w/ mic** to capture FaceTime
  (app audio) both ends — test it, Apple sometimes restricts. Cellular call audio is muted from screen recordings.
- **Implication:** for iPhone calls Elijah does NOT need Pocket — iOS native recording + transcript → pipe into
  the Obsidian pipeline. The contact mic only wins for in-person/ambient or non-iPhone calls. ⚖️ both-ends =
  two-party-consent in many US states.

## Cheaper + more-customizable version of the contact mic (✅ the real answer)
The "contact mic" is just a **piezoelectric Vibration Conduction Sensor (VCS)** on MagSafe — a piezo disc
reading phone-chassis micro-vibrations, bypassing the air AND the OS (so it's silent, both-ends, FaceTime
included; no announcement). **A piezo disc is $3–10.** The branded recorders (Plaud ~$159, TicNote ~$90,
Pocket $99) aren't meaningfully cheaper AND lock you to their app/subscription = LESS customization.

**DIY path (cheapest + most customizable):** piezo disc ($3–10) → solder to a 3.5mm/USB connector →
into a cheap recorder OR phone OR an ESP32-S3 → the hub's **faster-whisper** (already installed) → Claude
clean/title/tag → **Obsidian MCP** vault note. **~$5–20 total, no subscription, fully private, your templates.**
- Trade-offs (honest): raw piezo-on-glass can sound thin → needs a buffer/DSP tuning (Pocket/Plaud tune theirs);
  you need a way to get the signal in (cheap USB audio interface, or a recorder); fiddlier than plug-and-play.
- **Middle path:** buy ONE cheap subscription-free MagSafe recorder for the polished hardware, but route its
  exported audio into YOUR pipeline (faster-whisper → Obsidian) instead of paying for its app/AI. Good HW, your SW.
- **This = the same project as Phase 0/2 above:** capture (piezo or mic) → faster-whisper → templated vault note.

## Sourcing the white-label base (✅ for a non-hardware person — buy, don't build)
The MagSafe AI-recorder market is **mostly identical white-label clones on the same OEM hardware.** One named
base: **Dongguan Kinghal Electronic Technology Co. — "L518" magnetic voice recorder** (a VCS/bone-conduction
MagSafe recorder). Pocket/Plaud/TicNote-class devices are reskins of this category.
- **Search terms (Alibaba / 1688 / AliExpress):** `L518 magnetic voice recorder`, `MagSafe AI voice recorder OEM`,
  `bone conduction / VCS call recorder`, `magnetic recorder record both sides phone call`.
- **What to require in the listing (this IS the "customization" for a non-engineer):**
  1. **Exports raw WAV/MP3 you can access** — over USB mass-storage or app file-export. This is the hook: plain
     files → route into faster-whisper → Obsidian yourself. AVOID devices locked to a cloud-only app with no export.
  2. **Piezoelectric / bone-conduction (VCS) mic** — required for silent both-ends (incl. FaceTime), not just air mics.
  3. **No mandatory subscription** for basic recording; MagSafe/magnetic; USB-C; decent battery.
- **Single unit vs batch:** Alibaba is wholesale (MOQ). For ONE test unit, the same L518-class device sells on
  **AliExpress/Amazon under random brands for ~$30–60**. Use Alibaba only to actually white-label/brand a batch
  (not needed for personal use).
- **Customization reality:** you will NOT reprogram the button/firmware (closed OEM). Customization lives in your
  SOFTWARE: faster-whisper (own transcription) → Claude (title/tag) → Obsidian MCP (templated note). Buy the device
  for (a) the VCS hardware + (b) raw audio export; the hub does everything after. **Zero soldering.**

## VERDICT — buy vs build, and how to actually do it (the decision)
**Two separate needs were tangled together:**
1. **"Speak my ideas into Obsidian frictionlessly"** (his real #1 gap) → needs **NO special hardware.** A phone
   Shortcut / desktop hotkey → voice memo → faster-whisper → Obsidian. Build this first; **$0, no device.**
2. **"Silently record BOTH ENDS of calls"** (Pocket's actual unique value) → DOES need the VCS contact-mic hardware.

**Effort vs payoff (honest):**
- **DIY the hardware (piezo):** SKIP — not worth it for a non-engineer; ~$20 saved over a clone, lots of fiddling.
- **Build the SOFTWARE pipeline:** LOW effort, because the hub already has **faster-whisper installed + Obsidian
  MCP wired** — it's a capture trigger + a small folder-watch script + a vault template (a few hours, mostly
  reused from the `auto-clip` pattern). HIGH payoff: frictionless capture forever, local, private, $0 ongoing.
- **Buy Pocket ($70–80 + $19.99/mo ≈ $240+/yr):** lowest upfront effort, but cloud storage, monthly fee, NO
  native Obsidian (you'd still build a bridge), locked ecosystem. Doesn't actually solve need #1 without extra work.

**Recommendation:**
- **Build the software pipeline NOW** for need #1 (ideas → Obsidian). Don't buy anything for this.
- For need #2 (calls): buy a **~$30–60 white-label VCS clone with raw-file export** → feed the SAME pipeline.
  Local storage, no subscription. Only buy **Pocket** instead if you want plug-and-play polish and don't mind
  the cloud + monthly (which he said he dislikes) — at which point the white-label clone wins on every axis he cares about.

**How you'd actually do it (reality):**
1. **Trigger:** iOS Shortcut "Capture idea" (records a memo → saves to an iCloud/watched folder) OR a desktop hotkey.
2. **Pipeline (new hub engine, mirrors `auto-clip`):** watch the folder → `faster-whisper` transcribe → Claude
   clean/title/tag → **Obsidian MCP** writes a templated `idea`/`daily` note per the vault property contract.
3. **Calls (optional/later):** white-label recorder set to export WAV → same watched folder → same pipeline.
4. Run on demand, or chain into the 7 AM `Daily Agent Refresh.bat`.
This is the post-reset build (a `voice-capture/` engine + a skill). Gate any spend on Phase-0 proving the value first.

## REFINED REQUIREMENT (what he actually wants — 2026-06-13)
Not really about calls. The core want: a **discreet, silent, SCREENLESS, ONE-BUTTON** capture he can use
**on the go** — see/think something → press → speak → press stop → and **trust** it auto-flows to the vault:
faster-whisper transcribes → Claude summarizes/organizes/routes → Obsidian note. "Speak into Obsidian on
phone/PC" is NOT it — the value is the physical button + no screen + zero friction while out and about.
Calls (both-ends, silent) are the same flow via the contact mic.

## Two realistic capture front-ends (the SOFTWARE half is identical either way)
- **A) White-label VCS recorder card** (~$30–60, one button, no screen, local files, contact mic for calls).
  Best for a truly discreet *dedicated gadget* + silent call recording. **Ingest = dock/USB sync (or its WiFi
  export) → watched folder.** Trade-off: a sync step, so near-real-time, not instant; but local + no vendor cloud.
- **B) Phone + hardware button** (iPhone 15 Pro+ **Action Button**, or a ~$15 BLE button) → **iOS Shortcut**
  records → auto-saves to a watched iCloud/Drive folder → pipeline. **Instant to vault, no new cloud, no monthly,
  screenless** (don't look at the phone; it's in your pocket). Fastest path, works today, $0–15.
- **Pick:** want the dedicated discreet device + silent calls → **A**. Want instant + cheapest + no new cloud →
  **B**. Many do both (B for ideas, A for calls). Either way both feed the SAME `voice-capture/` engine.

## The pipeline to build (post-reset) — `voice-capture/` engine + skill, mirrors `auto-clip`
watched folder → `faster-whisper` transcribe → **Claude** (summarize, extract action items, title, tag, decide
vault type idea/daily/etc.) → **Obsidian MCP** writes the templated note (property contract). On-demand or 7 AM job.

## Sources
- https://heypocket.com/ · https://docs.heypocketai.com · https://www.ycombinator.com/companies/pocket
- Mobvoi TicNote (same device class): https://www.mobvoi.com/us/pages/mobvoiticnote ·
  https://www.umevo.ai/blogs/ume-all-posts/plaud-vs-focase-rec-vs-mobvoi-ticnote-the-ultimate-ai-voice-recorder-showdown ·
  https://phandroid.com/2025/07/09/mobvoi-ticnote-review-a-handy-little-ai-powered-tool-for-your-meetings/
- Obsidian voice paths: https://community.obsidian.md/plugins/voice ·
  https://www.obsidianstats.com/plugins/voicenotes-sync · https://apps.apple.com/us/app/voice-inbox/id6452678291
