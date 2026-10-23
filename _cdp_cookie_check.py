#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""连接已达成的 CDP 调试端口，检查 weread cookie 是否可读（判断 App-Bound 是否解开）。"""
import os, json, sys

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

PORT = os.environ.get("CDP_PORT", "9222")


def main():
    ep = "http://127.0.0.1:%s" % PORT
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(ep)
        print("CONNECTED OK")
        ctx = b.contexts[0] if b.contexts else None
        if ctx is None:
            print("NO CONTEXT")
            return
        # 保险：把所有域的 cookie 都拉出来看
        try:
            cs = ctx.cookies()
        except Exception as e:
            print("COOKIES ERROR", e)
            cs = []
        print("total cookies:", len(cs))
        wr = [c for c in cs if "weread" in c.get("domain", "")]
        print("weread cookies:", len(wr))
        names = sorted({c["name"] for c in wr})
        print("names:", names)
        page = ctx.new_page()
        # 用页面内 fetch 直接验证登录态
        try:
            page.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=30000)
            res = page.evaluate("""async () => {
                const r = await fetch('/web/shelf/sync', {method:'POST', credentials:'include',
                    headers:{'content-type':'application/json'}, body: JSON.stringify({synckey:0})});
                return await r.text();
            }""")
            print("LOGIN CHECK:", res[:160])
        except Exception as e:
            print("LOGIN CHECK ERROR:", str(e)[:200])
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cookies_live.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump([{"name": c["name"], "value": c["value"], "domain": c.get("domain")} for c in wr],
                      f, ensure_ascii=False, indent=1)
        print("saved ->", out)
        b.close()


if __name__ == "__main__":
    main()
