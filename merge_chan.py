# -*- coding: utf-8 -*-
"""合并缠论 OCR 分片为完整文本，并做基础清洗。

用法: python merge_chan.py
输出: .raw/distilled/缠论108课详解-OCR-简体.txt
"""
import io, os, glob, re, json

BASE = 'E:/Work Buddy/交易学习/.raw/distilled'
SHARD_DIR = f'{BASE}/chan_shards'
OUT = f'{BASE}/缠论108课详解-OCR-简体.txt'
PROGRESS = f'{BASE}/_ocr_chan_progress.json'

# 1. 收集主分片
shards = sorted(glob.glob(f'{SHARD_DIR}/p*.txt'))
shards = [s for s in shards if 'retry' not in os.path.basename(s)]
print(f'主分片 {len(shards)} 个')

# 2. retry 文件覆盖对应页（失败页的重跑版本）
retries = glob.glob(f'{SHARD_DIR}/p*-retry.txt')
print(f'重跑分片 {len(retries)} 个')

def page_no(path):
    m = re.search(r'p(\d+)-', os.path.basename(path))
    return int(m.group(1)) if m else 0

page_text = {}
for sp in shards:
    for blk in io.open(sp, encoding='utf-8').read().split('=== 第'):
        if not blk.strip():
            continue
        num = int(re.match(r'(\d+)页', blk).group(1))
        page_text[num] = blk

covered = 0
for rp in retries:
    for blk in io.open(rp, encoding='utf-8').read().split('=== 第'):
        if not blk.strip():
            continue
        num = int(re.match(r'(\d+)页', blk).group(1))
        if '[OCR失败' in blk:
            continue
        page_text[num] = blk
        covered += 1

print(f'重跑覆盖 {covered} 页')

# 3. 统计失败
failed = sorted(n for n, t in page_text.items() if '[OCR失败' in t)
total = io.open(f'{SHARD_DIR}/../道氏理论-OCR-简体.txt', encoding='utf-8').read(0) if False else ''

# 4. 按页码排序输出
parts = []
for n in sorted(page_text):
    parts.append(f'=== 第{n}页 ===\n' + page_text[n])

full = '\n\n'.join(parts)
io.open(OUT, 'w', encoding='utf-8').write(full)

print(f'\n合并完成 -> {OUT}')
print(f'页数: {len(page_text)}')
print(f'总字数: {len(full)}')
if failed:
    print(f'⚠ 仍失败 {len(failed)} 页: {failed}')
    json.dump(failed, io.open(f'{BASE}/_ocr_chan_failed.json', 'w'))
else:
    print('✓ 全部页成功')
    for f in (f'{BASE}/_ocr_chan_failed.json', f'{BASE}/_ocr_chan_failed2.json'):
        if os.path.exists(f):
            os.remove(f)
if os.path.exists(PROGRESS):
    os.remove(PROGRESS)