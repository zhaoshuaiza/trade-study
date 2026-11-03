#!/usr/bin/env python3
# 登录态下抓取《从躺椅上操作：交易心理学》(vid 72a327c0811e260b2g017333) 章节清单
import json, os, time, socket, subprocess, sys
from playwright.sync_api import sync_playwright

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PROFILE = "E:/_edge_fresh"
PORT = 9222
VID = "72a327c0811e260b2g017333"
OUT = "E:/Work Buddy/交易学习/raw/distilled/steenbarger-2002-tradepsych-zh/_chapters.json"

def po(p):
    s = socket.socket(); s.settimeout(0.5)
    try: s.connect(("127.0.0.1", p)); s.close(); return True
    except: return False

def start_edge():
    if po(PORT): return True
    subprocess.Popen([EDGE, f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}", "about:blank"])
    for _ in range(40):
        if po(PORT): return True
        time.sleep(1)
    return False

def main():
    if not start_edge():
        print("START_EDGE_FAIL"); sys.exit(1)
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = b.contexts[0]
        pg = ctx.new_page()
        pg.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(4000)
        body = pg.evaluate("()=>document.body.innerText") or ""
        print("HOMEPAGE_LOGIN?", ("我的书架" in body) or ("登录" not in body), "| has登录Btn?", "登录" in body)
        # 尝试 1: chapterInfos API (带登录 cookie)
        for ep in [
            f"https://weread.qq.com/web/book/chapterInfos?bookId={VID}",
            f"https://weread.qq.com/web/book/getChapterInfos?bookId={VID}",
        ]:
            try:
                res = pg.evaluate("""(url) => fetch(url,{credentials:'include'}).then(r=>r.text()).catch(e=>'ERR:'+e)""", ep)
                print("API", ep.split('/')[-1], "->", repr(res[:200]))
            except Exception as e:
                print("API_ERR", ep, e)
        # 尝试 2: bookDetail INITIAL_STATE
        pg.goto(f"https://weread.qq.com/web/bookDetail/{VID}", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(3000)
        st = pg.evaluate("""() => {
            const s=document.body.innerHTML.indexOf('window.__INITIAL_STATE__');
            return s;
        }""")
        print("bookDetail INITIAL_STATE idx:", st)
        # 尝试 3: reader 目录面板
        pg.goto(f"https://weread.qq.com/web/reader/{VID}", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(5000)
        # 点目录
        for sel in ["button:has-text('目录')", "[class*=catalog]", "[class*=toc]", "text=目录"]:
            try:
                el = pg.query_selector(sel)
                if el:
                    try: el.click(timeout=2000)
                    except: pg.evaluate("(e)=>e.click()", el)
                    print("clicked", sel); break
            except Exception: pass
        pg.wait_for_timeout(3000)
        cat = pg.evaluate("""() => {
            const items=[...document.querySelectorAll('[class*=chapterItem],[class*=catalogItem],.readerCatalog li,a[href*=chapterUid]')];
            return items.slice(0,5).map(i=>({t:(i.innerText||'').trim().slice(0,30), href:(i.getAttribute('href')||'').slice(-30)}));
        }""")
        print("CATALOG_ITEMS_SAMPLE:", json.dumps(cat, ensure_ascii=False))
        # 也抓整个 catalog 文本
        cattext = pg.evaluate("""() => {
            const c=document.querySelector('[class*=catalog],.readerCatalog');
            return c? c.innerText.slice(0,400): 'NO_CATALOG_EL';
        }""")
        print("CATALOG_TEXT:", repr(cattext[:400]))
        pg.screenshot(path="E:/Work Buddy/交易学习/_reader_2002tw.png", full_page=False)
        print("SHOT saved")
    print("DONE")

if __name__ == "__main__":
    main()
