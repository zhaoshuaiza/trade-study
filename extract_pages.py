# -*- coding: utf-8 -*-
"""按页码从缠论 OCR 全文中抽取原文片段，用于 claims 页引用核实。"""
import io, re, sys

SRC = r'E:/Work Buddy/交易学习/raw/distilled/缠论108课详解-OCR-简体.txt'
t = io.open(SRC, encoding='utf-8').read()
lines = t.split('\n')
idx = {}
for i, l in enumerate(lines):
    m = re.match(r'=== 第(\d+)页 ===', l.strip())
    if m:
        idx[int(m.group(1))] = i

pages = [int(x) for x in sys.argv[1:]]
n = int(__import__('os').environ.get('N', '26'))
for p in pages:
    s = idx.get(p)
    print(f'##### 第{p}页')
    if s is None:
        print('[未找到该页]')
    else:
        print('\n'.join(lines[s:s + n]))
    print('=' * 72)