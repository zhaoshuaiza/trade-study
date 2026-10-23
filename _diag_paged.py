#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断: 1) 章节响应体格式  2) ArrowRight 是否翻页"""
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
        bodies = []

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in r.url and last.startswith("e_"):
                try:
                    bodies.append((r.url[-25:], r.body()[:120]))
                except Exception:
                    pass

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)

        print("=== 响应体样本 ===")
        for u, body in bodies[:4]:
            print(u, "|", body[:110])

        def title():
            try:
                return page.evaluate("""() => {const e=document.querySelector('.readerTopBar_title_chapter');
                                              return e?e.textContent.trim():'(空)';}""")
            except Exception:
                return "(err)"

        print("title before:", title())
        # 点击正文区获得焦点，再翻页
        page.mouse.click(700, 450)
        time.sleep(1)
        for i in range(6):
            page.keyboard.press("ArrowRight")
            time.sleep(1.2)
            print("after ArrowRight %d: title=%s" % (i, title()))
        # 也试 PageDown
        for i in range(3):
            page.keyboard.press("PageDown")
            time.sleep(1.2)
            print("after PageDown %d: title=%s" % (i, title()))
        b.close()


if __name__ == "__main__":
    main()
