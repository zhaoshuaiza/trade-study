# -*- coding: utf-8 -*-
import os, json, time, hashlib, urllib.request

COOKIE = os.environ.get("WR_COOKIE")
BOOK = "3300129049"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/web/reader/%s" % BOOK)
    req.add_header("Cookie", COOKIE)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8","ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8","ignore")

t = str(int(time.time()*1000))
for uid in ["1","2","5"]:
    base = "https://res.weread.qq.com/wrco/tar_CB_%s_%s" % (BOOK, uid)
    # formula A
    signA = hashlib.md5((BOOK+uid+t).encode()).hexdigest()
    for tag, url in [
        ("no_sign", base),
        ("A_md5(b+u+t)", base+"?sign=%s&_=%s"%(signA,t)),
    ]:
        st, body = fetch(url)
        print("uid=%s %s -> %s | head=%s" % (uid, tag, st, body[:120].replace("\n"," ")))
