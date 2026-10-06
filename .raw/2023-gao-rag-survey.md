---
title: Retrieval-Augmented Generation for Large Language Models: A Survey
authors: Yunfan Gao, Yunxiang Zhou, Peng Li, Siqian Kong
year: 2023
arxiv: 2312.10997
url: https://arxiv.org/abs/2312.10997
ingested: 2026-10-06
---

# Retrieval-Augmented Generation for Large Language Models: A Survey

## 摘要要点

Large language models (LLMs) demonstrate powerful capabilities, but they still face
challenges in practical applications, such as hallucinations, slow knowledge updates,
and lack of transparency in answers. Retrieval-Augmented Generation (RAG) refers to the
retrieval of relevant information from external knowledge bases before answering
questions with LLMs. RAG has been demonstrated to significantly enhance answer
accuracy, reduce model hallucination, particularly for knowledge-intensive tasks.

RAG effectively combines the parameterized knowledge of LLMs with non-parameterized
external knowledge bases.

## 背景动因

LLM 落地的三个具体障碍：

1. **幻觉**（hallucination）——生成不实内容
2. **知识更新慢**（slow knowledge updates）——参数化知识是静态快照
3. **答案不透明**（lack of transparency）——用户无法验证

RAG 的额外价值：**引用来源**，用户可自行核实，从而提升信任。

## 三个范式（本文核心分类）

### Naive RAG（朴素 RAG）

传统「索引 → 检索 → 生成」三段式流程。

**缺陷：**
- 检索**精度低**（precision）：选中的文本块与问题错位
- 检索**召回率低**（recall）：遗漏相关文本块
- 可能把**过期信息**喂给模型——恰是 RAG 本该先解决的问题
- 由此引发幻觉与不准确回答
- 增强环节引入**冗余与重复**
- 多段落检索时，排序与风格/语气的协调也是难点
- 半结构化数据（如含表格的 PDF）会被传统文本切分破坏完整性，导致输出逻辑与语调连贯性受损

### Advanced RAG（高级 RAG）

在检索**前后**插入优化环节，提升上下文质量。

**预检索（pre-retrieval）** —— 优化数据索引，五种手段：
1. 增强数据粒度（enhancing data granularity）
2. 优化索引结构（optimizing index structures）
3. 添加元数据（adding metadata）
4. 对齐优化（alignment optimization）
5. 混合检索（mixed retrieval）

具体技术：滑动窗口、细粒度分割（以命题为检索单元）、Small2Big 策略（检索小句子但
输入大上下文）。检索阶段可通过微调 embedding 模型或使用动态 embedding
（如 OpenAI 的 embeddings-ada-002）提升。

**查询侧优化**：查询重写（query rewriting）、多查询扩展（multi-query expansion）、
HyDE（生成假设性答案再算相似度）。

**后检索（post-retrieval）**：
- **重排（reranking）**——把最相关文档移到提示词边缘
- 用小型语言模型**过滤或压缩**无关 token

**关键洞察——「中间遗忘」（lost in the middle）**：长上下文中间位置的信息容易被忽略，
所以要把最相关的挪到边缘。

### Modular RAG（模块化 RAG）

打破固定链式结构，重构为**可自由插拔的组件网络**。新增：

- **路由（routing）**——在不同数据源间导航
- **记忆（memory）**——利用 LLM 输出构建自我增强的记忆池
- **预测（predicting）**——直接生成上下文以减少外部噪声

**三种增强过程：**
- **迭代检索（iterative）**——检索与生成交替进行
- **递归检索（recursive）**——用思维链拆解子问题，逐步细化搜索
- **自适应检索（adaptive）**——如 FLARE、Self-RAG，通过监控生成概率或生成「反思令牌」，
  让模型自主决定是否触发检索、何时停止

## 与微调、提示工程的对比

| 方法 | 作用层次 | 是否需要训练 |
|---|---|---|
| RAG | 补充外部知识 | 否 |
| Fine-Tuning | 适配模型行为 | 是 |
| Prompt Engineering | 挖模型内在能力 | 否 |

三者互补，非互斥。

## 评估指标

- 答案准确性（answer accuracy）
- 检索精度/召回（retrieval precision/recall）
- 归因质量（attribution quality）
- 幻觉率（hallucination rate）

基准：Natural Questions、TriviaQA、HotpotQA（多跳）、ASQA（歧义问题）

## 未来方向

纵向优化、横向扩展、技术栈与生态建设。多模态（视觉、听觉）数据整合是明确方向。

## 对比方法

论文指出 RAG 的检索策略源自传统信息检索（BM25、TF-IDF），但 LLM 时代演进出
稀疏检索、稠密检索（embedding、双编码器）、混合方案，以及**任务微调检索器**。
