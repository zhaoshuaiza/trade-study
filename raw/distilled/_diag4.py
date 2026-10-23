# -*- coding: utf-8 -*-
import os, base64, re
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
def decode_body(body):
    if not body or len(body)<=33: return None
    if body[32]!="P": return None
    try: return base64.b64decode(body[33:]).decode("utf-8","ignore")
    except: return None
captured={}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":1000})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    def on_resp(r):
        u=r.url
        if "/web/book/chapter/e_" in u:
            m=re.search(r"e_(\d+)$",u)
            if m:
                try: x=decode_body(r.body().decode("utf-8","ignore"))
                except: x=None
                if x: captured[int(m.group(1))]=x
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    # click 下一章 with real mouse, 3 times
    for k in range(3):
        btn=pg.evaluate("""()=>{const el=[...document.querySelectorAll('*')].find(e=>(e.textContent||'').trim()==='下一章'&&e.children.length===0); if(!el) return null; const r=el.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2};}""")
        print("btn:", btn)
        if not btn: break
        pg.mouse.click(btn['x'],btn['y'])
        pg.wait_for_timeout(2500)
        print("after click %d: URL=...%s captured=%s" % (k, pg.url[-30:], sorted(captured)))
    b.close()
