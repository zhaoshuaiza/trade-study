---
title: "2024-2025 长上下文位置效应实证：NoLiMa / RULER / Context Rot"
authors: "Ali Modarressi et al. (NoLiMa, Adobe Research) / Cheng-Ping Hsieh et al. (RULER, NVIDIA) / Kelly Hong, Anton Troynikov, Jeff Huber (Context Rot, Chroma)"
year: 2024-2025
venues: ICML 2025 / COLM 2024 / Chroma 技术报告 2025-07
arxiv: "2502.05167 / 2404.06654 / trychroma.com/research/context-rot"
ingested: 2026-10-06
---

# 2024-2025 长上下文位置效应实证

## 本资料要回答的问题

[[2023-liu-lost-in-the-middle]] 的被测模型是 2023 年的 GPT-3.5-Turbo / Claude-1.3，
已过时。核心问题：**当前模型（2024-2025，GPT-4o/4.1、Claude 4系列、Gemini 2.5、
Qwen3）是否已改善 U 型曲线？**

**结论：没有。三项独立研究用不同方法得到一致答案。**

---

## 证据一：NoLiMa（ICML 2025，Adobe Research）

**基本信息**
- 标题：NoLiMa: Long-Context Evaluation Beyond Literal Matching
- 作者：Ali Modarressi, Hanieh Deilamsalehy, Franck Dernoncourt, Trung Bui,
  Ryan A. Rossi, Seunghyun Yoon, Hinrich Schütze
- arXiv: 2502.05167（2025-02-07 首发，2025-07-09 v3）
- 会议：**ICML 2025**（PMLR 267, pp. 44554-44570）
- 代码：github.com/adobe-research/NoLiMa

**方法创新：去掉字面匹配的捷径**

标准 NIAH（needle-in-a-haystack）测试的问题是：问题与needle 文本高度重合，
模型可以靠**字面匹配**完成任务，无需真正理解语义。NoLiMa 重新设计 needle 集合，
使**问题与 needle 的词汇重叠最小化**，模型必须通过**推断潜在关联**来定位答案。

**这与Liu et al. 的键值检索任务形成互补**：
- Liu et al. 用 UUID 消除**语义**干扰，测「能不能看到」
- NoLiMa 消除**字面匹配**捷径，测「能不能理解地找到」

**关键数据**

| 条件 | 结果 |
|---|---|
| 短上下文（<1K） | 表现良好 |
| 32K 上下文 | **13 个模型中 11 个跌破短上下文基线的 50%** |
| **GPT-4o（表现最好的例外）** | **从 99.3% 降至 69.7%** |

即使是被评为top-performing 的 GPT-4o，也损失了约 30 个百分点。

**两个加重因素**

1. **推理能力不救场**：具备推理能力或用 CoT 提示的模型，
   在长上下文中同样难以维持表现
2. **注意力机制负担**：作者分析认为退化源于
   「长上下文中缺少字面匹配时，注意力机制面临更大困难，更难检索相关信息」

**被测范围**：13 个宣称支持至少 128K 的 LLM。

---

## 证据二：RULER（COLM 2024，NVIDIA）

**基本信息**
- 标题：RULER: What's the Real Context Size of Your Long-Context Language Models?
- 作者：Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya,
  Dima Rekesh, Fei Jia, Yang Zhang, Boris Ginsburg
- arXiv: 2404.06654，**COLM 2024**，代码 NVIDIA/RULER（Apache 2.0）

**核心概念：宣称长度 vs 有效长度**

- **Claimed length**：厂商宣传的最大上下文窗口
- **Effective length**：模型平均分仍高于阈值（**85.6%**，即 Llama-2-7B 在 4K 的分数）
  的最大输入长度

**关键数据：宣称 vs 有效**

| 模型 | 宣称 | 有效 |
|---|---|---|
| Gemini-1.5-Pro | 1M | >128K |
| GPT-4-1106-preview | 128K | 64K |
| Llama3.1-70B | 128K | 64K |
| Command-R-plus | 128K | 32K |
| Mistral (7B) | 32K | 16K |
| DBRX | 32K | 8K |
| **LWM (7B)** | **1M** | **<4K** |
| LongChat (7B) | 32K | <4K |

**17 个模型全部宣称 32K+，但只有一半能在 32K 达标。**
LWM 宣称 1M、有效不足 4K——**差两个数量级**。

**反直觉发现**：在 1M 窗口上训练的模型排名靠后，
而一个 32K 训练的模型通过外推胜出。**更大训练窗口不保证更好结果。**

**13 个任务分4 类**：检索、多跳追踪、聚合、问答。
RULER 作者批评 NIAH「只indicates一种表层的长上下文理解」。

---

## 证据三：Context Rot（Chroma 技术报告 2025-07）

**基本信息**
- 标题：Context Rot: How Increasing Input Tokens Impacts LLM Performance
- 作者：Kelly Hong, Anton Troynikov, Jeff Huber（Chroma Research）
- 发布：2025-07-14
- 代码：github.com/chroma-core/context-rot（MIT）
- Hacker News 260 分59 条评论热度

**实验设计的关键优势：保持任务复杂度恒定，只变输入长度。**
作者明确指出设计难点——「任务常随输入变长而变复杂，导致无法区分
性能下降究竟源于更长输入还是题目本身变难」。他们把这个问题隔离掉了。

**被测 18 个模型**，包含当时最强的一批：

- Anthropic：Claude Opus 4、Sonnet 4、Sonnet 3.7、Sonnet 3.5、Haiku 3.5
- OpenAI：o3、GPT-4.1（含 mini/nano）、GPT-4o、GPT-4 Turbo、GPT-3.5 Turbo
- Google：Gemini 2.5 Pro、2.5 Flash、2.0 Flash
- Qwen3：235B、32B、8B

**核心结论：18 个模型全部退化，无一例外。**

具体发现：

| 发现 | 内容 |
|---|---|
| 长度本身即成本 | 在加任何干扰项之前，**纯长度就造成约 7.9% 的准确率地板损失** |
| 语义相似度影响 | needle 与问题相似度**越低，退化越快** |
| 干扰项会叠加 | 加入 1 个、再加 4 个干扰项，性能持续下降 |
| 失败方式因家族而异 | **GPT 倾向幻觉；Claude 倾向拒答**（明确说找不到） |
| 思考模式不解决 | 缩小但未消除「聚焦片段 vs 完整历史」的差距 |
| LongMemEval | 给出**约 113K token 完整对话**不如给**约 300 token 相关片段** |

**最反直觉的发现：打乱顺序比逻辑连贯更可靠。**

在全部 18 个模型上，**随机打乱的 haystack 检索表现优于逻辑连贯的 haystack**。
作者解释：连贯的上下文创造了**更貌似相关的干扰项**，模型更容易被误导。

这直接反驳了「把检索结果整理得有条理更好」的直觉。

---

## 交叉验证：三者的一致结论

| 维度 | NoLiMa | RULER | Context Rot |
|---|---|---|---|
| 消除字面匹配 | ✅ 核心设计 | 部分 | ✅ 语义 needle |
| 控制任务难度 | — | ✅ | ✅ 复杂度恒定 |
| 消除字面匹配捷径 | ✅ | ✅ | ✅ |
| 被测模型数 | 13 | 17 | 18 |
| 结论 | 32K 时11/13 跌破基线 50% | 宣称 32K+ 仅半数达标 | 18/18 全部退化 |

**三者方法完全不同，但指向同一结论。**

---

## 机制解释

**注意力稀释（attention dilution）**

Transformer 的自注意力复杂度为 `C_attn(n) = O(n² · d)`。
10万token 需处理约 100 亿个成对关系。随着序列变长，
任何特定 token 的信号被稀释。

**位置偏置的存在性**

后续理论工作（*Lost in the Middle at Birth*，ICML 2025）
提出 U 型曲线在**随机初始化时即已存在**——它是拓扑性的，
训练并未「爬出」这个谷。RoPE 的有无不改变U 形。

---

## 关键结论

**1. 位置效应没有消失。** 2025 年的 Claude 4系列、GPT-4.1、Gemini 2.5
仍然呈现中间退化。**Llama-2-7B 在 4K 的水平，是 2026 年许多模型在 32K 都达不到的。**

**2. 扩大窗口依然不解决问题。** 这一点从 2023 到 2025 结论未变。
Context Rot 的「纯长度地板」概念更直白：**长度本身就是成本**，
不是只有干扰项才有害。

**3. 打乱顺序优于逻辑连贯**（18/18 模型）——
这与「把文档整理成连贯结构帮助理解」��直觉相反。

**4. 对 RAG 的直接含义**：
[[RAG]] 与长上下文不是替代关系，而是**分工**关系。
长上下文负责「装得下」，RAG 负责「挑得准 + 放对位置」。
Context Rot 的数据支持这一点：给 300 token 相关片段**优于**给 113K 完整对话。

**5. 推理能力不救场。** CoT 与推理模型在长上下文中同样退化，
这排除了「等模型变强就自然解决」的乐观预期。

## 局限与注意

- Chroma 是向量数据库厂商，**有商业动机**关注长上下文缺陷，
  解读其结论时应保留这一背景（其结论与其他独立研究一致，可交叉信任）
- 各研究任务设置不同，**具体数字不可跨研究直接比较**
- LongBench v2（清华，2024-12）显示：在**真实长文本**推理任务上，
  人类专家在 15 分钟限制下也仅达**53.7%**准确率——
  这说明真实长上下文任务本身极难，不能全归因于模型缺陷
- 「当前模型」的时效性：报告发布于 2025 年中，
  2026 年的模型表现需重新评测

## 关联

- [[中间遗忘]]（原始实证，2023）
- [[阅读器饱和]]
- [[LostInTheMiddle2023]]
- [[NoLiMa2025]]（新建）
- [[RULER2024]]（新建）
- [[上下文腐蚀]]（新建，Context Rot 的中文命名）
