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
    # find all elements containing the page's first sentence, report full text length
    res=pg.evaluate("""()=>{
        const key='查尔斯';
        const out=[];
        document.querySelectorAll('div,p,section,article,span').forEach(e=>{
            const t=(e.innerText||'');
            if(t.includes(key)){
                out.push({cls:String(e.className).slice(0,60), len:t.length, hasTitle:t.includes('为何纪律约束不起作用'), sample:t.slice(0,100)});
            }
        });
        out.sort((a,b)=>b.len-a.len);
        return out.slice(0,8);
    }""")
    print("elements containing chapter text:", json.dumps(res,ensure_ascii=False,indent=1))
    # list candidate containers by class name containing render/preRender/chapter
    res2=pg.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('[class*="render"],[class*="chapter"],[class*="Chapter"],[class*="content"]').forEach(e=>{
            const t=(e.innerText||'').trim();
            if(t.length>100) out.push({cls:String(e.className).slice(0,70), len:t.length});
        });
        out.sort((a,b)=>b.len-a.len);
        return out.slice(0,12);
    }""")
    print("\nrender/chapter containers:", json.dumps(res2,ensure_ascii=False,indent=1))
    b.close()
