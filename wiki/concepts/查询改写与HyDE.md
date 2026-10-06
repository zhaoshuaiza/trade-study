---
type: concept
status: draft
created: 2026-10-06
updated: 2026-10-06
sources: ["[[2023-gao-rag-survey]]"]
tags: [RAG, 检索优化, 查询处理]
---

# 查询改写与 HyDE

> 把用户模糊的问题，转成更适合检索的查询表示。

## 定义

**查询重写（query rewriting）**：改写原始查询以提升检索效果。

**HyDE（Hypothetical Document Embeddings）**：先让大模型**生成一个假设性答案**，
再用这个假设答案去计算与文档的相似度。

**多查询扩展（multi-query expansion）**：把一个问题扩展成多个查询，合并召回结果。

## 为什么有效

用户的原始提问通常不是好的检索查询——口语化、含指代、语义模糊。
这三类技术都在**查询侧**把自然语言问题映射到检索友好的表示。

## 所属阶段

属于**预检索**（pre-retrieval）优化：Advanced RAG 范式在检索前插入的加工环节。

## 关系

- 上位概念：[[RAG]]
- 同阶段其他技术：细粒度分割、Small2Big、滑动窗口、元数据增强（见[[稠密检索]]）
- 后续环节：[[重排序]]

## 来源

- [[2023-gao-rag-survey]]
