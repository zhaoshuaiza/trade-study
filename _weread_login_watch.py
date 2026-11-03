#!/usr/bin/env python3
# 后台看守：拉起可见 Edge，停在微信读书登录页，循环刷新二维码，
# 一旦检测到 wr_skey 登录态即自动退出（会话已写入 E:/_edge_fresh profile）。
import time, base64, re, os, sys
from playwright.sync_api import sync_playwright

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PROFILE = "E:/_edge_fresh"
PORT = 9222
OUT = "E:/Work Buddy/交易学习/_weread_qr.png"
LOG = "E:/Work Buddy/交易学习/_weread_login_watch.log"

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S") + " " + msg + "\n")
    print(msg, flush=True)

def extract_qr(page):
    return page.evaluate("""() => {
        try {
            const imgs=[...document.querySelectorAll('img')];
            const q=imgs.find(i=>(i.src||'').startsWith('data:image') && i.naturalWidth>60 && i.naturalWidth<400);
            if(q && q.src.startsWith('data:image')) return q.src;
        } catch(e){}
        try {
            const cv=document.querySelector('canvas');
            if(cv){ const d=cv.toDataURL('image/png'); if(d && d.startsWith('data:image')) return d; }
        } catch(e){}
        return null;
    }""")

def save_uri(uri, out):
    m = re.match(r'data:image/(\w+);base64,(.+)', uri)
    if not m: return False
    data = base64.b64decode(m.group(2))
    open(out, "wb").write(data)
    return True

def is_logged_in(page):
    try:
        ck = page.evaluate("() => document.cookie")
        if "wr_skey" in (ck or ""): return True
        # 也看 body 是否还停在登录态
        txt = page.evaluate("() => document.body.innerText || ''")
        if "我的书架" in txt or "微信读书书城" not in txt and "扫码登录" not in txt:
            return "wr_skey" in (ck or "")
        return False
    except Exception:
        return False

def main():
    open(LOG, "w", encoding="utf-8").close()
    log("launch edge ...")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            executable_path=EDGE,
            args=[f"--user-data-dir={PROFILE}",
                  f"--remote-debugging-port={PORT}",
                  "--no-first-run", "--no-default-browser-check",
                  "--window-size=480,720"],
        )
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        page.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        # 点击登录按钮弹出二维码
        for sel in ["text=登录", "button:has-text('登录')", "[class*=loginBtn]"]:
            try:
                el = page.query_selector(sel)
                if el:
                    el.click(timeout=2000); log(f"clicked {sel}"); break
            except Exception:
                pass
        time.sleep(2)
        log("watching for QR + login ...")
        last_save = 0
        for t in range(240):  # 最多 ~20 分钟
            # 刷新二维码
            uri = extract_qr(page)
            if uri and (time.time() - last_save > 20):
                if save_uri(uri, OUT):
                    last_save = time.time()
                    if t % 6 == 0:
                        log(f"QR refreshed ({os.path.getsize(OUT)} bytes)")
            if is_logged_in(page):
                log("LOGGED_IN detected -> wr_skey present")
                # 再存一张当前 QR 占位（无所谓）
                try:
                    page.screenshot(path="E:/Work Buddy/交易学习/_weread_loggedin.png", fonts=False)
                except Exception:
                    pass
                browser.close()
                return
            time.sleep(5)
        log("TIMEOUT: 20min passed, closing")
        browser.close()

if __name__ == "__main__":
    main()
