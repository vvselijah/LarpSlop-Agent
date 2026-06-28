# SESSION COMPACT & HANDOFF — 2026-06-17

> **READ FIRST on resume.** Baton for the 2026-06-17 session. Supersedes `SESSION-COMPACT-2026-06-16.md`
> for current state. Personal single-user use. ✅ done · ⚑ needs Elijah · 🔨 next.

## 1. WHAT THIS SESSION WAS
Almost entirely **Elijah's first long-form YouTube video** — recording setup, the essay itself, and post (audio).
NOT about the Telegram bridge (that's still the 06-16 baton's blocker: Claude billing / subscription-auth switch).

## 2. MX BRIO 4K RECORDING (researched + verified)
- **Best-quality recording guide** delivered (OBS, NVENC, color). Machine: **RTX 5070** (confirmed via WMI) + good lights
  (ring light right, 2 Nanlite sticks front/back → match ALL to ONE color temp, lock manual WB to it).
- **4K BLOCKED in OBS:** camera only offers **YUY2/I420, max 2560×1440, NO MJPEG**. MJPEG is required for 4K.
  **USB is FINE** (1440p uncompressed can't fit USB 2.0 → link is SuperSpeed; cable/port ruled out). Cause is **software**:
  Windows Camera **Frame Server** stripping MJPEG, or an app holding the cam (**G HUB is running**). One Brio interface
  `MI_03` shows Error (likely benign, non-video).
- **🔨 4K FIX LADDER (run when NOT recording, stop when MJPEG appears at 3840×2160):** (1) Quit OBS; fully **Quit from tray**
  Logi Options+/Tune/**G HUB**/Camera/Discord/NVIDIA Broadcast/browser; unplug/replug; launch OBS first; **delete + re-add**
  the source; Custom → 3840×2160 → check Video Format. (2) If still no MJPEG = Frame Server: set REG_DWORD
  `EnableFrameServerMode = 0` in BOTH `HKLM\SOFTWARE\Microsoft\Windows Media Foundation\Platform` and
  `…\WOW6432Node\…\Platform`, reboot (REVERSIBLE = set back to 1; tradeoff: one app at a time, can break Win Hello / UWP
  Camera / OBS Virtual Camera). (3) Firmware update via Logi Options+. (4) Device reset (uninstall Brio + MI_03, rescan, reboot).
  **Offered to run the registry fix for him — he hasn't taken it yet.**
- **V1 was FILMED at 1440p** (fine — YUY2 uncompressed is actually cleaner color than the Brio's MJPEG 4K, which oversaturates).

## 3. AUDIO ENGINE (our repeatable method — NO separate program needed)
Local **ffmpeg mastering chain** → muxed back into the video (`-c:v copy`, same length). ElevenLabs **Voice Isolator** (MCP
`isolate_audio`) is the heavy-isolation option only for genuinely noisy audio.
- **The chain (filter:a):** `adeclip,highpass=f=80,agate=threshold=0.02:range=0.2:ratio=2:attack=15:release=300,equalizer=f=250:t=q:w=1:g=-1.5,equalizer=f=7000:t=q:w=2:g=-1.5,acompressor=threshold=-22dB:ratio=3:attack=5:release=150:makeup=2,loudnorm=I=-14:TP=-2:LRA=8,alimiter=limit=0.794:attack=2:release=70:level=false`
  → `-c:a aac -b:a 320k -ar 48000`. (loudnorm −14 LUFS = YouTube.) ffmpeg at `…WinGet\Links\ffmpeg.exe`, run via PowerShell.
- **Files:** RAW `C:\Users\elija\Videos\mx brio\2026-06-17 04-12-21.mp4` (33:47, 1440p30 h264, AAC stereo 48k). 
  **MASTERED** `…\2026-06-17 04-12-21_MASTERED_FINAL.mp4` (v4 chain, Elijah-APPROVED; same length so DaVinci cuts line up). The earlier `_MASTERED.mp4` = REJECTED over-processed v1 — delete it. **LESSONS:** (1) do NOT run heavy denoise (afftdn) on already-clean audio — it sounds watery/robotic. (2) This source **clipped at 0 dBFS** (recorded too hot) → `adeclip` repairs the peaks + `alimiter` caps them; tell Elijah to lower his **audio capture input gain** so peaks land ~-6 to -12 dB next time. (3) Room **reverb** can't be removed by any ffmpeg filter — only **ElevenLabs Voice Isolator** does, and its **API key is 401-dead** → ⚑ Elijah must set a valid `ELEVENLABS_API_KEY`.
- ⚑ Awaiting his ear: re-tune dials = compression / brightness+de-ess / denoise / warmth.
- **His cuts (he does them himself in DaVinci):** trim head to **2:41**; silence cut **8:30→9:30**; one stutter/pause to cut.

## 4. THE TWO VIDEO ESSAYS (the core artifact)
Vault scripts in `obsidian/Elijah's vault/20-Content/Scripts/`:
- **`Longform — The 5 Secrets to Success.md`** — holds the shared SHOOT METHOD + STRUCTURE PLAYBOOK + cross-cutting questions.
  5 points: Delusion · Consistency · God · Losing it all · Ego/regulation. Thesis: *"who do I have to become to handle what I say I want?"*
- **`What Success Before 21 Cost Me.md`** — family/time · unlived young-adult years · unrealistic money perspective · can't stop · comparison/never-enough.
Each note has: cliché-to-avoid → deeper frame → paradox → his real story per point, PLUS **"ELIJAH'S REAL ANSWERS (his voice)"** woven in.

### Elijah's real answers (captured, in his voice — USE THESE, they're the gold):
- **Worth it? 1000% yes**, do it again — **except** he'd take back wanting to grow up so fast / would live more of his childhood (keep the business). ← spine of BOTH videos.
- **Load-bearing points: Losing it all + God.**
- **DOGE at 17 = pure delusional early belief** (everyone said he'd lose it all; many did; he was early because he trusted the vision).
- **⚑ THE TESTIMONY (age 14)** — the moment faith became real: took LSD (familiar/pure) but that night was different; doesn't remember it; grandparents described possession-like sounds/vibrations; **grandfather's hand on his heart, "in the name of Jesus… stop"**; projectile vomiting everywhere; paramedics+police → altercation (beaten, tased twice); **felt he died and went to hell**, felt eternity-without-God, that every accomplishment was "a lie from the devil"; ~a year to remember any of it, still fragments. He says it's "a video in itself" — **he's right.**
- **Never-enough origin:** grew up poor (mom broke, dad couch-to-couch); was a kleptomaniac kid → caught repeatedly → learned karma's real → realized he can make things happen (neg or pos); 2015–17 rebellious-teen / rap-culture pull to want freedom early.
- **Satisfaction = the process/middle of building**, not the destination; spending money = ~1-day high. "Journey not destination."
- **CTA (his words):** the 1% are the 1% because 99% won't do the work consistently — just do it, don't stop, reinvest everything; and **start/strengthen a relationship with God**.
- He edited the God section in V1 himself, adding: *"if the pieces are falling into place that's usually a sign God is looking out!"* — keep it.

### ⚑ PENDING CREATIVE DECISIONS (I asked, he hasn't answered — ask on resume):
1. **The testimony:** condense in V1 + tease a standalone testimony video [my rec] · tell it fully in V1 · make the standalone FIRST. 
2. **Detail level** on the drugs + police-beating for a public/monetized YouTube video (name plainly but don't dwell [rec] · spiritual-only · full).
3. **Braid "God" + "losing it all" into ONE moment** (the night at 14)? [strong idea — makes that night the video's center]
4. Kleptomania beat in V2 — in or out? Film order: **5 Secrets first** (rec), then What It Cost.

## 5. 🔨 TRANSCRIPTION / SUBTITLES (decided approach, not yet done)
- Use **Whisper large-v3** (local, via `hyperframes-media` transcribe) OR **ElevenLabs Scribe** (`speech_to_text`) → outputs `.srt`/`.vtt` + `.txt` + word-level.
- **Run on the FINAL CUT, not the raw** (cuts shift all timestamps). Upload our own `.srt` to YouTube (beats auto-captions; control name spellings).
- Plain-text **script** can be pulled from the raw now if he wants it for the description/title while editing.

## 6. CONTEXT MECHANICS NOTE
The context %-hook **over-reads ~5× on the 1M window** (it hit "111%" while real usage was fine). Don't panic at the number;
do still write a baton + compact at genuine clean boundaries. This session crossed into "long" territory → compact recommended.
