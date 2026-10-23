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
        cont=[]
        def on_resp(r):
            u=r.url
            if any(k in u for k in ["wrco","chapterContent","wrepub"]) or ("content" in u and "weread.qq.com" in u):
                cont.append((r.status,u[:300]))
        pg.on("response", on_resp)
        pg.goto(READER, timeout=30000)
        pg.wait_for_timeout(5000)
        # find the clickable ancestor with non-zero box containing 开始阅读
        target = pg.evaluate("""()=>{
            const els=[...document.querySelectorAll('*')].filter(e=>e.innerText&&e.innerText.includes('开始阅读'));
            let best=null;
            for(const e of els){
                const r=e.getBoundingClientRect();
                if(r.width>5&&r.height>5){
                    if(!best||(r.width*r.height)>(best.w*best.h)) best={x:r.x,y:r.y,w:r.width,h:r.height,cls:String(e.className).slice(0,50)};
                }
            }
            return best;
        }""")
        print("target box:", json.dumps(target,ensure_ascii=False))
        if target:
            cx=target['x']+target['w']/2
            cy=target['y']+target['h']/2
            pg.mouse.move(cx,cy)
            pg.mouse.click(cx,cy)
            print("clicked at", cx, cy)
        pg.wait_for_timeout(7000)
        print("URL:", pg.url)
        res = pg.evaluate("""()=>{
            const out=[];
            document.querySelectorAll('div,p,section,article').forEach(e=>{
                const t=(e.innerText||'').trim();
                if(t.length>300){
                    const c=String(e.className);
                    if(!c.includes('outline')&&!c.includes('ai_outline')&&!c.includes('readerCatalog')&&!c.includes('flyleaf')&&!c.includes('Cover'))
                        out.push({cls:c.slice(0,55), len:t.length, sample:t.slice(0,160)});
                }
            });
            out.sort((a,b)=>b.len-a.len);
            return out.slice(0,5);
        }""")
        print("reader body blocks:", json.dumps(res,ensure_ascii=False))
        print("=== network ===")
        for s,u in cont[:20]: print(s,u)
        b.close()
if __name__=="__main__":
    main()
