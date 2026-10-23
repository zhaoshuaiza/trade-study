# PIPELINE_STATE — 032《走出幻觉·走向成熟》

> cangjie-skill RIA-TV++ v2.5 流水线状态文件。中断后从此续跑，不要从头重来。

## 元信息
- **slug**: 032-zouchuhuanjue
- **标题**: 走出幻觉·走向成熟：从学生股民到系统交易专家
- **作者**: 金融帝国
- **源文本**: `books/032-zouchuhuanjue/source.txt`（212125 中文字，7408 行，零OCR 直抽）
- **索引**: `.cangjie/index/lexical.sqlite`（71 chunks，FTS5）
- **使用目的**: 接入交易学习工作流 + 跨书组合 → 倾向 **pack**
- **首跑试点**: 是（用户要求先试点 1 本）

## 阶段进度
| 阶段 | 状态 | 产出 | 完成时间 |
|---|---|---|---|
| 0 整书理解 | ✅ 已完成（用户已确认） | BOOK_OVERVIEW.md | 2026-10-23 |
| 1 并行提取 | 🔄 进行中 | candidates/*.md（5 路） | — |
| 1.5 三重验证 | ⏳ 待做 | verified.md / rejected/ | — |
| 1.6 晋级门 | ⏳ 待做 | .cangjie/capabilities/destinations.json | — |
| 2 RIA++ 能力卡 | ⏳ 待做 | .cangjie/capabilities/cards/*.md + verified.yaml | — |
| 3 Zettelkasten | ⏳ 待做 | GLOSSARY.md | — |
| 4 压力测试 | ⏳ 待做 | test-prompts | — |
| 5 编译交付 | ⏳ 待做 | cangjie.py compile + DIGEST.md | — |

## 阶段 1 提取器派发（2026-10-23）
- framework-extractor → candidates/frameworks.md（全量扫描）
- principle-extractor → candidates/principles.md（全量扫描）
- case-extractor → candidates/cases.md（检索式，用 index）
- counter-example-extractor → candidates/counter-examples.md（检索式，用 index）
- glossary-extractor → candidates/glossary.md（检索式，用 index）

## 全局路由决策（本次 82 本批次）
- **核心书走仓颉（cangjie）**: 032（试点，进行中）+ 021 蜡烛图 + 042 量价 + 062 波浪（用户仅选「技术类」纳入核心）
- **其余 ~78 本走既有轻量管线**（含 036 退学炒股、022 交易系统、030 通向财务自由、018 止损、011-012 庄家筹码、060 筹码天机 等；其中 58 本需 OCR）
- **9 本财富/哲学/传记类**: 仍留在交易学习库（不分流 hedge）

## 备注
- 阶段 0 候选 skill 数 12–15 个（系统/心理层）+ 第二章 24 原理可选 8–11 个，最终由阶段 1.5 决定。
- 批判（时代/立场/假设/最强反对 4 条）将作为下游能力卡 B 段来源。
- 作者主要在期货验证，A股单边/做空受限 → B 段须标注适用边界。
