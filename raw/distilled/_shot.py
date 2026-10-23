# -*- coding: utf-8 -*-
import os
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
    ctx=b.new_context(viewport={"width":1280,"height":800})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    pg.screenshot(path="_reader_shot.png", full_page=False)
    # also dump localStorage keys
    ls=pg.evaluate("()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k).slice(0,80);}return o;}")
    print("localStorage keys:", list(ls.keys()))
    for k,v in ls.items():
        if 'outline' in k.lower() or 'ai' in k.lower() or 'reader' in k.lower() or 'read' in k.lower():
            print("  ",k,"=",v)
    b.close()
print("screenshot saved")
