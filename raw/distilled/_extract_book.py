# -*- coding: utf-8 -*-
import os, sys, base64, re, json
from playwright.sync_api import sync_playwright

COOKIE=os.environ.get("WR_COOKIE")
READER=sys.argv[1] if len(sys.argv)>1 else "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
OUTDIR=sys.argv[2] if len(sys.argv)>2 else "steenbarger-2015-zh"
MAXP=170  # max next-page presses
WAIT=700

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
    try:
        raw=base64.b64decode(body[33:])
        return raw.decode("utf-8","ignore")
    except Exception:
        return None

def xhtml_to_text(x):
    # extract title + body text, dropping style/css and tags
    m=re.search(r"<title>(.*?)</title>", x, re.S)
    title=m.group(1).strip() if m else ""
    # remove style/script
    x2=re.sub(r"<style[\s\S]*?</style>","",x)
    x2=re.sub(r"<script[\s\S]*?</script>","",x2)
    # split into paragraphs by <p> or <div> or line breaks
    # keep paragraph breaks
    blocks=re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2)
    paras=[]
    for b in blocks:
        t=re.sub(r"<[^>]+>","",b)
        t=re.sub(r"&nbsp;"," ",t)
        t=re.sub(r"\s+"," ",t).strip()
        if t: paras.append(t)
    return title, "\n\n".join(paras)

os.makedirs(OUTDIR, exist_ok=True)
captured={}

with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":900})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg=ctx.new_page()
    def on_resp(r):
        u=r.url
        if "/web/book/chapter/e_" in u:
            m=re.search(r"e_(\d+)$", u)
            if not m: return
            n=int(m.group(1))
            try: body=r.body().decode("utf-8","ignore")
            except: return
            x=decode_body(body)
            if x and n not in captured:
                captured[n]=x
    pg.on("response", on_resp)
    pg.goto(READER,timeout=30000)
    pg.wait_for_timeout(8000)
    # ensure scroll/normal mode so ArrowRight = next chapter
    # press next page many times
    for i in range(MAXP):
        before=len(captured)
        pg.keyboard.press("ArrowRight")
        pg.wait_for_timeout(WAIT)
        if len(captured)==before and i>3:
            # maybe reached end; try a couple more then break
            pass
    # a final settle
    pg.wait_for_timeout(2000)
    b.close()

print("captured chapters:", len(captured))
# save each
meta=[]
for n in sorted(captured):
    x=captured[n]
    title, text=xhtml_to_text(x)
    fn=os.path.join(OUTDIR,"%04d.html"%n)
    with open(fn,"w",encoding="utf-8") as f:
        f.write(x)
    # also text
    tfn=os.path.join(OUTDIR,"%04d.txt"%n)
    with open(tfn,"w",encoding="utf-8") as f:
        f.write((title+"\n\n"+text) if title else text)
    meta.append({"n":n,"title":title,"chars":len(text)})
with open(os.path.join(OUTDIR,"_meta.json"),"w",encoding="utf-8") as f:
    json.dump(meta,f,ensure_ascii=False,indent=1)
print("saved to", OUTDIR)
for m in meta[:10]:
    print(m)
