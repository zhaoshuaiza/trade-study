# -*- coding: utf-8 -*-
"""修参数: chapterInfos 用 JSON 数组; 并验证付费章节能否拉到内容。"""
import os, json, urllib.request, urllib.parse, base64

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def get(url, cookie):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")

def main():
    cookie = os.environ.get("WR_COOKIE")
    bid = "3300129049"
    for fmt in ["3300129049", '["3300129049"]', "3300129049,3300220786", '["3300129049","3300220786"]']:
        url = "https://weread.qq.com/web/book/chapterInfos?bookIds=" + urllib.parse.quote(fmt)
        st, body = get(url, cookie)
        print("fmt=%r -> HTTP %s, len=%d, head=%s" % (fmt, st, len(body), body[:160].replace("\n"," ")))
    # 试拉第一章内容(验证付费权限)
    st, body = get("https://weread.qq.com/web/book/content?bookId=%s&chapterUid=1" % bid, cookie)
    print("\ncontent ch1 HTTP", st, "len", len(body))
    try:
        js = json.loads(body)
        data = js.get("data", {})
        c = data.get("content", "")
        print("content字段长度:", len(c))
        if c:
            raw = base64.b64decode(c).decode("utf-8", "ignore")
            print("base64解码样本:", raw[:400])
    except Exception as e:
        print("content解析失败:", e, body[:200])

if __name__ == "__main__":
    main()
