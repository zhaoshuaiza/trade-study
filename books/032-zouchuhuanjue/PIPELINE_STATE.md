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
| 1 并行提取 | ✅ 已完成 | candidates/*.md（principles 40 / cases 25 / counter-examples 28 / glossary 19） | 2026-10-23 |
| 1.5 三重验证 | ✅ 已完成 | candidates/_v15/verified.md + rejected.md | 2026-10-24 |
| 1.6 晋级门 | ✅ 已完成 | destinations.json（7 promoted / 22 router，router 于阶段2补全） | 2026-10-24 |
| 2 RIA++ 能力卡 | ✅ 已完成 | verified.yaml（29 能力：7 promoted + 22 router）+ cards/（29 张六段卡） | 2026-10-24 |
| 3 Zettelkasten | ✅ 已完成 | GLOSSARY.md（19 术语） | 2026-10-24 |
| 4 压力测试 | ✅ 已完成（fallback 自测；独立盲测待 sub-agent） | tests/*/test-prompts.json（56 条）+ tests/test-results.md | 2026-10-24 |
| 5 编译交付 | ✅ 已完成 | dist/pack（8 入口，校验 0 error / 0 warning）+ DIGEST.md | 2026-10-24 |

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

## ⚠️ 事故记录（2026-10-24）
- 会话续接后 `candidates/frameworks.md`（43 条框架）与 `candidates/_v15/`（三路验证输出）**双双丢失**，
  仅 principles/cases/counter-examples/glossary 四个文件幸存。
- 重跑 framework-extractor 时子代理撞 **429 限流**（03:29 重置），未能重建 frameworks.md。
- **补救措施（已执行）**：team-lead 在主代理直接合并，并从 source.txt 原文补齐了仅存在于 frameworks.md 的
  3 条原理（巨变效应 L768–778 / 对错悖论 L962–990 / 小蝴蝶 L1275–1297）与 1 条残差框架
  （外化而内不化 L1757–1765）。二八法则核查后确认是销售类比，已并入 SK-core-06。
- **遗留**：frameworks.md 仍缺失。阶段 2 如需框架版原文，待限流重置后重建，或直接用 principles.md 的 p20–p33
  （同一批命名原理的原则版，含原文引用）替代。

## 阶段 1.5 结果（2026-10-24）
- **验证通过 29 个 skill 候选** = 核心系统层 11 + 第二章命名原理 17（含 2 处合并：微宏互换→赌场原理、
  因果倒置→等效性）+ 残差框架 1（外化而内不化）
- **独立淘汰 17 条**（核心层 8 条 FAIL V3 常识 / 命名原理 6 条 FAIL V1 无跨章复用 / team-lead 追加 3 条）
- **支撑材料通过**：cases 25、glossary 19、counter-examples 28（供各卡 R/I/A/B 段引用）
- **4 条边界项待用户裁决**：f09 预测≠交易、f07 道与术、f12 开发系统个性化、p15–p19 赌博五原则

## 阶段 2 编排范围（2026-10-24，用户未选默认走推荐路径）
- 已进入 Bundle 的 **7 个晋级 Skill**（P0/P1 中最高频、意图最独立的 7 个）：
  1. trading-loss-as-cost 盈亏同源/成本观（critical）
  2. loss-maturity-ladder 亏损五境界（critical）
  3. risk-guard-two-points 风险防范两点（high）
  4. avoid-over-optimization 优化与组合陷阱（critical）
  5. insect-system-recipe 昆虫系统（high）
  6. high-winrate-trap 超市原理（critical）
  7. learning-effect-chasing-tail 学习效应（high）
- 入口数 = 1 路由 + 7 晋级 = 8，正好压在 promotion_budget=8 上限，因此**不能再新增晋级 Skill**，
  后续补充的能力只能以 `destination: router` 加入 Bundle。
- ✅ **22 个已验证能力的 router 补全已完成**（2026-10-24）：A 组 core-08/09/10/11、B 组 p24-01~17 共 17 条、
  C 组 misc-01，全部以 `destination: router` 写入 cards/ + 追加进 verified.yaml + 重算 destinations.json。
  编译器自动将其纳入路由表 / 能力索引 / cheatsheet / capability-index（重编 dist/pack 校验 0 error / 0 warning）。
  补全脚本：`candidates/_v15/gen_router_caps.py`（产出 22 卡 + 追加 YAML + 重算 destinations）。
- P2 五条（core-09 入场价位 / core-11 江恩警示 / p24-05 钟摆 / p24-13 小蝴蝶 / p24-17 复利）按用户范围决策
  降为引用，不单独成卡（已并入 22 张 router 卡的 A2 段或边界说明）。

## 备注
- 阶段 0 候选 skill 数 12–15 个（系统/心理层）+ 第二章 24 原理可选 8–11 个，最终由阶段 1.5 决定。
- 批判（时代/立场/假设/最强反对 4 条）将作为下游能力卡 B 段来源。
- 作者主要在期货验证，A股单边/做空受限 → B 段须标注适用边界。
