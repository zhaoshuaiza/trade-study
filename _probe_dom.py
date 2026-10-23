#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DOM 文本直抽探测: 导航到指定章节锚点,抽取渲染出的最大文本节点,
确认是否拿到整章正文(绕开已退化的网络分片组装)。
"""
import os, re, time, sys, argparse
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = {
    "2015": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
    "2002": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
}

# uid 89 的锚点(k 参数) —— "57项交易成功所需的最佳实践"
UID89_K = "764323602597647966b7a1c"


def extract_biggest(page):
    """在页面里找出 textContent 最长的元素(排除 UI 外壳),返回其 (tag,cls,text)。"""
    return page.evaluate(r"""() => {
        const UI = ["登录","目录","设置","书架","笔记","翻页","上一页","下一页","夜间","字号","亮度","全文","想法"];
        let best = null, bestLen = 0;
        const all = document.querySelectorAll('*');
        for (const el of all) {
            const t = (el.textContent || '');
            if (t.length <= bestLen) continue;
            let isUI = false;
            for (const w of UI) { if (t.indexOf(w) >= 0 && t.length < 400) { isUI = true; break; } }
            if (isUI) continue;
            bestLen = t.length;
            best = el;
        }
        if (!best) return {tag:null, cls:null, len:0, head:null, markers:{}};
        const head = (best.textContent || '').replace(/\s+/g,' ').slice(0, 220);
        const tx = best.textContent || '';
        const markers = {};
        for (const m of ['#1','#6','#7','#22','#23','#57','最佳实践','第1项','第22项','第23项']) {
            markers[m] = tx.indexOf(m) >= 0;
        }
        return {tag: best.tagName, cls: (best.className||'').toString().slice(0,60), len: tx.length, head, markers};
    }""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="2015", choices=["2015", "2002"])
    ap.add_argument("--k", default=UID89_K, help="阅读器 k 锚点(章节)")
    ap.add_argument("--wait", type=float, default=9.0, help="导航后等待渲染秒数")
    args = ap.parse_args()

    base = BOOK[args.book]
    target = "%s?k=%s" % (base, args.k)

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
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
            print("[cdp] cache cleared")
        except Exception as e:
            cdp = None
            print("[cdp] fail", str(e)[:70])

        print("[nav] ->", target[-50:])
        page.goto(target, wait_until="domcontentloaded", timeout=60000)
        time.sleep(args.wait)
        chap = page.evaluate("() => (document.body.innerText||'').split('\\n').slice(0,8).join(' | ')")
        print("[render] body 前几行:", chap[:200])
        info = extract_biggest(page)
        print("[biggest] tag=%s cls=%s len=%d" % (info["tag"], info["cls"], info["len"]))
        print("[biggest] head:", info["head"])
        print("[biggest] markers:", info["markers"])
        print("[url] now:", page.url[-60:])
        b.close()


if __name__ == "__main__":
    main()
