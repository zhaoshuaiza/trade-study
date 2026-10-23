#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断v2: 判断阅读模式(翻页/滚动),找出有效的翻页/滚动方式。"""
import os, re, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"

PROBE = """() => {
  const pick = document.querySelector('.readerChapterContent, .app_content, .reader_content, #app .reader');
  const src = pick || document.body;
  const t = (src.innerText||'').replace(/\\s+/g,' ').slice(0,160);
  return {v: src.scrollTop, h: src.scrollHeight, txt: t, url: location.href.slice(-40)};
}"""


def show(tag, s):
    print("  %-14s scrollTop=%-7s h=%-7s url=%s\n      %s" % (tag, s["v"], s["h"], s["url"], s["txt"][:110]))


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        page.bring_to_front()
        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(8)

        print("=== viewport ===", page.viewport_size, "device:", page.evaluate("()=>innerWidth+'x'+innerHeight"))
        print("=== DOM 骨架 ===")
        print(page.evaluate("""() => {
          const walk=(el,d)=>{ if(d>3) return '';
            let s=''; for(const c of el.children){ s+= '  '.repeat(d)+c.tagName+'.'+String(c.className).slice(0,45)+'\\n'+walk(c,d+1);} return s; };
          return walk(document.body,0).slice(0,1800);
        }"""))

        base = page.evaluate(PROBE)
        show("基线", base)

        cdp = ctx.new_cdp_session(page)

        def try_key(label, key, code, vk):
            page.keyboard.press(key)
            time.sleep(3.5)
            s = page.evaluate(PROBE)
            same = (s["txt"] == base["txt"]) and (s["v"] == base["v"])
            show("%s same=%s" % (label, same), s)
            return s

        for label, key, code, vk in [("ArrowRight", "ArrowRight", "ArrowRight", 39),
                                     ("ArrowDown", "ArrowDown", "ArrowDown", 40),
                                     ("PageDown", "PageDown", "PageDown", 34),
                                     ("Space", "Space", "Space", 32)]:
            try_key(label, key, code, vk)

        # 滚轮
        print("\n-- 鼠标滚轮 --")
        for _ in range(3):
            cdp.send("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": 700, "y": 400,
                                                  "deltaX": 0, "deltaY": 800,
                                                  "pointerType": "mouse"})
            time.sleep(0.5)
        time.sleep(3)
        show("wheel", page.evaluate(PROBE))

        print("\n-- JS scroll container --")
        print(page.evaluate("""() => {
          const c = document.querySelector('.readerChapterContent, .app_content, .reader_content, #app .reader') || document.scrollingElement;
          c.scrollTop += 1200;
          return 'scrolled '+c.scrollTop;
        }"""))
        time.sleep(3)
        show("js scroll", page.evaluate(PROBE))


if __name__ == "__main__":
    main()
