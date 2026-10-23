# -*- coding: utf-8 -*-
"""Playwright 探测: 注入cookie, 打开阅读器, 定位正文容器。"""
import os, json, re
from playwright.sync_api import sync_playwright

COOKIE = os.environ.get("WR_COOKIE")
READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"  # 2015书

def parse_cookies(s):
    out = []
    for kv in s.split(";"):
        kv = kv.strip()
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(),
                    "domain": ".weread.qq.com", "path": "/"})
    return out

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        ctx = b.new_context()
        ctx.add_cookies(parse_cookies(COOKIE))
        pg = ctx.new_page()
        # 先访问主页让cookie生效
        pg.goto("https://weread.qq.com/", timeout=30000)
        print("主页 title:", pg.title())
        # 打开阅读器(指定chapterUid=2, 首章是封面)
        url = READER + "?chapterUid=2"
        pg.goto(url, timeout=30000)
        pg.wait_for_timeout(4000)
        print("阅读器 title:", pg.title())
        # 找正文容器: 尝试若干选择器
        sel = ["#app", ".readerContent", ".readerChapterContent", ".readingArea",
               ".wr_readerContent", ".readerContainer", ".app_content", "main", "article"]
        for s in sel:
            try:
                txt = pg.eval_on_selector(s, "e => e.innerText") if False else None
            except Exception:
                pass
        # 直接取 body innerText 长度 + 样本
        body = pg.evaluate("() => document.body.innerText")
        print("body innerText 长度:", len(body))
        print("样本(前600):", body[:600])
        # 找包含较多文字的元素
        big = pg.evaluate("""() => {
            let best=null, bl=0;
            document.querySelectorAll('*').forEach(e=>{
                if(e.children.length===0){const t=e.innerText||''; if(t.length>bl){bl=t.length;best=e;}}
            });
            return best? {tag:best.tagName, cls:best.className, len:bl, sample:best.innerText.slice(0,300)} : null;
        }""")
        print("最大纯文本叶子节点:", json.dumps(big, ensure_ascii=False))
        b.close()

if __name__ == "__main__":
    main()
