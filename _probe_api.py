#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在已登录页面上下文中直接调接口，看看能不能拿到章节列表与正文。"""
import os, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

BOOK_ID = "3300129049"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=40000)
        time.sleep(3)

        # 1) 章节列表
        res = page.evaluate("""async (bookId) => {
            try {
                const r = await fetch('/web/book/chapterInfos', {method:'POST', credentials:'include',
                    headers:{'content-type':'application/json'}, body: JSON.stringify({bookIds:[bookId]})});
                return await r.text();
            } catch(e) { return 'ERR ' + e.message; }
        }""", BOOK_ID)
        print("=== chapterInfos ===", res[:300])
        try:
            d = json.loads(res)
            chaps = (d.get("data") or [{}])[0].get("updated") or []
            print("chapter count:", len(chaps))
            print("sample:", json.dumps(chaps[:3], ensure_ascii=False)[:400])
        except Exception as e:
            print("parse err", e)

        # 2) 直取章节内容
        for url in ["/web/book/chapter/e_1", "/web/book/chapter/e_0"]:
            out = page.evaluate("""async (u) => {
                try { const r = await fetch(u, {credentials:'include'});
                      return r.status + ' | ' + (await r.text()).slice(0, 160); }
                catch(e) { return 'ERR ' + e.message; }
            }""", url)
            print("=== fetch %s ===" % url, out)

        # 3) 其他可能的内容端点
        for u in ["/web/book/chapterlist?bookId=%s" % BOOK_ID,
                  "/web/book/getChapter?bookId=%s" % BOOK_ID]:
            out = page.evaluate("""async (u) => {
                try { const r = await fetch(u, {credentials:'include'});
                      return r.status + ' | ' + (await r.text()).slice(0, 120); }
                catch(e) { return 'ERR ' + e.message; }
            }""", u)
            print("=== %s ===" % u, out[:180])
        b.close()


if __name__ == "__main__":
    main()
