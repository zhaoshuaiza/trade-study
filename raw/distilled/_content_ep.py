# -*- coding: utf-8 -*-
import os, json, urllib.request
COOKIE=os.environ.get("WR_COOKIE")
BOOK="3300129049"; UID="2"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def call(method,url,data=None):
    req=urllib.request.Request(url,data=data,method=method)
    req.add_header("User-Agent",UA); req.add_header("Referer","https://weread.qq.com/web/reader/%s"%BOOK); req.add_header("Cookie",COOKIE)
    if data: req.add_header("Content-Type","application/json")
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return r.status, r.read().decode("utf-8","ignore")[:200]
    except urllib.error.HTTPError as e:
        try: b=e.read().decode("utf-8","ignore")[:200]
        except: b=""
        return e.code, b
# 1 GET /web/book/content
print("GET /web/book/content:", call("GET","https://weread.qq.com/web/book/content?bookId=%s&chapterUid=%s"%(BOOK,UID)))
# 2 POST /web/book/content
print("POST /web/book/content:", call("POST","https://weread.qq.com/web/book/content", json.dumps({"bookId":BOOK,"chapterUid":int(UID)}).encode()))
# 3 GET /web/reader/chapterContent
print("GET /web/reader/chapterContent:", call("GET","https://weread.qq.com/web/reader/chapterContent?bookId=%s&chapterUid=%s"%(BOOK,UID)))
# 4 POST /web/book/chapterInfos already works; try the actual content via 'book/content' with chapterUid string
print("GET /web/book/content str uid:", call("GET","https://weread.qq.com/web/book/content?bookId=%s&chapterUid=%s&pos=0"%(BOOK,UID)))
