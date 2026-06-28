# Elijah's media system — capture → edit → archive → backup

Researched + verified 2026-06-25. Grounds: Insta360 Luna Ultra (8K), Windows + DaVinci Resolve (free), 1TB internal (full), 20TB Seagate Expansion, one 512GB V60 card, ~200 videos/mo, 100-200GB+/session.

## The core problem
You're missing the **middle tier**. Right now it's camera → 1TB computer (full). You need a fast **working SSD** between the card and the archive, plus a real **backup** behind the 20TB. That's it.

## The 4 tiers
| Tier | Role | Hardware |
|---|---|---|
| **1. Capture** | Record + transport only, never storage. Rotate 2 cards. | microSD **UHS-I V30 A2** (NOT UHS-II) — Insta360-approved, ≤1TB |
| **2. Working / scratch** | Dump footage here, edit Resolve off it. | **4TB external NVMe SSD** (Crucial X9 Pro) or internal NVMe if a free M.2 slot |
| **3. Archive** | Permanent "always-have" cold storage of originals + masters. | Your **20TB Seagate** (already correct) |
| **4. Backup** | The copies that make loss survivable (3-2-1). | 2nd HDD offsite + cloud; later a NAS |

**Why edit off SSD not the HDD:** it's latency, not bandwidth. One 8K stream is only ~15 MB/s (any HDD handles that), but editing does constant random reads (scrubbing, timelines, cache) and an HDD's ~10-15ms seek vs SSD's ~0.16ms = stutter.

## Buy NOW (fixes ~90% of the pain)
1. **4TB external NVMe SSD — Crucial X9 Pro** (~$280-360, USB 3.2 Gen2 10Gbps, ~900 MB/s sustained). Edit off this. Holds ~18-36 of your sessions. *Ends the "deleting games" problem.* — OR an **internal NVMe** (Crucial T500 / Samsung 990 Pro 2-4TB) if your PC has a free M.2 slot: faster + cheaper/TB, no cable. Pick one, not both.
2. **UHS-II USB-C card reader** (~$40-80, ProGrade / OWC / Sony). ~3× faster offload (50-100GB: ~15-20min → ~5-7min).
3. **Correct microSD card(s) for the Luna** — SanDisk Extreme PRO **1TB UHS-I V30 A2** + a 512GB for rotation. *(See SD-card note below.)*
4. **TeraCopy** (free) — verified, checksummed copies. This is what makes "no quality loss" *provable*.

## Buy SOON
- **2nd 20TB HDD** (~$270-440), mirror the Seagate, keep it **offsite** → real 3-2-1.
- **Cloud:** Backblaze Personal **$99/yr** unlimited (backs up PC + attached externals — enable Extended Version History + reconnect the archive drive monthly or its cloud copy expires after 30 days), OR a Backblaze B2 / iDrive e2 bucket (~$4-7/TB/mo).

## LATER (at scale)
- **Synology DS423+** 4-bay NAS (~$450 diskless): SHR/RAID-5 + Btrfs **scrubbing** (catches silent bit rot a lone exFAT drive can't). Archive/backup box, not for live 8K editing (1GbE).

## ⚠️ The SD-card catch
The Luna's slot is **UHS-I microSD**. A **V60 card is UHS-II** — off Insta360's approved list (their manual warns UHS-II "may cause recording to stop" + corrupt files), and a full-size SD won't fit the microSD slot at all. UHS-II buys **zero** in-camera speed (the bus is UHS-I). **Action:** standardize on **UHS-I V30 A2 microSD** for the Luna; your UHS-II card is genuinely useful as a fast **desktop reader card** instead. Get a 2nd card regardless — one card = one failure from losing a whole shoot.

## Offload SOP (highest quality, provably lossless)
1. Card → **UHS-II USB-C reader** (not camera-as-drive).
2. **TeraCopy → COPY** (never move/cut) originals to the working SSD, **Verify ON**.
3. Wait for the **checksum double-check** = proof it's bit-for-bit identical.
4. Mirror that folder SSD → **Seagate** (verified) — now it's in two places before the card is touched.
5. Quick-scrub each clip; confirm file counts/sizes match.
6. **Format the card IN-CAMERA** (not Windows) before reuse.
7. Edit Resolve off the SSD; keep the camera-original MP4 as untouched master.
8. Project done → move raw + master to the Seagate, clear the SSD. Re-verify archive checksums ~every 6 months.

## 8K → Instagram (the honest answer)
- **IG caps everything at 1080p** for Reels — it downscales + recompresses 8K/4K server-side. True 8K on IG is **impossible**. "Closest to 8K" = the cleanest possible **1080p**, which you get by **controlling the downscale yourself** (never uploading raw 8K — biggest file, IG's crude resizer softens it most).
- **Resolve export:** 1080×1920 timeline → drop 8K on it → Deliver: **Force Sizing to Highest Quality** (Rec.709 Gamma 2.4) → **light sharpen on the 1080p output** (not the source) → MP4 **H.264 ~30 Mbps** (~50 if true 60fps), AAC, ≤90s. (Note: "Force Debayer to Highest Quality" does nothing for HEVC — RAW only.)
- **Where the 8K master pays off:** (1) **reframe latitude** — punch-in/crop many sharp 1080p verticals + horizontals from one shoot (great for 200/mo repurposing); (2) **YouTube** gives a 4K/8K source higher bitrate so even 1080p viewers see it sharper; (3) **agency + future-proof** master. Bonus: **1080p downscaled from 8K looks sharper than native 1080p** (supersampling) — so shooting 8K *is* your IG quality win.

## "Quality loss over time" — the truth
- **Myth:** files degrade from being stored/copied. They don't — a copy is bit-for-bit identical; an HDD stores the exact same quality as an SSD.
- **Real threat 1 — re-encoding:** quality is lost only when you re-compress (every export). Keep the camera-original master untouched; for multi-pass edits render a **ProRes 422 HQ / DNxHR** intermediate instead of re-rendering long-GOP H.265 repeatedly (that *does* accumulate generation loss).
- **Real threat 2 — drive failure / bit rot:** single drives die (~1.36%/yr); exFAT has no checksums. Fix = **3-2-1 + periodic checksum verify** (+ a scrubbing NAS later).

## Agency delivery (your `Clipping.md` to-do)
- **Never** email/Slack/WhatsApp/IG (all recompress). Use **object storage** — a Backblaze **B2** or **Wasabi** bucket stores files byte-for-byte, share via link (B2 free egress up to 3× stored; Wasabi no egress fee). For big one-off raw dumps: **MASV** ($0.25/GB downloaded, no size limit). Always send the **original MP4 or a ProRes/DNxHR master** — never an IG-downloaded clip.

## "Unlimited free cloud" reality
Doesn't exist. Google ended unlimited Photos (2021); the last T-Mobile/Google One loophole closes **Mar 31 2026**. Every "unlimited" offer = throttling/egress caps/purges. Real cheap cold storage: **iDrive e2 ~$4/TB/mo**, **B2 $6.95/TB/mo**, or flat **Backblaze Personal $99/yr**. **S3 Glacier Deep Archive ~$1/TB/mo** only for a last-resort "fire vault" (slow + paid retrieval).
