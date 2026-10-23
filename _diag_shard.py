#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断: 通过 CDP 抓取 /web/book/chapter/e_ 分片原始字节,检查前缀与 base64 解码,
定位为何 assemble 全部失败。"""
import os, re, time, base64, json
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
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.clearBrowserCache")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})

        captured = {}  # idx -> base64 body

        def on_resp(ev):
            p = ev.get("params", {})
            resp = p.get("response", {})
            url = resp.get("url", "")
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in url and last.startswith("e_"):
                try:
                    rid = p["requestId"]
                    body = cdp.send("Network.getResponseBody", {"requestId": rid})
                    b64 = body.get("body", "")
                    idx = int(last.split("_")[1])
                    captured[idx] = (b64, body.get("base64Encoded", True))
                except Exception as e:
                    print("  [getBody fail]", last, str(e)[:60])

        cdp.on("Network.responseReceived", on_resp)

        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        # 预热 + 触发几章加载(慢速)
        for i in range(12):
            try: page.keyboard.press("ArrowRight")
            except Exception: pass
            time.sleep(2.5)
        time.sleep(3)
        print("[captured shards] idx 列表:", sorted(captured.keys()))
        # 对每组(以 e_0 开头)检查
        keys = sorted(captured.keys())
        if not keys:
            print("!!! 没有抓到任何分片 —— 说明网络层这次也没拿到正文请求")
            b.close()
            return
        # 取最小的 idx 组(通常是一组连续分片),展示前缀
        sample = keys[:6]
        print("[sample 前缀 hex]")
        for idx in sample:
            b64, isb = captured[idx]
            raw = base64.b64decode(b64) if isb else b64.encode("latin1")
            print("  e_%d  len=%d  head=%s" % (idx, len(raw), raw[:40].hex()))
        # 尝试 hdr=33 解码并看是否能找到 <?xml
        print("[decode 尝试 hdr=33]")
        for idx in sample:
            b64, isb = captured[idx]
            raw = base64.b64decode(b64) if isb else b64.encode("latin1")
            s = raw[33:].decode("latin1")
            try:
                dec = base64.b64decode(s + "=" * ((-len(s)) % 4))
                head = dec[:20]
                has_xml = b"<?xml" in dec
                print("  e_%d  decode_len=%d  has_xml=%s  head=%s" % (idx, len(dec), has_xml, dec[:30]))
            except Exception as e:
                print("  e_%d  decode FAIL: %s" % (idx, str(e)[:60]))
        b.close()


if __name__ == "__main__":
    main()
