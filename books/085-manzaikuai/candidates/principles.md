# 原则候选 · 《慢即是快：一个投资者20年的思考与实践》（三年一倍）

# 提取角色：principle-extractor（原则 / 清单 / 规则 / 断言）
# 扫描范围：全书 6073 行 / 403 页，已分块全量通读。
# 与 frameworks.md（f01–f32）的关系：框架是"怎么想"（可迁移推理结构），
#   本文件是"做不做"（可直接套用的操作规则 / 红线 / 清单）。凡框架已覆盖的
#   条目，此处取其具体操作化版本（如红线比例、排除清单、卖出三原则、建仓方式），
#   避免与框架重复而缺失原文。
# 每条 source_quote 均为 source.txt 原文，≤150 字。

- id: p01
  title: 一般不要踏入股市这个人博弈的市场
  type: principle
  source_chapter: 第二章 第一节 股市到底是天堂还是地狱
  source_quote: |
    一般不要踏入这个人性博弈的市场！如果你看到这后，还是执意要进入这个市场，并且还想在这个市场闯出一片属于自己的天地，那么你最好能够摸索出一条适合自己的稳健复利赚钱的道路来，并且知行合一地坚持下去。
  summary: |
    作者开篇即两次重复"一般不要踏入这个人性博弈的市场"。股市是逆人性的（别人卖时你买、别人追涨时你卖），注定不适合绝大部分人。若执意入场，前提是摸索出适合自己的稳健复利道路并知行合一坚持，否则不应进入。
  tags: [principle, gate, negative-checklist, behavior]

- id: p02
  title: 投资一定要用闲钱
  type: principle
  source_chapter: 第五章 第六节 分散投资应对黑天鹅事件
  source_quote: |
    投资者做投资一定还是要用闲钱，闲钱才能更好地面对各种不可预期的风险。
  summary: |
    闲钱（非救命钱、非短期要用的钱）才能扛住股市的不可预期波动与黑天鹅，避免在被动时点被迫割肉造成本金永久性损失。用必需资金去赌是投资大忌。
  tags: [principle, capital-preservation, risk]

- id: p03
  title: 任何好公司/好基金都不值得不计成本买入（全书复现≥3）
  type: principle
  source_chapter: 第三章 第三节 等待好股票的好买点
  source_quote: |
    任何一家公司，不论这家公司多么优秀，都不值得不计成本买入。投资者需要耐心等待好行业里的好公司出现好价格、好买点，而不是急于追高买入。
  summary: |
    作者针对股票（第三章）与基金（第四章）各强调一次，并多次"再次强调"：无论标的多优质，都必须等好价格/好买点，不可追高。这条在全书至少出现 3 次（股票章、基金章、反复重述），是核心纪律。
  tags: [principle, valuation, buy-rule, discipline]

- id: p04
  title: 好价格/好买点出现的四种触发情形
  type: checklist
  source_chapter: 第三章 第三节 等待好股票的好买点
  source_quote: |
    当好行业突发黑天鹅事件时，行业内所有公司的股价会出现全线下跌，这时好行业的好公司往往会被错杀，从而出现好价格、好买点。
  summary: |
    好公司出现好买点的四种情形清单：① 系统性风险错杀；② 行业黑天鹅（塑化剂、三聚氰胺、集采等）错杀；③ 估值进入低估分位（非周期PE近10年5%分位以下、周期PB近10年5%分位以下）；④ 技术面出现底部形态（C浪杀跌反转、突破趋势线、多头排列、V/W/头肩底、月线MACD/KDJ见底）。四者出现即可重点跟踪。
  tags: [checklist, buy-rule, valuation, opportunity]

- id: p05
  title: 股票卖出的三个常见原则
  type: checklist
  source_chapter: 第三章 第五节 等待好股票的好卖点
  source_quote: |
    以下就是好股票卖出的三个常见原则，只要触发这三个卖出原则的任何一个，投资者就可以选择卖出。
  summary: |
    卖出三原则清单：① 基本面实质恶化或底层逻辑颠覆，必须第一时间无条件卖出；② 价格严重高估（估值近10年90%分位以上）可分批卖出；③ 发现风险更低、潜在回报更高的更好机会可卖出。触发任一即可，可一键清仓或分批。
  tags: [checklist, sell-rule, discipline]

- id: p06
  title: 基金卖出的三个常见原则
  type: checklist
  source_chapter: 第四章 第五节 等待好基金的好卖点
  source_quote: |
    以下就是好基金卖出的三个常见原则，只要触发这三个卖出原则的任何一个，投资者就可以选择卖出。
  summary: |
    基金卖出三原则清单：① 核心基金经理离职变动，需重新评估；② 严重高估（持仓估值近10年90%分位以上）可分批卖出；③ 发现风险更低、回报更高的更好机会。与股票卖出原则对应，但把"基本面恶化"替换为"基金经理变动"。
  tags: [checklist, sell-rule, fund]

- id: p07
  title: 仓位红线——单行业≤30%、单只股票≤20%
  type: principle
  source_chapter: 第五章 第七节 仓位控制策略
  source_quote: |
    我们把投资账户中高风险的资金分别分配到3～5个行业中的5～10只股票上，单个行业的配置上限不能超过30%，单只股票的配置上限不能超过20%，投资中在任何时候都不要突破这两条投资的红线。
  summary: |
    用凯利公式算出最佳仓位后，仍受硬性红线约束：高风险资金分散在 3–5 个行业、5–10 只股票，单行业≤30%、单只≤20%，任何时候不突破。这是防止个股/行业黑天鹅伤筋动骨的铁律。
  tags: [principle, position-sizing, red-line, risk]

- id: p08
  title: 分批建仓——金字塔/均分/倒金字塔/定投
  type: principle
  source_chapter: 第三章 第三节 等待好股票的好买点
  source_quote: |
    左侧建仓方法可按照金字塔买入或者均分买入的方式来分批买入……右侧建仓方法可按照倒金字塔买入的方式来分批买入。
  summary: |
    不一次性满仓：左侧（下跌中）用金字塔（越跌越买）或均分买入；右侧（确认见底上涨后）用倒金字塔（越涨越少买）；基金还可用定期/不定额定投。分批建仓分散时点、降低波动影响、平滑成本。
  tags: [principle, position-sizing, cost-averaging]

- id: p09
  title: 技术指标先看大周期信号，再用小周期找买卖点
  type: principle
  source_chapter: 第一章 第四节 道术相结合综合投资的阶段
  source_quote: |
    使用技术指标时，当大周期指标出现抄底（或逃顶）信号后，再使用小周期指标寻找具体的买卖点。
  summary: |
    技术面操作次序：先等大周期（月线）出现抄底/逃顶信号，再用小周期精准定位具体买卖点。避免小周期噪音导致过早出手。
  tags: [principle, technical, timing, execution]

- id: p10
  title: 小周期技术指标不准，不必看
  type: principle
  source_chapter: 第一章 第二节 单纯的技术面阶段
  source_quote: |
    你发现了没有？上面我使用的技术指标周期都是大周期，小周期所有的指标可以说都不太准，没有必要看，看了也没有多少意义。
  summary: |
    短周期（日/分钟）信号噪音极大、互相矛盾，参考意义低；月线等大周期才简单有效。看大周期、忽略小周期，是技术分析的实操铁律。
  tags: [principle, technical, noise-filtering]

- id: p11
  title: 政策明确去杠杆/提示风险时，必须听话撤退
  type: principle
  source_chapter: 第一章 第四节 道术相结合综合投资的阶段
  source_quote: |
    2015年6月，出了一则各大券商严查场外配资……政策意图非常明显，发出信号去配资杠杆，这时候一定要听话，卸下杠杆撤退。
  summary: |
    "跟政策走"的具体执行：当宏观政策明确提示风险（如严查配资、降温），必须立刻行动、卸杠杆撤退；政策三番五次提示机会时才入场。逆政策而动必被套。
  tags: [principle, policy, macro, execution]

- id: p12
  title: 没有必要天天看盘（全书复现）
  type: principle
  source_chapter: 第六章 第三节 一天的涨跌对你真的那么重要吗
  source_quote: |
    对于大部分人来説，真的没有必要天天看盘。
  summary: |
    看盘是炒股中最没意义的事，多数时间在持股/持币等待。重点应放在内在价值上，每周看一次盘或不看，直到触发止盈或止损原则。天天看盘只会增加恐惧与频繁操作。
  tags: [principle, discipline, behavior, noise-filtering]

- id: p13
  title: 扛不住一天波动就别炒股，把钱存银行
  type: principle
  source_chapter: 第六章 第三节 一天的涨跌对你真的那么重要吗
  source_quote: |
    如果你连一天的波动都扛不住，我建议还是老老实实地把钱存银行吧。
  summary: |
    单日涨跌是正常现象，不应据此决策。若被一日波动牵着鼻子走，投资就成了苦差事且必亏。应拉长评估时间轴（以年为单位），关注内在价值而非每日报价。
  tags: [principle, behavior, time-horizon]

- id: p14
  title: ROE 低于 15%~20% 一律不看，优先高净利率、远离高杠杆（全书复现≥3）
  type: principle
  source_chapter: 第二章 第十节 ROE
  source_quote: |
    首先，财务指标是用来排除企业的，因为上市公司现在太多太多了，我们可以设置ROE低于20%的一律不看。
  summary: |
    作者在三处反复强调：用 ROE 作为排除法（第二章设"ROE<20%一律不看"，第三章要求"ROE最低连续多年≥15%且行业前三"，第五章排雷要求"ROE低于15%排除"）。并明确优先选高销售净利率模式、尽量远离高杠杆模式。全书复现≥3次。
  tags: [principle, screening, roe, quality, exclusion]

- id: p15
  title: 基本面排雷排除清单
  type: checklist
  source_chapter: 第五章 第四节 基本面排雷技巧
  source_quote: |
    排除资产负债率过高的上市公司……排除ROE低于15%的上市公司……排除从来不分红的“铁公鸡”或者分红非常少的上市公司。
  summary: |
    排雷清单（部分）：排除行业空间小/农林牧渔造假/行业前三外；排除重资产高杠杆无护城河；排除财务异常（高负债、经营现金流持续为负、扣非净利为负/ST、ROE<15%、有息负债高、存贷双高、高质押、审计非标、频繁换所等）；排除从不分红的"铁公鸡"。用排除法规避本金永久性损失。
  tags: [checklist, exclusion, risk, fundamental]

- id: p16
  title: 防范局部（非系统性）风险的三条措施
  type: checklist
  source_chapter: 第五章 第二节 防范局部风险
  source_quote: |
    有以下三条防范措施。(1)我们要选择好行业……(2)我们要选择好公司……(3)我们要分散投资、组合投资，用分散持仓的方式来规避这种不确定风险的发生。
  summary: |
    局部风险（行业/个股）防范三措施：① 选好行业（逻辑清晰、前景好、低波动）；② 选好公司（商业模式清晰、核心竞争力强、治理出色）；③ 分散/组合投资规避不确定性。
  tags: [checklist, risk, diversification]

- id: p17
  title: 系统性风险的两条应对建议
  type: checklist
  source_chapter: 第五章 第一节 系统性风险
  source_quote: |
    我们做投资需要把资金分别配置在不同类别的资产上，除了股票以外，还可以配置不动产、黄金、债券等资产，一旦股市系统性风险来临，不动产、债券、黄金等资产就会成为我们投资的避风港。
  summary: |
    系统性风险两条应对：① 对宏观/政策/地缘保持敏锐，提前感知并躲避（利弗莫尔："看到危险信号就躲开，几天后再回来"）；② 跨资产类别配置（股、债、黄金、不动产、现金），让避风港资产对冲股市系统性下挫。
  tags: [checklist, risk, systemic, asset-allocation]

- id: p18
  title: 防范股市诈骗清单
  type: checklist
  source_chapter: 第五章 第九节 股市防骗提醒
  source_quote: |
    警惕高收益诱惑：任何承诺“高收益、无风险”的投资都应该引起警惕。
  summary: |
    防骗清单（摘）：① 警惕高收益诱惑；② 不信内幕消息/专家推荐；③ 避免盲目跟风盈利截图；④ 小心虚假平台；⑤ 注意资金安全（不转账去不明平台）；⑥ 防范"杀猪盘"；⑦ 谨慎加入未经核实的投资群。任何许诺高额回报、转账到其他平台、保证输赢的荐股皆不可信。
  tags: [checklist, scam, security, behavior]

- id: p19
  title: 五种本金永久性损失情形须时时避免
  type: checklist
  source_chapter: 第五章 第三节 避免本金永久性损失的风险
  source_quote: |
    造成本金永久性损失的风险主要来自下面五种情况。
  summary: |
    五种情形清单：① 投资逻辑被彻底颠覆（行业技术革新致退市）；② 上不合理杠杆被迫卖出；③ 极端高估时买入后估值崩塌；④ 周期顶部业绩最好时买入随后下滑；⑤ 底部崩溃主动割肉把浮亏变实亏。这是投资者"唯一需要担心的风险"，须时时刻刻避免。
  tags: [checklist, risk, capital-preservation, survival]

- id: p20
  title: 买入前自问"下跌后敢加仓吗？不敢就别买"
  type: principle
  source_chapter: 第二章 第九节 逆向投资
  source_quote: |
    买股票（或指数）之前最好先问问自己，下跌后敢加仓吗？如果不敢，最好一开始就别买，因为价格的波动是不可避免的。
  summary: |
    逆向投资的实操自检：若下跌后不敢加仓，说明没研究透、不知内在价值，一开始就不应买。买之后的淡定源自买之前的深度分析；真正懂其价值，下跌只是更好的买点。
  tags: [principle, self-check, conviction, contrarian]

- id: p21
  title: 众人夺路而逃时，不挡路、不跟随
  type: principle
  source_chapter: 第二章 第九节 逆向投资
  source_quote: |
    正如邱国鹭所言：众人夺路而逃时，不挡路、不跟随。不挡路，是因为不想被踩死，不跟随是因为乌合之众往往跑错方向。
  summary: |
    逆向投资的行动准则：恐慌踩踏时不挡路（不被踩死）、不跟随（乌合之众常跑错方向），作壁上观等众人散去后捡其抛弃的金银。不与群体同向盲动。
  tags: [principle, contrarian, crowd, behavior]

- id: p22
  title: 必须克服的六种股市人性弱点
  type: checklist
  source_chapter: 第六章 第六节 投资中最大的敌人是自己
  source_quote: |
    股市中比较常见的一些人性弱点：一、贪婪；二、恐惧；三、羊群效应；四、锚定效应；五、线性外推；六、频繁交易。
  summary: |
    六大需克服的人性弱点清单：贪婪（顶部追高）、恐惧（底部割肉）、羊群效应（从众盲从）、锚定效应（被买入成本锚定而非内在价值）、线性外推（涨了以为永远涨、跌了以为永远跌，本质否定周期）、频繁交易（追逐每个波动、给券商打工）。
  tags: [checklist, behavior, psychology, self-awareness]

- id: p23
  title: 三年一倍实操法则（PE<30、净利增速>30%、拿住三年）
  type: principle
  source_chapter: 后记
  source_quote: |
    我的方法是：选一个扣非市盈率30倍（越小越好）以下的高成长类型的上市公司，扣非净利润增长率30%（越大越好）以上，这样三年后公司净利润增长一倍，即使市盈率不变，股价也应该增长一倍。
  summary: |
    "三年一倍"的可执行公式：选扣非PE<30倍（越小越好）、扣非净利增速>30%（越大越好）的公司，前提估值不高估，拿住三年，净利润翻倍即股价翻倍（市值=PE×利润）。这是复利的铁法则。
  tags: [principle, rule, compounding, growth]

- id: p24
  title: 看得准、下重手、拿得住
  type: principle
  source_chapter: 后记
  source_quote: |
    只要你看准一个好行业的好公司，在好价格（低估）的时候买入，耐心持有，高估卖出。或者换句话说，看得准、下重手、拿得住，三年赚一倍也不太难。
  summary: |
    成功投资的三步动作口诀：看得准（好行业好公司好价格）、下重手（在确定性机会上给足仓位）、拿得住（不被波动震出）。三者兼备，三年一倍不难。
  tags: [principle, maxim, execution, discipline]

- id: p25
  title: 只搞懂少数龙头，弱水三千只取一瓢（全书复现≥3）
  type: principle
  source_chapter: 第七章 第一节 99%的股票不值得投资
  source_quote: |
    我们普通散户如果能够完全搞懂5只个股，就一定能成为股市中赚钱那一部分人。股不在多，在精则灵；技不在杂，在专则明。
  summary: |
    作者多处强调（第七章"搞懂5只即可"、"股不在多在精则灵"、"弱水三千只取一瓢饮足矣"）：与其广撒网研究平庸股，不如深度搞懂少数龙头。普通散户搞懂5只以内即可成为赚钱的那部分人。全书复现≥3次。
  tags: [principle, focus, circle-of-competence, concentration]

- id: p26
  title: 投资成功的秘诀——找到适合自己且稳定盈利的策略，然后重复
  type: principle
  source_chapter: 第三章 第六节 股票的四大投资策略
  source_quote: |
    其实股市投资成功的秘诀，就是找到适合自己又能够稳定盈利的策略，然后重复操作。
  summary: |
    没有万能策略，只有适合自己的。找到能稳定盈利的策略后，关键动作是"重复操作"，把简单方法重复做、重复的事一直做，才能走向成功。
  tags: [principle, strategy, repetition, discipline]

- id: p27
  title: A股波动极大，进入高估区域必须止盈，否则坐过山车（全书复现≥3）
  type: principle
  source_chapter: 第七章 第二节 贵州茅台的长线投资机会
  source_quote: |
    虽然白酒行业非常适合长期投资，但是A股受到情绪影响波动性实在太大，当出现绝好的高估机遇，也是应该暂时脱手的，否则很容易坐过山车。
  summary: |
    即便是长线优质资产（茅台、伊利等），A股情绪化波动极大，作者多次提醒：进入高估区域必须止盈，否则易"坐过山车"回吐利润。长期持有≠无视高估，高点要舍得卖。全书在多个个股章节复现≥3次。
  tags: [principle, sell-rule, valuation, discipline]

- id: p28
  title: 顶部体感风险低但真实风险高；底部相反
  type: principle
  source_chapter: 第二章 第五节 均值回归
  source_quote: |
    在顶部区域，虽然体感风险低，但真实风险会非常高……；在底部区域，虽然体感风险高，但真实风险会非常低。
  summary: |
    体感风险与真实风险反向：顶部人人亢奋、体感安全，真实风险极高（应主动踏空防被套）；底部人人绝望、体感危险，真实风险极低（应主动被套防踏空）。用"真实风险"而非"体感"决策。
  tags: [principle, risk, contrarian, sentiment]

- id: p29
  title: 投资第一铁律——千万不能用融资上杠杆，不可考验人性（全书复现≥3）
  type: principle
  source_chapter: 第五章 第五节 永远不要上杠杆
  source_quote: |
    看来投资第一点，就是千万不能用融资。自有资金的话实在不行，可以装死躺平，融资的话压力巨大……千万不可考验人性。
  summary: |
    杠杆案例的血泪教训：自有资金被套可"装死躺平"，融资上杠杆在极端下跌中心态失衡、影响智商，甚至爆仓归零（与后市无关）。投资第一铁律是绝不能用融资，不可考验人性。作者在多个章节反复强调"永远不要上杠杆"。
  tags: [principle, leverage, risk, survival]

- id: p30
  title: 不要单吊一只股票，哪怕你非常了解这家公司
  type: principle
  source_chapter: 第五章 第五节 永远不要上杠杆
  source_quote: |
    （3）不要单投一只股票，哪怕你非常了解这家公司。
  summary: |
    即便深度了解、长期跟踪，也不应单吊一只股票。个体黑天鹅（即便核心资产如腾讯）可能造成毁灭性打击，分散是免费的保险。
  tags: [principle, diversification, concentration-risk]

- id: p31
  title: 不要在下跌趋势中加仓
  type: principle
  source_chapter: 第五章 第五节 永远不要上杠杆
  source_quote: |
    （2）还是要多维度综合判断更稳妥……不要在下跌趋势中加仓。
  summary: |
    趋势分析可在关键时保护你：下跌趋势中加仓易陷入越跌越深，应等多维度综合判断转好、趋势反转后再行动，而非凭"已很低"的直觉抄底。
  tags: [principle, trend, execution, behavior]

- id: p32
  title: 不要高估自己的承受力，也不要低估市场的极端
  type: principle
  source_chapter: 第五章 第五节 永远不要上杠杆
  source_quote: |
    （4）不要高估你的承受力，也不要低估市场的极端。
  summary: |
    人对自己承受亏损的能力常过度自信，对市场极端波动（个股腰斩、双腰斩、A股单周跌千点）常估计不足。敬畏市场极端，预留安全边际与心理缓冲。
  tags: [principle, risk, humility, behavior]

- id: p33
  title: 选主动基金的三个硬指标
  type: checklist
  source_chapter: 第四章 第三节 寻找好基金的路径
  source_quote: |
    选择基金成立10年及以上且没有中途更换过基金经理的基金；选择基金近10年年化收益率10%及以上的；选择基金近10年最大回撤不超过20%的。
  summary: |
    主动基金筛选硬指标清单：① 成立≥10年且未换经理；② 近10年年化收益≥10%；③ 近10年最大回撤≤20%（回撤过大没人拿得住）。三者筛出的主动基金极少但大概率是好基金。
  tags: [checklist, fund, screening, selection]

- id: p34
  title: 选指数（被动）基金的四个维度
  type: checklist
  source_chapter: 第四章 第三节 寻找好基金的路径
  source_quote: |
    我们可以按照跟踪的标的指数、跟踪误差、流动性、费率等维度对被动基金进行筛选和分析。
  summary: |
    指数基金筛选四维度清单：① 跟踪标的价值高（宽基如沪深300/中证A50，或长牛行业如消费/医药）；② 跟踪误差小（精确复制）；③ 流动性好（份额大、易买卖）；④ 费率低（省成本）。
  tags: [checklist, fund, screening, index]

- id: p35
  title: 核心卫星策略的比例建议
  type: principle
  source_chapter: 第四章 第六节 指数基金的六大投资策略
  source_quote: |
    保守型投资者可选择80%的核心资产和20%的卫星资产，稳健型可选择70%的核心资产和30%的卫星资产，激进型可选择60%的核心资产和40%的卫星资产。
  summary: |
    核心（稳健、宽基/债基）占大比例提供基本盘，卫星（行业/主题）占小比例博超额。比例随风险偏好：保守80/20、稳健70/30、激进60/40。核心是控回撤、提升持有体验。
  tags: [principle, asset-allocation, core-satellite, balance]

- id: p36
  title: 生钱账户中激进资产比例 = 100 − 年龄
  type: principle
  source_chapter: 第五章 第七节 仓位控制策略
  source_quote: |
    一般投资高风险资产的钱有不同的资金配置比例要求（100-你当下的年龄=你投资激进资产的比例）。
  summary: |
    标准普尔四笔钱中"生钱的钱"内部再分激进/稳健：激进资产比例 = 100 − 当前年龄（30岁则用70%配激进、30%配稳健）。年龄越大、风险敞口越小。
  tags: [principle, asset-allocation, age, risk]

- id: p37
  title: 亏损回本难度警示——亏越多回本越难
  type: principle
  source_chapter: 第五章 第七节 仓位控制策略
  source_quote: |
    我强烈建议所有读者，一定要把这张亏损回本涨幅表打印出来……时刻提醒自己：尽量不要亏损，尽量不要亏损，尽量不要亏损。
  summary: |
    回本公式 1/(1−亏损幅度)−1：亏50%需涨100%、亏90%需涨900%、亏99%需涨9900%。亏损极具毁灭性且可能瞬间发生。仓位控制的核心是"尽量不要亏损"，避免坠入深坑。
  tags: [principle, drawdown, math, capital-preservation]

- id: p38
  title: 投资最大的敌人是自己，心态占成功 85%
  type: principle
  source_chapter: 第六章 第六节 投资中最大的敌人是自己
  source_quote: |
    理念重于技术，心态重于理念……一个人在投资上的成功，有15%归结于他综合的投资能力，另外85%归结于他的投资心态。
  summary: |
    作者认为决定投资成败的最主要因素是心态：成功 = 15%综合能力 + 85%克服人性弱点的能力。股市放大缺点，战胜心魔（贪婪、恐惧等）才有机打败市场。
  tags: [principle, psychology, behavior, self-awareness]

- id: p39
  title: 信心比黄金更重要，相信相信的力量
  type: principle
  source_chapter: 第六章 第八节 信心比黄金更重要
  source_quote: |
    信心比黄金更重要，没有原因，因为相信，所以相信！
  summary: |
    在至暗时刻，信心是支撑穿越周期的动力。作者基于国运向上与周期/均值回归的信念，坚信熊去牛来。底部绝望时更需"相信相信的力量"，避免因恐慌在底部交出带血筹码。
  tags: [principle, psychology, conviction, sentiment]

- id: p40
  title: 不要被股市所累，投资要快乐，否则不如销户
  type: principle
  source_chapter: 第六章 第九节 诗与远方
  source_quote: |
    如果因为我们去做投资而影响了生活，天天心情不爽抑郁，甚至影响了家庭和睦，这真的是违背了投资的初衷。与其如此，倒不如销户远离股市。
  summary:
    投资目的是改善生活而非自寻烦恼。若炒股导致焦虑、抑郁、家庭不和，则违背初衷，应销户远离。投资中应追求心情舒畅、快乐投资。
  tags: [principle, life, behavior, well-being]

- id: p41
  title: 选股核心——研究主营产品需求是否快速增加
  type: principle
  source_chapter: 第三章 第一节 股票的底层逻辑
  source_quote: |
    影响股票长期价格的一个核心因素就是需求。所以，我个人认为研究股票的最核心的一个因素是研究上市公司主营产品的需求是否会快速增加，或临时性需求大幅增加。
  summary: |
    长期股价由内在价值（现在价值+未来成长性）决定，而成长性核心是"需求"：主营产品需求快速增加或临时大增，叠加市占率上升，才是好股票的根本。研究需求优先于研究其它。
  tags: [principle, research, demand, growth, stock-picking]

- id: p42
  title: 优先选非周期行业龙头，避开高难度强周期
  type: principle
  source_chapter: 第三章 第二节 寻找好股票的三种分析方法
  source_quote: |
    周期行业的绝大部分公司业绩往往忽上忽下，普通投资者很难把握，而非周期行业的龙头公司业绩基本能够长期持续且比较稳定地增长，我们做投资时应重点寻找非周期行业内龙头上市公司。
  summary:
    行业选择纪律：非周期（消费、医药、公用事业）龙头业绩长期稳定可预测，应重点寻找；强周期（房地产、能源、科技）业绩忽上忽下、普通投资者难把握，尽量避开。
  tags: [principle, industry-selection, non-cyclic, quality]

- id: p43
  title: 收益主要来自择股而非择时
  type: principle
  source_chapter: 第二章 第二节 知彼：正确认识股市的残酷性
  source_quote: |
    不论散户还是机构、公司法人投资者，择时收益都是负数，这说明投资一般不要去择时……选股收益都是正数，这说明投资正收益主要来源于择股。
  summary:
    上交所统计显示，各类投资者"择时收益均为负"，而"选股收益均为正"。结论：一般不要去择时，正收益主要来源于选对好行业好公司（在低估区买入并持有）。
  tags: [principle, stock-selection, timing, data]

- id: p44
  title: 真正最致命的问题是仓位控制（全书复现≥3）
  type: principle
  source_chapter: 第五章 第七节 仓位控制策略
  source_quote: |
    做投资亏钱，有时候是选企业出问题，有时候是因为买入时机出问题，但是这都不是致命的问题，真正最致命的问题，是仓位控制问题！
  summary:
    选错企业、买错时机都非致命，真正致命的是仓位控制：重仓/满仓遭遇黑天鹅或杠杆爆仓可伤筋动骨甚至归零。作者在仓位控制章及多章反复强调此点，全书复现≥3次。
  tags: [principle, position-sizing, risk, capital-preservation]

- id: p45
  title: 任何许诺高额回报、转账去其他平台、承诺保收益的荐股都是骗子
  type: principle
  source_chapter: 第五章 第九节 股市防骗提醒
  source_quote: |
    任何许诺你高额回报，任何让你转账去其他平台，诱导你下载某某App转钱的（假原油、假期货、博彩、虚拟币、假私募、假券商、场外配资等）都是骗子。
  summary:
    防骗底线规则：凡许诺高额回报、要求转账至非正规平台/下载App、保证输赢的荐股喊单，皆为诈骗。国内合法场所仅限上交所、深交所、北交所及正规期货交所；没有人能预测明天涨跌或永远稳赚。
  tags: [principle, scam, security, negative-checklist]
