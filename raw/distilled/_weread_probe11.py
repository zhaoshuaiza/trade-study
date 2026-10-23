# -*- coding: utf-8 -*-
"""用 cookiejar 先访问阅读页种 res 域 cookie, 再拉 TAR。"""
import os, json, urllib.request, urllib.parse, http.cookiejar, tarfile, io, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")
BID = "3300129049"

def strip_xhtml(raw):
    raw = raw.decode("utf-8", "ignore")
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"</p>", "\n", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", "", raw)
    for a, b in [("&nbsp;"," "),("&amp;","&"),("&lt;","<"),("&gt;",">"),("&quot;",'"')]:
        raw = raw.replace(a, b)
    raw = re.sub(r"\n{2,}", "\n", raw)
    return raw.strip()

def main():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    def get(url, post=None, ref="https://weread.qq.com/"):
        data = json.dumps(post).encode() if post is not None else None
        req = urllib.request.Request(url, data=data)
        for k, v in [("User-Agent", UA), ("Referer", ref), ("Origin", "https://weread.qq.com"),
                     ("Accept", "application/json"), ("Content-Type", "application/json"),
                     ("X-Requested-With", "XMLHttpRequest")]:
            req.add_header(k, v)
        if COOKIE:
            req.add_header("Cookie", COOKIE)
        with op.open(req, timeout=30) as r:
            return r.status, r.read()
    # 1) 访问阅读页, 种 cookie
    st, _ = get("https://weread.qq.com/web/reader/33d32010813ab98e8g019623", ref="https://weread.qq.com/web/book/3300129049")
    print("reader页 HTTP", st, "已存cookie数:", len(jar))
    # 2) 拉章节清单
    st, body = get("https://weread.qq.com/web/book/chapterInfos", post={"bookIds": [BID]})
    chaps = json.loads(body)["data"][0]["updated"]
    print("章节数:", len(chaps))
    # 3) 试 TAR (uid=2 和 uid=15)
    for uid in [2, 15]:
        tar_url = "https://res.weread.qq.com/wrco/tar_CB_%s_%s" % (BID, uid)
        try:
            st2, tb = get(tar_url, ref="https://weread.qq.com/web/reader/33d32010813ab98e8g019623")
        except urllib.error.HTTPError as e:
            st2, tb = e.code, e.read()
        print("\nuid=%s tar HTTP %s size=%d" % (uid, st2, len(tb)))
        if st2 != 200:
            print("  失败:", tb[:120]); continue
        tf = tarfile.open(fileobj=io.BytesIO(tb), mode="r:*")
        for m in tf.getmembers():
            if m.name.endswith((".xhtml",".html")):
                txt = strip_xhtml(tf.extractfile(m).read())
                print("  --- %s 文本样本 ---" % m.name)
                print(txt[:400]); print("  [字数 %d]" % len(txt)); break

if __name__ == "__main__":
    main()
