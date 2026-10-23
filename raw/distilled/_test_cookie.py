# -*- coding: utf-8 -*-
import os, json, urllib.request, urllib.parse

COOKIE = os.environ.get("WR_COOKIE")
print("cookie loaded:", bool(COOKIE), "len:", len(COOKIE) if COOKIE else 0)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def apiget(url, cookie):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", cookie)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

# Test 1: shelf/sync (no signature needed, validates cookie)
print("\n=== TEST shelf/sync ===")
try:
    data = apiget("https://weread.qq.com/web/shelf/sync", COOKIE)
    j = json.loads(data)
    print("keys:", list(j.keys())[:10])
    if "syncKey" in j:
        print("OK shelf sync, syncKey present")
    else:
        print("resp sample:", data[:300])
except Exception as e:
    print("ERR shelf:", e)

# Test 2: chapterInfos POST (bookId 2015 = 3300129049)
print("\n=== TEST chapterInfos POST (2015) ===")
try:
    url = "https://weread.qq.com/web/book/chapterInfos"
    req = urllib.request.Request(url, data=json.dumps({"bookIds":["3300129049"]}).encode(), method="POST")
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Content-Type", "application/json")
    req.add_header("Cookie", COOKIE)
    with urllib.request.urlopen(req, timeout=25) as r:
        d = r.read().decode("utf-8","ignore")
    j = json.loads(d)
    chaps = j.get("data",[{}])[0].get("updated",[])
    print("chapters count:", len(chaps))
    for c in chaps[:5]:
        print("  uid=%s | %s | tar=%s" % (c.get("chapterUid"), c.get("title"), c.get("tar", "")[:60]))
except Exception as e:
    print("ERR chapterInfos:", e)
