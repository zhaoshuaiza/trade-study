# -*- coding: utf-8 -*-
import os, hashlib, urllib.request, time

COOKIE = os.environ.get("WR_COOKIE")
BOOK="3300129049"; UID="2"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(url):
    req=urllib.request.Request(url)
    req.add_header("User-Agent",UA)
    req.add_header("Referer","https://weread.qq.com/web/reader/%s"%BOOK)
    req.add_header("Cookie",COOKIE)
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return r.status, r.read().decode("utf-8","ignore")[:80]
    except urllib.error.HTTPError as e:
        try: b=e.read().decode("utf-8","ignore")[:80]
        except: b=""
        return e.code, b

t=str(int(time.time()*1000))
base="https://res.weread.qq.com/wrco/tar_CB_%s_%s"%(BOOK,UID)
print("base(no sign):", fetch(base))
print("uid1 with mysign:", fetch(base+"?sign=%s&_=%s"%(hashlib.md5((BOOK+UID+t).encode()).hexdigest(),t)))
print()
formulas={
 "book+uid+t": (BOOK+UID+t),
 "uid+book+t": (UID+BOOK+t),
 "book+uid": (BOOK+UID),
 "t+book+uid": (t+BOOK+UID),
 "book+'_'+uid+t": (BOOK+"_"+UID+t),
 "tar_CB_"+BOOK+"_"+UID+t: ("tar_CB_"+BOOK+"_"+UID+t),
 "book+uid+ 'wrco' +t": (BOOK+UID+"wrco"+t),
}
for name,s in formulas.items():
    sign=hashlib.md5(s.encode()).hexdigest()
    st,b=fetch(base+"?sign=%s&_=%s"%(sign,t))
    print("%-22s -> %s | %s"%(name,st,b))
