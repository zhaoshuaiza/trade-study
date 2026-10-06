---
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
authors: Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela
year: 2020
venue: NeurIPS 2020
arxiv: 2005.11401
url: https://arxiv.org/abs/2005.11401
ingested: 2026-10-06
---

# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

## 摘要原文

Large pre-trained language models have been shown to store factual knowledge in their
parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP
tasks. However, their ability to access and precisely manipulate knowledge is still
limited, and hence on knowledge-intensive tasks, their performance lags behind
task-specific architectures. Additionally, providing provenance for their decisions
and updating their world knowledge remain open research problems. Pre-trained models
with a differentiable access mechanism to explicit non-parametric memory can overcome
this issue, but have so far been only investigated for extractive downstream tasks.
We explore a general-purpose fine-tuning recipe for retrieval-augmented generation
(RAG) -- models which combine pre-trained parametric and non-parametric memory for
language generation.

We introduce RAG models where the parametric memory is a pre-trained seq2seq model
and the non-parametric memory is a dense vector index of Wikipedia, accessed with a
pre-trained neural retriever. We compare two RAG formulations, one which conditions
on the same retrieved passages across the whole generated sequence, the other can
use different passages per token. We fine-tune and evaluate our models on a wide
range of knowledge-intensive NLP tasks and set the state-of-the-art on three open
domain QA tasks, outperforming parametric seq2seq models and task-specific
retrieve-and-extract architectures. For language generation tasks, we find that RAG
models generate more specific, diverse and factual language than a
state-of-the-art parametric-only seq2seq baseline.

## 出版信息

- 首次提交：2020-05-22（v1）
- 最新修订：2021-04-12（v4）
- 会议：NeurIPS 2020
- 分类：cs.CL（计算与语言）、cs.LG（机器学习）
- DOI: https://doi.org/10.48550/arXiv.2005.11401

## 要解决的问题

论文明确列出参数化知识的三个缺陷：

1. **知识访问与精确操作能力有限。** 知识密集型任务上，性能落后于任务专用架构。
2. **决策溯源（provenance）缺失。** 无法说明某个结论的依据来自哪里。
3. **世界知识难以更新。** 参数里的知识是训练时快照，之后要改就得重训。

第三条是最要命的：知识的更新成本与模型规模正相关。

## 方法

### 双记忆架构

RAG 模型同时使用两种记忆：

- **参数化记忆（parametric memory）**：预训练的 seq2seq 模型，存语法、风格、通用语言能力。
- **非参数化记忆（non-parametric memory）**：维基百科的稠密向量索引，通过预训练神经检索器访问。

论文提出的核心洞见是：把「不可微地检索」变成「**可微分地访问显式非参数记忆**」，
于是整个系统可以端到端微调。此前这类结构只用于抽取式任务，本文扩展到**生成式**任务。

### 两种 RAG 变体

论文比较了两种形式化，这是文章最有价值的技术区分：

| 变体 | 检索粒度 | 特点 |
|---|---|---|
| **RAG-Sequence** | 整个生成序列共用同一批检索段落 | 段落选择是全局决策 |
| **RAG-Token** | **每个 token 可用不同段落** | 段落选择是逐 token 决策 |

RAG-Token 更灵活：不同句子可以依赖不同来源。代价是检索更频繁。

## 结论

- 在三个开放域问答任务上取得当时最优（SOTA），超过参数化 seq2seq 模型和任务专用的
  retrieve-and-extract 架构。
- 在语言生成任务上，RAG 模型比当时最优的纯参数化 seq2seq 基线生成**更具体、更多样、
  更符合事实**的语言。

## 局限

- 训练需要索引与检索器同步微调，成本高。
- 检索范围限于维基百科快照，世界知识的新增依赖索引重建。
- 论文本身未涉及多跳推理、查询改写等后续被证明关键的环节。
