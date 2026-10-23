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
    ctx=b.new_context(viewport={"width":1280,"height":900})
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
    # count disabled TOC items
    pg.evaluate("""()=>{const el=[...document.querySelectorAll('.readerControls_item.catalog')][0]; if(el){const r=el.getBoundingClientRect(); window.__c={x:r.x+r.width/2,y:r.y+r.height/2};}}""")
    c=pg.evaluate("()=>window.__c"); pg.mouse.click(c['x'],c['y']); pg.wait_for_timeout(1600)
    cnt=pg.evaluate("""()=>{
        const items=[...document.querySelectorAll('.readerCatalog_list_item')];
        return {total:items.length, disabled:items.filter(e=>String(e.className).includes('disabled')).length,
                enabled:items.filter(e=>!String(e.className).includes('disabled')).length};
    }""")
    print("TOC:", cnt)
    # close catalog (click same button again)
    pg.mouse.click(c['x'],c['y']); pg.wait_for_timeout(1200)
    # find 下一章 button
    nav=pg.evaluate("""()=>{
        const els=[...document.querySelectorAll('*')].filter(e=>{
            const t=(e.textContent||'').trim();
            return (t==='下一章'||t==='上一章') && e.children.length===0;
        });
        return els.map(e=>{const r=e.getBoundingClientRect(); return {t:(e.textContent||'').trim(), cls:String(e.className).slice(0,40), x:Math.round(r.x+r.width/2), y:Math.round(r.y+r.height/2), w:Math.round(r.width)};});
    }""")
    print("nav buttons:", nav)
    # click 下一章 via JS
    seen_before=len(captured)
    r=pg.evaluate("""()=>{const el=[...document.querySelectorAll('*')].find(e=>(e.textContent||'').trim()==='下一章'&&e.children.length===0); if(el){el.click(); return 'clicked';} return 'notfound';}""")
    print("js click 下一章:", r)
    pg.wait_for_timeout(3000)
    print("URL:", pg.url[-50:])
    print("captured now:", sorted(captured))
    b.close()
