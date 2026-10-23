# -*- coding: utf-8 -*-
"""探针: 用 cookie 拉书架列表, 拿到真实 bookId + 标题, 并顺带核验候选 bookId。"""
import os, sys, json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def get(url, cookie):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", cookie)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

def main():
    cookie = os.environ.get("WR_COOKIE")
    # 候选 bookId 测试
    for bid in ["5ea329c0813abbcb", "5ea329c0813abbcbeg01667b", "33d32010813ab98e", "33d32010813ab98e8g019623"]:
        try:
            js = json.loads(get("https://weread.qq.com/web/book/info?bookId="+bid, cookie))
            print("bookId=%s -> %s" % (bid, js.get("errMsg")))
        except Exception as e:
            print("bookId=%s -> ERR %s" % (bid, e))
    # 拉书架
    for ep in ["https://weread.qq.com/web/shelf/finish",
               "https://weread.qq.com/web/shelf/book",
               "https://weread.qq.com/web/shelf/sync"]:
        try:
            raw = get(ep, cookie)
            js = json.loads(raw)
            print("\n=== shelf endpoint: %s ===" % ep)
            books = js.get("books", js.get("recentBooks", []))
            print("books count:", len(books))
            for b in books[:80]:
                bi = b.get("book", b)
                print("  bookId=%s | %s | author=%s" % (bi.get("bookId"), bi.get("title"), bi.get("author")))
        except Exception as e:
            print("\n=== shelf endpoint: %s -> ERR %s ===" % (ep, e))

if __name__ == "__main__":
    main()
