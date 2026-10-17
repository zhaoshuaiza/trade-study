# -*- coding: utf-8 -*-
"""书籍正文提取器 —— 每本书独立目录，输出到 raw/books/<分类>/<书名>/book.txt

支持 epub / mobi / azw3 / azw / pdf(电子版)
用法:
  python extract_books.py 0            # 处理全部未提取的书
  python extract_books.py epubscan      # 只做零OCR 书
  python extract_books.py pdfscan       # 只做 PDF（电子版直抽，扫描版自动转 OCR）
"""
import io, os, re, sys, zipfile, json, subprocess, time

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
SRCROOT = 'E:/电子书/202061010投资电子书'

# 广告/授权噪声行
NOISE = re.compile(
    r'全国最低交易手续费|任何地方费用比|Z-Library|www\.|QQ微信|期货开户|'
    r'本书仅供|版权所有|违者必究|www\.[a-z]|ISBN|扫描版|扫码|'
    r'^={0,3}\s*第\s*\d+\s*页\s*={0,3}\s*$|^\s*\d{1,4}\s*$')


def strip_noise(text):
    out = []
    for ln in text.split('\n'):
        ln = ln.rstrip()
        if not ln.strip():
            out.append('')
            continue
        if NOISE.search(ln):
            continue
        out.append(ln.strip())
    # 压缩连续空行
    res, blank = [], 0
    for ln in out:
        if ln == '':
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        res.append(ln)
    return '\n'.join(res)


# ---------- EPUB ----------
def extract_epub(path):
    """epub = zip，按 spine 顺序抽 xhtml/html"""
    import html as htmllib
    try:
        zf = zipfile.ZipFile(path)
    except Exception as e:
        return None, f'zip打开失败:{e}'
    names = zf.namelist()
    # 找 spine 顺序
    order = []
    try:
        import xml.etree.ElementTree as ET
        for n in names:
            if n.lower().endswith('container.xml'):
                root = ET.fromstring(zf.read(n))
                for e in root.iter():
                    if e.tag.endswith('rootfile'):
                        opf = e.get('full-path')
                        if opf and opf in names:
                            oroot = ET.fromstring(zf.read(opf))
                            man = None
                            for x in oroot.iter():
                                if x.tag.endswith('item') and 'spine' in str(x.attrib):
                                    man = x.get('idref')
                            if man:
                                for x in oroot.iter():
                                    if x.tag.endswith('itemref') and x.get('idref') == man:
                                        rp = x.get('idref')
                                idmap = {}
                                for x in oroot.iter():
                                    if x.tag.endswith('item'):
                                        idmap[x.get('id')] = x.get('href')
                                for x in oroot.iter():
                                    if x.tag.endswith('itemref'):
                                        href = idmap.get(x.get('idref'))
                                        if href:
                                            full = os.path.normpath(
                                                os.path.join(os.path.dirname(opf), href)).replace('\\', '/')
                                            if full in names:
                                                order.append(full)
    except Exception:
        pass
    if not order:
        order = [n for n in names if n.lower().endswith(('.html', '.xhtml', '.htm'))
                 and 'toc' not in n.lower()]
    parts = []
    for n in order:
        try:
            raw = zf.read(n).decode('utf-8', 'ignore')
        except Exception:
            continue
        raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
        raw = re.sub(r'(?i)<br[^>]*>|</p>|</div>|</h\d>|</li>|</tr>', '\n', raw)
        raw = re.sub(r'<[^>]+>', '', raw)
        raw = htmllib.unescape(raw)
        parts.append(raw)
    return strip_noise('\n'.join(parts)), None


# ---------- MOBI / AZW ----------
def extract_mobi(path):
    """mobi/azw3 优先用 mobi/calibre 转 epub；无则用 kindleunpack 思路直抽"""
    # 1) 尝试 calibre ebook-convert（若已装）
    for exe in ('ebook-convert', 'ebook-convert.exe'):
        try:
            out = path.rsplit('.', 1)[0] + '.__tmp.epub'
            r = subprocess.run([exe, path, out], capture_output=True, timeout=300)
            if r.returncode == 0 and os.path.exists(out):
                txt, err = extract_epub(out)
                os.remove(out)
                return txt, err
        except (FileNotFoundError, subprocess.TimeoutExpired):
            break
    # 2) 退路：MOBI 是 PalmDB，文本存在 MOBI/EXTH 之后的未压缩段
    try:
        data = io.open(path, 'rb').read()
    except Exception as e:
        return None, f'读取失败:{e}'
    out = []
    # PalmDOC 压缩：1 = 无压缩
    idx = 0
    cnt = 0
    while True:
        i = data.find(b'\x00\x00\x00\x00', idx)
        j = data.find(b'x\x00\x00', idx)
        break
    # 用宽松策略：抽取长段可打印 ASCII + UTF-8，中文书籍多为此类
    for enc in ('utf-8', 'gbk', 'big5'):
        try:
            t = data.decode(enc, 'ignore')
        except Exception:
            continue
        cjk = len(re.findall(r'[\u4e00-\u9fff]', t))
        if cjk > 2000:
            return strip_noise(t), None
    return None, 'MOBI解码失败：建议装 calibre 后重试（ebook-convert <in> <out>.epub）'


# ---------- PDF（电子版） ----------
def extract_pdf_text(path):
    import pymupdf
    doc = pymupdf.open(path)
    parts = []
    for i in range(doc.page_count):
        t = doc[i].get_text()
        if t.strip():
            parts.append(f'\n=== 第{i+1}页 ===\n' + t)
    doc.close()
    return strip_noise('\n'.join(parts))


def body_ratio_of(text):
    lines = [l for l in text.split('\n') if l.strip()]
    if not lines:
        return 0.0
    body = sum(1 for l in lines if not re.fullmatch(r'[\d\s.\-—第页版=]+', l))
    return body / len(lines)


def process_dir(d, force=False):
    meta_p = f'{d}/_meta.json'
    out_p = f'{d}/book.txt'
    if os.path.exists(out_p) and not force:
        n = os.path.getsize(out_p)
        return 'skip', f'已存在({n//1024}KB)'

    meta = json.load(io.open(meta_p, encoding='utf-8'))
    files = meta.get('files', [])
    order_pref = ['.epub', '.azw3', '.azw', '.mobi', '.pdf']
    picked = None
    for ext in order_pref:
        for f in files:
            if f.lower().endswith(ext):
                picked = f
                break
        if picked:
            break
    if not picked:
        return 'fail', '无可用源文件'

    full = os.path.join(SRCROOT, picked.replace('/', os.sep))
    if not os.path.exists(full):
        return 'fail', f'源文件不存在:{picked}'

    ext = picked.rsplit('.', 1)[-1].lower()
    t0 = time.time()
    if ext == 'epub':
        text, err = extract_epub(full)
    elif ext in ('mobi', 'azw', 'azw3'):
        text, err = extract_mobi(full)
    else:
        try:
            text = extract_pdf_text(full)
            err = None
        except Exception as e:
            text, err = None, f'PDF抽取失败:{str(e)[:60]}'

    if not text:
        meta['extract_status'] = 'fail'
        meta['extract_error'] = err
        json.dump(meta, io.open(meta_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return 'fail', err or '空'

    ratio = body_ratio_of(text)
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
    meta.update({
        'picked_file': picked, 'chars': len(text), 'cjk': cjk,
        'body_ratio': round(ratio, 2),
        'extract_status': 'ok' if (cjk > 2000 and ratio > 0.5) else 'suspicious',
        'extract_sec': round(time.time() - t0, 1),
    })
    # ⭐ 铁律：非空校验通过才写盘
    if cjk > 500:
        io.open(out_p, 'w', encoding='utf-8').write(text)
    json.dump(meta, io.open(meta_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return meta['extract_status'], f'{cjk}字 {len(text)//1024}KB {ratio:.0%} {meta["extract_sec"]}s'


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    dirs = []
    for cat in sorted(os.listdir(BOOKS)):
        cp = os.path.join(BOOKS, cat)
        if not os.path.isdir(cp):
            continue
        for b in sorted(os.listdir(cp)):
            bd = os.path.join(cp, b)
            if os.path.exists(f'{bd}/_meta.json'):
                dirs.append(bd)

    stat = {}
    for d in dirs:
        st, msg = process_dir(d)
        stat[st] = stat.get(st, 0) + 1
        if st != 'skip':
            print(f'[{st:10}] {os.path.basename(d)[:40]:42} {msg}', flush=True)
    print('\n统计:', stat, f'（共{len(dirs)}本）')


if __name__ == '__main__':
    main()