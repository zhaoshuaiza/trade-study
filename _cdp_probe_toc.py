#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""探查: 阅读器页面发出的所有 XHR endpoint + 目录 DOM 是否带章节 id 属性。"""
import os, re, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
seen = {}


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")

        def on_sent(ev):
            req = ev.get("request", {})
            u = req.get("url", "")
            if "weread.qq.com" not in u:
                return
            if req.get("method") == "POST" or "/web/" in u:
                key = re.sub(r"\d{10,}", "T", u)
                old = seen.get(key)
                seen[key] = old or {"method": req.get("method"), "post": req.get("postData")}

        cdp.on("Network.requestWillBeSent", on_sent)

        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(8)
        for _ in range(2):
            page.keyboard.press("ArrowRight")
            time.sleep(2.0)
        time.sleep(2)

        print("=== endpoints ===")
        for u, d in seen.items():
            print(" -", d["method"], u[:150])
            if d["post"]:
                print("     post:", str(d["post"])[:160])

        # 目录 DOM 探查
        print("=== 目录 DOM 探查 ===")
        info = page.evaluate("""() => {
          const res = {};
          const titles = document.querySelectorAll('.readerCatalogListItem, .catalogListItem, [class*="Catalog"] li, [class*="catalog"] li');
          res.counts = [document.querySelectorAll('.readerCatalogListItem').length,
                        document.querySelectorAll('[class*="atalog"] li').length];
          const sample = [];
          document.querySelectorAll('[class*="atalog"] li').forEach((el, i) => {
            if (i < 6) {
              const attrs = {};
              for (const a of el.attributes) attrs[a.name] = String(a.value).slice(0, 80);
              sample.push({txt: el.innerText.slice(0,40), attrs: attrs, html: el.outerHTML.slice(0, 300)});
            }
          });
          res.sample = sample;
          // 全文中出现的所有 24 位 hex 片段數量
          const h = document.documentElement.innerHTML;
          res.hex24 = (h.match(/[0-9a-f]{24}/g) || []).slice(0, 12);
          res.hexN = (h.match(/[0-9a-f]{24}/g) || []).length;
          return res;
        }""")
        print(json.dumps(info, ensure_ascii=False)[:4000])


if __name__ == "__main__":
    main()
