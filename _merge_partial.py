#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把已抓到的碎片合并成一份去重后的连续正文(按抓取顺序),并列出仍缺的目录小节。"""
import os, re, io, json, hashlib

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "raw/distilled/steenbarger-2015-zh")


def main():
    files = sorted(f for f in os.listdir(BASE) if re.match(r"\d{4}\.txt$", f))
    seen = set()
    chunks = []
    dup_chars = 0
    for f in files:
        t = io.open(os.path.join(BASE, f), encoding="utf-8").read()
        ps = [p.strip() for p in t.split("\n\n") if len(p.strip()) > 8]
        keep = []
        for p in ps:
            h = hashlib.md5(p.encode("utf-8")).hexdigest()
            if h in seen:
                dup_chars += len(p)
                continue
            seen.add(h)
            keep.append(p)
        if keep:
            chunks.append((f, keep))
    total = sum(len(p) for _f, ps in chunks for p in ps)
    out = ["# 《交易心理分析2.0》(Steenbarger 2015) 已抓取正文\n",
           "> 来源: 微信读书阅读器陆续抓取的 %d 个片段,段落级去重后合并。" % len(files),
           "> 去重后净字数 %d / 全书约 %d 字 (%.1f%%)。重复丢弃 %d 字。"
           % (total, 302982, total / 302982 * 100, dup_chars),
           "> ⚠️ 本书尚未抓全,缺章见 `_缺口清单.md`。\n"]
    for f, ps in chunks:
        out.append("\n<!-- 来源片段 %s -->\n" % f)
        out.append("\n\n".join(ps))
    opath = os.path.join(BASE, "_正文_已抓取.md")
    io.open(opath, "w", encoding="utf-8").write("\n".join(out))
    print("[saved]", opath, os.path.getsize(opath), "bytes, 净字数", total)

    # 缺口清单
    toc = json.load(io.open(os.path.join(BASE, "_toc.json"), encoding="utf-8"))
    corp = re.sub(r"\s+", "", "\n".join(p for _f, ps in chunks for p in ps))
    miss = [t for t in toc if re.sub(r"\s+", "", t) not in corp]
    chaps = json.load(io.open(os.path.join(BASE, "_chapters.json"), encoding="utf-8"))
    miss_uid = [(c["chapterUid"], c["title"]) for c in chaps
                if re.sub(r"\s+", "", c["title"]) not in corp and len(c["title"]) > 3]
    lines = ["# 仍未抓到的内容清单\n",
             "- 目录小节 %d/%d 命中,缺 %d 个" % (len(toc) - len(miss), len(toc), len(miss)),
             "- 章节级(95章)缺 %d 章:\n" % len(miss_uid)]
    for u, t in miss_uid:
        lines.append("  - uid %d 《%s》" % (u, t))
    lines.append("\n## 缺失的小节标题\n")
    for m in miss:
        lines.append("- %s" % m)
    mp = os.path.join(BASE, "_缺口清单.md")
    io.open(mp, "w", encoding="utf-8").write("\n".join(lines))
    print("[saved]", mp, "| 缺章节 %d, 缺小节 %d" % (len(miss_uid), len(miss)))


if __name__ == "__main__":
    main()
