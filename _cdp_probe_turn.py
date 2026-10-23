#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断: 找出真正能翻页的交互方式 (按钮坐标点击 / 键盘事件注入)。"""
import os, re, time, json

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def sig(page):
    try:
        u = page.url
        m = re.search(r"k([0-9a-f]{20,})", u)
        t = page.evaluate("() => (document.body.innerText||'').slice(0,200)")
        return (m.group(1) if m else "noanchor", t[:40].replace("\n", "|"))
    except Exception as e:
        return ("err", str(e)[:40])


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(8)
        page.bring_to_front()

        print("=== activeElement ===")
        print(page.evaluate(
            "() => {const a=document.activeElement; return a ? a.tagName+'.'+String(a.className).slice(0,60) : 'none';}"))

        print("=== 含 arrow 的元素 ===")
        els = page.evaluate("""() => {
          const out=[];
          document.querySelectorAll('*').forEach(e=>{
            const c=String(e.className||'');
            if (/arrow/i.test(c) || /arrow/i.test(String(e.id||''))) {
              const r=e.getBoundingClientRect();
              if (r.width>0 && r.height>0) out.push({cls:c.slice(0,70), id:e.id, x:Math.round(r.x+r.width/2), y:Math.round(r.y+r.height/2), w:Math.round(r.width), h:Math.round(r.height)});
            }
          });
          return out.slice(0,15);
        }""")
        for e in els:
            print("  ", e)

        base = sig(page)
        print("\n基线:", base)

        # 方式 1: 点击最后一个(通常是右箭头)元素坐标
        if els:
            e = els[-1]
            print("\n-- 测试点击最右箭头 (%d,%d) cls=%s" % (e["x"], e["y"], e["cls"][:40]))
            page.mouse.click(e["x"], e["y"])
            time.sleep(4)
            print("   结果:", sig(page), "同基线?" , sig(page) == base)

        # 方式 2: JS 键盘事件注入 (window -> document -> body)
        print("\n-- 测试 JS 注入 keydown ArrowRight")
        page.evaluate("""() => {
          const ev = () => new KeyboardEvent('keydown', {key:'ArrowRight', code:'ArrowRight',
             keyCode:39, which:39, bubbles:true, cancelable:true});
          window.dispatchEvent(ev());
          document.dispatchEvent(ev());
          document.body.dispatchEvent(ev());
        }""")
        time.sleep(4)
        print("   结果:", sig(page))

        # 方式 3: CDP 原生按键
        print("\n-- 测试 CDP Input.dispatchKeyEvent")
        cdp = ctx.new_cdp_session(page)
        for t, k in [("rawKeyDown", "ArrowRight"), ("char", "ArrowRight"), ("keyUp", "ArrowRight")]:
            cdp.send("Input.dispatchKeyEvent", {
                "type": t, "windowsVirtualKeyCode": 39, "code": "ArrowRight",
                "key": "ArrowRight", "nativeVirtualKeyCode": 39})
            time.sleep(0.6)
        time.sleep(4)
        print("   结果:", sig(page))

        # 方式 4: 直接 JS 调用翻页 API (若 Vue 实例暴露)
        print("\n-- 测试 app.__vue__ / router 是否存在")
        print(page.evaluate("""() => {
          const keys = Object.keys(window).filter(k=>/vue|reader|app/i.test(k)).slice(0,10);
          return JSON.stringify(keys);
        }"""))


if __name__ == "__main__":
    main()
