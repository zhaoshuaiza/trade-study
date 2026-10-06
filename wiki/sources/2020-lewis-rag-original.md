---
type: source
status: complete
created: 2026-10-06
updated: 2026-10-06
source_file: ".raw/2020-lewis-rag-original.md"
hash: 6bbe7b12c86467d2
author: "Lewis et al."
url: "https://arxiv.org/abs/2005.11401"
published: "2020-05-22"
ingested: 2026-10-06
tags: [RAG, 论文, 一手资料]
---

# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

## 出处

- 作者：Patrick Lewis 等12 人（Facebook AI Research）
- 链接：https://arxiv.org/abs/2005.11401
- 发表：NeurIPS 2020（2020-05-22 首发，2021-04-12 v4 修订）
- 原始文件：`.raw/2020-lewis-rag-original.md`
- 内容 hash：`6bbe7b12c86467d2`

## 摘要

论文针对参数化知识的三项缺陷（知识访问与精确操作能力有限、决策缺乏溯源、
世界知识难以更新），提出 RAG：把可微分访问的显式非参数记忆引入生成式模型。
具体做法是将预训练 seq2seq 作为参数化记忆、维基百科稠密向量索引作为非参数化记忆，
用预训练神经检索器访问。核心洞见是把原本不可微的检索变成可微的记忆访问，
使端到端联合微调成为可能。在三个开放域 QA 任务上取得 SOTA。

## 核心论点

1. **参数化知识的三个缺陷是可定位的。** 性能落后于任务专用架构、无法溯源、
   知识更新成本随规模上升——这三项都能通过引入非参数化记忆缓解。
2. **可微分访问是关键。** 此前「显式非参数记忆」只用于抽取式任务，
   扩展到生成式任务需要让检索参与端到端训练。
3. **RAG-Token 比 RAG-Sequence 更灵活。** 逐token 选择段落 vs 整个序列共用段落。

## 抽取出的页面

**概念**
- [[RAG]]
- [[参数化知识与外部知识]]

**实体**
- [[RAG论文2020]]

## 可验证性

- **事实**：作者归属、发表会议、arXiv 编号、两种变体的定义 —— 均为可核实的一手事实
- **实验结论**：「三个开放域 QA 任务 SOTA」「生成更具体/更多样/更符合事实」 ——
  是作者对自己实验的报告，**在其实验设定下成立**，不等同于普适结论。
  尤其"更具体、更多样"是主观描述，无严格量化指标。
- **未涉及**：多跳推理、查询改写等后续被证明关键的环节（见 [[2023-gao-rag-survey]]）

## 备注

这是本知识库的第一份资料，也是 [[RAG]] 概念的源头。
与 [[2023-gao-rag-survey]] 构成「原始提出 → 系统综述」的对照。
