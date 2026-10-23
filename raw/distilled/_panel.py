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
    # get all readerControls_item with positions
    items=pg.evaluate("""()=>{
        return [...document.querySelectorAll('.readerControls_item')].map(e=>{
            const r=e.getBoundingClientRect();
            return {cls:String(e.className).slice(0,50), x:Math.round(r.x+r.width/2), y:Math.round(r.y+r.height/2)};
        });
    }""")
    print("controls:", json.dumps(items,ensure_ascii=False))
    # click the 2nd one (settings/Aa)
    if len(items)>1:
        it=items[1]
        pg.mouse.click(it['x'],it['y'])
        print("clicked control#2 at",it)
        pg.wait_for_timeout(2500)
        pg.screenshot(path="_panel_shot.png")
        # dump panel texts
        panel=pg.evaluate("""()=>{
            const out=[];
            document.querySelectorAll('div,span,button,li,p').forEach(e=>{
                const t=(e.innerText||'').trim();
                const r=e.getBoundingClientRect();
                if(t && t.length<40 && r.width>20 && r.height>10 && (t.includes('滚动')||t.includes('单页')||t.includes('翻页')||t.includes('模式')||t.includes('上下')))
                    out.push({cls:String(e.className).slice(0,50),text:t,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});
            });
            return out.slice(0,20);
        }""")
        print("mode-related texts:", json.dumps(panel,ensure_ascii=False,indent=1))
    b.close()
