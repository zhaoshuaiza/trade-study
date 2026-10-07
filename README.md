# llm-wiki-claude-v2

基于 LLM Wiki 架构的个人知识库。**一次编译，持续复用。**

架构来源：Andrej Karpathy 的 LLM Wiki 构想（2026-04）。
方法论参考：[《我用 WorkBuddy + Obsidian：搭了一套懒人版可进化的AI知识库》](https://mp.weixin.qq.com/s/94wtoB0UCAO-NFvrtUMhuA)

## 三层架构

| 层 | 路径 | 权限 | 说明 |
|---|---|---|---|
| raw | `.raw/` | 只读 | 原始资料，事实来源，永不修改 |
| wiki | `wiki/` | AI 写，人审核 | 编译产物 |
| schema | `CLAUDE.md` | 人维护 | 规则与工作流 |

Obsidian 是 IDE，Agent 是程序员，wiki 是代码库。

> 🆕 **第一次用先看→ [新手上手指南.md](新手上手指南.md)**
> 讲清了每个文件放什么、每类页面怎么区分。日常三件事：存资料 → 说「编译」→ 问问题。

## 快速开始

1. 用 Obsidian 打开本文件夹（仓库管理器 → 打开文件夹作为仓库）
2. 启用 **Templater** 社区插件（可选，用于自动套用 `templates/`）
3. 把资料放进 `.raw/`
4. 在本目录启动 Agent 会话，读取 `CLAUDE.md` 后要求编译

推荐搭配：**Obsidian Web Clipper**（浏览器一键存入 `.raw/`）、
**Obsidian Git**（自动提交，每 15 分钟）。

## 日常三条工作流

**编译** —— 资料进 `.raw/`，Agent 提取概念/实体/来源/观点，更新索引。
增量机制：内容 hash 记入 `.raw/.manifest.json`，命中则跳过，不重复编译。

**查询** —— 先读 `wiki/hot.md` → `wiki/index.md` → 相关页面。
**不要全量加载 wiki/**。回答须引用具体页面；库里没有就说没有，不用训练数据补。

**治理** —— 每周跑一次检查，查孤立页、死链、索引漂元信息缺失、矛盾。
报告写入 `wiki/meta/lint/`。知识库越长大越需要治理。

## 目录

```
llm-wiki-claude-v2/
├── CLAUDE.md              维护规范（schema 层，先读这个）
├── .raw/                  原始资料（只读）
│   └── .manifest.json     内容 hash，增量编译用
├── wiki/
│   ├── index.md           总索引（查询入口）
│   ├── hot.md             近期上下文缓存（覆盖写）
│   ├── log.md             操作日志（追加写）
│   ├── overview.md        知识库全景
│   ├── concepts/          概念
│   ├── entities/          实体
│   ├── sources/           来源
│   ├── claims/            观点
│   ├── comparisons/       对比
│   ├── syntheses/         综合理解
│   ├── questions/         问答归档
│   └── meta/lint/         健康检查报告
├── templates/             七类页面模板
└── .attachments/          图片、PDF
```

## 原则

- 原始资料不可变，编译产物可重建
- 不确定的信息标 `status: uncertain`，**不编造**
- 知识库中没有的内容，如实说没有
- 人守住两个环节：**信息筛选** 与 **编译审核**

## 局限

页面到几百篇后，仅靠 `index.md` 渐进加载的检索效率会下降，token 消耗上升。
届时需补本地检索（BM25 召回 + 向量重排）。

**LLM Wiki 与 RAG 不互斥**：本方案是编译时产物，RAG 是运行时召回手段。
构建阶段把散落材料固化为完整语义单元，查询阶段再靠 RAG 精准定位。
