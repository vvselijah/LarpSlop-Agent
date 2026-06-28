# -*- coding: utf-8 -*-
"""One-off: pull ~6 months of @elijahaifl post performance for the growth video.
Reuses refresh.api()/get_token()/categorize(). Uses cached insights from
store.json where present; pulls insights for the top-engagement posts that lack
them (capped, to stay under rate limits). Writes data/sixmonth_summary.md."""
import json, time, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import refresh

tok = refresh.get_token(); acct = refresh.ACCOUNT_ID
if not tok: print("NO TOKEN"); sys.exit(1)
DAYS = 185
cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
fields = "id,caption,media_type,media_product_type,timestamp,like_count,comments_count"

posts, after, pages = [], None, 0
while True:
    p = {"fields": fields, "limit": 50, "access_token": tok}
    if after: p["after"] = after
    page = refresh.api(f"{acct}/media", p)
    if "error" in page:
        print("media err:", page["error"].get("message","")[:80]); break
    items = page.get("data", [])
    if not items: break
    stop = False
    for m in items:
        ts = datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00"))
        if ts < cutoff: stop = True; break
        posts.append(m)
    after = page.get("paging", {}).get("cursors", {}).get("after")
    pages += 1
    if stop or not after or pages > 90: break
    time.sleep(0.12)
print(f"pulled {len(posts)} posts over ~{DAYS}d ({pages} pages)")

store_p = HERE / "data" / "store.json"
store = json.load(open(store_p, encoding="utf-8")) if store_p.exists() else {}
have = store.get("posts", {})

def cached(pid):
    ins = (have.get(pid, {}) or {}).get("insights", {}) or {}
    return ins.get("views"), ins.get("reach"), ins.get("saved"), ins.get("shares")

for m in posts:
    m["_v"], m["_r"], m["_s"], m["_sh"] = cached(m["id"])

missing = [m for m in posts if m["_v"] is None]
missing.sort(key=lambda m: (m.get("like_count", 0) or 0) + (m.get("comments_count", 0) or 0), reverse=True)
CAP = 70
for m in missing[:CAP]:
    ins = refresh.api(f'{m["id"]}/insights', {"metric": "views,reach,saved,shares", "access_token": tok})
    if "error" not in ins:
        for d in ins.get("data", []):
            val = d.get("values", [{}])[0].get("value")
            if d["name"] == "views": m["_v"] = val
            elif d["name"] == "reach": m["_r"] = val
            elif d["name"] == "saved": m["_s"] = val
            elif d["name"] == "shares": m["_sh"] = val
    time.sleep(0.15)
print(f"insight pulls: {min(len(missing), CAP)} (of {len(missing)} missing); cached covered {len(posts)-len(missing)}")

bymonth = defaultdict(lambda: {"posts": 0, "likes": 0, "comments": 0, "views": 0, "vknown": 0, "saves": 0, "shares": 0})
fmt = defaultdict(int)
cat = defaultdict(lambda: [0, 0, 0])  # posts, views(known), vknown
for m in posts:
    mo = m["timestamp"][:7]; b = bymonth[mo]
    b["posts"] += 1
    b["likes"] += m.get("like_count", 0) or 0
    b["comments"] += m.get("comments_count", 0) or 0
    if m["_v"] is not None: b["views"] += m["_v"]; b["vknown"] += 1
    if m["_s"] is not None: b["saves"] += m["_s"]
    if m["_sh"] is not None: b["shares"] += m["_sh"]
    fmt[m.get("media_product_type") or m.get("media_type") or "?"] += 1
    c = refresh.categorize(m.get("caption"))
    cat[c][0] += 1
    if m["_v"] is not None: cat[c][1] += m["_v"]; cat[c][2] += 1

known = [m for m in posts if m["_v"] is not None]
top = sorted(known, key=lambda m: m["_v"], reverse=True)[:15]
total_v = sum(m["_v"] for m in known)
snaps = sorted(store.get("follower_snapshots", {}).items())
followers = snaps[-1][1] if snaps else None

L = []
L.append("# 6-Month Performance Pull — @elijahaifl")
L.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · window ~{DAYS}d · {len(posts)} posts · views known for {len(known)}/{len(posts)} ({round(100*len(known)/max(1,len(posts)))}%)_")
L.append(f"\n**Followers now:** {followers:,}" if followers else "")
L.append(f"**Total views across posts with known views:** {total_v:,} (partial — full per-post view sum needs a bigger pull)")
L.append("\n## By month (newest first)")
L.append("| Month | Posts | Likes | Comments | Views (known) | Posts w/ views |")
L.append("|---|---|---|---|---|---|")
for mo in sorted(bymonth, reverse=True):
    b = bymonth[mo]
    L.append(f"| {mo} | {b['posts']} | {b['likes']:,} | {b['comments']:,} | {b['views']:,} | {b['vknown']} |")
L.append("\n## Format mix (6mo)")
for k, v in sorted(fmt.items(), key=lambda x: -x[1]):
    L.append(f"- {k}: {v} posts")
L.append("\n## Category mix (posts / known-views / #w-views)")
for c, (n, vv, vk) in sorted(cat.items(), key=lambda x: -x[1][1]):
    L.append(f"- {c}: {n} posts / {vv:,} views / {vk} w/views")
L.append("\n## Top 15 posts by views")
for m in top:
    cap = (m.get("caption") or "").strip().replace("\n", " ")[:70]
    L.append(f"- {m['_v']:,} views · {(m['_s'] or 0):,} saves · {(m['_sh'] or 0):,} shares · {m['timestamp'][:10]} · {refresh.categorize(m.get('caption'))} · {cap}")
out = "\n".join(x for x in L if x is not None)
(HERE / "data" / "sixmonth_summary.md").write_text(out, encoding="utf-8")
print("\n" + out)
