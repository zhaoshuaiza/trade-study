# -*- coding: utf-8 -*-
"""新增书 OCR 队列：依次处理 082-093 中无文本层的 10 本扫描版。
用法: python run_ocr_queue.py
输出日志: raw/distilled/_ocr_queue_log.txt
每本完成后追加一行 '=== DONE <书名> ==='
"""
import subprocess, sys, io, os, time

PY = sys.executable
BASE = 'E:/Work Buddy/交易学习/raw/distilled'
LOG = f'{BASE}/_ocr_queue_log.txt'
SCRIPT = 'E:/Work Buddy/交易学习/ocr_book.py'

# (关键字, 书名标签)
QUEUE = [
    ('092超级富翁', '092超级富翁的9个习惯'),
    ('090神奇的三角形操盘法', '090神奇的三角形操盘法'),
    ('089主力操盘手法揭秘', '089主力操盘手法揭秘'),
    ('088市场轮廓理论', '088市场轮廓理论'),
    ('086高胜算反弹操盘法', '086高胜算反弹操盘法'),
    ('087高胜算操盘II', '087高胜算操盘II理性交易'),
    ('093股价波动原理与箱体理论', '093股价波动原理与箱体理论'),
    ('084窥破天机', '084窥破天机：期货实战88问'),
    ('082金融交易学  第3卷', '082金融交易学第3卷'),
    ('091股市博弈论', '091股市博弈论'),
]

def log(msg):
    with io.open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

log(f'=== OCR队列启动 {time.strftime("%Y-%m-%d %H:%M:%S")} ===')

for kw, label in QUEUE:
    # 若输出已存在且够大，跳过
    out = f'{BASE}/{label}-OCR-简体.txt'
    if os.path.exists(out) and os.path.getsize(out) > 50000:
        log(f'SKIP {label}（已有输出 {os.path.getsize(out)}B）')
        continue
    log(f'START {label} @ {time.strftime("%H:%M:%S")}')
    t0 = time.time()
    try:
        r = subprocess.run([PY, SCRIPT, kw],
                           capture_output=True, text=True, encoding='utf-8', errors='replace',
                           timeout=7200)
        ok = r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 50000
        log(f'{"DONE" if ok else "FAIL"} {label} {int(time.time()-t0)}s rc={r.returncode} size={os.path.getsize(out) if os.path.exists(out) else 0}')
        if not ok:
            log((r.stdout + r.stderr)[-1500:])
    except Exception as e:
        log(f'ERROR {label}: {e}')

log(f'=== OCR队列结束 {time.strftime("%Y-%m-%d %H:%M:%S")} ===')
