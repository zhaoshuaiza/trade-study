#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断v3: 硬刷新恢复正文,定位上一页/下一页按钮并验证点击有效。"""
import os, re, time

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def content_len(page):
    return page.evaluate("""() => {
      const c = document.querySelector('.readerChapterContent') || document.body;
      return (c.innerText||'').length;
    }""")


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        page.bring_to_front()
        try:
            page.set_viewport_size({"width": 1440, "height": 900})
        except Exception as e:
            print("[vp]", str(e)[:50])
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.clearBrowserCache")
        print("[cdp] cache cleared")

        for attempt in (1, 2, 3):
            try:
                page.goto(READER, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print("[nav]", str(e)[:50])
            time.sleep(9)
            print("  尝试%d 正文字数=%d url=%s" % (attempt, content_len(page), page.url[-30:]))
            if content_len(page) > 800:
                break
            page.keyboard.press("F5")
            time.sleep(6)

        print("\n=== 寻找上一页/下一页按钮 ===")
        info = page.evaluate("""() => {
          const out=[];
          const walk = (el) => {
            for (const c of el.children) {
              const tx = (c.textContent||'').trim();
              if ((tx==='下一页'||tx==='上一页') && c.children.length<=3) {
                const r=c.getBoundingClientRect();
                if (r.width>0) out.push({txt:tx, cls:String(c.className).slice(0,60),
                   tag:c.tagName, x:Math.round(r.x+r.width/2), y:Math.round(r.y+r.height/2),
                   w:Math.round(r.width), h:Math.round(r.height)});
              }
              walk(c);
            }
          };
          walk(document.body);
          return out;
        }""")
        for e in info:
            print("  ", e)

        nxt = [e for e in info if e["txt"] == "下一页"]
        if nxt:
            e = nxt[0]
            before = page.evaluate("() => (document.querySelector('.readerChapterContent')||document.body).innerText.slice(0,120)")
            print("\n-- 点击下一页 (%d,%d) cls=%s" % (e["x"], e["y"], e["cls"][:40]))
            page.mouse.click(e["x"], e["y"])
            time.sleep(5)
            after = page.evaluate("() => (document.querySelector('.readerChapterContent')||document.body).innerText.slice(0,120)")
            print("   before:", before.replace("\n", "|")[:100])
            print("   after :", after.replace("\n", "|")[:100])
            print("   变化?", before != after, "| url:", page.url[-40:])
        else:
            print("  未找到下一页按钮; 列出所有含'页'的可点元素:")
            print(page.evaluate("""() => {
              const out=[]; document.querySelectorAll('div,span,button,a').forEach(e=>{
                const t=(e.textContent||'').trim();
                if(/下一页|上一页|目录/.test(t) && t.length<12){
                  const r=e.getBoundingClientRect();
                  out.push({t:t, cls:String(e.className).slice(0,50), x:Math.round(r.x+r.width/2), y:Math.round(r.y+r.height/2)});
                }});
              return out.slice(0,10);
            }"""))


if __name__ == "__main__":
    main()
