#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断 Canvas hook 为何拿不到内容"""
import os, sys, time, argparse
from playwright.sync_api import sync_playwright

HOOK = r"E:/Work Buddy/tools/weread-exporter-main/weread_exporter/hook.js"
VID = "33d32010813ab98e8g019623"
K89 = "764323602597647966b7a1c"


def probe(page, tag):
    try:
        info = page.evaluate("""() => {
            const o = {};
            o.url = location.href;
            o.title = document.title;
            const W = window.canvasContextHandler;
            o.hasHook = !!W;
            o.complete = W ? W.data.complete : null;
            o.mdLen = W ? (W.data.markdown || '').length : -1;
            o.mdHead = W ? (W.data.markdown || '').slice(0, 120) : '';
            o.canvases = document.getElementsByTagName('canvas').length;
            o.ctxPatched = HTMLCanvasElement.prototype.getContext.toString().length < 200
                           ? HTMLCanvasElement.prototype.getContext.toString() : 'native-ish';
            o.patchedFlag = (HTMLCanvasElement.prototype.getContext.toString().indexOf('origGetContext')>=0);
            const fb = document.getElementsByClassName('readerFooter_button');
            o.footerCount = fb.length;
            o.footerText = fb.length ? fb[0].innerText : '(none)';
            o.appHtmlLen = document.body.innerHTML.length;
            const w = document.querySelector('.wr_reader_wrapper, .readerChapterContent, canvas');
            o.hasReaderRoot = !!w;
            o.bodyText = (document.body.innerText||'').slice(0,160);
            return o;
        }""")
    except Exception as e:
        print("[%s] evaluate 失败: %s" % (tag, str(e)[:120]))
        return
    print("---- %s ----" % tag)
    for k in ["url", "title", "hasHook", "complete", "mdLen", "canvases",
              "patchedFlag", "footerCount", "footerText", "appHtmlLen",
              "hasReaderRoot"]:
        print("   %-14s = %s" % (k, info.get(k)))
    print("   bodyText      = %s" % repr(info.get("bodyText"))[:170])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="slash", choices=["slash", "query", "plain"])
    ap.add_argument("--inject", action="store_true")
    ap.add_argument("--wait", type=float, default=12)
    a = ap.parse_args()

    hook_src = open(HOOK, encoding="utf-8").read()
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        if a.inject:
            ctx.add_init_script(hook_src +
                                "\n;window.canvasContextHandler = canvasContextHandler;")
            print("[已注入 hook.js via add_init_script]")
        page = ctx.new_page()

        if a.mode == "slash":
            url = "https://weread.qq.com/web/reader/%sk%s" % (VID, K89)
        elif a.mode == "query":
            url = "https://weread.qq.com/web/reader/%s?k=%s" % (VID, K89)
        else:
            url = "https://weread.qq.com/web/reader/%s" % VID
        print("[goto]", url)
        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print("[goto 失败]", str(e)[:150])
        time.sleep(a.wait)
        probe(page, "t=%.0fs" % a.wait)
        time.sleep(6)
        probe(page, "t=%.0fs" % (a.wait + 6))
        try:
            page.close()
        except Exception:
            pass
        try:
            b.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
