#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试可靠的「回到扉页」: 打开目录面板(校验可见) -> 真实鼠标点第一项。"""
import os, time

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def title(pg):
    try:
        return pg.evaluate("""() => {const e=document.querySelector('.readerTopBar_title_chapter');
                                     return e?e.textContent.trim():'(none)';}""")
    except Exception:
        return "(err)"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        hits = {"n": 0}
        page.on("response", lambda r: hits.__setitem__("n", hits["n"] + 1)
                if "/web/book/chapter/" in r.url else None)

        print("title now:", title(page))
        # 打开目录
        for _ in range(3):
            try:
                page.locator("button.readerControls_item.catalog").first.click(timeout=4000)
            except Exception:
                pass
            time.sleep(1.5)
            box = None
            try:
                box = page.locator(".readerCatalog_list_item").first.bounding_box()
            except Exception:
                pass
            print("first item box:", box)
            if box and box.get("width", 0) > 0 and box.get("x", -1) >= 0:
                break
        box = page.locator(".readerCatalog_list_item").first.bounding_box()
        print("final box:", box)
        if not box:
            print("目录不可见,放弃")
            b.close()
            return
        before = hits["n"]
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        time.sleep(4)
        print("after click -> title:", title(page), "| new responses:", hits["n"] - before)
        # 再按左键确认是否已在首页
        n = 0
        for _ in range(30):
            page.keyboard.press("ArrowLeft")
            time.sleep(0.2)
            n += 1
        print("after %d ArrowLeft -> title: %s" % (n, title(page)))
        b.close()


if __name__ == "__main__":
    main()
