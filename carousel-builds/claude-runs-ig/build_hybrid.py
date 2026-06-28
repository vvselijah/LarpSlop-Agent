# -*- coding: utf-8 -*-
"""Full 8-slide HYBRID deck: editorial texture bg + recurring mascot + real
product shots (Claude Code terminal recreation + real dashboard) + brush
headlines + stickers + page pills. No handle. Render with render_hybrid.ps1."""
import os
BASE = os.path.dirname(os.path.abspath(__file__))
N = 8

BURST = ('<svg width="112" height="112" viewBox="0 0 100 100"><g fill="#cf5f2c">'
 + ''.join('<rect x="47.6" y="%d" width="4.8" height="%d" rx="2.4" transform="rotate(%d 50 50)"/>'
   % ((3,47,k) if k%60==0 else (9,41,k)) for k in range(0,360,30)) + '</g></svg>')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:#f1ddc8;
 color:#241813;font-family:'Inter',sans-serif}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.scrim{position:absolute;inset:0;background:radial-gradient(125% 95% at 50% 22%, rgba(248,238,226,.42), rgba(236,200,168,.06))}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.10;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:420px 420px}
.wrap{position:absolute;inset:0;padding:120px 92px;display:flex;flex-direction:column;justify-content:center}
.pill{position:absolute;top:60px;right:70px;background:rgba(0,0,0,.07);border:1px solid rgba(0,0,0,.2);
 border-radius:40px;padding:9px 24px;font:700 28px 'Inter';color:#241813;letter-spacing:.04em}
.swipe{position:absolute;right:88px;bottom:42px;font:600 28px 'Inter';color:#8a6147}
.eyebrow{font:600 26px 'Inter';letter-spacing:.24em;text-transform:uppercase;color:#b14a24;margin-bottom:26px}
.kick{font:700 64px 'Caveat';color:#241813;transform:rotate(-2deg);margin-bottom:6px}
.h{font-family:'Anton';font-weight:400;line-height:.95;letter-spacing:.5px;color:#241813;text-shadow:2px 3px 0 rgba(0,0,0,.07)}
.h.xl{font-size:150px}.h.lg{font-size:78px}.h.md{font-size:66px;line-height:1.02}
.or{color:#c2552c}
.brush{display:inline-block;background:#100c08;color:#fff;font-family:'Anton';letter-spacing:1px;
 padding:10px 30px 16px;
 clip-path:polygon(1% 16%,16% 5%,34% 11%,52% 3%,70% 12%,86% 4%,99% 10%,98% 78%,84% 95%,64% 86%,44% 96%,24% 85%,9% 94%,1% 82%)}
.sub{font:500 36px/1.35 'Inter';color:#241813;margin-top:26px}
.sub b{font-weight:700}
.body{font:400 38px/1.42 'Inter';color:#6e4f3c;margin-top:24px;max-width:840px}
.body b{color:#241813;font-weight:600}
.sticker{position:absolute;top:188px;right:90px;width:158px;height:158px;background:#fbf7ef;border-radius:30px;
 transform:rotate(13deg);box-shadow:0 20px 38px rgba(120,60,20,.26);display:flex;align-items:center;justify-content:center}
.crown{position:absolute;top:-36px;left:-16px;font-size:54px;transform:rotate(-18deg)}
.masc{position:absolute;filter:drop-shadow(0 24px 34px rgba(120,60,20,.30))}
.card{background:#fdf6ec;border:1px solid #e6d3bd;border-radius:24px;box-shadow:0 18px 34px rgba(120,60,20,.16)}
.list{list-style:none;margin-top:36px}
.list li{display:flex;align-items:center;gap:24px;font:400 38px/1.12 'Inter';color:#241813;
 padding:19px 0;border-bottom:1px solid #e2cdb5}
.list li:last-child{border-bottom:none}
.list li i{font-style:normal;font-size:42px;width:58px;text-align:center;flex:none}
.shot{border-radius:16px;box-shadow:0 22px 42px rgba(90,50,20,.30);border:6px solid #fff}
/* terminal */
.term{width:600px;background:#181410;border-radius:16px;overflow:hidden;
 box-shadow:0 24px 44px rgba(80,40,10,.34);border:1px solid rgba(255,255,255,.08)}
.tbar{display:flex;align-items:center;gap:12px;padding:15px 18px;background:#221c16;
 font:500 21px 'JetBrains Mono';color:#cbb9a6}
.bot{width:28px;height:28px;border-radius:7px;background:#d4622e;position:relative;flex:none}
.bot:before,.bot:after{content:"";position:absolute;top:8px;width:6px;height:9px;background:#181410;border-radius:1px}
.bot:before{left:6px}.bot:after{right:6px}
.tbody{padding:22px 24px 26px;font:400 24px/1.5 'JetBrains Mono';color:#d9cdbd}
.tbody .mut{color:#8c7e6e}.tbody .or2{color:#e8853f}.tbody .gr{color:#69c389}
.cur{display:inline-block;width:12px;height:24px;background:#e8853f;vertical-align:-4px;margin-left:4px}
/* insight card */
.insight{margin-top:40px}
.ihead{display:flex;align-items:center;gap:16px;font:600 30px 'Inter';color:#241813;padding:34px 38px 0}
.idot{width:30px;height:30px;border-radius:50%;background:#c2552c;flex:none}
.ibody{font:400 34px/1.38 'Inter';color:#6e4f3c;padding:18px 38px 0}
.iquote{font:700 38px/1.3 'Inter';color:#c2552c;padding:14px 38px 34px}
/* chart */
.chart{margin-top:40px}
.bar{display:flex;align-items:center;gap:20px;margin:20px 0}
.blab{width:190px;font:600 32px 'Inter';color:#241813}
.btrack{flex:1;display:flex}
.bfill{height:46px;border-radius:10px;background:#c9a98f;min-width:12px}
.bar.big .bfill{background:#c2552c}
.bval{width:230px;text-align:right;font:600 31px 'Inter';color:#6e4f3c}
.bar.big .bval{color:#241813}
.cap{margin-top:30px;font:400 31px/1.38 'Inter';color:#6e4f3c}
/* repo */
.repo{margin-top:40px;padding:40px}
.rhead{font:400 38px 'Inter';color:#241813;display:flex;align-items:center;gap:12px}
.rpill{font:600 22px 'Inter';border:1px solid #e6d3bd;border-radius:30px;padding:5px 18px;color:#8a6147}
.rdesc{font:400 31px/1.4 'Inter';color:#6e4f3c;margin-top:22px}
.rmeta{display:flex;gap:34px;margin-top:28px;font:500 28px 'Inter';color:#8a6147}
/* steps */
.steps{margin-top:42px;display:flex;flex-direction:column;gap:24px}
.step{display:flex;align-items:center;gap:30px;padding:34px 40px}
.snum{width:78px;height:78px;border-radius:50%;background:#c2552c;color:#fff;font:400 42px 'Anton';
 display:flex;align-items:center;justify-content:center;flex:none}
.stext{font:500 40px/1.15 'Inter';color:#241813}
.center{height:100%;display:flex;flex-direction:column;justify-content:center}
"""

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
 '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
 '<style>%s</style></head><body>') % CSS
TAIL = '</body></html>'

def chrome(i, swipe=True):
    s = '<img class="bg" src="assets/m_texture.png"><div class="scrim"></div><div class="grain"></div>'
    s += '<div class="pill">%d/%d</div>' % (i, N)
    if swipe: s += '<div class="swipe">swipe &rarr;</div>'
    return s

STICKER = '<div class="sticker"><span class="crown">&#128081;</span>%s</div>' % BURST
MASC = lambda style: '<img class="masc" src="assets/m_mascot.png" style="%s">' % style

TERMINAL = ('<div class="term"><div class="tbar"><span class="bot"></span>Claude&nbsp;Code&nbsp;&middot;&nbsp;Opus&nbsp;4.8</div>'
 '<div class="tbody"><span class="mut">Using</span> Opus 4.8 <span class="mut">(.claude/settings.json)</span><br>'
 '&rsaquo; run my instagram<span class="cur"></span><br>'
 '<span class="or2">&#9656;&#9656; bypass permissions on</span><br><span class="gr">&#9679;</span> high <span class="mut">/effort</span></div></div>')

def bars():
    data=[("Reels",5000000,1),("Stories",23806,0),("Posts",18587,0),("Carousels",1378,0)]
    out=""
    for nm,v,big in data:
        w=max(12,round(700*v/5000000)); cls="bar big" if big else "bar"
        out+='<div class="%s"><div class="blab">%s</div><div class="btrack"><div class="bfill" style="width:%dpx"></div></div><div class="bval">%s</div></div>'%(cls,nm,w,format(v,","))
    return out

SLIDES = []
# 1 hook
SLIDES.append(chrome(1)+STICKER+MASC("bottom:-26px;right:-44px;width:560px")+
 '<div class="wrap"><div class="kick">Claude can now run your</div>'
 '<div class="h xl">ENTIRE<br><span class="or">INSTAGRAM</span></div>'
 '<div style="margin-top:18px"><span class="brush" style="font-size:84px">BETTER THAN YOU</span></div>'
 '<div class="sub">so I open-sourced the whole project. <b>free.</b> &#128274;</div></div>')
# 2 shift + terminal
SLIDES.append(chrome(2)+
 '<div class="wrap"><div class="eyebrow">the unfair advantage</div>'
 '<div class="h lg">Instagram&rsquo;s API hides<br><span class="or">50+ metrics</span> you never see.</div>'
 '<div class="body">I plugged it into Claude. Now it reads <b>all</b> of them &mdash; and tells me exactly what to post next.</div>'
 '<div style="margin-top:46px;transform:rotate(-2.5deg)">'+TERMINAL+'</div></div>')
# 3 reveal + list + dashboard thumb
SLIDES.append(chrome(3)+MASC("bottom:40px;right:-30px;width:300px")+
 '<div class="wrap"><div class="eyebrow">what it sees on your account</div>'
 '<div class="h md">Everything. &#128064;</div>'
 '<ul class="list">'
 '<li><i>&#9201;&#65039;</i>Watch-time + skip rate on every reel</li>'
 '<li><i>&#128202;</i>Reach by format &mdash; reels vs carousels</li>'
 '<li><i>&#127919;</i>WHO you actually reach (not just followers)</li>'
 '<li><i>&#128278;</i>Saves &middot; shares &middot; sends</li>'
 '<li><i>&#128200;</i>Best time to post &amp; daily growth</li></ul></div>')
# 4 value + insight + mascot
SLIDES.append(chrome(4)+MASC("bottom:-20px;right:-40px;width:330px")+
 '<div class="wrap"><div class="eyebrow">it doesn&rsquo;t just show numbers</div>'
 '<div class="h lg">It tells you<br><span class="or">what to do next.</span></div>'
 '<div class="card insight"><div class="ihead"><span class="idot"></span>Claude</div>'
 '<div class="ibody">Your AI/Tech reels hold attention 2&times; longer than your motivation posts. Lean in &mdash; try:</div>'
 '<div class="iquote">&ldquo;ain&rsquo;t no way this AI just did this&hellip;&rdquo;</div></div></div>')
# 5 proof + chart + real dashboard
SLIDES.append(chrome(5)+
 '<div class="wrap"><div class="eyebrow">real data &middot; my account &middot; this month</div>'
 '<div class="h md">I left an entire <span class="or">format</span> on the table.</div>'
 '<div class="chart">'+bars()+'</div>'
 '<img class="shot" src="_real_dashboard.png" style="width:600px;margin-top:34px;transform:rotate(-2deg)">'
 '<div class="cap">The dashboard caught it in seconds.</div></div>')
# 6 free game + repo + mascot
SLIDES.append(chrome(6)+MASC("bottom:-24px;right:-42px;width:340px")+
 '<div class="wrap"><div class="eyebrow">so I made it free</div>'
 '<div class="h lg">I open-sourced<br><span class="or">the whole thing.</span> &#128274;</div>'
 '<div class="body">Everything you need to build it for your own account. No course. No paywall.</div>'
 '<div class="card repo"><div class="rhead">&#9638; elijahaifl /&nbsp;<b>ig-claude-dashboard</b><span class="rpill">Public</span></div>'
 '<div class="rdesc">Your own AI-run Instagram analytics dashboard.</div>'
 '<div class="rmeta"><span>&#9733; 1.2k</span><span>&#9282; 214</span><span>&#9679; Python</span><span>MIT</span></div></div></div>')
# 7 how
SLIDES.append(chrome(7)+
 '<div class="wrap"><div class="eyebrow">set it up in ~10 minutes</div>'
 '<div class="h md">Three steps. <span class="or">That&rsquo;s it.</span></div>'
 '<div class="steps">'
 '<div class="card step"><div class="snum">1</div><div class="stext">Connect Instagram&rsquo;s API to Claude</div></div>'
 '<div class="card step"><div class="snum">2</div><div class="stext">Run the dashboard</div></div>'
 '<div class="card step"><div class="snum">3</div><div class="stext">Ask Claude what to post next</div></div></div></div>')
# 8 cta
SLIDES.append(chrome(8,swipe=False)+STICKER+MASC("bottom:-26px;right:-46px;width:520px")+
 '<div class="wrap"><div class="center"><div class="eyebrow">your turn</div>'
 '<div class="h lg">Comment <span class="or">&ldquo;VIRAL&rdquo;</span><br>&amp; I&rsquo;ll DM you the repo.</div>'
 '<div class="sub">Save this. Send it to a creator flying blind.</div>'
 '<div style="margin-top:30px;font:400 28px Inter;color:#8a6147">building in public &middot; Jesus is how &#128591;</div></div></div>')

for i, frag in enumerate(SLIDES, 1):
    with open(os.path.join(BASE, "hyb-%d.html" % i), "w", encoding="utf-8") as f:
        f.write(HEAD + '<div class="slide">' + frag + '</div>' + TAIL)
# contact sheet
thumbs="".join('<div style="width:330px;height:412px;overflow:hidden;border-radius:14px;border:1px solid #d8c4ac"><div class="slide" style="transform:scale(.30556);transform-origin:top left">%s</div></div>'%f for f in SLIDES)
board=(HEAD.replace('<body>','<body style="background:#17171c">')+
 '<div style="display:flex;flex-wrap:wrap;gap:16px;width:1410px;padding:22px">'
 '<div style="width:100%;color:#fff;font:600 30px Inter;padding:4px">Hybrid deck — texture + mascot + real product</div>'
 +thumbs+'</div>'+TAIL)
with open(os.path.join(BASE,"hyb_board.html"),"w",encoding="utf-8") as f: f.write(board)
print("wrote 8 slides + board")
