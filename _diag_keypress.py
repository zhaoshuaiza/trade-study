#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在当前页面按 ArrowLeft 回到 uid89,同步抓取 e_ 分片 body(在响应事件内读取)。"""
import os, re, time, base64
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

BOOK = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


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
            if "/web/book/chapter/" in url and "e_" in last:
                m = re.search(r"e_e?_(\d+)$", last) or re.search(r"e_(\d+)$", last)
                idx = int(m.group(1)) if m else -1
                try:
                    st = resp.status
                    body = resp.body()
                except Exception as e:
                    print("  [err %s] %s" % (last, str(e)[:50]))
                    return
                if body:
                    shards[idx] = body
                    print("  [got %s] status=%s len=%d" % (last, st, len(body)))

        page.on("response", on_resp)
        # 先按几次 ArrowLeft 回到 uid89 区域(慢速)
        for i in range(6):
            try: page.keyboard.press("ArrowLeft")
            except Exception: pass
            time.sleep(2.5)
        time.sleep(5)
        print("[total idx]", sorted(shards.keys()))
        for idx in sorted(shards.keys()):
            raw = shards[idx]
            s = raw[33:].decode("latin1")
            try:
                dec = base64.b64decode(s + "=" * ((-len(s)) % 4))
                print("  e_%s len=%d has_xml=%s head=%s" % (idx, len(raw), b"<?xml" in dec, dec[:24]))
            except Exception as e:
                print("  e_%s FAIL %s" % (idx, str(e)[:50]))
        b.close()


if __name__ == "__main__":
    main()
