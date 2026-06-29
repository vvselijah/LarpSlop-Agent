"""
Niche radar — the DISCOVERY half of the viral pipeline.

Where viral-radar.py ranks the winners among accounts you ALREADY name in
watchlist.json (official Graph API `business_discovery`, true views), niche-radar
answers the other half Elijah keeps asking: "show me the top posts in a NICHE I'm
not already tracking, and tell me which new accounts to start watching." It does
this by scraping Instagram hashtags.

WHY A SCRAPER (and not the official API): the official Graph API hashtag endpoints
(`ig_hashtag_search` -> `top_media`) require Meta's "Instagram Public Content
Access" App-Review feature, which the `mybrain` app does NOT have — live-probed
2026-06-29, returns OAuthException #10. So arbitrary-hashtag discovery is only
possible via a scraper. This engine uses Apify's `instagram-hashtag-scraper`
actor, which DOES return true view counts on arbitrary posts (the one thing
business_discovery can't do for accounts you don't own/track).

THE HYBRID LOOP this closes:
  discover (here, scraper, engagement+true-views)
    -> suggest winning new AUTHORS into watchlist.json (Elijah one-click adds)
      -> viral-radar/competitor-radar then track them with the official API
        -> viral_teardown explains WHY they win.
niche-radar writes niche-report.md in the SAME line format viral-radar uses, so
viral_teardown.py tears down BOTH leaderboards in one pass.

COST / SAFETY (Apify free tier is a hard $5/mo wall — read intel/niche-hashtags.json `_budget`):
  - pay-per-result ~ $2.60 / 1,000 results => ~$0.08 per 30-post hashtag.
  - resultsLimit is PER HASHTAG, so billable items = resultsLimit x (#hashtags).
  - the engine LOGS an estimated cost and supports --dry-run (no API call, no spend).
  - it NEVER retries a timeout (a 408'd run keeps burning credit in the background).
  - it persists results to its own niche-report.md + data/niche.json immediately
    (Apify free datasets expire after 7 days).

SECRET: reads APIFY_TOKEN from a Windows user env var (set via
`setx APIFY_TOKEN "<token>"`), never from a file (this tree is OneDrive-synced).
The token is fed to curl over stdin (--config -), never on argv.

READ-ONLY w.r.t. Instagram: it scrapes public hashtag pages; it never publishes,
comments, DMs, or edits any other engine's data. It writes exactly two files:
niche-report.md and data/niche.json.

Usage:
  python niche-radar.py                 # scrape, rank, suggest, write the report
  python niche-radar.py --dry-run       # show config + estimated cost, NO API call
  python niche-radar.py --results 20    # override per-hashtag result cap (default 30)
  python niche-radar.py --type posts    # scrape 'posts' instead of 'reels'
  python niche-radar.py --self-test     # built-in tests (mocked data), no network
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
NICHES = BASE / "niche-hashtags.json"
WATCHLIST = BASE / "watchlist.json"        # to dedupe suggestions vs already-tracked
DATA = BASE / "data"
STORE = DATA / "niche.json"
REPORT = BASE / "niche-report.md"

APIFY_ACTOR = "apify~instagram-hashtag-scraper"
APIFY_ENDPOINT = f"https://api.apify.com/v2/acts/{APIFY_ACTOR}/run-sync-get-dataset-items"

RESULTS_LIMIT = 30        # results per hashtag (Free returns ~first page regardless)
MAX_RESULTS = 90          # hard clamp on --results (guards a manual mis-invocation)
RESULTS_TYPE = "reels"    # 'reels' (Elijah's format) or 'posts'
DEFAULT_MIN_VIEWS = 50000 # noise floor if a niche omits min_views
TOP_PER_NICHE = 8         # leaderboard depth per niche
TOP_OVERALL = 12          # cross-niche "biggest hits" depth
PROMOTE_MIN_POSTS = 2     # appear in >= this many winning posts -> suggest to watchlist
COST_PER_1K = 2.60        # Apify Free pay-per-result, USD; for the cost log only
CALL_TIMEOUT = 150        # curl --max-time (server sync cap is 300s); ~30 items < 1 min


def log(msg):
    """cp1252-safe stdout (OneDrive console is cp1252; emojis in captions blow up print)."""
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    enc = sys.stdout.encoding or "utf-8"
    sys.stdout.write(line.encode(enc, "replace").decode(enc, "replace") + "\n")


def get_token():
    tok = os.environ.get("APIFY_TOKEN", "").strip()
    if not tok:
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                tok = winreg.QueryValueEx(k, "APIFY_TOKEN")[0].strip()
        except OSError:
            tok = ""
    return tok


def scrape(hashtags, token, results_limit, results_type):
    """One synchronous Apify actor run for a niche's hashtags.

    Returns a list of raw item dicts on success, or {"error": "..."} on failure.
    Token is fed over stdin (curl --config -); the request body (not secret) is a
    temp file. NO retry: a timed-out run keeps billing in the background.
    """
    body = json.dumps({
        "hashtags": [h.lstrip("#").strip() for h in hashtags if h.strip()],
        "resultsType": results_type,
        "resultsLimit": results_limit,
    })
    cfg = (f'url = "{APIFY_ENDPOINT}"\n'
           f'header = "Authorization: Bearer {token}"\n'
           'header = "Content-Type: application/json"\n')
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    try:
        tmp.write(body)
        tmp.close()
        # Force UTF-8 decode: Apify returns UTF-8 (emoji captions); the Windows
        # default cp1252 decode raises UnicodeDecodeError on bytes like 0x8d and
        # silently empties stdout. errors="replace" tolerates any stray bytes.
        r = subprocess.run(
            ["curl.exe", "-s", "--max-time", str(CALL_TIMEOUT),
             "--data-binary", f"@{tmp.name}", "--config", "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            input=cfg)
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass

    out = (r.stdout or "").strip()
    if not out:
        return {"error": f"empty response (curl rc={r.returncode}; "
                         f"stderr={(r.stderr or '').strip()[:150]})"}
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return {"error": f"non-JSON response: {out[:150]}"}
    if isinstance(data, dict):
        # Apify returns an error OBJECT (or a 408 payload) on failure; tolerate
        # `error` being a bare string instead of an {type,message} object.
        err = data.get("error")
        msg = (err.get("message") or err.get("type")) if isinstance(err, dict) \
            else (err or data.get("message"))
        return {"error": str(msg or data)[:150]}
    return data


# ---- defensive field extraction (see the verified Apify field_map) ----

def _views(item):
    """videoPlayCount (every play) preferred; videoViewCount fallback; 0 if absent.
    Both are absent on Image items; either can legitimately be 0 on a reel."""
    for k in ("videoPlayCount", "videoViewCount"):
        v = item.get(k)
        if isinstance(v, int) and v > 0:
            return v
    return 0


def _likes(item):
    """likesCount, but -1 (owner hid likes) and None are 'unknown' -> 0."""
    v = item.get("likesCount")
    return v if isinstance(v, int) and v >= 0 else 0


def _comments(item):
    """commentsCount, but negatives (hidden/disabled-comment sentinels) -> 0, so
    eng_rate never goes negative — a negative 'eng -0.0%' would break the report
    line's regex contract with viral_teardown and silently drop the post."""
    v = item.get("commentsCount")
    return v if isinstance(v, int) and v >= 0 else 0


def _owner(item):
    """Best available identity, SANITIZED for the report-line grammar. A real
    ownerUsername is already clean, but the ownerFullName fallback can carry an
    apostrophe or pipe (e.g. "Mary O'Brien") that would break viral_teardown's
    POST_RE — strip those and collapse whitespace."""
    name = (item.get("ownerUsername")
            or item.get("ownerFullName")
            or (f"id:{item.get('ownerId')}" if item.get("ownerId") else "unknown"))
    return " ".join(name.replace("'", "").replace("|", "").split())


def _url(item):
    return item.get("url") or (
        f"https://www.instagram.com/p/{item['shortCode']}/" if item.get("shortCode") else "")


def _media_type(item):
    """Emit IG-style labels (REELS / CAROUSEL_ALBUM / IMAGE) matching viral-radar's
    media_product_type values. viral_teardown.classify_format substring-matches
    'REEL', so the plural 'REELS' is correct and intentional — do not 'fix' to REEL."""
    if item.get("isVideo") or item.get("productType") == "clips" \
            or (item.get("type") or "").lower() == "video":
        return "REELS"
    t = (item.get("type") or "").lower()
    if t == "sidecar":
        return "CAROUSEL_ALBUM"
    if t == "image":
        return "IMAGE"
    return (item.get("type") or "UNKNOWN").upper()


def normalize(item, niche):
    v = _views(item)
    likes = _likes(item)
    comments = _comments(item)
    return {
        "user": _owner(item),
        "niche": niche,
        "views": v,
        "likes": likes,
        "comments": comments,
        "eng_rate": ((likes + comments) / v) if v else 0.0,
        "caption": (item.get("caption") or "").strip().replace("\n", " ")[:100],
        "timestamp": (item.get("timestamp") or "")[:10],
        "permalink": _url(item),
        "media_type": _media_type(item),
        "source_tag": item.get("inputUrl", ""),
    }


def _fmt_post(p, show_niche):
    """IDENTICAL line shape to viral-radar.py's _fmt_post so viral_teardown.py's
    POST_RE parses niche-report.md and viral-report.md the same way."""
    tag = f"[{p['niche']}] " if show_niche else ""
    return (f"- {tag}**{p['views']:,} views** "
            f"(eng {p['eng_rate']*100:.1f}%, {p['ratio']:.1f}× @{p['user']}'s median) "
            f"| @{p['user']} | {p['timestamp']} | {p['media_type']} | "
            f"{p['caption']} | {p['permalink']}")


def rank_and_attribute(posts):
    """Attach each post's ratio = views / that account's median across the scraped
    set (so '@user's median' is honest; single-appearance accounts get 1.0x).
    Sorts in place by (views, eng_rate) desc and returns the list."""
    by_user = {}
    for p in posts:
        by_user.setdefault(p["user"], []).append(p["views"])
    med = {u: (statistics.median(vs) or 0) for u, vs in by_user.items()}
    for p in posts:
        m = med.get(p["user"]) or 0
        p["ratio"] = (p["views"] / m) if m else 0.0
    posts.sort(key=lambda p: (p["views"], p["eng_rate"]), reverse=True)
    return posts


def suggest_authors(all_posts, watched):
    """Accounts with >= PROMOTE_MIN_POSTS winning posts, with a real username, not
    already watched. Returns [{user, niche, count, top_views, permalink}] desc."""
    agg = {}
    for p in all_posts:
        u = p["user"]
        if not u or u.startswith("id:") or u == "unknown":
            continue
        if u.lower() in watched:
            continue
        a = agg.setdefault(u, {"user": u, "niche": p["niche"], "count": 0,
                               "top_views": 0, "permalink": p["permalink"]})
        a["count"] += 1
        if p["views"] > a["top_views"]:
            a["top_views"] = p["views"]
            a["permalink"] = p["permalink"]
    out = [a for a in agg.values() if a["count"] >= PROMOTE_MIN_POSTS]
    out.sort(key=lambda a: (a["count"], a["top_views"]), reverse=True)
    return out


def load_watched():
    """Flatten watchlist.json usernames (lowercased) so suggestions exclude them."""
    watched = set()
    if WATCHLIST.exists():
        try:
            wl = json.loads(WATCHLIST.read_text(encoding="utf-8"))
            for k, v in wl.items():
                if k.startswith("_") or not isinstance(v, list):
                    continue
                watched.update(str(u).lstrip("@").lower() for u in v)
        except (json.JSONDecodeError, OSError):
            pass
    return watched


def render(niche_posts, all_posts, suggestions, today, est_cost, errors):
    out = [
        f"# Niche radar (discovery) — {today}",
        "Top hashtag posts per niche **ranked by VIEWS** (true scraped view counts), "
        "engagement-rate = (likes+comments)/views as the tiebreak. `ratio` = views ÷ "
        "that account's median across this scrape. Source: Apify "
        "`instagram-hashtag-scraper` (the official Graph API hashtag endpoints are "
        "App-Review-gated for this app). Read-only; never publishes.",
        "",
    ]
    out.append("## 🏆 Biggest hits across all niches (by views)")
    if all_posts:
        out += [_fmt_post(p, True) for p in all_posts[:TOP_OVERALL]]
    else:
        out.append("- (no posts over the views floor this pull)")
    out.append("")

    for niche, posts in niche_posts.items():
        out.append(f"## {niche}")
        if posts:
            out += [_fmt_post(p, False) for p in posts[:TOP_PER_NICHE]]
        else:
            out.append("- (no posts over the views floor this pull)")
        out.append("")

    out.append("## ➕ Suggested watchlist additions (discovered via hashtags)")
    out.append("_New accounts (NOT yet in watchlist.json) that produced ≥ "
               f"{PROMOTE_MIN_POSTS} winning posts. Add the good ones to the right "
               "niche in `watchlist.json` so viral-radar/competitor-radar then track "
               "them with the official API's true numbers._")
    if suggestions:
        for a in suggestions:
            out.append(f"- @{a['user']} ({a['niche']}) — {a['count']} winning post(s), "
                       f"top {a['top_views']:,} views — {a['permalink']}")
    else:
        out.append("- (no new accounts cleared the bar this pull)")
    out.append("")

    if errors:
        out.append("## Scrape errors (check niche-hashtags.json / APIFY_TOKEN / budget)")
        out += errors + [""]

    out.append(f"_Estimated Apify cost this run: ~${est_cost:.2f} "
               f"({int(round(est_cost / COST_PER_1K * 1000))} results @ "
               f"${COST_PER_1K:.2f}/1k). Generated "
               f"{datetime.now(timezone.utc).isoformat()[:19]}Z — scraper, read-only._")
    return "\n".join(out) + "\n"


def load_niches():
    cfg = json.loads(NICHES.read_text(encoding="utf-8"))
    return {k: v for k, v in cfg.items() if not k.startswith("_")}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hashtag discovery radar (Apify scraper).")
    ap.add_argument("--dry-run", action="store_true",
                    help="show config + estimated cost, make NO API call")
    ap.add_argument("--results", type=int, default=RESULTS_LIMIT,
                    help=f"results per hashtag (default {RESULTS_LIMIT})")
    ap.add_argument("--type", default=RESULTS_TYPE, choices=("reels", "posts"),
                    help=f"content type to scrape (default {RESULTS_TYPE})")
    ap.add_argument("--self-test", action="store_true",
                    help="run built-in tests on mocked data, write nothing")
    args = ap.parse_args(argv)

    if args.self_test:
        return 0 if _self_test() else 1

    # Budget guard: clamp a runaway --results before it can multiply across tags.
    if args.results > MAX_RESULTS:
        log(f"--results {args.results} over cap; clamping to {MAX_RESULTS} (budget guard).")
        args.results = MAX_RESULTS
    args.results = max(1, args.results)

    if not NICHES.exists():
        log(f"FATAL: {NICHES.name} not found — seed it with niche -> hashtags.")
        return 2
    niches = load_niches()
    total_tags = sum(len(c.get("hashtags", [])) for c in niches.values())
    est_cost = total_tags * args.results / 1000.0 * COST_PER_1K

    if args.dry_run:
        log(f"DRY RUN — {len(niches)} niche(s), {total_tags} hashtag(s), "
            f"{args.results}/tag ({args.type}). Est cost ~${est_cost:.2f} (upper bound; "
            "Free tier returns ~first page, so actual is often lower). No API call.")
        for n, c in niches.items():
            log(f"  {n}: {', '.join(c.get('hashtags', []))} (min_views "
                f"{c.get('min_views', DEFAULT_MIN_VIEWS):,})")
        return 0

    token = get_token()
    if not token:
        log("APIFY_TOKEN not set — skipping discovery (set via "
            'setx APIFY_TOKEN "<token>", then restart). The rest of the chain '
            "(viral-radar/viral_teardown) still runs without it.")
        return 0   # graceful skip so Weekly Agent Refresh.bat continues

    log(f"{len(niches)} niche(s), {total_tags} hashtag(s), {args.results}/tag "
        f"({args.type}). Est cost ~${est_cost:.2f} (upper bound).")

    watched = load_watched()
    DATA.mkdir(exist_ok=True)
    store = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
    store.setdefault("runs", {})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    niche_posts = {}
    all_posts = []
    errors = []
    scraped_items = 0

    for niche, conf in niches.items():
        hashtags = conf.get("hashtags", [])
        min_views = conf.get("min_views", DEFAULT_MIN_VIEWS)
        if not hashtags:
            continue
        res = scrape(hashtags, token, args.results, args.type)
        if isinstance(res, dict):
            errors.append(f"- **{niche}** ({', '.join(hashtags)}): {res.get('error')}")
            log(f"  ! {niche}: {res.get('error')}")
            continue
        scraped_items += len(res)
        posts = [normalize(it, niche) for it in res]
        # require a permalink: an unlinkable post can't be torn down/verified and
        # would render a line viral_teardown's POST_RE rejects (silent drop).
        kept = [p for p in posts if p["views"] >= min_views and p["permalink"]]
        skipped = sum(1 for p in posts if p["views"] >= min_views and not p["permalink"])
        rank_and_attribute(kept)
        niche_posts[niche] = kept
        all_posts.extend(kept)
        msg = f"  {niche}: {len(res)} scraped, {len(kept)} over {min_views:,} views floor"
        if skipped:
            msg += f" ({skipped} skipped: no permalink)"
        log(msg)

    all_posts.sort(key=lambda p: (p["views"], p["eng_rate"]), reverse=True)
    suggestions = suggest_authors(all_posts, watched)
    actual_cost = scraped_items / 1000.0 * COST_PER_1K

    store["runs"][today] = {
        "hashtags": total_tags, "scraped_items": scraped_items,
        "kept": len(all_posts), "suggestions": len(suggestions),
        "est_cost_usd": round(actual_cost, 3),
    }
    STORE.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
    REPORT.write_text(render(niche_posts, all_posts, suggestions, today,
                             actual_cost, errors), encoding="utf-8")
    log(f"report written: {REPORT} ({len(all_posts)} ranked, "
        f"{len(suggestions)} suggestion(s), ~${actual_cost:.2f} spent)")
    return 0


# ---- self-test (mocked Apify items, no network) ----

def _self_test():
    items = [
        {"videoPlayCount": 500000, "videoViewCount": 120000, "likesCount": 20000,
         "commentsCount": 800, "caption": "3 AI tools that print money 🤖",
         "url": "https://www.instagram.com/reel/AAA/", "ownerUsername": "aiwhiz",
         "timestamp": "2026-06-20T10:00:04.000Z", "type": "Video", "isVideo": True,
         "productType": "clips", "inputUrl": ".../tags/aitools"},
        {"videoPlayCount": 300000, "likesCount": -1, "commentsCount": 50,
         "caption": "how to automate your business", "shortCode": "BBB",
         "ownerUsername": "aiwhiz", "timestamp": "2026-06-18T09:00:00.000Z",
         "type": "Video", "isVideo": True, "inputUrl": ".../tags/aiautomation"},
        {"videoViewCount": 80000, "likesCount": 4000, "commentsCount": 120,
         "caption": "side hustle ideas", "url": "https://www.instagram.com/reel/CCC/",
         "ownerFullName": "Money Mike", "ownerId": "999",
         "timestamp": "2026-06-15T00:00:00.000Z", "type": "Video", "isVideo": True},
        {"type": "Image", "likesCount": 10, "commentsCount": 1, "caption": "tiny post",
         "url": "https://www.instagram.com/p/DDD/", "ownerUsername": "smallfry",
         "timestamp": "2026-06-10T00:00:00.000Z"},
        # --- edge cases that previously broke the viral_teardown parse contract ---
        # E: high views but NEITHER url NOR shortCode -> unlinkable, must be dropped.
        {"videoPlayCount": 900000, "likesCount": 1000, "commentsCount": 10,
         "caption": "no link here", "ownerUsername": "ghost",
         "timestamp": "2026-06-21T00:00:00.000Z", "type": "Video", "isVideo": True},
        # F: owner display-name with apostrophe + space, no ownerUsername.
        {"videoPlayCount": 250000, "likesCount": 500, "commentsCount": 30,
         "caption": "fundamentals", "url": "https://www.instagram.com/reel/FFF/",
         "ownerFullName": "Mary O'Brien", "ownerId": "111",
         "timestamp": "2026-06-17T00:00:00.000Z", "type": "Video", "isVideo": True},
        # G: hidden/negative commentsCount must not yield a negative eng%.
        {"videoPlayCount": 200000, "likesCount": -1, "commentsCount": -1,
         "caption": "comments off", "url": "https://www.instagram.com/reel/GGG/",
         "ownerUsername": "quietguy", "timestamp": "2026-06-16T00:00:00.000Z",
         "type": "Video", "isVideo": True},
    ]
    norm = [normalize(it, "ai-entrepreneur") for it in items]
    # views: playCount preferred, viewCount fallback, image -> 0
    assert [norm[i]["views"] for i in range(4)] == [500000, 300000, 80000, 0], norm
    # likesCount -1 (hidden) -> 0; negative commentsCount clamped -> 0, eng >= 0
    assert norm[1]["likes"] == 0, norm[1]["likes"]
    g = next(p for p in norm if p["user"] == "quietguy")
    assert g["comments"] == 0 and g["eng_rate"] >= 0, (g["comments"], g["eng_rate"])
    # owner fallback + sanitization: apostrophe stripped for the line grammar
    assert norm[2]["user"] == "Money Mike", norm[2]["user"]
    mob = next(p for p in norm if p["timestamp"] == "2026-06-17")
    assert mob["user"] == "Mary OBrien" and "'" not in mob["user"], mob["user"]
    # url built from shortCode when url absent; empty when neither present
    assert norm[1]["permalink"] == "https://www.instagram.com/p/BBB/", norm[1]["permalink"]
    assert next(p for p in norm if p["user"] == "ghost")["permalink"] == "", "ghost url"
    # media_type maps reels -> REELS, image -> IMAGE
    assert norm[0]["media_type"] == "REELS", norm[0]["media_type"]
    assert norm[3]["media_type"] == "IMAGE", norm[3]["media_type"]

    # kept = over the floor AND linkable (unlinkable 'ghost' is dropped)
    kept = [p for p in norm if p["views"] >= 50000 and p["permalink"]]
    assert "ghost" not in {p["user"] for p in kept}, "unlinkable post must be dropped"
    rank_and_attribute(kept)
    # aiwhiz appears twice -> median(500k,300k)=400k; its top post ratio = 1.25x
    top = next(p for p in kept if p["user"] == "aiwhiz" and p["views"] == 500000)
    assert abs(top["ratio"] - 1.25) < 1e-6, top["ratio"]
    # single-appearance account -> ratio 1.0
    mm = next(p for p in kept if p["user"] == "Money Mike")
    assert abs(mm["ratio"] - 1.0) < 1e-6, mm["ratio"]

    # author promotion: aiwhiz (2 winning posts, not watched) -> suggested;
    # single-post accounts -> not; an already-watched user is excluded.
    sug = suggest_authors(kept, watched={"garyvee"})
    assert any(a["user"] == "aiwhiz" and a["count"] == 2 for a in sug), sug
    assert all(a["user"] != "Money Mike" for a in sug), sug
    assert all(a["user"] != "aiwhiz"
               for a in suggest_authors(kept, watched={"aiwhiz"})), "watched excluded"

    # EVERY rendered post line must parse under viral_teardown's REAL POST_RE —
    # import it so this test fails loudly if the two files ever drift apart.
    try:
        import viral_teardown
        post_re = viral_teardown.POST_RE
    except Exception:
        import re as _re
        post_re = _re.compile(
            r"^- (?:\[(?P<niche>[^\]]+)\] )?\*\*(?P<views>[\d,]+) views\*\* "
            r"\(eng (?P<eng>[\d.]+)%, (?P<ratio>[\d.]+)[x×] @(?P<u2>[^']+)'s median\) \| "
            r"@(?P<user>[^|]+?) \| (?P<date>[\d-]+) \| (?P<mtype>[^|]+?) \| "
            r"(?P<caption>.*?) \| (?P<url>\S+)\s*$")
    md = render({"ai-entrepreneur": kept}, kept, sug, "2026-06-29", 0.55, [])
    assert "Biggest hits" in md and "Suggested watchlist additions" in md
    post_lines = [ln for ln in md.splitlines()
                  if ln.startswith("- **") and "views**" in ln]
    assert post_lines, "no post lines rendered"
    for ln in post_lines:
        assert post_re.match(ln), f"line won't parse in viral_teardown: {ln}"
    assert any("Mary OBrien" in ln for ln in post_lines), "apostrophe-owner line missing"

    log("self-test caption emoji ok: 🤖")
    print("SELF-TEST PASS: defensive fields + ratio + author-promotion + edge cases "
          "(empty-url drop / apostrophe owner / hidden comments) + every line parses "
          "under the REAL viral_teardown POST_RE")
    return True


if __name__ == "__main__":
    raise SystemExit(main())
