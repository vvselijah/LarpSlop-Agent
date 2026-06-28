import re, os, glob

VAULT = r"C:\Users\elija\OneDrive\Desktop\ai agent team\obsidian\Elijah's vault\40-Projects\LarpSlop\Color-Grading-Masterclass"
SCREENS = os.path.join(VAULT, "screens")
have = set(os.path.basename(p) for p in glob.glob(os.path.join(SCREENS, "*.jpg")))
total = 0
broken = []
for md in glob.glob(os.path.join(VAULT, "*.md")):
    txt = open(md, encoding="utf-8").read()
    for m in re.findall(r"!\[\[screens/([^\]]+)\]\]", txt):
        total += 1
        if m not in have:
            broken.append((os.path.basename(md), m))
print("total embeds:", total, "| screenshots available:", len(have))
print("broken embeds:", len(broken))
for f, m in broken:
    print("  ", f, "->", m)
