#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""排除样式表分片(e_2)后，按序号拼接正文分片并解码。"""
import os, time, base64, re

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"

CSS_PREFIX = ("Lyoq", "IyAg", "LmZy", "QGlt")  # '/*' 等样式表/资源起始特征


def b64(s):
    s = s.strip()
    pad = (-len(s)) % 4
    try:
        return base64.b64decode(s + "=" * pad)
    except Exception:
        return None


def group_records(recs, gap=0.9):
    groups, cur, seen, last = [], [], set(), None
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
    total = 0
    for gi, g in enumerate(groups):
        parts = sorted(g, key=lambda x: x[0])
        # 剔除样式表分片（不能独立拼进正文流）
        body_parts = [(i, b) for i, b in parts
                      if not any(b[33:].decode("latin1", "ignore").startswith(pfx) for pfx in CSS_PREFIX)]
        if not body_parts:
            continue
        for hdr in (33, 32, 34):
            concat = b"".join(p[hdr:] for _, p in body_parts)
            raw = b64(concat)
            if not raw:
                continue
            txt = raw.decode("utf-8", "ignore")
            docs = re.findall(r"<\?xml[\s\S]*?</html>", txt)
            if docs:
                chars = sum(len(d) for d in docs)
                total += len(docs)
                print("[g%d] idxs=%s hdr=%d -> docs=%d chars=%d first=%r"
                      % (gi, [i for i, _ in body_parts], hdr, len(docs), chars, docs[0][:60]))
                break
        else:
            print("[g%d] idxs=%s -> 解码失败" % (gi, [i for i, _ in body_parts]))
    print("TOTAL DOCS:", total)


if __name__ == "__main__":
    main()
