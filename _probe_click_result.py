#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""点目录项后：检查标题是否真的跳转 + 统计所有相关网络请求。"""
import os, time

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.new_page()
        reqs = []
        resps = []

        def on_req(r):
            if "/web/book/chapter/" in r.url or "chapter" in r.url:
                reqs.append(r.url)
        def on_resp(r):
            if "/web/book/chapter/" in r.url:
                resps.append((r.url, r.status))

        page.on("request", on_req)
        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        print("[load] requests=%d responses=%d" % (len(reqs), len(resps)))

        def title():
            try:
                return page.evaluate("""() => {const e=document.querySelector('.readerTopBar_title_chapter');
                                              return e?e.textContent.trim():'';}""")
            except Exception:
                return "?"

        # 打开目录
        try:
            page.locator("button.readerControls_item.catalog").first.click(timeout=6000)
            time.sleep(2)
        except Exception as e:
            print("catalog open fail", str(e)[:80])

        for idx in [10, 20, 30]:
            before = len(resps)
            print("[before %d] title=%s" % (idx, title()))
            ok = False
            try:
                page.locator(".readerCatalog_list_item").nth(idx).click(timeout=6000)
                ok = True
            except Exception as e:
                print("  click fail:", str(e)[:70])
            time.sleep(4)
            print("[after %d] clicked=%s title=%s new_resp=%d" % (idx, ok, title(), len(resps) - before))

        print("total responses:", len(resps))
        for u, s in resps[:10]:
            print("   ", s, u[-40:])
        b.close()


if __name__ == "__main__":
    main()
