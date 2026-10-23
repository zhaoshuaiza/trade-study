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
    # open catalog
    clicked = pg.evaluate("""()=>{
        const el=[...document.querySelectorAll('.readerControls_item.catalog')][0];
        if(!el) return 'no catalog btn';
        const r=el.getBoundingClientRect();
        window.__cat={x:r.x+r.width/2,y:r.y+r.height/2};
        return 'ok';
    }""")
    print("catalog btn:", clicked)
    if clicked=="ok":
        c=pg.evaluate("()=>window.__cat")
        pg.mouse.click(c['x'],c['y'])
        pg.wait_for_timeout(2500)
        # dump TOC structure
        toc=pg.evaluate("""()=>{
            const res=[];
            // candidate containers
            const roots=document.querySelectorAll('[class*="readerCatalog"]');
            let root=roots[0];
            if(root){
                const items=root.querySelectorAll('*');
                // find clickable chapter-like entries: have text, reasonable size
                const seen=[];
                root.querySelectorAll('div,p,li,span,a').forEach(e=>{
                    const t=(e.innerText||'').trim();
                    const r=e.getBoundingClientRect();
                    if(t.length>0 && t.length<60 && r.width>20 && r.height>8){
                        seen.push({cls:String(e.className).slice(0,45), text:t, x:Math.round(r.x), y:Math.round(r.y), scrollH: root.scrollHeight, clientH: root.clientHeight});
                    }
                });
                return {scrollH:root.scrollHeight, clientH:root.clientHeight, count:seen.length, sample:seen.slice(0,15)};
            }
            return {roots:roots.length};
        }""")
        print(json.dumps(toc,ensure_ascii=False,indent=1))
    b.close()
