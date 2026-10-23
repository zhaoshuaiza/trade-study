# -*- coding: utf-8 -*-
import os, base64, re, urllib.request, urllib.error
COOKIE=os.environ.get("WR_COOKIE")
READER_URL="https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def fetch(n):
    url="https://weread.qq.com/web/book/chapter/e_%d"%n
    req=urllib.request.Request(url)
    req.add_header("User-Agent",UA)
    req.add_header("Referer",READER_URL)
    req.add_header("Accept","application/json, text/plain, */*")
    req.add_header("Cookie",COOKIE)
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return r.status, r.read().decode("utf-8","ignore")
    except urllib.error.HTTPError as e:
        try: b=e.read().decode("utf-8","ignore")
        except: b=""
        return e.code, b
for n in [0,1,2,3]:
    st,body=fetch(n)
    print("e_%d -> %s | %s" % (n, st, body[:60]))
