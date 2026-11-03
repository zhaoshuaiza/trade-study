# -*- coding: utf-8 -*-
"""第二批OCR队列·第2轮 - cangjie深度蒸馏候选。"""
import subprocess, sys, time, os

PY = 'E:/Python310/python.exe'
SCRIPT = 'E:/Work Buddy/交易学习/ocr_book.py'
DISTILLED = 'E:/Work Buddy/交易学习/raw/distilled'

# 按优先级：cangjie深度蒸馏候选
QUEUE = [
    '通向财务自由之路',           # 030 范撒普仓位管理经典
    '简简单单做股票',             # 022 楚云风交易系统构建
    '著名游资悟道心得',            # 017 游资心法
    '退学炒股',                   # 036 淘股吧超短打板
]

todo = []
for kw in QUEUE:
    # 检查是否已有OCR全文
    found = False
    for f in os.listdir(DISTILLED):
        if kw in f and f.endswith('-OCR-简体.txt') and os.path.getsize(os.path.join(DISTILLED, f)) > 5000:
            print(f'⏭ 已有全文，跳过: {kw} ({f})')
            found = True
            break
    if not found:
        todo.append(kw)

if not todo:
    print('队列空，全部已完成')
    sys.exit(0)

print(f'第2轮OCR队列: {len(todo)} 本')
for i, kw in enumerate(todo, 1):
    print(f'\n{"="*60}')
    print(f'[{i}/{len(todo)}] 开始OCR: {kw}')
    print(f'{"="*60}')
    t0 = time.time()
    r = subprocess.run([PY, SCRIPT, kw], cwd='E:/Work Buddy/交易学习')
    el = time.time() - t0
    status = '✅' if r.returncode == 0 else f'❌(exit={r.returncode})'
    print(f'{status} {kw} 耗时{el/60:.0f}分钟')

print('\n第2轮OCR队列完毕')
