# -*- coding: utf-8 -*-
"""生成 22 个 router-served 能力：22 张卡片 + 追加进 verified.yaml + 重算 destinations.json。
所有 source_quote 已逐一核验存在于 source.txt。所有 YAML 字符串标量双引号包裹，避免内嵌引号/逗号破 YAML。"""
import os, json, re

BASE = "E:/Work Buddy/交易学习/books/032-zouchuhuanjue"
CAP_DIR = os.path.join(BASE, ".cangjie/capabilities")
CARD_DIR = os.path.join(CAP_DIR, "cards")

ROUTER = "zouchuhuanjue"  # 来源路由入口名（与 entry.name / router_entry.name 一致）

def q(s):
    """YAML 双引号标量：转义双引号与反斜杠。"""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'

def flow(lst):
    return "[" + ", ".join(q(x) for x in lst) + "]"

# (id, slug, title, imp, rationale, oneliner, intents, kws, loc, quote, intent, app, boundary, tags)
E = [
("cap.032.never-open-without-signal","never-open-without-signal","永不非信号开仓——每笔都对应系统信号","high",
 "一致性最可执行的落地闸门；第六章昆虫系统核心纪律，使潜在亏损落入系统既定分布，杜绝随手进场。",
 "每笔开仓必须对应一个系统信号，使潜在亏损符合系统的亏损分布；无信号不开仓。",
 ["盘中临时起意想加一笔","怎么管住自己不随手追","为什么必须等信号","no signal no entry discipline"],
 ["非信号开仓","随手进场","信号","一致性","纪律"],
 "第六章 系统之路 · 昆虫系统",
 "永不非信号开仓！如果我的每次开仓都对应一个信号的话，那么我的潜在亏损也必然符合跟踪系统的亏损分布。",
 "随手开仓会让亏损脱离系统可统计的分布，等于在系统外偷偷下注，长期必然侵蚀期望值。",
 "只有每笔都对应信号，系统的亏损率与赔率才成立；把顺手追一笔挡在系统外。",
 "A股同样适用；与 insect-system-recipe（机械执行）、loss-maturity-ladder（第①层先别谈系统）衔接。",
 ["discipline","signal-only","consistency"]),

("cap.032.good-entry-price","good-entry-price","良好的入场价位保住趋势位置","low",
 "成本是心理优势的源头；入场价与能否守住趋势直接因果，常被误读为单纯摊薄成本。",
 "没有良好的入场价位就更容易丢掉趋势中的位置；优先在信号点附近建仓，不追最高趋势感。",
 ["追高后被震出","一进场就套怎么办","入场价重不重要","entry price position holding"],
 ["入场价位","成本优势","追高","守位置"],
 "第六章 系统之路 · 昆虫系统",
 "如果你没有一个良好的入场价位，那么你会更容易丢掉趋势中的位置。",
 "成本优势=心理优势=更能忍受正常回撤=更可能永不丢掉位置；入场价与趋势强度互损。",
 "优先在信号点附近建仓而非追高；入场价差是系统能否扛过回撤的隐形杠杆。",
 "与 risk-guard-two-points（不丢位置）、insect-system-recipe 衔接；属 P2 引用级。",
 ["entry-price","cost-advantage","trend-position"]),

("cap.032.just-right-consolidation","just-right-consolidation","趋势跟踪者怕恰到好处的整理","medium",
 "识别出特定失效区（幅度刚好触发止损又不构成反转），而非笼统震荡市不适合，是系统韧性的关键认知。",
 "小整理被包容、大整理能兑现利润，最伤的是幅度刚好触发止损又不构成反转的整理。",
 ["连续被擦损出局是不是系统失效","震荡市是不是该停系统","为什么总在整理里亏","consolidation whipsaw"],
 ["恰到好处的整理","擦损","损耗","回撤"],
 "第六章 系统之路 · 昆虫系统",
 "大的整理能够让我们获利，小的整理能够被我们包容，我们怕的是那种不大不小、恰到好处的整理。",
 "系统会被反复恰到好处的整理磨损，这是趋势跟踪的结构性成本，不是系统失效。",
 "接受磨损、不因此改参数或弃系统；用分散与等额平滑这段必经之路。",
 "与 avoid-over-optimization（优化陷阱）、just-right-consolidation 同源；属 router 引用级。",
 ["consolidation","whipsaw","system-resilience"]),

("cap.032.gann-warning","gann-warning","江恩警示——勿陷时间周期怪圈","low",
 "点名否定具体权威流派的可验证主张（价格与时间不可分离预测），是技术分析批判的具体抓手。",
 "价格与时间不可分离预测；时间周期多是事后合理的幻觉，勿数日子套周期当预测依据。",
 ["某日是变盘时间窗可信吗","江恩时间周期怎么看","数浪数日子准不准","gann time cycle technical analysis"],
 ["江恩","时间周期","分离预测","技术分析"],
 "第四章 技术分析",
 "但我绝对不相信，江恩理论能够将价格与时间分离而进行单独预测！",
 "价格与时间必须绑定；脱离价格单独数日子是树形原理（事后合理不等于事先可知）的翻版。",
 "阻止用户把时间窗当预测依据；作为技术分析批判与反预测的实体证据。",
 "与 tree-principle（树形原理）、全书的反预测元立场衔接；属 P2 引用级。",
 ["gann","time-cycle","technical-criticism"]),

("cap.032.iceberg","iceberg-principle","冰山原理——承认无知","medium",
 "把片面认知直接定性为幻觉，是全书非线性世界观的底座，撑起系统应对而非预测的立场。",
 "任何分析都只是冰山一角、断章取义；放弃预测全貌的幻觉，改用概率与规则应对。",
 ["复盘很完美是不是能复制","为什么分析总遗漏","怎么接受看不全","iceberg incomplete knowledge"],
 ["冰山","不完全认知","幻觉","无知"],
 "第二章 概念解释 · 冰山原理",
 "我们永远不可能认识事物的全貌，我们由于对事物不完全认识而形成的信念，也只不过是一种幻觉。",
 "我们看到的永远是冰山一角，据此形成的信念多是事后合理的幻觉。",
 "放弃预测全貌的执念；以系统应对替代精确预判，承认无知是纪律的起点。",
 "与 tree-principle（树形原理）、anxiety-principle 衔接；router 引用级。",
 ["iceberg","humility","incomplete-knowledge"]),

("cap.032.tree","tree-principle","树形原理——事后合理不等于事先可知","high",
 "以球穿墙的概率机制区分事前事后，是反预测论证的地基，跨章复用确凿。",
 "未来有无数分支，单一结果事后看似必然、事先不可知；勿把幸存路径当可复制规律。",
 ["复盘把幸存路径当规律","为什么历史总说得通","事后看都对事先呢","tree hindsight bias"],
 ["树形","事后合理","事先不可知","分支"],
 "第二章 概念解释 · 树形原理",
 "当你将一个球抛向墙壁时，通常球会被弹回来。但如果你能尝试足够次数的话，小球总会有一两次能够穿过墙壁上的洞。",
 "未来像树枝有无数分支，单一结果事后看必然、事先不可知。",
 "复盘把某条幸存路径当规律等于树形谬误；承认事先不可知，改用系统应对。",
 "与 iceberg-principle、anxiety-principle、反预测元立场衔接；高频引用。",
 ["tree","hindsight-bias","nonlinear"]),

("cap.032.huge-change","huge-change-effect","巨变效应——原因渐进、结果跳跃","medium",
 "原因渐进、结果跳跃的非线性世界观；常态被深信时巨变开始，要能存活于两极短暂转换而非预测它。",
 "上涨本身在聚集下跌力量（负反馈加封存效应）；临界态小事件引发瞬间巨变。",
 ["市场风格长期单向要不要换策略","为什么平静期突然崩","巨变怎么应对","regime shift nonlinear"],
 ["巨变","非线性","跳跃","临界"],
 "第二章 概念解释 · 巨变效应",
 "原因是渐进的、结果是跳跃的。",
 "上涨在聚集下跌力量，常态越被深信巨变越近；小事件在临界态引发瞬间跳跃。",
 "不预测巨变，而是确保自己能承受跳跃式结果、在两极短暂转换中存活。",
 "与 dinosaur-effect、pendulum-effect 衔接；router 引用级。",
 ["regime-shift","nonlinear","jump"]),

("cap.032.dinosaur","dinosaur-effect","恐龙效应——光环与陨落同源","medium",
 "昆虫活下来、恐龙灭绝的对比式论证具体；让人封神的成功模式常正是其崩塌根源（过度适应环境）。",
 "让人封神的成功模式，往往正是其未来崩塌的根源（过度适应特定环境）。",
 ["某策略近两年大赚是不是神","为什么好方法后来失效","过度适应市场","dinosaur overfit hubris"],
 ["恐龙","光环","陨落","过度适应"],
 "第二章 概念解释 · 恐龙效应",
 "交易者戴上光环与走向陨落，从本质上来说其实是同源的。",
 "适应得越好越依赖，环境一变即陨落；昆虫（简单、分散）比恐龙（庞大、专精）更活。",
 "对封神的方法保持警惕；环境变了，曾经的护城河就是坟场。",
 "与 insect-system-recipe（昆虫系统）、dinosaur-effect 同源；router 引用级。",
 ["dinosaur","overfitting","hubris"]),

("cap.032.pendulum","pendulum-effect","钟摆效应——市场真理成对出现","low",
 "断言不存在为单次交易负责的单向真理，直接否定单笔归因与这次不一样的单向叙事。",
 "多空两套道理常同时成立；拒绝这次不一样的单向真理执念。",
 ["这次逻辑不一样是不是新规律","多空说法都对","为什么没有单向真理","pendulum paired truth"],
 ["钟摆","成对真理","单向","矛盾"],
 "第二章 概念解释 · 钟摆效应",
 "市场并不存在为单次交易负责的单向真理，市场上的真理在概念上都是成对出现的。",
 "多空两套道理常同时成立；任何单向叙事都在忽略对面的真理。",
 "拒绝这次不一样；用成对真理约束自己的单笔归因冲动。",
 "与 right-wrong-paradox、tree-principle 衔接；router 引用级。",
 ["pendulum","paired-truth","narrative"]),

("cap.032.learning-effect","learning-effect","学习效应（狗咬尾巴）——近况定势误判","high",
 "把学习总结经验这个正面行为定性为负向现象；近期成败是微观随机，据此调整永远慢市场半拍。",
 "用近期成败反复切换方法等于原地转圈；近期成败是微观随机，据此调整永远慢市场半拍。",
 ["三个月改了三种方法","为什么越学越亏","最近不行要不要换","learning effect dog chasing tail"],
 ["学习效应","狗咬尾巴","近况","切换方法"],
 "第二章 概念解释 · 学习效应",
 "市场的机制就是制造微观定势，然后突然打破这种定势，将追随定势的交易者一网打尽。",
 "市场先制造微观定势再打破它；用近期成败切换方法等于原地转圈、永远慢半拍。",
 "识别后要求先固定一套跑满样本（如 30 笔以上），不以近况裁定方法生死。",
 "与 learning-effect-chasing-tail（晋级）、right-wrong-paradox 衔接；高频引用。",
 ["learning-effect","recency-bias","dog-chasing-tail"]),

("cap.032.ostrich","ostrich-phenomenon","鸵鸟现象——面对而非逃避亏损","medium",
 "亏损是最好的风险释放、爱上亏损极端反直觉；把头埋沙里只会让亏损长大。",
 "把头埋沙里逃避亏损只会让亏损长大；亏损是风险释放，越早释放越保护本金。",
 ["套牢后不敢看账户","亏损了想装没发生","怎么面对账面绿","ostrich face the loss"],
 ["鸵鸟","逃避","风险释放","包容亏损"],
 "第二章 概念解释 · 鸵鸟现象",
 "当你明白盈亏同源后，你就知道亏损本身就是最好的风险释放过程，这时你会爱上你的亏损。",
 "逃避亏损让亏损长大；亏损是风险释放过程，越早释放越保护本金。",
 "主动支付成本、包容亏损；与 loss-maturity-ladder 第①层（拒绝面对）对应。",
 "与 trading-loss-as-cost、loss-maturity-ladder 衔接；router 引用级。",
 ["ostrich","face-loss","risk-release"]),

("cap.032.barrel","barrel-theory","圆木桶理论——补齐最短板","medium",
 "给赢亏不对称条件（赢要全对、亏只需一错），把木桶比喻落到交易；优化应针对短板而非锦上添花。",
 "盈利取决于最薄弱环节；优化应针对最短板，而非给强项锦上添花。",
 ["系统不赚钱先改哪","是不是该调参","短板在哪","barrel weakest link"],
 ["圆木桶","短板","环节","盈利条件"],
 "第二章 概念解释 · 圆木桶理论",
 "对于一笔获利的交易而言，你必须把各个环节都做正确；但对于一笔亏损的交易而言，并不需要把每个环节都做错。",
 "盈利要求每个环节都对，亏损只需一个错；系统瓶颈在唯一最短板。",
 "系统不赚钱时先找最短板（常是执行或资金），而非调参加过滤器。",
 "与 avoid-over-optimization（优化陷阱）、insect-system-recipe 衔接；router 引用级。",
 ["barrel","weakest-link","bottleneck"]),

("cap.032.penalty","penalty-principle","点球原理——信息越少越易获利","medium",
 "知道得越少越赚钱与直觉完全相反；过度信息制造噪声，简化决策反而提升执行。",
 "过度信息制造噪声与干扰，简化决策反而提升执行；需要知道的越少获利越容易。",
 ["指标越多越好吗","多指标共振靠谱吗","怎么简化决策","penalty less is more"],
 ["点球","信息","简化","噪声"],
 "第二章 概念解释 · 点球原理",
 "你需要知道的事情越少，获利就会越容易一些。",
 "信息越多约束越多越难自控；少而必要的信号优于多指标共振。",
 "建议减到最少必要信号；与 equivalence-principle、avoid-over-optimization 同源。",
 "与 avoid-over-optimization、equivalence-principle 衔接；router 引用级。",
 ["penalty","simplicity","less-is-more"]),

("cap.032.anxiety","anxiety-principle","焦虑原理——接受确定性不存在","medium",
 "把焦虑归因到确定性需求而非泛泛心理调节；停止向市场索要确定性，改以概率与规则应对。",
 "焦虑源于对确定性的执念；停止向市场索要确定性，改以概率与规则应对。",
 ["不确定好焦虑怎么办","为什么越不确定越怕","总想求证涨跌","anxiety certainty need"],
 ["焦虑","确定性","追求","安宁"],
 "第二章 概念解释 · 焦虑原理",
 "人的一生总是在追逐确定性，认为只有得到确定性才能使自己感到安全。事实上，确定性是不可能追求得到的。",
 "焦虑来自向市场索要确定性；意识到确定性不存在，内心才得安宁。",
 "把对确定的需求当症状处理；用概率与规则替代对确定答案的执念。",
 "与 casino-principle、反预测元立场衔接；router 引用级。",
 ["anxiety","certainty","need-for-certainty"]),

("cap.032.casino","casino-principle","赌场原理——微观不确定、宏观确定","high",
 "微宏两层确定性切分，给出明知单笔亏损仍下单的数理依据；靠次数足够多实现长期必然盈利。",
 "单笔不可知，足够多样本后可由概率精确计算；靠次数足够多实现长期必然盈利。",
 ["凭 5 笔否定系统对不对","为什么敢明知会亏还下","大数定律怎么用","casino micro macro"],
 ["赌场","微观不确定","宏观确定","大数"],
 "第二章 概念解释 · 赌场原理",
 "对于赌场而言，赌博的结果具有微观不确定性，以及宏观确定性。",
 "单笔不可知，但足够多样本后收益可由概率精确计算；次数越多越接近理论值。",
 "用微观样本（几笔）评价宏观系统等于谬误；以次数足够多支撑长期必然盈利。",
 "与 trading-loss-as-cost（盈亏同源）、equivalence-principle 衔接；高频引用。",
 ["casino","micro-macro","law-of-large-numbers"]),

("cap.032.attrition","attrition-principle","损耗原理——包容连续小亏损","medium",
 "大赔率在嘲笑我的思考——明确否定用思考改善损耗；趋势利润来自偶发大赔率，本就伴大量小亏。",
 "趋势系统的利润来自偶发大赔率，本就伴随大量小亏损损耗；不要用主观思考去优化掉它们。",
 ["连亏后想加过滤器","小亏太多是不是方法错","怎么看待连续止损","attrition small losses"],
 ["损耗","连续小亏","包容","大赔率"],
 "第二章 概念解释 · 损耗原理",
 "趋势跟踪系统产生的大赔率在嘲笑众多小亏损的同时，也在嘲笑其他的分析方法以及我的思考。",
 "趋势利润来自偶发大赔率，本就伴大量小亏；用主观思考优化掉损耗等于砍掉大赔率。",
 "连亏时是系统正常呼吸，维持等额；不因此加过滤器。",
 "与 just-right-consolidation（恰到好处的整理）、avoid-over-optimization 衔接；router 引用级。",
 ["attrition","small-losses","trend-cost"]),

("cap.032.butterfly","butterfly-effect","小蝴蝶效应——少则得，多则惑","low",
 "用要所有颜色变黑的寓言说明取舍；叠加方法时优势与劣势同时叠加，想要全部优势的人最终什么都得不到。",
 "叠加交易方法时，优势与劣势同时叠加；想要所有方法优势的人最终什么都得不到。",
 ["能不能多策略组合","各种方法都加上行吗","为什么不能全都要","butterfly less is more"],
 ["小蝴蝶","叠加","取舍","黑色"],
 "第二章 概念解释 · 小蝴蝶的故事",
 "你可以选择赤橙黄绿青蓝紫中的任何一种颜色作为自己的交易方法。但如果你吸取了所有的颜色，结果只能是什么颜色都没有的黑色！",
 "每种方法取其一种颜色即可；吸取所有颜色等于叠加全部劣势，最终一无所获。",
 "选定一种方法并坚持，而非把多种系统组合以期全优。",
 "与 avoid-over-optimization（优化陷阱）、equivalence-principle 衔接；router 引用级。",
 ["butterfly","overlap-methods","trade-off"]),

("cap.032.equivalence","equivalence-principle","等效性原则——敏感与迟钝、正确率与赔率互损","high",
 "给出两端数学等效的具体机制，是全书反优化论证的地基；否定更敏感参数更好、技术越高级越好。",
 "参数的敏感与迟钝等效、正确率与赔率互损；没有免费午餐，只有取舍。",
 ["参数选 5 日还是 20 日","技术越高级越好吗","为什么没更优参数","equivalence tradeoff"],
 ["等效性","敏感迟钝","互损","取舍"],
 "第二章 概念解释 / 第六章 一致性",
 "跟踪系统中参数的敏感与迟钝是等效的，而策略与技术、正确率与赔率又是互损的。",
 "两端在大样本中等效；没有更优只有更早固定；正确率与赔率互损。",
 "参数两端等效，选定即可；拒绝更灵敏等于更好的常识。",
 "与 insect-system-recipe 双高、avoid-over-optimization 衔接；高频引用。",
 ["equivalence","tradeoff","interdependence"]),

("cap.032.supermarket","supermarket-principle","超市原理——高正确率是亏损根源","high",
 "正确率太高是亏损主因最具冲击力的反直觉断言；散户高胜率源自本能的利润兑现加亏损挂起。",
 "散户高胜率源自利润兑现、亏损挂起的自私本能，利润被多次平分、亏损由少数次承担。",
 ["我胜率 80% 却亏钱","为什么赚小亏大","高胜率好不好","supermarket win rate trap"],
 ["超市","高正确率","胜率","亏损根源"],
 "第二章 概念解释 · 超市原理",
 "在我看来，股民们大面积亏损的一个最为主要的原因就是正确率太高了！",
 "高胜率是小赚就跑、大亏死扛本能的产物；利润被多次平分，亏损集中承担。",
 "纠正把胜率做上去的本能目标；与 双高系统、赔率 衔接。",
 "与 high-winrate-trap（晋级）、insect-system-recipe 双高 衔接；高频引用。",
 ["supermarket","high-win-rate","win-rate-trap"]),

("cap.032.right-wrong","right-wrong-paradox","对错悖论——对错基于原因而非结果","high",
 "明确把对错锚定到策略而非结果，并指出这是学习效应的直接产因；用结果评价方法会滑入狗咬尾巴。",
 "用结果评价方法会导致任何方法都好也都坏，随即滑入学习效应的狗咬尾巴。",
 ["这笔止损了是不是做错了","亏了是不是方法不行","怎么判断操作对不对","right-wrong result vs cause"],
 ["对错悖论","结果","原因","评价"],
 "第二章 概念解释 · 对错悖论",
 "对错的评价不应该是基于结果，而应该是基于原因。",
 "用结果评价方法会使其既好又坏，进而滑入学习效应循环。",
 "只要合乎系统，亏损也是对；用原因（是否按系统）而非盈亏结果评价。",
 "与 loss-maturity-ladder（五境界）、learning-effect-chasing-tail 衔接；高频引用。",
 ["right-wrong","process-over-outcome","evaluation"]),

("cap.032.compound","compound-paradox","复利悖论——稳定性优于速度","low",
 "指出稳定性与速度不可兼得必须做取舍，而非泛泛慢慢变富；追求快速暴利常破坏稳定性。",
 "追求快速暴利常破坏稳定性；把资金曲线的稳定性放在增长速度之前。",
 ["能不能加杠杆加速","怎么平衡稳和快","暴利好不好","compound stability vs speed"],
 ["复利","稳定性","速度","取舍"],
 "第二章 概念解释 · 复利悖论",
 "无论你承认与否，交易者追求的很多东西是永远也无法真正得到的。",
 "追求快速暴利损害稳定性；长期复利更依赖稳定而非速度。",
 "把资金曲线稳定性置于增速之前；拒绝为速度牺牲稳定。",
 "与 good-entry-price 分散减震器、dinosaur-effect 衔接；router 引用级。",
 ["compound","stability","speed-tradeoff"]),

("cap.032.external-flex-internal-rigid","external-flex-internal-rigid","外化而内不化——弹性方向靠刚性规则","medium",
 "给出弹性等于刚性表面上矛盾的统一机制，并用黄豆图实证；宏观上的高抛低吸必须靠微观上的追涨杀跌实现。",
 "对外（行情方向）完全灵活，对内（规则基石）绝对不变；刚性体现在规则而非方向。",
 ["既灵活又守纪律怎么做","宏观和微观矛盾吗","规则与方向","external flex internal rigid"],
 ["外化内不化","弹性","刚性","规则"],
 "第二章 概念解释",
 "弹性的方向与刚性的规则，很类似于庄子所说，外化而内不化（交易化而规则不化）。",
 "看似矛盾：对外方向完全灵活、对内规则绝对不变；宏观高抛低吸靠微观追涨杀跌实现。",
 "要灵活的是方向，要刚性的是规则；别把规则也灵活化。",
 "与 insect-system-recipe（昆虫系统）、trading-loss-as-cost 衔接；router 引用级。",
 ["flexibility","rigidity","rule-vs-direction"]),
]

def card_md(e):
    cid,slug,title,imp,rat,one,intents,kws,loc,quote,intent,app,bound,tags = e
    ints = "\n".join("- " + x for x in intents)
    kw = "、".join(kws)
    tag = "[" + ", ".join(tags) + "]"
    return (
"<!-- capability_id: " + cid + " | revision: 1 | status: active -->\n"
"<!-- 来源: books/032-zouchuhuanjue/source.txt —《走出幻觉·走向成熟》金融帝国 -->\n\n"
"# " + title + "\n\n"
"## R — 原文\n"
"> " + quote + "\n"
"—— " + loc + "\n\n"
"## I — 自述\n"
+ intent + "\n\n" + app + "\n\n"
"## A — 何时触发\n"
+ ints + "\n"
"语言信号：" + kw + "\n\n"
"## B — 边界\n"
+ bound + "\n"
"（重要度：" + imp + "；经来源路由入口可达，不单独晋级。）\n"
    )

def cap_yaml(e):
    cid,slug,title,imp,rat,one,intents,kws,loc,quote,intent,app,bound,tags = e
    return (
"  - capability_id: " + cid + "\n"
"    revision: 1\n"
"    status: active\n"
"    aliases: []\n"
"    supersedes: []\n"
"    merged_into: null\n"
"    split_into: []\n"
"    slug: " + slug + "\n"
"    title: " + q(title) + "\n"
"    importance: " + imp + "\n"
"    importance_rationale: " + q(rat) + "\n"
"    one_liner: " + q(one) + "\n"
"    intents: " + flow(intents) + "\n"
"    keywords: " + flow(kws) + "\n"
"    also_read: []\n"
"    card: cards/" + slug + ".md\n"
"    frontmatter:\n"
"      description: |\n"
"        " + intent.replace("\n"," ") + "\n"
"        信号：" + "、".join(kws) + "。\n"
"      tags: " + flow(tags) + "\n"
"    source_evidence:\n"
"      - source_id: src-main-book\n"
"        location: " + q(loc) + "\n"
"    promotion:\n"
"      destination: router\n"
"      notes: 阶段1.5通过验证（V1跨域加V2预测力加V3独特性全过）；按预算已满，以 router 形式经来源路由入口可达。\n"
    )

# 写 22 张卡片
for e in E:
    slug=e[1]
    open(os.path.join(CARD_DIR, slug+".md"),"w",encoding="utf-8").write(card_md(e))
print("cards written:", len(E))

# 追加进 verified.yaml（文本追加，不重序列化既有 7 条）
with open(os.path.join(CAP_DIR,"verified.yaml"),"r",encoding="utf-8") as f:
    cur=f.read()
if "destination: router" not in cur:
    with open(os.path.join(CAP_DIR,"verified.yaml"),"a",encoding="utf-8") as f:
        f.write("\n" + "".join(cap_yaml(e) for e in E))
    print("verified.yaml appended")
else:
    print("verified.yaml already has router entries; skip append")

# 重算 destinations.json（不依赖 yaml 解析，直接用已知结构）
pid_map = {
 "trading-loss-as-cost":"cap.032.loss-as-cost","loss-maturity-ladder":"cap.032.loss-maturity-ladder",
 "risk-guard-two-points":"cap.032.risk-two-points","avoid-over-optimization":"cap.032.avoid-over-optimization",
 "insect-system-recipe":"cap.032.insect-system","high-winrate-trap":"cap.032.high-winrate-trap",
 "learning-effect-chasing-tail":"cap.032.chasing-tail"}
d = {"bundle_id":"bundle.zouchuhuanjue","destinations":{}}
for s,cid in pid_map.items():
    d["destinations"][cid] = {"promoted_to":s,"router_view":f"{ROUTER}/references/capabilities/{s}.md"}
for e in E:
    cid,slug = e[0],e[1]
    d["destinations"][cid] = {"served_by":ROUTER,"card":f"{ROUTER}/references/capabilities/{slug}.md"}
json.dump(d,open(os.path.join(CAP_DIR,"destinations.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("destinations written:",len(d["destinations"]))
print("router caps:",len(E))
