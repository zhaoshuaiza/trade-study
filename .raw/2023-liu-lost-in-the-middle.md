---
title: Lost in the Middle: How Language Models Use Long Contexts
authors: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
year: 2023
venue: TACL 2023 (Transactions of the Association for Computational Linguistics)
arxiv: 2307.03172
url: https://arxiv.org/abs/2307.03172
ingested: 2026-10-06
---

# Lost in the Middle: How Language Models Use Long Contexts

## 摘要原文

While recent language models have the ability to take long contexts as input,
relatively little is known about how well they use longer context. We analyze the
performance of language models on two tasks that require identifying relevant
information in their input contexts: multi-document question answering and
key-value retrieval. We find that performance can degrade significantly when changing
the position of relevant information, indicating that current language models do not
robustly make use of information in long input contexts. In particular, we observe
that performance is often highest when relevant information occurs at the beginning or
end of the input context, and significantly degrades when models must access relevant
information in the middle of long contexts, **even for explicitly long-context models**.

Our analysis provides a better understanding of how language models use their input
context and provides new evaluation protocols for future long-context language models.

## 出版信息

- 首发：2023-07-06（v1）
- 修订：2023-11-20（v3）
- 会议：**TACL 2023**（Transactions of the Association for Computational Linguistics）
- 篇幅：18 页，16 张图
- 分类：cs.CL
- DOI: https://doi.org/10.48550/arXiv.2307.03172

## 核心发现：U 型性能曲线

改变「答案所在文档」在输入上下文中的位置，模型准确率呈明显的 **U 型**：

- **开头最好**（primacy bias，首位偏置）
- **结尾次之**（recency bias，近因偏置）
- **中间显著退化**

两个实验任务：多文档问答（multi-document QA）、键值检索（key-value retrieval）。

### 多文档问答实测数据（20 篇文档，Table 6）

| 模型 | 位置 0（开头） | 位置 4 | 位置 9（中间） | 位置 14 | 位置 19（结尾） |
|---|---|---|---|---|---|
| Claude-1.3 | 59.9% | 55.9% | 56.8% | 57.2% | 60.1% |
| Claude-1.3 (100K) | 59.8% | 55.9% | 57.0% | 57.4% | 60.0% |
| **GPT-3.5-Turbo** | **75.8%** | 57.2% | **53.8%** | 55.4% | 63.2% |
| GPT-3.5-Turbo (16K) | 75.7% | 57.3% | 54.1% | 55.4% | 63.1% |
| MPT-30B-Instruct | 53.7% | 51.8% | 52.2% | 52.7% | 56.3% |
| LongChat-13B (16K) | 68.6% | 57.4% | 55.3% | 52.5% | 55.0% |

**最惊人的发现**：GPT-3.5-Turbo 在中间位置（53.8%）的表现**低于闭卷基线
（closed-book，不看任何文档，约 56.1%）**。

> 也就是说：把正确文档放在中间位置，比根本不给文档**效果更差**。

### 30 篇文档时（Table 7）—— 上下文越长，中间的退化越严重

| 模型 | 位置 0 | 位置 9 | 位置 19 | 位置 24 | 位置 29（结尾） |
|---|---|---|---|---|---|
| Claude-1.3 | 59.1% | 54.8% | 56.4% | 56.2% | 59.9% |
| Claude-1.3 (100K) | 59.1% | 54.9% | 56.6% | 56.1% | 60.0% |
| **GPT-3.5-Turbo (16K)** | **73.4%** | **50.5%** | 51.8% | 54.9% | 63.7% |
| MPT-30B-Instruct | 51.6% | 51.2% | 49.6% | 51.3% | 54.1% |
| LongChat-13B (16K) | 66.9% | 52.5% | 52.2% | 51.3% | 55.1% |

GPT-3.5-Turbo (16K) 从位置 0 的 73.4% 跌到位置 9 的 50.5%，
**落差达 22.9 个百分点**。对比 20 文档时的75.7% → 54.1%（落差 21.6点），
可见退化在加长上下文时**不会自动缓解**。

## 关键结论：扩展上下文窗口不解决问题

GPT-3.5-Turbo 与 GPT-3.5-Turbo (16K) 的「准确率-位置」曲线**几乎完全重合**。
在两者都能容纳的prompt 长度下，16K 版本并未表现出更好的中间位置表现。

**这意味着**：扩大窗口主要只是「装得下更多 token」，而**没有教会模型更好地
使用中间位置**。论文摘要里那句 "even for explicitly long-context models"
（即使对显式长上下文模型）就是指这个。

Claude-1.3 (100K) 同样如此——曲线与 Claude-1.3 几乎一致。

## 键值检索任务：纯匹配任务也会退化

合成任务：给定若干 `{key, value}` 对（key/value 均为 128-bit UUID），
输入一个 key，要求返回对应的 value。这**不需要任何推理**，纯字符串匹配。

- Claude-1.3 与 Claude-1.3 (100K) 在所有位置和长度上**接近满分**
- GPT-3.5-Turbo、GPT-3.5-Turbo (16K)、MPT-30B-Instruct 呈现U 型曲线，
  中间位置明显下降，**在 140 或 300 个键值对时尤甚**

**意义**：这排除了「中间遗忘是因为语义理解困难」的解释。
连纯匹配都做不到，说明模型**根本没把注意力分配到中间信息**——
是「能不能看到」的问题，不是「能不能理解」的问题。

## 查询感知上下文化：有效但有限

把查询**同时放在数据之前和之后**（query-aware contextualization）：

- 键值检索任务上**几乎完全解决**问题，GPT-3.5-Turbo (16K) 在 300 对时达到 **100% 准确率**
- 但在真实的多文档问答上**只有微小差异**，U 型曲线依然存在

说明这个技巧对**结构化、单一答案**任务有效，对**开放域语义问答**帮助有限。

## 检索器-阅读器案例研究

开放式问答中，**阅读器性能在检索器召回率之前就已饱和**。

**关键推论**：增加检索到的文档数量，只会增加上下文长度，**不会成比例提升准确率**。
反而因为中间退化，更长的上下文可能**降低**表现。

## 架构与训练的影响

**编码器-解码器 vs 仅解码器**：
- Flan-UL2（编码器-解码器）在训练长度内（≤2048 token）位置鲁棒，
  最佳与最差位置差异仅 **约 1.9 个百分点**
- 但一旦超出训练长度（>2048），Flan-UL2 和 Flan-T5-XXL 也出现 U 型曲线

**指令微调**：
提升绝对准确率，但**未消除**首位/近因偏置。

**模型规模**：
较大的 Llama-2 变体比小变体呈现**更明显**的 U 型行为。
（反直觉：更大的模型并未自动获得位置鲁棒性）

## 论文性质说明

论文明确指出：
- 该结果是**对被测模型、提示词、任务的评测发现**，
  不应读作「所有长上下文模型都有完全相同的位置敏感性」
- 许多被测系统是**闭源模型**，无法把行为完全归因于架构、数据、对齐或服务细节
- 论文指出了一种**失效模式**，但**未提出架构层面的修复方案**；
  后续工作需在匹配条件下比较缓解策略

## 缓解方法（论文本身及后续实践总结）

论文主要做诊断而非提供方案。综合论文与后续实践的缓解思路：

1. **把最重要的内容放在开头或结尾**，而非中间
2. **重排序**：用reranker 对检索结果按相关性排序，把最相关的放末尾
   （利用近因偏置；U 型曲线不对称，尾部表现比中部高约 10 个百分点）
3. **查询感知上下文化**：查询放前后各一次
4. **限制有效上下文长度**：即使模型支持 100K+，也把实际 prompt 控制在较短范围
5. **锚定提示**：在回答前插入「以下是与问题最相关的句子：」等提示，
   显著提升中间位置召回

后续机制性解释与缓解工作（不在本篇范围）：
- *Found in the Middle*（Hsieh et al. 2024）—— 位置注意力偏置
  `Attn(d,k) = rel(d) + bias(k) + ε`，其中 bias(k) 呈 U 型
- 后续工作指出 74% 的错误案例中，最高注意力文档也是答案最常被反映的文档
