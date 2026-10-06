---
type: source
status: complete
created: 2026-10-06
updated: 2026-10-06
source_file: ".raw/2023-gao-rag-survey.md"
hash: a0008debd48ea096
author: "Gao et al."
url: "https://arxiv.org/abs/2312.10997"
published: "2023-12"
ingested: 2026-10-06
tags: [RAG, 综述, 一手资料]
---

# Retrieval-Augmented Generation for Large Language Models: A Survey

## 出处

- 作者：Yunfan Gao, Yunxiang Zhou, Peng Li, Siqian Kong
- 链接：https://arxiv.org/abs/2312.10997
- 发表：2023-12，arXiv 预印本
- 原始文件：`.raw/2023-gao-rag-survey.md`
- 内容 hash：`a0008debd48ea096`

## 摘要

综述 LLM 时代的 RAG 技术。指出 LLM 落地的三大障碍：幻觉、知识更新慢、
答案不透明。核心贡献是把 RAG 演进划分为**Naive / Advanced / Modular** 三代范式，
并按**检索器、生成器、增强方法**三大组件加评估体系来组织全貌。

## 核心论点

1. **Naive RAG 的问题是机制性的，不是调参能解决的。** 检索精度低、召回率低、
   可能喂入过期信息——而喂过期信息恰恰是 RAG 本该先解决的事。
2. **Advanced RAG 在检索前后插入优化。** 预检索侧优化索引（粒度、结构、元数据、
   对齐、混合检索）与查询表示（重写、多查询扩展、HyDE）；后检索侧重排与压缩。
3. **长上下文有「中间遗忘」问题。** 上下文中间位置的信息影响力显著低于边缘，
   所以要把最相关的挪到边缘——这是重排序策略的直接动因。
4. **Modular RAG 是结构升级。** 从固定链式变成可插拔组件网络，新增路由、记忆、预测模块；
   检索与生成的关系从单次变为迭代、递归、自适应三种。
5. **RAG、微调、提示工程互补而非互斥。**

## 抽取出的页面

**概念**
- [[RAG]]
- [[参数化知识与外部知识]]
- [[稠密检索]]
- [[中间遗忘]]（标记 uncertain —— 缺原始实证论文）
- [[重排序]]
- [[查询改写与HyDE]]
- [[RAG三代范式对比]]

**实体**
- [[RAG综述2023]]

**观点**
- [[观点-RAG不彻底解决幻觉]]
- [[观点-中间遗忘是上下文排序的硬约束]]

## 可验证性

- **事实**：范式分类、组件划分、基准数据集名称 —— 综述的归纳结论，属二手整理
- **需溯源**：[[中间遗忘]] 的原始实证研究（Liu et al.）综述未给全称，
  已标`status: uncertain`，待补摄入
- **主观性**：Adaptive RAG 部分对 FLARE / Self-RAG 的效果描述缺乏统一量化对比
- **时效**：2023-12 出版，2024-2025 年的新进展（多模态 RAG、Agentic RAG、
  长上下文对RAG 的冲击）**不在本篇覆盖范围**，需另行补足

## 备注

与 [[2020-lewis-rag-original]] 互为补充：2020 提供原始机制，2023 提供三年演进全貌。
本篇的[[RAG三代范式对比]] 是本知识库目前最有复用价值的结构化结论。
