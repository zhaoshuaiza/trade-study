# -*- coding: utf-8 -*-
"""对 raw/books/ 下「待OCR」的书批量 OCR，输出到各自独立目录的 book.txt

⭐ 铁律（见操盘手记页踩过的坑）：
   - 分片为空或合并后过短 → 直接退出，绝不写 book.txt
   - 每片写盘前 os.makedirs(exist_ok=True)
   - 断点续传：已存在 book.txt 则跳过

用法:
  python ocr_pending.py            # 处理全部待OCR
  python ocr_pending.py 江恩        # 只处理名字含「江恩」的书
"""
import io, os, re, sys, json, time
import pymupdf

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
SRCROOT = 'E:/电子书/202061010投资电子书'
DPI = 160
CHUNK = 10


def find_pending(filt=None):
    out = []
    for dp, dn, fn in os.walk(BOOKS):
        mp = f'{dp}/_meta.json'
        if not os.path.exists(mp):
            continue
        m = json.load(io.open(mp, encoding='utf-8'))
        if os.path.exists(f'{dp}/book.txt'):
            continue
        if m.get('extract_status') == 'fail' or m.get('verdict') == '需OCR':
            if (not filt) or (filt in m.get('book', '')):
                out.append((dp, m))
    return out


def ocr_book(d, m):
    files = m.get('files', [])
    pdf = next((f for f in files if f.lower().endswith('.pdf')), None)
    if not pdf:
        return 'skip', '无PDF源'
    full = os.path.join(SRCROOT, pdf.replace('/', os.sep))

    shard_dir = f'{d}/_shards'
    os.makedirs(shard_dir, exist_ok=True)
    tmp = f'{d}/_tmp.png'

    from rapidocr_onnxruntime import RapidOCR
    try:
        import opencc
        cc = opencc.OpenCC('t2s')
    except Exception:
        cc = None
    ocr = RapidOCR()
    doc = pymupdf.open(full)
    total = doc.page_count
    t0 = time.time()
    buf, chunk_start, n, retry = [], 1, 0, []

    def page_text(i):
        last = None
        for d_ in (DPI, 130, 100):
            for _ in range(2):
                try:
                    pix = doc[i].get_pixmap(dpi=d_)
                    pix.save(tmp)
                    res, _ = ocr(tmp)
                    lines = [r[1].strip() for r in (res or []) if r and len(r[1].strip()) > 1]
                    return '\n'.join(lines), None
                except Exception as e:
                    last = f'{type(e).__name__}'
                    time.sleep(0.4)
        return None, last

    for i in range(total):
        pg = i + 1
        sp = f'{shard_dir}/p{chunk_start:04d}-{min(pg,chunk_start+CHUNK-1):04d}.txt'
        if os.path.exists(sp):
            buf = []
            chunk_start = pg + 1
            continue
        text, err = page_text(i)
        if text is None:
            buf.append(f'=== 第{pg}页 ===\n[OCR失败:{err}]')
            retry.append(pg)
        else:
            buf.append(f'=== 第{pg}页 ===\n' + (cc.convert(text) if cc else text))
        if pg % CHUNK == 0 or pg == total:
            with io.open(sp, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(buf))
            buf = []
            chunk_start = pg + 1
        n += 1
        if n % 30 == 0:
            el = time.time() - t0
            print(f"    {m['book'][:22]}: {pg}/{total} {el:.0f}s ETA{el/n*(total-pg):.0f}s", flush=True)

    doc.close()
    if os.path.exists(tmp):
        os.remove(tmp)

    # ⭐ 合并前铁律校验
    parts = sorted(x for x in os.listdir(shard_dir) if x.endswith('.txt'))
    if not parts:
        return 'fail', '分片为空，拒绝写入'
    full_text = []
    for p in parts:
        full_text.append(io.open(f'{shard_dir}/{p}', encoding='utf-8').read())
    text = '\n\n'.join(full_text)
    cjk = len(re.findall(r'[一-鿿]', text))
    if cjk < 2000:
        return 'fail', f'合并后仅{cjk}字，拒绝写入'
    io.open(f'{d}/book.txt', 'w', encoding='utf-8').write(text)
    m.update({'chars': len(text), 'cjk': cjk, 'extract_status': 'ok',
              'ocr_pages': total, 'ocr_sec': round(time.time() - t0),
              'ocr_retry': retry})
    json.dump(m, io.open(f'{d}/_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return 'ok', f'{cjk}字 / {total}页 / {round((time.time()-t0)/60,1)}min' + (f' / 失败{len(retry)}页' if retry else '')


def main():
    os.environ.setdefault('OMP_NUM_THREADS', '1')
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    todo = find_pending(filt)
    print(f'待OCR {len(todo)} 本：')
    for d, m in todo:
        print(f'   {m["book"][:40]:42} {m.get("pages",0)}页')
    print()
    for d, m in todo:
        print(f'>> {m["book"][:40]}', flush=True)
        st, msg = ocr_book(d, m)
        print(f'   [{st}] {msg}', flush=True)


if __name__ == '__main__':
    main()