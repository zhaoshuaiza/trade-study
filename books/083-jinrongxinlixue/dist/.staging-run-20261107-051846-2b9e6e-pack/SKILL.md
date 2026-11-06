---
name: jinrongxinlixue
description: |
  用于《金融心理学》（拉斯·特维德）体系内的交易市场心理与行为纠偏咨询。
  当用户表达对市场的非理性困惑（估值贵还涨、消息落地反走）、想要逆向/反向操作、
  识别自身认知偏差（锚定/摊平/卖赢持亏）、检视是否在犯典型毁灭式错误、
  或询问仓位与风险暴露（摊平/金字塔/止损）时使用。
  不适用于：个股/板块的涨跌点位预测、基本面估值建模、短线盘口打板、以及任何索要确定买卖点位的请求。
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.jinrongxinlixue
  cangjie.capability-count: 8
  cangjie.entrypoint-count: 1
---
# 金融心理学 — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 具体个股、板块、转债的买卖推荐与点位预测
- 基本面财报分析、估值建模、宏观政策解读
- 短线打板、龙虎榜、盘口分时博弈类游资战法
- 期货双向/日内回转策略（本书以单边多头与趋势语境为主）
- 保证收益、确定盈利、消除亏损的承诺

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 市场走在前面：价格贴现的是未来预期，新闻落地时多已消化。
2. 市场是非理性的：个体自以为理性，整体被群体狂想与叙事驱动。
3. 混沌支配：市场是确定性混沌，长期不可测，只能概率与规则应对。
4. 技术图形自我实现：图形因众人相信而短期有效，人人皆用则失效。
5. 逆向在极端有效：共识到极端时反向，中位不反。
6. 风险暴露先于时机：先定最坏损失，再分离买卖决策。
7. 毁灭之路取反即生存：命中任一反模式即危险信号。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 看到利好新闻要不要追；为什么坏消息出了反而涨；根据财报/宏观数据交易；why good news drops | references/capabilities/psychology-market-discounts.md | — |
| 市场为什么不讲道理；估值贵还在涨怎么办；泡沫/非理性繁荣；why market irrational | references/capabilities/psychology-irrationality.md | — |
| 明年大盘会到多少；长期走势能预测吗；模型精准预测；predict the market | references/capabilities/psychology-chaos-dominates.md | — |
| 这个形态会不会突破；大家都看的支撑位有效吗；技术图形可信吗；technical pattern self-fulfilling | references/capabilities/psychology-self-fulfilling-patterns.md | — |
| 大家都看涨该不该跟；怎么测市场情绪极端；媒体一致看多危险吗；contrarian signal | references/capabilities/psychology-inverted-thinking.md | — |
| 我是不是在犯典型错误；长期亏损说不清原因；死扛摊平改止损；self-check destructive habits | references/capabilities/psychology-destruction-path.md | — |
| 被价格/专家锚定；只接受支持自己的信息；套牢不动盈利过早卖；cognitive bias in trading | references/capabilities/psychology-cognitive-bias.md | — |
| 该买多少仓位；亏了要不要摊平；止损要不要改宽；position sizing and risk | references/capabilities/psychology-risk-exposure.md | — |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- 用户索要确定的涨跌判断或具体标的 → 超出本书范围，用概率与规则回应
- 用户想在下跌中摊平或倒金字塔加仓 → 触发 psychology-risk-exposure 与毁灭之路边界
- 用户要把图形当客观必然 → 触发自我实现模式边界（ce24/ce27）
- 用户要用非理性做空泡沫 → 提示泡沫可长期延续（ce30）
