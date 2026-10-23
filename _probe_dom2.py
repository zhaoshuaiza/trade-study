#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""确认阅读器是否把整本书渲染进 DOM: 比较 innerText(可见) 与
各容器 textContent(全量),并对照目录计算覆盖。把最大容器全文落盘供分析。
"""
import os, re, time, json, argparse
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = {
    "2015": ("https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
             os.path.join(ROOT, "raw/distilled/steenbarger-2015-zh")),
    "2002": ("https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
             os.path.join(ROOT, "raw/distilled/steenbarger-2002-zh")),
}
UID89_K = "764323602597647966b7a1c"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="2015", choices=["2015", "2002"])
    ap.add_argument("--k", default=UID89_K)
    ap.add_argument("--wait", type=float, default=12.0)
    ap.add_argument("--out", default=None, help="落盘全文到此文件")
    args = ap.parse_args()

    base, out_dir = BOOK[args.book]
    target = "%s?k=%s" % (base, args.k)

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        try:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.enable")
            cdp.send("Network.clearBrowserCache")
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        except Exception:
            cdp = None
        page.goto(target, wait_until="domcontentloaded", timeout=60000)
        time.sleep(args.wait)

        diag = page.evaluate(r"""() => {
            const arr = [];
            document.querySelectorAll('*').forEach(el => {
                const t = (el.textContent||'');
                arr.push({tag: el.tagName, cls: (el.className||'').toString().slice(0,40), len: t.length});
            });
            arr.sort((a,b)=>b.len-a.len);
            const top = arr.slice(0,6);
            const inner = (document.body.innerText||'').length;
            return {top, inner};
        }""")
        print("[diag] innerText(可见)长度:", diag["inner"])
        print("[diag] 最长元素 top6:")
        for e in diag["top"]:
            print("   ", e["tag"], "|", e["cls"], "| len=", e["len"])

        full = page.evaluate(r"""() => {
            let best=null, bestLen=0;
            document.querySelectorAll('div,section,article,main').forEach(el=>{
                const t=(el.textContent||'');
                if (t.length>bestLen){bestLen=t.length; best=el;}
            });
            return best ? best.textContent : '';
        }""")
        print("[full] 最长DIV容器字符数:", len(full))
        toc_path = os.path.join(out_dir, "_toc.json")
        try:
            toc = json.load(open(toc_path, encoding="utf-8"))
        except Exception:
            toc = []
        hit = 0
        miss = []
        for t in toc:
            k = re.sub(r"[（(].*?[)）]", "", t.strip()).strip()
            if len(k) >= 2 and k in full:
                hit += 1
            else:
                miss.append(k)
        print("[coverage] 目录命中 %d/%d" % (hit, len(toc)))
        if miss:
            print("[coverage] 未命中样例:", miss[:15])
        for m in ["#1","#6","#22","#23","#57","第1项","最佳实践#1","最佳实践#23","小结"]:
            print("   marker %-12s : %s" % (m, m in full))
        if args.out:
            with open(args.out, "w", encoding="utf-8", newline="") as f:
                f.write(full)
            print("[write] 全文已落盘:", args.out, "len=", len(full))
        b.close()


if __name__ == "__main__":
    main()
