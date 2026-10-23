# -*- coding: utf-8 -*-
"""Playwright 探测 v2: 诊断正文未渲染原因(时序/付费墙/报错)。"""
import os, json
from playwright.sync_api import sync_playwright

COOKIE = os.environ.get("WR_COOKIE")
READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623?chapterUid=2"

def parse_cookies(s):
    out = []
    for kv in s.split(";"):
        kv = kv.strip()
        if "=" not in kv: continue
        k, v = kv.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(), "domain": ".weread.qq.com", "path": "/"})
    return out

def main():
    msgs, failed = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        ctx = b.new_context()
        ctx.add_cookies(parse_cookies(COOKIE))
        pg = ctx.new_page()
        pg.on("console", lambda m: msgs.append("[%s] %s" % (m.type, m.text[:200])))
        pg.on("requestfailed", lambda r: failed.append("%s %s" % (r.failure, r.url[:120])))
        pg.goto(READER, timeout=30000)
        pg.wait_for_timeout(12000)
        # 检查付费墙/试读提示
        hint = pg.evaluate("""() => {
            const t = document.body.innerText;
            const m = t.match(/购买|试读|加入书架|此章节|需要购买|立即购买|开通会员|付费/);
            return m? m[0] : null;
        }""")
        print("付费墙/提示命中:", hint)
        # 找最大文本容器
        info = pg.evaluate("""() => {
            let best=null, bl=0;
            document.querySelectorAll('div,p,section,article,span').forEach(e=>{
                const t=(e.innerText||'').trim(); if(t.length>bl){bl=t.length;best=e;}
            });
            return best? {tag:best.tagName, cls:String(best.className).slice(0,60), len:bl, sample:best.innerText.slice(0,400)}:null;
        }""")
        print("最大文本容器:", json.dumps(info, ensure_ascii=False))
        print("\n--- 控制台(前15) ---")
        for m in msgs[:15]: print(m)
        print("\n--- 失败请求(前15) ---")
        for f in failed[:15]: print(f)
        b.close()

if __name__ == "__main__":
    main()
