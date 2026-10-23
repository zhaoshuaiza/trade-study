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
    ctx=b.new_context(viewport={"width":1280,"height":900})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    print("on load: bodylen=", pg.evaluate("()=>document.body.innerText.length"))
    # open catalog, click item 4
    pg.evaluate("""()=>{const el=[...document.querySelectorAll('.readerControls_item.catalog')][0]; if(el){const r=el.getBoundingClientRect(); window.__c={x:r.x+r.width/2,y:r.y+r.height/2};}}""")
    c=pg.evaluate("()=>window.__c"); pg.mouse.click(c['x'],c['y']); pg.wait_for_timeout(1500)
    box=pg.evaluate("""()=>{const items=document.querySelectorAll('.readerCatalog_list_item'); const e=items[4]; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2,t:(e.innerText||'').trim()};}""")
    print("click item4:", box['t'])
    pg.mouse.click(box['x'],box['y']); pg.wait_for_timeout(3000)
    print("after click: URL=", pg.url[-40:])
    print("bodylen=", pg.evaluate("()=>document.body.innerText.length"))
    txt=pg.evaluate("()=>document.body.innerText")
    print("has 序言 content:", "时间是一个事件" in txt)
    print("sample:", txt[:300].replace("\n"," | "))
    # find the content container
    cont=pg.evaluate("""()=>{
        let best=null,bl=0;
        document.querySelectorAll('div,section,article').forEach(e=>{
            const t=(e.innerText||'');
            if(t.length>bl){bl=t.length;best=e;}
        });
        return {cls:String(best.className).slice(0,60), len:bl};
    }""")
    print("max container:", cont)
    b.close()
