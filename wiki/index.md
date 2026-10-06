---
type: index
updated: 2026-10-06
---

# Wiki 总索引

> 查询入口。回答问题前先读本文件，再按需下钻，**不要全量加载 wiki/**。

## 统计

| 类别 | 数量 | 目录 |
|---|---|---|
| 概念 | 8 | `concepts/` |
| 实体 | 3 | `entities/` |
| 来源 | 3 | `sources/` |
| 观点 | 2 | `claims/` |
| 对比 | 1 | `comparisons/` |
| 综合 | 1 | `syntheses/` |
| 问答 | 0 | `questions/` |
| **合计** | **21** | |

另有 3 个支撑文件（不计入主题页面）：`overview.md`（全景）、`hot.md`（缓存）、
`log.md`（日志）。

## 主题地图

当前知识库聚焦 **RAG（检索增强生成）** 主题，另含方法论层面的 [[LLM Wiki]]。
以 [[RAG]] 为枢纽，向下分为四层：

- **概念层** — [[参数化知识与外部知识]]、[[稠密检索]]、[[重排序]]、
  [[中间遗忘]]、[[查询改写与HyDE]]、[[阅读器饱和]]
- **实体层** — [[RAG论文2020]]（源头）、[[RAG综述2023]]（三年演进全貌）、
  [[LostInTheMiddle2023]]（实证支撑）
- **观点层** — [[观点-RAG不彻底解决幻觉]]、
  [[观点-中间遗忘是上下文排序的硬约束]]
- **结构层** — [[RAG三代范式对比]] → [[RAG三年演进的核心逻辑]]（跨来源交叉结论）

另有 [[LLM Wiki]] 描述本知识库自身采用的架构，与上述主题互为参照。


## 概念 Concepts

- [[RAG]] — 检索增强生成，⭐ 枢纽
- [[参数化知识与外部知识]] — 双记忆的存储与更新成本差异
- [[稠密检索]] — 向量语义检索及其与稀疏检索的取舍
- [[重排序]] — 后检索阶段把最相关挪到边缘
- [[中间遗忘]] — 长上下文位置效应，✅ **status: verified**
- [[阅读器饱和]] — 加更多检索文档收益趋零
- [[查询改写与HyDE]] — 查询侧表示转换
- [[LLM Wiki]] — 编译时知识组织方法论

## 实体 Entities

- [[RAG论文2020]] — Lewis et al., NeurIPS 2020，RAG 原始提出
- [[RAG综述2023]] — Gao et al., 2023-12，三代范式分类法
- [[LostInTheMiddle2023]] — Liu et al., TACL 2023，位置效应实证

## 来源 Sources

- [[2020-lewis-rag-original]] — 原始论文，hash `6bbe7b12c86467d2`
- [[2023-gao-rag-survey]] — 综述论文，hash `a0008debd48ea096`
- [[2023-liu-lost-in-the-middle]] — 实证论文，hash `a1555c45066a79ef`

## 观点 Claims

- [[观点-RAG不彻底解决幻觉]] — verifiable: partial
- [[观点-中间遗忘是上下文排序的硬约束]] — ✅ **verifiable: verified**（已闭环）

## 对比 Comparisons

- [[RAG三代范式对比]] — Naive / Advanced / Modular

## 综合理解 Syntheses

- [[RAG三年演进的核心逻辑]] — 上下文质量控制权的转移

## 问答归档 Questions

_尚无内容。_

## 支撑文件

- `overview.md` — 知识库全景与架构说明
- `hot.md` — 近期上下文缓存（新会话首读）
- `log.md` — 操作日志（append-only）

---

## 待补充的知识点

按优先级排列，供定向摄入或 `/autoresearch` 使用：

1. **[最高优先级]** **2024-2025 年模型的位置敏感性实证** ——
   [[LostInTheMiddle2023]] 被测模型为2023 年的 GPT-3.5-Turbo / Claude-1.3，
   已过时。当前模型（GPT-4o、Claude 3.x、Gemini 1.5）是否仍有U 型曲线、
   落差多大，直接决定 [[RAG]] 与长上下文的边界判断
2. **位置注意力偏置的机制解释** ——
   `Attn(d,k) = rel(d) + bias(k) + ε` 模型（Hsieh et al. 2024, *Found in the Middle*），
   补上可回答「为什么会这样」
3. **Agentic RAG** —— 2023-12 之后成型，超出综述覆盖范围
4. **带幻觉率量化指标的 RAG 评测基准**（RAGTruth 等），用于升级
   [[观点-RAG不彻底解决幻觉]] 从 `partial` 到 `confirmed`
5. **Karpathy 的 LLM Wiki 原始构想文档** —— 当前 [[LLM Wiki]] 仅有中文二手转述
6. **2024-2025 RAG 新进展**：多模态 RAG、图 RAG、缓存策略

## 已完成

- [x] ~~[[中间遗忘]] 原始实证论文（Liu et al.）~~ —— **2026-10-06 完成**，
      hash `a1555c45066a79ef`，`中间遗忘` 与
      [[观点-中间遗忘是上下文排序的硬约束]] 均已升级为 verified
