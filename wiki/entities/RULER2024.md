---
type: entity
status: draft
created: 2026-10-06
updated: 2026-10-06
sources: ["[[2025-long-context-evidence]]"]
tags: [长上下文, 评估基准]
---

# RULER 2024

## 基本信息

| 项 | 值 |
|---|---|
| 全名 | RULER: What's the Real Context Size of Your Long-Context Language Models? |
| 作者 | Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, Boris Ginsburg |
| 机构 | **NVIDIA** |
| 时间 | 2024-04-09 首发 |
| 会议 | **COLM 2024** |
| arXiv | [2404.06654](https://arxiv.org/abs/2404.06654) |
| 代码 | NVIDIA/RULER（Apache 2.0） |

## 核心贡献：宣称长度 vs 有效长度

提出「**有效长度**」这一概念——模型平均分仍高于固定阈值
（**85.6%**，即 Llama-2-7B 在 4K 的分数）的最大输入长度。

阈值刻意定得低：这是「2023 年一个小模型在 4K 就能做到」的水平。

## 关键发现

**17 个模型全部宣称 32K+，只有一半能在 32K 达标。**

极端案例：

| 模型 | 宣称 | 有效 | 差距 |
|---|---|---|---|
| LWM (7B) | 1M | **<4K** | 差两个数量级 |
| DBRX | 32K | 8K | 4 倍 |
| GPT-4-1106-preview | 128K | 64K | 2 倍 |

**反直觉**：在 1M 窗口上训练的模型排名靠后，
而 32K 训练的模型通过外推胜出。**更大训练窗口不保证更好结果。**

## 基准设计

**13 个任务分4 类**：检索（Retrieval）、多跳追踪（Multi-hop Tracing）、
聚合（Aggregation）、问答（QA）。

**全部合成生成**——论文说明理由：合成输入减少对参数化知识的依赖，
而参数化知识会干扰长上下文输入的利用。生成可配置化，
序列长度与任务复杂度可任意设定。

每个任务每长度 500 个样本，全量运行可达 39,000 个评分样本。
用目标模型自己的 tokenizer 构造样本，确保测试的是真实窗口而非估算字数。

## 对 NIAH 的批评

作者认为 NIAH 测的是「一种**表层**的长上下文理解」——
多数模型NIAH 接近满分，但在RULER 的更难任务上随长度急剧下降。

## 关系

- 概念：[[宣称长度与有效长度]]、[[上下文腐蚀]]、[[中间遗忘]]
- 姊妹基准：[[NoLiMa2025]]（2025，ICML）、上下文腐蚀（Chroma 2025）
- 来源：[[2025-long-context-evidence]]

## 沿革

- 社区后续建立 RULER v1 / v2 双分支，v2 基于 NeMo-Skills 构建
- 被测模型从原始 17 个开源模型扩展到商业模型
  （Claude、GPT-4o 等）——**部分新行标星为「模型作者自报」而非 NVIDIA 复现**

## 来源

- [[2025-long-context-evidence]]
