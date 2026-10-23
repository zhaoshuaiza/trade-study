#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证宽松解码器：不再要求分隔符必须是 P，并尝试 gzip。"""
import os, time, base64, gzip

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def flexible_decode(body):
    """返回 (offset, kind, text) 或 None。"""
    if not body or len(body) < 40:
        return None
    for off in (33, 32, 34):
        try:
            raw = base64.b64decode(body[off:])
        except Exception:
            continue
        try:
            t = raw.decode("utf-8", "ignore")
        except Exception:
            continue
        if ("<html" in t) or ("<?xml" in t) or ("<!DOCTYPE" in t):
            return (off, "plain", t)
        if t and len(t) > 20 and "<" in t and ">" in t:
            return (off, "textish", t)
        for gz in (gzip.decompress, lambda r: gzip.decompress(r[2:]) if False else None):
            pass
        try:
            g = gzip.decompress(raw)
            gt = g.decode("utf-8", "ignore")
            if "<" in gt:
                return (off, "gzip", gt)
        except Exception:
            pass
    return None


def main():
    results = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                body = r.body()
            except Exception:
                return
            sep = (body[32:33] or b"").decode("latin1")
            got = flexible_decode(body)
            results.append((last, len(body), sep, got[0] if got else None,
                            got[1] if got else None, (got[2][:60] if got else "")))

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        for _ in range(80):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(0.18)
        time.sleep(4)
        b.close()

    print("total chapter responses:", len(results))
    ok, bad = 0, 0
    kinds = {}
    for last, ln, sep, off, kind, head in results:
        if off is None:
            bad += 1
            print("  FAIL %-6s len=%-7d sep=%r head=%r" % (last, ln, sep, head[:40]))
        else:
            ok += 1
            kinds["%s@%d" % (kind, off)] = kinds.get("%s@%d" % (kind, off), 0) + 1
    print("ok=%d bad=%d" % (ok, bad))
    print("kinds:", kinds)


if __name__ == "__main__":
    main()
