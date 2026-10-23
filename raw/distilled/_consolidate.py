# -*- coding: utf-8 -*-
"""
Consolidate captured WeRead chapters (steenbarger-2015-zh / steenbarger-2002-zh)
into a single clean UTF-8 text file per book, in reading order (e_0, e_1, ...),
with chapter titles as headings. Also drops front/back matter that is purely
boilerplate (copyright page etc. kept but marked).
"""
import os, sys, json, re

SRC = sys.argv[1] if len(sys.argv) > 1 else "steenbarger-2015-zh"
OUT = sys.argv[2] if len(sys.argv) > 2 else (SRC + "_FULL.txt")

meta_path = os.path.join(SRC, "_meta.json")
if not os.path.exists(meta_path):
    print("NO _meta.json in", SRC)
    sys.exit(1)

meta = json.load(open(meta_path, encoding="utf-8"))
# sort by n
meta.sort(key=lambda m: m["n"])

lines = []
total = 0
for m in meta:
    n = m["n"]
    tfn = os.path.join(SRC, "%04d.txt" % n)
    if not os.path.exists(tfn):
        continue
    txt = open(tfn, encoding="utf-8").read()
    title = m.get("title", "") or ""
    # Heading
    if title:
        lines.append("\n\n# %s\n" % title)
    else:
        lines.append("\n\n# [章节 %d]\n" % n)
    lines.append(txt)
    total += len(txt)

full = "".join(lines)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(full)

print("book:", SRC)
print("chapters:", len(meta))
print("total chars:", total)
print("written ->", OUT)
# show title list
for m in meta:
    print("  e_%d  %s  (%d chars)" % (m["n"], m.get("title", "") or "[无标题]", m["chars"]))
