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
            'E:/笔记Obsidian/电子书/黑马王子系列',
            # ⭐⭐ 2026-10-14 新增：第二批素材库（101 本）
            'E:/电子书/202061010投资电子书',
            'E:/电子书/202061010投资电子书/01价值投资',
            'E:/电子书/202061010投资电子书/02趋势技术',
            'E:/电子书/202061010投资电子书/03游资超短',
            'E:/电子书/202061010投资电子书/04基金、可转债',
            'E:/电子书/202061010投资电子书/05其他',
            # ⭐⭐ 2026-10-27 新增：公众号每日更新批次（82本，百度盘同步60本）
            'E:/Work Buddy/电子书/电子书资料每日更新（公众号私信 01 获取）']

DPI = 160
CHUNK = 10

kw = sys.argv[1]
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 99999

def find_pdf(k):
    """⚠️ 2026-10-14 修正：原实现对「系列多册同名」会命中错误的一册。
    事故：《像欧奈尔信徒一样交易》与《像欧奈尔信徒一样交易（二）》书名高度重叠，
    用短名搜会命中第二册（目录 10_ 排在 9_ 之前被遍历到），
    导致两次 OCR 跑的其实是同一册，第一册从未处理。
    修法：收集全部候选，按「文件名去掉括号后缀后与关键词完全相等」优先精确匹配，
    仍不唯一则报错退出，绝不静默选第一个。
    """
    hits = []
    for d in SRC_DIRS:
        for root, _, files in os.walk(d):
            for fn in files:
                if k in fn and fn.lower().endswith('.pdf'):
                    hits.append(os.path.join(root, fn))
    # ⚠️ 同一本书可能同时存在于多个源目录（路径分隔符不同但内容同一），
    # 按 realpath 去重，避免被误判为「多册歧义」。
    uniq, seen = [], set()
    for h in hits:
        rp = os.path.realpath(h).replace('\\', '/')
        if rp not in seen:
            seen.add(rp); uniq.append(h)
    hits = uniq
    if not hits:
        return None
    if len(hits) == 1:
        return hits[0]

    # 精确匹配优先：书名主体（去掉 （一）（二）等后缀）等于关键词
    def stem(fn):
        base = os.path.splitext(os.path.basename(fn))[0]
        base = re.sub(r'[（(][^）)]*[）)]\s*$', '', base)   # 去尾部括号
        base = re.sub(r'\s*\(.*?\)\s*', ' ', base)          # 去 Z-Library 的 (作者) 段
        return re.sub(r'[\s_]+', '', base)
    exact = [h for h in hits if stem(h) == re.sub(r'[\s_]+', '', k)]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        print(f'⚠️ 关键词「{k}」精确匹配到 {len(exact)} 个候选，无法判定：')
        for e in exact: print('   ', e)
        print('   请用更完整的书名（含册次）重试。'); sys.exit(1)
    print(f'⚠️ 关键词「{k}」命中 {len(hits)} 个候选，无法判定，请用更完整的书名：')
    for h in hits: print('   ', h)
    sys.exit(1)

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

# 📌 2026-10-16 修复：改为 while 显式控制。
# 事故：原 for 循环里「跳过分片」只推进了 chunk_start，而 for 的 i 仍逐页 +1，
# 两者永久失步 → 跳过后又去 OCR 已有的页，且写片条件 `done % CHUNK` 与
# chunk_start 失相位 → 分片名整体 +1 偏移（p0001-0010 后出现 p0002-0011），相邻重叠 1 页。
pg = START
while pg <= END:
    # ⭐ 断点续跑：若该分片已存在且非空，则跳过整片（避免从头重跑）
    sp = shard_path(chunk_start)
    if chunk_start == pg and os.path.exists(sp) \
       and os.path.getsize(sp) > 100:
        skipped += 1
        pg = chunk_start + CHUNK
        chunk_start = pg
        continue

    i = pg - 1
    text = ocr_page(i)
    if text is None:
        buf.append(f'=== 第{pg}页 ===\n[OCR失败]')
        failed.append(pg)
    else:
        if cc:
            text = cc.convert(text)
        buf.append(f'=== 第{pg}页 ===\n{text}')
    done += 1
    pg += 1

    if pg - chunk_start >= CHUNK or pg > END:
        os.makedirs(SHARD_DIR, exist_ok=True)   # 目录可能被外部清理，每片自愈
        with io.open(shard_path(chunk_start), 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(buf))
        el = time.time() - t0
        eta = el/done*(END-pg) if pg <= END else 0
        json.dump({'done': pg-1, 'total': END, 'elapsed': round(el),
                   'eta_sec': round(eta), 'failed': len(failed)},
                  io.open(PROGRESS, 'w'), ensure_ascii=False)
        print(f'  {pg-1}/{END}  {el:.0f}s  ETA {eta:.0f}s  失败{len(failed)}', flush=True)
        buf, chunk_start = [], pg

# 合并：走健壮合并器（按页号归并，容忍历史重叠分片）
# ⛔ 防护：校验页号无重复且覆盖完整（历史教训：bug 期重跑产生重叠分片）
try:
    import subprocess, sys as _sys
    _safe = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'merge_shards_safe.py')
    _r = subprocess.run([_sys.executable, _safe, SHARD_DIR, FULL],
                        capture_output=True, text=True, encoding='utf-8')
    print(_r.stdout, flush=True)
    if _r.returncode != 0:
        print(_r.stderr, flush=True)
        print('   → 合并失败，未写出全文。', flush=True)
        sys.exit(1)
    # 二次闸门：确认写出文件非空且页数完整
    _chk = io.open(FULL, encoding='utf-8').read()
    _pg2 = re.findall(r'^===== 第(\d+)页 =====', _chk, re.M)
    if len(_chk) < 5000 or not _pg2:
        print(f'⛔⛔ 中止：写出内容异常（{len(_chk)} 字符 / {len(_pg2)} 页），已删除。', flush=True)
        os.remove(FULL)
        sys.exit(1)
    print(f'\n✓ 完成 -> {FULL}（{len(_pg2)} 页）', flush=True)
except SystemExit:
    raise
except Exception as e:
    print(f'⛔ 合并异常：{e}', flush=True)
    sys.exit(1)

if skipped:
    print(f'⏭跳过 {skipped} 个已有分片（断点续跑）', flush=True)
print(f'耗时 {time.time()-t0:.0f}s，失败 {len(failed)} 页: {failed[:30]}', flush=True)