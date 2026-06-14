# Clipping Campaign Folder — Build/Feasibility Research

**Date:** 2026-06-14
**Candidate id:** `clipping-campaign-folder`
**Source:** `obsidian/Elijah's vault/To do general/Clipping.md`
**Verdict:** **ADD-NOW** (Phase 0 is a thin packaging script over already-built auto-clip output) · **Confidence: high** · **Build effort: S** (Phase 0 ≈ half a day; full skill ≈ 1 day)

---

## Headline verdict

Build it. This is the single highest-leverage, lowest-risk addition in the queue because it has
**no new heavy dependencies, no model downloads, no API keys, no ToS/ban surface**, and it turns the
already-built-and-tested `auto-clip` engine into a live revenue deliverable. The "new" work is almost
entirely **filesystem packaging + a manifest/index file** — the kind of glue code that is safe on the
OneDrive disk.

The two open research questions in the vault note are now answered:

1. **Which service stores at near-original quality with ~unlimited capacity and easy hand-off?**
   → **Dropbox is the correct delivery layer; Google Drive is the acceptable cheaper fallback he likely already owns. Frame.io is overkill here.** (Details below.) All three preserve original quality (no transcode on upload); the differentiator is *handoff reliability and recipient adoption*, where Dropbox wins decisively for delivering to outside teams.
2. **One campaign or split by niche (software / ads / finance-motivation / viral-funny)?**
   → **Split by niche.** The industry guidance is explicit: separate niches each get their own brief, footage set, and reporting. This also matches the hub's own data — Money/Finance is Elijah's runaway view-leader and AI/Tech his best save-rate, so those niches deserve their own dedicated, larger folders.

The clippers' "quantity > only-the-best" advice is **half right**, and the research sharpens it: volume
helps, **but only if the folder is clean, well-labeled, and easy to work with.** Campaigns with clean,
easy-to-use, well-organized assets get **3–5x more clip submissions** than messy ones; if a clipper
can't easily work with your files they skip your campaign. So the deliverable is *not* a raw dump — it
is an **organized, indexed, niche-split library**. That is exactly the gap this candidate fills.

---

## What it is / what it does

A **packaging + delivery layer** that sits *after* the existing `auto-clip` engine. Today `auto-clip`
stops at loose files in `auto-clip/out/` (`<stem>_clip<NN>.mp4`, `_cap.mp4`, and a flat
`<stem>.manifest.json` with `rank/title/hook/duration`). There is no concept of:

- a **niche/category** for each clip,
- a **library folder structure** that accumulates across many source videos,
- a **human-readable index** an agency can skim,
- a **delivery target** (a synced cloud folder with a shareable link).

This candidate adds exactly those four things. It does **not** generate clips (auto-clip already does)
and it does **not** publish (CLAUDE.md rule 1 — it stops at a shareable folder/link, Elijah does the
final hand-off).

### What "clipping campaign" means (confirmed)

A clipping campaign = a brand/creator gives a network of independent editors ("clippers") a library of
source footage; clippers cut their own short-form edits and distribute them across TikTok / Reels /
Shorts / X, paid per-view (CPM) or per-result. The brand's job is to supply **clean, hook-rich,
well-organized source content** and a brief. ([reach.cat][1], [clippingculture][2])

### The partner (confirmed)

**organictrafficfunnel.com (OTF)** is a short-form **content distribution / posting** service —
self-serve packages **$500–$2,000/mo**, enterprise **$5,000+/mo**, guaranteeing monthly view minimums
(100K–25M+) and posting client content across TikTok/Reels/Shorts within 48h of a kickoff call. Content
is taken in via a **brand brief on a kickoff call** — i.e. they expect a clean shared link / folder, not
a streaming-quality re-upload. This *confirms* the deliverable: an organized, niche-split, link-shareable
folder is exactly what OTF (and Vinnie/Elton) will ask for. Their page does not document a specific
intake mechanism, so a Dropbox/Drive share link is the safe universal default. ([organictrafficfunnel.com][3])

---

## Storage / delivery decision (the core open question)

| | **Dropbox** | **Google Drive** | **Frame.io** |
|---|---|---|---|
| Re-compresses on upload? | **No** | **No** | **No** (but its *review player* streams proxies) |
| Large-binary reliability | **Best** (delta-sync, built for ProRes/RAW masters) | Weaker for big binary files | Good (camera-to-cloud, proxy uploads) |
| Handoff to an outside team | **Industry standard** — recipients already have it; no-account view/download share links | Works; share links; many already have it | "Client access, no account" but it's a *review* tool, not a bulk-handoff drive |
| Capacity | 9 TB+ business tiers, 2 TB/file | 2 TB starter, scalable | 2 TB starter |
| Monthly cost (rough) | ~$24/user | ~$12/user | ~$15/user |
| Best for | **Delivering a footage library to an external agency** | Cheap fallback / docs | Timecoded cut *review*, not what this needs |

**Recommendation:** Deliver via **Dropbox** if Elijah wants the most friction-free agency experience
(no-account download links, universal adoption, built for large media). **Google Drive is a perfectly
acceptable Phase-0 fallback** if he already pays for it — it does not re-compress either, and a shared
folder link works. **Skip Frame.io** — it's a review/approval tool, not a bulk-library handoff drive, and
adds cost/complexity for zero benefit here. ([toolsforfilm][4])

**Key correction to a common worry:** none of these three "compress your video on upload." The
compression fear usually comes from sending clips through *messaging apps* (iMessage/WhatsApp/Slack
inline) or platform DMs, which transcode. A cloud-drive **file** stays bit-identical. So the
quality-preservation requirement is satisfied by *any* of the three as long as the clips are uploaded as
**files to a folder** (not as media in a chat). The packaging script just needs to drop the original
1080×1920 H.264 MP4s into a synced folder.

---

## Integration sketch — how it composes with the hub

**Upstream (already built):** `auto-clip/` engine → `out/<stem>_clip<NN>.mp4` (+ `_cap.mp4`) and
`out/<stem>.manifest.json` (`rank/title/hook/duration`). The `auto-clip` SKILL already lets Claude tag
each clip's niche during highlight selection (it explicitly reasons over Money/Finance vs AI/Tech vs
funny). So **niche is already available at selection time** — we just need to persist it.

**New piece — `auto-clip/library.py` (or a `clip-library` skill wrapper):**

1. **Input:** one or more `out/*.manifest.json` files **+** a niche tag per clip. Cleanest path: extend
   the highlight `picks.json` schema with an optional `"niche"` field (one of
   `software | ads | finance-motivation | viral-funny | other`). `highlight.py` already writes
   `highlights.json`; carry `niche` through into the manifest. Zero new deps — it's a JSON field.
2. **Organize:** copy (not move — keep `out/` as the working dir) each clip into a library tree:
   ```
   clip-library/
     finance-motivation/
       <source-slug>__clip01__<short-title>.mp4
       ...
     software/
     ads/
     viral-funny/
     _index.csv          # flat catalog: niche, file, source, title, hook, duration, captioned(y/n)
     _index.md           # human-skimmable, grouped by niche, for the agency
     README-for-agency.md # one-pager: what's here, naming scheme, how to pick (auto-generated from brief)
   ```
   Filenames encode source + clip# + slugified title so a clipper can scan without opening files.
3. **Prefer the captioned/tightened variant** when present (`_cap.mp4` / `_tight*.mp4`), else the base
   `_clipNN.mp4`. Make this a flag (`--prefer captioned|raw`) — some agencies want clean source they can
   re-caption themselves (clippers re-edit anyway), so **raw, uncaptioned 9:16 may actually be the better
   deliverable**. Default to `raw` for the agency handoff, with captioned as an option.
4. **Delivery:** point `clip-library/` at a synced cloud folder. Two options:
   - **Simplest (Phase 0):** create `clip-library/` *outside* the OneDrive tree (e.g. a Dropbox or
     Google-Drive-synced local folder) so OneDrive doesn't double-sync large MP4s. The script takes a
     `--dest <path>` so the target is configurable and never hardcoded.
   - The script never uploads or shares automatically — it stages files; **Elijah creates/sends the
     share link himself** (consistent with the "no publish without per-action confirmation" posture).

**Data shapes (concrete):**
- Extend `picks.json` item: `{... , "niche": "finance-motivation"}` (optional; defaults `other`).
- `_index.csv` columns: `niche,file,source,clip_no,title,hook,duration_s,captioned`.
- `library.manifest.json`: `{ generated_at, dest, counts_by_niche, clips:[...] }` — so re-runs are
  idempotent (skip files already copied, append new ones — the library **accumulates** across many
  source videos, which is the whole point).

**Reuse, don't rebuild:** auto-clip (clips), the existing `manifest.json` writer, and the niche
reasoning already in the auto-clip SKILL. No caption-engine, no Remotion, no MCP needed for Phase 0.

---

## Phased build sketch

**Phase 0 — smallest safe thing (½ day): "stage what already exists."**
A `library.py` that reads existing `out/*.manifest.json`, asks Claude (or a simple CLI flag) for a niche
per clip, copies clips into `clip-library/<niche>/` with descriptive filenames, and writes `_index.csv`
+ `_index.md`. Dest defaults to a folder Elijah names (his Dropbox/Drive sync path). No schema changes
yet — niche supplied at package time. **This alone unblocks the vault to-do:** he can package the 6
existing test clips and any new auto-clip runs into a sendable folder today.

**Phase 1 — wire niche into the pipeline (½ day).** Add the optional `"niche"` field to `picks.json`
and carry it through `highlight.py` → `highlights.json` → `manifest.json`, so niche is captured at
selection time (where Claude is already reasoning about it) instead of re-asked at packaging. Update the
`auto-clip` SKILL step 3 to set `niche`.

**Phase 2 — the `clip-library` skill + agency one-pager (½ day).** A thin skill that orchestrates
"clip these N videos → sort into the library → regenerate the index → print a share-ready summary,"
plus an auto-generated `README-for-agency.md` (naming scheme, niche breakdown, counts, suggested brief
language pulled from the niche). Idempotent accumulation across many sources.

**Phase 3 (optional, later) — delivery niceties.** `--prefer captioned|raw`, dedupe by content hash,
a `--dest` validator that warns if the target is inside the OneDrive tree (double-sync), and optionally
a one-line `rclone`/Drive-CLI *stub* (Elijah-gated, never auto-runs) if he wants scripted upload later.
Not needed to ship.

---

## Risks / compliance / ToS

- **Ban / ToS risk: essentially none for the folder itself.** This stages *Elijah's own footage* into a
  cloud folder. No scraping, no platform automation, no publishing. The clipping *activity* has its own
  considerations (clippers must edit transformatively, disclosures, platform repost rules), but those
  live with the agency's brief, **not** with this storage/packaging tool. ([reach.cat — fair use][5])
- **OneDrive double-sync (real, mild):** if `clip-library/` lives inside the OneDrive tree *and* a
  Dropbox/Drive folder, large MP4s sync twice and can churn the disk. Mitigation: `--dest` defaults
  *outside* OneDrive; warn if it isn't. (Consistent with the hub's "keep heavy artifacts off the synced
  disk" rule.)
- **Disk/quota:** a real campaign library is many GB. Free Dropbox (2 GB) / Drive (15 GB) will fill fast;
  flag that a paid tier (~$12/mo Drive, ~$24/mo Dropbox) is the actual cost of this motion. This is a
  *business* cost decision for Elijah, not a code blocker.
- **Quality myth (addressed above):** the only way these clips lose quality is if sent through chat/DM
  transcoding. The script must deliver **files into a folder**, never as chat media. Documented in the
  agency README.
- **Honest low-value caveat:** the engineering here is genuinely small — it's `shutil.copy` + a CSV/MD
  writer + a niche tag. The *value* is real (unblocks active revenue), but nobody should over-build this
  into a heavy asset-manager. Resist scope creep (no DAM, no database, no web UI). A folder tree + two
  index files is the right altitude.

---

## Recommendation summary

Ship **Phase 0 now** — it's a half-day script that directly clears the vault to-do and feeds the OTF
partnership. Deliver via **Dropbox** (or Drive as fallback), **split by niche** with Money/Finance and
AI/Tech as the priority folders, deliver **clean files into a folder** (not chat), and lean toward
**uncaptioned 1080×1920 source** as the default agency hand-off (clippers re-edit) with captioned as an
option. No heavy deps, no torch/cv2/cloud-API, no ban surface.

---

## Sources

- [1] Clipping for Brands: How Companies Use Clippers in 2026 — reach.cat — https://reach.cat/blog/clipping-for-brands-how-companies-use-clippers/
- [2] What Is a Clipping Campaign? / Clipping Marketing Strategy — clippingculture.com — https://clippingculture.com/blog/what-is-clipping , https://clippingculture.com/blog/clipping-marketing-strategy
- [3] Organic Traffic Funnel (the partner) — https://organictrafficfunnel.com
- [4] Dropbox vs Frame.io vs Google Drive for Film Production — toolsforfilm.com — https://www.toolsforfilm.com/blog/dropbox-vs-frameio-vs-google-drive-film-production
- [5] Is Clipping Legal? Copyright & Fair Use Guide 2026 — reach.cat — https://reach.cat/blog/is-clipping-legal-copyright-fair-use/
- Google Drive organization for creators — https://influenceflow.io/resources/google-drive-organization-for-creators-the-ultimate-guide-to-streamlined-content-management/
- Building a clip library (2026) — https://joyspace.ai/creating-clip-library-organize-assets
- Best clipping platforms 2026 — https://www.ssemble.com/blog/best-clipping-platforms-2026
