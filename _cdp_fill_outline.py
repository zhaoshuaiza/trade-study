#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补齐缺失章节的大纲：单章逐个请求 /web/book/outline（批量请求时空返的章节，单请求可能返回）。

只对缺大纲的 uid 发请求，每章间隔 2.5s；合并回 _outline_full.json 并重生成 _outline.md。
"""
import os, re, time, json, argparse

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = {
    "2015": {"reader": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
             "bookId": "3300129049",
             "out": os.path.join(HERE, "raw/distilled/steenbarger-2015-zh")},
    "2002": {"reader": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
             "bookId": "3300220786",
             "out": os.path.join(HERE, "raw/distilled/steenbarger-2002-zh")},
}

JS = """async (argv) => {
  const [bk, uid] = argv;
  const r = await fetch('/web/book/outline', {method:'POST', credentials:'include',
    headers:{'Content-Type':'application/json;charset=UTF-8'},
    body: JSON.stringify({bookId: bk, chapterUids: [uid]})});
  return await r.text();
}"""


def regen_md(out_dir, outlines, titles, book):
    md = ["# 《%s》全书大纲（接口原生数据）\n" % book]
    total = 0
    for uid in sorted(outlines):
        items = outlines[uid]
        if not items:
            continue
        md.append("\n## 第%s章 uid=%d  %s\n" % (uid, uid, titles.get(uid, "")))
        for it in items:
            lvl = int(it.get("level", 3) or 3)
            txt = (it.get("text") or "").strip()
            if not txt:
                continue
            total += len(txt)
            pref = "  " * max(0, lvl - 2)
            md.append("%s- %s" % (pref, txt))
    mp = os.path.join(out_dir, "_outline.md")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    return total, os.path.getsize(mp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=list(BOOKS))
    ap.add_argument("--pause", type=float, default=2.5)
    args = ap.parse_args()
    cfg = BOOKS[args.book]
    chs = json.load(io_open(os.path.join(cfg["out"], "_chapters.json")))
    titles = {c["chapterUid"]: c.get("title", "") for c in chs}
    jpath = os.path.join(cfg["out"], "_outline_full.json")
    outlines = json.load(io_open(jpath)) if os.path.exists(jpath) else {}
    outlines = {int(k): v for k, v in outlines.items()}

    todo = [c["chapterUid"] for c in chs if c["chapterUid"] not in outlines or not outlines.get(c["chapterUid"])]
    print("[%s] 已有 %d 章大纲，待补 %d 章: %s" % (args.book, len(outlines), len(todo), todo))

    got = 0
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]; page = ctx.pages[0]; page.bring_to_front()
        try:
            page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(6)
        for uid in todo:
            txt = None
            for attempt in (1, 2):
                try:
                    txt = page.evaluate(JS, [cfg["bookId"], uid])
                    if txt and "itemsArray" in txt:
                        break
                except Exception as e:
                    print("  [uid %d fail %d] %s" % (uid, attempt, str(e)[:60]))
                time.sleep(2.0)
            n = 0; chars = 0
            try:
                d = json.loads(txt or "{}")
                for it in d.get("itemsArray", []):
                    if it.get("chapterUid") == uid and it.get("items"):
                        outlines[uid] = it["items"]; n = 1
                        chars = sum(len(x.get("text", "")) for x in it["items"])
            except Exception as e:
                print("  [uid %d json fail] %s" % (uid, str(e)[:60]))
            print("  uid %-4d %-28s -> %s (%d 字)" % (uid, titles.get(uid, "")[:28], "OK" if n else "空", chars))
            got += n
            time.sleep(args.pause)

    with open(jpath, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in outlines.items()}, f, ensure_ascii=False, indent=1)
    total, size = regen_md(cfg["out"], outlines, titles, args.book)
    print("[saved] %s (%d bytes) | _outline.md %d bytes, 大纲总字数 %d" % (jpath, os.path.getsize(jpath), size, total))
    print("[done] %s: 新得 %d 章，现有大纲 %d / %d 章" % (args.book, got, len(outlines), len(chs)))


def io_open(p):
    import io
    return io.open(p, encoding="utf-8")


if __name__ == "__main__":
    main()
