#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从微信读书导出「交易类」书籍的笔记内容（划线 + 想法/点评）。

用法:
  export WEREAD_API_KEY=wrk-xxx
  python _weread_export_trading.py           # 只列出交易类书 (+笔记数)
  python _weread_export_trading.py --export  # 真正导出 Markdown
"""
import os, re, sys, json, time, argparse, urllib.request

GW = "https://i.weread.qq.com/api/agent/gateway"
VER = "1.0.5"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(ROOT, "raw", "weread")

# 交易类判定关键词（书名/作者/分类任一命中即入选）
KEYWORDS = [
    "交易", "股票", "投资", "期货", "华尔街", "金融", "投机", "操盘", "盘口",
    "筹码", "止损", "波段", "K线", "蜡烛", "证券", "基金", "技术分析", "缠论",
    "缠中说禅", "趋势", "量化", "龙头", "资产配置", "复利", "资产",
    "Trading", "trading", "Invest", "Stock", "Technical",
]


def call(api_name, **params):
    key = os.environ.get("WEREAD_API_KEY")
    if not key:
        sys.exit("未设置 WEREAD_API_KEY，请先 export WEREAD_API_KEY=<wrk-...>")
    body = dict(params)
    body["api_name"] = api_name
    body["skill_version"] = VER
    req = urllib.request.Request(
        GW, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode("utf-8"))
    if d.get("upgrade_info"):
        sys.exit("!! 服务端要求升级: %s\n%s" % (d["upgrade_info"].get("message"),
                                            d["upgrade_info"].get("upgrade_url")))
    return d


def is_trading(b):
    s = ((b.get("title") or "") + " " + (b.get("author") or "") + " "
         + str(b.get("category") or "")).lower()
    return [k for k in KEYWORDS if k.lower() in s]


def safe_name(s, limit=48):
    s = re.sub(r'[\\/:*?"<>|\r\n]+', "_", s).strip()
    return s[:limit]


def ts(v):
    try:
        return time.strftime("%Y-%m-%d", time.localtime(int(v)))
    except Exception:
        return "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true", help="真正导出 Markdown")
    ap.add_argument("--sleep", type=float, default=1.2, help="每本书之间的间隔秒数")
    args = ap.parse_args()

    shelf = call("/shelf/sync")
    books = shelf.get("books") or []
    albums = shelf.get("albums") or []
    mp = shelf.get("mp")
    print("书架可见条目 = %d（电子书 %d + 专辑 %d + 文章收藏 %d）"
          % (len(books) + len(albums) + (1 if mp else 0), len(books), len(albums),
             1 if mp else 0))

    sel = [(b, is_trading(b)) for b in books if is_trading(b)]
    print("\n=== 交易类候选 %d 本 ===\n" % len(sel))
    for i, (b, kw) in enumerate(sel, 1):
        print("%2d. %-42s | %s | 分类:%s | 命中:%s"
              % (i, (b.get("title") or "")[:42], (b.get("author") or "")[:12],
                 b.get("category") or "-", ",".join(kw)))

    json.dump([{"bookId": b.get("bookId"), "title": b.get("title"),
                "author": b.get("author"), "category": b.get("category"),
                "keywords": kw} for b, kw in sel],
              open(os.path.join(ROOT, "_weread_trading_books.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    if not args.export:
        print("\n（未导出内容，加 --export 才会写 Markdown）")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    index_lines = ["# 微信读书 · 交易类书籍笔记导出", "",
                   "> 口径：划线内容 + 想法/点评内容；书签仅计数不可导出", ""]
    total_book = total_hl = total_rev = 0

    for i, (b, kw) in enumerate(sel, 1):
        bid = b.get("bookId")
        title = b.get("title") or bid
        print("\n[%d/%d] %s ..." % (i, len(sel), title))
        try:
            hl = call("/book/bookmarklist", bookId=bid)
        except Exception as e:
            print("   划线获取失败:", e)
            hl = {}
        time.sleep(args.sleep)
        try:
            rv = call("/review/list/mine", bookid=bid, count=100)
        except Exception as e:
            print("   想法获取失败:", e)
            rv = {}

        marks = hl.get("updated") or []
        chapters = {c.get("chapterUid"): c.get("title")
                    for c in (hl.get("chapters") or [])}
        reviews = rv.get("reviews") or []

        if not marks and not reviews:
            print("   无笔记，跳过")
            continue

        fname = safe_name(title) + ".md"
        path = os.path.join(OUTDIR, fname)
        L = ["# %s" % title, "",
             "- 作者：%s" % (b.get("author") or "-"),
             "- 分类：%s" % (b.get("category") or "-"),
             "- bookId：`%s`" % bid,
             "- 导出时间：%s" % time.strftime("%Y-%m-%d %H:%M"),
             "- 划线 %d 条 / 想法 %d 条" % (len(marks), len(reviews)), ""]

        if marks:
            L += ["## 划线原文", ""]
            by_chap = {}
            for m in marks:
                by_chap.setdefault(m.get("chapterUid"), []).append(m)
            for uid, ms in by_chap.items():
                L += ["### %s" % (chapters.get(uid) or "未归类"), ""]
                for m in ms:
                    L.append("> %s" % (m.get("markText") or "").replace("\n", " "))
                    L.append("")
                    L.append("<sub>%s · %s</sub>" % (ts(m.get("createTime")),
                                                     m.get("range") or ""))
                    L.append("")
        if reviews:
            L += ["## 想法 / 点评", ""]
            for r in reviews:
                rr = r.get("review") or r
                chap = rr.get("chapterName")
                head = "- **%s**%s：" % (ts(rr.get("createTime")),
                                        (" · %s" % chap) if chap else "")
                L.append(head + (rr.get("content") or "").replace("\n", " "))
                L.append("")

        open(path, "w", encoding="utf-8", newline="").write("\n".join(L))
        total_book += 1
        total_hl += len(marks)
        total_rev += len(reviews)
        index_lines.append("- [[%s]] — 划线 %d / 想法 %d（%s）"
                           % (safe_name(title), len(marks), len(reviews),
                              b.get("author") or "-"))
        print("   -> %s（划线 %d / 想法 %d）" % (fname, len(marks), len(reviews)))
        time.sleep(args.sleep)

    index_lines += ["", "合计：%d 本有笔记，划线 %d 条，想法 %d 条"
                    % (total_book, total_hl, total_rev)]
    idx = os.path.join(OUTDIR, "_索引.md")
    open(idx, "w", encoding="utf-8", newline="").write("\n".join(index_lines))
    print("\n=== 完成：%d 本 · 划线 %d 条 · 想法 %d 条 ===" % (total_book, total_hl, total_rev))
    print("输出目录:", OUTDIR)


if __name__ == "__main__":
    main()
