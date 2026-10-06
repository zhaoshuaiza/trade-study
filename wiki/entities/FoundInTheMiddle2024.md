---
type: entity
status: draft
created: 2026-10-07
updated: 2026-10-07
sources: ["[[2026-position-bias-mechanism]]"]
tags: [长上下文, 论文, 机制]
---

# Found in the Middle 2024

## 基本信息

| 项 | 值 |
|---|---|
| 标题 | Found in the Middle: Calibrating Positional Attention Bias Improves Long Context Utilization |
| 作者 | Cheng-Yu Hsieh, Yung-Sung Chuang, Chun-Liang Li, Zifeng Wang, Long T. Le, Abhishek Kumar, James Glass, Alexander Ratner, Chen-Yu Lee, Ranjay Krishna, Tomas Pfister |
| 机构 | IBM Research 等 |
| 时间 | 2024-06-23 |
| 会议 | **ACL Findings 2024**（pp. 14982-14995） |
| arXiv | [2406.16008](https://arxiv.org/abs/2406.16008) |

>注：与[[RULER2024]]的 Cheng-Ping Hsieh 同姓但为不同作者。

## 简介

[[U型注意力偏置]]的**经验层面**论证 + 校准方案。
证明了位置偏置独立于内容相关性，并给出**训练无关的推理时解法**。

## 三项贡献

1. **诊断**——建立 lost-in-the-middle 与 LLM **内在注意力偏置**的联系：
   U 型偏置使首尾 token 获得高注意力，无论是否相关
2. **缓解**——提出 `found-in-the-middle` 校准机制，
   让模型能忠实按相关性关注中间上下文
3. **验证**——RAG 性能提升**最多 15 个百分点**，优于 6 种对照方法

## 关键数据

| 指标 | 数值 |
|---|---|
| NaturalQuestions Recall@3，K=20，gold 在中间 | **20.52% → 68.32%** |
| 同上K=10 | **36.38% → 74.27%** |
| 端到端 QA | +6–15 个百分点 |
| 有效配置数 | **22/24** |

**数据集**：NaturalQuestions（2,655 条真实维基查询）、
SynthWiki（990 条 GPT-4 生成，排除记忆干扰）
**模型**：Vicuna-7b、Tulu-2-7b
**对照方法**：vanilla attention、query-generation ranking、
relevance-generation prompting、attention sorting、prompt reordering、
LongLLMLingua-rk

## 最重要的一句话

> 模型**确实**注意到了中间位置的相关信息，
> 但这个信号被首尾的注意力尖峰**淹没了**。

这把问题从「看不到」重新定义为「看到了但被淹没」——
前者需要让模型能访问，后者只需压低偏置。

## 三项局限（作者承认）

1. **线性分解假设可疑**——dummy 文档法假设偏置可分离可加，
   真实偏置可能与内容非线性交互
2. **成本未评估**——O(K) 前向传播，「可接受」但从未测延迟/成本
3. **偏置可能有用**——近因偏置可能正是模型正确加权近期记录的原因，
   无差别移除可能有害。**被承认但未被研究**

## 关系

- 概念：[[U型注意力偏置]]、[[拓扑U型]]
- 现象层：[[中间遗忘]]
- 来源：[[2026-position-bias-mechanism]]

## 时效性风险

被测模型是 **Vicuna-7b / Tulu-2-7b（2023 年代）**，
与当前前沿模型代际差距大。校准方法是否仍有效**尚未验证**。

## 来源

- [[2026-position-bias-mechanism]]