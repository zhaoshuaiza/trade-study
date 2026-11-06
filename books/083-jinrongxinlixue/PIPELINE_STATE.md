# PIPELINE_STATE · 083《金融心理学》

> 仓颉流水线状态看板。源地址：`E:/电子书/电子书资料每日更新（公众号私信 01 获取）/083金融心理学.pdf`

## 源文本事实
- `source.txt`：399,901 字符 / 353 页（**零 OCR，真文字层**，pymupdf 直抽）
- 索引：`.cangjie/index/lexical.sqlite`（39 chunks，FTS5）
- 作者 [挪威] 拉斯·特维德；中信 2013（原版 The Psychology of Finance, 2002）

## 阶段表
| 阶段 | 状态 | 产出 | 完成时间 |
|---|---|---|---|
| 0 整书理解 | ✅ 已完成 | BOOK_OVERVIEW.md | 2026-11-04 |
| 1 并行提取 | ✅ 已完成 | candidates/*.md | 2026-11-07 |
| 1.5 三重验证 | ✅ 已完成 | verified.md + rejected/ | 2026-11-07 |
| 1.6 晋级门 | ✅ 已完成 | destinations.json | 2026-11-07 |
| 2 RIA++ 能力卡 | ✅ 已完成 | verified.yaml + cards/ | 2026-11-07 |
| 3 Zettelkasten | ✅ 已完成 | GLOSSARY.md | 2026-11-07 |
| 4 压力测试 | ✅ 已完成 | tests/ | 2026-11-07 |
| 5 编译交付 | ✅ 已完成 | dist/pack + DIGEST.md | 2026-11-07 |

## 路由
- 核心书，走仓颉六阶段（与 021 同级）。属「交易心理」元框架，与 032《走出幻觉》互补。
- 优先级排在本批新 12 本前列。

## 备注
- 与 021（微观 K 线形态）差异：本书是市场心理的**元框架**（为什么趋势/非理性/图形自我实现）。
- 边界：纯理解框架，不含买卖点；案例多为欧美史实，引用须注明时效。
- 同批零 OCR 的 085《慢即是快》可并行启动。


## 交付记录（2026-11-07）
- 阶段 0–5 **全部完成**；`dist/pack` 已编译发布，`validate_skill_pack.py` **0 error / 1 warning**（name-dir，与 032 同类可接受）。
- `tests/` 8 套 × 8 条 = 64 条压力测试（含可转债品种越界边界用例）。
- `GLOSSARY.md` 27 条 + `.cangjie/capabilities/book/{overview,glossary}.md` 已就位，SKILL.md 引用闭合。
