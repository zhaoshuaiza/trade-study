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
        pg.wait_for_timeout(4000)
        print("URL after load:", pg.url)
        # locate 开始阅读 precisely
        btns = pg.evaluate("""()=>{
            return [...document.querySelectorAll('*')].filter(e=>e.innerText&&e.innerText.trim()==='开始阅读').map(e=>({tag:e.tagName,cls:String(e.className).slice(0,60),pid:String(e.parentElement&&e.parentElement.className).slice(0,60)}));
        }""")
        print("开始阅读 elems:", json.dumps(btns,ensure_ascii=False))
        # real click
        try:
            pg.get_by_text("开始阅读", exact=True).first.click(timeout=8000, force=True)
            print("real click done")
        except Exception as e:
            print("real click err:", e)
        pg.wait_for_timeout(6000)
        print("URL after click:", pg.url)
        # scan for reader containers
        scan = pg.evaluate("""()=>{
            const res=[];
            document.querySelectorAll('[class*="reader"]').forEach(e=>{
                const t=(e.innerText||'').trim();
                if(t.length>50) res.push({cls:String(e.className).slice(0,70), len:t.length, sample:t.slice(0,120)});
            });
            return res.slice(0,8);
        }""")
        print("reader containers:", json.dumps(scan,ensure_ascii=False))
        # also check frames text
        fr = pg.frames
        print("frames:", len(fr))
        for f in fr:
            try:
                t=(f.evaluate("()=>document.body?document.body.innerText:''") or "")[:120]
                if t.strip(): print("  frame text:", t.replace("\n"," ")[:120])
            except: pass
        b.close()
if __name__=="__main__":
    main()
