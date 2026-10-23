#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断 k 跳转: 事件中只存 Response 对象,等待后统一读 body,处理 e_e_N。"""
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

        stored = []
        def on_resp(resp):
            url = resp.url
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in url and "e_" in last:
                stored.append(resp)
                print("  [store] %s" % last)

        page.on("response", on_resp)
        target = "%s?k=%s" % (READER, K)
        page.goto(target, wait_until="domcontentloaded", timeout=60000)
        time.sleep(15)

        shards = {}
        for resp in stored:
            url = resp.url
            last = url.rstrip("/").split("/")[-1]
            m = re.search(r"e_e_(\d+)$", last) or re.search(r"e_(\d+)$", last)
            idx = int(m.group(1)) if m else -1
            try:
                body = resp.body()
            except Exception as e:
                print("  [body fail %s] %s" % (last, str(e)[:50]))
                continue
            if body:
                shards[idx] = body
                print("  [got] %s len=%d" % (last, len(body)))
        print("[total idx]", sorted(shards.keys()))
        for idx in sorted(shards.keys()):
            raw = shards[idx]
            s = raw[33:].decode("latin1")
            try:
                dec = base64.b64decode(s + "=" * ((-len(s)) % 4))
                print("  e_%s len=%d has_xml=%s head=%s" % (idx, len(raw), b"<?xml" in dec, dec[:24]))
            except Exception as e:
                print("  e_%s decode FAIL %s" % (idx, str(e)[:50]))
        b.close()


if __name__ == "__main__":
    main()
