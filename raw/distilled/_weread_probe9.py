# -*- coding: utf-8 -*-
"""打印 chapterInfos 真实结构。"""
import os, json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

def req(url, cookie, post):
    data = json.dumps(post).encode()
    r = urllib.request.Request(url, data=data)
    for k, v in [("User-Agent", UA), ("Referer", "https://weread.qq.com/"),
                 ("Origin", "https://weread.qq.com"), ("Cookie", cookie),
                 ("Accept", "application/json"), ("Content-Type", "application/json"),
                 ("X-Requested-With", "XMLHttpRequest")]:
        r.add_header(k, v)
    with urllib.request.urlopen(r, timeout=25) as resp:
        return resp.read().decode("utf-8", "ignore")

def main():
    body = req("https://weread.qq.com/web/book/chapterInfos", COOKIE, {"bookIds": ["3300129049"]})
    js = json.loads(body)
    print("top keys:", list(js.keys()))
    d0 = js.get("data", [{}])
    if isinstance(d0, list):
        d0 = d0[0] if d0 else {}
    print("data[0] keys:", list(d0.keys()))
    for k in d0.keys():
        v = d0[k]
        if isinstance(v, list):
            print("  %s: list len=%d sample=%s" % (k, len(v), json.dumps(v[:2], ensure_ascii=False)[:300]))
        else:
            print("  %s: %s" % (k, json.dumps(v, ensure_ascii=False)[:200]))

if __name__ == "__main__":
    main()
