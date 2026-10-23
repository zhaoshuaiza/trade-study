#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""零风险检查当前页面状态(不导航),确认是否登录/限流。"""
import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        url = page.url
        title = page.title()
        snippet = page.evaluate("() => (document.body.innerText||'').replace(/\\s+/g,' ').slice(0,300)")
        has_login = "登录" in snippet or "登录后" in snippet
        has_book = "交易心理" in snippet
        print("URL:", url)
        print("TITLE:", title)
        print("SNIPPET:", snippet)
        print("has_login:", has_login, "| has_book:", has_book)
        b.close()


if __name__ == "__main__":
    main()
