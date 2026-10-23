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

captured=[]
def on_response(resp):
    u=resp.url
    if "wrco" in u or "chapterContent" in u or ("/web/book/" in u and "content" in u.lower()) or "wrepub" in u:
        captured.append((resp.status, u[:300]))

def main():
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--no-sandbox"])
        ctx=b.new_context()
        ctx.add_cookies(parse_cookies(COOKIE))
        pg=ctx.new_page()
        pg.on("response", on_response)
        # Try direct chapter navigation
        pg.goto(READER+"?chapterUid=2", timeout=30000)
        pg.wait_for_timeout(4000)
        # Is there 开始阅读?
        has_start = pg.evaluate("""()=>{
            const els=[...document.querySelectorAll('*')].filter(e=>e.innerText&&e.innerText.trim()==='开始阅读');
            return els.length;
        }""")
        print("开始阅读 buttons:", has_start)
        if has_start:
            pg.evaluate("""()=>{const els=[...document.querySelectorAll('*')].filter(e=>e.innerText&&e.innerText.trim()==='开始阅读');els[0].click();}""")
            pg.wait_for_timeout(6000)
        # try scroll to trigger chapter loads
        for _ in range(6):
            pg.mouse.wheel(0, 1500)
            pg.wait_for_timeout(1200)
        pg.wait_for_timeout(3000)
        # Dump text containers
        info=pg.evaluate("""()=>{
            let best=null,bl=0;
            document.querySelectorAll('div,p,section,article').forEach(e=>{
                const t=(e.innerText||'').trim(); if(t.length>bl){bl=t.length;best=e;}
            });
            const fr=window.frames;
            return {maxlen:bl, tag:best?best.tagName:null, cls:best?String(best.className).slice(0,80):null,
                    frames:fr.length, sample:best?best.innerText.slice(0,300):''};
        }""")
        print("DOM:", json.dumps(info, ensure_ascii=False))
        print("\n=== captured network (%d) ===" % len(captured))
        for st,u in captured[:40]:
            print(st, u)
        b.close()

if __name__=="__main__":
    main()
