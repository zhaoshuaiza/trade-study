# -*- coding: utf-8 -*-
"""通用 OCR 脚本 —— 分片 + 断点续传 + 降dpi/切半图重试。

用法:
  python ocr_book.py量柱擒涨停
  python ocr_book.py 战胜华尔街
会按关键字在 E:/笔记Obsidian/电子书/ 下递归找 PDF。
"""
import pymupdf, io, os, time, json, sys, glob, re

BASE = 'E:/Work Buddy/交易学习/raw/distilled'
SRC_DIRS = ['E:/笔记Obsidian/电子书',
            'E:/笔记Obsidian/电子书/黑马王子系列']

DPI = 160
CHUNK = 10

kw = sys.argv[1]
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 99999

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
END = min(END, TOTAL)

safe = re.sub(r'[^\w]', '_', kw)   # 纯 ASCII，避免中文路径在shell 中出问题
SHARD_DIR = f'{BASE}/shards_{safe}'
TMP = f'{BASE}/_tmp_ocr.png'
PROGRESS = f'{BASE}/_ocr_{safe}_progress.json'
FULL = f'{BASE}/{kw}-OCR-简体.txt'

print(f'《{kw}》共 {TOTAL} 页，本次 {START}~{END}', flush=True)

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None
ocr = RapidOCR()

def ocr_page(i):
    """降 dpi + 切半图，逐级尝试。返回文本或 None。"""
    for d in (DPI, 130, 100):
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
    # 切半 / 三分
    for parts in (2, 3):
        try:
            rect = doc[i].rect
            got = []
            for k in range(parts):
                clip = pymupdf.Rect(0, rect.height*k/parts, rect.width, rect.height*(k+1)/parts)
                pix = doc[i].get_pixmap(dpi=100, clip=clip)
                pix.save(TMP)
                res, _ = ocr(TMP)
                if res:
                    got += [r[1].strip() for r in res if len(r[1].strip()) > 1]
            if got:
                return '\n'.join(got)
        except Exception:
            pass
    return None

def shard_path(p):
    return f'{SHARD_DIR}/p{p:04d}-{min(p+CHUNK-1, END):04d}.txt'

buf, chunk_start, done, failed, skipped = [], START, 0, [], 0
t0 = time.time()

for i in range(START-1, END):
    pg = i + 1
    # ⭐ 断点续跑：若该分片已存在且非空，则跳过整片（避免从头重跑）
    sp = shard_path(chunk_start)
    if chunk_start == pg and os.path.exists(sp) \
       and os.path.getsize(sp) > 100:
        skipped += 1
        done += CHUNK
        buf, chunk_start = [], pg + 1
        continue

    text = ocr_page(i)
    if text is None:
        buf.append(f'=== 第{pg}页 ===\n[OCR失败]')
        failed.append(pg)
    else:
        if cc:
            text = cc.convert(text)
        buf.append(f'=== 第{pg}页 ===\n{text}')
    done += 1

    if done % CHUNK == 0 or pg == END:
        os.makedirs(SHARD_DIR, exist_ok=True)   # 目录可能被外部清理，每片自愈
        with io.open(shard_path(chunk_start), 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(buf))
        el = time.time() - t0
        eta = el/done*(END-pg)
        json.dump({'done': pg, 'total': END, 'elapsed': round(el),
                   'eta_sec': round(eta), 'failed': len(failed)},
                  io.open(PROGRESS, 'w'), ensure_ascii=False)
        print(f'  {pg}/{END}  {el:.0f}s  ETA {eta:.0f}s  失败{len(failed)}', flush=True)
        buf, chunk_start = [], pg + 1

# 合并
parts = []
for sp in sorted(glob.glob(f'{SHARD_DIR}/p*.txt')):
    parts.append(io.open(sp, encoding='utf-8').read())
merged = '\n\n'.join(parts)

# ⛔ 防护：校验页号无重复且覆盖完整（历史教训：bug 期重跑产生重叠分片）
_pg = re.findall(r'^=== 第(\d+)页 ===', merged, re.M)
if len(_pg) != len(set(_pg)):
    from collections import Counter
    dup = [p for p, c in Counter(_pg).items() if c > 1]
    print(f'\n⛔⛔ 中止：合并后有 {len(dup)} 个重复页号（分片区间重叠）', flush=True)
    print(f'   重复页号示例: {sorted(dup, key=int)[:10]}', flush=True)
    print(f'   分片目录: {SHARD_DIR}', flush=True)
    print('   → 需人工清理重叠分片后重跑，本次未写出全文。', flush=True)
    sys.exit(1)

io.open(FULL, 'w', encoding='utf-8').write(merged)
print(f'\n✓ 完成 -> {FULL}（{len(_pg)} 页）', flush=True)
if skipped:
    print(f'⏭跳过 {skipped} 个已有分片（断点续跑）', flush=True)
print(f'耗时 {time.time()-t0:.0f}s，失败 {len(failed)} 页: {failed[:30]}', flush=True)