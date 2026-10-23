# -*- coding: utf-8 -*-
import os, json
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
    reqs=[]; resps=[]
    def on_req(r):
        u=r.url
        if "weread" in u or "qpic" in u:
            reqs.append(u)
    def on_resp(r):
        u=r.url
        # capture content-type of weread responses
        try: ct=r.headers.get("content-type","")
        except: ct=""
        if "weread.qq.com" in u:
            resps.append((r.status, ct, u[:160]))
    pg.on("request", on_req)
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(9000)
    # Trigger chapter navigation by clicking 下一页 a few times to force content loads
    for _ in range(4):
        pg.keyboard.press("ArrowRight")
        pg.wait_for_timeout(1500)
    pg.wait_for_timeout(3000)
    print("=== distinct request URLs containing 'content' or 'tar' or 'chapter' ===")
    seen=set()
    for u in reqs:
        if any(k in u.lower() for k in ["content","tar","chapter","wrco","wrepub"]):
            if u not in seen:
                seen.add(u); print(u[:200])
    print("\n=== responses (weread) count:", len(resps))
    seen2=set()
    for st,ct,u in resps:
        if u not in seen2:
            seen2.add(u); print(st, ct[:30], u[:160])
    b.close()
