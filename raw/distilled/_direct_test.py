# -*- coding: utf-8 -*-
import os, base64, json, urllib.request
COOKIE=os.environ.get("WR_COOKIE")
BOOK="3300129049"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def fetch(n):
    url="https://weread.qq.com/web/book/chapter/e_%d"%n
    req=urllib.request.Request(url)
    req.add_header("User-Agent",UA)
    req.add_header("Referer","https://weread.qq.com/web/reader/%s"%BOOK)
    req.add_header("Cookie",COOKIE)
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return r.status, r.read().decode("utf-8","ignore")
    except urllib.error.HTTPError as e:
        try: b=e.read().decode("utf-8","ignore")
        except: b=""
        return e.code, b
def decode(body):
    if len(body)<=33: return None
    pre=body[:32]; sep=body[32]; b64=body[33:]
    if sep!="P": return None
    try:
        raw=base64.b64decode(b64)
        return raw.decode("utf-8","ignore")
    except Exception as e:
        return "<b64err %s>"%e
for n in [0,1,2,3,5,10,30,50,94,95,96,120,200]:
    st,body=fetch(n)
    if st==200 and body:
        x=decode(body)
        title=""
        if x and "<title>" in x:
            title=x.split("<title>")[1].split("</title>")[0]
        # grab visible text approximation: strip tags
        import re
        txt=re.sub(r"<[^>]+>"," ",x) if x else ""
        txt=re.sub(r"\s+"," ",txt).strip()
        print("e_%d OK len=%d title=%r sample=%s" % (n, len(body), title, txt[:60]))
    else:
        print("e_%d -> %s | %s" % (n, st, body[:80]))
