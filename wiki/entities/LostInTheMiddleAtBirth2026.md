---
type: entity
status: draft
created: 2026-10-07
updated: 2026-10-07
sources: ["[[2026-position-bias-mechanism]]"]
tags: [长上下文, 论文, 理论]
---

# LostInTheMiddleAtBirth 2026

## 基本信息

| 项 | 值 |
|---|---|
| 标题 | Lost in the Middle at Birth: An Exact Theory of Transformer Position Bias |
| 作者 | Borun D Chowdhury |
| 时间 | 2026-03-10 |
| 篇幅 | 11 页，7 图 |
| arXiv | [2603.10123](https://arxiv.org/abs/2603.10123) |

>⚠️ **单作者论文**，且为较新的预印本（2026-03），
> 尚未见同行评审记录。引用时应标注这一点。

## 简介

[[拓扑U型]]的理论证明。主张 U 型曲线是**因果解码器 + 残差连接的固有几何属性**，
在**随机初始化时即存在**。

## 核心贡献

把多层因果注意力建模为 **Cesàro 矩阵的迭代幂**，
在连续极限下推导出**精确闭式的影响密度**。

三个关键结构：

| 结构 | 数学性质 |
|---|---|
| **Primacy Tail**（首因尾部） | 梯度影响的**对数发散** |
| **Recency Delta**（近因增量） | 孤立的 **O(1)** 锚点 |
| **阶乘死区** | **O(1/(H−1)!)**，H 为网络深度 |

## 挑战的两个主流解释

1. **习得的 Softmax 工件**——若为习得，应随训练改变
2. **RoPE 距离衰减**——**实验证明有无 RoPE 结果一致**

## 实验验证

| 验证项 | 结果 |
|---|---|
| 随机初始化 **Qwen2** / **GPT-2** | **Step 0 即 U 型** |
| 有无 RoPE | **一致** |
| 初始化 vs 预训练 | **训练未克服拓扑谷** |

## 在理论演进中的位置

```
Xiao et al. 2023     现象：Attention Sinks
        ↓
Wu et al. 2025       图论：因果掩码 → 指数级路径优势
        ↓             ⚠️ 但纯注意力设定预测「纯首因」，无法解释 U 型
Herasimchyk 2026     残差感知 rollout：Spearman 0.88–0.98
        ↓
Chowdhury 2026       本篇：精确闭式 + 随机权重，无需训练参数
```

**本篇的关键贡献是引入残差连接挽救了近因锚点**，
从而生成了完整的 U 型——这正是 Wu et al. 无法解释的部分。

## 明确不主张的内容

作者主动划定边界：
- **不**主张该偏置不可逾越
- **不**主张 RoPE 修改之类的干预无用
- **不**主张雅可比范数直接度量检索准确率

主张的是：确立基线及其来源，使后续努力可精准定位。

## 关系

- 概念：[[拓扑U型]]、[[U型注意力偏置]]
- 经验层对应：[[FoundInTheMiddle2024]]
- 来源：[[2026-position-bias-mechanism]]

## 来源

- [[2026-position-bias-mechanism]]