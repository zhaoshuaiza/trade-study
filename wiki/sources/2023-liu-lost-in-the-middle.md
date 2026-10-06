---
type: source
status: complete
created: 2026-10-06
updated: 2026-10-06
source_file: ".raw/2023-liu-lost-in-the-middle.md"
hash: a1555c45066a79ef
author: "Liu et al."
url: "https://arxiv.org/abs/2307.03172"
published: "2023-07-06"
ingested: 2026-10-06
tags: [长上下文, 论文, 一手资料]
---

# Lost in the Middle: How Language Models Use Long Contexts

## 出处

- 作者：Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape,
  Michele Bevilacqua, Fabio Petroni, Percy Liang
- 链接：https://arxiv.org/abs/2307.03172
- 发表：**TACL 2023**（2023-07-06 首发，2023-11-20 v3）
- 篇幅：18 页，16 图
- 原始文件：`.raw/2023-liu-lost-in-the-middle.md`
- 内容 hash：`a1555c45066a79ef`

## 摘要

研究模型**如何使用**长输入上下文（而非是否能接收）。在多文档问答与键值检索
两个任务上，改变相关信息的位置会显著改变性能——**呈U 型曲线**：
开头最好、结尾次之、中间显著退化，**即使对显式长上下文模型也是如此**。

## 核心论点

1. **位置效应真实存在且量级可观。** GPT-3.5-Turbo 中间位置（53.8%）
   甚至**低于闭卷基线**（56.1%）——给错位置的正确文档比不给更糟。
2. **扩大上下文窗口不解决问题。** GPT-3.5-Turbo 与 16K 版本曲线几乎重合；
   Claude-1.3 与 100K 版本同样如此。窗口变长主要是「装得下」，
   不是「用得好」。
3. **退化不是理解问题。** 连UUID 键值匹配这种零推理任务也退化，
   证明是注意力分配问题——「能不能看到」而非「能不能理解」。
4. **模型规模不带来鲁棒性。** 更大的 Llama-2 变体U 型更明显；
   指令微调不消除位置偏置。
5. **阅读器性能早于检索器召回饱和。** 加更多检索文档不提升准确率，
   只增加上下文长度与成本。

## 抽取出的页面

**概念**
- [[中间遗忘]]（从 uncertain **升级为 verified**）
- [[阅读器饱和]]（新建）

**实体**
- [[LostInTheMiddle2023]]（新建）

**观点**
- [[观点-中间遗忘是上下文排序的硬约束]]（从 uncertain **升级为 verified**）

## 可验证性

- **事实**：全部数据表格（Table 6/7）、会议归属（TACL 2023）、作者列表 —— 可核实
- **量化结论**：U 型曲线幅度、闭卷基线对比、16K vs 原版曲线重合 —— **一手实验数据**
- **注意**：被测模型截至 2023 年，**GPT-3.5-Turbo / Claude-1.3 现已过时**。
  论文位置效应的**机制**应仍成立，但**强度不可外推**到 2024-2025 的模型
- **后续工作**：位置注意力偏置机制解释（Hsieh et al. 2024）不在本篇范围，
  需另行摄入

## 备注

本篇是本知识库第三份资料，也是唯一一份**以实验数据为核心**的资料。
[[2023-gao-rag-survey]] 中的「中间遗忘」论述此前仅有二手转述，
本篇补齐后证据链闭合。

与[[2020-lewis-rag-original]] 存在作者重叠：Fabio Petroni 同时是两篇作者，
这构成一条有趣的技术谱系线索（Facebook AI 2020 → 2023 转向长上下文评测）。
