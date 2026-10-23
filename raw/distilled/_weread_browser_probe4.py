# -*- coding: utf-8 -*-
"""Playwright 探测 v4: JS强制点开始阅读, 检查iframe与阅读容器。"""
import os, json
from playwright.sync_api import sync_playwright

COOKIE = os.environ.get("WR_COOKIE")
READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"

def parse_cookies(s):
    out = []
    for kv in s.split(";"):
        kv = kv.strip()
        if "=" not in kv: continue
        k, v = kv.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(), "domain": ".weread.qq.com", "path": "/"})
    return out

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        ctx = b.new_context()
        ctx.add_cookies(parse_cookies(COOKIE))
        pg = ctx.new_page()
        pg.goto(READER, timeout=30000)
        pg.wait_for_timeout(3000)
        # JS强制点 开始阅读
        clicked = pg.evaluate("""() => {
            const els=[...document.querySelectorAll('div')].filter(e=>e.innerText && e.innerText.trim()==='开始阅读');
            if(els.length){els[0].click(); return true;} return false;
        }""")
        print("JS点击开始阅读:", clicked)
        pg.wait_for_timeout(8000)
        # 检查iframe
        frames = pg.frames
        print("iframe数:", len(frames))
        for f in frames[1:]:
            print("  frame url:", f.url[:100])
        # 在当前页查阅读容器
        info = pg.evaluate("""() => {
            let best=null, bl=0;
            document.querySelectorAll('div,p,section,article,span').forEach(e=>{
                const t=(e.innerText||'').trim(); if(t.length>bl){bl=t.length;best=e;}
            });
            return best? {tag:best.tagName, cls:String(best.className).slice(0,80), len:bl, sample:best.innerText.slice(0,400)}:null;
        }""")
        print("最大文本容器:", json.dumps(info, ensure_ascii=False))
        b.close()

if __name__ == "__main__":
    main()
