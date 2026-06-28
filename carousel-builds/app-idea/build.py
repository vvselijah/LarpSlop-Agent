# -*- coding: utf-8 -*-
"""'AI Builder Cheat Codes No.01' — find a million-dollar app idea with Claude.
Reverse-engineered from the 'Illegal Claude Secrets' reel, reframed to Elijah's
voice + anti-vibe-slop stance + his own series name. Dark 'gold' theme (money).
Render with ..\\headroom\\render.ps1 (headless Edge)."""
import os
BASE = os.path.dirname(os.path.abspath(__file__))

STRUCT = """
*{margin:0;padding:0;box-sizing:border-box}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;
  background:var(--bg);color:var(--ink);padding:150px 96px;
  display:flex;flex-direction:column;justify-content:center;
  font-family:var(--fb),'Segoe UI',sans-serif}
.brand{position:absolute;top:84px;left:96px;font:600 30px var(--fb);color:var(--muted);letter-spacing:.02em}
.swipe{position:absolute;bottom:78px;right:96px;font:500 30px var(--fb);color:var(--muted);opacity:.9}
.eyebrow{font:600 27px var(--fb);letter-spacing:.26em;text-transform:uppercase;color:var(--eye);margin-bottom:30px}
.h1{font-family:var(--fh);font-weight:var(--hw);color:var(--ink);letter-spacing:var(--ht)}
.h1.xl{font-size:96px;line-height:1.04}
.h1.lg{font-size:80px;line-height:1.07}
.h1.md{font-size:70px;line-height:1.09}
.ac{color:var(--accent)}
b{color:var(--ink);font-weight:700}
.emo{font-family:'Segoe UI Emoji'}
.sub{font:400 40px/1.4 var(--fb);color:var(--muted);margin-top:36px;max-width:900px}
.body{font:400 39px/1.45 var(--fb);color:var(--muted);margin-top:34px;max-width:900px}
.cap{margin-top:34px;font:400 33px/1.42 var(--fb);color:var(--muted);max-width:900px}
.footer{margin-top:58px;font:400 28px var(--fb);color:var(--muted)}
.step{display:inline-flex;align-items:center;gap:20px;margin-bottom:26px}
.snum{width:78px;height:78px;border-radius:20px;background:var(--accent);color:var(--onac);
  font:800 44px var(--fh);display:flex;align-items:center;justify-content:center;flex:none}
.steplab{font:600 27px var(--fb);letter-spacing:.22em;text-transform:uppercase;color:var(--eye)}
.prompt{margin-top:44px;background:var(--card);border:1px solid var(--cbd);border-left:5px solid var(--accent);
  border-radius:22px;padding:38px 42px}
.plabel{font:600 24px var(--fb);letter-spacing:.18em;text-transform:uppercase;color:var(--eye);margin-bottom:18px}
.ptext{font:500 37px/1.42 var(--fb);color:var(--ink)}
"""

THEMES = {
 "gold": {
  "label": "GOLD — dark, premium, money (AI Builder Cheat Codes)",
  "fonts": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Inter:wght@400;600;700&display=swap",
  "vars": """:root{
    --bg:repeating-linear-gradient(0deg, transparent 0 78px, rgba(245,179,1,.12) 78px 80px), repeating-linear-gradient(90deg, transparent 0 78px, rgba(245,179,1,.12) 78px 80px), radial-gradient(82% 62% at 100% 0%, rgba(245,179,1,.22), transparent 56%), radial-gradient(74% 60% at 0% 100%, rgba(176,128,12,.20), transparent 56%), radial-gradient(125% 100% at 16% -8%, #221a0b 0%, #17120a 52%, #0b0905 100%);
    --ink:#ffffff; --muted:#c9bfa6; --accent:#f5b301; --asoft:rgba(245,179,1,.13);
    --onac:#1a1407; --card:rgba(255,255,255,.05); --cbd:rgba(255,255,255,.14);
    --hair:rgba(255,255,255,.10); --eye:#f5c542; --barmute:rgba(255,255,255,.18);
    --fh:'Plus Jakarta Sans'; --fb:'Inter'; --hw:800; --ht:-.02em;}""",
 },
}

# --- design tweak variants of the gold deck (cover comparison) ---
_FONTS = THEMES["gold"]["fonts"]
THEMES["gold_pin"] = {"label": "GOLD · diagonal pinstripe", "fonts": _FONTS, "vars": """:root{
    --bg:repeating-linear-gradient(45deg, transparent 0 54px, rgba(245,179,1,.11) 54px 56px), radial-gradient(82% 62% at 100% 0%, rgba(245,179,1,.22), transparent 56%), radial-gradient(74% 60% at 0% 100%, rgba(176,128,12,.18), transparent 56%), radial-gradient(125% 100% at 16% -8%, #221a0b 0%, #17120a 52%, #0b0905 100%);
    --ink:#ffffff; --muted:#c9bfa6; --accent:#f5b301; --asoft:rgba(245,179,1,.13);
    --onac:#1a1407; --card:rgba(255,255,255,.05); --cbd:rgba(255,255,255,.14);
    --hair:rgba(255,255,255,.10); --eye:#f5c542; --barmute:rgba(255,255,255,.18);
    --fh:'Plus Jakarta Sans'; --fb:'Inter'; --hw:800; --ht:-.02em;}"""}
THEMES["gold_glow"] = {"label": "GOLD · glows only (no lines)", "fonts": _FONTS, "vars": """:root{
    --bg:radial-gradient(92% 72% at 100% 0%, rgba(245,179,1,.32), transparent 58%), radial-gradient(86% 70% at 0% 100%, rgba(176,128,12,.26), transparent 58%), radial-gradient(60% 50% at 48% 46%, rgba(245,179,1,.10), transparent 62%), radial-gradient(125% 100% at 16% -8%, #221a0b 0%, #17120a 52%, #0b0905 100%);
    --ink:#ffffff; --muted:#c9bfa6; --accent:#f5b301; --asoft:rgba(245,179,1,.13);
    --onac:#1a1407; --card:rgba(255,255,255,.05); --cbd:rgba(255,255,255,.14);
    --hair:rgba(255,255,255,.10); --eye:#f5c542; --barmute:rgba(255,255,255,.18);
    --fh:'Plus Jakarta Sans'; --fb:'Inter'; --hw:800; --ht:-.02em;}"""}
THEMES["green_grid"] = {"label": "GREEN · money accent + grid", "fonts": _FONTS, "vars": """:root{
    --bg:repeating-linear-gradient(0deg, transparent 0 78px, rgba(52,211,153,.12) 78px 80px), repeating-linear-gradient(90deg, transparent 0 78px, rgba(52,211,153,.12) 78px 80px), radial-gradient(82% 62% at 100% 0%, rgba(52,211,153,.22), transparent 56%), radial-gradient(74% 60% at 0% 100%, rgba(20,140,92,.20), transparent 56%), radial-gradient(125% 100% at 16% -8%, #0c241a 0%, #0a1712 52%, #050b08 100%);
    --ink:#ffffff; --muted:#a9c2b6; --accent:#34d399; --asoft:rgba(52,211,153,.13);
    --onac:#04130d; --card:rgba(255,255,255,.05); --cbd:rgba(255,255,255,.14);
    --hair:rgba(255,255,255,.10); --eye:#6ee7b7; --barmute:rgba(255,255,255,.18);
    --fh:'Plus Jakarta Sans'; --fb:'Inter'; --hw:800; --ht:-.02em;}"""}

BR = '<div class="brand">@elijahaifl</div>'
SW = '<div class="swipe">swipe &rarr;</div>'

def stephead(n, lab):
    return '<div class="step"><div class="snum">%d</div><div class="steplab">%s</div></div>' % (n, lab)

SLIDES = [
 # 1 — cover
 (BR + '<div><div class="eyebrow">AI builder cheat codes &middot; 01</div>'
  '<h1 class="h1 xl">how to find a <span class="ac">million-dollar app idea</span> in 60 seconds.</h1>'
  '<p class="sub">with Claude + your phone. no idea of your own required. save this. <span class="emo">&#128278;</span></p></div>' + SW),
 # 2 — premise
 (BR + '<div class="eyebrow">the unlock</div>'
  '<h1 class="h1 lg">every top app in the store is a <span class="ac">map to a better one.</span></h1>'
  '<p class="body">a calorie app built by two teens reportedly just sold for 8 figures. the idea that beats it is sitting in its 1-star reviews &mdash; here&rsquo;s how to pull it out. <span class="emo">&#128071;</span></p>' + SW),
 # 3 — step 1
 (BR + stephead(1, 'steal a proven market')
  + '<h1 class="h1 md">start with something people <span class="ac">already pay for.</span></h1>'
  '<p class="body">open the App Store, search a niche (&ldquo;meal tracker&rdquo;, &ldquo;habit tracker&rdquo;, anything). pick a top app &mdash; it already proved the demand is real.</p>' + SW),
 # 4 — step 2
 (BR + stephead(2, 'screenshot the complaints')
  + '<h1 class="h1 md">the <span class="ac">1-star reviews</span> are the goldmine.</h1>'
  '<p class="body">screenshot the features list AND the angry reviews. every complaint is a free list of what the market leader gets wrong.</p>' + SW),
 # 5 — step 3
 (BR + stephead(3, 'let Claude find the gap')
  + '<h1 class="h1 md">paste it in. ask for the <span class="ac">opening.</span></h1>'
  '<div class="prompt"><div class="plabel">the prompt</div><div class="ptext">&ldquo;here are an app&rsquo;s features + reviews. who&rsquo;s the ideal customer, the #1 problem it solves, and &mdash; based on the reviews &mdash; the gap nobody&rsquo;s filling?&rdquo;</div></div>'
  '<p class="cap">it hands you the wedge in seconds.</p>' + SW),
 # 6 — step 4
 (BR + stephead(4, 'find the AI angle')
  + '<h1 class="h1 md">where AI makes it <span class="ac">10x easier</span> = your edge.</h1>'
  '<div class="prompt"><div class="plabel">the prompt</div><div class="ptext">&ldquo;if I rebuilt this, where could AI make it 10x more convenient than the original?&rdquo;</div></div>'
  '<p class="cap">that answer is the unfair feature &mdash; the reason someone switches to yours.</p>' + SW),
 # 7 — step 5
 (BR + stephead(5, 'build it right')
  + '<h1 class="h1 md">ship it with a <span class="ac">system</span> &mdash; not vibe-slop.</h1>'
  '<p class="body">open Claude Code and build the MVP inside a loop (plan &rarr; build &rarr; review), so it holds up with real users. that&rsquo;s the line between a demo and a business.</p>' + SW),
 # 8 — CTA
 (BR + '<div><div class="eyebrow">your turn</div>'
  '<h1 class="h1 lg">save this. then run it on <span class="ac">your</span> niche tonight.</h1>'
  '<p class="sub">02: how to get your first 100 users. follow so you don&rsquo;t miss it.</p>'
  '<div class="footer">@elijahaifl &middot; putting you on game &middot; Jesus is how <span class="emo">&#128591;</span></div></div>'),
]

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="%s" rel="stylesheet"><style>%s\n%s</style></head><body>')
TAIL = '</body></html>'

BOARD_CSS = """
body{background:#14120c;font-family:Inter,sans-serif}
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
    thumbs = "".join('<div class="thumb"><div class="slide">%s</div></div>' % f for f in SLIDES)
    body = '<div class="board"><div class="title">%s</div>%s</div>' % (t["label"], thumbs)
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
