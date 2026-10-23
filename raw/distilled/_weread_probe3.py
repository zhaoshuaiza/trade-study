# -*- coding: utf-8 -*-
"""尝试 weread 章节/正文接口的多种候选路径与参数。"""
import os, json, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def get(url, cookie, post=False, data=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", cookie)
    req.add_header("Accept", "application/json, text/plain, */*")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")

def main():
    cookie = os.environ.get("WR_COOKIE")
    bid = "3300129049"; v = "506415078"; uid = "1"
    candidates = [
        ("chapterInfos plain", "https://weread.qq.com/web/book/chapterInfos?bookIds=%s" % bid),
        ("chapterInfos v", "https://weread.qq.com/web/book/chapterInfos?bookIds=%s&v=%s" % (bid, v)),
        ("chapterInfos array", "https://weread.qq.com/web/book/chapterInfos?bookIds=%s" % urllib.parse.quote('["%s"]' % bid)),
        ("content plain", "https://weread.qq.com/web/book/content?bookId=%s&chapterUid=%s" % (bid, uid)),
        ("content v", "https://weread.qq.com/web/book/content?bookId=%s&chapterUid=%s&v=%s" % (bid, uid, v)),
        ("reader/content", "https://weread.qq.com/web/reader/content?bookId=%s&chapterUid=%s" % (bid, uid)),
        ("book/read", "https://weread.qq.com/web/book/read?bookId=%s&chapterUid=%s" % (bid, uid)),
        ("reader page html", "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"),
    ]
    for name, url in candidates:
        st, body = get(url, cookie)
        print("[%s] HTTP %s len=%d head=%s" % (name, st, len(body), body[:120].replace("\n"," ")))

if __name__ == "__main__":
    main()
