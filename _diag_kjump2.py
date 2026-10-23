#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断 k 跳转: 原始 URL + CDP getResponseBody,处理 e_e_N 格式。"""
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

        pending = {}  # requestId -> {url, idx}
        shards = {}

        def on_recv(ev):
            params = ev.get("params", {})
            resp = params.get("response", {})
            url = resp.get("url", "")
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" in url and "e_" in last:
                rid = params["requestId"]
                # 解析 idx: 取末尾数字段
                m = re.search(r"e_(\d+)$", last) or re.search(r"e_e_(\d+)$", last)
                idx = int(m.group(1)) if m else -1
                pending[rid] = {"url": url, "idx": idx, "last": last}
                print("  [recv] %s  idx=%s" % (last, idx))

        def on_fin(ev):
            rid = ev.get("params", {}).get("requestId")
            if rid not in pending:
                return
            info = pending.pop(rid)
            try:
                body = cdp.send("Network.getResponseBody", {"requestId": rid})
                b64 = body.get("body", "")
                raw = base64.b64decode(b64) if body.get("base64Encoded") else b64.encode("latin1")
                shards[info["idx"]] = raw
                print("  [got] %s len=%d" % (info["last"], len(raw)))
            except Exception as e:
                print("  [getBody fail %s] %s" % (info["last"], str(e)[:50]))

        cdp.on("Network.responseReceived", on_recv)
        cdp.on("Network.loadingFinished", on_fin)

        target = "%s?k=%s" % (READER, K)
        page.goto(target, wait_until="domcontentloaded", timeout=60000)
        time.sleep(15)
        print("[total]", sorted(shards.keys()))
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
