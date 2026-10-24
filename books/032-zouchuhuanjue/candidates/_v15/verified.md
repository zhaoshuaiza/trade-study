格局说明：本文件是阶段 1.5（三重验证 V1 跨域 / V2 预测力 / V3 独特性）通过后的**合并去重清单**，
是阶段 2（RIA++ 能力卡）的唯一输入。每个条目已把多个提取器重复抽取的同名概念合并为一个 canonical 条目，
`sources` 字段保留原始 id 以供审计。

验证分工来源：
- v15-core（核心系统/心理层 15 概念）：7 通过 / 8 淘汰（通过率 47%）
- v15-principles24（第二章 24 命名原理）：17 通过 / 6 淘汰（通过率 74%）
- v15-misc（案例 / 术语 / 残差）：全部通过（案例 25 / 术语 19 / 残差框架 / 反例 28）

冲突裁决记录：
1. f18 套利原理 —— core 判 FAIL V3（本质是反面警示、非可迁移方法），misc 判 PASS。**裁决：REJECT**。
2. g10「赌博（作者定义）」—— core 报告写的"g10 赌博五原则被拒"实指**原则条目 p15–p19**；
   glossary 的 g10 是"交易=理性赌博"的认知底座，属作者特异定义。**裁决：g10 通过；p15–p19 另议（见边界项）**。
3. f17 亏损五境界、f19 分散/资金管理 —— core 与 misc 双份通过，**已去重合并**。
4. f20 二八法则 —— 原文核实为作者手机销售经历类比（20%努力→80%销量，要得剩余20%需再付80%），
   与 p12 优化陷阱、p13 双高"边际/不追完美"同源。**裁决：并入 SK-core-06，不单列**。

---

## A 组：核心系统 / 心理层（10 个 SLUG 候选）

- id: SK-core-01
  title: 盈亏同源——把亏损当进货成本
  type: principle
  source_chapter: 第六章 系统之路 · 成本观与盈亏同源
  source_quote: "当你规避了亏损，自然也就规避了利润，明白吗？"
  intent: 把亏损从"错误/失败"重新定义为"获取趋势利润必须垫付的进货成本"，是全书心理基石。
  application: 止损时不判断"我错了"，而是按系统必然支出支付；盈利兑现、亏损挂起的本能要反过来。
  sources: [p01, p02, f01, g01, g02, ce07]
  V1_cross_domain: {passed: true, note: "第二章·稻草压骆驼 + 第六章·系统之路 两处独立语境"}
  V2_predictive_power: {passed: true, note: "新场景：连续止损后应加仓还是减仓？按成本观，连续小亏=系统正常呼吸，应维持等额"}
  V3_exclusivity: {passed: true, why_not_common: "常识视亏损=做错了要避免；作者断言规避亏损必然同时规避利润，是同一硬币两面"}
  card_type: principle
  priority: P0

- id: SK-core-02
  title: 风险防范只有两点——保住趋势位置 + 绝对止损点
  type: principle
  source_chapter: 第六章 系统之路 · 风险防范
  source_quote: "我的风险防范策略只有两点，一个是不丢掉自己的位置，另一个是绝对的止损点。"
  intent: 断言分散、买优质股、买便宜股**都不是**风险防范，真正的风控只有这两条。
  application: 有绝对止损点后无需叠床架屋；守住位置意味着"失去犯错的资格"，利润自然增长。
  sources: [f10, p04, p05, p38, g13, ce05, ce19, ce22]
  V1_cross_domain: {passed: true, note: "第六章·风险防范 + 第七章·资金管理（分散≠风控）+ 第二章多个反例"}
  V2_predictive_power: {passed: true, note: "新场景：用户问'我是不是该再多配几个防守手段'→回答不需要，检查这两点是否做到"}
  V3_exclusivity: {passed: true, why_not_common: "直接否定'分散=避险''买好公司=避险'这两条最主流的常识"}
  card_type: principle
  priority: P0

- id: SK-core-03
  title: 亏损五境界——用亏损观自诊交易层次
  type: framework
  source_chapter: 第六章 系统之路 · 亏损与境界
  source_quote: "从一位交易者对亏损的认识境界，就完全能够看出他的交易境界。"
  intent: 把"对待亏损的态度"做成可诊断的五层阶梯：拒绝面对→规避→承认合理→盈亏同源→得失随缘。
  application: 让用户定位自己所处层级；最高层的标志是"感激连续小亏损，正是它们把更聪明的人挡在门外"。
  sources: [f17, p06, g14, ce07, ce21]
  V1_cross_domain: {passed: true, note: "第六章诊断 + 第二章鸵鸟/学习效应作为低层失败证据"}
  V2_predictive_power: {passed: true, note: "新场景：用户连续止损后想改系统→先诊断其境界层级，第①层不能谈系统优化"}
  V3_exclusivity: {passed: true, why_not_common: "常识只有'亏了=不好'一种态度；唯一把亏损观做成五层可执行阶梯的作者"}
  card_type: framework(诊断类)
  priority: P0

- id: SK-core-04
  title: 昆虫系统——分散+趋势跟踪+等额+赢冲输缩 的可复刻配方
  type: principle
  source_chapter: 第六章 系统之路 · 昆虫系统
  source_quote: "对于趋势跟踪者而言，我们不怕上涨也不怕下跌，甚至我们连整理都不怕。"
  intent: 作者唯一给出的**完整、可直接复刻**的系统模板（在期货上验证）。
  application: 跨品种充分分散 + 均等资金额度 + 趋势跟踪 + 赢冲输缩；用于让用户有落地范例而非只讲抽象原则。
  sources: [p14, g08, ce16]
  V1_cross_domain: {passed: true, note: "第六章昆虫系统 + 第七章资金管理（等额/分散）+ 第二章恐龙效应（为何是昆虫不是恐龙）"}
  V2_predictive_power: {passed: true, note: "新场景：A股单边+T+0受限环境下如何裁剪→保留分散/等额/仓位，去掉多空双向"}
  V3_exclusivity: {passed: true, why_not_common: "明确的四要素配方，非'建立你自己的系统'这类空话"}
  card_type: principle（配方类）
  priority: P1
  ⚠️A股适配: 原配方在期货验证；A股需裁剪（不能双向、T+1谢绝日内）

- id: SK-core-05
  title: 分散是资金减震器，不是风险防范
  type: framework
  source_chapter: 第七章 资金管理 · 系统与资金
  source_quote: "分散投资是一种资金管理工具，而不是一种风险防范工具。"
  intent: 分散只平滑资金曲线波动、帮人承受长横盘，不提高期望收益、不补救错误方法。
  application: 与 SK-core-02 的 B 段呼应：若方法是错的，分散十个也错。
  sources: [f19, g19, ce05]
  V1_cross_domain: {passed: true, note: "第七章资金管理 + 第六章风险防范（明确切割）+ 第二章"}
  V2_predictive_power: {passed: true, note: "新场景：用户想靠多持股'分散风险'→区分他要的是降波动还是提收益"}
  V3_exclusivity: {passed: true, why_not_common: "与'分散=分散风险'这一几乎全民常识直接对冲"}
  card_type: framework
  priority: P1

- id: SK-core-06
  title: 优化与组合陷阱——过度优化与叠加方法会互损
  type: principle
  source_chapter: 第六章 系统之路 · 优化与组合
  source_quote: "环境是变化的，而越能适应过去环境的方法，就越不可能适应变化以后的环境。"
  intent: 因"等效性"，没有更优参数、只有更早固定的家；加过滤器、组合多策略=叠加全部劣势。
  application: 任何"帮你调参/加筛选条件/多策略组合"的建议，先过此条反向检验。
  sources: [f11, p12, g17, ce04, ce14, ce15, ce26, f20, p36]
  V1_cross_domain: {passed: true, note: "第六章·优化与组合 + 第二章·小蝴蝶/损耗/超级掠食者 + 第七章"}
  V2_predictive_power: {passed: true, note: "新场景：用户想给系统加'大盘环境过滤'→推演：过滤器滤掉的正是能大赚的那几次"}
  V3_exclusivity: {passed: true, why_not_common: "常识认为多策略组合更稳健；作者给出'叠加=优势与劣势同时叠加'的具体机制"}
  card_type: principle
  priority: P0
  注: f20 二八法则（20%努力→80%销量，剩余20%需再付80%）因其边际递减论证与此同源，已并入本条作 source。

- id: SK-core-07
  title: 不必追求正确率与赔率"双高"
  type: principle
  source_chapter: 第六章 系统之路 · 优化与组合
  source_quote: "双高系统是指，正确率大于50％，与此同时赔率大于1。"
  intent: 正确率与赔率互损；低正确率+大赔率的趋势系统即可稳定获利。
  application: 用户抱怨"胜率太低"时纠正指标设置：散户胜率高恰是"小赚就跑、大亏死扛"的本能所致。
  sources: [p13, g07, ce26]
  V1_cross_domain: {passed: true, note: "第六章·优化与组合 + 第二章·超市原理（高正确率是亏损根源）"}
  V2_predictive_power: {passed: true, note: "新场景：比较两个系统哪个'更好'→回到期望值与用户资金属性，而非胜率"}
  V3_exclusivity: {passed: true, why_not_common: "'把胜率做上去'是绝大多数交易者的默认目标"}
  card_type: principle
  priority: P1

- id: SK-core-08
  title: 永不非信号开仓
  type: principle
  source_chapter: 第六章 系统之路 · 昆虫系统
  source_quote: "如果我的每次开仓都对应一个信号的话，那么我的潜在亏损也必然符合跟踪系统的亏损分布。"
  intent: 每笔开仓必须对应系统信号，使潜在亏损落入系统既定的亏损分布，杜绝主观随手进场。
  application: 无信号不开仓；这是把"顺手追一笔"挡在系统外的具体闸门。
  sources: [p34]
  V1_cross_domain: {passed: true, note: "第六章昆虫系统 + 第六章一致性（机械执行）"}
  V2_predictive_power: {passed: true, note: "新场景：盘中临时起意加仓→判定为破坏亏损分布，须禁止"}
  V3_exclusivity: {passed: true, why_not_common: "把'必须有信号'上升到'保证亏损可统计'的因果论证，非泛泛纪律口号"}
  card_type: principle
  priority: P1
  注: 本条由 team-lead 补验证（三路 worker 均未覆盖），理由是它是"一致性"唯一可执行的落地闸门。

- id: SK-core-09
  title: 良好的入场价位是保住位置的基石
  type: principle
  source_chapter: 第六章 系统之路 · 昆虫系统
  source_quote: "如果你没有一个良好的入场价位，那么你会更容易丢掉趋势中的位置。"
  intent: 成本优势=心理优势=更能忍受正常回撤=更可能"永不丢掉位置"。
  application: 优先在信号点附近建仓，不追最高趋势感；入场价与趋势强度互损。
  sources: [p37]
  V1_cross_domain: {passed: true, note: "第六章昆虫系统 + 第六章风险防范（不丢位置）"}
  V2_predictive_power: {passed: true, note: "新场景：追高后被震出 vs 信号位进场→推演后者能撑过回撤"}
  V3_exclusivity: {passed: true, why_not_common: "把'入场价位'与'能否守住趋势'建立因果链，非常规的成本摊薄说辞"}
  card_type: principle
  priority: P2
  注: team-lead 补验证。

- id: SK-core-10
  title: 趋势跟踪者怕"恰到好处"的整理
  type: framework
  source_chapter: 第六章 系统之路 · 昆虫系统
  source_quote: "我们怕的就是那种'恰到好处'的整理！"
  intent: 小整理被包容、大整理能兑现利润，最伤的是幅度"刚好"触发止损又不构成反转的整理。
  application: 接受系统会被反复磨损，不因此改参数或弃系统；用分散与等额平滑。
  sources: [p39]
  V1_cross_domain: {passed: true, note: "第六章昆虫系统 + 第二章损耗原理"}
  V2_predictive_power: {passed: true, note: "新场景：连续被'擦损'出局→判定为系统固有损耗，非系统失效"}
  V3_exclusivity: {passed: true, why_not_common: "识别出'恰到好处'这个特定失效区，而非笼统'震荡市不适合'"}
  card_type: framework
  priority: P1
  注: team-lead 补验证。

- id: SK-core-11
  title: 江恩警示——不要陷入时间周期怪圈
  type: counter-example
  source_chapter: 第四章 技术分析
  source_quote: "但我绝对不相信，江恩理论能够将价格与时间分离而进行单独预测！"
  intent: 价格与时间不可分离预测；时间周期多是事后合理的幻觉。
  application: 阻止用户"数日子、套周期"当预测依据；作为技术分析批判的具体抓手。
  sources: [p35]
  V1_cross_domain: {passed: true, note: "第四章技术分析 + 第二章树形原理（事后合理≠事先可知）"}
  V2_predictive_power: {passed: true, note: "新场景：用户拿'XXX日是变盘时间窗'来问→用此条判定为分离预测谬误"}
  V3_exclusivity: {passed: true, why_not_common: "点名否定具体权威流派的可验证主张，不是泛泛的'技术无用论'"}
  card_type: counter-example
  priority: P2
  注: team-lead 补验证。

---

## B 组：第二章 24 个命名原理（17 个通过）

- id: SK-p24-01
  title: 冰山原理——承认无知
  type: framework
  source_chapter: 第二章 概念解释 · 冰山原理
  source_quote: "我们永远不可能认识事物的全貌……我们由于对事物不完全认识而形成的信念，也只不过是一种幻觉。"
  intent: 任何分析都只是冰山一角、断章取义；放弃"预测全貌"的幻觉。
  sources: [p21, f23]
  V1_cross_domain: {passed: true, note: "第二章定义 + 第三章基本分析批判 + 第六章（多处以'承认无知'支撑系统应对）"}
  V2_predictive_power: {passed: true, note: "新场景：用户给一份'完美归因复盘'→判定为冰山一角的事后合理化"}
  V3_exclusivity: {passed: true, why_not_common: "把'片面认知'直接定性为幻觉，而非常规的'要全面客观'"}
  card_type: framework
  priority: P1

- id: SK-p24-02
  title: 树形原理——事后合理 ≠ 事先可知
  type: framework
  source_chapter: 第二章 概念解释 · 树形原理
  source_quote: "当你将一个球抛向墙壁时，通常球会被弹回来。但如果你能尝试足够次数的话，小球总会有一两次能够穿过墙壁上的洞。"
  intent: 未来有无数分支，单一结果事后看似必然、事先不可知。
  sources: [p22, f24]
  V1_cross_domain: {passed: true, note: "第二章 + 第四章（江恩/时间周期批判）+ 第六章"}
  V2_predictive_power: {passed: true, note: "新场景：复盘把幸存路径当可复制规律→判定为树形谬误"}
  V3_exclusivity: {passed: true, why_not_common: "以'球穿墙'的概率机制区分事前/事后，非泛泛的'结果不可逆推'"}
  card_type: framework
  priority: P0

- id: SK-p24-03
  title: 巨变效应——原因是渐进的、结果是跳跃的
  type: framework
  source_chapter: 第二章 概念解释 · 巨变效应
  source_quote: "原因是渐进的、结果是跳跃的。"
  intent: 上涨本身在聚集下跌力量（负反馈+封存效应）；临界状态下小事件引发瞬间巨变。
  application: 常态被深信不疑时，通常巨变就开始；要能在两个极端的短暂转换中存活，而非预测它。
  sources: [f25, ce(跨越共制)]
  V1_cross_domain: {passed: true, note: "第二章巨变效应 + 第30–31页市场热点轮回实证（1995/1996/1997/2001各年代风格巨变）+ 第四章"}
  V2_predictive_power: {passed: true, note: "新场景：市场风格长期单向持续，问要不要换策略→答案是先确保能承受跳跃式结果"}
  V3_exclusivity: {passed: true, why_not_common: "'原因是渐进的、结果是跳跃的'是本会非线性世界观的核心，配合'赌/Swatch'逻辑"}
  card_type: framework
  priority: P1
  注: 原件 frameworks.md 丢失，本条已回原文（source.txt 行 768–778, 801–804, 991）重极。

- id: SK-p24-04
  title: 恐龙效应——光环与陨落同源
  type: framework
  source_chapter: 第二章 概念解释 · 恐龙效应
  source_quote: "交易者戴上光环与走向陨落，从本质上来说其实是同源的。"
  intent: 让人封神的成功模式，往往正是其未来崩塌的根源（过度适应环境）。
  sources: [p24, f26]
  V1_cross_domain: {passed: true, note: "第二章 + 第一章（大师结局：格雷厄姆/威尔德/利物默）+ 第六章"}
  V2_predictive_power: {passed: true, note: "新场景：某策略近两年大赚→警示其适应了特定环境，环境一变即陨落"}
  V3_exclusivity: {passed: true, why_not_common: "'昆虫活下来、恐龙灭绝'的对比式论证，全套很具体"}
  card_type: framework
  priority: P1

- id: SK-p24-05
  title: 钟摆效应——市场真理成对出现
  type: framework
  source_chapter: 第二章 概念解释 · 钟摆效应
  source_quote: "市场并不存在为单次交易负责的单向真理，市场上的真理在概念上都是成对出现的。"
  intent: 多空两套道理常同时成立；拒绝"这次不一样"的单向叙事。
  sources: [p23, f27]
  V1_cross_domain: {passed: true, note: "第二章 + 第三章/第四章（成对出现的基本面与技术面结论）+ 第六章"}
  V2_predictive_power: {passed: true, note: "新场景：用户辩称'这次逻辑不一样'→判定为单向真理执念"}
  V3_exclusivity: {passed: true, why_not_common: "断言'不存在为单次交易负责的真理'，直接否定单笔归因"}
  card_type: framework
  priority: P2

- id: SK-p24-06
  title: 学习效应（狗咬尾巴）
  type: framework
  source_chapter: 第二章 概念解释 · 学习效应
  source_quote: "市场的报表会先制造微观定势、再打破它，把追随定势者一网打尽。"（释义，原文见 g09）
  intent: 用近期成败反复切换方法=原地转圈；近期成败是微观随机，据此调整永远慢市场半拍。
  sources: [g09, f30, ce03]
  V1_cross_domain: {passed: true, note: "第二章学习效应 + 第二章对错悖论（明确说'这种对错观的直接产物就是我们后面要谈的学习效应'）+ 第六章一致性"}
  V2_predictive_power: {passed: true, note: "新场景：用户三个月改了三种方法→判定为狗咬尾巴，要求先固定一套跑满样本"}
  V3_exclusivity: {passed: true, why_not_common: "把'学习/总结经验'这个正面行为定性为负级现象"}
  card_type: framework
  priority: P0

- id: SK-p24-07
  title: 鸵鸟现象——面对而非逃避亏损
  type: framework
  source_chapter: 第二章 概念解释 · 鸵鸟现象
  source_quote: "当你明白'盈亏同源'后，你就知道亏损本身就是最好的风险释放过程，这时你会爱上你的亏损。"
  intent: 把头埋沙里逃避亏损只会让亏损长大；亏损是风险释放，越早释放越保护本金。
  sources: [p27, f33]
  V1_cross_domain: {passed: true, note: "第二章 + 第六章亏损与境界 + 第一章作者自述（两次虚假业绩、19岁亏掉父母积蓄过半）"}
  V2_predictive_power: {passed: true, note: "新场景：用户套牢后不敢看账户→判定鸵鸟行为，要求主动支付成本"}
  V3_exclusivity: {passed: true, why_not_common: "'亏损是最好的风险释放''爱上亏损'的表述极端反直觉"}
  card_type: framework
  priority: P1

- id: SK-p24-08
  title: 圆木桶理论——补齐系统最短的板
  type: framework
  source_chapter: 第二章 概念解释 · 圆木桶理论
  source_quote: "对于一笔获利的交易而言，你必须把各个环节都做正确；但对于一笔亏损的交易而言，并不需要把每个环节都做错。"
  intent: 盈利取决于最薄弱环节；优化应针对短板而非给强项锦上添花。
  sources: [p28, f34]
  V1_cross_domain: {passed: true, note: "第二章 + 第六章系统之路（多环节：入场/持仓/止损/仓位）+ 第四章"}
  V2_predictive_power: {passed: true, note: "新场景：用户系统不赚钱→先找唯一最短板（常是执行或资金），而非调参"}
  V3_exclusivity: {passed: true, why_not_common: "给赢/亏的不对称条件（赢要全对、亏只需一错），把木桶比喻落到交易上"}
  card_type: framework
  priority: P1

- id: SK-p24-09
  title: 点球原理——信息越少越易获利
  type: framework
  source_chapter: 第二章 概念解释 · 点球原理
  source_quote: "你需要知道的事情越少，获利就会越容易一些。"
  intent: 过度信息制造噪声与干扰，简化决策反而提升执行。
  sources: [p29, f35, ce(点球/确认后捕捉趋势 c16)]
  V1_cross_domain: {passed: true, note: "第二章 + 第六章（ treatise 越多/越复杂的约束越难自控）+ 第一章作者自述"}
  V2_predictive_power: {passed: true, note: "新场景：用户沉迷多指标共振→建议减到最少必要信号"}
  V3_exclusivity: {passed: true, why_not_common: "'知道得越少越赚钱'与'信息越多决策越优'的直觉完全相反"}
  card_type: framework
  priority: P1

- id: SK-p24-10
  title: 焦虑原理——接受确定性不存在
  type: framework
  source_chapter: 第二章 概念解释 · 焦虑原理
  source_quote: "事实上，确定性是不存在的。"
  intent: 焦虑源于对确定性的执念；停止向市场索要确定性，改以概率与规则应对。
  sources: [p32, f40]
  V1_cross_domain: {passed: true, note: "第二章焦虑原理 + 第六章再见确定性 + 第一章（对确定性追求的破灭）"}
  V2_predictive_power: {passed: true, note: "新场景：用户因不确定而反复询价求证→诊断为向市场索要确定性"}
  V3_exclusivity: {passed: true, why_not_common: "把焦虑归因到'确定性需求'，而非泛泛的心理调节"}
  card_type: framework
  priority: P1

- id: SK-p24-11
  title: 赌场原理——微观不确定 / 宏观确定
  type: framework
  source_chapter: 第二章 概念解释 · 赌场原理
  source_quote: "对于赌场而言，赌博的结果具有微观不确定性，以及宏观确定性。"
  intent: 单笔不可知，足够多样本后可由概率精确计算；靠"次数足够多"实现长期必然盈利。
  sources: [p20, f41, g05, f21(微宏互换并入)]
  V1_cross_domain: {passed: true, note: "第二章赌场原理 + 第六章赌博（作者定义）+ 第六章一致性（大数前提）+ 第七章"}
  V2_predictive_power: {passed: true, note: "新场景：用户凭 5 笔交易否定系统→判定为用微观样本评价宏观系统"}
  V3_exclusivity: {passed: true, why_not_common: "微/宏两层确定性切分，给出'为什么可以明知单笔亏损仍下单'的数理依据"}
  card_type: framework
  priority: P0

- id: SK-p24-12
  title: 损耗原理——包容连续小亏损
  type: framework
  source_chapter: 第二章 概念解释 · 损耗原理
  source_quote: "趋势跟踪系统产生的大赔率在嘲笑众多小亏损的同时，也在嘲笑其他的分析方法以及我的思考。"
  intent: 趋势系统的利润来自偶发大赔率，本就伴随大量小亏损"损耗"；不要用主观思考去优化掉它们。
  sources: [p30, f37]
  V1_cross_domain: {passed: true, note: "第二章损耗原理 + 第六章昆虫系统（连续小亏后才出大利润）+ SK-core-10 恰到好处的整理"}
  V2_predictive_power: {passed: true, note: "新场景：连亏后想加过滤器减少亏损→推演会砍掉大赔率"}
  V3_exclusivity: {passed: true, why_not_common: "'大赔率在嘲笑我的思考'——明确否定用思考改善损耗"}
  card_type: framework
  priority: P1

- id: SK-p24-13
  title: 小蝴蝶效应——少则得，多则惑
  type: framework
  source_chapter: 第二章 概念解释 · 小蝴蝶的故事
  source_quote: "如果你吸取了所有的颜色，结果只能是什么颜色都没有的黑色！"
  intent: 叠加交易方法时，优势与劣势同时叠加；想要所有方法优势的人最终什么都得不到。
  sources: [f36]
  V1_cross_domain: {passed: true, note: "第二章小蝴蝶 + 第六章优化与组合（明确引用'圆木桶理论''小蝴蝶的故事'）+ 第四章"}
  V2_predictive_power: {passed: true, note: "新场景：用户想同时使用多种系统滤选→推演为叠加劣势变黑"}
  V3_exclusivity: {passed: true, why_not_common: "用'要所有颜色→变黑'的寓言说明取舍，反直觉且记忆锚点强"}
  card_type: framework
  priority: P2
  注: 原件 frameworks.md 丢失，本条已回原文（source.txt 行 1275–1297）重极。

- id: SK-p24-14
  title: 等效性原则——敏感与迟钝、正确率与赔率互损
  type: framework
  source_chapter: 第二章 概念解释 / 第六章 一致性
  source_quote: "跟踪系统中参数的敏感与迟钝是等效的；而'策略与技术''正确率与赔率'……又是互损的。"
  intent: 否定了"更敏感参数更好""技术越高级越好"的常识；没有免费午餐，只有取舍。
  sources: [p33, f06, g06, f22(因果倒置并入)]
  V1_cross_domain: {passed: true, note: "第二章 + 第六章一致性 + 第六章优化与组合（g17 引用此作为论证核心）+ 第七章"}
  V2_predictive_power: {passed: true, note: "新场景：用户纠结参数选 5 日还是 20 日→回答大样本等效，选定即可"}
  V3_exclusivity: {passed: true, why_not_common: "给出'两端数学等效'的具体机制，是全书反优化论证的地基"}
  card_type: framework
  priority: P0

- id: SK-p24-15
  title: 超市原理——高正确率是亏损根源
  type: framework
  source_chapter: 第二章 概念解释 · 超市原理
  source_quote: "在我看来，股民们大面积亏损的一个最为主要的原因就是正确率太高了！"
  intent: 散户高胜率源自"利润兑现、亏损挂起"的本能，利润被多次平分、亏损由少数次承担。
  sources: [p25, f31]
  V1_cross_domain: {passed: true, note: "第二章超市原理 + 第六章（$双高/正确率讨论）+ SK-core-07"}
  V2_predictive_power: {passed: true, note: "新场景：用户炫耀 80% 胜率却亏损→直接判定超市原理"}
  V3_exclusivity: {passed: true, why_not_common: "'正确率太高是亏损主因'是最具冲击力的反直觉断言"}
  card_type: framework
  priority: P0

- id: SK-p24-16
  title: 对错悖论——对错的评价应基于原因而非结果
  type: framework
  source_chapter: 第二章 概念解释 · 对错悖论
  source_quote: "对错的评价不应该是基于结果，而应该是基于原因。"
  intent: 用结果评价方法会导致"任何方法都好也都坏"，随即滑入学习效应的狗咬尾巴怪圈。
  sources: [f29]
  V1_cross_domain: {passed: true, note: "第二章对错悖论明确导出'学习效应'（第二章）+ 第六章亏损五境界（不用结果评价）+ 第一章作者三次超越系统的自承错误"}
  V2_predictive_power: {passed: true, note: "新场景：用户问'这笔止损了是不是做错了'→判为用结果评价；只要合乎系统就该*} 
  V3_exclusivity: {passed: true, why_not_common: "明确把'对错'锚定到策略而非结果，并指出这是学习效应的直接产因"}
  card_type: framework
  priority: P0
  注: 原件 frameworks.md 丢失，本条已回原文（source.txt 行 962–990）重极。

- id: SK-p24-17
  title: 复利悖论——稳定性优于速度
  type: framework
  source_chapter: 第二章 概念解释 · 复利悖论
  source_quote: "无论你承认与否，交易者追求的很多东西是永远也无法真正得到的。"
  intent: 追求快速暴利常破坏稳定性；把资金曲线的稳定性放在增长速度之前。
  sources: [p26, f32]
  V1_cross_domain: {passed: true, note: "第二章复利悖论 + 第七章资金管理（资金曲线/仓位）+ 第六章"}
  V2_predictive_power: {passed: true, note: "新场景：用户想提高杠杆加速→推演稳定性下降后长期复利更差"}
  V3_exclusivity: {passed: true, why_not_common: "指出'稳定性与速度不可兼得'必须做取舍，而非泛泛'慢慢变富'"}
  card_type: framework
  priority: P2

---

## C 组：残差框架（1 个）

- id: SK-misc-01
  title: 外化而内不化——弹性的方向必须靠刚性的规则实现
  type: framework
  source_chapter: 第二章 概念解释
  source_quote: "弹性的方向与刚性的规则，很类似于庄子所说，外化而内不化（交易化而规则不化）。"
  intent: 看似矛盾的组合：对外（行情/方向）完全灵活，对内（规则/基石）绝对不变。Macro 上的高抛低吸必须靠 micro 上的追涨杀跌实现。
  sources: [f16]
  V1_cross_domain: {passed: true, note: "第二章（外化而内不化）+ source.txt 行 1760–1764（黄豆走势图：中期趋势跟踪系统在大尺度上实现高抛低吸）+ 第六章一致性"}
  V2_predictive_power: {passed: true, note: "新场景：用户想'既灵活又守纪律'的缝合法→指出刚性体现在规则而非方向"}
  V3_exclusivity: {passed: true, why_not_common: "给出'弹性≒刚性'这一表面上矛盾的统一机制，并用黄豆图实证"}
  card_type: framework
  priority: P1
  注: 本条在每个 worker 范围边缘，team-lead 回原文（source.txt 行 1757–1765）确认后纳入。

---

## D 组：支撑材料（验证通过，不单列为 skill，供各卡片的 R/I/A1/A2/B 段引用）

cases（25 条，全部通过）：c01–c25
  作者亲身 12 条：c01 19岁亏父母积蓄过半 / c02 1997大庆联谊自欺 / c03 2000达尔曼虚假业绩 /
    c04 1999西安民生错失7涨停 / c05 三次"超越"系统丢数千万 / c06 2006期货两月17万→60万 /
    c12 期货内勤内幕 / c13 十年大计对话 / c14 鸵鸟两次虚假业绩 / c16 点球捕捉趋势需确认 /
    c19 三次无效止损父母压力 / c22 曾买绩差上涨股 / c23 手机店试验
  转述历史 13 条：c07 格雷厄姆转效率市场 / c08 威尔德弃指标 / c09 利物默三度破产自杀 /
    c10 江恩完美预测却穷困 / c11 艾略特道氏无获利记载 / c15 期货看对却因资金管理输钱 /
    c17 2005论坛 / c18 2000牛市三次跳水狼来了 / c20 香港人巴菲特 / c21 反缺口1996·630 /
    c24 房产中介高价参照 / c25 朋友房贷超级掠食者

glossary（19 条，全部通过）：g01–g19
  ⭐ 关键术语（下游极易误用）：g01 盈亏同源 / g02 成本观念 / g03 趋势跟踪系统（低正确率+大赔率是特征非缺陷）/
    g05 微观宏观确定性 / g06 等效性 / g07 双高系统 / g08 昆虫系统 / g09 学习效应 / g10 赌博（理性赌博）/
    g11 套利原理 / g13 风险防范两点 / g14 亏损五境界 / g16 预测≠交易成环 / g18 价值投资≠占便宜 / g19 分散=减震器

counter-examples（28 条，全部通过）：ce01–ce28
  ⭐ 作者第一人称自承错误（最适合做 B 段锚点）：ce03（随近期成败切换方法）/ ce06（曾迷信江恩波浪、看对行情卖在
    地板价）/ ce27（三次"超越"系统丢掉数千万：2001忽略卖出信号亏50%、2003赌气追求确定性亏50%、2006放弃买入信号）
  ⭐ 其余高频反例：ce01 确定性幻觉 / ce02 高正确率陷阱 / ce04 过度优化与组合 / ce05 把分散当风控 /
    ce07 把亏损当敌人 / ce08 高低错觉 / ce09 依赖他人 / ce11 恐龙效应 / ce12 焦虑弃系统 /
    ce13 圆木桶系统过复杂 / ce14 小蝴蝶叠方法 / ce15 损耗效应 / ce17 等看出趋势再动 / ce19 怕隔夜→日内重仓 /
    ce21 用结果评价对错 / ce22 传统风控三误区 / ce23 大师迷信 / ce24 抄底逃顶 / ce26 双高执念 / ce28 形态成交量误区

---

## 边界项（team-lead 判定为可捞回 / 需你裁决）

以下 4 项worker 判为 FAIL V3，但 team-lead 认为"内核是常识、作者有独特机制或修辞"，是否捞回请决定：
1. f09/p07 预测≠交易·必须成环 —— 常识版"想法≠执行"是常见，但"点状/环状"的对举+gis)"我能回答此刻买/持/卖"的判别式很可执行。建议捞回为 A（应用）段。
2. f07/p08 道重于术 —— 理念>技术是常识，但作者给出"求道者舍钱而终得道"的具体取舍路径。建议不单列，作为一切 skill 的元立场引用。
3. f12/p10 开发系统必须个性化 —— "要个性化"是常识，但"开发的终点是接受自身能承受的缺陷"这个反转很有价值。建议捞回为 system-development 卡片的 A2 段。
4. p15–p19 赌博五原则 —— worker 判为"理性博彩通用建议"。其中 **p18 赢冲输缩** 与 **p15 输不起不赌** 交易针对性最强，建议捞回并入 SK-core-04 昆虫系统（赢冲输缩已是其内嵌元素）；p16/p19 偏通用心态，建议不单列。
