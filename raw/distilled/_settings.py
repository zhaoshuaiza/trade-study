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
    ctx=b.new_context(viewport={"width":1280,"height":800})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    # dump reader control buttons (sidebar)
    ctrls=pg.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('[class*="readerControls"] [class*="item"], [class*="reader_control"], [class*="control_item"], [class*="icon"]').forEach(e=>{
            const r=e.getBoundingClientRect();
            if(r.width>5&&r.height>5) out.push({cls:String(e.className).slice(0,55), x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height), text:(e.innerText||'').slice(0,20).trim()});
        });
        return out.slice(0,25);
    }""")
    print("controls:", json.dumps(ctrls,ensure_ascii=False,indent=1))
    b.close()
