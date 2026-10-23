#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""收集章节响应体样本，分析为何部分无法解码。"""
import os, time, base64, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    samples = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                body = r.body()
            except Exception:
                return
            b32 = body[32:33]
            samples.append({
                "url": last,
                "len": len(body),
                "sep": b32.decode("latin1") if b32 else "",
                "head": body[:40].decode("latin1"),
                "tail_after_33": body[33:120].decode("latin1", "ignore"),
            })

        page.on("response", on_resp)
        # 重新加载阅读器，确保会有内容请求
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        for _ in range(120):
            try:
                page.keyboard.press("ArrowLeft")
            except Exception:
                pass
            time.sleep(0.15)
        time.sleep(4)
        for _ in range(120):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(0.15)
        time.sleep(4)
        b.close()

    print("collected:", len(samples))
    json.dump(samples, open(os.path.join(ROOT, "_resp_samples.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    seps = {}
    for s in samples:
        seps[s["sep"]] = seps.get(s["sep"], 0) + 1
    print("separator stats:", seps)
    for s in samples[:6]:
        print("---")
        print("url:", s["url"], "len:", s["len"], "sep:", repr(s["sep"]))
        print("head:", repr(s["head"]))
        print("after33:", repr(s["tail_after_33"][:80]))


if __name__ == "__main__":
    main()
