"""最小连接诊断: 逐步打印, 定位 connect/cdp.send/goto 的卡点。"""
import os, time, sys
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

def log(s): print("[%6.1f] %s" % (time.time()-T0, s), flush=True)

T0 = time.time()
log("import ok")
with sync_playwright() as p:
    log("connect_over_cdp...")
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    log("connected; contexts=%d" % len(b.contexts))
    ctx = b.contexts[0]
    log("ctx.pages=%d" % len(ctx.pages))
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    log("got page; new_cdp_session...")
    cdp = ctx.new_cdp_session(page)
    log("cdp session; Network.enable...")
    cdp.send("Network.enable")
    log("Network.enable done; clearBrowserCache...")
    cdp.send("Network.clearBrowserCache")
    log("clearBrowserCache done; setCacheDisabled...")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    log("setCacheDisabled done; goto...")
    try:
        page.goto("https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
                  wait_until="domcontentloaded", timeout=30000)
        log("goto done")
    except Exception as e:
        log("goto ERR: " + str(e)[:80])
    time.sleep(5)
    log("sleep done; evaluating title...")
    try:
        t = page.evaluate("() => document.title")
        log("title=%r" % t)
    except Exception as e:
        log("eval ERR: " + str(e)[:80])
    b.close()
    log("closed")
