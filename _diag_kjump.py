#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断 k 锚点跳转是否触发完整 e_0..e_N 分片。"""
import os, re, time, base64
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
K = "764323602597647966b7a1c"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.clearBrowserCache")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})

        shards = {}
        def on_resp(resp):
            url = resp.url
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in url and last.startswith("e_"):
                try:
                    body = resp.body()
                    if body:
                        shards[int(last.split("_")[1])] = body
                        print("  [+e_%d] len=%d" % (int(last.split("_")[1]), len(body)))
                except Exception as e:
                    print("  [body fail e_%s] %s" % (last, str(e)[:50]))

        page.on("response", on_resp)
        target = "%s?k=%s" % (READER, K)
        print("[nav]", target[-40:])
        page.goto(target, wait_until="domcontentloaded", timeout=60000)
        time.sleep(15)
        print("[total e_ shards]", sorted(shards.keys()))
        for idx in sorted(shards.keys()):
            raw = shards[idx]
            s = raw[33:].decode("latin1")
            try:
                dec = base64.b64decode(s + "=" * ((-len(s)) % 4))
                head = dec[:30]
                has_xml = b"<?xml" in dec
            except Exception:
                head = b""; has_xml = False
            print("  e_%d len=%d has_xml=%s head=%s" % (idx, len(raw), has_xml, head[:24]))
        b.close()


if __name__ == "__main__":
    main()
