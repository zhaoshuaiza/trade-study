# -*- coding: utf-8 -*-
"""探测 res.weread.qq.com 的 TAR 静态内容端点（与 /web/book/chapter 不同主机，可能未受限流）。"""
import os, time, json, io, re, base64
os.environ["NO_PROXY"] = "127.0.0.1,localhost"; os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
BOOKID = "3300129049"
UIDS = [90, 89, 8, 20, 30, 60, 88, 91, 92, 4, 5]

JS = """async (argv) => {
  const [bk, uids] = argv;
  const out = [];
  for (const u of uids) {
    const url = 'https://res.weread.qq.com/wrco/tar_CB_' + bk + '_' + u;
    try {
      const r = await fetch(url, {credentials:'include'});
      const buf = await r.arrayBuffer();
      const b = new Uint8Array(buf);
      let head = '';
      for (let i = 0; i < Math.min(24, b.length); i++) head += b[i].toString(16).padStart(2,'0');
      out.push([u, r.status, b.length, head]);
    } catch(e) { out.push([u, 'ERR', 0, String(e).slice(0,60)]); }
  }
  return out;
}"""

SAVE_JS = """async (argv) => {
  const [bk, u] = argv;
  const url = 'https://res.weread.qq.com/wrco/tar_CB_' + bk + '_' + u;
  const r = await fetch(url, {credentials:'include'});
  const buf = await r.arrayBuffer();
  const b = new Uint8Array(buf);
  let s = '';
  for (let i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
  return [r.status, b.length, btoa(s)];
}"""

def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]; page = ctx.pages[0]; page.bring_to_front()
        try: page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e: print("nav", str(e)[:60])
        time.sleep(7)
        for u, st, ln, head in page.evaluate(JS, [BOOKID, UIDS]):
            magic = "gzip" if head.startswith("1f8b") else ("tar/ustar" if "7573746172" in head else head[:16])
            print("uid %-4d status=%-4s len=%-8s magic=%s" % (u, st, ln, magic))
        # 把 uid 90 的完整内容存下来看结构
        st, ln, b64 = page.evaluate(SAVE_JS, [BOOKID, 90])
        raw = base64.b64decode(b64)
        print("save uid90:", st, ln, "magic", raw[:4].hex())
        with open("_tar_90.bin", "wb") as f:
            f.write(raw)

main()
