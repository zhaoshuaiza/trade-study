# -*- coding: utf-8 -*-
import os, sys, json, time, hashlib, urllib.request, base64

COOKIE = os.environ.get("WR_COOKIE")
BOOK = "3300129049"
UID = "2"   # 版权信息 chapter
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/web/reader/%s" % BOOK)
    req.add_header("Cookie", COOKIE)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return "HTTPERR %s" % e.code

t = str(int(time.time()*1000))

formulas = {
    "A_md5(bookId+uid+t)": hashlib.md5((BOOK+UID+t).encode()).hexdigest(),
    "B_md5(uid&bookId&_=t)": hashlib.md5(("chapterUid=%s&bookId=%s&_=%s"%(UID,BOOK,t)).encode()).hexdigest(),
    "C_md5(bookId+uid)": hashlib.md5((BOOK+UID).encode()).hexdigest(),
}

for name, sign in formulas.items():
    url = "https://weread.qq.com/web/reader/chapterContent?bookId=%s&chapterUid=%s&_=%s&sign=%s" % (BOOK,UID,t,sign)
    print("=== %s ===" % name)
    d = fetch(url)
    print(d[:400])
    print()
