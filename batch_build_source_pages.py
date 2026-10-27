# -*- coding: utf-8 -*-
"""为23本零OCR书批量建 wiki/sources/ 页骨架。
基于 survey CSV + 已抽文本字数，建 frontmatter + 出处 + 一句话定位。
核心论点留空待精读，不编造。
"""
import io, os, csv, re
from datetime import date

SURVEY = "E:/Work Buddy/交易学习/raw/books/_survey_newbatch.csv"
DISTILLED = "E:/Work Buddy/交易学习/raw/distilled"
SOURCES_DIR = "E:/Work Buddy/交易学习/wiki/sources"
SRC_PDF = "E:/Work Buddy/电子书/电子书资料每日更新（公众号私信 01 获取）"

# 分流判定：hedge类（非交易方法论，登记分流不建交易库source页）
HEDGE = {
    "009跟錢做朋友：向日本股神學習影響一生的致富觀，打通金錢通道的理財課": "理财鸡汤/生活类",
    "024《大胆投资自己》松浦弥太郎": "生活方式/个人成长",
    "029问道全球 (刘润)": "商业访谈/非交易方法论",
    "047黑石传 (【美】戴维·凯里 约翰·莫里斯)": "机构传记/非交易方法",
}

# 书名 -> source页文件名（去掉编号前缀、清理特殊字符）
def slug(book):
    # 去掉开头编号
    s = re.sub(r'^\d+\s*', '', book)
    s = re.sub(r'[\\/:*?"<>|]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

TAGS = {
    "01价值投资": ["价值投资", "基本面"],
    "02趋势技术": ["技术分析", "趋势"],
    "03游资超短": ["游资", "超短线", "打板"],
    "04基金、可转债": ["选股", "工具"],
    "05其他": ["交易方法论"],
}

def main():
    with io.open(SURVEY, encoding="utf-8-sig") as fp:
        rows = list(csv.DictReader(fp))
    zero = [r for r in rows if r["verdict"] == "零OCR" and r["book"] != "032走出幻觉 走向成熟从学生股民到系统交易专家"]

    created = []
    diverted = []
    for r in zero:
        book = r["book"]
        # 找抽出来的txt
        txt_name = book + "-全文.txt"
        txt_path = os.path.join(DISTILLED, txt_name)
        words = os.path.getsize(txt_path) if os.path.exists(txt_path) else 0

        # hedge分流
        if book in HEDGE:
            diverted.append((book, HEDGE[book]))
            continue

        # 已有source页？
        page_name = slug(book) + ".md"
        page_path = os.path.join(SOURCES_DIR, page_name)
        if os.path.exists(page_path):
            print(f"  已存在: {page_name}")
            continue

        cat = r["category"]
        tags = TAGS.get(cat, ["交易"])
        pdf_path = os.path.join(SRC_PDF, r["file"])

        today = "2026-10-27"
        content = f"""---
type: source
status: draft
source_file: "{pdf_path.replace(os.sep, '/')}"
extracted: "raw/distilled/{txt_name}"
pages: {r['pages']}
chars: {words}
compiled: {today}
category: {cat}
tags: {tags}
---

# {slug(book)}

> **待精读**：本页为自动登记骨架，核心论点与概念页待后续精读补充。

## 出处

| 项 | 值 |
|---|---|
| 原PDF | `{pdf_path.replace(os.sep, '/')}` |
| 页数 | {r['pages']} 页 |
| 文字层 | 真文字层（零OCR直抽） |
| 分类 | {cat} |
| 全文文本 | `raw/distilled/{txt_name}`（{words} 字符） |

## 定位

按 `CLAUDE.md` 判据：本书内容**待精读确认**是否可落成"看盘时用得上的动作"。

## 核心论点（待精读）

1. 
2. 
3. 

## 抽取出的页面（待建）

**概念**
- [[]]

**实体**
- [[]]

**观点**
- [[]]

## 编译状态

- [x] 全文抽取（{r['pages']}页 / {words}字符）
- [ ] 精读与概念提取
- [ ] 与本库既有体系的关联
"""
        with io.open(page_path, "w", encoding="utf-8") as fp:
            fp.write(content)
        created.append(page_name)
        print(f"  ✅ {page_name}")

    print(f"\n=== 汇总 ===")
    print(f"新建source页: {len(created)}")
    print(f"分流hedge: {len(diverted)}")
    for b, reason in diverted:
        print(f"  - {b[:40]} ({reason})")

    # 写分流清单
    with io.open("E:/Work Buddy/交易学习/raw/books/_diverted_from_batch2.csv", "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["book", "reason", "target"])
        for b, reason in diverted:
            w.writerow([b, reason, "E:/笔记Obsidian/hedge/（待确认）"])

if __name__ == "__main__":
    main()
