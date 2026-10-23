- id: ce01
  title: 确定性幻觉（追求确定性必败）
  type: counter-example
  source_chapter: 第二章·点球原理 / 第六章·再见确定性
  source_quote: |
    "不追求确定性还有可能成功，而追求确定性就必然会失败！"
  failure_mode: |
    为追求"每笔必赚"的确定性，要么放弃趋势中绝大部分利润，要么等所有向好迹象出现才买入，
    结果抬高成本、错过行情，甚至把技术弄模糊、毫无章法地随机交易。
  mechanism: |
    市场不存在确定性；越追求"有把握"越牺牲赔率。任何确定下来的方法都会被证实不具有确定性，
    于是交易者只能混合众多不确定方法以求幻觉，反而无法使用一致性方法。
  warning_signs:
    - 买入前必须"看懂行情/找到理由"才动手
    - 频繁用指标、过滤器确认"确定性"
    - 因没把握而踏空后追高
    - 把"看对"视为获利的关键
  bound_to:
    - "成本观念/盈亏同源"
    - "一致性原则"
    - "预测与交易区分"
    - "趋势跟踪系统"
  tags: [counter-example, determinism-delusion, overconfidence]

- id: ce02
  title: 高正确率陷阱（超市原理）
  type: counter-example
  source_chapter: 第二章·超市原理
  source_quote: |
    "在我看来，股民们大面积亏损的一个最为主要的原因就是正确率太高了！"
  failure_mode: |
    本能"利润兑现、亏损挂起"制造出高正确率，但利润被众多小赚平分、亏损由少数大亏承担，
    长期来看是稳定亏损的根源。
  mechanism: |
    正确率与离市策略高度相关而非预测水平；止损幅度数倍于止盈即可数倍正确次数。
    高正确率恰是"盈利兑现、亏损挂起"癖好的体现，正是亏损根源之一。
  warning_signs:
    - 盈利单拿不住、亏损单死扛
    - 以"对了几成"自夸
    - 账户"小赚多笔、偶尔一笔大亏"
  bound_to:
    - "成本观念/盈亏同源"
    - "趋势跟踪系统"
    - "亏损五境界"
  tags: [counter-example, high-winrate-trap, cognitive-bias]

- id: ce03
  title: 学习效应/狗咬尾巴（随近期成败切换方法）
  type: counter-example
  source_chapter: 第二章·学习效应
  source_quote: |
    "我见过很多炒股时间超过十年的人，大多数仍旧无法跳出'狗咬尾巴'的怪圈。"
  failure_mode: |
    没有一致性基石，受身边或近期成败影响，反复在矛盾两极（趋势↔整理、敏感↔迟钝、业绩↔题材）
    间切换，原地转圈十年毫无进展。
  mechanism: |
    结果决定论怪圈 + "市场制造微观定势后突然打破"。向近期成功者学习反而被一网打尽。
    作者自承："上面两个故事的主人公就是曾经的我！"
  warning_signs:
    - 看到别人某法赚钱就改学
    - 牛市学死多、熊市学死空来回变
    - 十几年仍在寻找"最好方法"
  bound_to:
    - "一致性原则"
    - "系统开发"
    - "学习效应"
  tags: [counter-example, method-switching, learning-effect]

- id: ce04
  title: 过度优化参数/叠加组合（优化与组合陷阱）
  type: counter-example
  source_chapter: 第六章·优化与组合
  source_quote: |
    "越是过度优化的系统就越难在未来获利。由此我们可以得知，过度优化系统参数是绝对没有任何意义的。"
  failure_mode: |
    为绕开假信号成本不断加过滤器、调参数，或把不同核心方法组合，结果历史完美、未来失效；
    组合反而叠加劣势、互损。
  mechanism: |
    市场无典型幅度（能量分布），敏感与迟钝等效；单一方法有效时收入与成本同叠加，
    组合优势被损耗效应抵消（圆木桶、小蝴蝶）。稳定性好的系统依赖理念而非参数优化。
  warning_signs:
    - 系统参数随最近一次行情反复改
    - 给系统加多个"滤嘴"
    - 把两套方法拼一起求"双高"
  bound_to:
    - "系统开发"
    - "优化与组合"
    - "如何开发系统"
  tags: [counter-example, over-optimization, curve-fitting]

- id: ce05
  title: 把分散投资当风险防范
  type: counter-example
  source_chapter: 第六章·风险防范
  source_quote: |
    "分散投资是一种资金管理工具，而不是一种风险防范工具。……这种可怜的分散投资只能是让交易者更加平稳地亏损。"
  failure_mode: |
    用分散（买十只以上、获利兑现亏损挂起）来"防风险"，结果稳定地亏损，且持续过滤成弱势股集中营。
  mechanism: |
    方法若错，十个账户也错；分散只是资金波动的减震器，不能提高期望收益，
    反使"盈利兑现、亏损挂起"的本能更平滑地侵蚀本金。
  warning_signs:
    - 认为"多买几只就安全"
    - 持仓被止损后剩一篮子弱势股
    - 用分散替代绝对止损点
  bound_to:
    - "风险防范两点"
    - "资金管理/分散魅力"
  tags: [counter-example, diversification-myth, risk-control]

- id: ce06
  title: 预测≠交易（点状观点不成环）
  type: counter-example
  source_chapter: 第六章·预测与交易
  source_quote: |
    "你可以在完全看不懂行情的情况下获取利润，也可能在看对行情的时候亏钱。"
  failure_mode: |
    把分析师式的"点状、相对"预测当交易，有观点无买卖闭环（开/持/平），看对行情却因离市、资金管理做不好而亏。
  mechanism: |
    预测无需二元选择（卖还是持），交易必须绝对化闭环；"看多"需要资金资格，
    观点正确只是获利的次要因素。作者自承曾迷信江恩/波浪，看对行情却卖在地板价。
  warning_signs:
    - 能说清点位/阻力却无买卖规则
    - "我看多但没钱了"
    - 以"分析对"衡量自己水平
  bound_to:
    - "预测与交易区分"
    - "趋势跟踪系统"
  tags: [counter-example, prediction-vs-trading, analysis-paralysis]

- id: ce07
  title: 把亏损当敌人（鸵鸟现象/怕亏情结）
  type: counter-example
  source_chapter: 第二章·鸵鸟现象
  source_quote: |
    "这种亏不起的心态，最终的结果只能是上涨没他事，下跌他肯定跑不了。"
  failure_mode: |
    拒绝/回避亏损（怕亏、怕隔夜、怕赌、怕错），用"盈利兑现、亏损挂起"暂时视而不见，未来承受更大代价。
  mechanism: |
    亏损是系统必然成本；对抗亏损使交易者只能追求高正确率、陷入零取整存，最终被市场扫地出门。
    作者曾受虚假业绩伤害而陷入指责牢骚，靠"从对抗到包容"才走出。
  warning_signs:
    - "你说过两天能不亏损吗"式提问
    - 不愿在交易前计划亏损
    - 亏损后指责外界而非自省
  bound_to:
    - "成本观念/盈亏同源"
    - "亏损五境界"
    - "风险防范"
  tags: [counter-example, loss-aversion, ostrich]

- id: ce08
  title: 高低错觉（用历史参照物判断买卖）
  type: counter-example
  source_chapter: 第二章·高低错觉
  source_quote: |
    "高低根本就不应该作为买卖的理由！……更多的交易者都喜欢同历史比较而得出高低的结论。"
  failure_mode: |
    以过去价格作参照物判断"高低"来买卖（抄底逃顶），错把"比历史低=聪明"当依据。
  mechanism: |
    庄家与基本面制造参照物以制造"超值错觉"；趋势信徒只看未来，涨势中多高都不嫌高，
    过去的参照物与未来走势无关。
  warning_signs:
    - "今天比昨天高，买的人都是傻子"
    - 因"跌多了"而买入
    - 用60日线等历史成本判断贵贱
  bound_to:
    - "趋势是你的朋友"
    - "成本观念"
  tags: [counter-example, anchoring, high-low-illusion]

- id: ce09
  title: 依赖他人/推卸责任（依赖现象）
  type: counter-example
  source_chapter: 第二章·依赖现象
  source_quote: |
    "把自己的钱袋寄托在别人的身上是一件最为愚蠢的事情。"
  failure_mode: |
    把股评、政府、上市公司当救世主又当出气筒，咨询他人只为寻求认同以事后推卸责任，从不自我负责。
  mechanism: |
    国人不重个体责任感；"你只能指责一次并且此后不再相信"，否则永远在相信—依赖—指责的循环里。
  warning_signs:
    - 亏损怪证监会/庄家/黑嘴
    - 征求意见直到有人支持
    - 做对归自己、做错归别人
  bound_to:
    - "一致性原则"
    - "风险防范"
    - "独立思考"
  tags: [counter-example, dependency, responsibility]

- id: ce10
  title: 绿草坪/羊群（羡慕他人、守不住自己的道）
  type: counter-example
  source_chapter: 第二章·绿草坪效应
  source_quote: |
    "请不要羡慕任何人，交易获利的关键在于：守住自己的'道'。"
  failure_mode: |
    别人赚钱就眼红模仿，陷入学习效应怪圈；媒体挖出事后正确的"分析大师"让人以为行情可懂。
  mechanism: |
    任何方法都有占便宜和吃亏的时候；总有观点正确的大师 ≠ 某大师总正确；模仿他人即放弃自身概率优势。
  warning_signs:
    - "张三1800点就看到4000点，真神"
    - 追热点、换方法跟风
    - 因别人赚而怀疑自己系统
  bound_to:
    - "一致性原则"
    - "学习效应"
    - "系统个性化"
  tags: [counter-example, herd, green-grass]

- id: ce11
  title: 恐龙效应（过度适应微观规律而陨落）
  type: counter-example
  source_chapter: 第二章·恐龙效应
  source_quote: |
    "能够戴上光环的交易者，必然更多地利用、依赖了市场中的微观规律。……当市场的特征出现巨变的时候，这种过度适应市场的交易者就会被市场迅速扫地出门。"
  failure_mode: |
    靠过度适应某阶段微观规律戴光环，市场特征巨变（巨变法）时快速陨落；交易比赛冠军、明星常昙花一现。
  mechanism: |
    越微观的规律战绩越辉煌但有效期越短；过度适应即埋下陨落伏笔，巨变效应在极短时间内翻转环境。
  warning_signs:
    - 某阶段"屡试不爽"的方法被神化
    - 宣称掌握"抄底逃顶"秘技
    - 近期战绩极佳而轻视风控
  bound_to:
    - "系统个性化"
    - "趋势跟踪系统"
    - "恐龙效应"
  tags: [counter-example, overfitting-era, dinosaur]

- id: ce12
  title: 焦虑原理（为不确定性焦虑而放弃系统）
  type: counter-example
  source_chapter: 第二章·焦虑原理
  source_quote: |
    "可能出现的亏损，比确定的大幅亏损更加可怕。"
  failure_mode: |
    对"可能亏损"的焦虑甚于确定亏损，在系统付出成本阶段心力交瘁，放弃未来能带来巨大利润的系统。
  mechanism: |
    人本能追逐确定性求安全，却不能承受"不知还要亏多久"；焦虑使行为重确定性而非利润，挺不过交易冬天。
  warning_signs:
    - 夜看外盘焦虑难眠
    - 回撤期频繁怀疑系统
    - "再亏下去怎么办"式恐慌
  bound_to:
    - "一致性原则"
    - "成本观念"
    - "亏损五境界"
  tags: [counter-example, anxiety, drawdown-panic]

- id: ce13
  title: 圆木桶/系统过复杂（失败者游戏）
  type: counter-example
  source_chapter: 第二章·圆木桶理论
  source_quote: |
    "对于一笔获利的交易而言，你必须把各个环节都做正确；但对于一笔亏损的交易而言，并不需要你把各个环节都做错，只要做错一个环节就足够了！"
  failure_mode: |
    系统大厦过于庞大复杂，任一环节出问题即满盘皆输；功能越多越易故障，期货看对行情也因某环节死得快。
  mechanism: |
    成败不取决最大优势而取决最大劣势；复杂=更多短板=更高失败概率。交易是"失败者的游戏"，应简单而非繁琐。
  warning_signs:
    - 系统含开仓/持仓/离市/资金多模块多技术
    - 追求"完美覆盖"
    - 一处疏忽即大亏
  bound_to:
    - "系统开发"
    - "奥姆剃刀/简单"
    - "圆木桶理论"
  tags: [counter-example, overcomplexity, barrel]

- id: ce14
  title: 小蝴蝶/叠加方法（逃避不确定性反入深渊）
  type: counter-example
  source_chapter: 第二章·小蝴蝶的故事
  source_quote: |
    "在叠加交易方法的过程中，不但是将全部方法的优势进行叠加，同时也会将全部方法的劣势进行叠加。"
  failure_mode: |
    面对众多方法无法取舍，想"得到全部优势"而叠加方法，结果优势互损、劣势互叠，带入宏观不确定性。
  mechanism: |
    选择即利弊取舍，无全优选择；为逃避微观不确定而叠加，反而丧失单一方法长期（宏观）的确定性。
  warning_signs:
    - "集百家之长"式拼凑
    - 同时用几种指标互相确认
    - 不愿放弃任何方法
  bound_to:
    - "优化与组合"
    - "系统开发"
    - "小蝴蝶"
  tags: [counter-example, method-stacking, butterfly]

- id: ce15
  title: 损耗效应（趋势跟踪上叠研判反而更差）
  type: counter-example
  source_chapter: 第二章·损耗原理
  source_quote: |
    "将他们组合起来的结果，很可能是不如单一使用其中的任何一种方法。"
  failure_mode: |
    在趋势跟踪系统上叠加主观研判/其他分析来"规避假信号"，放过小真信号，得不偿失。
  mechanism: |
    趋势跟踪正确率常<40%，随机放弃一次信号都易避损；叠加需极高正确率才有意义，而研判达不到，优势被损耗。
  warning_signs:
    - 用基本面/指标"过滤"趋势信号
    - 因一次假信号就加研判层
    - 系统外"人工把关"
  bound_to:
    - "优化与组合"
    - "一致性原则"
    - "损耗原理"
  tags: [counter-example, combination-loss, decay]

- id: ce16
  title: 传统套利思维缺陷（自作聪明找不合理）
  type: counter-example
  source_chapter: 第六章·套利原理
  source_quote: |
    "套利是不可能具有弹性的，你因为市场的不合理而开始套利，那么你应该不会因为市场的更不合理而结束套利行为。"
  failure_mode: |
    靠找市场"不合理"来做无风险套利，利润有限而风险无限；市场扩大不合理程度时死无葬身之地（玉麦比价案例）。
  mechanism: |
    套利指手画脚告诉市场该如何，无弹性；与敬畏市场、随市而动相悖；完美套利模型只存在书本。
  warning_signs:
    - "这明显定价错误，必回归"
    - 重仓赌价差回归
    - 忽视"更不合理"的可能
  bound_to:
    - "套利原理"
    - "趋势跟踪系统"
  tags: [counter-example, arbitrage-trap, no-elasticity]

- id: ce17
  title: 等"看出趋势"再动（点球原理反面）
  type: counter-example
  source_chapter: 第二章·点球原理
  source_quote: |
    "守门员扑点球不是看出来的，而是赌出来的。……如果等看出球的走向后再选择扑球方向，那么扑到球的概率为0。"
  failure_mode: |
    等看出趋势/确认信号才行动，结果要么扑空（概率0）要么追在不利位置；用"需要看懂行情"提高门槛牺牲赔率。
  mechanism: |
    确定性不存在；看趋势是赌不是看。迟钝（多条件确认）靠丧失赔率换正确率，反而提高成本、丧失赔率。
  warning_signs:
    - "等明朗了再进场"
    - 必须多指标共振才买
    - 错过启动后懊悔
  bound_to:
    - "趋势跟踪系统"
    - "成本观念"
    - "点球原理"
  tags: [counter-example, wait-for-confirmation, penalty]

- id: ce18
  title: 大众无效率观点/卖完理论（指责扩容等）
  type: counter-example
  source_chapter: 第二章·卖完理论
  source_quote: |
    "大众对很多最简单与基本的问题，却存在完全无效率的观点。"
  failure_mode: |
    对最基本问题持无效率观点（反对升值、指责扩容圈钱），被虚高价格/参照物误导，站在买家却反对上涨。
  mechanism: |
    供给受限使价格虚高，买方拥护虚高；对买方有利的从来不是高价格而是能涨的价格，却因参照物错觉支持高价。
  warning_signs:
    - 股民骂扩容/圈钱导致下跌
    - 买入者反对标的上涨
    - 用"对外缩水"等错误逻辑
  bound_to:
    - "基本分析批判"
    - "独立思考"
    - "卖完理论"
  tags: [counter-example, crowd-inefficiency, mass-delusion]

- id: ce19
  title: 怕隔夜→日内重仓误区（鸵鸟怕隔夜）
  type: counter-example
  source_chapter: 第二章·鸵鸟现象（怕隔夜情结）
  source_quote: |
    "在日内的有限时间内，交易者基本上不可能靠放长利润来实现大赔率。自然他们就只能够掩耳盗铃地追求高正确率了，通常最终的结果就是'零取整存'。"
  failure_mode: |
    受隔夜跳空伤害后不持隔夜单，陷入日内+重仓误区，只能追求高正确率，最终零取整存。
  mechanism: |
    隔夜跳空是噪声，止损应有下限；过小止损无意义→仓位不能太重→应轻仓包容隔夜风险，而非放弃隔夜。
  warning_signs:
    - 只做日内、绝不隔夜
    - 重仓博短线
    - 因一次跳空就否定持仓
  bound_to:
    - "资金管理"
    - "风险防范"
    - "鸵鸟现象"
  tags: [counter-example, intraday-heavy, overnight-fear]

- id: ce20
  title: 怕赌/怕错情结（制造确定性幻觉）
  type: counter-example
  source_chapter: 第二章·鸵鸟现象（怕赌、怕错情结）
  source_quote: |
    "更多的人是自以为在做交易的赌徒！"
  failure_mode: |
    不愿面对不确定性，把技术弄模糊、混合众多不确定方法以求确定；或事前找借口推卸错误，自尊重于钞票。
  mechanism: |
    确定方法必被证伪，于是交易者毫无章法、随心所欲；以为混合不确定方法能得确定，实则逃避责任。
  warning_signs:
    - 反感把交易称"赌"
    - 行动前四处征求意见
    - 方法含混、无明确规则
  bound_to:
    - "赌博五原则"
    - "一致性原则"
    - "鸵鸟现象"
  tags: [counter-example, deny-gambling, responsibility]

- id: ce21
  title: 用结果评价对错（对错悖论误用）
  type: counter-example
  source_chapter: 第二章·对错悖论
  source_quote: |
    "如果真的按照这样的逻辑来分析对错的话，那么任何方法都是好方法，同样任何方法也都是坏方法。"
  failure_mode: |
    以盈亏结果评判方法好坏（赚=好、亏=坏），陷入结果决定论，无法建立固定基石，永远原地转圈。
  mechanism: |
    对错的评价应基于原因/策略而非结果；结果不可左右，用结果定对错直接催生学习效应的狗咬尾巴。
  warning_signs:
    - "这方法让我亏了所以是错的"
    - 凭单笔盈亏改系统
    - 崇拜短期盈利者
  bound_to:
    - "盈亏同源"
    - "亏损五境界"
    - "对错悖论"
  tags: [counter-example, result-bias, right-wrong]

- id: ce22
  title: 传统风控三误区（买优质/买便宜/分散）
  type: counter-example
  source_chapter: 第六章·风险防范
  source_quote: |
    "很多人告诉我高价股亏损十几元很轻松，而低价就算'跌没了'才几块钱。难道这些股民炒股票不看幅度而看绝对的价格吗？"
  failure_mode: |
    用买优质股、买便宜股（低价/下跌/疲弱）、分散来防风险，实则加速亏损的思维误区。
  mechanism: |
    涨跌只与业绩预期变化相关，与当前收益无关；低价股想象空间与风险都更高；买弱势股占便宜荒唐（强弱互换需五年）。
  warning_signs:
    - "业绩好所以安全"
    - "跌多了更便宜"
    - 专买下跌中的股票
  bound_to:
    - "风险防范两点"
    - "基本分析批判"
  tags: [counter-example, value-trap, cheap-stock]

- id: ce23
  title: 大师迷信/破大师（连大师都自我否定破产）
  type: counter-example
  source_chapter: 第一章·大师的结局
  source_quote: |
    "这位华尔街的教父于1976年去世前不久……却宣布他不再信奉基本分析流派，而最终相信'效率市场'理论。"
  failure_mode: |
    盲目崇拜/依赖大师预测与权威，以为跟随即可战胜市场，忽视大师自己也转向或破产。
  mechanism: |
    没有谁能战胜市场；大师也会自我否定（格雷厄姆转效率市场、威尔德弃指标），江恩完美难用于实战、利物默自杀。
  warning_signs:
    - 奉某大师理论为圣经
    - 照搬他人"圣杯"
    - 信"权威预测点位"
  bound_to:
    - "反预测"
    - "独立思考"
    - "基本/技术分析批判"
  tags: [counter-example, guru-worship, break-guru]

- id: ce24
  title: 抄底逃顶/分析师逆势（求势不舍价）
  type: counter-example
  source_chapter: 第一章·学生股民（资深分析师误区）
  source_quote: |
    "典型的逆势交易！趋势的朋友应该是：在牛市中持有多单，每逢超过一定幅度的调整时平多出来，等到整理结束后再以更高的价位买入。"
  failure_mode: |
    "求势不舍价"：以为牛市中调整后便宜买回是顺势，实为逆势；分析师报告理论上可行、可操作性差、证明自己比市场聪明。
  mechanism: |
    把"不会买错"当"不会买贵"，逆势抄底逃顶，与"趋势做朋友"相悖；报告全部试图战胜市场指手画脚。
  warning_signs:
    - "调整后更便宜所以买"
    - 用"价值"抗拒趋势
    - 信分析师"指点江山"
  bound_to:
    - "趋势是你的朋友"
    - "成本观念"
  tags: [counter-example, bottom-fishing, anti-trend]

- id: ce25
  title: 超级掠食者/羊群无效率（追求相对收益）
  type: counter-example
  source_chapter: 第二章·超级掠食者理论
  source_quote: |
    "生活在群体中的个体，往往会丧失思考的能力。而集体形成的盲目性，又很容易将其带入毁灭的深渊。"
  failure_mode: |
    羊群思维使个体丧失思考、比拼速度不比方向，群体极端无效率；基金经理因赎回压力只敢犯"集体错误"。
  mechanism: |
    追求相对（指数）收益者必犯集体错误；趋势跟踪者追求绝对收益，错误必是特有的，难吸纳资金却更独立。
  warning_signs:
    - "大家都这么干"
    - 怕跑输指数甚于怕亏钱
    - 随大流不思考
  bound_to:
    - "独立思考"
    - "趋势跟踪系统"
    - "超级掠食者"
  tags: [counter-example, herd-thinking, predator]

- id: ce26
  title: 双高系统执念/过滤信号徒劳
  type: counter-example
  source_chapter: 第六章·优化与组合
  source_quote: |
    "问题不在于过滤以后得到的战绩输出是否能够达到双高要求，而在于我们过滤出去的交易机会是否也能够使我们实现利润。"
  failure_mode: |
    执着开发"正确率>50%且赔率>1"的双高系统、不断加过滤器，过滤掉的信号本也可获利，闲置资金无他用。
  mechanism: |
    边际利润>边际成本即可；过滤掉的行情明天可能就要执行信号，放弃本属自己的利润并不划算。
  warning_signs:
    - "我要高正确率又高赔率"
    - 系统加250日均线滤嘴等
    - 嫌某些信号"不好"而删
  bound_to:
    - "优化与组合"
    - "系统开发"
    - "双高系统"
  tags: [counter-example, dual-high-obsession, filtering]

- id: ce27
  title: 背离系统/自作聪明"超越"（作者自承丢数千万）
  type: counter-example
  source_chapter: 第六章·一致性
  source_quote: |
    "回头看看这十年多的战绩，我'超越'没了数千万的利润！而这种结果，系统只不过是打击了我三次。"
  failure_mode: |
    找到获利方法后仍不甘心放弃思考，频繁"超越"系统（忽略信号/赌气/放弃信号），背离系统自作聪明。
  mechanism: |
    人类思考在市场面前是负值；墨菲法则——本能反应为负值。三次超越（2001忽略卖号亏50%、2003赌气亏50%、
    2006放弃买号）让作者丢失十倍于当时的财富，复利放大错误。
  warning_signs:
    - "这次不一样，我来判断"
    - 忽略系统信号凭感觉
    - 认为规则太死板想优化
  bound_to:
    - "一致性原则"
    - "系统开发"
  tags: [counter-example, override-system, self-sabotage]

- id: ce28
  title: 形态/成交量误区（缩量不预示反转）
  type: counter-example
  source_chapter: 第四章·形态分析（误区）
  source_quote: |
    "成交量是与价格同步，而从来没有领先过价格。遗憾的是，很多股民在'调整'（下跌）中，以成交量萎缩作为不卖出的理由。"
  failure_mode: |
    把缩量当作"调整非反转"不卖的理由、把形态三大提示当真理，实则成交量与价格同步、并无提示作用。
  mechanism: |
    衡量命题好坏不在正确率而在"符合却不成功的比例"；缩量在反转形成中也接近100%存在，成交量无领先性。
  warning_signs:
    - "缩量下跌不用怕"
    - 信双顶/三重顶等形态必然
    - 用OBV等量价指标预测
  bound_to:
    - "技术分析批判"
    - "趋势跟踪系统"
    - "形态分析"
  tags: [counter-example, volume-myth, pattern-illusion]
