"""单次精准探测: 直接 POST 微信读书正文分片接口 e_0, 看 status/len。
1 个请求, 不翻页不跳章, 不加重限流。结果写文件便于查看。"""
import os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
P0 = {"b": "33d32010813ab98e8g019623", "c": "861322a025a8613985ec87a", "r": 9865881, "st": 0,
      "ps": "326321207aaf520cg0171a3", "pc": "e5932ec07aaf520cg018303", "sc": 0, "s": "5290312e"}

PROBE = """async (p0) => {
  try {
    const r = await fetch('/web/book/chapter/e_0', {method:'POST', credentials:'include',
      headers:{'Content-Type':'application/json;charset=UTF-8'},
      body: JSON.stringify({...p0, ct: Math.floor(Date.now()/1000)})});
    const t = await r.text();
    return [r.status, t.length, t.slice(0,60)];
  } catch (e) { return ['ERR', String(e).slice(0,80), '']; }
}"""

def main():
    out = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            out.append("[nav] " + str(e)[:60])
        time.sleep(8)
        try:
            st, ln, head = page.evaluate(PROBE, P0)
        except Exception as e:
            st, ln, head = "EVAL_ERR", str(e)[:80], ""
        out.append("探测结果: status=%s len=%s head=%r" % (st, ln, head))
        b.close()
    line = "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), " | ".join(out))
    print(line)
    with open(os.path.join(ROOT, "_probe_limit.log"), "a", encoding="utf-8") as f:
        f.write(line + "\n")

if __name__ == "__main__":
    main()
