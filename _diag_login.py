#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断登录态：接口层验证 + 页面截图 + cookie 回读"""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))

def parse_cookie(s):
    out = []
    for part in s.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(),
                    "domain": ".qq.com", "path": "/"})
    return out

with open(os.path.join(ROOT, "_cookie.txt"), encoding="utf-8") as fh:
    cookies = parse_cookie(fh.read().strip())

proxy = None
env_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if env_proxy:
    proxy = {"server": env_proxy}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, proxy=proxy, args=["--no-sandbox"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    ctx.add_cookies(cookies)
    page = ctx.new_page()

    # 1) 接口层验证：shelf/sync 是否认登录态
    try:
        r = page.request.get("https://weread.qq.com/web/shelf/sync",
                             headers={"Referer": "https://weread.qq.com/"})
        print("== shelf/sync status:", r.status)
        print("== shelf/sync body:", r.text()[:200])
    except Exception as e:
        print("shelf request error:", e)

    # 2) 打开书页
    page.goto("https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
              wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(ROOT, "_diag_login.png"), full_page=False)

    # 3) 回读注入的 cookie（非 HttpOnly 部分）
    print("== document.cookie:", (page.evaluate("document.cookie") or "")[:300])
    # 4) 页面文本前 400 字
    print("== body text:", (page.evaluate("document.body.innerText") or "")[:400].replace("\n", " | "))
    browser.close()
