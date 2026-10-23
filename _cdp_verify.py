#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 CDP 连上真实 Edge（原始 profile），验证微信读书登录态"""
import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    print("CONNECTED")
    ctx = b.contexts[0]
    cs = ctx.cookies()
    wr = {c["name"]: c["value"] for c in cs if "weread" in (c.get("domain") or "")}
    print("weread cookie count:", len(wr))
    for k in ("wr_vid", "wr_skey", "wr_rt", "wr_name"):
        v = wr.get(k)
        print(f"  {k}: {'YES len=' + str(len(v)) if v else 'MISSING'}")
    page = ctx.new_page()
    for url in ("https://weread.qq.com/web/shelf/sync",):
        try:
            r = page.request.get(url, headers={"Referer": "https://weread.qq.com/"})
            print("shelf/sync:", r.text()[:250])
        except Exception as e:
            print("shelf error:", repr(e))
    page.close()
    # 注意：不要 b.close()，会关掉 headless Edge
