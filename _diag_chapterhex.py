#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""元数据探测: 提取每章的 k-hex(阅读器 URL 锚点) 与 chapterUid 映射, 重点拿 chapterUid=1 的 hex。"""
import os, re, time, json
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
BOOKID = "3300129049"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)
        # 在页内 fetch chapterInfos(元数据, 不受限流影响)
        info = page.evaluate("""async () => {
            try {
                const r = await fetch('/web/book/chapterInfos?bookId=%s', {credentials:'include'});
                const j = await r.json();
                const arr = j.data || j.chapters || j.items || [];
                // 看看每个元素有哪些字段
                if (arr.length) return {count: arr.length, sample: arr[0], keys: Object.keys(arr[0])};
                return {raw: JSON.stringify(j).slice(0,500)};
            } catch(e){ return {err: String(e).slice(0,200)}; }
        }""" % BOOKID)
        print(json.dumps(info, ensure_ascii=False, indent=1)[:2000])
        b.close()


if __name__ == "__main__":
    main()
