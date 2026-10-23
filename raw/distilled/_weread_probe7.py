# -*- coding: utf-8 -*-
"""最后尝试: content/chapterInfos 走 POST + vid 等参数。"""
import os, json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

def req(url, cookie, post=None):
    data = json.dumps(post).encode() if post is not None else None
    r = urllib.request.Request(url, data=data)
    r.add_header("User-Agent", UA)
    r.add_header("Referer", "https://weread.qq.com/")
    r.add_header("Origin", "https://weread.qq.com")
    r.add_header("Cookie", cookie)
    r.add_header("Accept", "application/json, text/plain, */*")
    r.add_header("X-Requested-With", "XMLHttpRequest")
    if post is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=25) as resp:
            return resp.status, resp.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")

def main():
    bid = "3300129049"
    tests = [
        ("content POST json", "https://weread.qq.com/web/book/content", {"bookId": bid, "chapterUid": 1}),
        ("chapterInfos POST json", "https://weread.qq.com/web/book/chapterInfos", {"bookIds": [bid]}),
        ("content GET vid", "https://weread.qq.com/web/book/content?bookId=%s&chapterUid=1&vid=1609593" % bid, None),
    ]
    for name, url, post in tests:
        st, body = req(url, COOKIE, post)
        print("[%s] HTTP %s len=%d head=%s" % (name, st, len(body), body[:160].replace("\n"," ")))

if __name__ == "__main__":
    main()
