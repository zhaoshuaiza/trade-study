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
    ctx=b.new_context(viewport={"width":1280,"height":1000})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    # check top bar for 登录 link vs avatar
    top=pg.evaluate("""()=>{
        const t=document.body.innerText;
        return {hasLoginLink: t.includes('登录'), hasLogout: t.includes('退出'),
                snippet: t.slice(0,150)};
    }""")
    print(top)
    # check via API in page context: /web/shelf/sync
    r=pg.evaluate("""async ()=>{
        const resp=await fetch('https://weread.qq.com/web/shelf/sync',{method:'GET',credentials:'include'});
        const j=await resp.json();
        return {errCode:j.errCode, books:(j.books||[]).length};
    }""")
    print("in-page shelf/sync:", r)
    b.close()
