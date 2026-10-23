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
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":900})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    seen=[]
    def on_resp(r):
        u=r.url
        if "/web/book/chapter/" in u or "login" in u or "passport" in u:
            seen.append((r.status,u[:120]))
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)
    # is login page?
    title=pg.title()
    bodylen=pg.evaluate("()=>document.body.innerText.length")
    hasreader=pg.evaluate("()=>document.querySelectorAll('.readerCatalog_list_item').length")
    print("page title:", title, "| bodylen:", bodylen, "| list_item on load:", hasreader)
    # open catalog
    pg.evaluate("""()=>{const el=[...document.querySelectorAll('.readerControls_item.catalog')][0]; if(el){const r=el.getBoundingClientRect(); window.__c={x:r.x+r.width/2,y:r.y+r.height/2};}}""")
    c=pg.evaluate("()=>window.__c")
    print("cat btn coords:", c)
    if c: pg.mouse.click(c['x'],c['y']); pg.wait_for_timeout(1500)
    total=pg.evaluate("()=>document.querySelectorAll('.readerCatalog_list_item').length")
    print("TOC items after open:", total)
    # click item index 4
    box=pg.evaluate("""()=>{const items=document.querySelectorAll('.readerCatalog_list_item'); if(items.length<5) return null; const e=items[4]; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2,t:(e.innerText||'').trim().slice(0,30)};}""")
    print("item4 box:", box)
    seen.clear()
    if box:
        pg.mouse.click(box['x'],box['y'])
        pg.wait_for_timeout(3000)
    print("responses after click item4:")
    for s,u in seen: print("  ",s,u)
    # current url + whether list still open
    print("URL after click:", pg.url)
    print("list_item after click:", pg.evaluate("()=>document.querySelectorAll('.readerCatalog_list_item').length"))
    pg.screenshot(path="_diag.png")
    b.close()
