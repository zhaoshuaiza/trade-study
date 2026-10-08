# -*- coding: utf-8 -*-
"""缠论108课 OCR —— 分批 + 断点续传 + 繁转简

用法:
  python ocr_chan.py 1 20      # 跑第 1~20 页
  python ocr_chan.py 1 593     # 全量
分片输出到 .raw/distilled/chan_shards/, 每 10 页一个文件, 可断点续跑。
"""
import pymupdf, io, os, time, json, sys

PDF = 'E:/笔记Obsidian/电子书/缠论108课详解 扫地僧读缠论108课札记(高清).pdf'
BASE = 'E:/Work Buddy/交易学习/.raw/distilled'
SHARD_DIR = f'{BASE}/chan_shards'
TMP = f'{BASE}/_tmp_chan.png'
PROGRESS = f'{BASE}/_ocr_chan_progress.json'
DPI = 160
CHUNK = 10   # 每片页数

START = int(sys.argv[1]) if len(sys.argv) > 1 else 1
END = int(sys.argv[2]) if len(sys.argv) > 2 else 593

os.makedirs(SHARD_DIR, exist_ok=True)

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None

ocr = RapidOCR()
doc = pymupdf.open(PDF)
total_pages = doc.page_count
END = min(END, total_pages)
print(f'PDF 共 {total_pages} 页，本次处理 {START}~{END}，DPI={DPI}', flush=True)

def shard_path(p):
    return f'{SHARD_DIR}/p{p:04d}-{min(p+CHUNK-1, END):04d}.txt'

done_pages = 0
t0 = time.time()
buf, chunk_start = [], START
retry_log = []

def ocr_page(doc, i, dpi):
    """OCR 单页，失败自动降 dpi 重试。返回文本。"""
    last = None
    for d in (dpi, 130, 100):
        for attempt in range(2):
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

for i in range(START-1, END):
    pg = i + 1
    text, err = ocr_page(doc, i, DPI)
    if text is None:
        buf.append(f'=== 第{pg}页 ===\n[OCR失败 dpi降级后仍失败: {err}]')
        retry_log.append(pg)
    else:
        if cc:
            text = cc.convert(text)
        buf.append(f'=== 第{pg}页 ===\n{text}')
    done_pages += 1

    # 每满一页就检查是否该落盘
    if done_pages % CHUNK == 0 or pg == END:
        sp = shard_path(chunk_start)
        with io.open(sp, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(buf))
        el = time.time() - t0
        eta = el / done_pages * (END - pg)
        json.dump({'done': pg, 'total': END, 'elapsed': round(el),
                   'eta_sec': round(eta), 'dpi': DPI},
                  io.open(PROGRESS, 'w'), ensure_ascii=False)
        print(f'  {pg}/{END}  {el:.0f}s  ETA {eta:.0f}s  -> {os.path.basename(sp)}', flush=True)
        buf, chunk_start = [], pg + 1

print(f'\n完成 {START}~{END}，耗时 {time.time()-t0:.0f}s', flush=True)
if retry_log:
    rf = f'{BASE}/_ocr_chan_failed.json'
    json.dump(retry_log, io.open(rf, 'w'))
    print(f'⚠ {len(retry_log)} 页失败: {retry_log}', flush=True)
else:
    print('全部成功', flush=True)