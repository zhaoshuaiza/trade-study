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
def decode_chunk(body):
    if not body or len(body)<=33: return None
    if body[32]!="P": return None
    try: return base64.b64decode(body[33:])
    except: return None
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":1000})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    stream=[]  # ordered (url, bytes)
    def on_resp(r):
        u=r.url
        if "/web/book/chapter/e_" in u:
            try: raw=r.body()
            except: return
            b64=raw.decode("utf-8","ignore")
            data=decode_chunk(b64)
            stream.append((u.rsplit("/",1)[-1], data))
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    stream.clear()  # discard initial load
    # navigate: click 下一章 twice
    for k in range(2):
        pg.evaluate("()=>window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(600)
        btn=pg.evaluate("""()=>{const el=[...document.querySelectorAll('*')].find(e=>(e.textContent||'').trim()==='下一章'&&e.children.length===0); if(!el) return null; el.scrollIntoView({block:'center'}); const r=el.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2};}""")
        if not btn: break
        pg.mouse.click(btn['x'],btn['y'])
        pg.wait_for_timeout(2500)
    print("stream after 2 next-chapter clicks:")
    full=b"".join(d for _,d in stream if d)
    print("total bytes:", len(full), "chunks:", [(u,len(d) if d else 0) for u,d in stream])
    txt=full.decode("utf-8","ignore")
    # strip tags for a peek
    t=re.sub(r"<style[\s\S]*?</style>","",txt)
    t=re.sub(r"<[^>]+>"," ",t)
    t=re.sub(r"\s+"," ",t)
    print("TEXT sample:", t[:500])
    b.close()
