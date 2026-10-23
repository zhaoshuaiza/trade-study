#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""探查页面 <head> 是否内嵌整本书正文(作为 JSON/变量),若有则解析提取。"""
import os, re, time, json, argparse
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = {
    "2015": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
    "2002": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="2015", choices=["2015", "2002"])
    ap.add_argument("--wait", type=float, default=12.0)
    args = ap.parse_args()

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
        page.goto(BOOK[args.book], wait_until="domcontentloaded", timeout=60000)
        time.sleep(args.wait)

        info = page.evaluate(r"""() => {
            const out = {};
            // 1) 所有 script 标签
            const scripts = Array.from(document.scripts);
            out.scriptCount = scripts.length;
            out.scriptLens = scripts.map(s => (s.textContent||'').length).sort((a,b)=>b-a).slice(0,8);
            // 2) 找包含正文的 script(含 'Text/chapter' 或 '最佳实践' 或 '<p')
            out.bigScripts = [];
            for (const s of scripts) {
                const t = s.textContent||'';
                if (t.length > 5000) {
                    out.bigScripts.push({
                        len: t.length,
                        hasChapter: t.indexOf('Text/chapter') >= 0,
                        hasBest: t.indexOf('最佳实践') >= 0,
                        hasPtag: t.indexOf('<p') >= 0,
                        hasXml: t.indexOf('<?xml') >= 0,
                        head: t.replace(/\s+/g,' ').slice(0,160)
                    });
                }
            }
            // 3) 是否某个 script 含完整 xhtml
            out.anyFullXhtml = scripts.some(s => (s.textContent||'').indexOf('<?xml') >= 0 && (s.textContent||'').indexOf('</html>') >= 0);
            return out;
        }""")
        print(json.dumps(info, ensure_ascii=False, indent=1))
        b.close()


if __name__ == "__main__":
    main()
