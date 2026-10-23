#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扫描宽范围偏移量，找出每个响应的真实载荷起点。"""
import os, time, base64, gzip, zlib

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def try_offset(body, off):
    try:
        raw = base64.b64decode(body[off:], validate=True)
    except Exception:
        return None
    if len(raw) < 8:
        return None
    for name, dec in (("plain", lambda r: r),
                      ("gzip", gzip.decompress),
                      ("zlib", zlib.decompress)):
        try:
            t = dec(raw).decode("utf-8", "ignore")
        except Exception:
            continue
        if ("<?xml" in t) or ("<html" in t) or ("<!DOCTYPE" in t):
            return (off, name, t)
    return None


def scan(body):
    for off in range(0, 96):
        got = try_offset(body, off)
        if got:
            return got
    return None


def main():
    samples = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                samples.append((last, r.body()))
            except Exception:
                pass

        page.on("response", on_resp)
        page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        time.sleep(9)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        for _ in range(60):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(0.2)
        time.sleep(4)
        b.close()

    print("responses:", len(samples))
    ok = 0
    offs = {}
    for last, body in samples:
        got = scan(body)
        if got:
            ok += 1
            offs["%s@%d" % (got[1], got[0])] = offs.get("%s@%d" % (got[1], got[0]), 0) + 1
            print("OK  %-5s len=%-7d -> %s@%d  %r" % (last, len(body), got[1], got[0], got[2][:50]))
        else:
            print("BAD %-5s len=%-7d head=%r" % (last, len(body), body[:44].decode("latin1")))
    print("ok=%d/%d  patterns=%s" % (ok, len(samples), offs))


if __name__ == "__main__":
    main()
