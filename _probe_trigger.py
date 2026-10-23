#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""找出真正能触发下一批章节内容加载的输入方式（以网络请求到达为准）。"""
import os, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        hits = {"n": 0}
        titles = []

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in r.url and last.startswith("e_"):
                hits["n"] += 1

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        print("[load] initial responses:", hits["n"])

        def title():
            try:
                return page.evaluate("""() => {const e=document.querySelector('.readerTopBar_title_chapter');
                                              return e?e.textContent.trim():'';}""")
            except Exception:
                return "?"

        def trial(name, fn):
            before = hits["n"]
            fn()
            time.sleep(3)
            print("[%s] new_responses=%d  title=%s" % (name, hits["n"] - before, title()))

        print("start title:", title())

        # A: 细密滚轮
        trial("wheel x10 @center", lambda: [ (page.mouse.move(700, 450), page.mouse.wheel(0, 400), time.sleep(0.25)) for _ in range(10) ])
        # B: 空格键
        trial("space x5", lambda: [ (page.keyboard.press("Space"), time.sleep(0.3)) for _ in range(5) ])
        # C: 点击正文区 + ArrowDown
        trial("click+ArrowDown x5", lambda: [ (page.mouse.click(700, 450), page.keyboard.press("ArrowDown"), time.sleep(0.3)) for _ in range(5) ])
        # D: 点击「下一章」按钮（坐标来自 readerFooter_button）
        trial("next-chapter button", lambda: page.evaluate("""() => {
            const b = Array.from(document.querySelectorAll('button.readerFooter_button'))
                           .find(x => (x.textContent||'').trim() === '下一章');
            if (b) b.click();
        }"""))
        # E: 目录第一项点击
        trial("catalog item 1", lambda: page.evaluate("""() => {
            const it = document.querySelectorAll('.readerCatalog_list_item')[1];
            if (it) it.click();
        }"""))
        b.close()


if __name__ == "__main__":
    main()
