"""
IG Dashboard sync engine v2 for @elijahaifl.

Pulls media + per-post insights (with velocity history) + account daily
metrics (incl. follower/non-follower view split) + audience-online hours +
follower demographics from the Instagram Graph API.

Writes data/store.json (full state) and data/data.js (dashboard payload).
Token comes from INSTAGRAM_ACCESS_TOKEN env var -- NEVER stored in this
OneDrive-synced folder.

Usage:
  python refresh.py            # incremental refresh (fast; run on open / daily)
  python refresh.py --full     # re-fetch insights for ALL posts (slow, monthly)
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
STORE = DATA / "store.json"
DATA_JS = DATA / "data.js"
LOG = DATA / "refresh.log"

GRAPH = "https://graph.facebook.com/v22.0"
ACCOUNT_ID = "17841400159953101"  # @elijahaifl
POST_LIMIT = 300                  # how many recent posts to track
REFETCH_DAYS = 14                 # re-pull insights for posts younger than this
PAGE_SIZE = 50
CALL_SLEEP = 0.12
HISTORY_CAP = 90                  # max velocity snapshots kept per post

MEDIA_FIELDS = ("id,caption,media_type,media_product_type,permalink,"
                "timestamp,like_count,comments_count,thumbnail_url,media_url,shortcode")
CORE_INSIGHTS = "views,reach,saved,shares,total_interactions"
REEL_EXTRAS = "ig_reels_avg_watch_time,ig_reels_video_view_total_time"
DAILY_METRICS = "reach,profile_views,website_clicks,accounts_engaged,total_interactions"
DAILY_BACKFILL_DAYS = 29          # API only serves ~30 days back
DEMO_BREAKDOWNS = ["age", "gender", "country", "city"]

# caption keyword -> category, first match wins (priority order)
CATEGORIES = [
    ("Child Safety / PSA", ["safety", "psa", "parent", "child", "kids", "predator", "blur your"]),
    ("Founder / Business", ["founder", "cofounder", "co-founder", "business", "entrepreneur",
                            "ceo", "startup", "company", "clients"]),
    ("AI / Tech",          ["ai ", " ai", "artificial intelligence", "software", "tech ",
                            "automation", "coding", "developer"]),
    ("Real Estate",        ["real estate", "property", "realtor", "housing", "development deal"]),
    ("Money / Finance",    ["money", "financ", "invest", "wealth", "broke", "rich", "income"]),
    ("Jewelry",            ["jewel", "diamond", "vvs", "gold chain", "custom piece"]),
    ("Faith",              ["jesus", "god ", "faith", "pray", "bible", "church", "scripture"]),
    ("Motivation / Life",  ["motivat", "lock in", "grind", "mindset", "discipline", "success",
                            "dream", "goal", "lazy", "potential", "yourself"]),
]


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def api(path, params):
    """GET a Graph API path via curl.exe (PowerShell/urllib hang on this host)."""
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{GRAPH}/{path}?{qs}"
    for attempt in (1, 2, 3):
        # feed the URL via --config on stdin so the token never appears in argv
        r = subprocess.run(["curl.exe", "-s", "--max-time", "45", "--config", "-"],
                           capture_output=True, text=True, input=f'url = "{url}"\n')
        out = r.stdout.strip()
        if out:
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                log(f"  ! non-JSON response (attempt {attempt}): {out[:120]}")
        time.sleep(1.5 * attempt)
    return {"error": {"message": "no response after 3 attempts", "code": -1}}


def get_token():
    tok = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
    if not tok:
        # scheduled tasks sometimes get a stale env; read the registry directly
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                tok = winreg.QueryValueEx(k, "INSTAGRAM_ACCESS_TOKEN")[0].strip()
        except OSError:
            tok = ""
    return tok


def refresh_token_expiry(store, token):
    """Resolve the token's real expiry via /debug_token and cache it in the store
    (an app developer's user token may inspect itself)."""
    r = api("debug_token", {"input_token": token, "access_token": token})
    exp = r.get("data", {}).get("expires_at")
    if "error" not in r and exp is not None:
        store["meta"]["token_expires"] = (
            "never" if exp == 0
            else datetime.fromtimestamp(exp, timezone.utc).strftime("%Y-%m-%d"))


def categorize(caption):
    c = (caption or "").lower()
    for name, kws in CATEGORIES:
        if any(kw in c for kw in kws):
            return name
    return "Other"


def load_store():
    if STORE.exists():
        with open(STORE, "r", encoding="utf-8") as f:
            s = json.load(f)
    else:
        s = {}
    for key, default in [("posts", {}), ("daily", {}), ("follower_snapshots", {}),
                         ("online_followers", {}), ("demographics", {}), ("meta", {})]:
        s.setdefault(key, default)
    return s


def save_store(store):
    DATA.mkdir(exist_ok=True)
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False)


def write_data_js(store, token_status, account):
    posts = sorted(store["posts"].values(), key=lambda p: p["timestamp"], reverse=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "token_status": token_status,
        "token_expires": store["meta"].get("token_expires", "2026-08-10"),
        "account": account or store["meta"].get("account", {}),
        "posts": posts,
        "daily": store["daily"],
        "follower_snapshots": store["follower_snapshots"],
        "online_followers": store["online_followers"],
        "demographics": store["demographics"],
        "categories": [c[0] for c in CATEGORIES] + ["Other"],
    }
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("window.DASHBOARD_DATA = ")
        json.dump(payload, f, ensure_ascii=False)
        f.write(";")
    log(f"wrote data.js ({len(posts)} posts, {len(store['daily'])} daily records)")


def sync_posts(store, token, full):
    fetched, after = [], None
    while len(fetched) < POST_LIMIT:
        params = {"fields": MEDIA_FIELDS, "limit": PAGE_SIZE, "access_token": token}
        if after:
            params["after"] = after
        page = api(f"{ACCOUNT_ID}/media", params)
        if "error" in page:
            log(f"media page error: {page['error'].get('message')}")
            break
        items = page.get("data", [])
        if not items:
            break
        fetched.extend(items)
        after = page.get("paging", {}).get("cursors", {}).get("after")
        if not after:
            break
        time.sleep(CALL_SLEEP)
    fetched = fetched[:POST_LIMIT]
    log(f"media list: {len(fetched)} posts")

    now = datetime.now(timezone.utc)
    new_count, refetch_count = 0, 0
    for m in fetched:
        pid = m["id"]
        prev = store["posts"].get(pid, {})
        post = {**prev, **m}
        post["category"] = prev.get("category_override") or categorize(m.get("caption"))
        ts = datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00"))
        age_days = (now - ts).days

        if (full or "insights" not in post
                or "_error" in post.get("insights", {})
                or age_days <= REFETCH_DAYS):
            ins = api(f"{pid}/insights", {"metric": CORE_INSIGHTS, "access_token": token})
            vals = {}
            if "error" not in ins:
                for d in ins.get("data", []):
                    vals[d["name"]] = d.get("values", [{}])[0].get("value")
            else:
                # keep previously cached numbers; the _error marker makes the
                # post eligible for re-fetch on the next run
                vals = {**prev.get("insights", {}),
                        "_error": ins["error"].get("message", "")[:100]}
            if m.get("media_product_type") == "REELS":
                ex = api(f"{pid}/insights", {"metric": REEL_EXTRAS, "access_token": token})
                if "error" not in ex:
                    for d in ex.get("data", []):
                        vals[d["name"]] = d.get("values", [{}])[0].get("value")
            post["insights"] = vals
            post["insights_updated"] = now.isoformat()
            # velocity history: snapshot the moving numbers while the post is young
            if "_error" not in vals and age_days <= REFETCH_DAYS:
                hist = post.get("history", [])
                hist.append({"t": now.isoformat(),
                             "views": vals.get("views"), "reach": vals.get("reach"),
                             "interactions": vals.get("total_interactions"),
                             "saved": vals.get("saved"), "shares": vals.get("shares"),
                             "likes": m.get("like_count"), "comments": m.get("comments_count")})
                post["history"] = hist[-HISTORY_CAP:]
            new_count += 0 if "insights" in prev else 1
            refetch_count += 1 if "insights" in prev else 0
            time.sleep(CALL_SLEEP)
        store["posts"][pid] = post

    keep = sorted(store["posts"].values(), key=lambda p: p["timestamp"], reverse=True)[:POST_LIMIT]
    store["posts"] = {p["id"]: p for p in keep}
    log(f"insights: {new_count} new, {refetch_count} re-fetched")


def sync_daily(store, token):
    """Daily account metrics + follower/non-follower view split, backfilled."""
    filled = 0
    for i in range(1, DAILY_BACKFILL_DAYS + 1):
        day = datetime.now() - timedelta(days=i)
        key = day.strftime("%Y-%m-%d")
        rec = store["daily"].get(key, {})
        if rec.get("_complete"):
            continue
        since = int(day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        until = since + 86400

        r = api(f"{ACCOUNT_ID}/insights",
                {"metric": DAILY_METRICS, "period": "day", "metric_type": "total_value",
                 "since": since, "until": until, "access_token": token})
        if "error" in r:
            log(f"daily {key} error: {r['error'].get('message')[:80]}")
            continue
        for d in r.get("data", []):
            rec[d["name"]] = d.get("total_value", {}).get("value")

        v = api(f"{ACCOUNT_ID}/insights",
                {"metric": "views", "period": "day", "metric_type": "total_value",
                 "breakdown": "follow_type", "since": since, "until": until,
                 "access_token": token})
        if "error" not in v:
            for d in v.get("data", []):
                tv = d.get("total_value", {})
                rec["views"] = tv.get("value")
                for br in tv.get("breakdowns", []):
                    for res in br.get("results", []):
                        dim = (res.get("dimension_values") or ["?"])[0]
                        if dim == "FOLLOWER":
                            rec["views_followers"] = res.get("value")
                        elif dim == "NON_FOLLOWER":
                            rec["views_non_followers"] = res.get("value")
            rec["_complete"] = True
        else:
            # leave the day incomplete so the backfill loop retries it next run
            log(f"daily {key} views error: {v['error'].get('message', '')[:80]}")
        store["daily"][key] = rec
        filled += 1
        time.sleep(CALL_SLEEP)
    if filled:
        log(f"daily metrics: filled/completed {filled} day(s)")


def sync_online_followers(store, token):
    """Hourly when-is-my-audience-online histogram (API serves ~2 recent days)."""
    r = api(f"{ACCOUNT_ID}/insights",
            {"metric": "online_followers", "period": "lifetime", "access_token": token})
    if "error" in r:
        log(f"online_followers error: {r['error'].get('message')[:80]}")
        return
    for d in r.get("data", []):
        for v in d.get("values", []):
            day = (v.get("end_time") or "")[:10]
            hours = v.get("value") or {}
            if day and hours:
                store["online_followers"][day] = hours
    # keep a rolling 30 days
    keys = sorted(store["online_followers"].keys())
    for k in keys[:-30]:
        del store["online_followers"][k]
    log(f"online_followers: {len(store['online_followers'])} day(s) stored")


def sync_demographics(store, token):
    # merge per-breakdown so a failed call keeps the previously cached data
    demo = store.get("demographics") or {}
    ok = 0
    for b in DEMO_BREAKDOWNS:
        r = api(f"{ACCOUNT_ID}/insights",
                {"metric": "follower_demographics", "period": "lifetime",
                 "metric_type": "total_value", "breakdown": b, "access_token": token})
        if "error" in r:
            log(f"demographics[{b}] error: {r['error'].get('message')[:80]}")
            continue
        out = {}
        for d in r.get("data", []):
            for br in d.get("total_value", {}).get("breakdowns", []):
                for res in br.get("results", []):
                    out[(res.get("dimension_values") or ["?"])[0]] = res.get("value")
        demo[b] = out
        ok += 1
        time.sleep(CALL_SLEEP)
    if ok:
        demo["fetched_at"] = datetime.now(timezone.utc).isoformat()
    store["demographics"] = demo
    log(f"demographics: refreshed {ok}/{len(DEMO_BREAKDOWNS)} breakdown(s)")


def write_stats_md(store):
    """Emit a compact stats summary into team/stats.md — the auto-fed piece of
    the file-based context system (CLAUDE.md + profile + stats + memory)."""
    team = BASE.parent / "team"
    try:
        team.mkdir(exist_ok=True)
        now = datetime.now(timezone.utc)
        posts = sorted(store["posts"].values(), key=lambda p: p["timestamp"], reverse=True)
        recent = [p for p in posts
                  if (now - datetime.fromisoformat(p["timestamp"].replace("+0000", "+00:00"))).days <= 30]
        snaps = sorted(store["follower_snapshots"].items())
        followers = snaps[-1][1] if snaps else 0
        delta30 = None
        for day, n in snaps:
            if (now - datetime.fromisoformat(day + "T00:00:00+00:00")).days <= 30:
                delta30 = followers - n
                break

        def views(p):
            return (p.get("insights") or {}).get("views") or 0

        top = sorted(recent, key=views, reverse=True)[:5]
        cats = {}
        for p in recent:
            c = cats.setdefault(p.get("category", "Other"), [0, 0])
            c[0] += 1
            c[1] += views(p)
        lines = [
            "# stats.md — auto-generated daily by ig-dashboard/refresh.py (do not hand-edit)",
            f"Updated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            f"**@elijahaifl** — {followers:,} followers"
            + (f" ({delta30:+,} over the last 30d of snapshots)" if delta30 is not None else ""),
            f"Posts tracked: {len(posts)} | posted in last 30d: {len(recent)}",
            "",
            "## Top posts — last 30 days, by views",
        ]
        for p in top:
            cap = (p.get("caption") or "").strip().replace("\n", " ")[:80]
            lines.append(f"- {views(p):,} views | {p.get('category', '?')} | "
                         f"{p['timestamp'][:10]} | {cap}")
        lines += ["", "## Category mix — last 30 days (posts / total views)"]
        for name, (n, v) in sorted(cats.items(), key=lambda kv: -kv[1][1]):
            lines.append(f"- {name}: {n} posts / {v:,} views")
        lines += ["", f"IG token expires: {store['meta'].get('token_expires', 'unknown')}. "
                      "Full data: ig-dashboard/dashboard.html (open via Open Dashboard.bat)."]
        with open(team / "stats.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        log("wrote team/stats.md")
    except Exception as e:
        log(f"stats.md error: {e}")


def main():
    full = "--full" in sys.argv
    token = get_token()
    store = load_store()

    if not token:
        log("FATAL: INSTAGRAM_ACCESS_TOKEN env var not set")
        write_data_js(store, "missing", None)
        sys.exit(1)

    acct = api(ACCOUNT_ID, {"fields": "username,name,followers_count,follows_count,"
                                      "media_count,profile_picture_url,biography",
                            "access_token": token})
    if "error" in acct:
        code = acct["error"].get("code")
        log(f"token check failed: {acct['error'].get('message')}")
        write_data_js(store, "expired" if code == 190 else "error", None)
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    store["follower_snapshots"][today] = acct.get("followers_count")
    store["meta"]["account"] = acct
    log(f"token OK -- @{acct.get('username')} {acct.get('followers_count'):,} followers")
    refresh_token_expiry(store, token)

    sync_posts(store, token, full)
    sync_daily(store, token)
    sync_online_followers(store, token)
    sync_demographics(store, token)

    save_store(store)
    write_data_js(store, "ok", acct)
    write_stats_md(store)
    log("refresh complete")


if __name__ == "__main__":
    main()
