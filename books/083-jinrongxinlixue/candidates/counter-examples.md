# 反例 / 失败模式 / 陷阱 / 误区 · 《金融心理学》
# 提取自拉斯·特维德《金融心理学》（中文版，中信 2013），检索式取块 + 全量扫尾
# 分类：认知偏差类 / 操作纪律类 / 错误信念类 / 群体陷阱类
# 字段：id / title / type / source_chapter / source_quote / failure_mode / mechanism / warning_signs / bound_to / summary / tags

# ===== 一、操作纪律类（作者明确列的「毁灭之路」及仓位/风险心理） =====

- id: ce01
  title: 倒金字塔加注
  type: counter-example
  source_chapter: 第25章 风险暴露和时机选择 · 第26章 毁灭之路(13)
  source_quote: |
    "这种系统被称为『倒金字塔形』，它是一种高度紧密连接的投资，我们不断地将
    所有的利润都投入到同一只股票上，增加我们的风险暴露……当道氏理论的某一种
    与趋势相反的、不可避免的反应开始出现的时候，它最终是要倒塌的。"
  failure_mode: |
    赢利后不断把全部利润再加码同一标的，风险暴露随盈利同步放大；一旦趋势出现
    与方向相反的必然回撤，杠杆式仓位瞬间坍塌，新手往往第一次交易就是最后一次。
  mechanism: |
    把"盈利"误当"安全垫"，实则盈利越多风险敞口越大；正反馈让人越涨越加，缺乏
    基本/次要/末位三级风险暴露的递减约束。
  warning_signs:
    - '盈利后持续加码同一标的而非金字塔式递减'
    - '账户风险暴露随浮盈同步上升'
    - '"这次不一样，还能涨"的兴奋感'
  bound_to:
    - '"金字塔形风险暴露（赢利后追加量逐步减少）"'
    - '"基本/次要/末位三级风险暴露策略"'
  summary: 倒金字塔加注是作者点名"绝对可以让我们在股市赔个精光"的头号仓位错误。
  tags: [counter-example, discipline, position-sizing, ruin-path]

- id: ce02
  title: 靠下跌摊平成本
  type: counter-example
  source_chapter: 第25章 风险暴露和时机选择 · 第26章 毁灭之路(13)
  source_quote: |
    "人们买进一只股票后，它开始下跌，然后他们买进更多，以期降低平均成本。
    然后又开始下跌，他们再买进更多。亏了就是亏了，你要么亏要么赚，但是亏了的
    是不可能赚回来的。"
  failure_mode: |
    标的下跌后持续加仓"摊低成本"，把亏损头寸越做越大，期待反转回本；最终深套
    或爆仓，且无法挽回损失。
  mechanism: |
    沉没成本谬误 + 厌恶实现亏损的心理，使人在不利头寸上不断投入新资金，违反
    "风险暴露与基本趋势相反时应可预防"的原则。
  warning_signs:
    - '持仓亏损后第一反应是"再加点拉低均价"'
    - '不愿承认初始判断错误'
    - '越跌越买且仓位越来越重'
  bound_to:
    - '"明确止损策略（跌破成交密集区即出局）"'
    - '"每日自检：若今天没有它，我还会买吗？不会就卖"'
  summary: 摊平成本是沉没成本谬误在交易中的典型表现，索罗斯明确反对"靠它挽回损失"。
  tags: [counter-example, discipline, sunk-cost, averaging-down]

- id: ce03
  title: 与趋势作对 + 频繁改动止损
  type: counter-example
  source_chapter: 第25章 成交密集区交易 · 第26章 毁灭之路(15)
  source_quote: |
    "与趋势作对，当然不会有好结果……许多投资者在趋势的中期改变了自己的心理
    轨迹，将每一个趋势中断和成交密集区都当成趋势反转……损失惨重。"
    "当市场与你作对时，不断地改变止损值，因为你一直在做反转的美梦。"
  failure_mode: |
    把趋势途中的正常回调/成交密集区误判为反转，逆势操作；亏损后不执行原止损，
    反而不断把止损位挪远，死等"反转美梦"。
  mechanism: |
    趋势的自我强化（正反馈）使中途震荡极多，逆势者反复被洗；改止损是用希望代
    替纪律，敞口在无意识中放大。
  warning_signs:
    - '在强势趋势中猜顶/抄底'
    - '亏损后把止损价越调越远'
    - '"这肯定是最后一次恐惧冲动"的自我安慰'
  bound_to:
    - '"趋势市：买强弃弱，跌破成交密集区才止损"'
    - '"趋势越强，破坏前所需证据越多"'
  summary: 与趋势作对且改止损，是把短期噪音当反转、用幻想覆盖纪律的双重错误。
  tags: [counter-example, discipline, trend-fighting, stop-loss]

- id: ce04
  title: 一套方法通吃所有市况
  type: counter-example
  source_chapter: 第26章 毁灭之路(14)
  source_quote: |
    "无论市场处于趋势市、成交密集区还是处于转折市，都使用同一操作策略。"
  failure_mode: |
    用同一种策略应对趋势市、平衡市、转折市三种完全不同的心理结构，必然在某一
    类市况中系统性亏损。
  mechanism: |
    三类市况（趋势/成交密集区/反转）各有独特交易策略；"10步测试法"先判定市况
    再选策略，混用则失去决策可信度。
  warning_signs:
    - '不先判断"趋势/震荡/反转"就直接套用熟悉手法'
    - '同一种止损/仓位规则用遍所有环境'
  bound_to:
    - '"10步测试法（趋势继续/反转/上下波动先定性）"'
    - '"成交密集区买弱弃强 vs 趋势市买强弃弱"'
  summary: 不分市况统一策略，是作者对"毁灭之路"明确列出的第14条。
  tags: [counter-example, discipline, regime-fit]

- id: ce05
  title: 用对冲隐瞒损失而非壮士断腕
  type: counter-example
  source_chapter: 第26章 毁灭之路(18)
  source_quote: |
    "利用对冲隐瞒损失，而不是壮士断腕。"
  failure_mode: |
    亏损后用对冲（如反向头寸、复杂衍生组合）遮掩账面损失，拖延决策，使小亏拖
    成大亏，并掩盖真实风险。
  mechanism: |
    回避实现亏损带来的心理痛苦（自我防御态度），用账面"中性"自欺，错失止损时机。
  warning_signs:
    - '亏损后以加对冲代替砍仓'
    - '组合越来越复杂只为"看起来没亏"'
  bound_to:
    - '"明确止损纪律"'
    - '"风险暴露策略与时机策略彻底分离"'
  summary: 以对冲藏亏是自我防御态度驱动的拖延，违背"壮士断腕"。
  tags: [counter-example, discipline, hedging, denial]

- id: ce06
  title: 短线亏损守成"长线投资"
  type: counter-example
  source_chapter: 第26章 毁灭之路(10-12)
  source_quote: |
    "仅仅一个星期就退出所有长期投资，原因是已经获利……如果亏损，就守住短线
    投资……并且其美名曰『长线投资』。"
  failure_mode: |
    盈利的仓位拿不住（过早落袋），亏损的仓位反而"长线持有"，美其名曰价值投资，
    实质是把短线错误拖成长期套牢。
  mechanism: |
    处置效应（急于实现盈利、回避实现亏损）+ 自我说服效应（为套牢找理由）。
  warning_signs:
    - '赚钱的单子拿几天就跑，亏钱的单子越拿越久'
    - '给套牢头寸贴上"长期价值"标签'
  bound_to:
    - '"有限度地亏，无限度地赢"'
    - '"趋势不再维持即出局"'
  summary: 盈短亏长，是处置效应在仓位管理上的经典失败模式。
  tags: [counter-example, discipline, disposition-effect]

- id: ce07
  title: 从不明确风险策略、不抓大机遇
  type: counter-example
  source_chapter: 第26章 毁灭之路(9)
  source_quote: |
    "从来不明确任何形式的风险策略，不抓住大机遇。"
  failure_mode: |
    没有风险暴露框架，全凭感觉进出；趋势性大行情来临时因无计划而仓位过小或错失。
  mechanism: |
    风险暴露永远应是策略出发点（基于金融痛苦临界点）；缺位则无法在三级信号同向
    时"尽全力参与"。
  warning_signs:
    - '开仓前算不清"最坏损失"'
    - '大行情中犹疑、仓位不足'
  bound_to:
    - '"风险暴露策略（基本/次要/末位三级）"'
    - '"信号同向时全力参与"'
  summary: 无风险策略是毁灭之路第九条，使投资者在机会与风险前都失据。
  tags: [counter-example, discipline, risk-exposure]

- id: ce08
  title: 依赖谣言/熟人/出租车司机建议
  type: counter-example
  source_chapter: 第26章 毁灭之路(1-2)
  source_quote: |
    "选择一些专业小规模市场，始终炒作它们。将自己对市场的认识建立在信息杂烩
    基础上，这些杂烩包括谣言、谣传、熟人或出租车司机的建议。"
  failure_mode: |
    信息源杂乱、无验证，把小道消息当决策依据，尤其在流动性差的小市场易被操纵。
  mechanism: |
    公共信息瞬间被市场贴现无交易价值；真正有价值的往往是独有信息，但道听途说
    既非独有也未经核实。
  warning_signs:
    - '决策依据是"听人说""群里看到的"'
    - '集中交易冷门小市场'
  bound_to:
    - '"信息价值层级（内部人>套利者>散户）"'
    - '"公共信息无新闻价值，只看独有信息"'
  summary: 以信息杂烩为认知基础，是毁灭之路开篇两条。
  tags: [counter-example, discipline, information-hygiene]

- id: ce09
  title: 用市价而非基本价值作判断准则
  type: counter-example
  source_chapter: 第26章 毁灭之路(17)
  source_quote: |
    "用市场价格而不是基本价值作为你的判断准则。"
  failure_mode: |
    把当前价格当作"该不该买卖"的唯一依据，追涨杀跌，忽视价格偏离基本面的方向。
  mechanism: |
    市场价格是他人行为的参照点（锚），易被正反馈裹挟；价格本身不提供价值判断。
  warning_signs:
    - '"涨了所以该买，跌了所以该卖"的纯价格驱动'
    - '不看基本面/估值锚'
  bound_to:
    - '"市场走在前面（价格反映预期而非价值）"'
    - '"内部人交易比千份预测更可靠"'
  summary: 以价格替代价值作准则，混淆了"参照点"与"判断基准"。
  tags: [counter-example, discipline, price-anchor]

- id: ce10
  title: 基于偶然价格跳动而非图形全面分析行动
  type: counter-example
  source_chapter: 第26章 毁灭之路(8)
  source_quote: |
    "根据价格的偶然变化（在计算机屏幕上或股票行情上）采取行动，而不是对图形的
    全面分析。"
  failure_mode: |
    被分时/逐笔的随机跳动牵着走，频繁交易，忽视更大周期图形与成交密集区结构。
  mechanism: |
    短期波动多属噪音（噪音区难以预测）；只在边缘支撑/阻力区突破才有意义。
  warning_signs:
    - '看盘口/分时即下单'
    - '不做多周期图形分析'
  bound_to:
    - '"趋势越强看图越久越深入"'
    - '"基于收盘价评估突破有效性"'
  summary: 被偶然跳动驱动交易，是毁灭之路第八条。
  tags: [counter-example, discipline, noise-trading]

- id: ce11
  title: 孤立看待每一项投资、忽视广度
  type: counter-example
  source_chapter: 第26章 毁灭之路(19) · 第16章 和谐与共振
  source_quote: |
    "孤立地看待每一项投资活动。忘记了这是世界上最艰巨的市场。"
    "如果整个市场开始下跌，那么所有股票重心都要下移，无论它是『便宜』还是
    『贵』。恐慌时，人们卖出手中所有可以卖出的股票。"
  failure_mode: |
    只盯单只标的，不看市场广度/相关性；系统性下跌时独立个股无一幸免。
  mechanism: |
    股票彼此影响，广度（市场相似性）决定个股重心；单股"便宜"在系统性风险前无效。
  warning_signs:
    - '只研究个股不看病态大盘'
    - '忽视板块/指数共振'
  bound_to:
    - '"广度/市场相似性（大盘险峻则推迟买个股）"'
    - '"和谐与共振"'
  summary: 孤立投资忽视系统性关联，是毁灭之路第十九条。
  tags: [counter-example, discipline, breadth]

# ===== 二、认知偏差类（系统性心理偏误） =====

- id: ce12
  title: 沉没成本谬误
  type: counter-example
  source_chapter: 第25章 风险暴露和时机选择（沉没成本谬误）
  source_quote: |
    "钱花得越多，就越有可能来看演出……你要么想看演出并愿花30美元，要么不想，
    与你丢了现金还是丢了票毫无关系。但很多人觉得损失了沉没成本，要投更多钱在
    曾经付出的东西上。"
  failure_mode: |
    因已投入（金钱/时间/情感）而继续投入，决策被过去成本绑架而非未来预期驱动。
  mechanism: |
    自我防御态度拒绝承认亏损；把"已付出"误当"继续的理由"。
  warning_signs:
    - '"已经亏这么多了，再等等"'
    - '因舍不得已交的"学费"而硬扛'
  bound_to:
    - '"止损纪律"'
    - '"『若今天没有它还会买吗』自检"'
  summary: 沉没成本谬误是摊平、死扛等失败操作的心理根源。
  tags: [counter-example, cognitive-bias, sunk-cost]

- id: ce13
  title: 代表性效应 / 方向参照（线性外推）
  type: counter-example
  source_chapter: 第14章 框架和态度（当金融价格成为精神参照点）
  source_quote: |
    "我们有一种非理性的倾向，就是认为最近的价格变化趋势会延续下去……这种精神
    外推有时叫做『代表性效应』，它意味着我们倾向于认为最近的趋势在将来有可能
    延续下去。"
  failure_mode: |
    把"近期趋势"当作"未来必然延续"，在趋势末端仍线性外推，接最后一棒。
  mechanism: |
    代表性启发：以相似性判断概率，误将"一直涨"等同于"还会涨"，忽略分叉与反转。
  warning_signs:
    - '"都涨这么久了肯定还能涨"'
    - '用过去N日斜率直接推断未来'
  bound_to:
    - '"趋势反转预警（不再创新高/更低头部）"'
    - '"动量极值=调整警告"'
  summary: 代表性效应是泡沫形成与接盘的认知燃料。
  tags: [counter-example, cognitive-bias, representativeness, extrapolation]

- id: ce14
  title: 锚定效应（转盘实验）
  type: counter-example
  source_chapter: 第14章 框架和态度（转盘实验）
  source_quote: |
    "抽中大的随机数的正常人，普遍认为联合国中非洲国家的数量多于那些抽中小的
    随机数的人。"
  failure_mode: |
    决策被先入为主的随机参照点锚定，对真实数值的估计严重偏离，且当事人不自知。
  mechanism: |
    参照点（锚）提供"看似正确答案"的输入，框定后续判断（术语：参照点/锚定）。
  warning_signs:
    - '买入价/前期高点成心理锚，影响买卖'
    - '"它曾经到过X"式推理'
  bound_to:
    - '"以基本价值而非市场价格作判断"'
    - '"图形全面分析"'
  summary: 锚定使投资者被无关或过去的数字绑架。
  tags: [counter-example, cognitive-bias, anchoring]

- id: ce15
  title: 事后偏见（早就知道效应）
  type: counter-example
  source_chapter: 第15章 趋势开始形成（事后偏见和急跌买进）
  source_quote: |
    "一旦我们听说几种可能性中的某一种发生时，我们改变了在知道这件事之前的看法。
    我们现在可能会认为，我们早就有这种预感……如果价格跌回到我们最初犯错误的
    价位时，我们非常想买回来。"
  failure_mode: |
    事件发生后高估自己事前的预判能力（"我早知道"），并因此更急于"纠错"追涨杀跌。
  mechanism: |
    记忆重构 + 自我说服效应，导致过度自信与追悔性交易。
  warning_signs:
    - '"我早就说会跌"'
    - '跌回原错误价位就忍不住买回'
  bound_to:
    - '"记录事前计划，避免记忆重构"'
    - '"与趋势作对警告"'
  summary: 事后偏见放大追悔交易，是崩盘后盲目抄底的心理推手。
  tags: [counter-example, cognitive-bias, hindsight-bias]

- id: ce16
  title: 适应态度 / 从众同化
  type: counter-example
  source_chapter: 第14章 框架和态度（适应态度）
  source_quote: |
    "我们无意识地形成和我们认同的人一样的态度……当我们的银行、经纪人和朋友告诉
    我们股票要上涨时，我们在形成同样的看法，不是通过逻辑推理，而是在潜意识地
    适应他们。"
  failure_mode: |
    无意识模仿周围人（银行/经纪人/朋友）的观点，形成一致性错觉，丧失独立判断。
  mechanism: |
    社会比较 + 适应态度：人作为社会动物默认同化，且常犯"对比错误"嘲笑异见者。
  warning_signs:
    - '观点与朋友圈/媒体完全一致且无逻辑依据'
    - '对异见者本能排斥嘲笑'
  bound_to:
    - '"逆向思维（好友指数极值反向）"'
    - '"独立判断信息价值"'
  summary: 适应态度是群体癫狂与泡沫得以蔓延的心理基础。
  tags: [counter-example, cognitive-bias, conformity, adaptive-attitude]

- id: ce17
  title: 错误舆论效应
  type: counter-example
  source_chapter: 第15章 趋势开始形成（错误的舆论效应）
  source_quote: |
    "我们过于重视有多少人同意我们的态度和看法……这种偏见被称为『错误的舆论
    效应』……它让我们在必须旁观时随波逐流。"
  failure_mode: |
    以"多少人同意"来衡量自己决策的安全感，人多即安心，最终随大流接盘或踏错。
  mechanism: |
    将共识误当正确性（混淆"流行"与"正确"），强化从众。
  warning_signs:
    - '"大家都这么看，应该没错"'
    - '用赞同人数替代证据'
  bound_to:
    - '"共识往往错（逆向思维）"'
    - '"内部人/套利者信号优于大众"'
  summary: 错误舆论效应把"多数同意"错当安全背书。
  tags: [counter-example, cognitive-bias, false-consensus]

- id: ce18
  title: 选择性暴露与选择性感知
  type: counter-example
  source_chapter: 附录6 术语（选择性暴露 / 选择性感知）
  source_quote: |
    "选择性暴露：我们只是试图暴露对我们行为和态度有利的信息。
     选择性感知：我们曲解信息，使它看起来可以验证我们的行为和态度。"
  failure_mode: |
    只接收支持自己头寸的信息，并曲解中性/反面信息以维护原有观点，陷入确认偏误。
  mechanism: |
    态度先于事实：先有立场再筛信息，同化错误（把信息误读为支持己见）。
  warning_signs:
    - '只看看涨/看跌一方研报'
    - '把利空解读为"洗盘"'
  bound_to:
    - '"曲解信息适应所为（毁灭之路4）的反面"'
    - '"独立信息验证"'
  summary: 选择性暴露/感知是"曲解信息适应所为"的术语化表述。
  tags: [counter-example, cognitive-bias, confirmation-bias]

- id: ce19
  title: 框架效应（收益/损失表述扭曲决策）
  type: counter-example
  source_chapter: 第18章 牛市与熊市的差异（框架实验）
  source_quote: |
    "两个问题完全相同，只是表达的方式有所差异……第一个重点在收益，72%选A；
    第二个重点在损失，只有22%选A。人们对于收益和损失的态度是不一样的。"
  failure_mode: |
    同一事实因表述框架（收益vs损失）不同而产生截然相反的"非理性"选择。
  mechanism: |
    框定：决策受输入信息的呈现方式影响，而非客观期望值。
  warning_signs:
    - '同一数据"盈利+X%"与"亏损-Y%"引发相反操作'
    - '被媒体措辞带节奏'
  bound_to:
    - '"牛熊成交量反常（框架解释）"'
    - '"客观期望值决策"'
  summary: 框架效应解释为何牛市成交量大于熊市等非逻辑现象。
  tags: [counter-example, cognitive-bias, framing-effect]

- id: ce20
  title: 过度乐观 / 分析师系统性偏见
  type: counter-example
  source_chapter: 第11章 最快的游戏（难以置信的买进）
  source_quote: |
    "每股收益年增长率预期值平均高于实际值9%……18年间有16年收益预测高于实际。
     到2001年4月，瑞士信贷跟踪1328只股票，建议卖出仅11只。"
  failure_mode: |
    轻信分析师"强力买进"等乐观评级与收益预测，忽视其系统性高估偏差。
  mechanism: |
    分析师行话隐含反向含义（"持仓"≈卖出），且受雇关系与乐观文化导致系统性偏见。
  warning_signs:
    - '把"强力买进"当无脑买入信号'
    - '忽视"卖出"建议占比极低的结构性失真'
  bound_to:
    - '"内部人交易比千份预测可靠"'
    - '"看投资建议的系统性偏见"'
  summary: 分析师乐观偏见是"专家能预测"错误信念的市场表现。
  tags: [counter-example, cognitive-bias, over-optimism, analyst-bias]

# ===== 三、错误信念类（作者重点驳斥的错误认知） =====

- id: ce21
  title: 有效市场假说（市场完全理性有效）
  type: counter-example
  source_chapter: 第3章 第一项基本原理 · 第4章 市场是非理性的
  source_quote: |
    "金融市场定价常常千奇百怪，极不理性……虽然学术界认为市场反映真实价值，因为
    人是理性的，但事实是市场定价常常极不理性。"
  failure_mode: |
    相信价格总是合理反映所有已知信息、市场有效，从而放弃对心理与反馈过程的研判。
  mechanism: |
    新古典"理性人"假设在金融市场失效；价格由希望/恐惧/贪婪驱动，常严重偏离价值。
  warning_signs:
    - '"市场总是对的/价格即合理"'
    - '否认泡沫与恐慌的存在'
  bound_to:
    - '"市场是非理性的（原理二）"'
    - '"确定性混沌框架"'
  summary: 有效市场假说是本书重点批判的错误信念，对应原理二"市场是非理性的"。
  tags: [counter-example, false-belief, efficient-market]

- id: ce22
  title: 经济/市场可用线性模型精确预测
  type: counter-example
  source_chapter: 第3章 第三项基本原理：混沌支配
  source_quote: |
    "传统经济模拟建立在基于均衡函数的线性模型基础上……线性模型不是不够完善，
    而是可能从本质上就搞错了。理论上正确的非线性模型也可能导致完全的不可预测性。"
  failure_mode: |
    相信宏观/市场可用传统统计与线性模型长期精确预测，据此重仓下注。
  mechanism: |
    系统含正反馈与分叉，对初始条件极端敏感（蝴蝶效应），不可预测性是内在性质。
  warning_signs:
    - '"模型说目标价X，所以买"'
    - '用长期宏观预测指导短期交易'
  bound_to:
    - '"混沌支配（原理三）：只能短期预测"'
    - '"确定性混沌框架"'
  summary: 线性外推与精确预测是作者对科学界误区的核心批评。
  tags: [counter-example, false-belief, chaos, prediction]

- id: ce23
  title: 公共新闻/财经媒体可用来赚钱
  type: counter-example
  source_chapter: 第11章 最快的游戏（新情况）
  source_quote: |
    "公共信息或许有解释价值，但很少或根本没有新闻价值。靠盯住行情显示屏播放的
    财经新闻是不可能赚钱的，更不用说看电视了。市场会瞬间让那种消息大打折扣。"
  failure_mode: |
    以为跟着公开财经新闻、电视股评买卖能获利，实则消息已被市场即时贴现。
  mechanism: |
    公共信息人人可得，价格瞬间反映；独有信息才有交易价值（且利用内幕违法）。
  warning_signs:
    - '"新闻说X利好，赶紧买"'
    - '以电视/头条为交易触发器'
  bound_to:
    - '"信息价值层级：独有信息>公共信息"'
    - '"内部人/套利者信号"'
  summary: 公共新闻无交易价值，是信息心理章的核心反例。
  tags: [counter-example, false-belief, news, information]

- id: ce24
  title: 技术图形有客观、普适的"真实含义"
  type: counter-example
  source_chapter: 第6章 技术图形自我实现 · 第10章 心理与金融结合
  source_quote: |
    "图形分析得到广泛使用的背后，不仅在于它是一种理解市场的技巧，有时还在于
    技术分析产生心理作用。如果所有人都使用同样的技术分析，那么它的效果就不是
    自我实现，而是自我毁灭。"
  failure_mode: |
    相信图形形态有独立于人心的客观含义，机械套用形态而忽视"自我实现/自我毁灭"
    的心理前提。
  mechanism: |
    图形之所以有效，是因众人同画同线产生正反馈（自我实现）；一旦人人都用，反而
    自我毁灭。第一代图学家缺理论（奇幻思维）。
  warning_signs:
    - '"头肩顶=必跌"的机械信条'
    - '忽视使用该形态的人数拥挤度'
  bound_to:
    - '"技术图形自我实现框架"'
    - '"图形是心理共振而非客观真理"'
  summary: 图形无客观含义，其有效性来自群体心理的自我实现。
  tags: [counter-example, false-belief, technical-analysis, self-fulfilling]

- id: ce25
  title: 专家/分析师能持续准确预测市场
  type: counter-example
  source_chapter: 第11章 最快的游戏（难以置信的买进）
  source_quote: |
    "分析师平均预期1980～1981年和1990～1991年有10%左右的收益增长，而实际上
    这几年是衰退期，收益是下降的。"
  failure_mode: |
    把分析师/经济学家的预测当可靠行动依据，忽视其系统性高估与低命中率。
  mechanism: |
    预测受职场激励（乐观）与认知偏差双重扭曲；详见 ce20。
  warning_signs:
    - '依据某大行目标价建仓'
    - '相信"专家共识=方向"'
  bound_to:
    - '"混沌不可预测（原理三）"'
    - '"内部人信号优先"'
  summary: '"专家能预测"是本书列为错误信念的核心之一。'
  tags: [counter-example, false-belief, expert-prediction]

- id: ce26
  title: 价值回归必然、可单靠基本面长期持有
  type: counter-example
  source_chapter: 第4章 市场是非理性 · 第25章 风险暴露
  source_quote: |
    "金融工具的价格有时因为其他原因而发生变化……市场往往表现为非理性。但是，
    它确实比科学家发现的任何其他单个指标都要来得准（作为领先指标）。"
  failure_mode: |
    坚信"价格终将回归内在价值"而长期死扛，忽略市场可在非理性中运行极久、且领先
    经济6–9个月。
  mechanism: |
    市场走在前面（原理一），短期由心理与正反馈主导，价值回归既非及时也非必然。
  warning_signs:
    - '"便宜所以不会更便宜"的长期死扛'
    - '用价值单一叙事对抗价格趋势'
  bound_to:
    - '"市场走在前面（原理一）"'
    - '"市场是非理性（原理二）"'
  summary: 纯粹价值叙事忽视市场心理层面的非理性与领先性。
  tags: [counter-example, false-belief, value-investing]

- id: ce27
  title: 图学家"奇幻思维"——无理论地宣称规律
  type: counter-example
  source_chapter: 第10章 心理与金融相结合（不是真正的理论）
  source_quote: |
    "如果用职业心理学家的眼光来看，他们的方法要么被归类为『奇幻思维』，要么被
    归类为『激进社会行为主义』……他们几乎没有解释为什么他们的『理论』或『定律』
    起作用。"
  failure_mode: |
    仅凭观察到的重复形态就宣称可预测规律，不做假设检验、无底层机制解释。
  mechanism: |
    科学要求可证伪与机制解释；缺理论的经验规律在样本外易失效（奇幻思维）。
  warning_signs:
    - '"历史多次出现所以必灵"'
    - '拒绝解释"为什么有效"'
  bound_to:
    - '"图形自我实现（有心理机制）框架"'
    - '"假说须可被检验"'
  summary: 无理论的形态崇拜是作者点名的奇幻思维。
  tags: [counter-example, false-belief, magical-thinking]

# ===== 四、群体陷阱类（群体心理导致的系统性错误） =====

- id: ce28
  title: 随波逐流（与群众同买同卖）
  type: counter-example
  source_chapter: 第26章 毁灭之路(5-6) · 第13章 逆向思维
  source_quote: |
    "当邻居和所有人似乎都在买进时你也买进，当市场已经崩溃时你才卖出……绝大多数
    时间你都认为证券市场会上涨。"
  failure_mode: |
    涨时随大流追入、崩时随大流杀出，在群体情绪的两个极端反向接盘/割肉。
  mechanism: |
    适应态度+社会比较+正反馈，使个体放弃独立判断，价格变化自身成为买卖理由
    （希勒调查：崩盘时几乎无人提及经济消息，只因"市场在跌"而卖）。
  warning_signs:
    - '周围人都在谈买/卖时你跟着动'
    - '卖出理由只是"它还在跌"'
  bound_to:
    - '"逆向思维（好友指数极值反向）"'
    - '"随波逐流真惬意（仅限政府干预失效时）"'
  summary: 随波逐流是毁灭之路第5–6条，也是群体陷阱的总纲。
  tags: [counter-example, group-trap, herding, follow-the-crowd]

- id: ce29
  title: 逆向思维滥用（大主力操纵例外）
  type: counter-example
  source_chapter: 第13章 逆向思维（相反的永远是正确的吗？）
  source_quote: |
    "逆向思维不是任何时候都起好作用……当一个大的市场主力想操纵大势时，就会
    出现这种典型的例外情况……当所有人都按逆向思维做，逆向本身也会失效。"
  failure_mode: |
    机械反大众操作，忽视"大主力操纵市场"的例外，或在人人都逆向时反而被反向收割。
  mechanism: |
    逆向有效的前提是 crowd 主导且无人操纵；主力控盘或逆向拥挤时规律反转。
  warning_signs:
    - '"大家都看多所以我必空"的机械反向'
    - '忽视主力/操纵信号'
  bound_to:
    - '"逆向思维（需警惕操纵例外）"'
    - '"人气未达临界值前不逆"'
  summary: 逆向思维不是万能钥匙，滥用会落入反向陷阱。
  tags: [counter-example, group-trap, contrarian-abuse]

- id: ce30
  title: 金融泡沫 / 庞氏式自我强化
  type: counter-example
  source_chapter: 第17章 牛市的心理（金融泡沫）· 第16章 庞氏
  source_quote: |
    "金融泡沫是一个疯狂的牛市……绝大多数利润取决于先到者把手中的货卖给后来的
    新投资者的能力，而不是来源于上市公司创造的现金流。当不再有新投资者接手时，
    整座大楼就要坍塌。"
  failure_mode: |
    在泡沫末期因"这次不一样"继续追高，成为后来接盘的最后一棒；或误信庞氏式高回报。
  mechanism: |
    所有正反馈环交织（赚钱效应→新资金→涨价）形成自我强化，脱离现金流基础。
  warning_signs:
    - '新股/概念"稳赚不赔"叙事'
    - '价格涨速远超盈利增速'
  bound_to:
    - '"正反馈环识别"'
    - '"泡沫头部（加速上行）预警"'
  summary: 庞氏/泡沫是群体正反馈的极端形态，必以坍塌收场。
  tags: [counter-example, group-trap, bubble, ponzi]

- id: ce31
  title: 崩盘恐慌正反馈（肉体心理/社会比较/框定）
  type: counter-example
  source_chapter: 第23章 追踪怪物的足迹（崩盘时的心理现象）
  source_quote: |
    "价格下跌产生精神压力，精神压力引起态度迅速改变。这导致新的卖压，反过来又
    促使价格进一步下跌……社会比较、框定、事后聪明偏见加剧了恐慌。"
  failure_mode: |
    下跌中因生理恐慌（心跳加速、出汗）与群体恐慌相互强化而恐慌性抛售，卖在最低点。
  mechanism: |
    肉体心理理论（威胁→身体反应→更恐慌）+ 社会比较（别人跑我也跑）+ 框定（价格
    跌=经济崩）。
  warning_signs:
    - '盯盘时生理紧张、急于平仓'
    - '"大家都在逃，我也逃"'
  bound_to:
    - '"明确止损（跌破密集区才动，非盘中恐慌）"'
    - '"区分噪音与反转"'
  summary: 崩盘是群体恐慌的正反馈，作者用"怪物"比喻其自我强化。
  tags: [counter-example, group-trap, crash, panic]

- id: ce32
  title: 凯恩斯选美/正反馈——猜测别人而非价值
  type: counter-example
  source_chapter: 第6章 技术图形自我实现（凯恩斯和选美比赛）
  source_quote: |
    "每个参加者都不选自己真认为最美者，而是运用智力推测一般人认为最美者……
    这已经达到了第三级、第四级推测。"
  failure_mode: |
    在"猜别人猜什么"的无限回归中迷失，决策完全脱离价值，沦为博弈预期的预期。
  mechanism: |
    正反馈环中人人猜测他人行动，价格由"他人会怎么看"驱动而非基本面。
  warning_signs:
    - '"我觉得别人觉得它会涨所以买"'
    - '完全脱离标的本身讨论"市场预期"'
  bound_to:
    - '"市场是非理性（原理二）"'
    - '"图形自我实现（群体同画同线）"'
  summary: 选美博弈揭示价格由预期链驱动，而非客观价值。
  tags: [counter-example, group-trap, keynes-beauty-contest]

- id: ce33
  title: 在平衡市/过分扩张时追高（媒体鼓吹）
  type: counter-example
  source_chapter: 第13章 逆向思维（当大家都看出来……）
  source_quote: |
    "当有那么一天，我们在报刊上猛然看到市场上升趋势『将持续几年』，或者某只股票
    已经涨了很多时还有人在鼓吹它是『很好的投资对象』时，真正的危险即将来临。"
  failure_mode: |
    在趋势已充分展开、媒体用大号字一致鼓吹时追入，恰处风险最高的拥挤区。
  mechanism: |
    媒体放大共识+错误舆论效应，使个人在极值区反向成为"接盘侠"；好友指数超买即派发尾声。
  warning_signs:
    - '主流媒体头条一致看多/看空'
    - '"将持续几年"式叙事'
  bound_to:
    - '"逆向思维（人气极值反向）"'
    - '"过分扩张时警惕"'
  summary: 媒体一致鼓吹是群体陷阱的末尾信号，而非买入信号。
  tags: [counter-example, group-trap, media, late-chase]

- id: ce34
  title: 牛熊成交量反常误判（框架解释缺失）
  type: counter-example
  source_chapter: 第18章 牛市与熊市的差异
  source_quote: |
    "『有限度地亏，无限度地赢』若普遍遵循，牛市成交量应小、熊市应大。然而事实
    恰好相反：牛市的成交量一般大于熊市的成交量。"
  failure_mode: |
    用"放量看涨/缩量看跌"的朴素量价常识，在牛市中因放量而误判顶部、熊市缩量误判底部。
  mechanism: |
    框架效应（收益/损失不对称）+ 处置效应：盈利落袋意愿强，亏损死扛，导致牛市长
    黄、熊市缩量。
  warning_signs:
    - '牛市放量就恐慌"出货"'
    - '忽视心理框架对成交量的重塑'
  bound_to:
    - '"牛熊差异框架（成交量反常的心理根源）"'
    - '"框架效应认知"'
  summary: 量价常识在牛熊不对称下失效，需以心理框架纠正。
  tags: [counter-example, group-trap, volume, framing]

- id: ce35
  title: 线性外推权威叙事（"市场会持续几年"）
  type: counter-example
  source_chapter: 第13章 逆向思维 · 第17章 泡沫
  source_quote: |
    "媒体用小号字体温柔指出趋势时无妨；当猛然看到上升趋势『将持续几年』时，真正
    的危险即将来临。"
  failure_mode: |
    接受"趋势会长期延续"的权威线性外推，在泡沫末端重仓，忽视分叉与反转的突发性。
  mechanism:
    代表性效应 + 错误舆论效应 + 媒体放大，把短期正反馈误判为永久趋势。
  warning_signs:
    - '"这次是结构性长牛"叙事'
    - '专家连篇看多且无人看空'
  bound_to:
    - '"混沌支配：长期不可预测"'
    - '"泡沫头部预警"'
  summary: 长牛叙事是群体陷阱在泡沫末期的标准化话术。
  tags: [counter-example, group-trap, extrapolation, narrative]
