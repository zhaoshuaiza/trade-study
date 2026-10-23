#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抓取全量章节大纲(/web/book/outline),落盘 json + markdown。

每批 8 个 chapterUid,失败自动重试一次。
"""
import os, re, time, json, argparse

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

BOOKS = {
    "2015": {"reader": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
             "bookId": "3300129049",
             "out": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "raw/distilled/steenbarger-2015-zh")},
    "2002": {"reader": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
             "bookId": "3300220786",
             "out": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "raw/distilled/steenbarger-2002-zh")},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=list(BOOKS))
    ap.add_argument("--maxuid", type=int, default=200)
    args = ap.parse_args()
    cfg = BOOKS[args.book]
    os.makedirs(cfg["out"], exist_ok=True)

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        try:
            page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(7)

        # 1) 取全部章节元信息 -> uid/title/wordCount
        meta = page.evaluate(
            """async (bk) => {
              const r = await fetch('/web/book/chapterInfos', {method:'POST', credentials:'include',
                headers:{'Content-Type':'application/json;charset=UTF-8'},
                body: JSON.stringify({bookIds:[bk]})});
              return await r.text();
            }""", cfg["bookId"])
        try:
            j = json.loads(meta)
            chs = j["data"][0]["updated"]
        except Exception as e:
            print("[ chapterInfos fail]", str(e)[:80], meta[:200])
            return
        with open(os.path.join(cfg["out"], "_chapters.json"), "w", encoding="utf-8") as f:
            json.dump(chs, f, ensure_ascii=False, indent=1)
        uids = [c["chapterUid"] for c in chs]
        titles = {c["chapterUid"]: c.get("title", "") for c in chs}
        print("[chapters] %d 章, uid %d..%d, 总字数 %d" %
              (len(chs), uids[0], uids[-1], sum(c.get("wordCount", 0) for c in chs)))

        # 2) 分批取大纲
        js = """async (argv) => {
          const [bk, uids] = argv;
          const r = await fetch('/web/book/outline', {method:'POST', credentials:'include',
            headers:{'Content-Type':'application/json;charset=UTF-8'},
            body: JSON.stringify({bookId: bk, chapterUids: uids})});
          return await r.text();
        }"""
        outlines = {}
        B = 8
        for i in range(0, len(uids), B):
            batch = uids[i:i + B]
            txt = None
            for attempt in (1, 2):
                try:
                    txt = page.evaluate(js, [cfg["bookId"], batch])
                    d = json.loads(txt)
                    if "itemsArray" in d or isinstance(d, dict):
                        break
                except Exception as e:
                    print("  [batch %d-%d fail %d] %s" % (batch[0], batch[-1], attempt, str(e)[:60]))
                time.sleep(2.0)
            if not txt:
                print("  [skip]", batch)
                continue
            try:
                d = json.loads(txt)
            except Exception:
                print("  [json fail]", batch, txt[:120])
                continue
            for it in d.get("itemsArray", []):
                uid = it.get("chapterUid")
                if it.get("items"):
                    outlines[uid] = it["items"]
            print("  [outline] uid %d-%d -> 已得 %d 章" % (batch[0], batch[-1], len(outlines)))
            time.sleep(1.0)

        jpath = os.path.join(cfg["out"], "_outline_full.json")
        with open(jpath, "w", encoding="utf-8") as f:
            json.dump(outlines, f, ensure_ascii=False, indent=1)
        print("[saved]", jpath, os.path.getsize(jpath), "bytes")

        # 3) 转 markdown
        md = ["# 《%s》全书大纲（接口原生数据）\n" % args.book]
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
        mpath = os.path.join(cfg["out"], "_outline.md")
        with open(mpath, "w", encoding="utf-8") as f:
            f.write("\n".join(md))
        print("[saved]", mpath, os.path.getsize(mpath), "bytes, 大纲条目字数", total)
        print("[done] 有大纲章节 %d / %d" % (len(outlines), len(uids)))


if __name__ == "__main__":
    main()
