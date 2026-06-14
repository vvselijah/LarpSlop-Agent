# News Update System — Build / Feasibility Research

**Candidate id:** `news-update-system`
**Date:** 2026-06-14
**Source of request:** vault `Brainstorming/In the moment ideas.md` → "create news update system"
**Roadmap status:** STILL-TO-RESEARCH (Automation)

---

## Headline verdict: ADD-NOW (Phase 0), confidence HIGH

Build it. This is the single best-fit, lowest-risk candidate on the roadmap: it is a near-clone of
the engine pattern this hub already runs (`intel/trend-radar.py`), it rides infrastructure that
already exists (`Daily Agent Refresh.bat` + Task Scheduler), it uses **only keyless, stdlib + curl**
data paths I verified live today, it has **zero ban/ToS risk** (read-only RSS + a permissively-licensed
public dataset), and it feeds his #1 strength niches (AI/Tech, Money/Finance) with timely, fact-based
hooks that compose directly with `weekly-content-plan` and `carousel-builder`.

**Rough effort:** ~half a day for a useful Phase 0 (curated-RSS → one vault digest note). The Python is
~250 lines and structurally a fork of `trend-radar.py`. The only real work is **curation + editorial
filtering**, not plumbing.

**The one honest caveat:** the value is bounded by *editorial discipline*, not by fetching. Raw GDELT
is a global, multilingual, politics-heavy firehose (see "What it is" below — my live test pulled 3 G7
politics stories out of 5 for an "artificial intelligence" query). The "unbiased / fact-based /
non-politically-swinging" requirement is met by **source selection** (primary-source + government RSS)
plus **Claude as the editor** (the same `--provider agent` move auto-clip uses), *not* by any single API.
Get the source allowlist right and this is high-value; skip the curation and it's just another noisy feed.

---

## What it is / what it actually does

A daily-refresh **sibling engine** to `competitor-radar.py` / `trend-radar.py`:

> On an interval (the existing 7 AM scheduled task), pull the most important **fact-based,
> non-political** news across Elijah's niches — primarily **AI/Tech** and **Money/Finance** — plus
> general "important non-hype AI news," and **write it into the Obsidian vault** as readable notes.
> No publishing. No accounts. No paid keys.

Critically, this is **distinct from the trend radar**, which is an *acceleration detector*: it tells you
*"Bitcoin pageviews are 3× their 28-day baseline"* on a fixed watchlist. The trend radar does **not**
tell you *what actually happened* — it has no headlines, no article bodies, no "here's the story." The
news system fills exactly that gap: it delivers the **actual stories** (headline + source + 1-line
summary + link) so Elijah has concrete, timely material to turn into a hook. They are complementary:
**trend radar = "something is moving," news system = "here is the thing that moved."**

### Best 2026 approach + tools (researched, with licenses)

Two keyless source classes, ranked by fit. Both verified reachable from this machine today via the
same `curl.exe` path the trend radar already uses.

**1. Curated RSS allowlist (PRIMARY) — the "fact-based, non-political" guarantee lives here.**
The non-political requirement is an *editorial* problem, and the cleanest solution is to read from
**primary sources and government feeds**, which are inherently fact-first:

| Niche | Feed (keyless RSS) | Verified today |
|---|---|---|
| AI/Tech | `huggingface.co/blog/feed.xml` | ✅ clean RSS 2.0 XML |
| AI/Tech | `export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate` | (arXiv API, Atom) |
| AI/Tech | OpenAI / Google AI / DeepMind blog feeds | candidate (validate per-feed) |
| Finance | `federalreserve.gov/feeds/press_all.xml` | ✅ clean RSS 2.0 XML |
| Finance | SEC EDGAR / press feeds (`sec.gov/about/rss-feeds`) | candidate (gov, fact-only) |

  - **License/ToS:** standard RSS is published *for* syndication; reading titles/links/summaries is the
    intended use. Government feeds (Fed, SEC) are US public-domain works — zero restriction.
  - **Dependency weight:** **ZERO new deps.** RSS 2.0 / Atom parse with stdlib `xml.etree.ElementTree`.
    Do **NOT** add `feedparser` — its `sgmllib3k` dependency is an 11-year-stale, self-described
    "quick and dirty" Py3 port and is exactly the kind of fragile import this OneDrive-synced hub avoids.
  - **Gotcha I caught live:** `anthropic.com/rss.xml` returned an **HTML 404 page, not XML** — blog-listed
    feed URLs go stale. The engine must **validate each feed** (is the body XML? does it parse?) and
    **log dead feeds** instead of poisoning a note — exactly how `trend-radar.py` logs Wikipedia titles
    that return no data.

**2. GDELT DOC 2.0 `mode=artlist` (SUPPLEMENT / discovery) — broad coverage, needs heavy filtering.**
The trend radar already calls GDELT in `timelinevol` mode; switching `mode=artlist&format=json` returns
the **actual articles**. Verified live today — real fields: `title`, `url`, `seendate`, `domain`,
`language`, `sourcecountry` (up to 250 records, `timespan` down to 15 min).
  - **License/ToS:** GDELT terms (verified today): *"unlimited and unrestricted use for any academic,
    commercial, or governmental use of any kind without fee"* — only requirement is **attribution + a
    link to gdeltproject.org**. No ban risk, commercial/content use explicitly allowed.
  - **Honest limitation:** the raw feed is a **global, multilingual, politics-saturated firehose**. My
    live `"artificial intelligence"` query returned G7-summit stories in Russian, Spanish, and Italian.
    To use GDELT here you MUST constrain: `sourcelang:english`, an English-domain allowlist, exclude
    political phrasing, dedupe by domain+title. Treat it as **discovery for things the RSS allowlist
    missed**, not the primary feed. Same 1-request/5s politeness the trend radar already honors.
  - **Rate limit:** GDELT publishes no hard number; the trend radar already sleeps ~5s between GDELT
    calls — reuse that.

**Rejected on purpose:**
  - *Paid news APIs* (Newsdata.io, NewsAPI, etc.) — free tiers are throttled/branding-locked and add a
    key to manage; violates the hub's "local scripts + official sources over paid scrapers" rule.
  - *exa / tavily / firecrawl* — dead 401 keys; out of scope by mandate.
  - *Feedly / Daigest / hosted aggregators* — paid, cloud, and put a third party between Elijah and the
    vault. No.

### Windows + OneDrive feasibility

**Green across the board.** No torch, no cv2, no compiled extensions, no large model downloads, no
cloud calls, nothing that touches the slow synced disk beyond writing small `.md`/`.json`. It is HTTP
GET via `curl.exe` + stdlib JSON/XML + file writes — i.e. **byte-for-byte the trend radar's profile**,
which already runs clean in the 7 AM task. The "heavy imports hang on OneDrive" gotcha simply does not
apply to this engine.

---

## How it composes with the hub (integration sketch)

**Where it lives:** `intel/news-radar.py` (sibling to `competitor-radar.py` / `trend-radar.py`), with a
`intel/news-sources.json` allowlist Elijah edits freely (mirrors `trend-watchlist.json`).

**Wiring:** add one line to `Daily Agent Refresh.bat`:
```bat
echo --- News radar (fact-based niche news) ---
python "%ROOT%intel\news-radar.py"
```
No new scheduled task — it inherits the existing "IG Dashboard Daily Refresh" 7 AM run.

**Data shapes:**
  - **Input** — `intel/news-sources.json`:
    ```json
    {
      "niches": {
        "ai-software": { "rss": ["https://huggingface.co/blog/feed.xml", "..."],
                         "gdelt_query": "(\"AI agent\" OR \"open source model\") sourcelang:english",
                         "exclude": ["election", "senator", "lawsuit", "...political noise"] },
        "money-finance": { "rss": ["https://www.federalreserve.gov/feeds/press_all.xml"],
                           "gdelt_query": "(\"interest rates\" OR \"inflation\") sourcelang:english",
                           "exclude": ["..."] }
      }
    }
    ```
  - **State** — `intel/data/news-history.json`: `{seen_urls: [...]}` so a story is never written twice
    across runs (URL = dedupe key, same idea as the vault using IG permalink as the unique id).
  - **Raw output** — `intel/news-report.md`: ranked, deduped, English-filtered digest grouped by niche
    (headline · source domain · seendate · 1-line summary · link). This is the *engine's* artifact, and
    it is enough for Phase 0.

**The "Claude as editor" layer (Phase 1) — this is the differentiator and the hub's signature move.**
The engine produces a clean candidate list; **Claude does the editorial pass** (the same pattern as
auto-clip's `--provider agent` highlight brain and `niche-intel`'s synthesis): read `news-report.md`,
drop anything political/hype/duplicative, keep the genuinely useful items, and write them into the vault.

**Vault write target — respects the property contract (verified against `_templates/`):**
  - **Best fit:** one note per run in `20-Content/Ideas/` (or `70-Knowledge/Concepts/`) using the
    **existing `idea` template** — do **not** invent a `news` type (the contract forbids new property
    names without Elijah's say-so). The `idea` block (`type: idea`, `domain`, `stage: raw`,
    `status: open`, `date_captured`, `tags`) maps cleanly: `domain: ai-software`, body sections become
    "Top fact-based items today" + "Hook angles." File name e.g.
    `2026-06-14-AI-news-digest.md`.
  - Alternatively append a "News" section to that day's `10-Daily/YYYY-MM-DD.md`. **Recommendation:** a
    standalone dated `idea` note per niche — it's linkable, queryable by a Base, and survives next to the
    content ideas it's meant to seed.
  - **Hard rule honored:** writing vault notes only — **never publishes** (matches standing rule #1 and
    the auto-clip "stops at `out/`" precedent).

**Downstream composition (the payoff):**
  - `weekly-content-plan` already reads vault ideas → these digests become Monday's raw material.
  - `carousel-builder` turns a fact-based AI-news item into a saveable carousel (his untapped format).
  - `niche-intel` synthesis can fold "what actually happened" (news) alongside "what's accelerating"
    (trend radar) for a complete briefing.

---

## Phased build sketch

**Phase 0 — smallest safe thing (~half a day). Curated RSS → one digest `.md`. No vault write yet.**
  - `news-radar.py` + `news-sources.json` with ~3 verified feeds per niche (HuggingFace, arXiv-cs.AI,
    Fed press, etc.).
  - Fetch via the trend radar's `curl.exe` helper; parse with stdlib `xml.etree`; per-feed validation +
    dead-feed log; dedupe via `news-history.json`; write `intel/news-report.md`.
  - **Exit check:** run it, confirm a clean English digest with live, real links and no dupes on a
    second run. This is already useful on its own.

**Phase 1 — Claude editorial pass → vault `idea` note.**
  - A thin skill (or extend `niche-intel`) that reads `news-report.md`, filters political/hype, and
    writes a templated `idea` note to `20-Content/Ideas/`. Manual trigger first; verify the property
    block matches `_templates/idea.md` exactly.

**Phase 2 — GDELT discovery supplement + Daily Refresh wiring.**
  - Add `mode=artlist` GDELT with strict English/domain/exclude filtering as a *supplement* to catch
    big stories the RSS allowlist missed. Only after Phase 0/1 prove the signal is clean, add the
    `Daily Agent Refresh.bat` line so it runs unattended at 7 AM.

**Phase 3 (optional) — feedback + scoring.**
  - Tag which digest items actually became posts (close the loop via `reel-analytics`); lightly rank
    sources by how often they yield a used hook. Nice-to-have, not required.

---

## Risks / compliance / ToS

| Risk | Severity | Mitigation |
|---|---|---|
| **GDELT noise** (multilingual, politics-heavy firehose) | Med (quality) | English-only + domain allowlist + exclude list + Claude editor; treat GDELT as supplement, RSS as primary. Verified live as the real failure mode. |
| **Stale/dead feed URLs** (Anthropic RSS 404'd today) | Low | Per-feed XML validation + dead-feed log; degrade gracefully (trend-radar already does this for Wikipedia). |
| **"Non-political / unbiased" is subjective** | Med | Lean on primary-source + government feeds (inherently fact-first); Claude filters; Elijah owns the allowlist + exclude list. This is the design's whole point — own it explicitly. |
| **Ban / ToS** | **None** | RSS is published for syndication; Fed/SEC are public domain; GDELT explicitly permits commercial/content use with attribution. No scraping, no auth bypass, no rate abuse. |
| **Duplication of trend-radar** | Low | Different job (stories vs. acceleration); shares the curl helper but not the purpose. Document the distinction in the engine docstring. |
| **OneDrive / heavy-dep hang** | **None** | Stdlib + curl + small file writes only. Same profile as the engine that already runs daily. |
| **Vault contract violation** | Low | Reuse the `idea` template verbatim; never invent a `news` type/property; never overwrite human-written note bodies. |

---

## Sources

- [GDELT DOC 2.0 API debuts (modes, formats, maxrecords, timespan)](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
- [GDELT Project Terms of Use (verified permissive license)](https://www.gdeltproject.org/about.html)
- [GDELT DOC API Python client (alex9smith/gdelt-doc-api)](https://github.com/alex9smith/gdelt-doc-api)
- [Best AI News RSS Feeds 2026 (Readless)](https://www.readless.app/blog/best-ai-news-rss-feeds-2026)
- [Best Tech & AI RSS Feeds 2026 — feed URLs (daige.st)](https://daige.st/en/blog/best-tech-rss-feeds-2026)
- [Federal Reserve Board — RSS Feeds](https://www.federalreserve.gov/feeds/feeds.htm)
- [SEC.gov — RSS Feeds](https://www.sec.gov/about/rss-feeds)
- [Hugging Face Blog RSS](https://huggingface.co/blog/feed.xml)
- [feedparser sgmllib3k deprecation (why we avoid it)](https://github.com/kurtmckee/feedparser/issues/279)
- Live verification (this machine, 2026-06-14): GDELT `mode=artlist&format=json` returned real
  `title/url/seendate/domain/language/sourcecountry`; HuggingFace + Federal Reserve RSS returned clean
  parseable XML via `curl.exe`; `anthropic.com/rss.xml` returned an HTML 404 (stale-feed gotcha).
