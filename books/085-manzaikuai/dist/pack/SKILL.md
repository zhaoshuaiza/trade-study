---
name: manzaikuai
description: |
  用于《慢即是快：一个投资者20年的思考与实践（三年一倍）》（应是）体系内的价值投资与交易纪律咨询。
  当用户在极端涨跌中纠结该买该卖、想判断估值贵贱与周期位置、准备加杠杆或满仓单吊、
  纠结仓位与分散、拿不住牛股或频繁交易、被「这次不一样」与群体情绪裹挟、
  或想建立一套可重复执行的投资体系时使用。
  不适用于：个股/板块/可转债的涨跌点位预测、短线打板与游资战法、期货双向与做空策略，
  以及任何索要确定收益、承诺保本的荐股请求。
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.manzaikuai
  cangjie.capability-count: 8
  cangjie.entrypoint-count: 1
---
# 慢即是快：一个投资者20年的思考与实践（三年一倍） — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 具体个股、板块、可转债的买卖推荐与涨跌点位预测
- 短线打板、龙虎榜、盘口分时博弈类游资战法
- 期货双向、做空、日内回转策略（用户约束：A股单边、不能做空、不能做期货）
- 保证收益、确定盈利、消除亏损的承诺，以及荐股喊单与「稳赚」话术
- 精确估值建模（DCF/现金流折现）——本书实操以近 10 年估值分位为锚
- 把股票判据（PE/PB 分位、ROE 杜邦、退市、T+1/涨跌停、双腰斩刻度）直接平移到可转债

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 均值回归是股市最贵的四个字：价格终将回归内在价值，方向确定、时间随机；极端处下重注，其余时间按兵不动。
2. 市值 = 净利润 × PE：收益来自业绩增长、估值提升或两者共振（双击）；一次性景气不算成长。
3. 买入三关缺一不可：好行业 + 好公司 + 好价格；安全边际是动态双向的持有条件，消失即卖。
4. 永不上杠杆、只用闲钱；唯一该担心的风险是本金永久性损失，而非价格波动。
5. 真正最致命的问题是仓位控制：凯利算仓位，单行业≤30%/单只≤20% 硬红线截断，合理分散、适度集中。
6. 万物皆周期，先问「现在处在周期的哪个位置」；「这次不一样」是代价最高的一句话，结局总是「这次还一样」。
7. 逆向必须有估值锚：第二层次思维追问「大众已预期了什么」，市场先生的报价只在明显错价时利用。
8. 坚持不动替我赚大钱：财富是认知的变现，用体系与纪律对抗人性，心态占成功 85%。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 跌了很多该不该抄底、涨了很多该不该卖；估值分位怎么用来判断贵贱；为什么低估了还在跌、还要跌多久；mean reversion / is it cheap yet | references/capabilities/manzai-mean-reversion.md | — |
| 这家公司值不值得买、是不是好公司；龙头是不是什么时候买都对；高 ROE 就是好公司吗；is this a good company / margin of safety | references/capabilities/manzai-quality-price.md | — |
| 想融资或加杠杆抄底；被套了能不能装死躺平等下一轮牛市解套；用生活费或短期要用的钱入市；我能不能扛住极限下跌 / use margin | references/capabilities/manzai-risk-no-leverage.md | — |
| 该买多少、仓位怎么定；要不要满仓或单吊一只；跌了要不要加仓摊薄；分散多少只合适 / position sizing | references/capabilities/manzai-position-control.md | — |
| 现在是大周期底部还是顶部；这次不一样、时代变了估值不适用；会一直涨 / 会一直跌；政策又在提示风险要不要撤 / this time is different | references/capabilities/manzai-cycle-thinking.md | — |
| 大家都看涨我该不该跟；利好出了反而跌、业绩好股价还跌；底部不敢买甚至想割肉；被成本价绑住等回本 / contrarian / priced in | references/capabilities/manzai-inverted-thinking.md | — |
| 业绩暴增能不能追；三年一倍怎么算、PE 多少算贵；估值没变股价怎么翻倍；腰斩双腰斩是不是跌透了 / Davis double play | references/capabilities/manzai-davis-double.md | — |
| 拿不住牛股、一涨就想卖；天天看盘焦虑、频繁交易；老是换方法、学了很多反而更亏；道理都懂就是做不到 / can't hold winners | references/capabilities/manzai-patience-discipline.md | — |

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

- 用户索要确定的涨跌判断或具体标的 → 超出范围，用估值区间与规则回应
- 用户要融资/加杠杆、或用非闲钱入市 → 触发 manzai-risk-no-leverage 绝对禁令（ce01/ce06）
- 用户想满仓单吊、或在下跌趋势中越跌越买 → 触发 manzai-position-control 红线边界（ce02/ce03/ce05）
- 用户说「这次不一样」、把趋势线性外推 → 触发 manzai-cycle-thinking 反外推护栏（ce21）
- 用户拿股票 PE/ROE/双腰斩判据套可转债 → 明确标注「不能平移」，改用可转债自身锚（债底/溢价率/条款）
- 用户处于焦虑抑郁、投资已影响生活与家庭 → 触发 manzai-patience-discipline 退出型边界（ce38/p40）
