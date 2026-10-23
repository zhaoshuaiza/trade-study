# -*- coding: utf-8 -*-
"""下载 weread JS bundle, 提取真实 API 路径。"""
import os, re, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

def get(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", COOKIE)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

def main():
    # 常见 bundle
    for f in ["common.6f9af10c.js", "10.6b98eead.js", "21.5e82836d.js", "8.7f3c6bfa.js"]:
        url = "https://cdn.weread.qq.com/web/wrwebnjlogic/js/" + f
        try:
            js = get(url)
        except Exception as e:
            print(f, "下载失败", e); continue
        print("=== %s (len=%d) ===" % (f, len(js)))
        # 找 /web/book/ 或 /web/reader/ 后接的内容
        hits = set(re.findall(r"/web/(?:book|reader)/[a-zA-Z0-9_/?=&%.\-]+(?:chapterInfos|content|chapterContent|chapterList|infos)[a-zA-Z0-9_/?=&%.\-]*", js))
        for h in sorted(hits)[:30]:
            print("  PATH:", h)
        # 也找带 bookId 的模板串
        tmpl = set(re.findall(r"[\"'`]/web/(?:book|reader)/[a-zA-Z0-9_\-]+(?:\?|/)[^\"'`]{0,80}", js))
        for t in sorted(tmpl)[:30]:
            if "bookId" in t or "chapter" in t or "content" in t:
                print("  TMPL:", t)

if __name__ == "__main__":
    main()
