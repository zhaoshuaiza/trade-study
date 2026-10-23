# -*- coding: utf-8 -*-
"""测试: 拉取章节 tar 包, 解析 XHTML 文本。"""
import os, json, urllib.request, tarfile, io, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

def req(url, cookie, post=None):
    data = json.dumps(post).encode() if post is not None else None
    r = urllib.request.Request(url, data=data)
    for k, v in [("User-Agent", UA), ("Referer", "https://weread.qq.com/"),
                 ("Origin", "https://weread.qq.com"), ("Cookie", cookie),
                 ("Accept", "application/json"), ("Content-Type", "application/json"),
                 ("X-Requested-With", "XMLHttpRequest")]:
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()

def strip_xhtml(raw):
    raw = raw.decode("utf-8", "ignore")
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"</p>", "\n", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = re.sub(r"&nbsp;", " ", raw)
    raw = re.sub(r"&amp;", "&", raw)
    raw = re.sub(r"&lt;", "<", raw)
    raw = re.sub(r"&gt;", ">", raw)
    raw = re.sub(r"&quot;", '"', raw)
    raw = re.sub(r"\n{2,}", "\n", raw)
    return raw.strip()

def main():
    bid = "3300129049"
    st, body = req("https://weread.qq.com/web/book/chapterInfos", COOKIE, {"bookIds": [bid]})
    chaps = json.loads(body)["data"][0]["updated"]
    # 选 uid=2(常规章) 与 uid=15(可能付费)
    for uid in [2, 15]:
        tar_url = "https://res.weread.qq.com/wrco/tar_CB_%s_%s" % (bid, uid)
        st2, tar_bytes = req(tar_url, COOKIE)
        print("\n=== uid=%s tar HTTP %s size=%d ===" % (uid, st2, len(tar_bytes)))
        if st2 != 200:
            print("  !! 拉取失败:", tar_bytes[:120])
            continue
        try:
            tf = tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:*")
            members = tf.getmembers()
            print("  tar成员:", [m.name for m in members][:6])
            for m in members:
                if m.name.endswith(".xhtml") or m.name.endswith(".html"):
                    x = tf.extractfile(m).read()
                    txt = strip_xhtml(x)
                    print("  --- %s 文本样本(前500) ---" % m.name)
                    print(txt[:500])
                    print("  [字数约 %d]" % len(txt))
                    break
        except Exception as e:
            print("  tar解析失败:", e)

if __name__ == "__main__":
    main()
