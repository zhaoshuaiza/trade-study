#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把书架里「交易类」书籍能拿到的内容全部做出来:
   书籍详情 + 完整章节目录 + 阅读进度 + 热门划线原文(读者划得最多的段落)

用法:
  export WEREAD_API_KEY=wrk-xxx
  python _weread_trading_package.py
"""
import os, re, sys, json, time, urllib.request

GW = "https://i.weread.qq.com/api/agent/gateway"
VER = "1.0.5"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(ROOT, "raw", "weread")

KEYWORDS = [
    "交易", "股票", "投资", "期货", "华尔街", "金融", "投机", "操盘", "盘口",
    "筹码", "止损", "波段", "K线", "蜡烛", "证券", "基金", "技术分析", "缠论",
    "缠中说禅", "趋势", "量化", "龙头", "资产配置", "复利",
    "Trading", "trading", "Invest", "Stock", "Technical",
]


def call(api_name, **params):
    key = os.environ.get("WEREAD_API_KEY")
    if not key:
        sys.exit("未设置 WEREAD_API_KEY")
    body = dict(params)
    body["api_name"] = api_name
    body["skill_version"] = VER
    req = urllib.request.Request(
        GW, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
    if d.get("upgrade_info"):
        sys.exit("!! 需升级: %s" % d["upgrade_info"].get("upgrade_url"))
    return d


def ymd(v):
    try:
        return time.strftime("%Y-%m-%d", time.localtime(int(v)))
    except Exception:
        return "-"


def hm(sec):
    try:
        sec = int(sec)
    except Exception:
        return "-"
    h, m = sec // 3600, (sec % 3600) // 60
    return ("%d小时%d分钟" % (h, m)) if h else ("%d分钟" % m)


def safe(s, limit=44):
    return re.sub(r'[\\/:*?"<>|\r\n]+', "_", s or "").strip()[:limit]


def main():
    shelf = call("/shelf/sync")
    books = shelf.get("books") or []

    def kw_hit(b):
        s = ((b.get("title") or "") + " " + (b.get("author") or "") + " "
             + str(b.get("category") or "")).lower()
        return [k for k in KEYWORDS if k.lower() in s]

    sel = [(b, kw_hit(b)) for b in books if kw_hit(b)]
    os.makedirs(OUTDIR, exist_ok=True)
    index = ["# 微信读书 · 交易类书籍（自动导出）", "",
             "> 来源：微信读书技能接口。含书籍详情、章节目录、阅读进度、",
             "> 热门划线（全站读者划得最多的原文，按人数排序，每本最多 20 条）。",
             "> 个人划线/想法已核实基本为空，故以热门划线作为内容来源。", ""]

    stat = []
    for i, (b, kw) in enumerate(sel, 1):
        bid = b.get("bookId")
        title = b.get("title") or bid
        print("[%d/%d] %s" % (i, len(sel), title))
        L = ["# %s" % title, "", "- 命中标签：%s" % ",".join(kw), ""]
        try:
            info = call("/book/info", bookId=bid)
            L += ["## 书籍信息", "",
                  "- 作者：%s" % (info.get("author") or "-"),
                  "- 译者：%s" % (info.get("translator") or "-"),
                  "- 出版社：%s（%s）" % (info.get("publisher") or "-",
                                        info.get("publishTime") or "-"),
                  "- 分类：%s" % (info.get("category") or "-"),
                  "- 字数：%s" % (info.get("wordCount") or "-"),
                  "- 评分：%s / 100（%s 人评）" % (info.get("newRating") or "-",
                                                info.get("newRatingCount") or "-"),
                  "- ISBN：%s" % (info.get("isbn") or "-"),
                  "- bookId：`%s`" % bid, ""]
            if info.get("intro"):
                L += ["### 简介", "", "> %s" % info["intro"].strip(), ""]
            link = info.get("readerLink") or info.get("deepLink")
            if link:
                L += ["- 打开阅读：%s" % link, ""]
        except Exception as e:
            print("   info 失败:", e)

        n_chap = 0
        try:
            ci = call("/book/chapterinfo", bookId=bid)
            chaps = ci.get("chapters") or []
            n_chap = len(chaps)
            L += ["## 章节目录（%d 章）" % n_chap, ""]
            for c in chaps:
                lv = c.get("level") or 1
                wc = c.get("wordCount") or 0
                L.append("%s- %s（%d字）" % ("  " * (lv - 1), c.get("title") or "?", wc))
            L.append("")
        except Exception as e:
            print("   chapterinfo 失败:", e)
        time.sleep(0.8)

        prog = 0
        try:
            pg = (call("/book/getprogress", bookId=bid).get("book") or {})
            prog = pg.get("progress") or 0
            L += ["## 阅读进度", "",
                  "- 进度：**%d%%**" % prog,
                  "- 当前章节 UID：%s" % (pg.get("chapterUid") or "-"),
                  "- 累计阅读时长：%s" % hm(pg.get("recordReadingTime")),
                  "- 最后阅读：%s" % ymd(pg.get("updateTime")),
                  "- 读完时间：%s" % (ymd(pg.get("finishTime")) if pg.get("finishTime")
                                    else "未读完"), ""]
        except Exception as e:
            print("   progress 失败:", e)
        time.sleep(0.8)

        n_hl = 0
        try:
            bb = call("/book/bestbookmarks", bookId=bid)
            items = bb.get("items") or []
            n_hl = len(items)
            chaps = {c.get("chapterUid"): c.get("title")
                     for c in (bb.get("chapters") or [])}
            L += ["## 热门划线（%d 条）" % n_hl, "",
                  "> 全站读者划得最多的原文片段，按划线人数降序", ""]
            for it in items:
                chap = chaps.get(it.get("chapterUid")) or "未归类"
                L.append("**%s**（%d 人划线）" % (chap, it.get("totalCount") or 0))
                L.append("")
                L.append("> %s" % (it.get("markText") or "").replace("\n", " "))
                L.append("")
        except Exception as e:
            print("   bestbookmarks 失败:", e)
        time.sleep(0.8)

        fn = safe(title) + ".md"
        open(os.path.join(OUTDIR, fn), "w", encoding="utf-8", newline="") \
            .write("\n".join(L))
        stat.append((title, b.get("author") or "-", n_chap, prog, n_hl, fn))
        print("   -> %s | 章节%d 进度%d%% 热门划线%d" % (fn, n_chap, prog, n_hl))

    # 索引
    index += ["## 总览", "", "| # | 书名 | 作者 | 章节 | 进度 | 热门划线 |",
              "|---|------|------|------|------|------|"]
    for i, (t, a, nc, pg, nh, fn) in enumerate(stat, 1):
        index.append("| %d | [[%s]] | %s | %d | %d%% | %d |"
                     % (i, fn[:-3], a[:10], nc, pg, nh))
    index += ["", "- 合计 %d 本，章节 %d 章，热门划线 %d 条"
              % (len(stat), sum(s[2] for s in stat), sum(s[4] for s in stat)),
              "- 导出时间：%s" % time.strftime("%Y-%m-%d %H:%M"), ""]
    open(os.path.join(OUTDIR, "_索引.md"), "w", encoding="utf-8", newline="") \
        .write("\n".join(index))
    print("\n=== 完成 %d 本 · 章节 %d · 热门划线 %d ==="
          % (len(stat), sum(s[2] for s in stat), sum(s[4] for s in stat)))


if __name__ == "__main__":
    main()
