#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""尝试把同一批次的分片按 e_0..e_N 拼接后解码，验证能否还原完整 XHTML。"""
import os, time, base64, re

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"


def b64(s):
    s = s.strip()
    pad = (-len(s)) % 4
    try:
        return base64.b64decode(s + "=" * pad)
    except Exception:
        try:
            return base64.b64decode(s + "=" * pad, validate=False)
        except Exception:
            return None


def group_records(recs, gap=0.9):
    groups, cur = [], []
    seen = set()
    last = None
    for t, idx, body in recs:
        if last is not None and (t - last) > gap:
            if cur:
                groups.append(cur)
            cur, seen = [], set()
        if idx in seen:
            if cur:
                groups.append(cur)
            cur, seen = [], set()
        cur.append((idx, body))
        seen.add(idx)
        last = t
    if cur:
        groups.append(cur)
    return groups


def main():
    recs = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]

        def on_resp(r):
            last = r.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in r.url or not last.startswith("e_"):
                return
            try:
                idx = int(last.split("_")[1])
            except Exception:
                return
            try:
                recs.append((time.time(), idx, r.body()))
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
            time.sleep(0.22)
        time.sleep(4)
        b.close()

    print("responses:", len(recs))
    groups = group_records(recs)
    print("groups:", len(groups))
    total_docs = 0
    for gi, g in enumerate(groups):
        parts = sorted(g, key=lambda x: x[0])
        idxs = [i for i, _ in parts]
        joined = b"".join(b for _, b in parts)
        # 方式A: 先拼 base64 再解
        txtA = (b64(joined[33 * 0:]) or b"").decode("utf-8", "ignore") if False else None
        concat = b"".join(p[33:] for _, p in parts)
        rawA = b64(concat)
        txtA = rawA.decode("utf-8", "ignore") if rawA else ""
        docsA = len(re.findall(r"<html[ >]", txtA))
        # 方式B: 各片单独解码后拼接字节流
        rawB = b"".join([b64(p[33:]) or b"" for _, p in parts])
        txtB = rawB.decode("utf-8", "ignore")
        docsB = len(re.findall(r"<html[ >]", txtB))
        print("[group %d] idxs=%s lens=%s | concatDocs=%d eachDocs=%d | headA=%r"
              % (gi, idxs, [len(p) for _, p in parts], docsA, docsB, txtA[:60]))
        total_docs += max(docsA, docsB)
    print("total docs recovered:", total_docs)


if __name__ == "__main__":
    main()
