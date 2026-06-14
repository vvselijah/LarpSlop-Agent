"""
Viral radar — cross-niche top-performer board for the accounts in watchlist.json.

Sibling of competitor-radar.py. Where competitor-radar flags a post as a
*breakout relative to its own account's median*, viral-radar answers a different
question Elijah keeps asking: "show me the top best-performing posts of each
niche, ranked, so I can see what's actually winning and replicate it."

It does this on the SAME official, ToS-clean data path as competitor-radar —
Instagram `business_discovery` field-expansion via curl.exe (token fed over
stdin, never on argv) — and ranks every pulled post by VIEW COUNT (the 2026 IG
algorithm ranks reach/views, not likes), with engagement-rate as the secondary
sort. No scraping, no new dependencies, no hashtag-search budget burned.

Per run (one focused pass over watchlist.json — no aggressive looping):
  - pull each watched account's followers + last 25 posts via business_discovery
  - build a per-niche leaderboard of the top posts BY VIEWS (eng-rate as tiebreak)
  - compute each post's engagement rate = (likes + comments) / views
  - SUGGEST accounts worth adding to the watchlist: among the watched accounts,
    those whose median views punch above their follower size (high views-per-
    follower) — i.e. small accounts over-performing — are flagged for promotion.
  - write viral-report.md (ranked niche boards + suggestions) and accrue a light
    history in data/viral.json so "which winners keep winning" is visible later.

READ-ONLY: only Graph API GET reads (business_discovery). It never calls any
publish / comment / DM / write endpoint, and it never edits the other engines.

Usage:  python viral-radar.py
"""

import json
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent
WATCHLIST = BASE / "watchlist.json"
DATA = BASE / "data"
STORE = DATA / "viral.json"
REPORT = BASE / "viral-report.md"

GRAPH = "https://graph.facebook.com/v25.0"
OWN_ACCOUNT_ID = "17841400159953101"   # @elijahaifl (the discovery anchor)
MEDIA_LIMIT = 25          # posts pulled per account
TOP_PER_NICHE = 8         # leaderboard depth per niche
TOP_OVERALL = 12          # cross-niche "biggest hits" board depth
MIN_VIEWS = 5000          # noise floor: ignore tiny posts in the boards
# An account is "worth promoting" if its median views are at least this many
# times higher than the cohort-wide median views-per-follower would predict
# (i.e. it punches above its follower weight).
OVERPERFORM_X = 1.5
CALL_SLEEP = 0.5          # gentle pacing; mirrors competitor-radar


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
    fields = (f"business_discovery.username({username})"
              "{username,name,followers_count,media_count,"
              f"media.limit({MEDIA_LIMIT})"
              "{view_count,like_count,comments_count,caption,permalink,"
              "timestamp,media_type,media_product_type}}")
    return api(f"{GRAPH}/{OWN_ACCOUNT_ID}?fields={quote(fields, safe='(),.')}"
               f"&access_token={token}")


def views(m):
    return m.get("view_count") or 0


def eng_rate(m):
    """Engagement rate = (likes + comments) / views. Secondary ranking signal."""
    v = views(m)
    if not v:
        return 0.0
    return ((m.get("like_count") or 0) + (m.get("comments_count") or 0)) / v


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
    errors = []

    # Collected as we go: per-niche post lists, plus account-level stats for the
    # "suggest accounts to add" pass.
    niche_posts = {}          # niche -> [enriched post dict, ...]
    all_posts = []            # flat list for the cross-niche board
    account_stats = []        # [{user, niche, followers, median_views, vpf}]

    for niche, usernames in watchlist.items():
        niche_posts.setdefault(niche, [])
        for u in usernames:
            r = discover(u, token)
            bd = r.get("business_discovery")
            if not bd:
                msg = r.get("error", {}).get("message", "unknown error")[:120]
                errors.append(f"- **{u}** ({niche}): {msg}")
                log(f"  ! {u}: {msg}")
                time.sleep(CALL_SLEEP)
                continue

            followers = bd.get("followers_count") or 0
            media = bd.get("media", {}).get("data", [])
            scored = [m for m in media if views(m) > 0]
            med = statistics.median([views(m) for m in scored]) if scored else 0
            vpf = (med / followers) if followers else 0.0   # views-per-follower

            acct = store["accounts"].setdefault(u, {"niche": niche, "history": {}})
            acct["niche"] = niche
            acct["history"][today] = {"followers": followers,
                                      "median_views": int(med)}

            if med:
                account_stats.append({"user": u, "niche": niche,
                                      "followers": followers,
                                      "median_views": med, "vpf": vpf})

            for m in scored:
                if views(m) < MIN_VIEWS:
                    continue
                post = {
                    "user": u, "niche": niche, "followers": followers,
                    "views": views(m), "likes": m.get("like_count") or 0,
                    "comments": m.get("comments_count") or 0,
                    "eng_rate": eng_rate(m),
                    "ratio": (views(m) / med) if med else 0,
                    "caption": (m.get("caption") or "").strip().replace("\n", " ")[:100],
                    "timestamp": (m.get("timestamp") or "")[:10],
                    "permalink": m.get("permalink") or "",
                    "media_type": m.get("media_product_type") or m.get("media_type") or "",
                }
                niche_posts[niche].append(post)
                all_posts.append(post)

            log(f"  {u}: {followers:,} followers, median views {int(med):,}, "
                f"{len([m for m in scored if views(m) >= MIN_VIEWS])} post(s) over floor")
            time.sleep(CALL_SLEEP)

    # ---- ranking: VIEWS first, engagement-rate as the tiebreak ----
    rank_key = lambda p: (p["views"], p["eng_rate"])
    for niche in niche_posts:
        niche_posts[niche].sort(key=rank_key, reverse=True)
    all_posts.sort(key=rank_key, reverse=True)

    # ---- suggest accounts worth adding: over-performers (high views/follower) ----
    suggestions = []
    if account_stats:
        cohort_vpf = statistics.median([a["vpf"] for a in account_stats]) or 0
        for a in sorted(account_stats, key=lambda x: -x["vpf"]):
            if cohort_vpf and a["vpf"] >= OVERPERFORM_X * cohort_vpf:
                suggestions.append(a)

    # ---- write report ----
    out = [f"# Viral radar — {today}",
           "Top posts per niche **ranked by VIEWS** (2026 IG ranks reach/views, "
           "not likes); engagement-rate = (likes+comments)/views is the tiebreak "
           f"and a quality signal. Floor: ≥ {MIN_VIEWS:,} views. Official Graph "
           "API `business_discovery` only — no scraping, read-only.", ""]

    # Cross-niche biggest hits
    out.append("## 🏆 Biggest hits across all niches (by views)")
    if all_posts:
        for p in all_posts[:TOP_OVERALL]:
            out.append(_fmt_post(p, show_niche=True))
    else:
        out.append("- (no posts over the views floor this pull)")
    out.append("")

    # Per-niche leaderboards
    for niche, posts in niche_posts.items():
        out.append(f"## {niche}")
        if posts:
            for p in posts[:TOP_PER_NICHE]:
                out.append(_fmt_post(p, show_niche=False))
        else:
            out.append("- (no posts over the views floor this pull)")
        out.append("")

    # Suggested accounts to add to the watchlist
    out.append("## ➕ Suggested watchlist additions (over-performers)")
    out.append("_Watched accounts whose median views punch above their follower "
               f"size (≥ {OVERPERFORM_X}× the cohort's median views-per-follower) "
               "— these are the formats worth studying / adding more peers like._")
    if suggestions:
        for a in suggestions:
            out.append(f"- @{a['user']} ({a['niche']}) — {a['followers']:,} followers, "
                       f"median {int(a['median_views']):,} views "
                       f"= {a['vpf']*100:.1f} views per 100 followers")
    else:
        out.append("- (none stand out above the cohort this pull)")
    out.append("")

    if errors:
        out.append("## Lookup errors (fix usernames in watchlist.json)")
        out += errors + [""]

    out.append(f"_Generated {datetime.now(timezone.utc).isoformat()[:19]}Z — official "
               "Graph API (business_discovery), read-only, no scraping._")

    STORE.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    log(f"report written: {REPORT}  ({len(all_posts)} ranked posts, "
        f"{len(suggestions)} suggestion(s))")


def _fmt_post(p, show_niche):
    tag = f"[{p['niche']}] " if show_niche else ""
    return (f"- {tag}**{p['views']:,} views** "
            f"(eng {p['eng_rate']*100:.1f}%, {p['ratio']:.1f}× @{p['user']}'s median) "
            f"| @{p['user']} | {p['timestamp']} | {p['media_type']} | "
            f"{p['caption']} | {p['permalink']}")


if __name__ == "__main__":
    main()
