# -*- coding: utf-8 -*-
"""新批次勘察 v2：更严文字层判定（防封面误判）。

修正：v1 的 check_textlayer 只在少数采样页里撞到封面 1 行真文字就误报"真文字层"。
v2 要求「多数采样页都有真实中文正文」才算零OCR，否则判需OCR。

用法: python survey_newbatch.py
输出: raw/books/_survey_newbatch.csv
"""
import io, os, csv, re, importlib.util

SPEC = importlib.util.spec_from_file_location(
    "check_textlayer", "E:/Work Buddy/交易学习/check_textlayer.py")
ctl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ctl)

SRC = "E:/Work Buddy/电子书/电子书资料每日更新（公众号私信 01 获取）"
OUT = "E:/Work Buddy/交易学习/raw/books/_survey_newbatch.csv"

CAT_KW = {
    "03游资超短": ["游资", "退学炒股", "92科比", "打板", "首板", "超短", "新股战法"],
    "01价值投资": ["巴菲特", "索罗斯", "价值投资", "价值", "逆向", "邓普顿", "段永平",
                  "成长股", "雪球", "指数基金", "金融学", "投资的原则", "投资之道",
                  "漫步", "聪明的", "彼得林奇", "格雷厄姆", "柏基"],
    "02趋势技术": ["蜡烛图", "K线", "k线", "波浪", "缠论", "MACD", "均线", "量价",
                  "筹码", "背离", "亚当理论", "趋势", "盘中", "形态", "交易圣经",
                  "短线交易", "短线", "量能", "分时", "主力", "庄家", "散户", "黑马",
                  "道氏", "技术分析", "斐波那契", "黄金短线", "逻辑形态", "交易员量价",
                  "量价破解", "看透分时", "看穿主力", "透过F10"],
    "04基金、可转债": ["指数基金", "基金", "可转债", "ETF", "选股", "選股"],
}
HEDGE_KW = ["财富法则", "大胆投资自己", "问道全球", "黑石传", "金融哲学", "跟錢做朋友", "跟钱做朋友"]


def clean(name):
    return re.sub(r"\.(pdf|epub|mobi|azw3|azw)$", "", name, flags=re.I).strip()


def classify(name):
    if any(h in name for h in HEDGE_KW):
        return "05其他"
    for cat, kws in CAT_KW.items():
        if any(k in name for k in kws):
            return cat
    return "05其他"


def strict_check(path, sample_pages=15):
    """返回 (verdict_norm, raw_verdict, pages, real_page_frac, garbled)"""
    try:
        d = ctl.fitz.open(path)
    except Exception as e:
        return "异常", f"打开失败:{str(e)[:40]}", 0, 0, False
    n = d.page_count
    if n == 0:
        d.close(); return "异常", "空文件", 0, 0, False
    step = max(1, n // sample_pages)
    idxs = list(range(0, n, step))[:sample_pages]
    real_pages = 0
    garbled_hits = 0
    any_content = False
    for i in idxs:
        t = d[i].get_text()
        cjk = len([c for c in t if '一' <= c <= '鿿'])
        if cjk >= 50:
            real_pages += 1
            any_content = True
            # 乱码检测：中文标点极少 + 怪符号多
            punct = sum(t.count(c) for c in "，。：；、？！")
            garb = sum(t.count(c) for c in "9°`′″∷≡〓")
            if cjk and (punct / cjk < 0.012 and garb / cjk > 0.02):
                garbled_hits += 1
    d.close()
    frac = real_pages / len(idxs)
    if not any_content:
        return "需OCR", "扫描/无文字层（采样页均无正文）——必须OCR", n, 0, False
    if frac >= 0.6:
        if garbled_hits >= max(1, real_pages // 2):
            return "需OCR", "乱码层❌（采样页中文标点异常/怪符号多，CID映射损坏）——需换版本或OCR", n, round(frac, 2), True
        return "零OCR", "真文字层✅（多数采样页有真实正文）", n, round(frac, 2), False
    return "需OCR", f"伪/稀疏文字层❌（仅{real_pages}/{len(idxs)}采样页有正文，正文0字或扫描）——必须OCR", n, round(frac, 2), False


def main():
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".pdf"))
    rows = []
    for f in files:
        path = os.path.join(SRC, f)
        norm, raw, pages, frac, garb = strict_check(path)
        rows.append({
            "category": classify(clean(f)), "book": clean(f), "file": f,
            "pages": pages, "verdict": norm, "raw_verdict": raw,
            "real_page_frac": frac, "mb": round(os.path.getsize(path) / 1048576, 1),
        })
        print(f"  {clean(f)[:32]:34s} {norm:6s} p{pages:>4} frac={frac}  {raw}")
    rows.sort(key=lambda x: (x["category"], x["book"]))
    with io.open(OUT, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(f"\n共 {len(rows)} 本 -> {OUT}")
    print("分类:", dict(Counter(r["category"] for r in rows)))
    print("文字层(v2):", dict(Counter(r["verdict"] for r in rows)))


if __name__ == "__main__":
    main()
