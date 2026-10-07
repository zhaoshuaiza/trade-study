# -*- coding: utf-8 -*-
"""道氏理论 PDF OCR —— 200dpi + rapidocr"""
import pymupdf, io, os, time, json, sys

PDF = 'E:/笔记Obsidian/电子书/道氏理论.pdf'
OUT = 'E:/Work Buddy/交易学习/.raw/distilled/道氏理论-OCR.txt'
PROGRESS = 'E:/Work Buddy/交易学习/.raw/distilled/_ocr_progress.json'
START, END = 1, 223   # 1-indexed

from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
d = pymupdf.open(PDF)
total = END - START + 1
print(f'共 {total} 页 ({START}~{END})，开始 OCR', flush=True)

buf = []
t0 = time.time()
for i in range(START-1, END):
    pg = i + 1
    try:
        pix = d[i].get_pixmap(dpi=200)
        tmp = f'E:/Work Buddy/交易学习/.raw/distilled/_tmp.png'
        pix.save(tmp)
        res, _ = ocr(tmp)
        lines = [r[1] for r in res] if res else []
        # 过滤页码噪声
        lines = [l for l in lines if len(l.strip()) > 1]
        buf.append(f'=== 第{pg}页 ===\n' + '\n'.join(lines))
    except Exception as e:
        buf.append(f'=== 第{pg}页 ===\n[OCR失败: {e}]')
    if pg % 5 == 0 or pg == END:
        el = time.time() - t0
        eta = el / (pg - START + 1) * (END - pg)
        json.dump({'done': pg, 'total': END, 'elapsed': round(el),
                   'eta_sec': round(eta)}, io.open(PROGRESS,'w'), ensure_ascii=False)
        print(f'  {pg}/{END}  {el:.0f}s  ETA {eta:.0f}s', flush=True)

io.open(OUT,'w',encoding='utf-8').write('\n\n'.join(buf))
print(f'\n✓ 完成，输出 {OUT}', flush=True)
print(f'总耗时 {time.time()-t0:.0f}s', flush=True)
if os.path.exists(PROGRESS): os.remove(PROGRESS)
if os.path.exists('.raw/distilled/_tmp.png'): os.remove('.raw/distilled/_tmp.png')
