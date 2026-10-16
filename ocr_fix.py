# -*- coding: utf-8 -*-
"""修复 ocr_book.py 失败的页 —— 低 dpi + 切半图（2/3/4 分）逐级尝试。

用法:
  python ocr_fix.py 量柱擒涨停
会扫描 shards_<书名>/ 下所有含 [OCR失败] 的页，原地重写对应分片。
"""
import pymupdf, io, os, time, json, sys, glob, re

BASE = 'E:/Work Buddy/交易学习/raw/distilled'
# 📌 2026-10-16 补齐：与 ocr_book.py 的 SRC_DIRS 保持一致。
# 缺失这些目录会导致「未找到 PDF」而静默失败（第二批素材库都在 E:/电子书/ 下）。
SRC_DIRS = ['E:/笔记Obsidian/电子书',
            'E:/笔记Obsidian/电子书/黑马王子系列',
            'E:/电子书/202061010投资电子书',
            'E:/电子书/202061010投资电子书/01价值投资',
            'E:/电子书/202061010投资电子书/02趋势技术',
            'E:/电子书/202061010投资电子书/03游资超短',
            'E:/电子书/202061010投资电子书/04基金、可转债',
            'E:/电子书/202061010投资电子书/05其他']

def _safe_name(k):
    """⭐ 必须与 ocr_book.py 完全一致，否则找不到分片目录。
    ocr_book.py 用 re.sub(r'[^\w]','_',kw)；历史上两脚本规则不一致导致全文清零。"""
    return re.sub(r'[^\w]', '_', k)

kw = sys.argv[1]

def find_pdf(k):
    for d in SRC_DIRS:
        for root, _, files in os.walk(d):
            for fn in files:
                if k in fn and fn.lower().endswith('.pdf'):
                    return os.path.join(root, fn)
    return None

pdf = find_pdf(kw)
if not pdf:
    print(f'未找到含「{kw}」的 PDF'); sys.exit(1)

doc = pymupdf.open(pdf)
TOTAL = doc.page_count
# ⚠️ 必须与 ocr_book.py 的命名规则完全一致，否则找不到分片目录
safe = re.sub(r'[^\w]', '_', kw)
SHARD_DIR = f'{BASE}/shards_{safe}'
TMP = f'{BASE}/_tmp_fix_{safe}.png'
FULL = f'{BASE}/{kw}-OCR-简体.txt'

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None
ocr = RapidOCR()

# 1) 找出所有失败页
targets = []
for sp in sorted(glob.glob(f'{SHARD_DIR}/p*.txt')):
    txt = io.open(sp, encoding='utf-8').read()
    pages = [int(m) for m in re.findall(r'=== 第(\d+)页 ===\n\[OCR失败\]', txt)]
    for p in pages:
        targets.append((p, sp))

print(f'《{kw}》共 {TOTAL} 页，待修复 {len(targets)} 页', flush=True)

def ocr_page(i):
    # 更低 dpi 逐级
    for d in (100, 80, 65):
        try:
            pix = doc[i].get_pixmap(dpi=d)
            pix.save(TMP)
            res, _ = ocr(TMP)
            if res:
                lines = [r[1].strip() for r in res if len(r[1].strip()) > 1]
                if lines:
                    return '\n'.join(lines)
        except Exception:
            pass
    # 切半/ 三分/ 四分
    for parts in (2, 3, 4):
        try:
            rect = doc[i].rect
            got = []
            for k in range(parts):
                clip = pymupdf.Rect(0, rect.height*k/parts, rect.width, rect.height*(k+1)/parts)
                pix = doc[i].get_pixmap(dpi=90, clip=clip)
                pix.save(TMP)
                res, _ = ocr(TMP)
                if res:
                    got += [r[1].strip() for r in res if len(r[1].strip()) > 1]
            if got:
                return '\n'.join(got)
        except Exception:
            pass
    return None

by_shard = {}
for p, sp in targets:
    by_shard.setdefault(sp, []).append(p)

fixed, still = [], []
t0 = time.time()
for sp, pages in by_shard.items():
    txt = io.open(sp, encoding='utf-8').read()
    for p in pages:
        text = ocr_page(p - 1)
        if text:
            if cc:
                text = cc.convert(text)
            old = f'=== 第{p}页 ===\n[OCR失败]'
            new = f'=== 第{p}页 ===\n{text}'
            if old in txt:
                txt = txt.replace(old, new)
                fixed.append(p)
                print(f'  ✓ 第{p}页 修复 ({len(text)} 字)', flush=True)
            else:
                still.append(p)
        else:
            still.append(p)
            print(f'  ✗ 第{p}页 仍失败', flush=True)
    io.open(sp, 'w', encoding='utf-8').write(txt)

# 2) 重新合并全文
# 📌 2026-10-16：改走健壮合并器（按页号归并，容忍历史重叠分片）。
# 原实现是 50 片直接拼接，遇到历史重叠分片会写出重复页全文
#（江恩那次 17.3万 → 34.3万 字，页数翻倍）。
# ⛔ 防护：合并器自带闸门（解析为空 / 总字数<5000 / 页号缺失）→ 拒绝写出。
import subprocess, sys as _sys
_safe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'merge_shards_safe.py')
_r = subprocess.run([_sys.executable, _safe, SHARD_DIR, FULL],
                    capture_output=True, text=True, encoding='utf-8')
print(_r.stdout, flush=True)
if _r.returncode != 0:
    print(_r.stderr, flush=True)
    print('   ⛔ 合并失败，已跳过写出，原全文保持不变。', flush=True)
    sys.exit(1)

print(f'\n✓ 修复 {len(fixed)} 页，仍失败 {len(still)} 页: {still}', flush=True)
if fixed:
    print(f'  修复页: {sorted(fixed)}', flush=True)
print(f'✓ 已重新合并 -> {FULL}（走 merge_shards_safe.py 按页号归并）', flush=True)
print(f'耗时 {time.time()-t0:.0f}s', flush=True)