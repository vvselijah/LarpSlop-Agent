"""
News radar — a daily, fact-based NEWS-STORY surfacer on FREE, keyless sources.

SIBLING to trend-radar.py, but a DIFFERENT job:
  - trend-radar.py is an *acceleration detector*: "Bitcoin pageviews are 3x baseline."
    It tells you something is MOVING, but has no headlines, no stories.
  - news-radar.py delivers the ACTUAL STORIES (headline + source + date + 1-line
    summary + link) so Elijah has concrete, timely material to turn into a reel or
    carousel hook. Trend radar = "something moved"; news radar = "here is the thing."

The "fact-based / non-political" guarantee lives in SOURCE SELECTION, not in any API:
it reads primary-source + government RSS feeds (HuggingFace, arXiv, Federal Reserve),
which are inherently fact-first, then drops anything matching a per-niche political/
hype exclude list. A Claude editorial pass (a runtime/skill layer, NOT this engine) is
the intended Phase-1 refinement — this engine produces the clean candidate list and a
content-angle hook for each top story.

Sources (all keyless, stdlib + curl.exe; verified reachable 2026-06-14):
  - Curated RSS / Atom allowlist (PRIMARY)  -> real headlines, parsed with xml.etree
  - GDELT DOC 2.0 mode=artlist (SUPPLEMENT)  -> broad discovery, English-only,
    rate-limited and skipped GRACEFULLY when slow/flaky (it often is)

Writes:
  - news-report.md           ranked, deduped digest grouped by niche, each with a hook
  - data/news.json           history of seen URLs (so a story is never re-surfaced) + run log

Scoring (per story): recency (newer = higher) + niche relevance (keyword hits in
title/summary) + a small primary-source bonus. Excluded stories are dropped outright.
Dedup is by normalized URL across the whole run AND across past runs (news.json).

No keys, no accounts, no scraping, no heavy deps. NEVER publishes. Read-only.

Usage:  python news-radar.py
        python news-radar.py --no-gdelt     (skip the slow GDELT supplement)
        python news-radar.py --all          (include stories already seen on prior runs)
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote, urlparse
from xml.etree import ElementTree as ET

BASE = Path(__file__).resolve().parent
SOURCES = BASE / "news-sources.json"
DATA = BASE / "data"
HISTORY = DATA / "news.json"
REPORT = BASE / "news-report.md"

USER_AGENT = "news-radar/1.0 (elijah content research; local hub)"
HISTORY_KEEP = 1200       # cap remembered seen-URLs so news.json stays small
TOP_PER_NICHE = 8         # how many stories to surface per niche in the report
MAX_AGE_DAYS = 10         # only consider stories newer than this (it's a NEWS radar)
PER_FEED_CAP = 40         # newest-N per feed (some feeds dump their whole archive)
RECENCY_HALFLIFE_H = 36.0 # a story this many hours old scores ~half a fresh one
GDELT_SLEEP = 5.2         # GDELT asks for <= 1 request / 5 seconds
GDELT_MAXTIME = 22        # GDELT is often slow; cap hard and skip gracefully
GDELT_RECORDS = 25


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def fetch_text(url, max_time=30):
    """GET raw text via curl.exe (matches trend-radar's keyless path). Returns str or None."""
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run(
                ["curl.exe", "-s", "-g", "-L", "--max-time", str(max_time),
                 "-A", USER_AGENT, url],
                capture_output=True, text=True, encoding="utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            log(f"    curl error: {e}")
            return None
        out = (r.stdout or "").strip()
        if out:
            return out
        time.sleep(1.0 * attempt)
    return None


def fetch_json(url, max_time=30, rate_sleep=0.0):
    """GET + parse JSON. Returns parsed obj or None. Optional politeness sleep after."""
    txt = fetch_text(url, max_time=max_time)
    result = None
    if txt and txt[0] in "[{":
        try:
            result = json.loads(txt)
        except json.JSONDecodeError:
            result = None
    if rate_sleep:
        time.sleep(rate_sleep)
    return result


# ---- text helpers ---------------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def clean(text):
    """Strip HTML tags + collapse whitespace; safe for cp1252 report writing."""
    if not text:
        return ""
    text = _TAG_RE.sub(" ", text)
    text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'").replace("&apos;", "'")
                .replace("&nbsp;", " "))
    return _WS_RE.sub(" ", text).strip()


def one_line(text, limit=240):
    text = clean(text)
    if len(text) > limit:
        text = text[: limit - 1].rsplit(" ", 1)[0] + "…"
    return text


def norm_url(url):
    """Normalize a URL for dedup: drop scheme, trailing slash, common query cruft."""
    if not url:
        return ""
    u = url.strip()
    u = re.sub(r"^https?://", "", u, flags=re.I)
    u = re.sub(r"#.*$", "", u)
    u = re.sub(r"\?(utm_|ref=|source=).*$", "", u, flags=re.I)
    return u.rstrip("/").lower()


def domain_of(url):
    try:
        d = urlparse(url if "://" in url else "http://" + url).netloc.lower()
        return d[4:] if d.startswith("www.") else d
    except Exception:  # noqa: BLE001
        return ""


def parse_date(raw):
    """Best-effort parse of RSS pubDate / Atom updated / GDELT seendate -> aware UTC dt."""
    if not raw:
        return None
    raw = raw.strip()
    # GDELT compact form: 20260614T013000Z
    m = re.match(r"^(\d{8})T?(\d{6})?Z?$", raw)
    if m:
        try:
            dt = datetime.strptime(m.group(1) + (m.group(2) or "000000"),
                                   "%Y%m%d%H%M%S")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    # RFC822 (RSS pubDate)
    try:
        dt = parsedate_to_datetime(raw)
        if dt:
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        pass
    # ISO 8601 (Atom updated/published)
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ---- RSS / Atom -----------------------------------------------------------

def _findtext(el, names):
    """Find first child text matching any of `names` (namespace-insensitive)."""
    for child in el.iter():
        tag = child.tag.split("}")[-1].lower()
        if tag in names and (child.text or "").strip():
            return child.text.strip()
    return None


def _find_link(el):
    """RSS <link>text</link> OR Atom <link href=...> (prefer rel=alternate)."""
    alt = None
    for child in el:
        tag = child.tag.split("}")[-1].lower()
        if tag != "link":
            continue
        href = child.get("href")
        if href:  # Atom
            if child.get("rel") in (None, "alternate"):
                return href
            alt = alt or href
        elif (child.text or "").strip():  # RSS
            return child.text.strip()
    return alt


def parse_feed(xml_text, niche):
    """Parse RSS 2.0 or Atom into a list of story dicts. Returns [] on unparseable XML."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None  # signal: not valid XML (stale/404 HTML feed)
    items = []
    # RSS: channel/item ; Atom: feed/entry
    nodes = [e for e in root.iter() if e.tag.split("}")[-1].lower() in ("item", "entry")]
    for node in nodes:
        title = _findtext(node, {"title"})
        link = _find_link(node)
        if not title or not link:
            continue
        summary = _findtext(node, {"description", "summary", "content"}) or ""
        raw_date = _findtext(node, {"pubdate", "published", "updated", "date"})
        items.append({
            "title": clean(title),
            "url": link.strip(),
            "summary": one_line(summary),
            "date": parse_date(raw_date),
            "domain": domain_of(link),
            "niche": niche,
            "via": "rss",
        })
    return items


# ---- GDELT artlist (supplement) -------------------------------------------

def fetch_gdelt(query, niche):
    """GDELT DOC 2.0 artlist. Returns list of story dicts or [] (skips gracefully)."""
    q = quote(query, safe="")
    url = (f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}"
           f"&mode=artlist&format=json&maxrecords={GDELT_RECORDS}"
           "&timespan=3d&sort=datedesc")
    data = fetch_json(url, max_time=GDELT_MAXTIME, rate_sleep=GDELT_SLEEP)
    if not data or "articles" not in data:
        return None  # signal: GDELT unavailable/slow -> caller logs + skips
    out = []
    for a in data.get("articles", []):
        title, link = a.get("title"), a.get("url")
        if not title or not link:
            continue
        out.append({
            "title": clean(title),
            "url": link.strip(),
            "summary": "",
            "date": parse_date(a.get("seendate")),
            "domain": (a.get("domain") or domain_of(link)).lower(),
            "niche": niche,
            "via": "gdelt",
        })
    return out


# ---- scoring --------------------------------------------------------------

PRIMARY_SOURCE_HINTS = ("arxiv.org", "huggingface.co", "federalreserve.gov",
                        "sec.gov", "openai.com", "deepmind.google", "ai.googleblog.com")


def recency_score(dt, now):
    if not dt:
        return 0.3  # unknown date: small floor, don't let it win
    age_h = max((now - dt).total_seconds() / 3600.0, 0.0)
    # exponential decay with the configured half-life, clamped to [0,1]
    return 0.5 ** (age_h / RECENCY_HALFLIFE_H)


def relevance_score(story, cfg):
    text = (story["title"] + " " + story["summary"]).lower()
    kws = cfg.get("keywords", [])
    hits = sum(1 for k in kws if k in text)
    # diminishing returns: first few hits matter most
    return min(hits, 5) / 5.0, hits


def is_excluded(story, cfg):
    text = (story["title"] + " " + story["summary"]).lower()
    for bad in cfg.get("exclude", []):
        if bad.lower() in text:
            return bad
    return None


def score_story(story, cfg, now):
    rec = recency_score(story["date"], now)
    rel, hits = relevance_score(story, cfg)
    primary = 0.15 if any(h in story["domain"] for h in PRIMARY_SOURCE_HINTS) else 0.0
    # weighted: relevance is the gate, recency keeps it timely
    score = 0.55 * rel + 0.40 * rec + primary
    story["_score"] = round(score, 4)
    story["_rec"] = round(rec, 3)
    story["_hits"] = hits
    return score


# ---- content angle (hook seed) --------------------------------------------

def content_angle(story):
    """One-line hook seed. This is a deterministic STARTER; the Claude editorial
    layer (skill, not this engine) writes the real on-brand hook."""
    t = story["title"]
    short = one_line(t, 90)
    if story["niche"] == "money-finance":
        return f"Money angle: what \"{short}\" means for your wallet in 60 seconds"
    return f"AI/tech angle: break down \"{short}\" — why it matters, in plain English"


# ---- main -----------------------------------------------------------------

def main():
    args = set(sys.argv[1:])
    use_gdelt = "--no-gdelt" not in args
    only_new = "--all" not in args

    cfg_all = json.loads(SOURCES.read_text(encoding="utf-8"))["niches"]
    DATA.mkdir(exist_ok=True)
    hist = json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.exists() else {}
    seen = set(hist.get("seen_urls", []))
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    by_niche = {}          # niche -> [scored stories]
    feed_notes = []        # dead/empty feeds
    gdelt_notes = []       # gdelt skip notes
    counts = {"fetched": 0, "excluded": 0, "dupe": 0, "kept": 0}

    for niche, cfg in cfg_all.items():
        log(f"niche: {niche}")
        run_dedup = set()  # within-run dedup
        candidates = []

        # ---- RSS allowlist (primary) ----
        for feed_url in cfg.get("rss", []):
            xml_text = fetch_text(feed_url)
            if not xml_text:
                feed_notes.append(f"{niche}: feed unreachable (empty) — {feed_url}")
                log(f"  RSS unreachable: {feed_url}")
                continue
            stripped = xml_text.lstrip()
            if stripped[:1] != "<" or "<html" in stripped[:200].lower():
                feed_notes.append(f"{niche}: feed returned HTML/non-XML (stale URL?) — {feed_url}")
                log(f"  RSS not XML (stale?): {feed_url}")
                continue
            items = parse_feed(xml_text, niche)
            if items is None:
                feed_notes.append(f"{niche}: feed did not parse as RSS/Atom — {feed_url}")
                log(f"  RSS unparseable: {feed_url}")
                continue
            # Some feeds (e.g. HuggingFace) dump their entire archive. Keep only the
            # newest PER_FEED_CAP by date so this stays a *news* radar, not a crawler.
            items.sort(key=lambda it: (it["date"] or datetime.min.replace(tzinfo=timezone.utc)),
                       reverse=True)
            items = items[:PER_FEED_CAP]
            log(f"  RSS ok ({len(items)} kept of feed): {feed_url}")
            candidates.extend(items)

        # ---- GDELT supplement (discovery; graceful skip) ----
        if use_gdelt and cfg.get("gdelt_query"):
            g = fetch_gdelt(cfg["gdelt_query"], niche)
            if g is None:
                gdelt_notes.append(f"{niche}: GDELT slow/unavailable — skipped (RSS still covered it)")
                log(f"  GDELT skipped (slow/unavailable)")
            else:
                log(f"  GDELT ok ({len(g)} articles)")
                candidates.extend(g)

        # ---- filter + score + dedup ----
        scored = []
        for st in candidates:
            counts["fetched"] += 1
            # age window: it's a NEWS radar — drop anything older than MAX_AGE_DAYS
            # (stories with no parseable date are allowed through; relevance gate applies)
            if st["date"] and (now - st["date"]).days > MAX_AGE_DAYS:
                counts["stale"] += 1
                continue
            bad = is_excluded(st, cfg)
            if bad:
                counts["excluded"] += 1
                continue
            key = norm_url(st["url"])
            if not key or key in run_dedup:
                counts["dupe"] += 1
                continue
            run_dedup.add(key)
            if only_new and key in seen:
                counts["dupe"] += 1
                continue
            score_story(st, cfg, now)
            # require at least a little niche relevance OR a primary source,
            # so generic global-news noise can't top the list on recency alone
            if st["_hits"] == 0 and not any(h in st["domain"] for h in PRIMARY_SOURCE_HINTS):
                continue
            st["_key"] = key
            scored.append(st)
            counts["kept"] += 1

        scored.sort(key=lambda s: -s["_score"])
        by_niche[niche] = scored

    # ---- update history (remember everything we surfaced this run) ----
    newly = [s["_key"] for sts in by_niche.values() for s in sts]
    merged = list(dict.fromkeys(list(seen) + newly))[-HISTORY_KEEP:]
    hist["seen_urls"] = merged
    runlog = hist.setdefault("runs", [])
    runlog.append({"day": today, "ts": now.isoformat()[:19] + "Z",
                   **{k: counts[k] for k in counts}})
    hist["runs"] = runlog[-90:]

    # ---- write report ----
    out = [f"# News radar — {today}",
           "Fact-based, non-political AI/tech + money/finance stories from keyless "
           "primary-source + government feeds (curated RSS) plus an optional GDELT "
           "discovery pass. Each story has a starter **content angle** — the Claude "
           "editorial layer (a skill, not this engine) writes the real on-brand hook.",
           "",
           f"_Run: fetched {counts['fetched']} · excluded {counts['excluded']} "
           f"(political/hype) · {counts['dupe']} dupes/seen · **{counts['kept']} surfaced**. "
           + ("New-only (default; pass --all to re-show seen)._" if only_new
              else "Showing all incl. previously-seen._"),
           ""]

    any_stories = False
    for niche, stories in by_niche.items():
        nice = {"ai-software": "🤖 AI / Software",
                "money-finance": "💰 Money / Finance"}.get(niche, niche)
        out.append(f"## {nice}")
        if not stories:
            out.append("- (no new fact-based stories this run — feeds may be quiet, "
                       "or everything was already surfaced. Try `--all`.)")
            out.append("")
            continue
        any_stories = True
        for s in stories[:TOP_PER_NICHE]:
            datestr = s["date"].strftime("%Y-%m-%d %H:%M") + "Z" if s["date"] else "date?"
            out.append(f"### {s['title']}")
            meta = (f"_{s['domain'] or '?'} · {datestr} · via {s['via']} · "
                    f"score {s['_score']} (relevance {s['_hits']} kw, "
                    f"recency {s['_rec']})_")
            out.append(meta)
            if s["summary"]:
                out.append(f"> {s['summary']}")
            out.append(f"- **Angle:** {content_angle(s)}")
            out.append(f"- Link: {s['url']}")
            out.append("")

    if not any_stories:
        out.append("_No stories surfaced this run. If this persists, check the feed "
                   "notes below — and remember GDELT is often slow (RSS is the reliable "
                   "primary). Run with `--all` to re-show previously-seen stories._")
        out.append("")

    if feed_notes:
        out.append("## Feed notes (fix entries in news-sources.json)")
        out += [f"- {n}" for n in feed_notes] + [""]
    if gdelt_notes:
        out.append("## GDELT notes (supplement only — RSS is primary)")
        out += [f"- {n}" for n in gdelt_notes] + [""]

    out.append(f"_Generated {now.isoformat()[:19]}Z — curated RSS/Atom + GDELT, "
               "all free/keyless. GDELT data via gdeltproject.org. Read-only; never publishes._")

    HISTORY.write_text(json.dumps(hist, ensure_ascii=False, indent=0), encoding="utf-8")
    # cp1252-safe write: the report uses a few unicode glyphs (emoji, ellipsis);
    # write UTF-8 explicitly so they survive on this Windows hub.
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    log(f"report written: {REPORT}  ({counts['kept']} surfaced across "
        f"{len(by_niche)} niches)")


if __name__ == "__main__":
    main()
