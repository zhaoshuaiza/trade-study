#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PDF 有文字层的直接抽取"""
import os, re, io, glob
import fitz

SRC = r"E:/电子书/202061010投资电子书"
OUT = r"E:/Work Buddy/交易学习/raw/distilled/新素材"

targets = ["大钱细思", "巴菲特致股东的信", "周期 (霍华德", "林园炒股秘籍",
           "价值投资之茅台大博弈", "新威科夫操盘法", "一本书搞懂龙头股战法"]

found = []
for root, dirs, files in os.walk(SRC):
    for f in files:
        if not f.lower().endswith(".pdf"):
            continue
        # ⭐ 精确匹配：书名去掉 Z-Library 尾巴后必须以某个 target 开头
        base = re.sub(r"\s*\(Z-Library\).*$", "", os.path.splitext(f)[0])
        for t in targets:
            if base.startswith(t):
                found.append((os.path.join(root, f), t))
                break

for fp, key in found:
    cat = fp.replace(SRC + "\\", "").split("\\")[0]
    # ⭐ 必须从 fp 取文件名，不能用循环残留变量 f
    name = os.path.splitext(os.path.basename(fp))[0]
    name = re.sub(r"\s*\(Z-Library\).*$", "", name)
    odir = os.path.join(OUT, cat)
    os.makedirs(odir, exist_ok=True)
    dest = os.path.join(odir, name + ".txt")
    if os.path.exists(dest) and os.path.getsize(dest) > 50000:
        print("[skip]", name); continue
    d = fitz.open(fp)
    parts = []
    for i in range(d.page_count):
        parts.append(d[i].get_text())
    d.close()
    t = "\n".join(parts)
    io.open(dest, "w", encoding="utf-8").write(t)
    print(f"[ok  ] {name[:50]}  {len(t)}")