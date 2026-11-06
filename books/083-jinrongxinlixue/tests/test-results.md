# 阶段4 压力测试 · 结果记录（083《金融心理学》）

> 记录日期：2026-11-07
> 测试对象：8 个晋级能力（psychology-market-discounts, psychology-irrationality, psychology-chaos-dominates, psychology-self-fulfilling-patterns, psychology-inverted-thinking, psychology-destruction-path, psychology-cognitive-bias, psychology-risk-exposure）
> 路由底座：single（`dist/pack`，1 入口 + 8 张内部能力卡）

---

## 1. 测试库存
8 套 `test-prompts.json`，每套 8 条 = **64 条用例**：

| 类型 | 数量/套 | 说明 |
|---|---|---|
| `should_trigger` | 4 | 概念求解 / 情境自述 / 复盘 / 主动求边界 |
| `should_not_trigger` | 3 | 跨 Skill 混淆诱饵 ×2 + 预测荐股越界 ×1 |
| `edge_case` | 1 | **可转债品种越界**：应命中但只输出 B 段边界 |

## 2. 测试方法（fallback）

按阶段4方法论：本环境无独立盲测 sub-agent，退回主流程自测——逐条比对 `dist/pack/SKILL.md` 路由表与能力卡 B 段。

## 3. 结论

- 正面用例：路由表关键词覆盖各卡 `aliases`/`one_liner`，应命中。
- 负面用例：`entry.out_of_scope` 已列「预测/荐股/点位」，跨卡诱饵由 `capability-index.md` 分流。
- 边界用例：各卡 B 段均标注**股票判据不可平移可转债**（T+0、无涨跌停、20%/30% 临停、强赎条款），命中但只答边界。
- ⚠️ 待办：本轮为静态路由核对，未做真实模型盲测；如需盲测需另起独立会话。
