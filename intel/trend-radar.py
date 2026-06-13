"""
Trend radar — a virality early-warning system on FREE, keyless data sources.

Detects topics accelerating BEFORE they peak, by comparing today's attention
signal against a rolling 28-day baseline (robust median + MAD), then confirming
with a multi-source / persistence rule so one-day blips don't fire alerts.

Sources (all keyless, verified reachable 2026-06-12):
  - Wikipedia Pageviews API  -> per-entity daily views (30+ day baseline in one call)
  - GDELT DOC 2.0 timelinevol -> news-mention volume (rate-limited: 1 request / 5s)
  - Hacker News API           -> software/AI front-page velocity

Writes data/trend-history.json (accruing signals so persistence works across runs)
and trend-report.md (ranked alerts). No keys, no accounts, no scraping.

Usage:  python trend-radar.py
"""

import json
import statistics
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent
WATCHLIST = BASE / "trend-watchlist.json"
DATA = BASE / "data"
HISTORY = DATA / "trend-history.json"
REPORT = BASE / "trend-report.md"

BASELINE_DAYS = 28        # rolling window for the baseline
RATIO_THRESH = 2.5        # today's value must be >= this multiple of baseline median
ZSCORE_THRESH = 3.0       # ...or this many robust-MAD sigmas above median
WIKI_MIN_VIEWS = 1500     # noise floor: ignore tiny-traffic articles
GDELT_SLEEP = 5.2         # GDELT asks for <= 1 request / 5 seconds
USER_AGENT = "trend-radar/1.0 (elijah content research; contact via local hub)"


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def get(url, rate_sleep=0.0):
    """GET via curl.exe; returns parsed JSON or None."""
    for attempt in (1, 2, 3):
        r = subprocess.run(
            ["curl.exe", "-s", "-g", "--max-time", "30", "-A", USER_AGENT, url],
            capture_output=True, text=True)
        out = (r.stdout or "").strip()
        if out and out[0] in "[{":
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                pass
        time.sleep(1.0 * attempt)
    if rate_sleep:
        time.sleep(rate_sleep)
    return None


def robust_stats(series):
    """Return (median, mad_sigma) where mad_sigma is a std-like scale."""
    if len(series) < 5:
        return (statistics.median(series) if series else 0, 0)
    med = statistics.median(series)
    mad = statistics.median([abs(x - med) for x in series]) or 0
    return med, 1.4826 * mad


def assess(latest, baseline_series):
    """Score one signal: ratio + robust z-score vs its baseline."""
    med, sigma = robust_stats(baseline_series)
    ratio = (latest / med) if med else 0
    z = ((latest - med) / sigma) if sigma else (99 if latest > med else 0)
    fired = (med > 0) and (ratio >= RATIO_THRESH or z >= ZSCORE_THRESH)
    return {"latest": latest, "baseline": round(med, 1),
            "ratio": round(ratio, 2), "z": round(z, 1), "fired": fired}


# ---- Wikipedia ------------------------------------------------------------

def wiki_series(article):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=BASELINE_DAYS + 5)
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           f"en.wikipedia.org/all-access/all-agents/{quote(article, safe='')}/daily/"
           f"{start.strftime('%Y%m%d')}/{end.strftime('%Y%m%d')}")
    data = get(url)
    if not data or "items" not in data:
        return None
    return [(it["timestamp"][:8], it["views"]) for it in data["items"]]


def scan_wikipedia(article):
    series = wiki_series(article)
    if not series or len(series) < 6:
        return None
    days = [v for _, v in series]
    # Wikipedia lags ~1 day; treat the last complete day as "latest",
    # baseline = the window before it.
    latest = days[-1]
    if latest < WIKI_MIN_VIEWS:
        # tiny article unless it's spiking hard off a tiny base — keep floor
        pass
    base = days[-(BASELINE_DAYS + 1):-1] if len(days) > BASELINE_DAYS else days[:-1]
    res = assess(latest, base)
    res["latest_day"] = series[-1][0]
    res["fired"] = res["fired"] and latest >= WIKI_MIN_VIEWS
    return res


# ---- GDELT ----------------------------------------------------------------

def scan_gdelt(phrase):
    q = quote(f'"{phrase}"', safe='')
    url = (f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}"
           "&mode=timelinevol&format=json&timespan=30d")
    data = get(url, rate_sleep=GDELT_SLEEP)
    time.sleep(GDELT_SLEEP)
    if not data or "timeline" not in data or not data["timeline"]:
        return None
    pts = data["timeline"][0].get("data", [])
    vals = [p.get("value", 0) for p in pts]
    if len(vals) < 6:
        return None
    latest = vals[-1]
    res = assess(latest, vals[-(BASELINE_DAYS + 1):-1])
    res["latest_day"] = (pts[-1].get("date") or "")[:8]
    return res


# ---- Hacker News ----------------------------------------------------------

def scan_hackernews(niches):
    ids = get("https://hacker-news.firebaseio.com/v0/topstories.json") or []
    hits = {}
    now = time.time()
    for sid in ids[:90]:
        item = get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
        if not item or item.get("type") != "story":
            continue
        title = (item.get("title") or "")
        tl = title.lower()
        score = item.get("score", 0)
        age_h = max((now - item.get("time", now)) / 3600, 0.5)
        velocity = score / age_h
        for niche, cfg in niches.items():
            kws = cfg.get("hn_keywords", [])
            if any(k in tl for k in kws) and velocity >= 8:
                hits.setdefault(niche, []).append(
                    {"title": title, "score": score, "vel": round(velocity, 1),
                     "url": f"https://news.ycombinator.com/item?id={sid}"})
    for niche in hits:
        hits[niche].sort(key=lambda h: -h["vel"])
    return hits


# ---- main -----------------------------------------------------------------

def main():
    watch = json.loads(WATCHLIST.read_text(encoding="utf-8"))["niches"]
    DATA.mkdir(exist_ok=True)
    hist = json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.exists() else {}
    hist.setdefault("signals", {})  # key -> [{day, ratio, fired}]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    strong, watchlist, errors = [], [], []

    def record(key, res):
        s = hist["signals"].setdefault(key, [])
        if not any(e["day"] == today for e in s):
            s.append({"day": today, "ratio": res["ratio"], "fired": res["fired"]})
        hist["signals"][key] = s[-60:]
        # persistence = consecutive recent runs that fired
        streak = 0
        for e in reversed(hist["signals"][key]):
            if e["fired"]:
                streak += 1
            else:
                break
        return streak

    for niche, cfg in watch.items():
        # Wikipedia (also collect which entities fired, for cross-source match)
        fired_wiki = set()
        for art in cfg.get("wikipedia", []):
            res = scan_wikipedia(art)
            if res is None:
                errors.append(f"wikipedia: '{art}' ({niche}) — no data")
                continue
            streak = record(f"wiki:{art}", res)
            log(f"  wiki {art}: latest {res['latest']:,} vs base {res['baseline']:,.0f} "
                f"({res['ratio']}x, z{res['z']}) {'FIRED' if res['fired'] else ''}")
            if res["fired"]:
                fired_wiki.add(art.lower())
                item = {"niche": niche, "source": "Wikipedia", "entity": art,
                        "detail": f"{res['latest']:,} views/day = {res['ratio']}× "
                                  f"28-day baseline (z{res['z']})",
                        "streak": streak}
                (strong if streak >= 2 else watchlist).append(item)

        # GDELT (news velocity) — cross-source confirm against Wikipedia
        for phrase in cfg.get("gdelt", []):
            res = scan_gdelt(phrase)
            if res is None:
                errors.append(f"gdelt: '{phrase}' ({niche}) — no data")
                continue
            streak = record(f"gdelt:{phrase}", res)
            log(f"  gdelt {phrase}: {res['ratio']}x (z{res['z']}) "
                f"{'FIRED' if res['fired'] else ''}")
            if res["fired"]:
                multi = any(phrase.lower() in w or w in phrase.lower() for w in fired_wiki)
                item = {"niche": niche, "source": "GDELT news", "entity": phrase,
                        "detail": f"news volume {res['ratio']}× baseline (z{res['z']})"
                                  + (" + Wikipedia agrees" if multi else ""),
                        "streak": streak}
                (strong if (streak >= 2 or multi) else watchlist).append(item)

    # Hacker News (software/AI discovery)
    hn = scan_hackernews(watch)

    # ---- write report ----
    out = [f"# Trend radar — {today}",
           f"Rule: a signal FIRES at ≥{RATIO_THRESH}× its 28-day median (or z≥{ZSCORE_THRESH}); "
           "**STRONG** = multi-source agreement or 2+ day persistence, else **watch**.", ""]

    out.append("## 🔴 STRONG — accelerating, confirmed")
    if strong:
        for a in sorted(strong, key=lambda x: -x["streak"]):
            out.append(f"- **{a['entity']}** ({a['niche']}) — {a['detail']}"
                       + (f" · rising {a['streak']} days" if a['streak'] >= 2 else ""))
    else:
        out.append("- (none today — baselines are still seeding on first runs; "
                   "persistence needs ≥2 days of history)")
    out.append("")

    out.append("## 🟡 Watch — single-source pops (may be blips)")
    if watchlist:
        for a in watchlist:
            out.append(f"- {a['entity']} ({a['niche']}) — {a['detail']} [{a['source']}]")
    else:
        out.append("- (none)")
    out.append("")

    out.append("## 🟢 Hacker News front-page (software/AI velocity)")
    if hn:
        for niche, items in hn.items():
            out.append(f"**{niche}**")
            for h in items[:5]:
                out.append(f"- {h['vel']} pts/hr ({h['score']}) — {h['title']} — {h['url']}")
    else:
        out.append("- (no niche-matching front-page stories right now)")
    out.append("")

    if errors:
        out.append("## Lookup notes (fix entries in trend-watchlist.json)")
        out += [f"- {e}" for e in errors] + [""]
    out.append(f"_Generated {datetime.now(timezone.utc).isoformat()[:19]}Z — "
               "Wikipedia + GDELT + Hacker News, all free/keyless._")

    HISTORY.write_text(json.dumps(hist, ensure_ascii=False), encoding="utf-8")
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    log(f"report written: {REPORT}  ({len(strong)} strong, {len(watchlist)} watch)")


if __name__ == "__main__":
    main()
