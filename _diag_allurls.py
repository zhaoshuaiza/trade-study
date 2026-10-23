#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""捕获全部 weread 响应 URL(无过滤),看阅读器现在到底请求什么。"""
import os, re, time
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

BOOK = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


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

        urls = []
        def on_resp(resp):
            u = resp.url
            if "weread.qq.com" in u:
                urls.append(u)

        page.on("response", on_resp)
        # 触发: 按 ArrowLeft 几次 + 等
        for i in range(4):
            try: page.keyboard.press("ArrowLeft")
            except Exception: pass
            time.sleep(2.0)
        time.sleep(4)
        # 去重并打印
        uniq = sorted(set(urls))
        print("[总 weread 响应数]", len(urls), "唯一", len(uniq))
        for u in uniq:
            print("  ", u.replace("https://weread.qq.com", ""))
        b.close()


if __name__ == "__main__":
    main()
