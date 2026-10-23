#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""探测阅读器的滚动容器与翻页机制。"""
import os, time

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def snap(page, tag):
    info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => e.scrollHeight > e.clientHeight + 50 &&
            ['auto','scroll'].includes(getComputedStyle(e).overflowY));
        return {
            scrollY: window.scrollY,
            docH: document.documentElement.scrollHeight,
            innerH: window.innerHeight,
            containers: els.slice(0,6).map(e => ({tag: e.tagName, cls: (e.className||'').toString().slice(0,60),
                                                 top: Math.round(e.scrollTop), sh: e.scrollHeight, ch: e.clientHeight})),
            title: (document.querySelector('.readerTopBar_title_chapter')||{}).textContent
        };
    }""")
    print("[%s] scrollY=%s docH=%s | %s" % (tag, info["scrollY"], info["docH"], info["title"]))
    for c in info["containers"]:
        print("      container", c)
    return info


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        snap(page, "init")

        # 方式1: window.scrollTo
        page.evaluate("() => window.scrollTo(0, 3000)")
        time.sleep(2)
        snap(page, "scrollTo")

        # 方式2: 先移动鼠标到正文区再滚轮
        page.mouse.move(700, 500)
        page.mouse.wheel(0, 4000)
        time.sleep(2)
        snap(page, "wheel-after-move")

        # 方式3: 键盘 PageDown / 空格
        page.keyboard.press("PageDown")
        time.sleep(1.5)
        snap(page, "pagedown")

        # 方式4: 容器 scrollTop
        page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('*')).filter(e => e.scrollHeight > e.clientHeight + 50 &&
                ['auto','scroll'].includes(getComputedStyle(e).overflowY));
            if (els[0]) els[0].scrollTop = 4000;
        }""")
        time.sleep(2)
        snap(page, "container-top")
        b.close()


if __name__ == "__main__":
    main()
