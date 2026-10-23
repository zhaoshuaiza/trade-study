# -*- coding: utf-8 -*-
import os, sys, base64, re, json
from playwright.sync_api import sync_playwright

COOKIE=os.environ.get("WR_COOKIE")
READER=sys.argv[1] if len(sys.argv)>1 else "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
OUTDIR=sys.argv[2] if len(sys.argv)>2 else "steenbarger-2015-zh"
os.makedirs(OUTDIR, exist_ok=True)

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

def xhtml_to_text(x):
    m=re.search(r"<title>(.*?)</title>", x, re.S)
    title=m.group(1).strip() if m else ""
    x2=re.sub(r"<style[\s\S]*?</style>","",x)
    x2=re.sub(r"<script[\s\S]*?</script>","",x2)
    blocks=re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2)
    paras=[]
    for b in blocks:
        t=re.sub(r"<[^>]+>","",b)
        t=re.sub(r"&nbsp;"," ",t)
        t=re.sub(r"\s+"," ",t).strip()
        if t: paras.append(t)
    return title, "\n\n".join(paras)

captured={}
for fn in os.listdir(OUTDIR):
    if re.match(r"\d{4}\.html$", fn):
        n=int(fn[:4]); captured[n]=open(os.path.join(OUTDIR,fn),encoding="utf-8").read()

def save(n,x):
    title,text=xhtml_to_text(x)
    open(os.path.join(OUTDIR,"%04d.html"%n),"w",encoding="utf-8").write(x)
    open(os.path.join(OUTDIR,"%04d.txt"%n),"w",encoding="utf-8").write((title+"\n\n"+text) if title else text)

new_count=[0]
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
            if x and n not in captured:
                captured[n]=x; save(n,x); new_count[0]+=1
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(6000)

    def cat_visible():
        return pg.evaluate("""()=>{
            const it=document.querySelector('.readerCatalog_list_item');
            if(!it) return false;
            const r=it.getBoundingClientRect();
            return r.width>10 && r.height>5 && r.y>-50 && r.y<900;
        }""")
    def open_cat():
        pg.evaluate("""()=>{const el=[...document.querySelectorAll('.readerControls_item.catalog')][0]; if(el){const r=el.getBoundingClientRect(); window.__c={x:r.x+r.width/2,y:r.y+r.height/2};}}""")
        c=pg.evaluate("()=>window.__c")
        if c: pg.mouse.click(c['x'],c['y']); pg.wait_for_timeout(1600)

    open_cat()
    if not cat_visible(): open_cat()
    total=pg.evaluate("()=>document.querySelectorAll('.readerCatalog_list_item').length")
    print("TOC total:", total, "pre-captured:", len(captured), flush=True)

    for i in range(total):
        if not cat_visible():
            open_cat()
        box=pg.evaluate("""(idx)=>{
            const items=document.querySelectorAll('.readerCatalog_list_item');
            if(idx>=items.length) return null;
            const e=items[idx];
            e.scrollIntoView({block:'center'});
            const r=e.getBoundingClientRect();
            if(!(r.width>10&&r.height>5)) return null;
            return {x:r.x+r.width/2, y:r.y+r.height/2, t:(e.innerText||'').trim().slice(0,30)};
        }""", i)
        if not box:
            continue
        before=set(captured)
        pg.mouse.click(box['x'],box['y'])
        pg.wait_for_timeout(1600)
        if (i+1)%15==0:
            print("progress %d/%d captured=%d" % (i+1,total,len(captured)), flush=True)
    pg.wait_for_timeout(2500)
    b.close()

print("FINAL captured:", len(captured), "max n:", max(captured) if captured else 0, flush=True)
meta=[]
for n in sorted(captured):
    x=captured[n]; title,_=xhtml_to_text(x)
    meta.append({"n":n,"title":title,"chars":len(x)})
json.dump(meta, open(os.path.join(OUTDIR,"_meta.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE ->", OUTDIR, flush=True)
