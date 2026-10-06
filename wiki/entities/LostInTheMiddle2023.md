---
type: entity
status: draft
created: 2026-10-06
updated: 2026-10-06
sources: ["[[2023-liu-lost-in-the-middle]]"]
tags: [长上下文, 论文]
---

# Lost in the Middle 2023

## 基本信息

| 项 | 值 |
|---|---|
| 标题 | Lost in the Middle: How Language Models Use Long Contexts |
| 作者 | Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang |
| 时间 | 2023-07-06 首发，2023-11-20 v3 |
| 会议 | **TACL 2023** |
| 篇幅 | 18 页，16 图 |
| arXiv | [2307.03172](https://arxiv.org/abs/2307.03172) |

## 简介

[[中间遗忘]] 概念的**原始实证来源**。用受控实验证明：模型对长上下文的位置
敏感，准确率呈 U 型曲线，且**扩大窗口无法缓解**。

## 关键贡献

1. 把「模型能否使用长上下文」从能力问题转化为**可测量的位置效应问题**
2. 两个受控任务：多文档问答、键值检索（后者排除理解因素的干扰）
3. 完整数据表格，展示 5-6 个模型 × 多个位置的准确率
4. 关键对照：GPT-3.5-Turbo vs 16K 版本、Claude-1.3 vs 100K 版本
5. 检索器-阅读器饱和现象的实证
6. 提出面向未来长上下文模型的**新评测协议**

## 被测模型

GPT-3.5-Turbo、GPT-3.5-Turbo (16K)、Claude-1.3、Claude-1.3 (100K)、
MPT-30B-Instruct、LongChat-13B (16K)，附录含更多模型。
编码器-解码器侧：Flan-UL2、Flan-T5-XXL。

## 重要时代局限

**被测模型截至 2023 年已过时。** GPT-3.5-Turbo、Claude-1.3 均为上一代。
论文的核心机制发现应仍成立，但**具体数字不可外推**到当前模型。

这是本知识库中时效性风险最高的一页，引用时应注意。

## 关系

- 概念：[[中间遗忘]]、[[阅读器饱和]]
- 观点：[[观点-中间遗忘是上下文排序的硬约束]]
- 来源页：[[2023-liu-lost-in-the-middle]]
- 同作者：[[RAG论文2020]]（Fabio Petroni 共同作者）

## 谱系线索

Fabio Petroni 参与了 2020 年的 RAG 论文与本篇长上下文研究，
构成 2020→2023 的技术转向轨迹：先解决「如何注入知识」，
再研究「注入后模型能否用好」。

## 来源

- [[2023-liu-lost-in-the-middle]]
