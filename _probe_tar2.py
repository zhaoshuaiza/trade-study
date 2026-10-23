#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""用 context.request（携带真实 cookie，不受同源限制）测试 TAR 下载。"""
import os, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

BOOK_ID = "3300129049"
ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]

        for uid in [2, 3, 5]:
            url = "https://res.weread.qq.com/wrco/tar_CB_%s_%d" % (BOOK_ID, uid)
            try:
                r = ctx.request.get(url, timeout=30000)
                body = r.body()
                print("uid %d -> status=%s bytes=%d" % (uid, r.status, len(body)))
                print("   head:", body[:80])
            except Exception as e:
                print("uid %d -> ERR %s" % (uid, str(e)[:160]))
        b.close()


if __name__ == "__main__":
    main()
