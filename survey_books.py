# -*- coding: utf-8 -*-
"""全量勘察：统计每本书的页数 + 文字层真伪，产出蒸馏计划表。

用法: python survey_books.py
输出: raw/books/_survey.csv  与  raw/books/_survey.md
"""
import io, os, csv, re, sys
import pymupdf

SRC = 'E:/电子书/202061010投资电子书'
OUT = 'E:/Work Buddy/交易学习/raw/books'
os.makedirs(OUT, exist_ok=True)

# 「伪文字层」判定：抽样页里正文行占比低、字数极少 → 视为扫描件需 OCR
def sample_textlayer(doc, n=8):
    pages = doc.page_count
    idx = [int(pages * (i + 0.5) / n) for i in range(n)]
    idx = [min(i, pages - 1) for i in idx]
    tot_chars, tot_lines, body_lines, noise_lines = 0, 0, 0, 0
    NOISE = re.compile(r'全国最低交易手续费|任何地方费用比|Z-Library|www\.|QQ微信|期货开户')
    for i in idx:
        try:
            t = doc[i].get_text().strip()
        except Exception:
            continue
        if not t:
            continue
        for ln in t.split('\n'):
            ln = ln.strip()
            if len(ln) < 2:
                continue
            tot_lines += 1
            tot_chars += len(ln)
            if NOISE.search(ln) or re.fullmatch(r'[\d\s.\-—第页版]+', ln):
                noise_lines += 1
            else:
                body_lines += 1
    return tot_chars, tot_lines, body_lines, noise_lines


def clean(name):
    """文件名 → 稳定 ASCII/中文混合的 slug"""
    name = re.sub(r'\s*\((?:[^()]*Z-Library[^()]*|[^()]*ePUBw[^()]*|etc\.[^()]*)\)', '', name)
    name = name.replace('(Z-Library)', '').strip()
    name = re.sub(r'\.(epub|mobi|pdf|azw3|azw)$', '', name, flags=re.I)
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = re.sub(r'\s+', ' ', name).strip(' .-')
    return name


rows = []
for dp, dn, fn in os.walk(SRC):
    for f in fn:
        ext = f.rsplit('.', 1)[-1].lower() if '.' in f else ''
        if ext not in ('pdf', 'epub', 'mobi', 'azw3', 'azw'):
            continue
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, SRC).replace('\\', '/')
        category = rel.split('/')[0] if '/' in rel else '根目录'
        # 书名优先取所在文件夹名（去掉 序号_ 前缀），更干净
        folder = os.path.basename(dp)
        bookname = clean(re.sub(r'^\d+_', '', folder)) if re.match(r'^\d+_', folder) else clean(f)
        mb = os.path.getsize(full) / 1048576

        if ext == 'pdf':
            try:
                doc = pymupdf.open(full)
                pages = doc.page_count
                ch, ln, body, noise = sample_textlayer(doc)
                ratio = (body / ln) if ln else 0
                if pages == 0:
                    kind, verdict = 'PDF空', '异常'
                elif ln == 0 or ratio < 0.3 or ch < pages * 100:
                    kind, verdict = '扫描PDF', '需OCR'
                else:
                    kind, verdict = '电子PDF', '零OCR'
                doc.close()
            except Exception as e:
                pages, ch, ln, body, noise, ratio, kind, verdict = 0, 0, 0, 0, 0, 0, 'PDF损坏', f'异常:{str(e)[:40]}'
        else:
            pages, ch, ln, body, noise, ratio = 0, 0, 0, 0, 0, 0
            kind = {'epub': 'EPUB', 'mobi': 'MOBI', 'azw3': 'AZW3', 'azw': 'AZW'}[ext]
            verdict = '零OCR'

        rows.append({
            'category': category, 'book': bookname, 'kind': kind,
            'pages': pages, 'mb': round(mb, 1), 'verdict': verdict,
            'body_ratio': round(ratio, 2), 'sample_chars': ch,
            'file': rel,
        })

rows.sort(key=lambda r: (r['category'], r['book']))
with io.open(f'{OUT}/_survey.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(f'共 {len(rows)} 本')
from collections import Counter
print(Counter(r['verdict'] for r in rows))
ocr_pages = sum(r['pages'] for r in rows if r['verdict'] == '需OCR')
print(f'需OCR总页数: {ocr_pages}  预计 {ocr_pages*7.9/60:.0f} 分钟（按缠论实测 7.9 秒/页）')