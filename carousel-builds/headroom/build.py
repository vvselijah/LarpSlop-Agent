# -*- coding: utf-8 -*-
"""Headroom carousel — 'I found a free tool' peer-share (NOT an ad).
Two fresh premium themes (Frost = light, Aqua = dark). Shared content + structure;
only the theme vars change. Emits 8 slide HTMLs/theme + a contact-sheet board.
Render to PNG with render.ps1 (headless Edge)."""
import os
BASE = os.path.dirname(os.path.abspath(__file__))

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
.h1{font-family:var(--fh);font-weight:var(--hw);color:var(--ink);letter-spacing:var(--ht)}
.h1.xl{font-size:98px;line-height:1.04}
.h1.lg{font-size:80px;line-height:1.07}
.h1.md{font-size:68px;line-height:1.1}
.ac{color:var(--accent)}
b{color:var(--ink);font-weight:700}
.emo{font-family:'Segoe UI Emoji'}
.sub{font:400 40px/1.4 var(--fb);color:var(--muted);margin-top:36px;max-width:900px}
.body{font:400 39px/1.45 var(--fb);color:var(--muted);margin-top:34px;max-width:900px}
.footer{margin-top:60px;font:400 28px var(--fb);color:var(--muted)}
.list{list-style:none;margin:46px 0 0}
.list li{display:flex;align-items:center;gap:28px;font:400 38px/1.18 var(--fb);
  color:var(--ink);padding:24px 0;border-bottom:1px solid var(--hair)}
.list li:last-child{border-bottom:none}
.list li i{font-style:normal;font-size:46px;width:64px;text-align:center;flex:none}
.twocol{display:flex;gap:26px;margin-top:52px}
.col{flex:1;background:var(--card);border:1px solid var(--cbd);border-radius:28px;padding:40px}
.coltag{font:600 25px var(--fb);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.colval{font:600 40px/1.28 var(--fh);color:var(--ink);margin-top:18px}
.col.hot{border-color:var(--accent);background:var(--asoft)}
.col.hot .colval{color:var(--accent)}
.cap{margin-top:40px;font:400 32px/1.42 var(--fb);color:var(--muted);max-width:900px}
.repo{margin-top:50px;background:var(--card);border:1px solid var(--cbd);border-radius:30px;padding:48px}
.rhead{font:400 42px var(--fb);color:var(--ink);display:flex;align-items:center;gap:14px}
.rpill{font:600 23px var(--fb);border:1px solid var(--cbd);border-radius:30px;padding:5px 20px;color:var(--muted)}
.rdesc{font:400 33px/1.45 var(--fb);color:var(--muted);margin-top:26px}
.rmeta{display:flex;flex-wrap:wrap;gap:20px 36px;margin-top:34px;font:500 28px var(--fb);color:var(--muted)}
.chart{margin-top:54px}
.bar{display:flex;align-items:center;gap:24px;margin:26px 0}
.blab{width:170px;font:600 32px var(--fb);color:var(--muted);text-transform:lowercase}
.btrack{flex:1;display:flex;align-items:center}
.bfill{height:54px;border-radius:12px;background:var(--barmute);min-width:14px}
.bar.big .bfill{background:var(--accent)}
.bval{width:230px;text-align:right;font:600 34px var(--fb);color:var(--muted)}
.bar.big .bval{color:var(--ink)}
.delta{font-family:var(--fh);font-weight:var(--hw);font-size:84px;color:var(--accent);margin-top:30px;letter-spacing:var(--ht)}
.footer{margin-top:58px;font:400 28px var(--fb);color:var(--muted)}
"""

THEMES = {
 "frost": {
  "label": "FROST  —  light, fresh, premium (teal)",
  "fonts": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Inter:wght@400;600;700&display=swap",
  "vars": """:root{
    --bg:repeating-linear-gradient(0deg, transparent 0 78px, rgba(11,134,128,.34) 78px 80px), repeating-linear-gradient(90deg, transparent 0 78px, rgba(11,134,128,.34) 78px 80px), radial-gradient(85% 65% at 2% 0%, rgba(12,156,149,.42), transparent 56%), radial-gradient(82% 64% at 100% 100%, rgba(8,138,132,.34), transparent 56%), linear-gradient(160deg, #ffffff 0%, #e9f3f2 55%, #ddebea 100%);
    --ink:#0b1418; --muted:#566169; --accent:#0c9c95; --asoft:rgba(12,156,149,.10);
    --onac:#ffffff; --card:#ffffff; --cbd:#d8e3e4; --hair:#dde7e8; --eye:#0a8a84;
    --barmute:#cdd9da;
    --fh:'Plus Jakarta Sans'; --fb:'Inter'; --hw:800; --ht:-.02em;}""",
 },
 "aqua": {
  "label": "AQUA  —  dark, premium, techy (turquoise)",
  "fonts": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Inter:wght@400;600;700&display=swap",
  "vars": """:root{
    --bg:repeating-radial-gradient(circle at 100% 0%, transparent 0 90px, rgba(45,212,191,.20) 90px 92px), radial-gradient(72% 62% at 100% 0%, rgba(45,212,191,.26), transparent 56%), radial-gradient(80% 66% at 0% 100%, rgba(20,130,124,.20), transparent 56%), radial-gradient(125% 100% at 16% -8%, #0b2a31 0%, #08171c 50%, #04090b 100%);
    --ink:#ffffff; --muted:#9fb6bb; --accent:#2dd4bf; --asoft:rgba(45,212,191,.13);
    --onac:#04130f; --card:rgba(255,255,255,.05); --cbd:rgba(255,255,255,.13);
    --hair:rgba(255,255,255,.10); --eye:#5eead4; --barmute:rgba(255,255,255,.18);
    --fh:'Plus Jakarta Sans'; --fb:'Inter'; --hw:800; --ht:-.02em;}""",
 },
}

import re
_FROST_VARS = THEMES["frost"]["vars"]
def _frost_bg(bg):
    return re.sub(r"--bg:[^;]*;", "--bg:" + bg + ";", _FROST_VARS, count=1)
_BGS = {
 "frost_grid":   ("FROST · graph grid",
   "repeating-linear-gradient(0deg, transparent 0 79px, rgba(12,156,149,.085) 79px 80px), "
   "repeating-linear-gradient(90deg, transparent 0 79px, rgba(12,156,149,.085) 79px 80px), "
   "radial-gradient(85% 68% at 100% 0%, rgba(12,156,149,.16), transparent 58%), "
   "radial-gradient(120% 95% at 50% -14%, #ffffff 0%, #eef3f4 52%, #e3edee 100%)"),
 "frost_dots":   ("FROST · dot matrix",
   "radial-gradient(rgba(12,156,149,.13) 1.4px, transparent 1.5px) 0 0 / 44px 44px, "
   "radial-gradient(120% 95% at 50% -14%, #ffffff 0%, #eef3f4 52%, #e3edee 100%)"),
 "frost_aurora": ("FROST · aurora gradient",
   "radial-gradient(80% 60% at 6% 2%, rgba(12,156,149,.13), transparent 55%), "
   "radial-gradient(70% 55% at 100% 100%, rgba(8,138,132,.10), transparent 55%), "
   "linear-gradient(160deg, #ffffff 0%, #eef4f4 55%, #e6eff0 100%)"),
}
for _k,(_lab,_bg) in _BGS.items():
    THEMES[_k] = {"label": _lab, "fonts": THEMES["frost"]["fonts"], "vars": _frost_bg(_bg)}

BR = '<div class="brand">@elijahaifl</div>'
SW = '<div class="swipe">swipe &rarr;</div>'

def _bars():
    before, after, mx = 48210, 3074, 48210
    rows = [("before", before, False), ("after", after, True)]
    out = ""
    for name, v, big in rows:
        w = max(16, round(400 * v / mx))
        cls = "bar big" if big else "bar"
        out += ('<div class="%s"><div class="blab">%s</div><div class="btrack">'
                '<div class="bfill" style="width:%dpx"></div></div>'
                '<div class="bval">%s</div></div>') % (cls, name, w, format(v, ","))
    return out

SLIDES = [
 # 1 — hook: the discovery (disbelief), peer share
 (BR + '<div><div class="eyebrow">ok i have to put you on</div>'
  '<h1 class="h1 xl">this AI tool is free and it <span class="ac">shouldn&rsquo;t be.</span></h1>'
  '<p class="sub">it deletes the tokens you&rsquo;re wasting &mdash; up to 90% &mdash; before you ever pay for them. same answers. swipe, then go grab it. <span class="emo">&#128274;</span></p></div>' + SW),
 # 2 — the problem
 (BR + '<div class="eyebrow">why your AI bill is so high</div>'
  '<h1 class="h1 lg">you&rsquo;re paying for <span class="ac">garbage</span> the model never even reads.</h1>'
  '<p class="body">every log, file, database dump, and doc your AI reads &mdash; you pay for <b>every token</b> of it. even the 90% that&rsquo;s pure noise.</p>' + SW),
 # 3 — the insight
 (BR + '<div class="eyebrow">the part nobody says</div>'
  '<h1 class="h1 lg">the model doesn&rsquo;t need all that. <span class="ac">so stop sending it.</span></h1>'
  '<p class="body">strip the junk <b>before</b> it hits the AI and you get the same answer for a fraction of the tokens. that&rsquo;s the whole trick.</p>' + SW),
 # 4 — the tool (reveal) — repo card holds the "what it is" info
 (BR + '<div class="eyebrow">the tool i found</div>'
  '<h1 class="h1 md">one free thing that sits <span class="ac">between you and the AI.</span></h1>'
  '<div class="repo"><div class="rhead">&#9638; headroomlabs-ai /&nbsp;<b>headroom</b><span class="rpill">Public</span></div>'
  '<div class="rdesc">Compress tool outputs, logs, files &amp; RAG chunks before they reach the LLM. 60&ndash;95% fewer tokens, same answers. Library, proxy, MCP server.</div>'
  '<div class="rmeta"><span>&#9733; 51k stars</span><span>&#9282; 3.5k</span><span>Apache-2.0 &middot; free</span><span>built by a Netflix engineer</span></div></div>' + SW),
 # 5 — how it works / the numbers
 (BR + '<div class="eyebrow">what that actually does</div>'
  '<h1 class="h1 md">same task. <span class="ac">94% fewer tokens.</span></h1>'
  '<div class="chart">' + _bars() + '</div>'
  '<p class="cap">it sits in as a library, proxy, or MCP and compresses everything your AI reads first. the repo&rsquo;s own benchmark: 60&ndash;95% fewer tokens, same answers.</p>' + SW),
 # 6 — what it strips
 (BR + '<div class="eyebrow">what it cleans up</div>'
  '<h1 class="h1 md">the stuff quietly <span class="ac">draining</span> your tokens:</h1>'
  '<ul class="list">'
  '<li><i class="emo">&#128220;</i>4,000-line logs &rarr; the lines that matter</li>'
  '<li><i class="emo">&#128193;</i>whole files &rarr; just the part it needs</li>'
  '<li><i class="emo">&#128451;</i>database dumps &rarr; only the rows that count</li>'
  '<li><i class="emo">&#128269;</i>giant RAG chunks &rarr; the relevant slice</li>'
  '<li><i class="emo">&#129520;</i>noisy tool output &rarr; the signal</li>'
  '</ul>' + SW),
 # 7 — why it's a cheat code (two wins)
 (BR + '<div class="eyebrow">why it&rsquo;s a cheat code</div>'
  '<h1 class="h1 lg">two wins, <span class="ac">not one.</span></h1>'
  '<div class="twocol"><div class="col"><div class="coltag">your wallet</div>'
  '<div class="colval">the bill just drops <span class="emo">&#128184;</span></div></div>'
  '<div class="col hot"><div class="coltag">your agent</div>'
  '<div class="colval">clean context = stays sharp on long tasks <span class="emo">&#129504;</span></div></div></div>'
  '<p class="cap">fewer tokens isn&rsquo;t just cheaper &mdash; a lighter context window keeps the AI actually good deep into a task, instead of going dumb halfway.</p>' + SW),
 # 8 — CTA: peer send
 (BR + '<div><div class="eyebrow">go get it &mdash; it&rsquo;s free</div>'
  '<h1 class="h1 lg">save this. <span class="ac">send it</span> to whoever&rsquo;s overpaying for AI.</h1>'
  '<p class="sub">it&rsquo;s on github: headroomlabs-ai / headroom. open source, no catch.</p>'
  '<div class="footer">@elijahaifl &middot; putting you on game &middot; Jesus is how <span class="emo">&#128591;</span></div></div>'),
]

# Reworded copy for the AQUA deck — same beats/facts/voice, fresh phrasing + a different hook.
SLIDES_AQUA = [
 (BR + '<div><div class="eyebrow">real ones need to see this</div>'
  '<h1 class="h1 xl">90% of your AI bill is <span class="ac">pure waste.</span></h1>'
  '<p class="sub">there&rsquo;s a free tool that strips it out before you ever pay &mdash; same answers, way fewer tokens. swipe. <span class="emo">&#128274;</span></p></div>' + SW),
 (BR + '<div class="eyebrow">where the money goes</div>'
  '<h1 class="h1 lg">your AI reads a <span class="ac">mountain of junk</span> &mdash; and bills you for all of it.</h1>'
  '<p class="body">logs, whole files, database dumps, docs. you pay <b>per token</b> &mdash; even for the 90% it never actually uses.</p>' + SW),
 (BR + '<div class="eyebrow">the move nobody makes</div>'
  '<h1 class="h1 lg">clean it up <span class="ac">before</span> it ever reaches the model.</h1>'
  '<p class="body">cut the noise on the way in and you get the same answer for a fraction of the cost. that&rsquo;s the entire hack.</p>' + SW),
 (BR + '<div class="eyebrow">meet the tool</div>'
  '<h1 class="h1 md">it slots in <span class="ac">between you and the model.</span></h1>'
  '<div class="repo"><div class="rhead">&#9638; headroomlabs-ai /&nbsp;<b>headroom</b><span class="rpill">Public</span></div>'
  '<div class="rdesc">Compress tool outputs, logs, files &amp; RAG chunks before they reach the LLM. 60&ndash;95% fewer tokens, same answers. Library, proxy, MCP server.</div>'
  '<div class="rmeta"><span>&#9733; 51k stars</span><span>&#9282; 3.5k</span><span>Apache-2.0 &middot; free</span><span>built by a Netflix engineer</span></div></div>' + SW),
 (BR + '<div class="eyebrow">the receipts</div>'
  '<h1 class="h1 md">one task. <span class="ac">94% fewer tokens.</span></h1>'
  '<div class="chart">' + _bars() + '</div>'
  '<p class="cap">drops in as a library, proxy, or MCP and shrinks everything your AI reads. the repo&rsquo;s own benchmark: 60&ndash;95% fewer tokens, same answers.</p>' + SW),
 (BR + '<div class="eyebrow">what gets trimmed</div>'
  '<h1 class="h1 md">the quiet token <span class="ac">drains</span> it kills:</h1>'
  '<ul class="list">'
  '<li><i class="emo">&#128220;</i>endless logs &rarr; only the lines that matter</li>'
  '<li><i class="emo">&#128193;</i>whole files &rarr; just the slice it needs</li>'
  '<li><i class="emo">&#128451;</i>database dumps &rarr; the rows that count</li>'
  '<li><i class="emo">&#128269;</i>bloated RAG chunks &rarr; the relevant bit</li>'
  '<li><i class="emo">&#129520;</i>messy tool output &rarr; the signal</li>'
  '</ul>' + SW),
 (BR + '<div class="eyebrow">why it&rsquo;s basically cheating</div>'
  '<h1 class="h1 lg">you win <span class="ac">twice.</span></h1>'
  '<div class="twocol"><div class="col"><div class="coltag">your wallet</div>'
  '<div class="colval">the bill drops <span class="emo">&#128184;</span></div></div>'
  '<div class="col hot"><div class="coltag">your agent</div>'
  '<div class="colval">lean context = stays sharp deep into long tasks <span class="emo">&#129504;</span></div></div></div>'
  '<p class="cap">fewer tokens isn&rsquo;t just cheaper &mdash; a clean context window keeps it from going dumb halfway through a big task.</p>' + SW),
 (BR + '<div><div class="eyebrow">grab it &mdash; free</div>'
  '<h1 class="h1 lg">save this. then <span class="ac">send it</span> to someone still overpaying.</h1>'
  '<p class="sub">find it on github: headroomlabs-ai / headroom. open source, zero catch.</p>'
  '<div class="footer">@elijahaifl &middot; putting you on &middot; Jesus is how <span class="emo">&#128591;</span></div></div>'),
]

def content_for(theme):
    return SLIDES_AQUA if theme == "aqua" else SLIDES

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="%s" rel="stylesheet"><style>%s\n%s</style></head><body>')
TAIL = '</body></html>'

BOARD_CSS = """
body{background:#14171a;font-family:Inter,sans-serif}
.board{display:flex;flex-wrap:wrap;gap:18px;width:1416px;padding:22px}
.title{width:100%;color:#fff;font:600 30px Inter;padding:6px 2px 4px;letter-spacing:.04em}
.thumb{width:330px;height:412px;overflow:hidden;border-radius:16px;border:1px solid rgba(255,255,255,.14)}
.thumb .slide{transform:scale(.30556);transform-origin:top left}
"""

def slide_doc(theme, frag):
    t = THEMES[theme]
    return HEAD % (t["fonts"], STRUCT, t["vars"]) + '<div class="slide">' + frag + '</div>' + TAIL

def board_doc(theme):
    t = THEMES[theme]
    thumbs = "".join('<div class="thumb"><div class="slide">%s</div></div>' % f for f in content_for(theme))
    body = '<div class="board"><div class="title">%s</div>%s</div>' % (t["label"], thumbs)
    return HEAD % (t["fonts"], STRUCT + BOARD_CSS, t["vars"]) + body + TAIL

for theme in THEMES:
    d = os.path.join(BASE, theme)
    os.makedirs(d, exist_ok=True)
    for i, frag in enumerate(content_for(theme), 1):
        with open(os.path.join(d, "slide-%d.html" % i), "w", encoding="utf-8") as f:
            f.write(slide_doc(theme, frag))
    with open(os.path.join(BASE, theme + "_board.html"), "w", encoding="utf-8") as f:
        f.write(board_doc(theme))
    print("wrote", theme, "(8 slides + board)")
print("done")
