# -*- coding: utf-8 -*-
"""提取有文字层 PDF 的全文，自动清理页眉页脚噪声。

用法: python extract_text.py
输出: .raw/distilled/<书名>-全文.txt
"""
import pymupdf, io, os, re, sys

BASE = 'E:/Work Buddy/交易学习/.raw/distilled'
os.makedirs(BASE, exist_ok=True)

BOOKS = [
    # (文件名关键字, 输出名, 噪声过滤)  —— 用关键字匹配，避免路径空格差异
    ('量柱擒涨停', '量柱擒涨停', True),
    ('量线捉涨停', '量线捉涨停', True),
    ('你不可不知的人性', '你不可不知的人性', False),
    ('数据分析实战', '数据分析实战', False),
    ('新手学炒股', '新手学炒股一本就够', False),
]

SRC_DIRS = [
    'E:/笔记Obsidian/电子书',
    'E:/笔记Obsidian/电子书/黑马王子系列',
]

# 广告/盗版站点噪声特征
NOISE = re.compile(r'(7help\.net|958218088|期货开户|书籍下载|www\.gucuan\.com|股窜网|'
                   r'零佣金|手续费免费办理|正规商品股指原油期货开户)')

def find_pdf(kw):
    """在源目录中递归查找文件名含关键字的 PDF"""
    for d in SRC_DIRS:
        for root, _, files in os.walk(d):
            for fn in files:
                if kw in fn and fn.lower().endswith('.pdf'):
                    return os.path.join(root, fn)
    return None

def clean(text, do_filter):
    lines = text.split('\n')
    out = []
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if do_filter and NOISE.search(s):
            continue
        out.append(s)
    return '\n'.join(out)

total_pages = 0
total_words = 0

for kw, name, do_filter in BOOKS:
    path = find_pdf(kw)
    if not path:
        print(f'跳过（未找到）: {name}')
        continue
    doc = pymupdf.open(path)
    buf = []
    for i in range(doc.page_count):
        try:
            t = doc[i].get_text()
        except Exception:
            t = ''
        t = clean(t, do_filter)
        buf.append(f'=== 第{i+1}页 ===\n{t}')
    full = '\n\n'.join(buf)
    out = f'{BASE}/{name}-全文.txt'
    io.open(out, 'w', encoding='utf-8').write(full)
    n = len(full)
    total_pages += doc.page_count
    total_words += n
    print(f'{name}: {doc.page_count}页 / {n} 字 -> {os.path.basename(out)}')
    doc.close()

print(f'\n合计 {total_pages} 页 / {total_words} 字')