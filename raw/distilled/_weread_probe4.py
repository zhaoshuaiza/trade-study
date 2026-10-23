# -*- coding: utf-8 -*-
"""从阅读页 HTML 里挖真实 API 路径 / 令牌。"""
import os, re, urllib.request

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
    html = get("https://weread.qq.com/web/reader/33d32010813ab98e8g019623", cookie)
    print("HTML len:", len(html))
    # 找 JS 里出现的接口路径
    paths = set(re.findall(r"/web/[a-zA-Z0-9_/]+\?|[a-zA-Z0-9_/]*chapterInfos[a-zA-Z0-9_/]*|[a-zA-Z0-9_/]*book/content[a-zA-Z0-9_/]*", html))
    print("命中路径:", list(paths)[:40])
    # 找可能的安全令牌
    for kw in ["sec=", "secretId", "secretKey", "secTraceId", "vid", "appId", "nonce"]:
        m = re.findall(kw + r"[\"']?\s*[:=]\s*[\"']?([0-9a-zA-Z_.\-]{4,40})", html)
        if m:
            print(kw, "->", list(set(m))[:8])
    # 找所有带 weread.qq.com 的 url
    urls = set(re.findall(r"https?://[a-zA-Z0-9_.\-]+weread\.qq\.com/[a-zA-Z0-9_./?=&%\-]+", html))
    print("weread urls:", list(urls)[:30])

if __name__ == "__main__":
    main()
