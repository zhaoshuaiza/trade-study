#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试能否直接下载章节 TAR 包（tar_CB_<bookId>_<chapterUid>）。"""
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

        # 抓基础信息
        res = page.evaluate("""async (bookId) => {
            const r = await fetch('/web/book/chapterInfos', {method:'POST', credentials:'include',
                headers:{'content-type':'application/json'}, body: JSON.stringify({bookIds:[bookId]})});
            return await r.text();
        }""", BOOK_ID)
        d = json.loads(res)
        chaps = (d.get("data") or [{}])[0].get("updated") or []
        print("chapters:", len(chaps))
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_chapters.json"),
                  "w", encoding="utf-8") as f:
            json.dump(chaps, f, ensure_ascii=False, indent=1)

        # 试几种 tar 取值方式
        for uid in [2, 3, 5]:
            url = "https://res.weread.qq.com/wrco/tar_CB_%s_%d" % (BOOK_ID, uid)
            out = page.evaluate("""async (u) => {
                try {
                    const r = await fetch(u, {credentials:'include'});
                    const t = await r.arrayBuffer();
                    return {status: r.status, bytes: t.byteLength,
                            head: Array.from(new Uint8Array(t.slice(0, 60)))
                                   .map(x => String.fromCharCode(x)).join('')};
                } catch(e) { return 'ERR ' + e.message; }
            }""", url)
            print("uid %d ->" % uid, json.dumps(out, ensure_ascii=False)[:220])
        b.close()


if __name__ == "__main__":
    main()
