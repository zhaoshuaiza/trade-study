# -*- coding: utf-8 -*-
import os, json, urllib.request
COOKIE=os.environ.get("WR_COOKIE")
def post(book):
    url="https://weread.qq.com/web/book/chapterInfos"
    req=urllib.request.Request(url, data=json.dumps({"bookIds":[book]}).encode(), method="POST")
    req.add_header("User-Agent","Mozilla/5.0")
    req.add_header("Referer","https://weread.qq.com/")
    req.add_header("Content-Type","application/json")
    req.add_header("Cookie",COOKIE)
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read().decode("utf-8","ignore"))
for book,label in [("3300129049","2015"),("3300220786","2002")]:
    j=post(book)
    chaps=j.get("data",[{}])[0].get("updated",[])
    print("=== BOOK %s : %d chapters ===" % (label, len(chaps)))
    out=[]
    for c in chaps:
        out.append((c.get("chapterIdx"), c.get("chapterUid"), c.get("title")))
    for idx,uid,title in out:
        print("  idx=%s uid=%s | %s" % (idx, uid, title))
    with open("_chaps_%s.json"%label,"w",encoding="utf-8") as f:
        json.dump([{"idx":i,"uid":u,"title":t} for i,u,t in out], f, ensure_ascii=False, indent=1)
