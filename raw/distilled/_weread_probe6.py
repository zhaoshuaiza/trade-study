# -*- coding: utf-8 -*-
"""下载 common.js, 直接搜 API 关键词上下文。"""
import os, re, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

def get(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", COOKIE)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def main():
    js = get("https://cdn.weread.qq.com/web/wrwebnjlogic/js/common.6f9af10c.js")
    for kw in ["chapterInfos", "book/content", "chapterContent", "bookId=", "/web/book/", "/web/reader/"]:
        idxs = [m.start() for m in re.finditer(re.escape(kw), js)]
        print("关键词 %r 出现 %d 次" % (kw, len(idxs)))
        for i in idxs[:4]:
            seg = js[max(0,i-80):i+120]
            seg = seg.replace("\n"," ")
            print("   ...", seg)
    # 找所有 /web/ 开头路径串
    paths = set(re.findall(r"/web/[a-zA-Z0-9_/?=&%.{\}\-]{3,80}", js))
    print("\n所有 /web/ 路径样本(前40):")
    for p in sorted(paths)[:40]:
        print("  ", p)

if __name__ == "__main__":
    main()
