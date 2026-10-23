#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""尝试用页内 fetch 调 Was this book's metadata endpoints, 找出 chapterUid -> c(24hex) 映射。"""
import os, re, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
BK = "3300129049"
BKSTR = "33d32010813ab98e8g019623"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(7)

        js = """async (argv) => {
          const [bk, bkstr] = argv;
          const out = {};
          const go = async (name, url, body) => {
            try {
              const r = await fetch(url, {method:'POST', credentials:'include',
                headers:{'Content-Type':'application/json;charset=UTF-8'},
                body: JSON.stringify(body)});
              const t = await r.text();
              out[name] = {status: r.status, len: t.length, head: t.slice(0, 900)};
            } catch (e) { out[name] = {err: String(e).slice(0,120)}; }
          };
          await go('outline', '/web/book/outline', {bookId: bk, chapterUids: [1,2,3,90,91,95]});
          await go('chapterInfos', '/web/book/chapterInfos', {bookIds:[bk]});
          await go('toc', '/web/book/toc', {bookId: bk});
          await go('getToc', '/web/book/getToc', {bookId: bk});
          return out;
        }"""
        res = page.evaluate(js, [BK, BKSTR])
        json.dump(res, open("_out_probe_meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for k, v in res.items():
            print("=== %s status=%s len=%s" % (k, v.get("status"), v.get("len")))
            print((v.get("head") or v.get("err") or "")[:900])
            print()


if __name__ == "__main__":
    main()
