# -*- coding: utf-8 -*-
import os, json
from playwright.sync_api import sync_playwright
COOKIE=os.environ.get("WR_COOKIE")
READER="https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
def parse_cookies(s):
    out=[]
    for kv in s.split(";"):
        kv=kv.strip()
        if "=" not in kv: continue
        k,v=kv.split("=",1)
        out.append({"name":k.strip(),"value":v.strip(),"domain":".weread.qq.com","path":"/"})
    return out
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":900})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    hdrs=[]
    def on_req(r):
        u=r.url
        if "/web/book/chapter/" in u:
            hdrs.append({"url":u,"headers":dict(r.headers)})
    pg.on("request", on_req)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(9000)
    for _ in range(2):
        pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(1500)
    pg.wait_for_timeout(1500)
    for h in hdrs[:2]:
        print("URL:", h["url"])
        for k,v in h["headers"].items():
            print("  %s: %s" % (k, v[:120]))
        print()
    b.close()
