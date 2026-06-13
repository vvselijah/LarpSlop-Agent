"""
Competitor radar — official-API competitive intelligence for the accounts in
watchlist.json. No scraping: uses Instagram business_discovery via the same
token as ig-dashboard (live-verified 2026-06-12: per-post view_count,
like_count, comments_count on any public Business/Creator account).

Per run: pulls each watched account's followers + last 25 posts, flags
breakouts (a post doing >= BREAKOUT_X times that account's own median views,
with a minimum-views floor), accrues follower/post history in
data/competitors.json, and writes radar-report.md grouped by niche.

Usage:  python competitor-radar.py
"""

import json
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
WATCHLIST = BASE / "watchlist.json"
DATA = BASE / "data"
STORE = DATA / "competitors.json"
REPORT = BASE / "radar-report.md"

GRAPH = "https://graph.facebook.com/v25.0"
OWN_ACCOUNT_ID = "17841400159953101"   # @elijahaifl (the discovery anchor)
MEDIA_LIMIT = 25
BREAKOUT_X = 3.0      # post views >= this multiple of the account's median
MIN_VIEWS = 25000     # ...and at least this many views (noise floor)
CALL_SLEEP = 0.5


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def get_token():
    import os
    tok = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
    if not tok:
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                tok = winreg.QueryValueEx(k, "INSTAGRAM_ACCESS_TOKEN")[0].strip()
        except OSError:
            tok = ""
    return tok


def api(url):
    """GET via curl.exe with the URL fed over stdin (token stays off argv)."""
    for attempt in (1, 2, 3):
        r = subprocess.run(["curl.exe", "-s", "-g", "--max-time", "45", "--config", "-"],
                           capture_output=True, text=True, input=f'url = "{url}"\n')
        out = r.stdout.strip()
        if out:
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                pass
        time.sleep(1.5 * attempt)
    return {"error": {"message": "no response after 3 attempts"}}


def discover(username, token):
    from urllib.parse import quote
    fields = (f"business_discovery.username({username})"
              "{username,name,followers_count,media_count,"
              f"media.limit({MEDIA_LIMIT})"
              "{view_count,like_count,comments_count,caption,permalink,"
              "timestamp,media_type,media_product_type}}")
    return api(f"{GRAPH}/{OWN_ACCOUNT_ID}?fields={quote(fields, safe='(),.')}"
               f"&access_token={token}")


def views(m):
    return m.get("view_count") or 0


def main():
    token = get_token()
    if not token:
        log("FATAL: INSTAGRAM_ACCESS_TOKEN not set")
        return

    watchlist = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    watchlist.pop("_readme", None)

    DATA.mkdir(exist_ok=True)
    store = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
    store.setdefault("accounts", {})

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report = [f"# Competitor radar — {today}",
              f"Breakout rule: views ≥ {BREAKOUT_X}× the account's median of its "
              f"last {MEDIA_LIMIT} posts AND ≥ {MIN_VIEWS:,} views.", ""]
    errors = []

    for niche, usernames in watchlist.items():
        report.append(f"## {niche}")
        for u in usernames:
            r = discover(u, token)
            bd = r.get("business_discovery")
            if not bd:
                msg = r.get("error", {}).get("message", "unknown error")[:120]
                errors.append(f"- **{u}** ({niche}): {msg}")
                log(f"  ! {u}: {msg}")
                time.sleep(CALL_SLEEP)
                continue

            acct = store["accounts"].setdefault(u, {"followers": {}, "posts": {}})
            acct["followers"][today] = bd.get("followers_count")
            acct["niche"] = niche

            media = bd.get("media", {}).get("data", [])
            reels = [m for m in media if views(m) > 0]
            med = statistics.median([views(m) for m in reels]) if reels else 0

            # follower delta vs oldest snapshot we have
            snaps = sorted(acct["followers"].items())
            delta = (bd.get("followers_count") or 0) - (snaps[0][1] or 0) if len(snaps) > 1 else 0

            breakouts = []
            for m in media:
                pid = m.get("id")
                if pid and pid not in acct["posts"]:
                    acct["posts"][pid] = {"first_seen": today, "permalink": m.get("permalink")}
                if med and views(m) >= max(BREAKOUT_X * med, MIN_VIEWS):
                    breakouts.append(m)

            line = (f"### @{u} — {bd.get('followers_count', 0):,} followers"
                    + (f" ({delta:+,} since tracking began)" if delta else "")
                    + f" | median views: {int(med):,}")
            report.append(line)
            for m in sorted(breakouts, key=views, reverse=True):
                cap = (m.get("caption") or "").strip().replace("\n", " ")[:90]
                ratio = views(m) / med if med else 0
                report.append(f"- 🔥 {views(m):,} views ({ratio:.1f}× median) | "
                              f"{(m.get('timestamp') or '')[:10]} | {cap} | {m.get('permalink', '')}")
            if not breakouts:
                report.append("- (no breakouts this pull)")
            report.append("")
            log(f"  {u}: {bd.get('followers_count', 0):,} followers, "
                f"median {int(med):,}, {len(breakouts)} breakout(s)")
            time.sleep(CALL_SLEEP)

    if errors:
        report += ["## Lookup errors (fix usernames in watchlist.json)"] + errors + [""]
    report.append(f"_Generated {datetime.now(timezone.utc).isoformat()[:19]}Z — official "
                  "Graph API (business_discovery), no scraping._")

    STORE.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    log(f"report written: {REPORT}")


if __name__ == "__main__":
    main()
