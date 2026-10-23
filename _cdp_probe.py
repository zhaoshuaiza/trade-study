#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""探测 CDP 连接：连上用户 Edge 调试端口，确认复用登录态"""
import os
# 避免 CDP 到 127.0.0.1 的 HTTP 请求被代理劫持
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
        print("version:", b.version)
        print("contexts:", len(b.contexts))
        for i, ctx in enumerate(b.contexts):
            print(f"  ctx[{i}] pages:", len(ctx.pages))
            for pg in ctx.pages:
                print("    url:", pg.url[:90])
        # 注意：CDP 模式下不要 b.close()，那会关掉用户的整个浏览器
except Exception as e:
    print("CDP ERROR:", repr(e))
