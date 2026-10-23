# -*- coding: utf-8 -*-
"""在书架里按关键词找出史丁巴格两本书的真实 bookId。"""
import os, json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def get(url, cookie):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", cookie)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

KW = ["史丁巴格", "Steenbarger", "steen", "交易心理", "交易心理学", "交易心理分析",
      "心流", "教练", "101", "交易训练", "Trading Psychology", "Psychology of Trading"]

def main():
    cookie = os.environ.get("WR_COOKIE")
    raw = get("https://weread.qq.com/web/shelf/sync", cookie)
    js = json.loads(raw)
    books = js.get("books", js.get("recentBooks", []))
    print("总书数:", len(books))
    hits = []
    for b in books:
        bi = b.get("book", b)
        title = (bi.get("title") or "")
        author = (bi.get("author") or "")
        blob = title + " " + author
        if any(k.lower() in blob.lower() for k in KW):
            hits.append(bi)
            print("  >>> bookId=%s | %s | author=%s" % (bi.get("bookId"), title, author))
    if not hits:
        print("未命中关键词, 以下是标题含'交易'的:")
        for b in books:
            bi = b.get("book", b)
            t = bi.get("title") or ""
            if "交易" in t or "心理" in t:
                print("  bookId=%s | %s | %s" % (bi.get("bookId"), t, bi.get("author")))

if __name__ == "__main__":
    main()
