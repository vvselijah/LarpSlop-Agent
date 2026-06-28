import json, re, os, sys

OUT = sys.argv[1]
VAULT = r"C:\Users\elija\OneDrive\Desktop\ai agent team\obsidian\Elijah's vault\40-Projects\LarpSlop\Color-Grading-Masterclass"
raw = open(OUT, encoding="utf-8", errors="replace").read()
obj = json.loads(raw)
res = obj["result"]
if isinstance(res, str):
    res = json.loads(res)
chs = res.get("chapters", [])

FENCE = chr(96) * 3  # ``` without putting backticks in shell


def clean(md):
    if not md:
        return ""
    md = md.strip()
    if md.startswith(FENCE):
        md = re.sub(r"^" + FENCE + r"[a-zA-Z]*\n", "", md)
        md = re.sub(r"\n" + FENCE + r"$", "", md)
    lines = md.split("\n")
    while lines and not lines[0].lstrip().startswith("#"):
        lines.pop(0)
    txt = "\n".join(lines)
    for pat in [r"\n-+\s*\n+\s*The finished chapter.*$", r"\n+The finished chapter is above.*$",
                r"\n+This chapter is grounded.*$", r"\n+I have written.*$", r"\n+\(Word count.*$",
                r"\n+The chapter is above.*$", r"\n+Note to editor.*$"]:
        txt = re.sub(pat, "\n", txt, flags=re.S | re.I)
    return txt.strip() + "\n"


n = 0
for c in chs:
    md = clean(c.get("markdown", ""))
    if not md or len(md) < 200:
        print("SKIP (short):", c.get("file"))
        continue
    fn = os.path.join(VAULT, c["file"] + ".md")
    open(fn, "w", encoding="utf-8").write(md)
    n += 1
    print("wrote", c["file"], "(%d chars)" % len(md))
print("--- wrote %d/%d chapters" % (n, len(chs)))
