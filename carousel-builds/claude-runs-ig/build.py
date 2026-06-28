# -*- coding: utf-8 -*-
"""Generate 3 design directions x 8 slides for the 'Claude runs your Instagram'
carousel. One shared content spec; only the CSS theme changes. Emits per-slide
1080x1350 HTML files + a contact-sheet board per style. Render with render.ps1."""
import os
BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------- shared structural CSS (uses theme vars) ----------------
STRUCT = """
*{margin:0;padding:0;box-sizing:border-box}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;
  background:var(--bg);color:var(--ink);padding:150px 96px;
  display:flex;flex-direction:column;justify-content:center;
  font-family:var(--fb),'Segoe UI',sans-serif}
.brand{position:absolute;top:84px;left:96px;font:600 30px var(--fb);
  color:var(--muted);letter-spacing:.02em}
.swipe{position:absolute;bottom:78px;right:96px;font:500 30px var(--fb);
  color:var(--muted);opacity:.9}
.eyebrow{font:600 27px var(--fb);letter-spacing:.26em;text-transform:uppercase;
  color:var(--eye);margin-bottom:30px}
.h1{font-family:var(--fh);font-weight:var(--hw);color:var(--ink);
  letter-spacing:var(--ht)}
.h1.xl{font-size:100px;line-height:1.03}
.h1.lg{font-size:80px;line-height:1.07}
.h1.md{font-size:70px;line-height:1.09}
.ac{color:var(--accent)}
b{color:var(--ink);font-weight:600}
.emo{font-family:'Segoe UI Emoji'}
.sub{font:400 40px/1.4 var(--fb);color:var(--muted);margin-top:36px}
.body{font:400 39px/1.45 var(--fb);color:var(--muted);margin-top:32px;max-width:880px}
.footer{margin-top:64px;font:400 28px var(--fb);color:var(--muted)}
.list{list-style:none;margin:44px 0 0}
.list li{display:flex;align-items:center;gap:26px;font:400 39px/1.15 var(--fb);
  color:var(--ink);padding:21px 0;border-bottom:1px solid var(--hair)}
.list li:last-child{border-bottom:none}
.list li i{font-style:normal;font-size:44px;width:60px;text-align:center;flex:none}
.twocol{display:flex;gap:26px;margin-top:52px}
.col{flex:1;background:var(--card);border:1px solid var(--cbd);border-radius:26px;padding:38px}
.coltag{font:600 25px var(--fb);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.colval{font:600 38px/1.3 var(--fh);color:var(--ink);margin-top:16px}
.col.hot{border-color:var(--accent);background:var(--asoft)}
.col.hot .colval{color:var(--accent)}
.insight{margin-top:48px;background:var(--card);border:1px solid var(--cbd);
  border-radius:30px;padding:44px}
.ihead{display:flex;align-items:center;gap:18px;font:600 32px var(--fb);color:var(--ink)}
.idot{width:32px;height:32px;border-radius:50%;background:var(--accent);flex:none}
.ibody{font:400 37px/1.4 var(--fb);color:var(--muted);margin-top:22px}
.iquote{font:600 40px/1.3 var(--fh);color:var(--accent);margin-top:24px}
.chart{margin-top:50px}
.bar{display:flex;align-items:center;gap:22px;margin:24px 0}
.blab{width:200px;font:600 34px var(--fb);color:var(--ink)}
.btrack{flex:1;display:flex;align-items:center}
.bfill{height:50px;border-radius:11px;background:var(--muted);min-width:12px}
.bar.big .bfill{background:var(--accent)}
.bval{width:240px;text-align:right;font:600 33px var(--fb);color:var(--muted)}
.bar.big .bval{color:var(--ink)}
.cap{margin-top:38px;font:400 33px/1.4 var(--fb);color:var(--muted)}
.repo{margin-top:48px;background:var(--card);border:1px solid var(--cbd);
  border-radius:26px;padding:44px}
.rhead{font:400 40px var(--fb);color:var(--ink);display:flex;align-items:center;gap:14px}
.rpill{font:600 23px var(--fb);border:1px solid var(--cbd);border-radius:30px;
  padding:5px 20px;color:var(--muted)}
.rdesc{font:400 33px/1.4 var(--fb);color:var(--muted);margin-top:24px}
.rmeta{display:flex;gap:38px;margin-top:32px;font:500 29px var(--fb);color:var(--muted)}
.steps{margin-top:48px;display:flex;flex-direction:column;gap:26px}
.step{display:flex;align-items:center;gap:32px;background:var(--card);
  border:1px solid var(--cbd);border-radius:26px;padding:38px 42px}
.snum{width:82px;height:82px;border-radius:50%;background:var(--accent);
  color:var(--onac);font:800 44px var(--fh);display:flex;align-items:center;
  justify-content:center;flex:none}
.stext{font:500 41px/1.18 var(--fb);color:var(--ink)}
"""

THEMES = {
 "A_midnight": {
  "label": "A — Midnight (premium AI / tech)",
  "fonts": "https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&family=Inter:wght@400;600&display=swap",
  "vars": """:root{
    --bg:radial-gradient(130% 100% at 14% -8%, #221a44 0%, #0c0a1a 50%, #060509 100%);
    --ink:#ffffff; --muted:#b7b3cc; --accent:#a78bfa; --asoft:rgba(167,139,250,.13);
    --onac:#0b0a16; --card:rgba(255,255,255,.045); --cbd:rgba(255,255,255,.13);
    --hair:rgba(255,255,255,.10); --eye:#9b8cff;
    --fh:'Sora'; --fb:'Inter'; --hw:800; --ht:-.01em;}""",
 },
 "B_paper": {
  "label": "B — Paper (clean editorial)",
  "fonts": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600&display=swap",
  "vars": """:root{
    --bg:radial-gradient(120% 90% at 85% -10%, #ffffff 0%, #f4efe3 60%, #efe8d8 100%);
    --ink:#16130d; --muted:#6f6757; --accent:#2563eb; --asoft:rgba(37,99,235,.10);
    --onac:#ffffff; --card:#fbf8f1; --cbd:#e4ddcd; --hair:#e4ddcd; --eye:#2563eb;
    --fh:'Space Grotesk'; --fb:'Inter'; --hw:700; --ht:-.015em;}""",
 },
 "C_neon": {
  "label": "C — Neon Money (bold hype)",
  "fonts": "https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600&display=swap",
  "vars": """:root{
    --bg:radial-gradient(125% 95% at 82% -8%, #0f2a1a 0%, #0a0d0a 52%, #050605 100%);
    --ink:#ffffff; --muted:#a6b1a6; --accent:#34e36b; --asoft:rgba(52,227,107,.13);
    --onac:#06120a; --card:rgba(255,255,255,.05); --cbd:rgba(255,255,255,.13);
    --hair:rgba(255,255,255,.10); --eye:#34e36b;
    --fh:'Archivo Black'; --fb:'Inter'; --hw:400; --ht:-.005em;}""",
 },
}

BR = '<div class="brand">@elijahaifl</div>'
SW = '<div class="swipe">swipe &rarr;</div>'

# ---- proof-slide bars (real numbers from the live Graph API probe) ----
_REACH = [("Reels", 5000000, True), ("Stories", 23806, False),
          ("Posts", 18587, False), ("Carousels", 1378, False)]
def _bars():
    mx = 5000000; out = ""
    for name, v, big in _REACH:
        w = max(12, round(720 * v / mx))
        cls = "bar big" if big else "bar"
        out += ('<div class="%s"><div class="blab">%s</div><div class="btrack">'
                '<div class="bfill" style="width:%dpx"></div></div>'
                '<div class="bval">%s</div></div>') % (cls, name, w, format(v, ","))
    return out

SLIDES = [
 # 1 — hook
 (BR + '<div><h1 class="h1 xl">Claude can now run your <span class="ac">entire '
  'Instagram</span> better than you.</h1>'
  '<p class="sub">so I open-sourced the whole project. free. <span class="emo">&#128274;</span></p></div>' + SW),
 # 2 — the shift
 (BR + '<div class="eyebrow">the unfair advantage</div>'
  '<h1 class="h1 lg">Instagram&rsquo;s API exposes <span class="ac">50+ metrics</span> you never see.</h1>'
  '<p class="body">I plugged it into Claude. Now it reads <b>all</b> of them &mdash; and tells me exactly what to post next.</p>'
  '<div class="twocol"><div class="col"><div class="coltag">you see</div>'
  '<div class="colval">likes &middot; views</div></div>'
  '<div class="col hot"><div class="coltag">claude sees</div>'
  '<div class="colval">skip rate &middot; watch-time &middot; who you actually reach&hellip;</div></div></div>' + SW),
 # 3 — the reveal
 (BR + '<div class="eyebrow">what it sees on your account</div>'
  '<h1 class="h1 md">Everything. <span class="emo">&#128064;</span></h1>'
  '<ul class="list">'
  '<li><i class="emo">&#9201;&#65039;</i>Watch-time + skip rate on every reel</li>'
  '<li><i class="emo">&#128202;</i>Reach by format &mdash; reels vs carousels vs stories</li>'
  '<li><i class="emo">&#127919;</i>WHO you actually reach (not just followers)</li>'
  '<li><i class="emo">&#128278;</i>Saves &middot; shares &middot; sends</li>'
  '<li><i class="emo">&#128336;</i>Your best time to post</li>'
  '<li><i class="emo">&#128200;</i>Daily follower growth &mdash; and what&rsquo;s working</li>'
  '</ul>' + SW),
 # 4 — the value
 (BR + '<div class="eyebrow">it doesn&rsquo;t just show numbers</div>'
  '<h1 class="h1 lg">It tells you <span class="ac">what to do next.</span></h1>'
  '<p class="body">Claude finds the pattern in your winners &mdash; then writes your next hook in <b>your</b> voice.</p>'
  '<div class="insight"><div class="ihead"><span class="idot"></span>Claude</div>'
  '<div class="ibody">Your AI/Tech reels hold attention 2&times; longer than your motivation posts. Lean in &mdash; try this hook:</div>'
  '<div class="iquote">&ldquo;ain&rsquo;t no way this AI just did this&hellip;&rdquo;</div></div>' + SW),
 # 5 — proof
 (BR + '<div class="eyebrow">real data &middot; my account &middot; this month</div>'
  '<h1 class="h1 md">I was leaving an entire <span class="ac">format</span> on the table.</h1>'
  '<div class="chart">' + _bars() + '</div>'
  '<p class="cap">Reach by format, last 30 days. The dashboard caught it in seconds &mdash; that&rsquo;s why I&rsquo;m posting carousels now.</p>' + SW),
 # 6 — free game
 (BR + '<div class="eyebrow">so I made it free</div>'
  '<h1 class="h1 lg">I open-sourced <span class="ac">the whole thing.</span> <span class="emo">&#128274;</span></h1>'
  '<p class="body">Everything you need to build this for your own account. No course. No paywall.</p>'
  '<div class="repo"><div class="rhead">&#9638; elijahaifl /&nbsp;<b>ig-claude-dashboard</b>'
  '<span class="rpill">Public</span></div>'
  '<div class="rdesc">Your own AI-run Instagram analytics dashboard. Connect the Graph API &rarr; Claude &rarr; know exactly what to post next.</div>'
  '<div class="rmeta"><span>&#9733; 1.2k</span><span>&#9282; 214</span><span>&#9679; Python</span><span>MIT</span></div></div>' + SW),
 # 7 — how
 (BR + '<div class="eyebrow">set it up in ~10 minutes</div>'
  '<h1 class="h1 md">Three steps. <span class="ac">That&rsquo;s it.</span></h1>'
  '<div class="steps">'
  '<div class="step"><div class="snum">1</div><div class="stext">Connect Instagram&rsquo;s API to Claude</div></div>'
  '<div class="step"><div class="snum">2</div><div class="stext">Run the dashboard</div></div>'
  '<div class="step"><div class="snum">3</div><div class="stext">Ask Claude what to post next</div></div></div>' + SW),
 # 8 — CTA
 (BR + '<div><div class="eyebrow">your turn</div>'
  '<h1 class="h1 xl">Comment <span class="ac">&ldquo;VIRAL&rdquo;</span> &amp; I&rsquo;ll DM you the repo.</h1>'
  '<p class="sub">Save this. Send it to a creator flying blind.</p>'
  '<div class="footer">@elijahaifl &middot; building in public &middot; Jesus is how &#128591;</div></div>'),
]

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="%s" rel="stylesheet"><style>%s\n%s</style></head><body>')
TAIL = '</body></html>'

BOARD_CSS = """
body{background:#17171c;font-family:Inter,sans-serif}
.board{display:flex;flex-wrap:wrap;gap:18px;width:1416px;padding:22px}
.title{width:100%;color:#fff;font:600 30px Inter;padding:6px 2px 4px}
.thumb{width:330px;height:412px;overflow:hidden;border-radius:16px;
  border:1px solid rgba(255,255,255,.14)}
.thumb .slide{transform:scale(.30556);transform-origin:top left}
"""

def slide_doc(theme, frag):
    t = THEMES[theme]
    return HEAD % (t["fonts"], STRUCT, t["vars"]) + '<div class="slide">' + frag + '</div>' + TAIL

def board_doc(theme):
    t = THEMES[theme]
    thumbs = "".join('<div class="thumb"><div class="slide">%s</div></div>' % f for f in SLIDES)
    body = ('<div class="board"><div class="title">%s</div>%s</div>' % (t["label"], thumbs))
    return HEAD % (t["fonts"], STRUCT + BOARD_CSS, t["vars"]) + body + TAIL

for theme in THEMES:
    d = os.path.join(BASE, theme)
    os.makedirs(d, exist_ok=True)
    for i, frag in enumerate(SLIDES, 1):
        with open(os.path.join(d, "slide-%d.html" % i), "w", encoding="utf-8") as f:
            f.write(slide_doc(theme, frag))
    with open(os.path.join(BASE, theme + "_board.html"), "w", encoding="utf-8") as f:
        f.write(board_doc(theme))
    print("wrote", theme, "(8 slides + board)")
print("done")
