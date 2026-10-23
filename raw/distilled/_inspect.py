# -*- coding: utf-8 -*-
import os, json
from playwright.sync_api import sync_playwright

COOKIE = os.environ.get("WR_COOKIE")
READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"

def parse_cookies(s):
    out=[]
    for kv in s.split(";"):
        kv=kv.strip()
        if "=" not in kv: continue
        k,v=kv.split("=",1)
        out.append({"name":k.strip(),"value":v.strip(),"domain":".weread.qq.com","path":"/"})
    return out

def main():
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--no-sandbox"])
        ctx=b.new_context()
        ctx.add_cookies(parse_cookies(COOKIE))
        pg=ctx.new_page()
        pg.goto(READER, timeout=30000)
        pg.wait_for_timeout(5000)
        info = pg.evaluate("""()=>{
            const el=[...document.querySelectorAll('*')].find(e=>e.innerText&&e.innerText.trim()==='开始阅读');
            if(!el) return {found:false};
            const r=el.getBoundingClientRect();
            const cs=getComputedStyle(el);
            const par=el.parentElement;
            const pcs=par?getComputedStyle(par):null;
            return {found:true, rect:{x:r.x,y:r.y,w:r.width,h:r.height},
                    display:cs.display, visibility:cs.visibility, opacity:cs.opacity,
                    zIndex:cs.zIndex, pointerEvents:cs.pointerEvents,
                    parentCls:String(par&&par.className).slice(0,60), parentDisplay:pcs&&pcs.display,
                    parentVisibility:pcs&&pcs.visibility, parentOpacity:pcs&&pcs.opacity};
        }""")
        print(json.dumps(info,ensure_ascii=False,indent=2))
        b.close()
if __name__=="__main__":
    main()
