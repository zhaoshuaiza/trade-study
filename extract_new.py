#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新素材批量抽取（E:/电子书/202061010投资电子书）
- epub: 直接 zip 解 XHTML，秒级
- mobi/azw3: 调 calibre ebook-convert 转 epub 再抽
- pdf: 先用 pymupdf 检测文字层质量，判定是否需 OCR
输出: raw/distilled/新素材/<分类>/<书名>.txt
⭐ 本脚本只读源文件，绝不修改/移动源书。
"""
import os, re, sys, zipfile, html, subprocess, json, shutil, io

SRC = r"E:/电子书/202061010投资电子书"
OUT = r"E:/Work Buddy/交易学习/raw/distilled/新素材"
CALIBRE = r"E:/Program Files/Calibre2/ebook-convert.exe"
TMP = r"E:/Work Buddy/交易学习/raw/distilled/_newtmp"

EBOOK = {".epub", ".mobi", ".azw3", ".pdf", ".azw", ".fb2", ".lit", ".pdb"}

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t\u00a0]+")
NL_RE = re.compile(r"\n{3,}")


def clean(s: str) -> str:
    s = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h[1-6]>|</li>", "\n", s)
    s = TAG_RE.sub(" ", s)
    s = html.unescape(s)
    s = WS_RE.sub(" ", s)
    return NL_RE.sub("\n\n", s)


def text_from_epub(path: str) -> str:
    parts, hits = [], []
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith((".xhtml", ".html", ".htm"))]
        # 按 opf spine 顺序更好，但没有就按文件名
        try:
            opf = [n for n in z.namelist() if n.lower().endswith(".opf")][0]
            base = os.path.dirname(opf)
            xml = z.read(opf).decode("utf-8", "ignore")
            order = re.findall(r'href="([^"]+\.x?html?)"', xml, re.I)
            ordered = [os.path.normpath(os.path.join(base, o)) for o in order]
            names = [n for n in ordered if n in names] + [n for n in names if n not in ordered]
        except Exception:
            pass
        for n in names:
            try:
                raw = z.read(n).decode("utf-8", "ignore")
            except Exception:
                continue
            t = clean(raw)
            if len(t.strip()) > 30:
                parts.append(t)
                hits.append(n)
    return "\n".join(parts)


def to_epub(src: str) -> str:
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, os.path.splitext(os.path.basename(src))[0][:60] + ".epub")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return out
    subprocess.run([CALIBRE, src, out], timeout=600,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out if os.path.exists(out) else ""


def pdf_probe(path: str):
    """返回 (页数, 平均每页字符数, 正文占比样本) —— 判断是否需要 OCR"""
    try:
        import fitz
    except ImportError:
        return None
    try:
        d = fitz.open(path)
        n = d.page_count
        probe = list(range(0, min(n, 12), 3)) + list(range(max(0, n - 4), n))
        cn = 0
        tot = 0
        chars = []
        for i in probe:
            if i >= n:
                continue
            t = d[i].get_text()
            chars.append(len(t.strip()))
            tot += len(t.strip())
            cn += len(re.findall(r"[\u4e00-\u9fff]", t))
        d.close()
        avg = tot / max(1, len(probe))
        return {"pages": n, "avg_chars": round(avg), "cn_ratio": round(cn / max(1, tot), 2)}
    except Exception as e:
        return {"error": str(e)[:80]}


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    rows = []
    for cat in sorted(os.listdir(SRC)):
        cdir = os.path.join(SRC, cat)
        if not os.path.isdir(cdir):
            continue
        for sub in sorted(os.listdir(cdir)):
            sdir = os.path.join(cdir, sub)
            files = []
            if os.path.isdir(sdir):
                for f in sorted(os.listdir(sdir)):
                    if os.path.splitext(f)[1].lower() in EBOOK:
                        files.append(os.path.join(sdir, f))
            else:
                ext = os.path.splitext(sdir)[1].lower()
                if ext in EBOOK:
                    files = [sdir]
                    sub = cat
            for fp in files:
                ext = os.path.splitext(fp)[1].lower()
                name = re.sub(r"\s*\(Z-Library\).*$", "", os.path.basename(fp))
                name = os.path.splitext(name)[0]
                odir = os.path.join(OUT, cat)
                os.makedirs(odir, exist_ok=True)
                dest = os.path.join(odir, name + ".txt")
                rec = {"cat": cat, "sub": sub, "file": os.path.basename(fp),
                       "ext": ext, "name": name}
                if only != "all" and only not in name:
                    continue
                if os.path.exists(dest) and os.path.getsize(dest) > 20000:
                    rec.update(status="cached", chars=os.path.getsize(dest))
                    rows.append(rec); print(f"[skip] {name}"); continue
                try:
                    if ext == ".epub":
                        t = text_from_epub(fp)
                    elif ext in (".mobi", ".azw3", ".azw", ".fb2", ".lit", ".pdb"):
                        e = to_epub(fp)
                        t = text_from_epub(e) if e else ""
                    else:  # pdf：只探测不抽，OCR 走另一条线
                        p = pdf_probe(fp)
                        rec.update(status="pdf", probe=p)
                        rows.append(rec); print(f"[pdf ] {name} {p}"); continue
                    if len(t.strip()) > 500:
                        with io.open(dest, "w", encoding="utf-8") as f:
                            f.write(t)
                        rec.update(status="ok", chars=len(t))
                    else:
                        rec.update(status="empty", chars=len(t))
                except Exception as e:
                    rec.update(status="err", err=str(e)[:100])
                rows.append(rec)
                print(f"[{rec['status']:6s}] {name}  {rec.get('chars', 0)}")
    with io.open(os.path.join(OUT, "_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print("\n=== SUMMARY ===")
    from collections import Counter
    print(Counter(r["status"] for r in rows))


if __name__ == "__main__":
    main()