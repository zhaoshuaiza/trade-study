# -*- coding: utf-8 -*-
"""决定性诊断：书架上其他书能否正常供给正文（区分账号级限流 vs 这两本书被下架）。"""
import os, time, re
os.environ["NO_PROXY"] = "127.0.0.1,localhost"; os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

BOOKS = ["02132c405e0b6a0216075c9", "15132dd05b9174151953a7d", "0633241059b4260632af2bf",
         "33d32010813ab98e8g019623", "5ea329c0813abbcbeg01667b"]

def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        hits = []
        def on_resp(r):
            if "/web/book/chapter" in r.url:
                try: n = len(r.body() or b"")
                except Exception: n = -1
                hits.append((r.url[-6:], n))
        page.on("response", on_resp)
        for bk in BOOKS:
            hits.clear()
            try:
                page.goto("https://weread.qq.com/web/reader/" + bk,
                          wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print("nav", str(e)[:40])
            time.sleep(13)
            t = re.sub(r"\s+", " ", page.evaluate("()=>(document.body.innerText||'')"))
            print("book %-24s chapter请求=%-3d 首条=%-18s 正文长度=%-6d | %s"
                  % (bk, len(hits), str(hits[:2]), len(t), t[:80]))
        page.close()

main()
