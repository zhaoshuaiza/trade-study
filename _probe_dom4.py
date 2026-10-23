#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抽取整页 textContent 并定位 #1/最佳实践 等标记的真实上下文,判断是否含可读正文。"""
import os, re, time, json, argparse
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = {
    "2015": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
    "2002": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="2015", choices=["2015", "2002"])
    ap.add_argument("--wait", type=float, default=12.0)
    ap.add_argument("--out", default="/tmp/full_textcontent.txt")
    args = ap.parse_args()

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        try:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.enable")
            cdp.send("Network.clearBrowserCache")
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        except Exception:
            cdp = None
        page.goto(BOOK[args.book], wait_until="domcontentloaded", timeout=60000)
        time.sleep(args.wait)
        full = page.evaluate("() => document.documentElement.textContent || ''")
        with open(args.out, "w", encoding="utf-8", newline="") as f:
            f.write(full)
        print("[write] textContent 长度:", len(full), "->", args.out)
        # 定位标记上下文
        for m in ["最佳实践#1", "最佳实践#22", "最佳实践#23", "#1", "适应变化", "小结：从思想到行动"]:
            i = full.find(m)
            if i >= 0:
                snip = full[max(0,i-80):i+160].replace("\n"," ")
                print("\n[命中 %s] @%d:\n  ...%s..." % (m, i, snip))
            else:
                print("\n[未命中] %s" % m)
        b.close()


if __name__ == "__main__":
    main()
