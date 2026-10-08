# -*- coding: utf-8 -*-
"""重跑缠论 OCR 失败页（多为大幅K线图）。

策略:
  1. 先用低 dpi(100) 整页试一次 —— 小图内存压力小
  2. 再切成上下半张, 分别 OCR 后拼接 —— 进一步降低单次负载
失败页多为大幅K线图, 文字量极少(图注+坐标轴), 价值有限, 允许最终失败。

用法: python ocr_chan_retry.py
"""
import pymupdf, io, os, time, json, sys

PDF = 'E:/笔记Obsidian/电子书/缠论108课详解 扫地僧读缠论108课札记(高清).pdf'
BASE = 'E:/Work Buddy/交易学习/.raw/distilled'
SHARD_DIR = f'{BASE}/chan_shards'
TMP = f'{BASE}/_tmp_retry.png'
FAILED = f'{BASE}/_ocr_chan_failed.json'
OUT_FAILED = f'{BASE}/_ocr_chan_failed2.json'

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None

ocr = RapidOCR()
doc = pymupdf.open(PDF)
failed = json.load(io.open(FAILED))
print(f'待重试 {len(failed)} 页', flush=True)

fixed, still_bad = [], []
t0 = time.time()

for idx, pg in enumerate(failed):
    i = pg - 1
    lines_all, got = [], False

    # 策略 1: 低 dpi 整页
    for d in (100, 130):
        try:
            pix = doc[i].get_pixmap(dpi=d)
            pix.save(TMP)
            res, _ = ocr(TMP)
            if res:
                lines_all = [r[1].strip() for r in res if len(r[1].strip()) > 1]
                got = True
                break
        except Exception:
            pass

    # 策略 2: 切上下半张
    if not got:
        for half in (2, 3):
            try:
                rect = doc[i].rect
                parts = []
                for k in range(half):
                    clip = pymupdf.Rect(0, rect.height*k/half, rect.width, rect.height*(k+1)/half)
                    pix = doc[i].get_pixmap(dpi=100, clip=clip)
                    pix.save(TMP)
                    res, _ = ocr(TMP)
                    if res:
                        parts += [r[1].strip() for r in res if len(r[1].strip()) > 1]
                if parts:
                    lines_all = parts
                    got = True
                    break
            except Exception:
                pass

    if got:
        text = '\n'.join(lines_all)
        if cc:
            text = cc.convert(text)
        sp = f'{SHARD_DIR}/p{i+1:04d}-retry.txt'
        io.open(sp, 'w', encoding='utf-8').write(f'=== 第{pg}页 ===\n{text}\n')
        fixed.append(pg)
    else:
        still_bad.append(pg)

    if (idx+1) % 10 == 0 or idx == len(failed)-1:
        json.dump(still_bad, io.open(OUT_FAILED, 'w'))
        print(f'  {idx+1}/{len(failed)} 成功{len(fixed)} 仍失败{len(still_bad)}  {time.time()-t0:.0f}s', flush=True)

print(f'\n✓ 修复 {len(fixed)} 页，仍失败 {len(still_bad)} 页: {still_bad}', flush=True)