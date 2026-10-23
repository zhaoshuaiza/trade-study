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
        # capture content responses
        cont=[]
        def on_resp(r):
            u=r.url
            if "wrco" in u or "chapterContent" in u or "wrepub" in u or ("content" in u and "weread.qq.com" in u):
                cont.append((r.status,u[:280]))
        pg.on("response", on_resp)
        pg.goto(READER+"?chapterUid=2", timeout=30000)
        pg.wait_for_timeout(5000)
        # hide overlay(s)
        hidden = pg.evaluate("""()=>{
            let n=0;
            document.querySelectorAll('*').forEach(e=>{
                const c=String(e.className||'');
                if(c.includes('outline_book_detail')||c.includes('ai_outline')||c.includes('wr_outline')){e.style.display='none';n++;}
            });
            return n;
        }""")
        print("hidden overlay elems:", hidden)
        pg.wait_for_timeout(2000)
        # find reader content containers (text > 200, not back-cover)
        res = pg.evaluate("""()=>{
            const out=[];
            document.querySelectorAll('div,p,section,article,span').forEach(e=>{
                const t=(e.innerText||'').trim();
                if(t.length>200){
                    out.push({cls:String(e.className).slice(0,70), len:t.length, sample:t.slice(0,160)});
                }
            });
            out.sort((a,b)=>b.len-a.len);
            return out.slice(0,6);
        }""")
        print("reader text blocks:", json.dumps(res,ensure_ascii=False))
        print("\n=== content network responses ===")
        for s,u in cont[:30]: print(s,u)
        b.close()
if __name__=="__main__":
    main()
