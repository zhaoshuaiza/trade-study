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
            if not m: return
            n=int(m.group(1))
            try: body=r.body().decode("utf-8","ignore")
            except: return
            x=decode_body(body)
            if x and n not in captured: captured[n]=x
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(8000)
    # scroll down many times
    for i in range(60):
        pg.mouse.wheel(0, 5000)
        pg.wait_for_timeout(700)
    pg.wait_for_timeout(2000)
    b.close()
print("captured via scroll:", len(captured), "max n:", max(captured) if captured else 0)
print(sorted(captured))
