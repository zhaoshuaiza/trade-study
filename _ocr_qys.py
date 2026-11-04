# -*- coding: utf-8 -*-
"""《股市晴雨表》专用 OCR 驱动 —— 复用 ocr_book.py 的逻辑，指定精确路径。

与 ocr_book.py 的差异：
  - 直接传绝对路径，不靠关键词在固定目录搜索（本书在 E:/电子书/ 根目录，
    不在 ocr_book.py 的 SRC_DIRS 内）。
  - 输出约定与库一致：raw/distilled/股市晴雨表-OCR-简体.txt
  - 分片目录：raw/distilled/shards_qys
其余（DPI 降级、切半图重试、繁转简、断点续传、merge_shards_safe 合并）保持一致。
"""
import pymupdf, io, os, time, json, sys, re
import subprocess as _sp

PDF = r"E:/电子书/04.华章经典·金融投资系列-股市晴雨表(高清).pdf"
BASE = r"E:/Work Buddy/交易学习/raw/distilled"
SHARD_DIR = f"{BASE}/shards_qys"
TMP = f"{BASE}/_tmp_ocr_qys.png"
PROGRESS = f"{BASE}/_ocr_qys_progress.json"
FULL = f"{BASE}/股市晴雨表-OCR-简体.txt"
DPI = 160
CHUNK = 10

START = int(sys.argv[1]) if len(sys.argv) > 1 else 1
END = int(sys.argv[2]) if len(sys.argv) > 2 else 99999

os.makedirs(BASE, exist_ok=True)
doc = pymupdf.open(PDF)
TOTAL = doc.page_count
END = min(END, TOTAL)

from rapidocr_onnxruntime import RapidOCR
try:
    import opencc
    cc = opencc.OpenCC('t2s')
except Exception:
    cc = None
ocr = RapidOCR()
print(f"《股市晴雨表》共 {TOTAL} 页，本次 {START}~{END}", flush=True)


def ocr_page(i):
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
    return f"{SHARD_DIR}/p{p:04d}-{min(p+CHUNK-1, END):04d}.txt"


buf, chunk_start, done, failed, skipped = [], START, 0, [], 0
t0 = time.time()
pg = START
while pg <= END:
    sp = shard_path(chunk_start)
    if chunk_start == pg and os.path.exists(sp) and os.path.getsize(sp) > 100:
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
        os.makedirs(SHARD_DIR, exist_ok=True)
        with io.open(shard_path(chunk_start), 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(buf))
        el = time.time() - t0
        eta = el/done*(END-pg) if pg <= END else 0
        json.dump({'done': pg-1, 'total': END, 'elapsed': round(el),
                   'eta_sec': round(eta), 'failed': len(failed)},
                  io.open(PROGRESS, 'w'), ensure_ascii=False)
        print(f'  {pg-1}/{END}  {el:.0f}s  ETA {eta:.0f}s  失败{len(failed)}', flush=True)
        buf, chunk_start = [], pg

try:
    _r = _sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 'merge_shards_safe.py'), SHARD_DIR, FULL],
                 capture_output=True, text=True, encoding='utf-8')
    print(_r.stdout, flush=True)
    if _r.returncode != 0:
        print(_r.stderr, flush=True)
        print('   -> 合并失败，未写出全文。', flush=True)
        sys.exit(1)
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
