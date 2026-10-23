# -*- coding: utf-8 -*-
"""POST chapterInfos 拿到章节; 再试 content 的多种 POST 路径。"""
import os, json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

def req(url, cookie, post=None):
    data = json.dumps(post).encode() if post is not None else None
    r = urllib.request.Request(url, data=data)
    r.add_header("User-Agent", UA)
    r.add_header("Referer", "https://weread.qq.com/")
    r.add_header("Origin", "https://weread.qq.com")
    r.add_header("Cookie", cookie)
    r.add_header("Accept", "application/json, text/plain, */*")
    r.add_header("X-Requested-With", "XMLHttpRequest")
    if post is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=25) as resp:
            return resp.status, resp.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")

def main():
    bid = "3300129049"; v = 506415078
    st, body = req("https://weread.qq.com/web/book/chapterInfos", COOKIE, {"bookIds": [bid]})
    js = json.loads(body)
    chaps = js["data"][0]["chapters"]
    print("章节数:", len(chaps))
    for c in chaps[:8]:
        print("  uid=%s idx=%s | %s" % (c.get("chapterUid"), c.get("chapterIdx"), c.get("title")))
    uid = chaps[0]["chapterUid"]
    print("首章 uid=", uid)
    # 试 content 多种 POST 路径
    bodies = [
        {"bookId": bid, "chapterUid": uid},
        {"bookId": bid, "chapterUid": uid, "v": v},
    ]
    paths = [
        "https://weread.qq.com/web/book/content",
        "https://weread.qq.com/web/book/chapterContent",
        "https://weread.qq.com/web/reader/content",
        "https://weread.qq.com/web/book/content?bookId=%s&chapterUid=%s" % (bid, uid),
    ]
    for p in paths:
        for b in bodies:
            st2, body2 = req(p, COOKIE, b if "?" not in p else None)
            ok = "OK" if st2 == 200 else "404"
            print("[%s] %s body=%s -> HTTP %s len=%d" % (ok, p[-30:], list(b.keys()), st2, len(body2)))

if __name__ == "__main__":
    main()
