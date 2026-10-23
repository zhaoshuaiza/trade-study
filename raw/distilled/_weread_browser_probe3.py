# -*- coding: utf-8 -*-
"""Playwright 探测 v3: 点 开始阅读 进入阅读视图, 抽取首章正文。"""
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
        # 点 开始阅读
        try:
            pg.get_by_text("开始阅读", exact=False).first.click(timeout=8000)
            print("已点击 开始阅读")
        except Exception as e:
            print("点击 开始阅读 失败:", e)
        pg.wait_for_timeout(8000)
        # 找阅读容器
        info = pg.evaluate("""() => {
            let best=null, bl=0;
            document.querySelectorAll('div,p,section,article,span').forEach(e=>{
                const t=(e.innerText||'').trim(); if(t.length>bl){bl=t.length;best=e;}
            });
            return best? {tag:best.tagName, cls:String(best.className).slice(0,80), len:bl, sample:best.innerText.slice(0,500)}:null;
        }""")
        print("最大文本容器:", json.dumps(info, ensure_ascii=False))
        b.close()

if __name__ == "__main__":
    main()
