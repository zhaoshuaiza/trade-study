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
    # 1) Does body.innerText include the chapter title text at all?
    print("body.innerText len:", pg.evaluate("()=>document.body.innerText.length"))
    print("contains 都希格:", pg.evaluate("()=>document.body.innerText.includes('都希格')"))
    print("contains 为何纪律约束:", pg.evaluate("()=>document.body.innerText.includes('为何纪律约束')"))
    # 2) Find the single element with max innerText length, excluding outline/catalog
    res=pg.evaluate("""()=>{
        let best=null, bl=0;
        const skip=(c)=>['outline','Outline','readerCatalog','flyleaf','Cover','review','Review','dialog','header','footer','control','Control'].some(k=>c.includes(k));
        document.querySelectorAll('div,p,section,article').forEach(e=>{
            const t=(e.innerText||'').trim();
            const c=String(e.className);
            if(!skip(c) && t.length>bl){ bl=t.length; best=e; }
        });
        return {len:bl, cls:best?String(best.className).slice(0,70):null,
                sample:best?best.innerText.slice(0,200):''};
    }""")
    print("BEST text block:", json.dumps(res,ensure_ascii=False,indent=1))
    # 3) canvas / frames / shadow
    print("canvas count:", pg.evaluate("()=>document.querySelectorAll('canvas').length"))
    for i,f in enumerate(pg.frames):
        try:
            t=f.evaluate("()=>document.body?document.body.innerText:''")
            print("frame",i,f.url[:50],"len",len(t),"has都希格",'都希格' in t)
        except Exception as e:
            print("frame",i,"err")
    b.close()
