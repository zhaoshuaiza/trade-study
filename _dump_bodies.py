#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把一次页面加载的全部章节响应原样存盘，供离线分析。"""
import os, time, hashlib

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
ROOT = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(ROOT, "_rawcap")
os.makedirs(DST, exist_ok=True)


def main():
    seen = set()
    n = 0
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]

        def on_resp(r):
            nonlocal n
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                body = r.body()
            except Exception:
                return
            h = hashlib.md5(body).hexdigest()[:12]
            if h in seen:
                return
            seen.add(h)
            n += 1
            path = os.path.join(DST, "%03d_%s_len%d.bin" % (n, last, len(body)))
            with open(path, "wb") as f:
                f.write(body)

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        for _ in range(60):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(0.22)
        time.sleep(5)
        b.close()
    print("saved %d bodies -> %s" % (n, DST))


if __name__ == "__main__":
    main()
