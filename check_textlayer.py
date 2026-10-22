#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check_textlayer.py · PDF 文字层真伪检测

用途：
  区分「真文字层」和「伪文字层」—— 后者整页都是盗版广告模板，
  抽样字数 > 100 看似有文字，实际正文 0 字，白跑 OCR。

背景：
  《股票魔法师》抽样每页 100+ 字，但去广告后正文 0 字。
  判断标准不能是字数，必须检查**内容本身**。

用法：
  python check_textlayer.py "文件路径"              # 检测单本
  python check_textlayer.py "路径1" "路径2" ...     # 检测多本
"""
import sys
import fitz

# 盗版广告/水印特征词
NOISE_KEYS = [
    "手续费", "开户", "PDF电子书", "微信公众号", "7help", "kxiangou",
    "期货开户", "QQ群", "加微信", "扫码", "更多金融", "下载更多",
    "www.", "http://", "https://", "淘宝", "支付宝", "客服",
    # ⭐ 2026-10-15 新增：Z-Library 版PDF 的页眉水印
    # 实测案例《可转债投资黄金宝典》218 页正文 0 字，
    # 每一页只有一行「公众号：财金视界」—— 因按"行数占比"算被稀释到 0.50 而漏判
    "公众号", "财金视界", "Z-Library", "更多免费金融投资理财电子书",
]

# 正文特征词（技术分析书常见）
CONTENT_KEYS = [
    "交易", "市场", "价格", "买入", "卖出", "风险", "仓位", "止损",
    "均线", "成交量", "趋势", "投资者", "期货", "股票", "盈利",
]

# ⭐ 2026-10-23 新增：乱码层检测（CID 字体映射损坏型）
# 实测《交易者的101堂心理訓練課(繁体).pdf》（寰宇 2010 扫描件）：
#   正文行占比 0.91 被原标准判为「真文字层✅」，但实际字符系统性错映射
#   （市場→市埸、，→9、。→°），根本无法引用——行/字占比抓不到这种损坏。
# 判别信号（30 页采样实测）：
#   乱码层：中文标点占比 0.005（，。：；几乎消失）、怪符号占比 0.037
#   正常层：中文标点占比 0.030、怪符号占比 0.008
# 两个条件同时满足才判乱码，避免误伤英文书/无标点排版。
CN_PUNCT = "，。：；、？！"
GARBLE_SYMS = "9°`′″∷≡〓"


def check(path, sample_pages=12):
    try:
        d = fitz.open(path)
    except Exception as e:
        return {"path": path, "error": str(e)}

    n = d.page_count
    if n == 0:
        d.close()
        return {"path": path, "error": "空文件"}

    # 均匀采样
    step = max(1, n // sample_pages)
    idxs = list(range(0, n, step))[:sample_pages]

    total_chars = 0
    noise_lines = 0
    real_chars = 0
    noise_chars = 0
    real_lines = 0
    samples = []
    # 乱码层检测累计器
    punct_chars = 0
    garble_chars = 0

    for i in idxs:
        t = d[i].get_text()
        total_chars += len(t.strip())
        punct_chars += sum(t.count(c) for c in CN_PUNCT)
        garble_chars += sum(t.count(c) for c in GARBLE_SYMS)
        for line in t.split("\n"):
            line = line.strip()
            if not line:
                continue
            if any(k in line for k in NOISE_KEYS):
                noise_lines += 1
                noise_chars += len(line)
            elif len(line) >= 8:
                real_lines += 1
                real_chars += len(line)
                if len(samples) < 3:
                    samples.append(line[:60])
    d.close()

    ratio = real_lines / (real_lines + noise_lines) if (real_lines + noise_lines) else 0
    # ⭐ 2026-10-15 新增：字数占比（比行数占比更硬）
    # 为什么需要：实测《可转债投资黄金宝典》218 页正文 0 字，
    #  每页仅一行「公众号：财金视界」。按行数算 = 1:1 → 占比0.50 漏判为可用。
    #  按字数算 = 广告8字 : 正文0字 → 占比 0.00 → 正确判为伪文字层。
    char_ratio = real_chars / (real_chars + noise_chars) if (real_chars + noise_chars) else 0

    # 乱码层指标：中文标点异常稀少 + 怪符号异常密集 = 字体映射损坏
    punct_ratio = punct_chars / total_chars if total_chars else 0
    garble_ratio = garble_chars / total_chars if total_chars else 0
    garbled = punct_ratio < 0.012 and garble_ratio > 0.02

    # 判定：两个指标都要过
    if real_lines == 0:
        verdict = "伪文字层❌（全是广告，正文0字）——必须OCR"
    elif char_ratio < 0.3:
        verdict = "伪文字层❌（广告占字数主体，正文极少）——必须OCR"
    elif garbled:
        verdict = "乱码层❌（CID映射损坏，字符系统性错映射，如「市場」→「市埸」）——必须OCR或换版本"
    elif ratio < 0.3:
        verdict = "伪文字层⚠️（正文占比低）——建议抽样验证"
    elif ratio > 0.7 and char_ratio > 0.7:
        verdict = "真文字层✅（可直接抽文本）"
    else:
        verdict = "混合⚠️（含较多噪声，需清洗）"

    return {
        "pages": n,
        "sampled": len(idxs),
        "avg_chars": total_chars // len(idxs),
        "real_lines": real_lines,
        "noise_lines": noise_lines,
        "content_ratio": round(ratio, 2),
        "char_ratio": round(char_ratio, 2),
        "punct_ratio": round(punct_ratio, 3),
        "garble_ratio": round(garble_ratio, 3),
        "verdict": verdict,
        "samples": samples,
    }


def main():
    paths = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not paths:
        print("用法：python check_textlayer.py \"文件路径\" [更多路径...]")
        print("\n例：python check_textlayer.py \"E:/笔记Obsidian/电子书/股票魔法师.pdf\"")
        return

    print("=" * 66)
    print("  PDF 文字层真伪检测")
    print("=" * 66)

    for p in paths:
        import os
        name = os.path.basename(p)
        r = check(p)
        if "error" in r:
            print(f"\n❌ {name}\n   {r['error']}")
            continue

        print(f"\n📄 {name}")
        print(f"   {r['pages']} 页 · 采样 {r['sampled']} 页 · 平均 {r['avg_chars']} 字/页")
        print(f"   正文行 {r['real_lines']} / 噪声行 {r['noise_lines']}"
              f"  → 正文行占比 {r['content_ratio']} / 字数占比 {r['char_ratio']}")
        print(f"   标点占比 {r['punct_ratio']} · 怪符号占比 {r['garble_ratio']}")
        print(f"   判定：{r['verdict']}")
        if r["samples"]:
            print("   正文样例：")
            for s in r["samples"]:
                print(f"· {s}")

    print("\n" + "=" * 66)
    print("  判定标准：正文行占比 > 0.7 = 可用；< 0.3 = 伪文字层，必须 OCR")
    print("=" * 66)


if __name__ == "__main__":
    main()