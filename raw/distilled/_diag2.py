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
    pg.evaluate("""()=>{const el=[...document.querySelectorAll('.readerControls_item.catalog')][0]; if(el){const r=el.getBoundingClientRect(); window.__c={x:r.x+r.width/2,y:r.y+r.height/2};}}""")
    c=pg.evaluate("()=>window.__c"); pg.mouse.click(c['x'],c['y']); pg.wait_for_timeout(1600)
    # find scrollable container among catalog ancestors
    info=pg.evaluate("""()=>{
        const item=document.querySelectorAll('.readerCatalog_list_item')[50];
        if(!item) return {err:'no item50'};
        // walk up to find scroller
        let cur=item.parentElement, scroller=null;
        while(cur){ if(cur.scrollHeight>cur.clientHeight+10){scroller=cur;break;} cur=cur.parentElement; }
        const r0=item.getBoundingClientRect();
        let before=null;
        if(scroller) before={cls:String(scroller.className).slice(0,50), st:scroller.scrollTop, sh:scroller.scrollHeight, ch:scroller.clientHeight};
        item.scrollIntoView({block:'center'});
        const r1=item.getBoundingClientRect();
        let after=null;
        if(scroller) after={st:scroller.scrollTop};
        return {rectBefore:{y:Math.round(r0.y),h:Math.round(r0.height)}, rectAfter:{y:Math.round(r1.y),h:Math.round(r1.height)}, scroller:before, afterScrollTop:after, itemText:(item.innerText||'').trim().slice(0,30)};
    }""")
    print(json.dumps(info,ensure_ascii=False,indent=1))
    # also dump item 50 outerHTML attrs
    html=pg.evaluate("""()=>{const it=document.querySelectorAll('.readerCatalog_list_item')[50]; return it?it.outerHTML.slice(0,400):'none';}""")
    print("item50 html:", html)
    b.close()
