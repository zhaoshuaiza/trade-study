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
    pg.wait_for_timeout(6000)
    # click the isHorizontalReader toggle to switch to scroll mode
    pg.evaluate("""()=>{
        const el=[...document.querySelectorAll('.readerControls_item.isHorizontalReader')][0];
        const r=el.getBoundingClientRect();
        window.__c={x:r.x+r.width/2,y:r.y+r.height/2};
    }""")
    c=pg.evaluate("()=>window.__c")
    pg.mouse.click(c['x'],c['y'])
    print("toggled layout at",c)
    pg.wait_for_timeout(6000)
    pg.screenshot(path="_scroll_shot.png")
    # now find chapter text container (exclude outline/catalog/etc)
    res=pg.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('div,p,section,article').forEach(e=>{
            const t=(e.innerText||'').trim();
            const c=String(e.className);
            if(t.length>500 && !c.includes('outline') && !c.includes('Outline') && !c.includes('readerCatalog') && !c.includes('flyleaf') && !c.includes('review') && !c.includes('Review') && !c.includes('dialog'))
                out.push({cls:c.slice(0,60), len:t.length, sample:t.slice(0,120)});
        });
        out.sort((a,b)=>b.len-a.len);
        return out.slice(0,6);
    }""")
    print("scroll-mode text blocks:", json.dumps(res,ensure_ascii=False,indent=1))
    b.close()
