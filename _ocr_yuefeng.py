# -*- coding: utf-8 -*-
"""月风《股市投机战法》上·下册 全书 OCR 驱动。

复用 _ocr_qys.py 已验证的链路（PyMuPDF 渲染 -> RapidOCR -> 分片 -> merge_shards_safe 按页归并）。
两册使用独立的临时图 / 分片目录 / 进度文件，可并行跑、可断点续跑。

用法:
  /e/Python310/python.exe _ocr_yuefeng.py 上 [START] [END]
  /e/Python310/python.exe _ocr_yuefeng.py 下 [START] [END]

⚠️ 环境：自带 python 3.13 无 pymupdf/rapidocr，必须用 /e/Python310/python.exe。
⚠️ opencc 在本机 3.10 缺失；原书为简体扫描件，脚本自动降级为不转换。
"""
import pymupdf, io, os, time, json, sys, re
import subprocess as _sp

BASE = r"E:/Work Buddy/交易学习/raw/distilled"
CONF = {
    '上': dict(
        PDF=r"E:/电子书/月风先生/股市投机战法上.pdf",
        FULL=f"{BASE}/股市投机战法上-OCR-简体.txt",
        SHARD=f"{BASE}/shards_yf_up",
        TAG='yf_up'),
    '下': dict(
        PDF=r"E:/电子书/月风先生/股市投机战法下.pdf",
        FULL=f"{BASE}/股市投机战法下-OCR-简体.txt",
        SHARD=f"{BASE}/shards_yf_down",
        TAG='yf_down'),
}

if len(sys.argv) < 2 or sys.argv[1] not in CONF:
    print(__doc__)
    sys.exit(2)
key = sys.argv[1]
c = CONF[key]
PDF, FULL, SHARD_DIR, TAG = c['PDF'], c['FULL'], c['SHARD'], c['TAG']
TMP = f"{BASE}/_tmp_ocr_{TAG}.png"
PROGRESS = f"{BASE}/_ocr_{TAG}_progress.json"
DPI = 160
CHUNK = 10

START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 99999

os.makedirs(SHARD_DIR, exist_ok=True)
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
print(f"《股市投机战法{key}》共 {TOTAL} 页，本次 {START}~{END}，繁转简={'开' if cc else '关(本机无opencc，原书为简体)'}", flush=True)


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
                clip = pymupdf.Rect(0, rect.height * k / parts, rect.width, rect.height * (k + 1) / parts)
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
    return f"{SHARD_DIR}/p{p:04d}-{min(p + CHUNK - 1, END):04d}.txt"


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
    text = ocr_page(pg - 1)
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
        with io.open(shard_path(chunk_start), 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(buf))
        el = time.time() - t0
        eta = el / done * (END - pg) if pg <= END else 0
        json.dump({'book': key, 'done': pg - 1, 'total': END, 'elapsed': round(el),
                   'eta_sec': round(eta), 'failed': len(failed)},
                  io.open(PROGRESS, 'w'), ensure_ascii=False)
        print(f'  [{key}] {pg-1}/{END}  {el:.0f}s  ETA {eta:.0f}s  失败{len(failed)}', flush=True)
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
    print(f'\n✓ 完成 -> {FULL}（{len(_pg2)} 页 / {len(_chk)} 字符）', flush=True)
except SystemExit:
    raise
except Exception as e:
    print(f'⛔ 合并异常：{e}', flush=True)
    sys.exit(1)

if skipped:
    print(f'⏭跳过 {skipped} 个已有分片（断点续跑）', flush=True)
print(f'耗时 {time.time()-t0:.0f}s，失败 {len(failed)} 页: {failed[:30]}', flush=True)
if os.path.exists(TMP):
    os.remove(TMP)
