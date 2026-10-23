#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在全新页面中探测目录结构与跳转能力。"""
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
        cnt = {"n": 0}

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in r.url and last.startswith("e_"):
                cnt["n"] += 1

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)
        print("[load] responses:", cnt["n"])

        info = page.evaluate("""() => {
            const items = Array.from(document.querySelectorAll('.readerCatalog_list_item'));
            const sample = items.slice(0, 6).map((it, i) => {
                const t = it.querySelector('[class*=title_text], [class*=title]');
                return {i, cls: it.className.toString().slice(0,90),
                        title: t ? t.textContent.trim().slice(0,30) : '',
                        locked: it.className.includes('lock') || it.className.includes('Lock') ||
                                it.className.includes('disable') || it.className.includes('Disable')};
            });
            return {total: items.length, sample: JSON.stringify(sample)};
        }""")
        print("catalog items:", info["total"])
        print(info["sample"])

        # 用真实鼠标点击第 3 个目录项
        try:
            box = page.locator(".readerCatalog_list_item").nth(2).bounding_box()
            print("box:", box)
            if box:
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        except Exception as e:
            print("click err", e)
        time.sleep(5)
        print("after click responses:", cnt["n"])
        print("URL now:", page.url)
        print("title now:", page.evaluate("""() => {const e=document.querySelector('.readerTopBar_title_chapter');
                                                    return e?e.textContent.trim():'';}"""))
        b.close()


if __name__ == "__main__":
    main()
