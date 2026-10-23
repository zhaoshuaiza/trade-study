#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断(playwright response 事件版): 捕获所有 weread 响应 URL,并检查 e_ 分片解码。"""
import os, re, time, base64
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass

        endpoints = {}
        shards = {}

        def on_resp(resp):
            url = resp.url
            if "weread.qq.com" not in url:
                return
            # 统计端点
            path = re.sub(r"\?.*$", "", url.split("weread.qq.com")[-1])
            path = re.sub(r"/[0-9a-f]{8,}", "/{id}", path)
            endpoints[path] = endpoints.get(path, 0) + 1
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in url and last.startswith("e_"):
                try:
                    body = resp.body()
                    if body:
                        idx = int(last.split("_")[1])
                        shards[idx] = body
                except Exception as e:
                    print("  [body fail]", last, str(e)[:50])

        page.on("response", on_resp)
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.clearBrowserCache")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})

        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        # 预热激活 + 多翻几章(慢速)
        for i in range(20):
            try: page.keyboard.press("ArrowRight")
            except Exception: pass
            time.sleep(2.0)
        time.sleep(2)
        print("[endpoints] 出现的 weread 端点:")
        for k, v in sorted(endpoints.items(), key=lambda x: -x[1]):
            print("   %4d  %s" % (v, k))
        print("[shards] 捕获 e_ 分片 idx:", sorted(shards.keys()))
        if shards:
            for idx in sorted(shards.keys())[:8]:
                raw = shards[idx]
                print("  e_%d len=%d head=%s" % (idx, len(raw), raw[:40].hex()))
            # decode hdr=33
            print("[decode hdr=33]")
            for idx in sorted(shards.keys())[:8]:
                raw = shards[idx]
                s = raw[33:].decode("latin1")
                try:
                    dec = base64.b64decode(s + "=" * ((-len(s)) % 4))
                    print("  e_%d dec_len=%d has_xml=%s head=%s" % (idx, len(dec), b"<?xml" in dec, dec[:24]))
                except Exception as e:
                    print("  e_%d FAIL %s" % (idx, str(e)[:50]))
        b.close()


if __name__ == "__main__":
    main()
