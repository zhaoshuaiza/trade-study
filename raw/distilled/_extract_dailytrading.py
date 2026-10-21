#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抽取《每日交易心理训练》PDF 全文到 raw/distilled/，并输出每页字数供身份验证"""
import os, sys
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import fitz

SRC = "E:/电子书/每日交易心理训练 101条规则把您训练成交易心理学家.pdf"
OUT = "E:/Work Buddy/交易学习/raw/distilled/每日交易心理训练101条规则-全文.txt"

d = fitz.open(SRC)
n = d.page_count
print(f"pages={n}")
lines = []
for i in range(n):
    t = d[i].get_text("text")
    lines.append(f"\n===== PAGE {i+1} =====\n{t}")
d.close()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(lines))
total = sum(len(l) for l in lines)
print(f"written={OUT} chars={total}")

# 打印前3页与中间页供身份验证
for p in (0, 1, 2):
    print(f"\n----- PAGE {p+1} (first 600 chars) -----")
    print(lines[p][:600])
