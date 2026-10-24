---
name: zouchuhuanjue
description: |
  《走出幻觉·走向成熟》（金融帝国）的来源路由入口。以下场景直接问它：
  纠结亏损止损用语与心理建设、判断自己对亏损处于哪个认知层级、
  厘清真正的风险防范该做什么、判断该不该优化参数或叠加策略、
  要一套可直接落地的分散趋势跟踪系统、解释为何高胜率却在亏钱、
  以及识别自己是不是在反复更换方法的"狗咬尾巴"循环里。
  更高频的独立意图已晋级为独立 Skill，可直接调用。
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: router
  cangjie.bundle-id: bundle.zouchuhuanjue
  cangjie.capability-count: 7
  cangjie.entrypoint-count: 8
---
# 走出幻觉·走向成熟 — 来源路由入口（compact pack）

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 具体个股、板块、转债的买卖推荐与点位预测
- 基本面财报分析、估值建模、宏观政策解读
- 短线打板、龙虎榜、盘口分时博弈类游资战法
- 期货双向/日内回转策略（作者在期货验证本书体系，但当前用途限于股票与可转债的单向多头）
- 保证收益、确定盈利、以及任何消除亏损的承诺

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 亏损不是错误，是获取趋势利润必须垫付的进货成本；规避亏损必然同时规避利润（盈亏同源）。
2. 对未来每一笔的恐惧源于索要确定性；接受不确定性后，盈亏便从道德问题降级为成本问题。
3. 让盈利之所以可能的结构是：低正确率＋大赔率＋一致性执行，而不是高胜率与精准预测。
4. 评价一笔交易的对错只能基于它是否符合系统，不能基于它的盈亏结果。
5. 系统不需要最优，需要能在大样本中重复执行；参数两端等效，早定下来的家才是好家。
6. 最高境界不是预测更准，而是能与必要的亏损共处，并对它心怀感激。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 亏损了要不要止损、怎么面对；一亏钱就难受、不敢看账户怎么办；如何正确看待交易亏损；stop loss psychology, how to accept trading losses | references/capabilities/trading-loss-as-cost.md | 已晋级为独立 Skill `trading-loss-as-cost`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 我现在算什么水平、交易境界到哪了；我明明知道要止损但就是做不到；怎么判断我是不是适合继续做交易；trading maturity levels, how to tell if I am a real trader | references/capabilities/loss-maturity-ladder.md | 已晋级为独立 Skill `loss-maturity-ladder`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 怎么做风险控制、如何防范风险；持仓回撤了要不要先出来；分散持股能不能降低风险；risk management trading, how to protect capital, does diversification reduce risk | references/capabilities/risk-guard-two-points.md | 已晋级为独立 Skill `risk-guard-two-points`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 参数怎么设最好、要不要再优化一下；要不要加个过滤条件提高胜率；能不能把两个方法组合在一起；overfitting, parameter optimization, combine trading strategies, add filters | references/capabilities/avoid-over-optimization.md | 已晋级为独立 Skill `avoid-over-optimization`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 给我一套能直接用的交易系统；趋势跟踪系统怎么搭、怎么分配资金；如何控制每笔仓位大小；trend following system, position sizing, equal allocation, how to build a trading system | references/capabilities/insect-system-recipe.md | 已晋级为独立 Skill `insect-system-recipe`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 我胜率很高为什么还亏钱；如何提高胜率、提高正确率；为什么赚小亏大、该怎么改；why high win rate still loses money, cut winners let losers run | references/capabilities/high-winrate-trap.md | 已晋级为独立 Skill `high-winrate-trap`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 我老是换方法、哪种都不灵怎么办；学习了很多方法反而更亏了；要不要根据最近表现换策略；strategy hopping, keep changing methods, why learning more makes me worse | references/capabilities/learning-effect-chasing-tail.md | 已晋级为独立 Skill `learning-effect-chasing-tail`（已安装时优先直接使用；本卡仅作原文与背景补充） |

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

- 用户索要确定的涨跌判断或具体标的 → 明确告知超出本书范围，不要硬套趋势跟踪语言去预测
- 用户尚处于"拒绝面对亏损"阶段（第①层） → 不要谈参数优化与系统开发，先做亏损诊断
- 无仓位计划、无固定止损、无重复执行样本 → 不进入系统有效性讨论，先补足这三项
- 用户要求把多种方法叠加或持续加过滤器 → 先过"优化与组合陷阱"再决定
