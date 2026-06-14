# FinceptTerminal eval — research + build/feasibility plan

- **Candidate id:** `fincept-terminal-eval`
- **Date:** 2026-06-14
- **Source:** vault `40-Projects/LarpSlop/Cool repos to checkout.md` ("Bloomberg terminal?" → STILL-TO-RESEARCH → Intel)
- **Why he wanted it:** highest-leverage un-researched Intel item; directly serves his #1 niche (Money/Finance, most views). Idea: feed real market/finance data into `news-update-system` + `carousel-builder` + `niche-intel` for fact-based finance hooks.

---

## Headline verdict: SKIP FinceptTerminal itself — ADD-NOW a ~30-line keyless `finance-data` helper instead

**Do NOT install or integrate FinceptTerminal.** It is the wrong shape for this hub on every axis that matters here, and it actively violates two hard constraints. But the *underlying goal* — real, free, fact-checkable finance numbers for hooks — is legitimately high-value for his #1 niche and is trivially achievable WITHOUT Fincept, using the same free data sources Fincept itself wraps (`yfinance`, FRED, World Bank). Build that thin helper; skip the terminal.

| Decision | Verdict | Effort |
|---|---|---|
| Integrate FinceptTerminal (v4 native or pip v2) | **SKIP** | n/a (would be days + risk) |
| Build a light `finance-data` helper on yfinance + FRED | **ADD-NOW** | S (~half a day, Phase 0 = ~1 hr) |

---

## What FinceptTerminal actually is

An open-source "Bloomberg Terminal alternative" from Fincept Corporation. There are **two distinct things** behind the name, and conflating them is the trap:

### 1. Fincept Terminal **v4** (the current flagship)
- **Tech:** native **C++20 (55%) + Python (43%), Qt6** desktop GUI app, compiled to a single binary. Versions hard-pinned: CMake 3.27.7, Ninja 1.11.1, **Qt 6.8.3**, Python 3.11.9, MSVC 19.38. "Newer or older versions are unsupported and may fail."
- **Scale:** markets 423,000+ instruments, 100+ data connectors, 37 AI agents, order execution for 16 brokerages, CFA-level analytics. Uses **two Python venvs** (`venv-numpy1` for legacy QuantLib, `venv-numpy2` for AI agents + connectors). Recommends **16GB RAM** for local-LLM/QuantLib modules. Pulls Qt modules incl. `qtwebengine`, `qtmultimedia`.
- **License:** **dual — AGPL-3.0** for personal/academic, **commercial license required for "any business use (paid or free)"** explicitly naming "startups at any stage" and "consulting deliverables." "Unauthorized commercial use is subject to liquidated damages starting at USD 50,000 per organization per year."
- **Latest:** v4.1.0, released 2026-06-11.
- **Maintenance:** as of June 2026, "due to funding constraints… moving to **one update per month** and **no longer maintained on a daily basis**." Team has pivoted to a **subscription-based private edition** + a new project, **Quantcept**. Repo stays public.
- **Interface:** strictly a full native GUI. **No headless / library / data-only / TUI mode** documented.

### 2. `fincept-terminal` on **PyPI** (the older Python lineage)
- **Version:** 2.0.8, released **2025-09-04** (stale; superseded by the C++ v4).
- **License:** MIT.
- **Shape:** a **DearPyGui-powered GUI** investment terminal ("GUI-powered investment terminal that brings Bloomberg-level insights to everyone"). Still a desktop GUI app, not a clean importable data library. Wraps `yfinance`, `AkShare`, `QuantLib`, Agno/OpenAI agents.

**Neither artifact is a keyless data library.** Both are end-user GUI terminals. The free data it surfaces comes from connectors it wraps (Yahoo Finance, FRED, IMF, World Bank, DBnomics, AkShare) — those are independently and trivially accessible without Fincept.

---

## Why it fails THIS hub's diligence (the rescope, same pattern as prior candidates)

1. **Wrong shape.** The hub is a headless agent that calls light Python scripts as subprocesses and writes vault notes. Fincept is a heavyweight interactive **GUI app** (Qt6 native, or DearPyGui). There is no documented headless/library mode to call from a script. We would never run its UI.
2. **OneDrive/Windows constraint — fails hard.** v4 needs a pinned C++ toolchain (MSVC, CMake, Ninja, Qt 6.8.3 SDK), **two Python venvs**, `qtwebengine`, 16GB RAM. That is exactly the class of heavy, multi-GB, build-from-source install that hangs/corrupts on the OneDrive-synced tree (the same reason torch/cv2 are off-disk). A multi-venv Qt build on a synced disk is a support nightmare for zero gain.
3. **License is a real risk.** AGPL-3.0 + an explicit commercial-use clause naming "startups at any stage" with **$50k/yr liquidated damages**. Elijah runs a creator business and multiple ventures (Cruncrr, Artifacial, etc.). Even though we'd only *read data*, linking/integrating an AGPL terminal into a business workflow is precisely the use it gates. Not worth the ambiguity for data we can get MIT/public-domain elsewhere.
4. **Maintenance is fading.** Public edition down to monthly updates, team pivoting to a paid private edition + Quantcept. Betting an Intel pipeline on a cooling OSS project whose authors are steering users to a paid SKU is poor leverage.
5. **No keyless advantage over going direct.** Its "100 connectors" headline includes paid feeds (Polygon, Adanos sentiment). The genuinely free ones (Yahoo/yfinance, FRED, World Bank, IMF) we can hit directly with one light dependency each — no Fincept layer, no license, no Qt.

**Bottom line:** Fincept is a great *product* and a useful reference for *which* free sources exist, but importing it is all cost and no fit. Take the idea, drop the tool.

---

## The actual high-value extract: a keyless `finance-data` helper

Same outcome he wanted (real numbers for finance hooks), none of the cost:

- **`yfinance`** — keyless, free, pure-Python, pip wheel. Quotes/history/fundamentals for any stock, ETF, index, and crypto. ~few MB, no torch/cv2/GPU. (Research/educational use; Yahoo's unofficial endpoints — fine for our read-only, low-volume use.)
- **FRED** (`fredapi` or raw REST) — free API key (one Windows env var, per secrets rule), public-domain Federal Reserve economic data: CPI/inflation, GDP, unemployment, Fed funds rate, 10Y yield, yield-curve spreads. Authoritative and citable.
- **World Bank / IMF** — keyless REST JSON for macro indicators (stdlib `urllib`/`requests` only). Good for global stats hooks.

All light, all subprocess-friendly, all off the "hang" list. This is the rescoped candidate.

### How it composes with the hub

```
finance-data/fetch.py  (new, light)
   ├─ pull(symbol|series) -> normalized dict/JSON  (yfinance / FRED / WorldBank)
   ├─ writes a tiny finance-snapshot JSON to team/ or intel/out/
   └─ CLI: python fetch.py --quote NVDA  |  --fred CPIAUCSL  |  --wb NY.GDP.MKTP.CD US
        │
        ├─► niche-intel skill        : add a "finance facts" block to the intel sweep
        │                              (live numbers next to competitor/trend hooks)
        ├─► carousel-builder skill   : data-slide carousels ("CPI just hit X", yield-curve)
        │                              — saves-first format, fact-based = screenshot-worthy
        └─► news-update-system        : fact-check / timestamp finance hooks against real prints
```

- **Data shape:** a flat JSON record per pull — `{source, symbol/series, asof, value, prev, change_pct, unit, citation_url}`. Carousel-builder and niche-intel read that; nothing heavy crosses a process boundary.
- **Citation field is the point:** every number carries its FRED/Yahoo URL so hooks are fact-checkable (his algorithm rewards credibility-driven shares/saves; a wrong stat tanks reach).
- **MCPs:** none required. This is local-script-only, which is the hub's stated preference over paid scrapers/MCPs.

---

## Phased build sketch

**Phase 0 — smallest safe thing (~1 hr, do first):**
- `pip show yfinance` to confirm a clean wheel install (use `pip show`, not `python -c import`, per hub env note). Install into the existing hub Python, NOT a new venv.
- One throwaway script: fetch NVDA quote + CPI (FRED) + one World Bank series, print normalized JSON. Confirm it runs as a subprocess via PowerShell (not Bash — Bash lacks the env here) and doesn't hang on the OneDrive disk.
- Decision gate: if `yfinance` import is snappy and FRED key works, proceed. If anything hangs, stop and report.

**Phase 1 — the helper (~2-3 hr):**
- `finance-data/fetch.py` with the 3 providers + normalized JSON + CLI flags above. `README.md` inside the folder (folder-README pattern like `intel/`, `ig-dashboard/`).
- FRED key into a Windows env var via `setx` (e.g. `FRED_API_KEY`); never in files (OneDrive sync rule).
- A curated `series.json` of ~15 high-signal finance indicators for his niche (CPI, Fed funds, 10Y, S&P, BTC, unemployment, mortgage rate) so the agent has a ready menu.

**Phase 2 — wire into one skill (~2 hr, pick carousel-builder first):**
- Add an optional "pull a live data point" step to `carousel-builder` so a data-slide carousel can cite a real, current number. Highest-leverage because he runs zero carousels and saves-first data posts are his untapped format.

**Phase 3 (later, optional):** add the finance block to `niche-intel` sweep and a fact-check hook in `news-update-system`. Only after Phase 2 proves the data actually improves a post.

---

## Risks / compliance

- **FinceptTerminal license (the real one):** AGPL-3.0 + commercial clause w/ $50k/yr liquidated damages for business use. **Avoided entirely by not integrating it.**
- **yfinance ToS:** uses Yahoo's unofficial endpoints; intended for research/educational use, can break if Yahoo changes them. Mitigation: low volume, read-only, cache results, treat as best-effort with FRED/World Bank (official APIs) as the authoritative spine for anything published.
- **FRED:** free key, public-domain data, official API — clean. Key in env var only.
- **No publish risk:** helper only fetches + writes JSON/vault drafts; never posts. Standing per-action-confirmation rule untouched.
- **No heavy-dep risk:** zero torch/cv2/Qt/cloud; all light wheels + stdlib HTTP, subprocess-friendly, OneDrive-safe.

---

## Sources

- FinceptTerminal repo — https://github.com/Fincept-Corporation/FinceptTerminal
- Fincept Corporation org — https://github.com/Fincept-Corporation
- PyPI `fincept-terminal` (v2.0.8, MIT, DearPyGui) — https://pypi.org/project/fincept-terminal/
- DeepWiki — Installation & Setup (two-venv, yfinance/QuantLib/AkShare/Agno) — https://deepwiki.com/Fincept-Corporation/FinceptTerminal/2.1-installation-and-setup
- Project site — https://fincept.in/
- Feel.Trading overview (37 AI analysts, 100 sources) — https://feel.trading/en/news/6142944ca6
- Cybernews ("bring your own data") — https://cybernews.com/security/bloomberg-terminal-challenged-by-freemium-app/
- yfinance — https://github.com/ranaroussi/yfinance · https://pypi.org/project/yfinance/
- FRED API — https://fred.stlouisfed.org/docs/api/fred/
- Awesome free financial-data APIs (2026 availability) — https://github.com/jeff3388/awesome-financial-data-apis
