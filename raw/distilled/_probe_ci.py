# -*- coding: utf-8 -*-
import os, json, urllib.request
COOKIE=os.environ.get("WR_COOKIE")
url="https://weread.qq.com/web/book/chapterInfos"
req=urllib.request.Request(url, data=json.dumps({"bookIds":["3300129049"]}).encode(), method="POST")
req.add_header("User-Agent","Mozilla/5.0")
req.add_header("Referer","https://weread.qq.com/")
req.add_header("Content-Type","application/json")
req.add_header("Cookie",COOKIE)
with urllib.request.urlopen(req,timeout=25) as r:
    raw=r.read().decode("utf-8","ignore")
j=json.loads(raw)
print("top keys:", list(j.keys()))
d=j.get("data")
print("data type:", type(d), "len:", len(d) if isinstance(d,list) else None)
if isinstance(d,list) and d:
    print("data[0] keys:", list(d[0].keys()))
    for k,v in d[0].items():
        if isinstance(v,list):
            print("  %s: list len %d" % (k, len(v)))
            if v: print("    first item keys:", list(v[0].keys()) if isinstance(v[0],dict) else type(v[0]))
        else:
            print("  %s: %s" % (k, str(v)[:80]))
