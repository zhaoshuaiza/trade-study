---
type: concept
status: verified
created: 2026-10-06
updated: 2026-10-06
sources: ["[[2025-long-context-evidence]]"]
tags: [长上下文, 评估基准]
---

# NoLiMa 2025

## 基本信息

| 项| 值 |
|---|---|
| 名称 | NoLiMa: Long-Context Evaluation Beyond Literal Matching |
| 作者 | Ali Modarressi, Hanieh Deilamsalehy, Franck Dernoncourt, Trung Bui, Ryan A. Rossi, Seunghyun Yoon, Hinrich Schütze |
| 机构 | Adobe Research 等 |
| 时间 | 2025-02-07 首发，2025-07-09 v3 |
| 会议 | **ICML 2025**（PMLR 267, pp. 44554-44570） |
| arXiv | [2502.05167](https://arxiv.org/abs/2502.05167) |
| 代码 | github.com/adobe-research/NoLiMa |

## 解决的问题

标准 NIAH 测试的**捷径问题**：问题与 needle 文本高度重合，
模型可以靠**字面匹配**完成任务，不必真正理解语义。

NoLiMa 重新设计 needle 集合，使**问题与 needle 的词汇重叠最小化**，
模型必须通过**推断潜在关联**来定位答案。

## 关键数据

| 条件 | 结果 |
|---|---|
| 短上下文（<1K） | 表现良好 |
| **32K 上下文** | **13 个模型中 11 个跌破短上下文基线的 50%** |
| **GPT-4o（表现最好者）** | **99.3% → 69.7%** |

## 两个加重因素

**1. 推理能力不救场。** 具备推理能力或使用 CoT 提示的模型，
在长上下文中同样难以维持表现。

**2. 注意力机制负担。** 作者分析认为退化源于——
「长上下文中缺少字面匹配时，注意力机制面临更大困难，更难检索相关信息」。

## 与 Liu et al. 的互补关系

两篇论文消除干扰的手法不同，因而结论可互相印证：

| | 消除什么干扰 | 测什么能力 |
|---|---|---|
| [[LostInTheMiddle2023]]（键值检索） | **语义**干扰（UUID 零语义） | 「能不能看到」 |
| **NoLiMa** | **字面匹配**捷径 | 「能不能理解地找到」 |

两者都指向同一结论：长上下文检索困难，**且不限于简单匹配**。

## 意义

**这是 2025 年最重要的长上下文评测之一**，因为它证明：
NIAH 的高分是**字面匹配的产物**，不代表真实长上下文能力。

配合 [[RULER2024]]（宣称 vs 有效长度）与[[上下文腐蚀]]（18 模型全部退化），
构成 2024-2025 的完整证据链。

## 关系

- 概念：[[中间遗忘]]、[[上下文腐蚀]]、[[宣称长度与有效长度]]
- 观点：[[观点-位置效应在2025年仍未消失]]
- 来源：[[2025-long-context-evidence]]

## 疑问

- [ ] 论文能否提供逐模型的完整退化曲线（非仅 32K 单点）？
      若能，可与 Liu et al. 的 U 型曲线直接叠合对比

## 来源

- [[2025-long-context-evidence]]
