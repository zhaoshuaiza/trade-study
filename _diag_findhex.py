#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在页内运行期状态里找 chapterUid -> k-hex 的映射, 取出 uid=1 的 hex。"""
import os, re, time, json
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
KNOWN = "764323602597647966b7a1c"  # uid89 的 hex(已知)


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        res = page.evaluate("""() => {
            const out = {found:false};
            // 遍历 window 顶层属性, 找包含已知 hex 的值
            for (const k of Object.keys(window)) {
                try {
                    const v = window[k];
                    const s = (typeof v === 'object' && v) ? JSON.stringify(v) : String(v);
                    if (s && s.indexOf('%s') >= 0) {
                        out.found = true; out.key = k; out.snippet = s.slice(0, 600); break;
                    }
                } catch(e){}
            }
            // 也试 __INITIAL_STATE__
            try { out.initial = JSON.stringify(window.__INITIAL_STATE__||{}).slice(0,300); } catch(e){ out.initial='ERR'; }
            return out;
        }""" % KNOWN)
        print(json.dumps(res, ensure_ascii=False, indent=1)[:2500])
        b.close()


if __name__ == "__main__":
    main()
