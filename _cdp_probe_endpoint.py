#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""探针: 抓一次真实的 chapter 请求(method/URL/headers),并测试页内 fetch 能否主动取分片。"""
import os, re, time, json, base64

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"

INFO = {}


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")

        def on_sent(ev):
            u = ev.get("request", {}).get("url", "")
            if "/web/book/chapter/" in u:
                INFO.setdefault("url", u)
                INFO.setdefault("method", ev["request"].get("method"))
                INFO.setdefault("headers", ev["request"].get("headers"))
                INFO.setdefault("post", ev["request"].get("postData"))

        cdp.on("Network.requestWillBeSent", on_sent)

        print("[nav]", page.url[:90])
        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav warn]", str(e)[:80])
        time.sleep(6)
        # 触发一次翻页以产生 chapter 请求
        for _ in range(3):
            page.keyboard.press("ArrowRight")
            time.sleep(2.5)
        time.sleep(3)

        print("=== 真实请求 ===")
        print("method:", INFO.get("method"))
        print("url   :", INFO.get("url"))
        print("post  :", str(INFO.get("post"))[:200])
        hs = INFO.get("headers") or {}
        for k in sorted(hs):
            if k.lower() in ("cookie", "referer", "wr_vid", "wr_skey", "x-requested-with",
                             "content-type", "accept", "sec-ch-ua", "user-agent"):
                print("  hdr %s: %s" % (k, str(hs[k])[:120]))

        # ---- 主动 fetch 测试 ----
        print("=== 页内 fetch 测试 ===")
        res = page.evaluate("""async () => {
          const out = [];
          for (const i of [0,1,3,4,5]) {
            try {
              const r = await fetch('/web/book/chapter/e_' + i, {credentials:'include'});
              const t = await r.text();
              out.push([i, r.status, t.length, t.slice(0,40)]);
            } catch (e) { out.push([i, 'ERR', String(e).slice(0,80), '']); }
          }
          return out;
        }""")
        for row in res:
            print("  e_%s status=%s len=%s head=%r" % tuple(row))


if __name__ == "__main__":
    main()
