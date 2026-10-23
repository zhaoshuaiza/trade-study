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
                cont.append((r.status,u[:280]))
        pg.on("response", on_resp)
        pg.goto(READER, timeout=30000)
        pg.wait_for_timeout(6000)
        # dispatch native click on 开始阅读
        clicked = pg.evaluate("""()=>{
            const el=[...document.querySelectorAll('*')].find(e=>e.innerText&&e.innerText.trim()==='开始阅读');
            if(!el) return 'no-el';
            el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));
            return 'dispatched';
        }""")
        print("click result:", clicked)
        pg.wait_for_timeout(6000)
        print("URL:", pg.url)
        res = pg.evaluate("""()=>{
            const out=[];
            document.querySelectorAll('div,p,section,article').forEach(e=>{
                const t=(e.innerText||'').trim();
                if(t.length>150){
                    const c=String(e.className);
                    if(!c.includes('outline')&&!c.includes('ai_outline'))
                        out.push({cls:c.slice(0,60), len:t.length, sample:t.slice(0,140)});
                }
            });
            out.sort((a,b)=>b.len-a.len);
            return out.slice(0,6);
        }""")
        print("reader text blocks (non-outline):", json.dumps(res,ensure_ascii=False))
        print("\n=== network ===")
        for s,u in cont[:30]: print(s,u)
        b.close()
if __name__=="__main__":
    main()
