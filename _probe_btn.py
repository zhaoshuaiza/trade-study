#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""列出阅读器顶栏所有可见控件，找出打开目录的入口。"""
import os, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.new_page()
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(10)
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        time.sleep(2)

        js = """() => {
            const out = [];
            document.querySelectorAll('button, a, div[class*=link], span[class*=link], div[class*=btn]').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width < 4 || r.height < 4) return;
                if (r.x > window.innerWidth || r.y > window.innerHeight) return;
                out.push({tag: el.tagName, cls: (el.className||'').toString().slice(0,70),
                          text: (el.textContent||'').trim().slice(0,16),
                          x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)});
            });
            return JSON.stringify(out.slice(0, 40), null, 1);
        }"""
        info = ""
        for attempt in range(3):
            try:
                info = page.evaluate(js)
                break
            except Exception as e:
                print("attempt %d err: %s" % (attempt, str(e)[:90]))
                time.sleep(4)
        print("=== 可见控件 ===")
        print(info)
        b.close()


if __name__ == "__main__":
    main()
