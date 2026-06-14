# Vault "repos" → combined-tools research (2026-06-13)

**Source node:** `obsidian/Elijah's vault/Ai agent team/Cool repos to checkout.md` (4 repos).
**Goal (Elijah):** research each repo SLOWLY + carefully (independent, verified), then design NOVEL
combinations with the existing hub stack that **maximize personal daily-life/work efficiency** — personal
use, NOT a product to sell. The prize is "the real combination of tools to make a tool nobody else has."
**This doc is the baton** — written because context hit ~115%; the verified deep-dive runs post-reset.

## The 4 repos + FIRST-PASS fit (⚠️ UNVERIFIED — claims to confirm against the live repos post-reset)
| Repo | Headline claim | First-pass fit with the hub | Pre-research verdict |
|---|---|---|---|
| [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) | 100 pg/s PDF→MD, CPU-only, OCR 80+ langs, LangChain, Apache-2.0, ~8.6k★, zero-cloud | **STANDOUT** — local doc→vault intake engine | strong build candidate |
| [ASCILINE](https://github.com/YusufB5/ASCILINE) | video→packed-text over WebSocket; feed frames to local LLMs; offline/light | cheap VISUAL signal for `auto-clip` (today audio-only) + screen-rec monitoring | niche but interesting |
| [Telegram-Drive](https://github.com/caamer20/Telegram-Drive) | "unlimited" free storage via Telegram servers | offload large media (clips/renders/sources) OUT of OneDrive | useful scratch layer; real ToS/privacy caveats |
| [train-llm-from-scratch](https://github.com/FareedKhan-dev/train-llm-from-scratch) | GPT training from scratch on consumer HW | educational; low direct tool value | learning resource, weakest fit |

## The integration thesis (the "tool nobody has")
**A local, offline, vault-native knowledge + media intake pipeline.** `opendataloader-pdf` is the engine:
drop any PDF (contracts, sponsor agreements, books, research papers, brand decks) → clean Markdown →
auto-classified + **property-contract-templated vault note** → Claude summarizes → instantly searchable
second brain. Mirror the `ig-dashboard/` / `intel/` engine pattern (new `docintake/` + `data/` + README),
optionally chained into the 7 AM `Daily Agent Refresh.bat` (watch an inbox folder). Fits the
secrets-local / OneDrive constraint: **$0, no cloud, no API key.** Then layer:
- **ASCILINE** as a cheap visual channel so `auto-clip`'s highlight brain sees *picture* changes, not just audio.
- **Telegram-Drive** as the large-media offload so the OneDrive-synced tree stays lean (non-sensitive only).

## Per-repo research plan (post-reset — ONE workflow at a time per `docs/RESEARCH-PROTOCOL.md`; DIRECT WebFetch/firecrawl FIRST)
For EACH: verify headline claims (stars/license/perf) · **Windows install reality + deps** · maturity/activity ·
the SPECIFIC wiring into the hub (which existing skill/engine it composes with, the data shapes, the NEW combined capability).
1. **opendataloader-pdf** — confirm perf/OCR/license; **check runtime dep (JVM? Python?)** + Windows install;
   MD quality on a REAL contract/PDF; design the vault-note auto-template + classifier. → write a build PLAN.
2. **ASCILINE** — confirm it's real + maintained; the "feed to local LLM" path; fps/fidelity; realistic
   `auto-clip` visual-signal use vs the already-wired `gemini-video`/TwelveLabs (don't rebuild what we have).
3. **Telegram-Drive** — ToS/ban risk, setup (bot + account), reliability, privacy; scope to **non-sensitive
   large media only**; never a sole backup.
4. **train-llm-from-scratch** — confirm educational; any realistic tiny-local-model angle (voice/style draft,
   content-category classifier on the RTX 5070) or shelve as a learning resource. Be honest if it's just curiosity.

## Output (post-reset)
Verified findings + a build PLAN for the **doc-intake engine** (highest leverage), gated for Elijah's approval
before building. Log a dated learning to `team/memory.md`. Update `AGENT-TEAM-BLUEPRINT.md` tiers if warranted.
