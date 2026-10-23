#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""拉取 /user/notebooks 全量（游标分页），落盘并与交易类候选书交叉核对。"""
import os, json, urllib.request

GW = "https://i.weread.qq.com/api/agent/gateway"
VER = "1.0.5"
ROOT = os.path.dirname(os.path.abspath(__file__))


def call(body):
    body = dict(body)
    body["skill_version"] = VER
    req = urllib.request.Request(
        GW, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + os.environ["WEREAD_API_KEY"],
                 "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))


def main():
    allb, last, page = [], None, 0
    while True:
        body = {"api_name": "/user/notebooks", "count": 100}
        if last:
            body["lastSort"] = last
        d = call(body)
        bs = d.get("books") or []
        page += 1
        print("第%d页: %d 本 | hasMore=%s" % (page, len(bs), d.get("hasMore")))
        allb += bs
        if not d.get("hasMore") or not bs or page > 20:
            break
        last = bs[-1].get("sort")

    json.dump(allb, open(os.path.join(ROOT, "_weread_notebooks.json"), "w",
                         encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n有笔记的书: %d 本，服务端 totalBookCount=%s"
          % (len(allb), d.get("totalBookCount")))

    rows = []
    for x in allb:
        b = x.get("book") or {}
        tot = (x.get("reviewCount") or 0) + (x.get("noteCount") or 0) \
              + (x.get("bookmarkCount") or 0)
        rows.append((b.get("title") or "?", x.get("reviewCount") or 0,
                     x.get("noteCount") or 0, x.get("bookmarkCount") or 0, tot,
                     x.get("bookId")))
    rows.sort(key=lambda r: -r[4])
    print("\n=== 笔记最多的 15 本 ===")
    for t, rv, nt, bk, tot, _ in rows[:15]:
        print("  %-40s 想法%-4d 划线%-5d 书签%-3d 合计%d" % (t[:40], rv, nt, bk, tot))

    # 与交易类候选交叉核对
    try:
        cand = json.load(open(os.path.join(ROOT, "_weread_trading_books.json"),
                              encoding="utf-8"))
    except Exception:
        cand = []
    titles = {c["title"]: c for c in cand}
    print("\n=== 12 本交易类候选的笔记实况 ===")
    found = 0
    for t, rv, nt, bk, tot, _ in rows:
        if t in titles:
            found += 1
            print("  ★ %-44s 想法%d 划线%d 书签%d = %d" % (t[:44], rv, nt, bk, tot))
    for c in cand:
        if c["title"] not in [r[0] for r in rows]:
            print("  - %-44s 无任何笔记" % c["title"][:44])
    print("\n交易类中有笔记的: %d / %d" % (found, len(cand)))


if __name__ == "__main__":
    main()
