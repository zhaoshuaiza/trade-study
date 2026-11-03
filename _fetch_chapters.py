"""v7: 点开目录, 记录全部响应(含 content-type), dump 面板文本"""
import sys, json, time, socket, subprocess

VID = sys.argv[1] if len(sys.argv) > 1 else "72a327c0811e260b2g017333"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/_chapters_2002tw.json"
PORT = 9222
PROFILE = "E:/_edge_fresh"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def port_open(p):
    s = socket.socket(); s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", p)); s.close(); return True
    except Exception:
        return False


if not port_open(PORT):
    subprocess.Popen([EDGE, f"--remote-debugging-port={PORT}",
                      f"--user-data-dir={PROFILE}", "about:blank"])
    for _ in range(40):
        if port_open(PORT):
            break
        time.sleep(1)

from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    ctx = b.contexts[0]
    page = ctx.new_page()
    allres = []
    page.on("response", lambda r: allres.append((r.status, r.url, r.headers.get("content-type",""))))
    page.goto(f"https://weread.qq.com/web/reader/{VID}",
              wait_until="networkidle", timeout=60000)
    time.sleep(4)
    page.evaluate("""() => { const c=[...document.querySelectorAll('button,div[role=button]')].find(x=>(x.innerText||'').trim()==='目录'||(x.getAttribute('title')||'').includes('目录')); if(c)c.click(); }""")
    time.sleep(4)
    print("[全部响应 含 json/html]")
    for st,u,ct in allres:
        if ("json" in ct) or ("html" in ct) or (("chapter" in u) or ("book" in u) or ("catalog" in u) or ("reader" in u) and "svg" not in u):
            print(f"  {st} [{ct}] {u[:120]}")
    print("\n[body.innerText 片段]")
    txt = page.evaluate("() => document.body.innerText")
    # 找目录/章节相关行
    lines = [l.strip() for l in (txt or "").splitlines() if l.strip()]
    print("总行数", len(lines))
    for l in lines[:80]:
        print("  ", l[:60])
