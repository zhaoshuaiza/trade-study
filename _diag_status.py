#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""单次导航,记录 e_ 响应的 HTTP 状态与 body 长度,判定是否限流。"""
import os, re, time
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.clearBrowserCache")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})

        seen = []
        def on_resp(resp):
            url = resp.url
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in url and "e_" in last:
                try:
                    st = resp.status
                    body = resp.body() or b""
                    seen.append((last, st, len(body)))
                    print("  [%s] status=%s body_len=%d" % (last, st, len(body)))
                except Exception as e:
                    print("  [%s] err %s" % (last, str(e)[:50]))

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(12)
        print("[summary] e_ 响应数:", len(seen))
        if not seen:
            print("  >>> 完全没有内容请求 —— 阅读器未向正文接口发请求(可能恢复上次位置且已缓存,或限流导致不发)")
        b.close()


if __name__ == "__main__":
    main()
