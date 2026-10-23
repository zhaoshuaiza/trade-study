# -*- coding: utf-8 -*-
"""
WeRead full-book extractor (final version).

Method (reverse-engineered):
- Reader fetches chapter content from /web/book/chapter/e_N
- Response body = 32-hex-char prefix + 1 separator char + base64(byte-stream chunk)
- Chunks concatenate in fetch order; documents end with </html>
- Navigation: real mouse clicks on the readerFooter_button (下一章) walk the book
  sequentially (membership session reads paid chapters, TOC jump may be locked)
- Requires a VALID cookie (wr_vid/wr_skey). Script aborts if session expired.

Usage:
  python _fetch_full.py <reader_url> <outdir>
"""
import os, sys, re, json, base64, hashlib
from playwright.sync_api import sync_playwright

COOKIE = os.environ.get("WR_COOKIE")
READER = sys.argv[1] if len(sys.argv) > 1 else "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else "out"
MAXCH = int(os.environ.get("MAXCH", "200"))
os.makedirs(OUTDIR, exist_ok=True)
LOG = open(os.path.join(OUTDIR, "_fetch.log"), "a", encoding="utf-8")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.write(s + "\n"); LOG.flush()

def parse_cookies(s):
    out = []
    for kv in s.split(";"):
        kv = kv.strip()
        if "=" not in kv: continue
        k, v = kv.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(), "domain": ".weread.qq.com", "path": "/"})
    return out

def decode_chunk(body):
    """body = 32-hex + 1 sep char + base64. Return decoded bytes or None."""
    if not body or len(body) < 40: return None
    if not re.match(r"^[0-9A-Fa-f]{32}$", body[:32]): return None
    b64 = body[33:]
    try:
        return base64.b64decode(b64)
    except Exception:
        return None

def clean_text(xhtml):
    x = re.sub(r"<style[\s\S]*?</style>", "", xhtml)
    x = re.sub(r"<script[\s\S]*?</script>", "", x)
    blocks = re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x)
    paras = []
    for b in blocks:
        t = re.sub(r"<[^>]+>", "", b)
        t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
        t = re.sub(r"[ \t\r\f\v]+", " ", t).strip()
        if t: paras.append(t)
    return "\n\n".join(paras)

def doc_title(xhtml):
    m = re.search(r"<title>(.*?)</title>", xhtml, re.S)
    return m.group(1).strip() if m else ""

seen_hashes = set()
docs = []  # list of (title, xhtml, text)

def feed(stream_bytes):
    """Split accumulated stream at </html> boundaries; keep tail as incomplete."""
    global stream_tail
    buf = stream_tail + stream_bytes
    parts = buf.split(b"</html>")
    stream_tail = parts[-1]  # incomplete tail kept for next feed
    new_docs = 0
    for p in parts[:-1]:
        doc = p + b"</html>"
        # cut at last <?xml or <html start to drop leading junk
        h = hashlib.md5(doc).hexdigest()
        if h in seen_hashes: continue
        seen_hashes.add(h)
        x = doc.decode("utf-8", "ignore")
        title = doc_title(x)
        text = clean_text(x)
        if len(text) < 2: continue
        docs.append((title, x, text))
        new_docs += 1
    return new_docs

if not COOKIE:
    log("ERROR: WR_COOKIE env not set"); sys.exit(1)

stream_tail = b""
window = []  # bytes captured since last navigation

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1280, "height": 1000})
    ctx.add_cookies(parse_cookies(COOKIE))
    pg = ctx.new_page()

    def on_resp(r):
        u = r.url
        if "/web/book/chapter/e_" in u:
            try: raw = r.body().decode("utf-8", "ignore")
            except Exception: return
            d = decode_chunk(raw)
            if d is not None: window.append(d)
    pg.on("response", on_resp)
    pg.goto(READER, timeout=30000)
    pg.wait_for_timeout(7000)

    # login check (in page context)
    chk = pg.evaluate("""async ()=>{
        const r = await fetch('https://weread.qq.com/web/shelf/sync',{credentials:'include'});
        const j = await r.json();
        return {err: j.errCode, n: (j.books||[]).length};
    }""")
    log("login check:", chk)
    if chk.get("err") != 0:
        log("SESSION EXPIRED - aborting. 请更新 cookie。")
        b.close(); sys.exit(2)

    def next_chapter_click():
        """Scroll to bottom, real-mouse-click 下一章. Returns True if clicked."""
        pg.evaluate("()=>window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(500)
        btn = pg.evaluate("""()=>{
            const el=[...document.querySelectorAll('*')].find(e=>
                (e.textContent||'').trim()==='下一章' && e.children.length===0);
            if(!el) return null;
            el.scrollIntoView({block:'center'});
            const r=el.getBoundingClientRect();
            return {x:r.x+r.width/2, y:r.y+r.height/2};
        }""")
        if not btn: return False
        pg.mouse.click(btn["x"], btn["y"])
        return True

    # initial window (current chapter on load)
    pg.wait_for_timeout(2500)
    n0 = feed(b"".join(window)); window.clear()
    log("initial docs:", len(docs), "new:", n0)

    stall = 0
    for i in range(MAXCH):
        clicked = next_chapter_click()
        if not clicked:
            log("no 下一章 button at step", i, "- end of book")
            break
        pg.wait_for_timeout(2600)
        n = feed(b"".join(window)); window.clear()
        if n == 0:
            stall += 1
            if stall >= 3:
                log("3 consecutive clicks with no new docs - stopping at step", i)
                break
        else:
            stall = 0
            last = docs[-1]
            log("step %d: +doc #%d %r (%d chars)" % (i, len(docs), last[0], len(last[2])))
        if (i + 1) % 10 == 0:
            log("progress: step %d, docs %d" % (i + 1, len(docs)))
    pg.wait_for_timeout(1500)
    b.close()

# save everything
meta = []
for k, (title, x, text) in enumerate(docs):
    with open(os.path.join(OUTDIR, "%04d.html" % k), "w", encoding="utf-8") as f: f.write(x)
    with open(os.path.join(OUTDIR, "%04d.txt" % k), "w", encoding="utf-8") as f:
        f.write((title + "\n\n" + text) if title else text)
    meta.append({"k": k, "title": title, "chars": len(text)})
json.dump(meta, open(os.path.join(OUTDIR, "_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log("DONE:", len(docs), "docs ->", OUTDIR)
