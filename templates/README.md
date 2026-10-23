# templates/ · 页面模板

> 八个模板，与 `wiki/` 的分型**一一对应**。

---

## 对应关系

| 模板 | 对应目录 | 用途 |
|---|---|---|
| `entity.md` | `wiki/entities/` | 体系与对象 |
| `concept.md` | `wiki/concepts/` | 抽象概念 |
| `source.md` | `wiki/sources/` | 原始资料 |
| `claim.md` | `wiki/claims/` | 观点主张 |
| `comparison.md` | `wiki/comparisons/` | 对比 |
| `synthesis.md` | `wiki/syntheses/` | 综合理解 |
| `question.md` | `wiki/questions/` | 问答存档 |
| `market.md` | `wiki/market/` | 行情实证（每日复盘联动，2026-10-23 新增） |

---

## 怎么用

**通常不用你操心** —— AI 编译时会自动套用对应模板。

需要手动用的场景：
- 你想自己建页
- 觉得AI 漏了某个类型
- 想重构某页的结构

装了 **Templater** 插件的话，可以用命令自动套用；否则复制粘贴模板内容即可。

---

## 模板为什么重要

结构统一带来三个好处：

1. **不漏字段** —— 每种页面该有的信息固定位置，不会漏
2. **可检索** —— frontmatter 统一，可以按 `type:` 筛选
3. **可校验** —— lint 能检查「元信息缺失」

---

## 交易库的模板特点

相比通用知识库，交易库的模板多了这些字段：

| 字段 | 作用 |
|---|---|
| `status: draft/verified/uncertain` | 结论可靠度分级 |
| `verifiable`（claim 专用） | 证据强度 |
| `source_file` + 出处页码 | 溯源依据 |
| 时效性字段 | 出版年份、适用市场、复核期限 |

> 📌 **不确定就标 `uncertain`**，别硬写一个确定答案。
> 交易领域错误方法比不知道更危险。

---

## 相关

- 上级说明：[../wiki/README.md]
- 规则：[../CLAUDE.md]
