---
type: entity
status: verified
created: 2026-10-07
updated: 2026-10-07
sources: ["[[2026-positional-failures-cre]]"]
tags: [长上下文, 评测, 位置效应, 2026]
---

# PositionalFailures2026

> **2026 年唯一一篇系统测量推理任务位置效应的论文**，同时发现整个领域的评测存在位置盲区。

## 基本信息

| 项 | 内容 |
|---|---|
| 标题 | Positional Failures in Long-Context LLMs: A Blind Spot in Reasoning Benchmarks |
| 作者 | Chuyifei Zhang、Hongyu Cui、Xiaowen Huang、Jitao Sang |
| 单位 | 北京交通大学 / 中南林业科技大学 |
| arXiv | **2605.23170** |
| 提交 | 2026-05-22 |
| 篇幅 | 20 页，**23 张表** |
| 状态 | ⚠️ **arXiv 预印本，未见同行评审** |

## 它要解决什么

此前所有位置效应证据（NIAH、RULER、NoLiMa）都来自**检索任务**。
本文问：**推理任务上位置效应同样存在吗？**

答案是**存在，而且可能更剧烈**。

## 核心贡献

### 1. 提出 CRE 框架

**Context Rot Evaluation** —— 同时控制三个因素：

```
任务位置 × 填充物内容 × 上下文长度
```

在 GSM8K 与 ARC-Challenge 上测试 **9 个模型**，分两轮
（5 个初始模型 + 4 个较新厂商版本）。

### 2. 量化了三个关键数字

| 发现 | 数据 |
|---|---|
| 最差情况 | MiMo-v2-Flash @ 64K：**−88pp**，中间准确率 **8%** |
| 次代改善 | MiMo-V2.5-Pro：收窄到 **−32pp** |
| 换填充物后 | `questions_only_v2`：四个模型**全部**退化 **−16 ～ −56pp** |

### 3. 诊断性验证（本文最硬的证据）

8K 条件下在**末尾追加一份目标任务副本** →
九个模型的中间位置准确率全部回到末尾基线 **±4pp** 内。

若只是「模型能力不足」，末尾副本不会有这种效果。**支持位置解释。**

### 4. 揭示评测盲区

- 审计 **11 个基准**：无一同时控制三因素用于推理
- 审计 **4 个厂商发布**：主结果表均无 NIAH/RULER 条目

## 为什么重要

它把「位置效应」从一个检索任务的工程现象，
**提升为影响整个评测体系可信度的结构性问题**。

## 局限

| 项 | 状态 |
|---|---|
| 同行评审 | ❌ **无** |
| 独立复现 | ❌ 未见 |
| 模型覆盖 | DeepSeek-V4-Pro、MiMo-V2.5-Pro、Kimi-K2.6、GLM-5.1。**GPT / Claude / Gemini 未在摘要列出** |

## 关系

- 来源：[[2026-positional-failures-cre]]
- 概念：[[填充物答案干扰]]、[[评测位置盲区]]
- 相关实体：[[NoLiMa2025]]、[[RULER2024]]、[[FoundInTheMiddle2024]]、[[LostInTheMiddle2023]]
- 相关观点：[[观点-位置效应在2025年仍未消失]]