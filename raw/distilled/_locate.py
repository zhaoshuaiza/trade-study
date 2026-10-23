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
    # light DOM check
    print("body.innerText has 都希格:", pg.evaluate("()=>document.body.innerText.includes('都希格')"))
    print("body.innerText has 为何纪律约束:", pg.evaluate("()=>document.body.innerText.includes('为何纪律约束')"))
    # canvas check
    print("canvas count:", pg.evaluate("()=>document.querySelectorAll('canvas').length"))
    # frames check
    for i,f in enumerate(pg.frames):
        try:
            t=f.evaluate("()=>document.body?document.body.innerText:''")
            print("frame %d url=%s len=%d has都希格=%s" % (i,f.url[:60],len(t),'都希格' in t))
        except Exception as e:
            print("frame %d err %s" % (i,str(e)[:50]))
    # shadow roots check
    sr=pg.evaluate("""()=>{
        let n=0;
        const walk=(el)=>{ if(el.shadowRoot){n++; walk(el.shadowRoot);} [...el.children].forEach(walk); };
        walk(document.body);
        return n;
    }""")
    print("shadow roots:", sr)
    b.close()
