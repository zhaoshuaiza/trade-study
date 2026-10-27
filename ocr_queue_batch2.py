# -*- coding: utf-8 -*-
"""第二批书OCR队列 - 按优先级依次跑。
每本完成后自动开始下一本。断点续跑（已有分片会跳过）。
"""
import subprocess, sys, time, os

PY = 'E:/Python310/python.exe'
SCRIPT = 'E:/Work Buddy/交易学习/ocr_book.py'

# 按优先级排序（交易方法论核心优先）
QUEUE = [
    '止损 如何克服贪婪和恐惧',      # 018 止损纪律核心
    '亚当理论',                    # 051 技术分析经典
    'MACD指标精讲',                # 063 实用指标
    '股市波浪派手册',              # 043 波浪理论补充
    '股市稳赚',                    # 已零OCR跳过，占位
]

# 过滤掉已存在全文的
DISTILLED = 'E:/Work Buddy/交易学习/raw/distilled'
todo = []
for kw in QUEUE:
    # 检查是否已有OCR全文
    full = os.path.join(DISTILLED, f'{kw}-OCR-简体.txt')
    if os.path.exists(full) and os.path.getsize(full) > 5000:
        print(f'⏭ 已有全文，跳过: {kw}')
        continue
    todo.append(kw)

if not todo:
    print('队列空，全部已完成')
    sys.exit(0)

print(f'OCR队列: {len(todo)} 本')
for i, kw in enumerate(todo, 1):
    print(f'\n{"="*60}')
    print(f'[{i}/{len(todo)}] 开始OCR: {kw}')
    print(f'{"="*60}')
    t0 = time.time()
    r = subprocess.run([PY, SCRIPT, kw], cwd='E:/Work Buddy/交易学习')
    el = time.time() - t0
    status = '✅' if r.returncode == 0 else f'❌(exit={r.returncode})'
    print(f'{status} {kw} 耗时{el/60:.0f}分钟')

print('\n全部队列处理完毕')
