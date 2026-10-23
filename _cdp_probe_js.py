# -*- coding: utf-8 -*-
"""扒阅读器前端 JS 里的全部 API 路径，寻找 chapter 正文的替代端点。"""
import os, re, time, json
os.environ["NO_PROXY"] = "127.0.0.1,localhost"; os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

JS = """async () => {
  const html = document.documentElement.outerHTML;
  const srcs = [...document.querySelectorAll('script[src]')].map(s => s.src);
  return [html.length, srcs];
}"""

FETCH_JS = """async (url) => {
  const r = await fetch(url);
  return await r.text();
}"""

def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]; page = ctx.pages[0]; page.bring_to_front()
        try: page.goto("https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
                       wait_until="domcontentloaded", timeout=60000)
        except Exception as e: print("nav", str(e)[:60])
        time.sleep(6)
        ln, srcs = page.evaluate(JS)
        print("html len", ln)
        for s in srcs[:20]:
            print("  script:", s)
        # 找主 bundle
        cand = [s for s in srcs if "/js/app" in s or "wrwebnjlogic" in s]
        if not cand:
            cand = srcs[-3:]
        js_url = cand[0]
        print("== fetch bundle:", js_url)
        txt = page.evaluate(FETCH_JS, js_url)
        print("bundle size:", len(txt))
        with open("_app_bundle.js", "w", encoding="utf-8") as f:
            f.write(txt)
        # 提取所有 /web/ 路径
        paths = sorted(set(re.findall(r'["\'`](/web/[a-zA-Z0-9_\-/\$\{\}\.]+)["\'`]', txt)))
        print("== /web/ 路径 %d 个 ==" % len(paths))
        for x in paths:
            print("  ", x)
        # 提取 res.weread 相关
        res = sorted(set(re.findall(r'["\'`]([a-z0-9\.\-]*weread[^"\'`]{0,60})["\'`]', txt)))
        print("== weread 资源模板 %d 个 ==" % len(res))
        for x in res[:40]:
            print("  ", x)

main()
