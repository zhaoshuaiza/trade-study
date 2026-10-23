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
print("errCode:", j.get("errCode"))
print("errMsg:", j.get("errMsg"))
info=j.get("info")
print("info type:", type(info), "len:", len(info) if hasattr(info,'__len__') else None)
if isinstance(info,list) and info:
    print("info[0] keys:", list(info[0].keys()) if isinstance(info[0],dict) else type(info[0]))
    for k,v in (info[0].items() if isinstance(info[0],dict) else []):
        if isinstance(v,list):
            print("  %s: list len %d" % (k,len(v)))
            if v and isinstance(v[0],dict): print("    item keys:", list(v[0].keys()))
        else:
            print("  %s: %s" % (k, str(v)[:80]))
elif isinstance(info,dict):
    print("info keys:", list(info.keys()))
