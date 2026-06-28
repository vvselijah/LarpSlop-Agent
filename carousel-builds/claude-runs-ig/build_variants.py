# -*- coding: utf-8 -*-
"""Composite each Higgsfield asset into a hook-slide variant (1080x1350)."""
import os
BASE = os.path.dirname(os.path.abspath(__file__))

BURST = ('<svg width="116" height="116" viewBox="0 0 100 100"><g fill="#cf5f2c">'
  + ''.join('<rect x="47.6" y="%d" width="4.8" height="%d" rx="2.4" transform="rotate(%d 50 50)"/>'
            % ((3,47,k) if k%60==0 else (9,41,k)) for k in range(0,360,30))
  + '</g></svg>')

CORE = """
*{margin:0;padding:0;box-sizing:border-box}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:'Inter',sans-serif}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.12;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:420px 420px}
.bgimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.scrim{position:absolute;inset:0}
.handle{position:absolute;top:70px;left:90px;font:600 30px 'Inter';color:var(--soft)}
.pill{position:absolute;top:64px;right:74px;background:var(--pillbg);border:1px solid var(--pillbd);
 border-radius:40px;padding:10px 26px;font:700 30px 'Inter';color:var(--ink);letter-spacing:.04em}
.kick{position:absolute;top:150px;left:96px;font:700 70px 'Caveat';color:var(--ink);
 transform:rotate(-2deg);text-shadow:1px 2px 0 rgba(0,0,0,.12)}
.big{position:absolute;top:232px;left:84px;font:400 152px/.9 'Anton';letter-spacing:1px;color:var(--ink);
 text-shadow:var(--bigshadow)}
.big .or{color:var(--accent)}
.brushwrap{position:absolute;top:540px;left:90px;transform:rotate(-1.6deg)}
.brush{display:inline-block;background:#100c08;color:#fff;font:400 88px 'Anton';letter-spacing:1px;
 padding:14px 38px 20px;
 clip-path:polygon(1% 16%,16% 5%,34% 11%,52% 3%,70% 12%,86% 4%,99% 10%,98% 78%,84% 95%,64% 86%,44% 96%,24% 85%,9% 94%,1% 82%)}
.sub{position:absolute;top:672px;left:96px;font:500 38px 'Inter';color:var(--ink)}
.sub b{font-weight:700}
.swipe{position:absolute;right:90px;bottom:44px;font:600 30px 'Inter';color:var(--soft)}
.sticker{position:absolute;top:196px;right:96px;width:166px;height:166px;background:#fbf7ef;
 border-radius:32px;transform:rotate(13deg);box-shadow:0 22px 40px rgba(0,0,0,.30);
 display:flex;align-items:center;justify-content:center}
.crown{position:absolute;top:-38px;left:-16px;font-size:58px;transform:rotate(-18deg)}
"""

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
 '<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
 '<style>%s\n%s</style></head><body>')

HEADLINE = ('<div class="kick">Claude can now run your</div>'
 '<div class="big">ENTIRE<br><span class="or">INSTAGRAM</span></div>'
 '<div class="brushwrap"><span class="brush">BETTER THAN YOU</span></div>'
 '<div class="sub">so I open-sourced the whole project. <b>free.</b> &#128274;</div>')

CHROME = ('<div class="grain"></div><div class="handle">@elijahaifl</div>'
 '<div class="pill">1/8</div>'
 '<div class="sticker"><span class="crown">&#128081;</span>%s</div>'
 '<div class="swipe">swipe &rarr;</div>') % BURST

VARIANTS = {
 # 1 — mascot on warm cream (matches asset bg so it blends)
 "v1_mascot": {
   "vars": "--ink:#241813;--soft:#7a5a48;--accent:#c2552c;--pillbg:rgba(0,0,0,.08);--pillbd:rgba(0,0,0,.22);--bigshadow:3px 4px 0 rgba(0,0,0,.10);",
   "slidebg": "background:radial-gradient(120% 100% at 25% 0%, #f6ece0 0%, #f1ddc8 60%, #ecc8a8 100%)",
   "extra": '<img src="assets/m_mascot.png" style="position:absolute;bottom:-30px;right:-40px;width:760px;filter:drop-shadow(0 30px 40px rgba(120,60,20,.28))">',
 },
 # 2 — cinematic full-bleed background, white text
 "v2_cinematic": {
   "vars": "--ink:#ffffff;--soft:rgba(255,255,255,.85);--accent:#ffae5c;--pillbg:rgba(0,0,0,.4);--pillbd:rgba(255,255,255,.35);--bigshadow:4px 5px 14px rgba(0,0,0,.55);",
   "slidebg": "background:#0a0806",
   "pre": '<img class="bgimg" src="assets/m_cinematic.png"><div class="scrim" style="background:linear-gradient(160deg, rgba(8,6,4,.82) 0%, rgba(8,6,4,.32) 46%, rgba(8,6,4,.55) 100%)"></div>',
 },
 # 3 — 3D object hero on warm peach
 "v3_object": {
   "vars": "--ink:#241813;--soft:#7a5a48;--accent:#c2552c;--pillbg:rgba(0,0,0,.08);--pillbd:rgba(0,0,0,.22);--bigshadow:3px 4px 0 rgba(0,0,0,.10);",
   "slidebg": "background:radial-gradient(120% 100% at 78% 8%, #fdeede 0%, #f7d9bf 58%, #f0c39e 100%)",
   "extra": '<img src="assets/m_object.png" style="position:absolute;bottom:-24px;left:50%;transform:translateX(-48%);width:820px;filter:drop-shadow(0 28px 40px rgba(120,60,20,.26))">',
 },
 # 4 — generated editorial texture backplate + real dashboard card
 "v4_texture": {
   "vars": "--ink:#2a1a11;--soft:#8a6147;--accent:#c2552c;--pillbg:rgba(0,0,0,.08);--pillbd:rgba(0,0,0,.22);--bigshadow:2px 3px 0 rgba(0,0,0,.08);",
   "slidebg": "background:#f1ddc8",
   "pre": '<img class="bgimg" src="assets/m_texture.png"><div class="scrim" style="background:radial-gradient(120% 90% at 50% 30%, rgba(246,236,224,.30), rgba(236,200,168,.10))"></div>',
   "extra": '<img src="_real_dashboard.png" style="position:absolute;bottom:64px;left:50%;transform:translateX(-50%) rotate(-2.5deg);width:760px;border-radius:16px;box-shadow:0 24px 46px rgba(90,50,20,.32);border:6px solid #fff">',
 },
}

for name, v in VARIANTS.items():
    body = ('<div class="slide" style="%s">%s%s%s%s</div>'
            % (v["slidebg"], v.get("pre",""), CHROME, HEADLINE, v.get("extra","")))
    html = HEAD % (CORE, ":root{%s}" % v["vars"]) + body + "</body></html>"
    with open(os.path.join(BASE, name + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", name)
print("done")
