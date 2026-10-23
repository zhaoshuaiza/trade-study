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
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(8000)
    print("URL:",pg.url)
    res=pg.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('*').forEach(e=>{
            const t=(e.innerText||'').trim();
            if(t.length>600 && t.includes('都希格') && !String(e.className).includes('outline')){
                out.push({cls:String(e.className).slice(0,65), len:t.length, childN:e.children.length});
            }
        });
        out.sort((a,b)=>a.len-b.len);
        return out.slice(0,6);
    }""")
    print("chapter containers:", json.dumps(res,ensure_ascii=False,indent=1))
    b.close()
