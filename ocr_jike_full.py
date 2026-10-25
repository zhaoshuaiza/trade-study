# -*- coding: utf-8 -*-
"""《股市极客思考录》升级版 PDF 全本 OCR（273页扫描件）。v2：断点续传 + 逐页进度。

复用 ocr_book.py 验证过的 recipe：rapidocr + dpi链(160→130→100) + 分片写盘 + opencc繁转简。
输出：
  分片 -> E:/Work Buddy/电子书蒸馏/_tmp/jike_shards/p0001-0010.txt ...
  全文 -> raw/books/03游资超短/股市极客思考录 十年磨一剑之龙头股战法揭秘/book_full_ocr.txt
"""
import pymupdf, io, os, time, re, sys, json

PDF = 'E:/Work Buddy/电子书蒸馏/_tmp/jike.pdf'
SHARD_DIR = 'E:/Work Buddy/电子书蒸馏/_tmp/jike_shards'
TMP = 'E:/Work Buddy/电子书蒸馏/_tmp/jike_ocr_tmp.png'
PROG = 'E:/Work Buddy/电子书蒸馏/_tmp/jike_progress.json'
OUT = 'E:/Work Buddy/交易学习/raw/books/03游资超短/股市极客思考录 十年磨一剑之龙头股战法揭秘/book_full_ocr.txt'
DPI = 160
CHUNK = 10

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None
ocr = RapidOCR()

doc = pymupdf.open(PDF)
TOTAL = doc.page_count
os.makedirs(SHARD_DIR, exist_ok=True)
print(f'共 {TOTAL} 页', flush=True)

def shard_path(p):
    return f'{SHARD_DIR}/p{p:04d}-{min(p+CHUNK-1, TOTAL):04d}.txt'

# ---- 断点续传：解析已有分片，覆盖的页不再 OCR ----
covered = {}
if os.path.isdir(SHARD_DIR):
    for fn in os.listdir(SHARD_DIR):
        if not fn.endswith('.txt'):
            continue
        raw = io.open(f'{SHARD_DIR}/{fn}', encoding='utf-8').read()
        for m in re.finditer(r'=== 第(\d+)页 ===\n(.*?)(?=\n\n=== 第|\Z)', raw, re.S):
            covered[int(m.group(1))] = m.group(2).strip()
print(f'已有分片覆盖 {len(covered)} 页，续跑', flush=True)

def ocr_page(i):
    for d in (DPI, 130, 100):
        try:
            pix = doc[i].get_pixmap(dpi=d)
            pix.save(TMP)
            res, _ = ocr(TMP)
            if res:
                lines = [r[1].strip() for r in res if r and len(r[1].strip()) > 1]
                if lines:
                    return '\n'.join(lines)
        except Exception:
            pass
    return None

buf, chunk_start, done, failed = [], 1, 0, []
t0 = time.time()
for i in range(TOTAL):
    pg = i + 1
    if pg in covered:
        if covered[pg] == '[OCR失败]':
            failed.append(pg)
    else:
        text = ocr_page(i)
        if text is None:
            buf.append(f'=== 第{pg}页 ===\n[OCR失败]')
            failed.append(pg)
        else:
            if cc:
                text = cc.convert(text)
            buf.append(f'=== 第{pg}页 ===\n{text}')
    done += 1
    # 写分片：仅当 buf 里有新 OCR 的页
    if pg % CHUNK == 0 or pg == TOTAL:
        if buf:
            with io.open(shard_path(chunk_start), 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(buf))
        buf, chunk_start = [], pg + 1
    el = time.time() - t0
    json.dump({'done': done, 'total': TOTAL, 'failed': len(failed),
               'elapsed': round(el), 'eta_sec': round(el/done*(TOTAL-done))},
              io.open(PROG, 'w'), ensure_ascii=False)
    print(f'  {done}/{TOTAL}  {el:.0f}s  ETA {el/done*(TOTAL-done):.0f}s  失败{len(failed)}', flush=True)

# ---- 合并 + 页号连续性校验 ----
parts = sorted(x for x in os.listdir(SHARD_DIR) if x.endswith('.txt'))
assert parts, '分片为空'
full = '\n\n'.join(io.open(f'{SHARD_DIR}/{p}', encoding='utf-8').read() for p in parts)
pgs = [int(x) for x in re.findall(r'^=== 第(\d+)页 ===', full, re.M)]
assert pgs == list(range(1, TOTAL+1)), f'页号不连续: {len(pgs)} 个页标记'
cjk = len(re.findall(r'[一-鿿]', full))
assert cjk > 5000, f'中文字符过少: {cjk}'
io.open(OUT, 'w', encoding='utf-8').write(full)
print(f'完成: {OUT}', flush=True)
print(f'  {len(full)}字符 / {cjk}中文字 / {TOTAL}页 / {round((time.time()-t0)/60,1)}min', flush=True)
print(f'  OCR失败页: {failed}', flush=True)
if os.path.exists(TMP):
    os.remove(TMP)
