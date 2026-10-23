"""决定性诊断: 真实翻页, 看正文分片 e_ 的实际响应体是否非空。
区分两种可能: (A) 真限流(所有 e_ body 为空)  (B) 监控写死参数过期(假限流, 真实翻页能拿到正文)。
1 次翻页 = 1 次真实章节请求, 极温和。"""
import os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"

def main():
    seen = {}
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def on_resp(resp):
            u = resp.url
            if "/web/book/chapter/e_" in u:
                idx = u.split("e_")[-1].split("?")[0]
                try:
                    body = resp.body()
                    seen[idx] = (resp.status, len(body), body[:40] if body else b"")
                except Exception as e:
                    seen[idx] = ("BODYERR", str(e)[:50], b"")

        page.on("response", on_resp)
        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(10)  # 等首章加载(e_0..e_N 真实请求)
        # 真实翻一页 (阅读器发下一个有效章节请求)
        try:
            page.keyboard.press("ArrowRight")
        except Exception:
            pass
        time.sleep(8)
        b.close()

    print("捕获到的 e_ 分片 (idx: status, len, head):")
    if not seen:
        print("  (无 e_ 请求 — 阅读器未发起正文加载)")
    for k in sorted(seen):
        st, ln, hd = seen[k]
        print("  e_%s: status=%s len=%s head=%r" % (k, st, ln, hd[:30] if isinstance(hd,(bytes,bytearray)) else hd))
    nonempty = [k for k in seen if isinstance(seen[k][1], int) and seen[k][1] > 50]
    print("非空分片数:", len(nonempty), "->", ("未限流, 可抓取" if nonempty else "疑似真限流(全部空)"))

if __name__ == "__main__":
    main()
