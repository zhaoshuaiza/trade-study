#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抓取章节请求的请求头(尤其 Range)与响应体片段,判断如何重组。"""
import os, time

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def main():
    recs = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        pending = {}

        def on_req(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            h = r.all_headers()
            pending[r.url + "|" + str(id(r))] = {
                "url": last,
                "full": r.url,
                "range": h.get("range"),
                "ct": h.get("content-type"),
                "extra": {k: v for k, v in h.items() if k.lower().startswith("x-") or k.lower() in ("range", "content-range")},
            }

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                body = r.body()
            except Exception:
                body = b""
            recs.append({
                "url": last,
                "full": r.url,
                "len": len(body),
                "hdr": r.headers,
                "head": body[:36].decode("latin1"),
                "payload": body[33:73].decode("latin1"),
            })

        page.on("request", on_req)
        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        for _ in range(50):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(0.2)
        time.sleep(4)
        b.close()

    print("records:", len(recs))
    for r in recs[:10]:
        print("---")
        print("url:", r["full"][-70:])
        print("resp hdr content-type:", r["hdr"].get("content-type"),
              "| range:", r["hdr"].get("content-range"), "| encoding:", r["hdr"].get("content-encoding"))
        print("len:", r["len"])
        print("head:", repr(r["head"]))
    print("=== 请求头样本 ===")
    for k, v in list(pending.items())[:5]:
        print(v["url"], "| range:", v["range"], "| extra:", v["extra"])


if __name__ == "__main__":
    main()
