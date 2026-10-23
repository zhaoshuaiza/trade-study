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
        # Walk up from the 开始阅读 text node to find first non-zero ancestor box
        info = pg.evaluate("""()=>{
            const el=[...document.querySelectorAll('*')].find(e=>e.innerText&&e.innerText.trim()==='开始阅读');
            if(!el) return {found:false};
            let cur=el, chain=[];
            for(let i=0;i<8 && cur;i++){
                const r=cur.getBoundingClientRect();
                chain.push({cls:String(cur.className).slice(0,45), x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)});
                cur=cur.parentElement;
            }
            // find first ancestor with box
            let clickable=null;
            for(const c of chain){
                if(c.w>5&&c.h>5){clickable=c;break;}
            }
            return {found:true, chain, clickable};
        }""")
        print(json.dumps(info,ensure_ascii=False,indent=1))
        if info.get("clickable"):
            c=info["clickable"]
            cx=c['x']+c['w']/2; cy=c['y']+c['h']/2
            pg.mouse.click(cx,cy)
            print("clicked ancestor at",cx,cy)
            pg.wait_for_timeout(7000)
            print("URL now:", pg.url)
            body=pg.evaluate("""()=>{
                const out=[];
                document.querySelectorAll('div,p,section,article').forEach(e=>{
                    const t=(e.innerText||'').trim();
                    if(t.length>300){const c=String(e.className);
                        if(!c.includes('outline')&&!c.includes('ai_outline')&&!c.includes('readerCatalog')&&!c.includes('flyleaf')&&!c.includes('Cover')&&!c.includes('review'))
                            out.push({cls:c.slice(0,50),len:t.length,sample:t.slice(0,140)});}
                });
                out.sort((a,b)=>b.len-a.len);return out.slice(0,5);
            }""")
            print("body:",json.dumps(body,ensure_ascii=False))
        b.close()
if __name__=="__main__":
    main()
