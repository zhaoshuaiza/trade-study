# -*- coding: utf-8 -*-
"""生成第二批60本电子书的总处理计划台账。
每本标注：分类、页数、文字层、路线、状态、下一步。
"""
import io, csv, os

SURVEY = "E:/Work Buddy/交易学习/raw/books/_survey_newbatch.csv"
BATCH_DIR = "E:/Work Buddy/交易学习"
OUT = f"{BATCH_DIR}/books/_BATCH2_PIPELINE.md"

# 已完成深度蒸馏的
DONE = {
    "021日本蜡烛图技术详解  酒田78条战法解析(高清).pdf": "✅ cangjie完成（books/021-jiutian78）",
    "032走出幻觉 走向成熟从学生股民到系统交易专家.pdf": "✅ cangjie完成（books/032-zouchuhuanjue）",
}

# 分流hedge
HEDGE = {
    "009跟錢做朋友：向日本股神學習影響一生的致富觀，打通金錢通道的理財課 .pdf": "分流hedge（理财鸡汤）",
    "024《大胆投资自己》松浦弥太郎.pdf": "分流hedge（生活方式）",
    "029问道全球 (刘润) .pdf": "分流hedge（商业访谈）",
    "047黑石传 (【美】戴维·凯里 约翰·莫里斯) .pdf": "分流hedge（机构传记）",
    "001财富法则 世界上最神奇的创富智慧.pdf": "分流hedge（创富鸡汤，待确认）",
}

# 正在OCR队列里的
OCR_QUEUE = {
    "018止损 如何克服贪婪和恐惧.pdf": "🔄 OCR完成（226页，p103失败）",
    "051亚当理论  赚钱最重要(高清).pdf": "🔄 OCR队列第2本",
    "063MACD指标精讲：从入门到精通(高清).pdf": "⏳ OCR队列第3本",
    "043股市波浪派手册(高清).pdf": "⏳ OCR队列第4本",
}

# 零OCR已直抽+建骨架的
ZERO_DONE = {
    "007大道无形段永平 (刘若愚).pdf",
    "008柏基投资之道 -- 李正 -- 2025 .pdf",
    "019投资的原则.pdf",
    "027雪球股票投资24章+(雪球)+.pdf",
    "076成长股的投资之道：如何通过只买入最好的公司持续获利.pdf",
    "003趋势2030.pdf",
    "044盘中策略思考篇以及问题解决篇.pdf",
    "023《92科比_新生代首板高手》 (92科比).pdf",
    "073Excel選股法我用一張表,每天早上5分鐘,3步驟選出穩賺股 (森口亮).pdf",
    "004因子投资 (石川, 刘洋溢, 连祥斌).pdf",
    "006股市稳赚.pdf",
    "025顶级专业交易员培训教程-301页.pdf",
    "028他是賭神，更是股神：從賭城連贏到華爾街的天才數學家，關於風險、財富和人生的第一手告白 .pdf",
    "033股票投资入门、进阶与实战 (朱孜、王俊龙).pdf",
    "037金融哲学三部曲01货币起源（OCR） (周洛华).pdf",
    "038金融哲学三部曲02市场本质（OCR） (周洛华) .pdf",
    "039金融哲学三部曲 03 估值原理（OCR） (周洛华) .pdf",
    "059期货大作手风云录 (逍遥刘强).pdf",
    "077胡立阳股票投资制胜30秘则 (胡立阳).pdf",
}

# 核心深度蒸馏候选（技术类，优先走cangjie）
CANGJIE_CANDIDATES = {
    "022简简单单做股票-交易系统的构建心得和运用技巧 (楚云风).pdf": "交易系统构建",
    "030通向财务自由之路 (范·撒普).pdf": "仓位管理经典",
    "031市场奇才 顶级交易员的经验 引进版 (杰克·D.施瓦格著；陈佶译, 施瓦格 (Schwager, Jack D.) etc.).pdf": "交易员访谈",
    "016股市投机讲义之《基础篇》.pdf": "投机基础",
    "017著名游资悟道心得（精英版）.pdf": "游资心法",
    "026月风_《新股战法》高清彩图.pdf": "新股战法",
    "036淘股吧 退学炒股 超短打板的心法与精髓.pdf": "超短打板",
}

def status_of(row):
    fn = row["file"]
    if fn in DONE: return DONE[fn], "已完成"
    if fn in HEDGE: return HEDGE[fn], "分流"
    if fn in OCR_QUEUE: return OCR_QUEUE[fn], "OCR中"
    if fn in ZERO_DONE: return "✅ 直抽完成+source页骨架，待精读", "直抽待精读"
    if row["verdict"] == "零OCR": return "待直抽", "待处理"
    if fn in CANGJIE_CANDIDATES:
        return f"待OCR→cangjie深度蒸馏（{CANGJIE_CANDIDATES[fn]}）", "排队OCR"
    return "待OCR→轻量管线（建source页+提取概念）", "排队OCR"

def main():
    with io.open(SURVEY, encoding="utf-8-sig") as fp:
        rows = list(csv.DictReader(fp))

    # 只保留百度盘60本里的
    import os
    SRC = "E:/Work Buddy/电子书/电子书资料每日更新（公众号私信 01 获取）"
    disk_files = set(os.listdir(SRC))
    rows = [r for r in rows if r["file"] in disk_files]

    rows.sort(key=lambda x: (x["category"], x["book"]))

    lines = []
    lines.append("# 第二批电子书处理计划总台账（百度盘60本）")
    lines.append("")
    lines.append("> 自动生成于 2026-10-27。每本标注路线、状态、下一步。")
    lines.append("> 路线说明：")
    lines.append("> - **cangjie深度蒸馏**：走books/下完整RIA流水线（阶段0-5），产出Skill包")
    lines.append("> - **轻量管线**：抽文本→建wiki/sources/页→提取关键概念/主张")
    lines.append("> - **分流hedge**：非交易方法论，登记后移出交易库")
    lines.append("")

    # 统计
    from collections import Counter
    cats = Counter(r["category"] for r in rows)
    lines.append("## 总览")
    lines.append("")
    lines.append(f"共 **{len(rows)}** 本：")
    for cat, n in sorted(cats.items()):
        lines.append(f"- {cat}: {n}本")
    lines.append("")

    # 按分类分组
    current_cat = None
    for r in rows:
        if r["category"] != current_cat:
            current_cat = r["category"]
            lines.append(f"\n## {current_cat}\n")
            lines.append("| # | 书名 | 页 | MB | 文字层 | 路线 | 状态/下一步 |")
            lines.append("|---|---|---|---|---|---|---|")
        status, tag = status_of(r)
        book_short = r["book"][:38]
        lines.append(f"| {r['book'][:3]} | {book_short} | {r['pages']} | {r['mb']} | {r['verdict']} | {tag} | {status} |")

    lines.append("\n---\n")
    lines.append("## 执行优先级")
    lines.append("")
    lines.append("### P0 · 进行中")
    lines.append("1. OCR队列：止损✅ → 亚当理论🔄 → MACD精讲 → 波浪派手册")
    lines.append("2. 042量柱擒涨停双路线（books/042-liangzhu/PIPELINE_STATE.md）")
    lines.append("")
    lines.append("### P1 · OCR完成后立即做")
    lines.append("- 为4本OCR完成的书建正式source页（替换骨架）")
    lines.append("")
    lines.append("### P2 · 核心深度蒸馏候选（cangjie）")
    lines.append("- 022简简单单做股票（交易系统构建）")
    lines.append("- 030通向财务自由之路（范撒普仓位管理）")
    lines.append("- 017著名游资悟道心得（游资心法）")
    lines.append("- 036退学炒股（超短打板）")
    lines.append("- 026月风新股战法")
    lines.append("")
    lines.append("### P3 · 轻量管线批量处理")
    lines.append("- 其余OCR完成的书：建source页+提取核心概念")
    lines.append("- 零OCR直抽的19本骨架页：按需精读填充")
    lines.append("")
    lines.append("### P4 · 待确认分流")
    lines.append("- 001财富法则（创富鸡汤，是否分流hedge待确认）")
    lines.append("- 037-039金融哲学三部曲（周洛华学术，偏金融哲学，是否留交易库待确认）")

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 台账已生成: {OUT}")
    print(f"共 {len(rows)} 本")

if __name__ == "__main__":
    main()
