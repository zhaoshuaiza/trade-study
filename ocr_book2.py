# -*- coding: utf-8 -*-
"""通用扫描书 OCR —— 分批 + 断点续传 + 繁转简

用法:
  python ocr_book2.py "<pdf路径>" <起始页> <结束页> <分片目录名>
例:
  python ocr_book2.py "E:/笔记Obsidian/电子书/黑马王子系列/黑马王子操盘手记1-1.pdf" 1 239 cpb1
"""
import pymupdf, io, os, time, json, sys

PDF = sys.argv[1]
START = int(sys.argv[2])
END = int(sys.argv[3])
TAG = sys.argv[4]          # 分片目录标识（ASCII）

BASE = 'E:/Work Buddy/交易学习/raw/distilled'
SHARD_DIR = f'{BASE}/{TAG}_shards'
TMP = f'{BASE}/_tmp_{TAG}.png'
PROGRESS = f'{BASE}/_ocr_{TAG}_progress.json'
DPI = 160
CHUNK = 10

os.makedirs(SHARD_DIR, exist_ok=True)

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None

ocr = RapidOCR()
doc = pymupdf.open(PDF)
total = doc.page_count
END = min(END, total)
print(f'{os.path.basename(PDF)} 共 {total} 页，本次 {START}~{END}，DPI={DPI}', flush=True)

buf, chunk_start, done_pages = [], START, 0
t0 = time.time()
retry_log = []


def ocr_page(i, dpi):
    last = None
    for d in (dpi, 130, 100):
        for _ in range(2):
            try:
                pix = doc[i].get_pixmap(dpi=d)
                pix.save(TMP)
                res, _ = ocr(TMP)
                lines = [r[1] for r in res] if res else []
                lines = [l.strip() for l in lines if len(l.strip()) > 1]
                return '\n'.join(lines), None
            except Exception as e:
                last = f'{type(e).__name__}: {str(e)[:60]}'
                time.sleep(0.5)
    return None, last


for i in range(START - 1, END):
    pg = i + 1
    text, err = ocr_page(i, DPI)
    if text is None:
        buf.append(f'=== 第{pg}页 ===\n[OCR失败: {err}]')
        retry_log.append(pg)
    else:
        buf.append(f'=== 第{pg}页 ===\n' + (cc.convert(text) if cc else text))
    done_pages += 1

    if done_pages % CHUNK == 0 or pg == END:
        sp = f'{SHARD_DIR}/p{chunk_start:04d}-{pg:04d}.txt'
        with io.open(sp, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(buf))
        el = time.time() - t0
        eta = el / done_pages * (END - pg)
        json.dump({'done': pg, 'total': END, 'elapsed': round(el), 'eta_sec': round(eta)},
                  io.open(PROGRESS, 'w'), ensure_ascii=False)
        print(f'  {pg}/{END}  {el:.0f}s  ETA {eta:.0f}s', flush=True)
        buf, chunk_start = [], pg + 1

print(f'\n完成 {START}~{END}，耗时 {time.time()-t0:.0f}s', flush=True)
if retry_log:
    json.dump(retry_log, io.open(f'{BASE}/_ocr_{TAG}_failed.json', 'w'))
    print(f'⚠ 失败 {len(retry_log)} 页: {retry_log}', flush=True)
else:
    print('全部成功', flush=True)
