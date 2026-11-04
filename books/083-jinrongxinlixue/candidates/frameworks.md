# Framework Candidates · 083《金融心理学》

> 来源：拉斯·特维德《金融心理学》（中文版，零 OCR 干净文本）
> 提取角色：framework-extractor（思维模型 / 决策框架 / 推理方法）
> 提取策略：全量扫描全书（Ch1–Ch26 + 附录），合并去重，宁错杀不筛选。
> 判断标准：该结构能否迁移到交易以外的决策场景 → 是则为框架。

---

- id: f01
  title: 市场走在前面（晴雨表 / 领先指标框架）
  type: framework
  source_chapter: 第3章 第一项基本原理：市场走在前面
  source_quote: |
    "市场价格的变化不仅反映过去，而且反映未来。将要发生的事情投下它们的影子，照在纽约证券交易所。"
  summary: |
    价格不是对新闻的事后反应，而是对未来的提前消化；市场是经济的领先指标（典型领先 6–9 个月）。
    迁移价值：在判断"某系统将走向何方"时，先看其价格/信号是否早已反映预期，而非等新闻确认。
    群体共识与价格行为，往往比权威预测更早泄露变化方向。
  tags: [leading-indicator, anticipation, mental-model, market-psychology]

- id: f02
  title: 市场是非理性的（群体情绪框架）
  type: framework
  source_chapter: 第4章 第二项基本原理：市场是非理性的
  source_quote: |
    "市场可能对事件反应非常快，但这是主观的、感性的，并且被人们的狂想所控制……价格随大众的疯狂和冷漠而摇摆，而不是由证券价值决定。"
  summary: |
    每个参与者都试图理性，但集体行为表现出非理性；价格由希望、恐惧、贪婪驱动，而非单纯由内在价值决定。
    迁移价值：不要假设"集体 = 理性个体之和"。在群体决策、舆论场、组织行为中，情绪共振会系统性偏离基本面。
  tags: [irrationality, crowd, mental-model, market-psychology]

- id: f03
  title: 确定性混沌（复杂系统不可长期预测的元框架）
  type: framework
  source_chapter: 序言 + 第5章 第三项基本原理：混沌支配
  source_quote: |
    "理解流动性金融市场动力学的最佳整体框架模型是确定性混沌，而不是随机漫步。"
  summary: |
    由反馈过程支配的系统，其运动总和不是随机而是"确定性混沌"：长期不可定量预测，但短期（非常短期）可部分预测。
    迁移价值：面对复杂自适应系统（经济、组织、生态、疫情），放弃精确长期预测，转而关注短期结构与反馈，并接受内在不可预测性。
  tags: [chaos, complex-systems, mental-model, forecasting]

- id: f04
  title: 技术图形自我实现（自我实现预言框架）
  type: framework
  source_chapter: 第6章 第四项原理：技术图形自我实现
  source_quote: |
    "如果许多人使用同样的图形系统，他们可能从中获利，而无论这些图形的实际含义是什么。"
  summary: |
    当足够多的人相信并使用同一套模式（画线、均线、软件），该模式的结果就被集体行动"制造"出来——期望创造现实。
    但若有所有人都使用同一模式，则效果会自我毁灭（图形走到众人皆知即失效）。
    迁移价值：社会事实可由共同的信念与行动创造（自我实现预言）；一旦人人都知道并利用，优势消失。
  tags: [self-fulfilling, reflexivity, mental-model, market-psychology]

- id: f05
  title: 负一阶导数（价格反映情绪的一阶变化而非水平）
  type: framework
  source_chapter: 第3章 第一项基本原理：市场走在前面
  source_quote: |
    "市场价格并不是大众感觉的直接反映，而是它的负一阶导数……虽然经济形势很好，但是如果没有更多的好消息，股市将下跌。"
  summary: |
    价格变动取决于"情绪的变化率"而非"情绪的水平"：利好出尽、无更多好消息时，即便基本面好也会跌。
    迁移价值：评估任何依赖预期的指标时，看的是"变化的速度/二阶导数"，而非绝对水平。边际变化比存量更重要。
  tags: [momentum, derivative, mental-model, expectation]

- id: f06
  title: 凯恩斯选美比赛（高阶预期 / 递归推理框架）
  type: framework
  source_chapter: 第6章 第四项原理 + 第12章 小鱼和大鱼
  source_quote: |
    "每个参加者都从同一观点出发……运用智力，推测一般人认为最美者。这已经达到了第三级推测，我相信有些人会运用到第四级、第五级。"
  summary: |
    获胜不在于"你认为什么最美"，而在于"预测别人会认为什么美，以及别人预测别人会怎么认为"。这是一层套一层的递归期望。
    迁移价值：在博弈/协调场景（竞价、舆论、择时），关键不是基本面，而是对他人预期的预期。二阶、三阶思维决定成败。
  tags: [higher-order-thinking, game-theory, recursion, mental-model]

- id: f07
  title: 领先一步 / 占位游戏（先发制人框架）
  type: framework
  source_chapter: 第1章 + 第12章 小鱼和大鱼
  source_quote: |
    "要仅仅设法先发制人，其所需智力少……玩这种职业投资者所玩把戏……音乐终止时，总有若干人占不到座位。"
  summary: |
    在由人群推动的市场中，取胜之道不是预测终极价值，而是比群众稍早一步行动、在音乐停止前离场（占位游戏）。
    迁移价值：在必然有终点的泡沫/热潮中，目标不是"正确"，而是"比别人早退出"。判断泡沫何时散场比判断价值更关键。
  tags: [first-mover, timing, game-theory, mental-model]

- id: f08
  title: 正反馈环 / 自我强化（趋势可短期预测、不可长期预测框架）
  type: framework
  source_chapter: 第5章 第三项基本原理 + 第17章 认识庞氏先生
  source_quote: |
    "正反馈意味如果你们理解动力学，你们有可能预测短期市场走势。但是，它同时意味预测长期走势是不可能的。"
  summary: |
    金融市场由强烈正反馈环支配（A→B→C→A 自我强化）：价格涨→信心增→买盘增→价格再涨。这使其短期有惯性、可跟踪，但长期必然失稳。
    迁移价值：识别任何自我强化的循环（潮流、恐慌、通胀预期、技术采纳），可顺势做短期判断，但绝不可外推为长期线性趋势。
  tags: [positive-feedback, self-reinforcement, mental-model, reflexivity]

- id: f09
  title: 蝴蝶效应（对初始条件的极端敏感框架）
  type: framework
  source_chapter: 第5章 第三项基本原理：混沌支配
  source_quote: |
    "复杂系统的计算结果与初始值有很大关系……巴西的一只蝴蝶扇扇翅膀，都可能是得克萨斯州飓风的诱因。"
  summary: |
    在非线性复杂系统中，极微小的初始差异会被指数级放大，导致结果天差地别；长期结果对细节高度敏感。
    迁移价值：对长期预测保持谦卑；小变量（关键人物、一则传闻）可能颠覆整个系统走向，长期规划应保留弹性与容错。
  tags: [butterfly-effect, sensitivity, chaos, mental-model]

- id: f10
  title: 分叉（参数越过临界值即发生体制切换框架）
  type: framework
  source_chapter: 第5章 第三项基本原理：混沌支配
  source_quote: |
    "在某个值时，曲线突然分裂成两条……这种现象被称为'分叉'，完全违背传统观念。"
  summary: |
    系统参数缓慢变化到某临界点时，平衡状态会突然从 1 个裂变为多个乃至混沌——平稳状态并非渐变，而是突变。
    迁移价值：许多系统的危机不是线性恶化，而是在临界参数越过时骤然切换。监控"临界指标"比监控平均值更重要。
  tags: [bifurcation, regime-shift, chaos, mental-model]

- id: f11
  title: 逆向思维（共识极端化时反向下注框架）
  type: framework
  source_chapter: 第13章 小鱼和大鱼
  source_quote: |
    "如果大多数人建议买进，你就卖出；大多数人建议卖出，你就买进。"
  summary: |
    当职业咨询家/媒体/散户高度一致地看多（好友指数 >70）或看空（<30）时，市场正处于派发或吸筹尾声，反向操作更优。
    迁移价值：群体共识的极端一致往往是转折信号（"大家都看出来的，显然是错误的"）。共识是反向指标，而非确认。
  tags: [contrarian, consensus, mental-model, market-psychology]

- id: f12
  title: 自我验证过程（价格反向影响真实价值框架）
  type: framework
  source_chapter: 第1章 理性人和真实世界
  source_quote: |
    "价格波动影响真实价值……当价格上升时，价值也相应提高。上述推理同样适用于股票。"
  summary: |
    价格涨跌会改变基本面：股价上涨→信用改善、融资更容易、用户信心增强→真实价值提高；反之亦然。因果是双向的，不是单向反映。
    迁移价值：叙事/价格/估值会反塑现实（如公司估值高反而更易招揽人才与资本）。避免"价格只是价值反映"的单向思维。
  tags: [reflexivity, self-verification, mental-model, value]

- id: f13
  title: 锚定与框架效应（无关参照点扭曲决策框架）
  type: framework
  source_chapter: 第14章 框架和态度
  source_quote: |
    "所谓参照点（又称'锚定点'）是指那些看起来可以提供答案线索的事物……框架则是指表述问题的方式。"
  summary: |
    面对难题时，人会不自觉被眼前无关的数字"锚定"（如转盘随机数影响对非洲国家数的估计），并被问题的表述方式"框住"。
    迁移价值：任何估算/判断都需警惕无关锚点与表述陷阱。先剥离锚点、重构问题，再做独立判断。
  tags: [anchoring, framing, bias, decision-framework]

- id: f14
  title: 群体思维 / 从众（压力情境下随大流框架）
  type: framework
  source_chapter: 第14章 框架和态度
  source_quote: |
    "如果看到前面的人这样做，将有1/3的人也会跟随，否认明显的事实……群体思维主要出现在精神高度紧张或情况非常复杂的时候。"
  summary: |
    在紧张或复杂情境下，人会放弃独立判断、跟随群体（阿什线段实验：前面 3 人说错，47% 跟随）。金融价格本身就成了最强参照点。
    迁移价值：越是不确定/高压的环境，越要主动保留独立判断。群体一致≠事实正确，往往是恐慌或狂热的放大器。
  tags: [groupthink, conformity, social-comparison, mental-model]

- id: f15
  title: 预期理论 / 损失厌恶（收益与损失非对称框架）
  type: framework
  source_chapter: 第18章 牛市与熊市的差异
  source_quote: |
    "人们对于收益和损失的态度是不一样的，即：人们更愿意赌损失而非收益。"
  summary: |
    面对等价的得与失，人对损失更敏感（卡尼曼-特维斯基）。在收益端倾向落袋为安（风险厌恶），在损失端倾向死扛豪赌回本（风险寻求）。
    迁移价值：决策不是围绕"绝对盈亏"，而是围绕"参照点（成本价）"的得与失。理解对方在收益端保守、损失端冒险，可预测其行为。
  tags: [prospect-theory, loss-aversion, bias, decision-framework]

- id: f16
  title: 后悔理论 / 处置效应（避免证明自己错框架）
  type: framework
  source_chapter: 第15章 趋势开始形成 + 第18章
  source_quote: |
    "后悔理论假设我们竭力避免那些证明自己错了的行动。"
  summary: |
    人极力回避会证明自己错误的行动：所以持有亏损头寸（"还没亏，只是浮亏"）、急于了结盈利头寸。典型表现为"卖赢持亏"。
    迁移价值：评估持仓/承诺时，用"如果今天空仓，我还会买它吗？"切断沉没成本与自我辩护，避免被"证明自己没错"的冲动绑架。
  tags: [regret-theory, disposition-effect, bias, decision-framework]

- id: f17
  title: 事后偏见（"我早知道"错觉框架）
  type: framework
  source_chapter: 第15章 趋势开始形成
  source_quote: |
    "一旦我们听说几种可能性中的某一种发生时，我们改变了在知道这件事之前的看法。我们现在可能会认为，我们早就有这种预感，知道它会发生。"
  summary: |
    事件发生后，人会重构记忆，以为自己"早就知道会这样"，从而高估自身预测能力，并急于在价格回落到错误价位时补救。
    迁移价值：警惕复盘时的"后见之明"。记录事前判断，区分"真预测"与"事后合理化"，避免据此过度自信地加大赌注。
  tags: [hindsight-bias, bias, decision-framework]

- id: f18
  title: 代表性效应（近期趋势外推为常态框架）
  type: framework
  source_chapter: 第14章 框架和态度 + 第17章
  source_quote: |
    "我们倾向于认为最近的趋势在将来有可能延续下去。我们可以称之为'方向参照'。这种精神外推有时叫做'代表性效应'。"
  summary: |
    人倾向用"与过去相似"来判断未来，于是把刚发生的趋势当作"典型"，认为它会一直延续（趋势市的心理燃料）。
    迁移价值：任何基于"最近一直如此"的外推都需打折。代表性启发式在平稳期有用，在拐点处最危险（把趋势当常态）。
  tags: [representativeness, extrapolation, bias, mental-model]

- id: f19
  title: 错误舆论效应（高估同道人数框架）
  type: framework
  source_chapter: 第15章 趋势开始形成
  source_quote: |
    "我们过于重视有多少人同意我们的态度和看法。这种偏见被称为'错误的舆论效应'……它让我们在必须旁观时随波逐流。"
  summary: |
    人系统性高估与自己持相同意见的人数；于是更安心地随大流，并在该旁观时盲目跟随。
    迁移价值：不要被"大家都这么想"安抚。主动清点真实分布（数据而非感觉），共识的虚高常是危险的来源。
  tags: [false-consensus, bias, mental-model]

- id: f20
  title: 沉没成本谬误（已投入越多越不肯撤框架）
  type: framework
  source_chapter: 第25章 风险暴露和时机选择
  source_quote: |
    "在投资者心目中，沉没成本谬误非常普遍。人们买进一只股票后，它开始下跌，然后他们买进更多，以期降低平均成本。"
  summary: |
    已付出越多（钱、时间、面子），越难退出；甚至为"摊低成本"加倍下注。实验显示：花 15 美元买的票比花 8 美元更愿意去看。
    迁移价值：决策只问"从当下看是否值得做"，与已投入无关。用"若今天空仓还会买吗？"破除沉没成本绑架。
  tags: [sunk-cost, fallacy, decision-framework]

- id: f21
  title: 金字塔形 / 倒金字塔形（仓位随胜败伸缩框架）
  type: framework
  source_chapter: 第25章 风险暴露和时机选择 + 第26章 毁灭之路
  source_quote: |
    "金字塔形表示当我们赢利时，我们不断追加投资，但是追加数量逐步减少……倒金字塔形……我们不断地将所有的利润都投入到同一只股票上，增加我们的风险暴露。"
  summary: |
    正确扩张：盈利后加仓但每笔递减（金字塔），使风险随信心增长而收敛。错误扩张：亏损后不断加码摊平（倒金字塔），趋势一反即崩塌。
    迁移价值：任何加杠杆/扩规模的行为，都应"赢时收敛加注、亏时绝不加倍赌回"。倒金字塔是自我毁灭的标准路径。
  tags: [position-sizing, pyramiding, risk, decision-framework]

- id: f22
  title: 风险暴露与时机选择彻底分离（仓位与择时解耦框架）
  type: framework
  source_chapter: 第25章 风险暴露和时机选择
  source_quote: |
    "我们的境界是实现风险暴露策略和时机选择策略的彻底分离……这种策略丝毫不应该受到以前盈亏的影响。"
  summary: |
    把"风险暴露（能承受的最大最坏损失、按基本/次要/末位三级分层）"与"时机选择（纯看市场信号）"拆成两个独立决策，互不污染。
    迁移价值：重大决策应分离"我愿承担多大风险"与"现在该不该动"。让盈亏历史、情绪不去篡改风险预算。
  tags: [risk-exposure, separation, decision-framework]

- id: f23
  title: 知识态度半衰期（态度改变需要时间框架）
  type: framework
  source_chapter: 第14章 框架和态度 + 第15章 + 第21章
  source_quote: |
    "态度一旦形成……半衰期……一般是6个月左右。但是……改变主要趋势的心理是需要时间的……当价格发生变化时，移动平均线通常要经过一段时间才能赶上来。"
  summary: |
    人的态度（对市场的认知）形成后需数月才衰减、改变；价格变了，心理适应要滞后一段时间。趋势反转靠"时间 + 反复确认"逐步完成。
    迁移价值：改变他人/组织看法不能靠一次冲击，而靠持续、重复的信号（半衰期）。耐心给认知以消化时间，否则信号被无视。
  tags: [attitude, half-life, time, mental-model]

- id: f24
  title: 身体标志 / 恐慌螺旋（压力→身体反应→抛售正反馈框架）
  type: framework
  source_chapter: 第24章 动物本性
  source_quote: |
    "价格下跌产生精神压力，精神压力引起态度迅速改变。这导致新的卖压，反过来又促使价格进一步下跌……这个妖魔终于现形。"
  summary: |
    暴跌→焦虑/恐慌（肾上腺素串联放大）→态度在数秒内崩塌→抛售→价格再跌→更强压力，形成自我强化的恐慌螺旋（达马西奥"身体标志"理论）。
    迁移价值：危机中的集体行为会脱离理性、被生理应激驱动。识别"恐慌螺旋"才能避免在低点被情绪裹挟，也才能预判崩盘的加速度。
  tags: [panic, feedback-loop, somatic-marker, mental-model]

- id: f25
  title: 趋势延续直至证伪（牛顿第一定律在金融框架）
  type: framework
  source_chapter: 第15章 趋势开始形成 + 第19章
  source_quote: |
    "道氏会说：'趋势仍然有效，除非你能证明它的反面成立。'有人称之为牛顿第一定律在金融市场的推广。"
  summary: |
    趋势默认延续，直到出现明确反证（更高的底被跌破、头部/底部结构破坏、广度丧失）。在证伪前，回调是加仓机会而非反转。
    迁移价值：面对既有趋势，用"除非证伪否则延续"的默认态度，避免在噪音中频繁转向；把精力放在寻找真正的反转证据上。
  tags: [trend, persistence, falsification, mental-model]

- id: f26
  title: 和谐共振 / 广度验证（相关信号互证才可信框架）
  type: framework
  source_chapter: 第16章 和谐与共振
  source_quote: |
    "如果没有得到运输股票的响应，工业股票的上涨不会持续太久……如果市场没有彼此验证，价格波动一定是由于非理性投机而产生的。"
  summary: |
    单一领涨不可信，须看相关市场/板块是否共振响应（道氏：工业涨须运输涨来印证；广度指标如腾落线、新高新低、扩散度验证趋势健康）。
    迁移价值：判断一个信号是否真实，看其是否得到"相邻维度"的互相确认。孤立的异常往往是噪声或操纵，共振才有持续性。
  tags: [confirmation, breadth, resonance, mental-model]

- id: f27
  title: 牛熊心理不对称（盈亏框架驱动行为差异框架）
  type: framework
  source_chapter: 第18章 牛市与熊市的差异
  source_quote: |
    "牛市的成交量一般大于熊市的成交量……答案来源于人的心理（不是逻辑）……当市场上涨时……很多股民将赚到的钱归功于自己超过常人的投资水平（自负）。"
  summary: |
    同一人在不同盈亏框架下行为相反：赚钱时归因于自身能力→频繁交易（牛市放量、自负）；亏损时否认失败、冻结不动（熊市缩量、后悔）。
    迁移价值：识别"人在赢/亏两种状态下会如何变"，可预测对手行为（赢家躁动、输家瘫软）。别假设人始终理性一致。
  tags: [bull-bear, asymmetry, overconfidence, mental-model]

- id: f28
  title: 10步测试法（先判市场状态再定策略框架）
  type: framework
  source_chapter: 第25章 风险暴露和时机选择
  source_quote: |
    "找到你要评估的图形，把它挂在墙上，后退10步，盯住它看。然后问自己：趋势继续保持吗？趋势开始反转？是否上下波动？"
  summary: |
    决策前先退一步判断宏观状态：是趋势市、反转市，还是成交密集区（平衡市）？三种状态对应完全不同的操作策略，且不能混用（毁灭之路之一即"所有市况用同一策略"）。
    迁移价值：面对复杂局面，先分类（趋势/反转/震荡）再行动。状态识别错了，再好的战术也白费；切忌一套方法通吃所有环境。
  tags: [state-classification, decision-framework, market-psychology]

- id: f29
  title: 毁灭之路（反模式清单·取其反面即生存法则框架）
  type: framework
  source_chapter: 第26章 毁灭之路
  source_quote: |
    "我们可以描述'毁灭之路'，其直接推论是：如果我们逆流而上，我们也许不会过得太糟。"
  summary: |
    作者把"如何稳定地亏光"总结为 20 条反模式（听信谣言、只看重听的话、曲解信息、随大流买卖、无风险策略、
    亏损后摊平、所有市况用同一策略、反复改止损、用对冲隐瞒亏损……）。其方法论价值在于：先穷举失败路径，
    再逐一取反，即得稳健路径。这种"先列反模式再逆向推导正确做法"的结构可迁移到任何风险决策领域。
  tags: [anti-pattern, inversion, risk, mental-model]

- id: f30
  title: 心理账户 / 玩庄家的钱（盈利后风险偏好异化框架）
  type: framework
  source_chapter: 第17章 认识庞氏先生
  source_quote: |
    "社会心理学家把这一现象称为'玩庄家的钱'：他们将自己最近的收获与其他财富分开，只在脑海中承认这笔钱。"
  summary: |
    人将新赚来的钱在心理上隔离为"庄家的钱"，用它去冒险的意愿远高于用本金。盈利反而推高风险偏好，
    亏损时又相反地冻结不动（见 f15/f16）。这解释了泡沫晚期加速与熊市缩量。
    迁移价值：警惕"用浮盈去博更大风险"的账户隔离错觉；评估风险时用整体资金视角，而非被分段账户麻痹。
  tags: [mental-accounting, house-money, bias, decision-framework]

- id: f31
  title: 说服效应（可信来源压倒可信论据框架）
  type: framework
  source_chapter: 第14章 框架和态度
  source_quote: |
    "说服效应。我们更容易被一个可信的消息来源所说服，而不是可信的论据。"
  summary: |
    人判断信息时，来源的"可信度"（权威、名人、价格本身）比论据本身的逻辑质量更能改变态度。
    故记者/分析师会顺着价格趋势措辞，价格本身也成了最有力的"可信来源"。
    迁移价值：任何说服场景（舆情、销售、管理沟通）中，先分辨"被谁说服"与"被什么论据说服"；
    对高权威低证据的信号保持警觉，不被来源光环替代逻辑检验。
  tags: [persuasion-effect, source-credibility, bias, decision-framework]
