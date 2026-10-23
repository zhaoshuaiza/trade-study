#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从微信读书的资源包(tar)直接下载有 tar 链接的章节,补齐翻页漏抓的部分。

用法: python _tar_fetch.py --book 2015
"""
import os, re, io, json, time, hashlib, tarfile, argparse

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS = {
    "2015": {"bookId": "3300129049", "out": os.path.join(ROOT, "raw/distilled/steenbarger-2015-zh")},
    "2002": {"bookId": "3300220786", "out": os.path.join(ROOT, "raw/distilled/steenbarger-2002-zh")},
}


def xhtml_to_text(x):
    x2 = re.sub(r"<style[\s\S]*?</style>", "", x)
    x2 = re.sub(r"<script[\s\S]*?</script>", "", x2)
    blocks = re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2)
    paras = []
    for b in blocks:
        t = re.sub(r"<[^>]+>", "", b).replace("&nbsp;", " ")
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    return "\n\n".join(paras)


def existing_hashes(out_dir):
    hs = set()
    for f in os.listdir(out_dir) if os.path.isdir(out_dir) else []:
        if re.match(r"\d+\.txt$", f):
            try:
                hs.add(hashlib.md5(
                    open(os.path.join(out_dir, f), "rb").read().decode("utf-8", "ignore")
                    .encode("utf-8")).hexdigest())
            except Exception:
                pass
    return hs


def next_index(out_dir):
    n = 0
    for f in os.listdir(out_dir) if os.path.isdir(out_dir) else []:
        m = re.match(r"(\d+)\.txt$", f)
        if m:
            n = max(n, int(m.group(1)) + 1)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    args = ap.parse_args()
    cfg = BOOKS[args.book]
    out_dir = cfg["out"]
    os.makedirs(out_dir, exist_ok=True)
    hashes = existing_hashes(out_dir)

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        pg = ctx.pages[0]
        # 章节列表
        r = pg.evaluate("""async (bid) => {
            const rr = await fetch('/web/book/chapterInfos',{method:'POST',credentials:'include',
                headers:{'content-type':'application/json'},body:JSON.stringify({bookIds:[bid]})});
            return await rr.text();
        }""", cfg["bookId"])
        updated = json.loads(r)["data"][0]["updated"]
        with_tar = [u for u in updated if u.get("tar")]
        print("[toc] 总章节 %d, 有 tar 的 %d 章" % (len(updated), len(with_tar)))
        saved = 0
        for u in with_tar:
            title = u["title"]
            try:
                resp = ctx.request.get(u["tar"], timeout=40000)
                body = resp.body()
            except Exception as e:
                print("  [err] uid=%s %s download fail: %s" % (u["chapterUid"], title, str(e)[:60]))
                continue
            if resp.status != 200 or len(body) < 200:
                print("  [skip] uid=%-3d %-30s status=%s len=%d"
                      % (u["chapterUid"], title, resp.status, len(body)))
                continue
            # 解析 tar
            texts = []
            try:
                tf = tarfile.open(fileobj=io.BytesIO(body), mode="r:")
                for m in tf.getmembers():
                    if not m.name.lower().endswith((".xhtml", ".html", ".htm")):
                        continue
                    f = tf.extractfile(m)
                    if not f:
                        continue
                    raw = f.read().decode("utf-8", "ignore")
                    t = xhtml_to_text(raw)
                    if len(t) >= 20:
                        texts.append((m.name, raw, t))
            except Exception as e:
                print("  [tar err] uid=%s %s : %s" % (u["chapterUid"], title, str(e)[:70]))
                continue
            for name, raw, t in texts:
                h = hashlib.md5(t.encode("utf-8")).hexdigest()
                if h in hashes:
                    print("  [dup]  uid=%-3d %-30s %s" % (u["chapterUid"], title, name))
                    continue
                hashes.add(h)
                idx = next_index(out_dir)
                with open(os.path.join(out_dir, "%04d.html" % idx), "w", encoding="utf-8", newline="") as fh:
                    fh.write(raw); fh.flush(); os.fsync(fh.fileno())
                with open(os.path.join(out_dir, "%04d.txt" % idx), "w", encoding="utf-8", newline="") as fh:
                    fh.write(t); fh.flush(); os.fsync(fh.fileno())
                # 回读校验
                rb = open(os.path.join(out_dir, "%04d.txt" % idx), "rb").read().decode("utf-8", "ignore")
                ok = hashlib.md5(rb.encode("utf-8")).hexdigest() == h
                print("  [已落盘] %04d %-28s %6d字 %s" % (idx, title[:26], len(t), "✓校验通过" if ok else "✗校验失败"))
                saved += 1
            time.sleep(0.4)
        print("[done] tar 补充落盘 %d 段, 磁盘共 %d 文件" % (saved, next_index(out_dir)))
        b.close()


if __name__ == "__main__":
    main()
