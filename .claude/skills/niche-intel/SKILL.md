---
name: niche-intel
description: Run Elijah's competitive + trend intelligence sweep and turn it into ideas. Use when he asks "what's working in my niche", "what should I make about X", "check the competition", "what's trending", "any breakouts", or wants a content-intel briefing. Runs the competitor radar + trend radar + Meta ad-library scan, then synthesizes into vault-ready hooks.
---

# Niche intelligence sweep

Turn live competitive + trend data into specific, on-brand content ideas. Full
strategy and tool tiers: `CONTENT-INTEL-PROTOCOL.md`.

## Steps (workspace root: `C:\Users\elija\OneDrive\Desktop\ai agent team`)

1. **Competitor breakouts** — run `python intel/competitor-radar.py`, then read
   `intel/radar-report.md`. These are reels already proven to beat their own
   account's median — the strongest "format that works right now" signal.
2. **Trend velocity** — run `python intel/trend-radar.py` (~3 min), then read
   `intel/trend-report.md`. STRONG alerts = ship fast. Watch/HN = monitor.
   (If run today already, just read the report — don't re-run needlessly.)
3. **Ad creatives** (optional, for a specific topic) — use the `meta-ads` MCP
   `ads_library_search` (search_terms = the niche/topic, countries=["US"],
   ad_active_status="ACTIVE"). These are live ads competitors are paying to run —
   strong commercial-intent signal. **Save snapshot URLs immediately** (no archive).
4. **Cross-reference with his own data** — read `team/stats.md`: which of his
   categories already over-perform (Money/Finance, AI/Tech)? Prioritize ideas at
   the intersection of "trending now" × "his audience already rewards this."
5. **Synthesize 5–10 concrete ideas**, each in Elijah's voice (per `team/profile.md`):
   the hook line, the format (talking-head / b-roll / AI-generated), the angle, and
   the source signal it's riding (which competitor reel or trend fired).
6. **Save the keepers to the vault** as `hook` notes in
   `obsidian/Elijah's vault/20-Content/Hooks/` (copy the `_templates/hook.md` property
   block exactly; include the source permalink + why it worked). This is the durable
   swipe file the Bases query.
7. **Log one learning** to `team/memory.md` (dated, newest-first).

## Rules
- Read-only on every external source; **never publish or DM** (workspace CLAUDE.md rule 1).
- Scraping layers (Apify/Bright Data) are optional and not yet wired — if a gap needs
  them (IG hashtags, TikTok sounds), say so and point to `CONTENT-INTEL-PROTOCOL.md`
  Layer 3; don't fake the data.
- Speed is the edge: when a STRONG trend matches his niche, flag it as time-sensitive.
