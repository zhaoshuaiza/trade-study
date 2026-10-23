#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""禁用缓存 + 跳首章后,打印每个分片的独立解码情况,定位组装失败原因。"""
import os, time, base64, re

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
ROOT = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(ROOT, "_rawcap2")
os.makedirs(DST, exist_ok=True)


def loose(s):
    try:
        return base64.b64decode(s + "=" * ((-len(s)) % 4))
    except Exception:
        return None


def main():
    recs = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        try:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            print("[cdp] cache disabled")
        except Exception as e:
            print("[cdp] fail", str(e)[:80])

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                idx = int(last.split("_")[1]); body = r.body()
            except Exception:
                return
            recs.append((time.time(), idx, body))

        page.on("response", on_resp)
        # 跳首章
        try:
            page.locator("button.readerControls_item.catalog").first.click(timeout=5000)
        except Exception:
            pass
        time.sleep(2)
        page.evaluate("""() => { const it=document.querySelectorAll('.readerCatalog_list_item')[0]; if(it) it.click(); }""")
        time.sleep(4)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        for _ in range(40):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(0.25)
        time.sleep(4)
        b.close()

    print("responses:", len(recs))
    for n, (t, i, body) in enumerate(recs[:14]):
        pay = body[33:].decode("latin1")
        raw = loose(pay)
        prev = ""
        if raw:
            prev = raw[:24].decode("utf-8", "ignore").replace("\n", "")
        open(os.path.join(DST, "%03d_e%d_len%d.bin" % (n, i, len(body))), "wb").write(body)
        print("[%02d] t=%+.2fs e_%d len=%-6d pay=%r decode=%r"
              % (n, t - recs[0][0], i, len(body), pay[:16], prev[:32]))


if __name__ == "__main__":
    main()
