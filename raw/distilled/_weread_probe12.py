# -*- coding: utf-8 -*-
"""下载所有 weread JS bundle, 搜索 tar_CB/res.weread/签名逻辑。"""
import os, re, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COOKIE = os.environ.get("WR_COOKIE")

BUNDLES = ["common.6f9af10c.js","10.6b98eead.js","21.5e82836d.js","8.7f3c6bfa.js",
           "27.98229a34.js","11.abed1c2f.js","5.5789b064.js","33.05a9272e.js",
           "23.12c41e88.js","31.b273cb80.js","16.8214bed0.js","19.17950725.js",
           "32.9b1225a1.js","34.59529be0.js","25.1e7bbf93.js","28.f5b1a04f.js"]

def get(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Cookie", COOKIE)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def main():
    hits = {}
    for f in BUNDLES:
        url = "https://cdn.weread.qq.com/web/wrwebnjlogic/js/" + f
        try:
            js = get(url)
        except Exception as e:
            print(f, "失败", e); continue
        for kw in ["tar_CB", "res.weread", "wrco", "/wrco/", "sec=", "sec:", "signature", "sign("]:
            if kw in js:
                hits.setdefault(kw, []).append(f)
    for kw, fs in hits.items():
        print("关键词 %r 命中 bundle: %s" % (kw, fs))
    # 针对 tar_CB 出现的 bundle, 打印上下文
    if "tar_CB" in hits:
        for f in hits["tar_CB"]:
            js = get("https://cdn.weread.qq.com/web/wrwebnjlogic/js/" + f)
            for m in re.finditer("tar_CB", js):
                i = m.start()
                print("\n[%s] ...%s..." % (f, js[max(0,i-120):i+160].replace("\n"," ")))

if __name__ == "__main__":
    main()
