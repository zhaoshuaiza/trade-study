# 《主力操盘手法揭秘》（蒋幸霖 编著）阶段 1.5 + 1.6 验证与晋级清单

> 书 slug：`089-zhuli` · 来源：`source.txt`（OCR，405,306 字节 / 7466 行 / 231 页，带 `===== 第N页 =====` 分页标记，固定列宽硬换行）
> 验证者：cangjie stage 1.5（三重验证）+ stage 1.6（五判据晋级门）执行器
> 候选池：frameworks(f01–f24) / principles(p01–p48) / cases(c01–c34) / counter-examples(ce01–ce36) / glossary(g01–g25)，共 **167** 条
> 格式对齐：`books/085-manzaikuai/verified.md`、`destinations.json`（同批已完成书，直接对齐其结构与命名风格）
> 段归属：本批按 stage 2 的 **R / I / A1 / A2 / E / B 六段**（R 原文 · I 自述 · A1 书中案例 · A2 触发与操作规则 · E 可执行步骤 · B 边界）标注。
> V 编号口径：沿用同批 085 的重新编号 —— **V1 自洽 / V2 溯源 / V3 跨域**；五判据亦沿用 085 口径 —— 源自原文 / 原子化 / 不重复 / actionable / 不矛盾。

---

## ★ 全局边界（定性护栏 · 必须随每个模块下发，见 `destinations.json` 各 module.guardrails）

> 以下三条为本批最高优先级硬约束，**写进 `verified.md` 全局段，并在 `destinations.json` 每个模块逐一携带**。任何下游 skill 生成动作前必须先过此段。

1. **时效 / 合规**：本书成书 **2013 年 5 月**、案例集中 **2009–2011 年**，对应股改后「多账户坐庄、庄股横行」的**旧庄股生态**。书中当作「业内常用手法」中性讲述的**对倒 / 对敲 / 虚假申报 / 连续交易 / 约定交易 / 自买自卖 / 多账户分仓 / 散布消息配合做盘 / 涨停板撤单**，在 **2020 年新《证券法》**、交易所 L2 逐笔穿透与账户关联核查下**多已明确违法且极易被识别**。→ **所有「识别类」条目只能作为防范对象晋级，绝不可晋级为可执行操作**；输出契约只允许「散户如何识别与防范」，严禁生成任何挂撤单、做量、分仓、散布消息、拉抬打压动作。
2. **用户交易约束**：**A 股单边做多、不做空、不做期货、主做可转债 + 股票**。全书判据基于**股票 T+1 / 10% 涨跌停 / 集合竞价 / 五档委托 / 换手率 / 60 日线 / 除权填权**，而可转债为 **T+0、无涨跌停（有临时停牌）、20%/30% 涨跌幅限制、与正股联动、有强赎/下修条款**——**股票量价与盘口判据不可平移可转债**；「假填权出货」「高送转诱多」在可转债上无对应物。引用股票阈值必须带「前置条件 + 不可平移」标注。
3. **g14 消歧（头号误用词）**：术语 **g14「做空 / 诱空 / 逼空 / 空头陷阱 / 反手做多」是 A 股口语**（分别指打压卖出、制造恐慌诱人离场、急速打压、跌势、看空离场/观望、逢低买入），**≠ 融券卖出、≠ 股指期货/期权做空、≠ 任何双向或杠杆机制**。成书前提即「我国股市不存在做空机制，必须低买高卖」（原文第 658、903 行实证）。→ **晋级时必须保留此消歧，否则下游会生成用户明令禁止的做空/双向/期货动作**。本书原文实测有 17+ 处「做空/诱空/逼空/反手做空」口语（如第 2038、2289、6004、6036、6133、6134 行），误用风险真实且高频，非假设。

> **识别类 vs 可执行类的晋级分界（落地总纲，详见第六节）**：本批把 167 条按输出契约切成两类——
> - **识别-防范 / 识别-推理类**（占绝大多数）：晋级后输出「痕迹怎么读 / 骗术怎么识别 / 阶段怎么判别 / 如何交叉校验」，**零主力手法操作**；涉及对倒、虚假申报、骗线、多空陷阱者一律只作防范对象。
> - **合规可执行动作类**：仅 `zhuli-exit-discipline`（及 `washout-distribution` 的卖出触发器、`intent-inference`/`follow-playbook` 的「等确认、空仓等待、中间仓位」）承载，且动作严格限于**散户对自身的、A 股单边做多框架内、用户约束允许**的动作（卖出离场 / 不买 / 轻仓 / 分批 / 观望 / 预设止损），**不含做空、杠杆、期货、对倒、分仓**。

---

## 一、三重验证结论（V1 / V2 / V3）

### V1 自洽校验（字段完整 / 引用闭合 / id 连续无重）
- **字段完整**：frameworks / principles 含 `id/title/type/source_chapter/source_quote/summary/tags`；cases 增 `bound_to/outcome`；counter-examples 增 `failure_mode/mechanism/warning_signs/bound_to/summary`；glossary 用 `term/author_definition/key_distinction/why_it_matters/tags` 并**额外增补** `source_quote/summary/bound_to`（满足本批统一自检）。5 类逐条核对 **全部齐整、无空字段**。
- **source_quote 闭合**：全部 YAML `|` 块闭合正常；frameworks / counter-examples / glossary 的成对 `"` 引号、cases / principles 的纯文本摘录均成对闭合、无截断。
- **id 连续无重**：f01–f24(24) / p01–p48(48) / c01–c34(34) / ce01–ce36(36) / g01–g25(25) = **167**，各类连续、无重复、无缺号、无多号。
- **V1 结论：167 条全部通过**（无需淘汰）。

### V2 溯源校验（≥30% 抽样 grep 回 source.txt；本批做到 100% 覆盖）
采用**双层核验**，覆盖强度远超 ≥30% 要求：
1. **全量 167 条归一化逐句核验（100% 覆盖）**：`source.txt` 为固定列宽硬换行 OCR，长引文用 `grep -F` 必然 MISS。故先对原文与引文做「去 `===== 第N页 =====` 标记 / 去所有空白 / 去标点，仅保留汉字·字母·数字·%」归一化，再按句读切分逐句做子串比对（等价 `grep -F`），共 **399 个句子探针**，原文归一化长度 121,946 字。
2. **`grep -F` 字面抽样交叉验证**（跨全部 5 类）：`再狡的狐狸` / `低迷状态、正常状态、活跃状态` / `短线拉升的必备条件` / `目标点位` / `不转移股票所有权` / `朝现有的卖单直接申报` / `深纺织A在2009年10月12日` / `空头陷阱不是空头市场` / `散户大厅` / `鳄鱼法则` / `海南国际旅游岛` / `市场的内在波动规律` 等均逐字命中；并定向核实 g14/ce36 的「我国证券市场没有做空机制」（第 658、903 行）与 ce34 的「主力不是万能」（第 532 行）。

- **结果**：**167 / 167 条全句命中，399 / 399 探针逐字命中（100%）**，**0 条无法定位、0 条需修 quote、0 条 needs_review**。引文为 OCR 原貌照抄（含「一且 / 造项 / 风凰 / 图47」等原貌错字，为可定位故保留），去空白后全部可在标注章节定位，**无编造、无断章取义、无概括改写冒充逐字引用**。
- 与同批 085（150/173 命中、6 条修 quote、2 条 needs_review）相比本批更干净，原因是本批抽取器统一采用「OCR 原貌逐字摘录」而非概括改写。
- **V2 结论：通过**（全量命中）。

### V3 跨域校验（是否真可迁移到盘口以外场景）
- **强跨域（可迁移到竞争情报 / 反欺诈 / 数据治理 / 组织 / 职业 / 个人决策 / 复杂系统）**：
  - **frameworks 几乎全类**，其中用户点名的 5 条尤为突出：**f01**（痕迹→意图：竞争情报/审计/反欺诈）、**f03**（反事实推理：识别刷单/虚假承诺/谈判姿态）、**f11**（试盘闭环：灰度发布/A-B 测试/小额试探）、**f08**（基线偏离：异常检测/A-B 归因/故障排查）、**f21**（净效果 vs 符号：看现金流而非利润包装/看净头寸而非口头表态）。另有 f02 信息分层、f05 阶段优先、f09 多维交叉、f10 证据分级、f13 连续性证伪、f14 反向校验、f16 养套杀、f17 消息验证、f18 环境过滤、f19 主体分层、f20 等确认、f22 序贯下注、f23 退出触发器、f24 模型谦逊均强跨域。
  - **principles**：p03/p26/p28/p30/p32/p34/p35/p37/p38/p39/p40/p42/p43/p44/p48（阈值判断 / 环境过滤 / 离场触发器 / 不确定管理 / 消息校验 / regime-change 重估 / 反例清单）约 18 条。
  - **counter-examples**：ce23/ce24/ce28–ce36（人性弱点 / 认知误区 / 过度自信 / 从众 / 幸存者偏差 / 不可证伪 / 时效合规）强跨域，约 12 条。
- **弱跨域（交易语境限定）**：
  - **frameworks**：f04/f06/f07/f15 为「盘口/坐庄骨架/换手率阈值/陷阱」专属，可迁移但需重挂情境。
  - **principles**：绝大多数换手率、振幅、涨跌停、均线、KDJ/MACD、分时、买卖点清单为**纯股票技术规则**（尤其不可平移可转债），约 30 条。
  - **glossary 全类 25 条**（作者私有术语定义/辨析）、**cases 全类 34 条**（2009–2011 个股/分时事后图例）整体交易语境限定。
  - **counter-examples**：ce01–ce18 具体骗术识别、ce19–ce22/ce25–ce27 误判类为盘口语境限定。
- **V3 结论**：框架层约 5/6 具备真实跨域价值（用户点名 5 条全部强跨域）；原则层约 1/3 强跨域、其余为股票专属阈值；反例层「人性/认知/纪律/批判」类强跨域、「具体骗术/误判」类交易限定；**术语与案例两类整体交易语境限定，标 `status: reference` 降级保留**。

---

## 二、五判据晋级门（GO / CONDITIONAL / NO）

> 判据1 源自原文 · 判据2 原子化可独立 · 判据3 不重复（重复则合并）· 判据4 对交易者 actionable（识别/防范或合规动作皆可）· 判据5 不矛盾
> **GO** = 五判据基本全过，作为 canonical 卡锚点/核心；**CONDITIONAL** = 有价值但须合并、或仅作子卡/边界卡/股票专属细则；**NO** = 降级 `status: reference`（术语卡/案例卡），**不进 `rejected/`、不失联**（1.6 硬规则）。
> ⚠️ 所有涉及对倒/虚假申报/骗线/多空陷阱的 GO/CONDITIONAL 条目，其判据4「actionable」一律解读为 **「actionable 于识别与防范」**，不作「actionable 于模仿操作」——见全局边界与第六节。

### 2.1 去重与合并总纲（先读这段，避免重复计数）

本批 167 条经合并后收敛为 **10 张 canonical 卡（8 promoted + 2 router 卡）+ 1 个来源路由入口**，而非 167 个 skill。用户点名的 5 个高重叠簇处理如下：

| 簇 | 成员 | 合并建议 | canonical 卡数 |
|----|------|----------|----------------|
| **① 换手率五态 + 量价三态** | f07 + p04–p09 / p13 + g03 | **合并为 1 张** `zhuli-turnover-volume`（promoted）。f07 为 I 段锚点；p04–p09/p13 七条阈值卡全部折进 A2（同一状态机，不再单列）；g03 术语卡入 R；B 段写死「股票流通盘 + T+1 专属，可转债不可平移」「量可被对倒伪造，与量柱体系立场冲突须交叉校验」 | **1** |
| **② 洗盘 vs 出货判别** | f12/f13/f14 + p20/p22/p24/p30–p33 + ce19–ce27 | **拆为 2 张**：`zhuli-washout-vs-distribution`（promoted：f12/f13 五维判别 + 60 日线延迟判定 + p22/p24/p30–p33 出货特征与离场触发器 + ce19/ce20 误判）＋ `zhuli-deception-defense`（promoted：f14 骗术反向校验层、ce21–ce24/ce27 量价误判）。二者输出契约不同（前者「判别 + 卖出离场」，后者「纯识别防范」），按 1.6 硬规则不强行拼成一个模糊 Skill。**f14 与簇③共享** | **2**（1 张与簇③共享） |
| **③ 骗术识别 / 反事实推理** | f01/f03/f10/f14/f15/f16 + ce01–ce18 + g12/g13/g14 | **拆为 2 张**：`zhuli-intent-inference`（promoted：f01/f02/f03/f08/f09/f21 跨域推理锚点，f10 证据分级）＋ `zhuli-deception-defense`（promoted：f14/f15/f16/f17 校验层 + ce01–ce18 十八种骗术识别防范）。f01/f03 是「怎么推理」，ce01–ce18 是「识别什么骗术」，契约不同不合并。**g12/g13/g14 消歧卡入 B 段（g14 为全局硬边界）** | **2** |
| **④ 坐庄五阶段** | f05/f06 + 各阶段 p/c | **合并为 1 张** `zhuli-stage-model`（promoted）。f05/f06 为 R/I，p14–p19/p27 各阶段阈值为 A2 清单，c01–c22 建仓/试盘/洗盘/拉升案例为 A1 证据卡按 `bound_to` 绑定；B 段标「十阶段为定位框架非刻板时间表 / 各阶段对敲分仓仅识别防范 / 事后叙事不可证伪」 | **1** |
| **⑤ 离场 / 弃庄 / 止损** | f23 + p30/p32/p44/p48 + ce28–ce36 | **合并为 1 张** `zhuli-exit-discipline`（promoted）。f23 为 R/I，p30/p32/p44/p48 为 A2 触发器清单，ce28–ce33 为 B 段纪律边界，ce34/ce35/ce36 批判层入 B（幸存者偏差 / 不可证伪 / 时效合规）。**这是唯一以「合规可执行动作」为主的模块** | **1** |

- **簇外补充**：`zhuli-orderbook-language`（promoted：f04/f10 + g04/g05/g06 + ce08/ce09/ce22 + p01–p03/p10–p12）、`zhuli-market-regime-filter`（promoted：f18 + p26 + ce34）、`zhuli-intent-inference`、`zhuli-deception-defense` 共同覆盖 8 个 promoted。
- **2 张超预算 router 卡（served_by）**：`zhuli-follow-playbook`（跟庄实战清单：f20 + p39–p46 + g16/g20/g23 + c05 等破绽/地量/强庄股/突然放量缩量涨停跌停应对）、`zhuli-actor-typology`（主力类型/周期 f19/f24 + g21/g22/g24 + p47/p27 + 目标点位公式）。
- **来源路由入口 `zhuli`（router）**：收纳全部术语卡 g01–g25、案例卡 c01–c34 的兜底，以及**全局边界卡** g14（消歧）、ce35（不可证伪）、ce36（时效合规）——三者 B 段被所有模块引用。
- **5 簇去重后净增 canonical 卡 = 8 张 promoted**（含簇②↔簇③共享 1 张、簇③↔模块1 共享 1 张）+ 2 张 router 卡，非简单相加。
- **cases c01–c34**：全部 A1 段证据卡，按 `bound_to` 绑定，**不晋级**。
- **glossary g01–g25**：全部定义卡 `status: reference`，并入对应卡 R/I/B，**不晋级**（g14 一词多义归全局 B 段）。

### 2.2 Frameworks（f01–f24）

| id | 标题 | verdict | 一句话理由（五判据 + 去向 + 识别/可执行分界） |
|----|------|---------|----------------------------------------------|
| f01 | 从可观测痕迹反推不可观测意图 | **GO** | 原话+原子+强跨域(痕迹→意图)；簇③锚点，入 `intent-inference` R（纯推理框架，零操作） |
| f02 | 信息按发送者意图四分（真/假/隐藏） | **GO** | 原话+原子+强跨域(尽调/舆情解码)；入 `intent-inference` I |
| f03 | 反事实推理识破展示性行为 | **GO** | 原话+原子+强跨域(刷单/姿态识别)；入 `intent-inference` I，兼 `orderbook-language` 证伪基础 |
| f04 | 盘口委托单语言解读框架 | **GO** | 原话+原子+盘口专属；入 `orderbook-language` R（**识别-防范**，挂撤单/夹板禁作操作） |
| f05 | 阶段优先于信号：先定阶段再解信号 | **GO** | 原话+原子+强跨域(先定阶段再解释指标)；入 `stage-model` I |
| f06 | 坐庄五阶段三段式判别框架 | **GO** | 原话+原子+全书骨架；簇④锚点，入 `stage-model` R（各阶段对敲分仓仅识别防范） |
| f07 | 换手率五态阈值框架 | CONDITIONAL | 原话+原子但阈值股票专属、不可平移可转债；簇①锚点并入 `turnover-volume` I，附适用边界 |
| f08 | 基线偏离检测：排除共因看残差 | **GO** | 原话+原子+强跨域(异常检测/A-B 归因)；入 `intent-inference` I |
| f09 | 位置为纲的多维交叉校验 | **GO** | 原话+原子+强跨域(多源独立证据交叉)；入 `intent-inference` I |
| f10 | 证据分级：一手数据 vs 可造假衍生指标 | **GO** | 原话+原子+强跨域(数据治理/情报评估)；入 `orderbook-language` I（盘口第一手资料） |
| f11 | 试盘闭环：主动探测→读反馈→分支决策 | **GO** | 原话+原子+强跨域(灰度/A-B/小额试探)；入 `stage-model` I |
| f12 | 洗盘 vs 出货判别（五维+延迟判定） | **GO** | 原话+原子+可跨域(正常回调 vs 趋势反转)；簇②锚点，入 `washout-distribution` R（**卖出离场**为唯一可执行的合规动作） |
| f13 | 量能连续性证伪单日巨量 | **GO** | 原话+原子+强跨域(识别刷量/脉冲营销)；入 `washout-distribution` I，与换手率/量柱体系交叉 |
| f14 | 骗术反向校验层：图形与量皆可伪造 | **GO** | 原话+原子+强跨域(反欺诈/信息战)；簇②③共享，入 `deception-defense` R（**纯识别防范，零可执行操作**） |
| f15 | 多空陷阱的设置与辨别 | CONDITIONAL | 真实但含「做空/诱空」口语，须随 g14 消歧；并入 `deception-defense` I，不单列 |
| f16 | 养套杀 / 培养惯性思维的伪装 | **GO** | 原话+原子+强跨域(补贴后收割/博弈)；入 `deception-defense` I |
| f17 | 消息与题材验证（实质 vs 价格反应错配） | **GO** | 原话+原子+强跨域(新闻/研报可信度)；入 `deception-defense` I，关联弃庄触发器 |
| f18 | 大盘环境过滤（弱市不介入、逆市压测） | **GO** | 原话+原子+强跨域(beta vs alpha/压力测试)；入 `market-regime-filter` R |
| f19 | 主力类型 / 周期分类 | CONDITIONAL | 真实但为 router 级分类资产、语境随注册制/量化改变；并入 `actor-typology`(router) I |
| f20 | 跟庄择时：等确认、跟破绽而非跟突破 | **GO** | 原话+原子+强跨域(等不可伪装证据再下注)；入 `intent-inference` I（「空仓等待/等确认」为非交易操作动作） |
| f21 | 表象与实质背离：看重心不看 K 线方向 | **GO** | 原话+原子+强跨域(净效果 vs 符号)；入 `intent-inference` I |
| f22 | 不确定时的中间仓位与分批渐进下注 | **GO** | 原话+原子+强跨域(序贯决策)；入 `exit-discipline` E（**合规可执行**：中间仓位/分批，不含做空杠杆期货） |
| f23 | 弃庄 / 离场触发器（预设退出条件） | **GO** | 原话+原子+强跨域(预设退出触发器)；簇⑤锚点，入 `exit-discipline` R |
| f24 | 目标点位估算 + 模型不可机械刻板 | CONDITIONAL | 真实但「信心系数2」无统计支撑、股票专属；并入 `actor-typology`(router) I，附失效条件 |

### 2.3 Principles（p01–p48）

| id | 标题（简写） | verdict | 一句话理由（去向 / 段 / 识别-可执行） |
|----|------|---------|--------------------------------------|
| p01 | 开盘三个 10 分钟 / 观察 30 分钟研判大势 | CONDITIONAL | 时段细则、股票集合竞价专属；并入 `orderbook-language` A2 |
| p02 | 尾市收红带长下影可跟进、星期五降仓 | CONDITIONAL | 时段 + 星期效应细则；并入 `orderbook-language` A2（尾盘做价仅识别防范） |
| p03 | 阻力/支撑有效突破后互换，冲过买进跌破卖出 | **GO** | 原话+原子+通用阈值判断；入 `orderbook-language` A2（**识别-防范**，关口造假仅识别） |
| p04 | 日换手率 >10% 且成交火爆 = 行情将逆转 | CONDITIONAL | 与 f07/p05–p09 同状态机；簇①并入 `turnover-volume` A2 |
| p05 | 日换手率 1%–10% 按原趋势加速 | CONDITIONAL | 同簇①，并入 `turnover-volume` A2 |
| p06 | 日换手率 <1% 不要轻易介入、出场观望 | CONDITIONAL | 同簇①，并入 `turnover-volume` A2（与 g16 地量看似冲突，须位置校准） |
| p07 | 3% 日换手率是短线拉升必备条件 | CONDITIONAL | 同簇①，并入 `turnover-volume` A2 |
| p08 | 高换手率警戒：>10%、连续 >7%、累计涨幅过大 | CONDITIONAL | 同簇①，并入 `turnover-volume` A2（高位校准） |
| p09 | 周换手率五态 = 日值 ×5 | CONDITIONAL | 同簇①，并入 `turnover-volume` A2 |
| p10 | 平开放量上冲：早盘 15–30 分钟量超常日即异动 | CONDITIONAL | 量价异动细则；并入 `orderbook-language` A2（先排大盘共因） |
| p11 | 急涨急跌：几分钟内 >3% 必是主力运作 | CONDITIONAL | 振幅细则、股票专属；并入 `orderbook-language` A2 |
| p12 | 振幅四情形：高位振幅 15%–20% + 量比突增 = 出货 | CONDITIONAL | 振幅×量比×位置矩阵；并入 `orderbook-language` A2 |
| p13 | 底部放量换手 10% 属异常特大量、进货需两周 | CONDITIONAL | 底部量能细则；并入 `turnover-volume` A2（对倒放量仅识别防范） |
| p14 | 温和上涨建仓期「买阴不买阳」、放巨量分批出局 | CONDITIONAL | 建仓阶段操作节奏；并入 `stage-model` A2（不含做空杠杆） |
| p15 | 跌停不可盲目杀跌；底部突发跌停持股不杀 | **GO** | 原话+原子+actionable(先判原因再动)；入 `stage-model` A2（跌停挂撤单吃筹属虚假申报，**仅识别防范、禁作操作**） |
| p16 | 底部形态突破必须放量确认；双底间隔≥1 月 | CONDITIONAL | 形态参数、股票专属；并入 `stage-model` A2（假突破仅识别防范） |
| p17 | 试盘时间/空间阈值；方向随大盘强弱切换 | CONDITIONAL | 试盘量化清单；并入 `stage-model` A2 |
| p18 | 低开高走低开幅度 >3%；试盘后走强即进场 | CONDITIONAL | 试盘进场细则；并入 `stage-model` A2 |
| p19 | 金针探底四条件才是最佳买点，勿抢快速下探 | CONDITIONAL | 探底进场清单；并入 `stage-model` A2（等确认，不抢探底） |
| p20 | 洗盘时间（3天/1周/1–3月）与空间（10%、30%–50%） | CONDITIONAL | 洗盘时空阈值；簇②并入 `washout-distribution` A2 |
| p21 | 筹码比例：约 20% 冬眠、控盘 30% 则 50% 浮筹威胁 | CONDITIONAL | 旧庄股筹码结构；并入 `stage-model` A2（不可平移可转债） |
| p22 | 关键位延迟判定：跌破 60 日线达 3% 考虑出货 | CONDITIONAL | 与 f12 五维判别重复；簇②并入 `washout-distribution` A2 |
| p23 | 关键位进出清单：放量突破跟进、跌破离场 | CONDITIONAL | 与 f12/p22 同簇；并入 `washout-distribution` A2 |
| p24 | 洗盘均线特征（10 日线上、不破 30 日线）与结束四标志 | CONDITIONAL | 洗盘均线细则；簇②并入 `washout-distribution` A2 |
| p25 | 洗盘后创新高即跟进；趋势未坏比主力更有耐心 | CONDITIONAL | 与 f12/ce19 同簇；并入 `washout-distribution` A2 |
| p26 | 弱市中尽量不要介入个股；对个股利好谨慎 | **GO** | 原话+原子+actionable(环境过滤开关)；入 `market-regime-filter` A2（**合规可执行**：弱市不介入/观望） |
| p27 | 拉升时间/升幅/控盘量化阈值清单 | CONDITIONAL | 拉升阈值、旧庄股专属；并入 `stage-model` A2 |
| p28 | 拔高阶段逃命：量价背离 + 放量长阴 = 大逃亡尾声 | **GO** | 原话+原子+actionable(逃命触发器)；入 `exit-discipline` A2（卖出离场，非做空） |
| p29 | 主力出货五时机清单 | CONDITIONAL | 与 p30–p33 出货识别簇重叠；并入 `washout-distribution` A2 |
| p30 | 一旦跌破关键价位即考虑出货（出货早期不需量） | **GO** | 原话+原子+硬离场触发器；入 `exit-discipline` A2（**合规可执行**：跌破即卖出） |
| p31 | 出货时间/空间阈值（2–3天、半月–3月、≥20% 空间） | CONDITIONAL | 出货时空细则；并入 `washout-distribution` A2 |
| p32 | 出货离场触发器清单（放量连阴/高位跌停/破5日线） | **GO** | 原话+清单+actionable；入 `exit-discipline` A2（卖出离场，非做空） |
| p33 | 出货市场/技术特征：长上影 + 换手 20%+、均线死叉 | CONDITIONAL | 出货特征阈值；并入 `washout-distribution` A2 |
| p34 | 落入多头陷阱：短线斩仓、长线先验基本面、假突破止损 | **GO** | 原话+actionable(止损/先验基本面)；入 `deception-defense` A2（**识别-防范**，止损为卖出） |
| p35 | 空头陷阱辨别三技巧：把握不准先避开、能定成本就守仓 | **GO** | 原话+actionable(不确定管理)；入 `deception-defense` A2（**含做空口语，随 g14 消歧，禁生成做空动作**） |
| p36 | 上影线试盘：放量上扬持股、转入下跌抛股、大涨长上影离场 | CONDITIONAL | 与 ce05/p19 影线簇重叠；并入 `deception-defense` A2 |
| p37 | 消息位置校验：股价已大幅拉高八成是配合出货的假消息 | **GO** | 原话+actionable(消息位置校验)；入 `deception-defense` A2（散布假消息仅识别防范） |
| p38 | 成交量骗术识别与短庄快进快出（放巨量涨停十之八九出货） | **GO** | 原话+actionable(识别对倒放量)；入 `deception-defense` A2（对倒放量/涨停撤单**仅识别防范、绝不作为操作**） |
| p39 | 发现主力 9 特征 + 地量 4 阶段进场清单 | **GO** | 原话+清单+actionable；入 `follow-playbook`(router) A2（事后图例，非统计验证） |
| p40 | 操盘破绽 7 条：破绽出现之时即买卖时机 | **GO** | 原话+清单+与 f21 重心呼应；入 `follow-playbook`(router) A2 |
| p41 | 强庄股筛选与跟进清单（榜单前20、低价区、均线黏合发散） | **GO** | 原话+清单；入 `follow-playbook`(router) A2（2013 软件史料，不可平移可转债） |
| p42 | 突然放量四情形应对 + 对敲甄别 10 法 | **GO** | 原话+清单+actionable(对敲甄别)；入 `follow-playbook`(router) A2（对敲**仅识别防范**） |
| p43 | 突然缩量应对：缩量空涨非坏事、放巨量后缩量阴跌警觉 | **GO** | 原话+actionable(regime-change 重估)；入 `follow-playbook`(router) A2 |
| p44 | 涨停股卖出/出局清单（3日不涨、5日线走平、回调1%） | **GO** | 原话+清单+actionable；入 `exit-discipline` A2（卖出触发器，非做空） |
| p45 | 突然跌停：放量打开跌停即买入机会，介入须分批增量 | **GO** | 原话+actionable(分批增量)；入 `follow-playbook`(router) A2（分批为**合规可执行**动作） |
| p46 | 特殊开盘/收盘应对：周五尾盘拉高不贸然介入 | CONDITIONAL | 与 p02/ce02 特殊时段簇重叠；并入 `follow-playbook`(router) A2（控制开收盘价仅识别防范） |
| p47 | 长/中线庄策略：经济周期初介入、捂股三五年、仓位 60%–80% | CONDITIONAL | 与 f19 分类簇重叠 + 旧生态语境；并入 `actor-typology`(router) A2 |
| p48 | 弃庄/止损/解套总清单（10%–25%/30%–45%/50%/70%–80% 阈值） | **GO** | 原话+清单+actionable(鳄鱼法则止损/不补仓)；簇⑤入 `exit-discipline` A2（止损为卖出，非做空） |

### 2.4 Glossary（g01–g25）→ 全部 **NO**（`status: reference`，术语定义卡，不晋级、不进 `rejected/`、不失联）

| id | 术语 | verdict | 一句话理由（并入去向 / 段） |
|----|------|---------|---------------------------|
| g01 | 主力 / 庄家 | **NO** | 定义卡；并入 `zhuli-intent-inference` R（意图性归因的「待验证假设」，见 ce34） |
| g02 | 坐庄 / 控盘 | **NO** | 定义卡；并入 `zhuli-stage-model` R（「控盘 50%」为旧生态前提） |
| g03 | 换手率五态 | **NO** | 定义卡(簇①状态机)；并入 `zhuli-turnover-volume` R，B 段写死不可平移可转债 |
| g04 | 上压板（大单压盘） | **NO** | 定义卡；并入 `zhuli-orderbook-language` R（展示性挂单，识别防范） |
| g05 | 下托板（大单托盘） | **NO** | 定义卡；并入 `zhuli-orderbook-language` R |
| g06 | 夹板 | **NO** | 定义卡；并入 `zhuli-orderbook-language` R |
| g07 | 试盘 | **NO** | 定义卡；并入 `zhuli-stage-model` R（探测闭环 f11） |
| g08 | 洗盘 | **NO** | 定义卡；并入 `zhuli-washout-vs-distribution` R（事前区分度未验证） |
| g09 | 出货 / 派发 | **NO** | 定义卡；并入 `zhuli-washout-vs-distribution` R（跌破关键位才离场） |
| g10 | 建仓 / 吸筹 | **NO** | 定义卡；并入 `zhuli-stage-model` R |
| g11 | 对敲 / 对倒（含自买自卖、虚假申报） | **NO** | 定义卡 + **识别防范对象硬边界**；并入 `zhuli-deception-defense` B（新证券法下违法，绝不作为操作） |
| g12 | 多头陷阱 | **NO** | 定义卡 + 「做空为A股口语」消歧；并入 `zhuli-deception-defense` B |
| g13 | 空头陷阱 | **NO** | 定义卡 + 「做空为A股口语」消歧（最易误用词）；并入 `zhuli-deception-defense` B |
| g14 | 做空 / 诱空 / 逼空（A 股口语） | **NO** | **头号消歧卡**：≠融券/期货做空；主去向 `zhuli`(来源路由入口) B，作为**全局硬边界被所有 10 个模块引用**，强制加载、不得降级为动作 |
| g15 | 骗线 / 做影线 | **NO** | 定义卡；并入 `zhuli-deception-defense` R（「识别之后要怀疑」） |
| g16 | 地量 | **NO** | 定义卡；并入 `zhuli-turnover-volume` R（与 p06 观望看似冲突，须位置校准；不可平移可转债） |
| g17 | 重心（股价重心） | **NO** | 定义卡(净效果 vs 符号)；并入 `zhuli-intent-inference` I |
| g18 | 60 日线（60 日均线） | **NO** | 定义卡；并入 `zhuli-washout-vs-distribution` R（延迟判定 + 未经统计验证） |
| g19 | 筹码 / 控盘度（冬眠筹码） | **NO** | 定义卡；并入 `zhuli-stage-model` I（旧庄股结构语言） |
| g20 | 破绽（操盘破绽） | **NO** | 定义卡；并入 `zhuli-follow-playbook` R（事后图例，非统计信号） |
| g21 | 短庄 / 中线庄 / 长庄 | **NO** | 定义卡；并入 `zhuli-actor-typology` R |
| g22 | 涨停板敢死队（闪电战术） | **NO** | 定义卡；并入 `zhuli-actor-typology` R（边拉边出，识别防范） |
| g23 | 强庄股 | **NO** | 定义卡；并入 `zhuli-follow-playbook` R（2013 软件史料 + 单一主力归因偏误） |
| g24 | 目标点位公式 | **NO** | 定义卡；并入 `zhuli-actor-typology` R（信心系数2无统计支撑） |
| g25 | 养套杀 / 见光死 | **NO** | 定义卡；并入 `zhuli-deception-defense` R，关联 `zhuli-exit-discipline` 弃庄触发器 |

> 理由总纲：本类是作者术语的「定义/辨析」资产，不具备独立意图与契约（判据1/2 不达标），**不进 `rejected/`**，按 1.6 硬规则降级为 `status: reference` 定义卡并入对应卡，不失联。**g14 为全局消歧硬边界，例外强制被所有模块 B 段引用**。

### 2.5 Cases（c01–c34）→ 全部 **NO**（`status: reference`，A1 段案例证据卡，不晋级、不失联）

| id | 案例 | verdict | 一句话理由（绑定去向） |
|----|------|---------|----------------------|
| c01 | 西藏发展·横盘震荡建仓 | **NO** | 案例卡(A1)；绑定 f06/p13/p14 → `zhuli-stage-model`（旧生态事后图例） |
| c02 | 特力A·温和上涨建仓 | **NO** | 案例卡(A1)；绑定 f06/p14 → `zhuli-stage-model` |
| c03 | 德赛电池·快速拉升建仓 | **NO** | 案例卡(A1)；绑定 f06/f08/p13 → `zhuli-stage-model` |
| c04 | 上海辅仁·底部连续跌停式建仓 | **NO** | 案例卡(A1)；绑定 f06/p15/f22 → `zhuli-stage-model`（跌停挂撤单仅识别防范） |
| c05 | 襄阳轴承·圆形底配地量结构 | **NO** | 案例卡(A1)；绑定 p16/p39/f20 → `zhuli-follow-playbook` |
| c06 | 莫高股份·矩形建仓与放量确认 | **NO** | 案例卡(A1)；绑定 p16/p23/f14 → `zhuli-stage-model` |
| c07 | 深纺织A·2009-10-12 高开低走试盘 | **NO** | 案例卡(A1)；绑定 f11/p18/f05 → `zhuli-stage-model` |
| c08 | 酒鬼酒·拉升前大幅低开高走试盘 | **NO** | 案例卡(A1)；绑定 f11/p18/f05 → `zhuli-stage-model` |
| c09 | 中青旅·尾盘大幅打压试盘 | **NO** | 案例卡(A1)；绑定 f11/p19/f20 → `zhuli-stage-model` |
| c10 | 深赤湾A·双针探底试盘后拉升 | **NO** | 案例卡(A1)；绑定 f11/p19/f20 → `zhuli-stage-model` |
| c11 | 万家乐·长下影洗盘加冲高回落试盘 | **NO** | 案例卡(A1)；绑定 f11/p36/f05 → `zhuli-stage-model` |
| c12 | 中信海直·2010-07-29 早盘冲高回落试盘 | **NO** | 案例卡(A1)；绑定 f08/f11/p10 → `zhuli-stage-model`（基线偏离） |
| c13 | 大唐发电·跌停式洗盘 | **NO** | 案例卡(A1)；绑定 f12/p15/p22 → `zhuli-washout-vs-distribution` |
| c14 | 梅花伞·上涨初期接连跌停洗盘 | **NO** | 案例卡(A1)；绑定 f12/p15/p22 → `zhuli-washout-vs-distribution` |
| c15 | 成飞集成·爆炒股短时平台洗盘 | **NO** | 案例卡(A1)；绑定 f12/p23/f05 → `zhuli-washout-vs-distribution` |
| c16 | 科学城·分时大幅震荡洗盘（易误读出货） | **NO** | 案例卡(A1)；绑定 f12/p12/p11 → `zhuli-washout-vs-distribution` |
| c17 | 太极集团·以 60 日线为依托不断拉升 | **NO** | 案例卡(A1)；绑定 p23/f12/p22 → `zhuli-washout-vs-distribution` |
| c18 | ST罗顿·海南国际旅游岛消息火箭式拉升 | **NO** | 案例卡(A1)；绑定 f17/p27/p26 → `zhuli-stage-model`（题材驱动） |
| c19 | 包钢稀土·多重利好接连拉升 | **NO** | 案例卡(A1)；绑定 f17/p26/f23 → `zhuli-stage-model` |
| c20 | 中金黄金·填权之后震荡下跌（失败） | **NO** | 案例卡(A1)；绑定 f17/p28/f23 → `zhuli-stage-model`（少见的「事后并不如愿」图例） |
| c21 | 维维股份·收购贵州醇连续 5 涨停 | **NO** | 案例卡(A1)；绑定 p27/p32/f17 → `zhuli-stage-model` |
| c22 | 中山公用·洗盘后连续缩量涨停 | **NO** | 案例卡(A1)；绑定 p28/p43/f13 → `zhuli-stage-model` |
| c23 | 深康佳A·高位宽幅震荡出货（看不见的手托价） | **NO** | 案例卡(A1)；绑定 p29/p30/f21 → `zhuli-washout-vs-distribution` |
| c24 | 浙江富润·涨停板反复打开完成派发 | **NO** | 案例卡(A1)；绑定 p32/p38/f14 → `zhuli-washout-vs-distribution` |
| c25 | 金岭矿业·除权后放量假填权出货（失败） | **NO** | 案例卡(A1)；绑定 p29/p38/f14/f17 → `zhuli-washout-vs-distribution`（可转债无对应物） |
| c26 | 金山开发·2011-04-01 高位放量大幅震荡出货 | **NO** | 案例卡(A1)；绑定 p29/p32/p33 → `zhuli-washout-vs-distribution` |
| c27 | 绿景控股·一字涨停尾盘跳水出货 | **NO** | 案例卡(A1)；绑定 p32/p46/f23 → `zhuli-washout-vs-distribution` |
| c28 | 凤凰股份·2011-06-01 午后拉高派发（失败） | **NO** | 案例卡(A1)；绑定 f08/f14/p10/p38 → `zhuli-deception-defense` |
| c29 | 旭飞投资·2011-11-11 尾盘拉涨停后大阴线（失败） | **NO** | 案例卡(A1)；绑定 f14/p46/p02 → `zhuli-deception-defense` |
| c30 | 中原环保·放量假突破诱多后加速下跌（失败） | **NO** | 案例卡(A1)；绑定 f14/f13/p38 → `zhuli-deception-defense` |
| c31 | 中瑞思创·高送转除权除息见光死（失败） | **NO** | 案例卡(A1)；绑定 f14/f17/f23/p37 → `zhuli-deception-defense` |
| c32 | 吉峰农机·高送转公告放量拉涨停诱多出货（失败） | **NO** | 案例卡(A1)；绑定 f14/f15/p37 → `zhuli-deception-defense` |
| c33 | 中山公用·空头陷阱急跌 50% 后连续涨停 450%（失败） | **NO** | 案例卡(A1)；绑定 f15/p35/f14 → `zhuli-deception-defense`（**做空为A股口语，随 g14 消歧**） |
| c34 | ST罗顿（罗顿发展）·题材两轮炒作见光死（失败） | **NO** | 案例卡(A1)；绑定 f23/f17/p26 → `zhuli-exit-discipline`（弃庄时机） |

> 理由总纲：案例是框架/原则的实证证据（判据2 不达标：无独立契约，只有叙事），经 `bound_to` 绑定到对应卡的 **A1 段**；且全为 **2009–2011 旧生态事后图例、无统计验证、无样本外检验**，判据1/4 过但按 1.6 硬规则不单独发现，降级 `status: reference`，不失联。

### 2.6 Counter-examples（ce01–ce36）

| id | 标题（简写） | verdict | 一句话理由（去向 / 段 / 识别-防范） |
|----|------|---------|-----------------------------------|
| ce01 | 骗线总纲·把刻意画出的图形与量当客观事实 | **GO** | 原话+头号反例；簇③锚点，入 `zhuli-deception-defense` B（**纯识别防范，零操作**） |
| ce02 | 尾盘拉升假进真出 | CONDITIONAL | 与 ce01/ce13/p46 尾盘簇重叠；并入 `zhuli-deception-defense` B |
| ce03 | 假突破·高位整理平台向上突破 | CONDITIONAL | 与 ce12/c30/p16 假突破簇重叠；并入 `zhuli-deception-defense` B |
| ce04 | 假填权·除权后放量小幅拉升诱多 | CONDITIONAL | 与 ce12/c25/p37 同簇；并入 `zhuli-deception-defense` B（可转债无对应物） |
| ce05 | 做影线·长上/下影线被机械解读 | CONDITIONAL | 与 p36/ce22 影线簇重叠；并入 `zhuli-deception-defense` B |
| ce06 | 多头陷阱·关口/指标/形态/量价配合/高送转诱多 | CONDITIONAL | 与 ce25/f15/g12 同簇；并入 `zhuli-deception-defense` B（「做多态势」为画出的表演） |
| ce07 | 空头陷阱·破位/连续阴跌/跳水诱使低位交筹 | **GO** | 原话+**含做空口语最易误用词**；入 `zhuli-deception-defense` B，强制随 g14 消歧（「大力做空」=打压卖出） |
| ce08 | 盘口委托单骗术·挂出来的大单不是真想成交 | CONDITIONAL | 与 ce22/f03/g04–g06 盘口簇重叠；并入 `zhuli-orderbook-language` B |
| ce09 | 虚假申报·不以成交为目的的频繁申报撤单 | **GO** | 原话+**识别防范对象**；入 `zhuli-orderbook-language` B（新证券法下违法，绝不作为操作） |
| ce10 | 对敲/对倒·不转移所有权的自买自卖 | **GO** | 原话+**识别防范对象**；入 `zhuli-deception-defense` B（新证券法下违法，绝不作为操作） |
| ce11 | 对倒放量拉升（成交量骗术一） | CONDITIONAL | 与 ce10/ce12/ce24 量骗术簇重叠；并入 `zhuli-deception-defense` B |
| ce12 | 久盘后突然放量突破（成交量骗术二） | CONDITIONAL | 与 ce03/c30/p38 同簇；并入 `zhuli-deception-defense` B |
| ce13 | 反弹制造假突破（成交量骗术三） | CONDITIONAL | 与 ce02/ce03 尾盘/突破簇重叠；并入 `zhuli-deception-defense` B |
| ce14 | 涨跌停板骗术·跌停板开盘引诱抄底盘 | CONDITIONAL | 与 p32/p45/ce26 跌停簇重叠；并入 `zhuli-deception-defense` B |
| ce15 | 盘口异动骗术·瞬间砸低又复原制造「捡便宜」 | CONDITIONAL | 与 ce08/p42 盘口异动簇重叠；并入 `zhuli-deception-defense` B |
| ce16 | 信息战术·把主力散布/分次发布的消息当利好 | CONDITIONAL | 与 f17/p37/ce06 信息战簇重叠；并入 `zhuli-deception-defense` B |
| ce17 | 折磨战术·长时间阴跌横盘磨走持股者 | CONDITIONAL | 与 f16/ce18 养套杀簇重叠；并入 `zhuli-deception-defense` B |
| ce18 | 养套杀 / 培养惯性思维的伪装 | CONDITIONAL | 与 f16/g25/ce17 同簇；并入 `zhuli-deception-defense` B |
| ce19 | 误判洗盘为出货·低位被吓出筹码 | **GO** | 原话+簇②核心误判；入 `zhuli-washout-vs-distribution` B（事前区分度未验证） |
| ce20 | 误判出货为洗盘·高位死守还抢反弹 | **GO** | 原话+与 ce19 对称；入 `zhuli-washout-vs-distribution` B |
| ce21 | 把对倒放量（短庄边拉边出）误读为主力建仓 | CONDITIONAL | 与 ce10/f13/p42 对倒簇重叠；并入 `zhuli-deception-defense` B |
| ce22 | 把上压板/大买单读成「主力在进货」 | CONDITIONAL | 与 ce08/f03/g04 盘口簇重叠；并入 `zhuli-orderbook-language` B |
| ce23 | 孤立看单一信号·忽略位置/量能连续性/大势 | **GO** | 原话+强跨域(多源交叉反面)；入 `zhuli-intent-inference` B |
| ce24 | 照搬经典量价理论（量增价涨才涨） | **GO** | 原话+与量柱体系立场冲突；入 `zhuli-turnover-volume` B（须交叉校验） |
| ce25 | 追高被套·被诱饵忘掉多头风险 | CONDITIONAL | 与 ce06/f15 多头陷阱簇重叠；并入 `zhuli-deception-defense` B |
| ce26 | 抢反弹/跌停抄底被套·不及时止损深套 | **GO** | 原话+actionable(止损)；入 `zhuli-exit-discipline` B（「不卖不亏」自欺） |
| ce27 | 把真实空头市场/趋势反转当成「空头陷阱」或洗盘 | CONDITIONAL | 与 ce07 互补、**含做空口语**；并入 `zhuli-deception-defense` B（随 g14 消歧） |
| ce28 | 满仓/重仓、无资金管理 | **GO** | 原话+强跨域(失去可逆性)；入 `zhuli-exit-discipline` B（对应 f22 中间仓位） |
| ce29 | 亏损后补仓/加仓摊低成本（违逆鳄鱼法则） | **GO** | 原话+硬纪律；入 `zhuli-exit-discipline` B（**绝不补仓摊平**为合规可执行禁令） |
| ce30 | 不止损 /「不卖不亏」式自欺 | **GO** | 原话+「止损是唯一保命绝招」；入 `zhuli-exit-discipline` B |
| ce31 | 贪婪·死顶硬扛、抱仓过久、不设盈利保护 | **GO** | 原话+强跨域(人性弱点)；入 `zhuli-exit-discipline` B |
| ce32 | 恐惧·暴跌中低位交出筹码 | **GO** | 原话+强跨域(与贪婪对称)；入 `zhuli-exit-discipline` B |
| ce33 | 未预设弃庄/离场触发器（见光死、全民疯狂、政策转向） | **GO** | 原话+actionable(预设退出)；入 `zhuli-exit-discipline` B |
| ce34 | 跟庄失败 /「主力不是万能的」被后文遗忘 | **GO** | 原话（第 532 行实证）+幸存者偏差；入 `zhuli-market-regime-filter` B（忽略无单一主力解释） |
| ce35 | 作者自相矛盾·「信号可任意伪造」与「可稳定反推」不能同真 | **GO** | 原话+全书最强反对意见；入 `zhuli`(来源路由入口) B，作为**全局不可证伪边界被所有模块引用** |
| ce36 | 时代/合规失效·把 2013 旧生态手法当成当下事实 | **GO** | 原话+**全局护栏总卡**；入 `zhuli`(来源路由入口) B（新证券法违法清单 / 可转债不可平移 / 做空口语），被所有模块引用 |

---

## 三、未晋级（NO）汇总段

- **Glossary g01–g25（25 条）**：全部 NO。降级为**术语定义卡**（`status: reference`），并入对应框架卡 R/I（g11 对倒、g12/g13/g14 做空口语归 B 段）。**g14 例外**：作为全局消歧硬边界被所有模块 B 段强制引用。不失联。
- **Cases c01–c34（34 条）**：全部 NO。降级为**案例证据卡（A1 段）**（`status: reference`），经 `bound_to` 绑定，统一标注「2009–2011 旧生态事后图例、非统计验证」。不失联。
- **Frameworks 中 CONDITIONAL（4 条）**：f07/f15/f19/f24，折叠进 `turnover-volume` / `deception-defense` / `actor-typology` 卡，不单列。
- **Principles 中 CONDITIONAL（30 条）**：换手率簇 p04–p09/p13、盘口时段簇 p01/p02/p10–p12、建仓试盘簇 p14/p16–p21/p27、洗盘出货阈值簇 p20/p22–p25/p29/p31/p33、影线簇 p36、特殊开收盘 p46、长中线策略 p47，折叠进对应 canonical 卡，不单列。
- **Counter-examples 中 CONDITIONAL（18 条）**：ce02–ce06/ce08/ce11–ce18/ce21/ce22/ce25/ce27，折叠进 `deception-defense` / `orderbook-language` 卡 B 段（与相邻反例或正面卡重叠），不单列。

> 按 stage 1.6 硬规则：**未晋级候选不进 `rejected/`**，而是降级为 `status: reference` 能力卡/术语卡/案例卡，保留在来源路由入口（`zhuli`）内，不会失联。`rejected/` 仅留给「知识验证未过」者 —— 本次 V1 全过、V2 全量命中无编造，故 **`rejected/` 为空**。

---

## 四、晋级统计（供主代理）

| type | 总数 | GO | CONDITIONAL | NO |
|------|-----|----|-----------|----|
| frameworks | 24 | 20 | 4 | 0 |
| principles | 48 | 18 | 30 | 0 |
| glossary | 25 | 0 | 0 | 25 |
| cases | 34 | 0 | 0 | 34 |
| counter-examples | 36 | 18 | 18 | 0 |
| **合计** | **167** | **56** | **52** | **59** |

- 经 2.1 合并后，**实际新增 canonical 能力卡 = 10 张**（8 张 promoted + 2 张 router 卡）+ 1 个来源路由入口 `zhuli`，而非 167：intent-inference、orderbook-language、turnover-volume、washout-vs-distribution、deception-defense、stage-model、exit-discipline、market-regime-filter、follow-playbook(router)、actor-typology(router)。
- 通过率（GO + CONDITIONAL / 总数）= 108 / 167 ≈ **64.7%**，与同批 085 的 67.1%、083 的 67% 一致，符合方法论「30–80%」健康区间。
- 降级率 59 / 167 ≈ **35.3%**，全部为术语卡(25) + 案例卡(34)，均 `status: reference` 保留、**无失联**。

---

## 五、推荐进入 dist/pack 的 Top 模块（zhuli-*）

按「最少可发现入口覆盖最多高价值意图」+ 软预算 **8**（1 来源路由入口 + 8 个 promoted skill）：

| 优先级 | 模块(skill pack) | 吸纳 canonical 卡 / 主题 | 段(R/I/A1/A2/E/B) | 输出契约 class | 晋级定位 |
|-------|------------------|--------------------------|--------------------|----------------|----------|
| 1 | `zhuli-intent-inference` | 簇③锚点：痕迹反推意图/信息四分/反事实推理/基线偏离/净效果 vs 符号/多维交叉/等确认 | R·I·A1·A2·B | 识别-推理（纯方法论，零操作） | **promoted** |
| 2 | `zhuli-orderbook-language` | 盘口委托单语言/上压板下托板夹板/证据分级/开盘尾盘时段/支撑阻力 | R·I·A1·A2·B | 识别-防范（挂撤单/虚假申报仅识别） | **promoted** |
| 3 | `zhuli-turnover-volume` | 簇①：换手率五态/量价三态/周换算/地量/量能连续性证伪/量价教条 | R·I·A1·A2·B | 识别-防范（对倒做量仅识别） | **promoted** |
| 4 | `zhuli-washout-vs-distribution` | 簇②前半：洗盘vs出货五维/60日线延迟判定/出货特征/离场触发器 | R·I·A1·A2·B | 识别-防范 + 合规卖出 | **promoted** |
| 5 | `zhuli-deception-defense` | 簇②③共享：骗线四式/成交量骗术/多空陷阱/养套杀/信息战术/十八种反例 | R·I·A1·A2·B | 识别-防范（**零可执行操作**） | **promoted** |
| 6 | `zhuli-stage-model` | 簇④：坐庄十阶段/五段三段式/建仓试盘洗盘拉升出货各阶段特征 | R·I·A1·A2·B | 识别-推理（事后叙事训练） | **promoted** |
| 7 | `zhuli-exit-discipline` | 簇⑤：弃庄/离场触发器/止损鳄鱼法则/中间仓位分批/克服贪婪恐惧 | R·I·A1·A2·E·B | 合规可执行动作（唯一主动作模块） | **promoted** |
| 8 | `zhuli-market-regime-filter` | 大盘环境过滤/弱市不介入/逆市压测/主力不是万能/beta vs alpha | R·I·A1·A2·B | 识别-推理 + 合规过滤 | **promoted** |
| 9（超预算） | `zhuli-follow-playbook` | 跟庄实战清单：发现主力9特征/地量4阶段/破绽7条/强庄股/突然放量缩量涨停跌停 | R·I·A1·A2·B | 识别-防范 + 模式识别训练 | **served_by(router 卡)** |
| —（超预算） | `zhuli-actor-typology` | 主力类型/周期分类/短中长庄/目标点位公式/长中线策略 | R·I·A1·A2·B | 识别-推理 + 估算谦逊 | **served_by(router 卡)** |
| — | `zhuli`（来源路由入口） | 全部术语卡/案例卡/全局边界卡(g14 消歧·ce35 不可证伪·ce36 时效合规)兜底 | R·I·A1·A2·E·B | router | **router** |

> 说明：预算内 8 个 promoted skill 恰好覆盖 5 个高重叠簇经去重后的 8 张 canonical 卡（簇①1 + 簇②1 + 簇③2 + 簇④1 + 簇⑤1 + 盘口1 + 环境1 = 8，其中簇②/簇③共享 deception-defense 已在计数内消去重复）。跟庄实战手册与主力类型分类作为 router 卡保留（split-on-evidence 后可升级为第 9/10 个 promoted）。**所有 GO/CONDITIONAL 条目在 `destinations.json` 中逐一映射，NO 条目以 `status: reference` 映射，无遗漏、无失联**。

---

## 六、识别类 vs 可执行类的晋级分界（落地说明）★

用户要求「所有『识别类』条目只能作为防范对象晋级，绝不可晋级为可执行操作」。本批通过 **4 层机制**把这条护栏从文字落成可机读约束：

1. **输出契约分类（module.output_contract + class）**：`destinations.json` 每个模块带 `class` 与 `output_contract` 两个字段，把 10 张卡切成三档——
   - `识别-防范`（orderbook-language / turnover-volume / deception-defense / follow-playbook）：输出只能是「信号形态 + 反事实证伪 + 位置校准 + 风险提示 + 不模仿」；
   - `识别-推理`（intent-inference / stage-model / market-regime-filter / actor-typology）：输出「怎么读、怎么证伪、怎么交叉校验」的跨域方法论，**不产生任何交易动作**；
   - `合规可执行动作`（exit-discipline 为主，washout-distribution 的卖出触发器为辅）：动作白名单 = **卖出离场 / 不买 / 轻仓 / 中间仓位 / 分批 / 观望 / 等确认 / 预设止损**。
2. **每个模块强制携带 `guardrails` 三键**（`destinations.json` 每个 module 逐一带上）：`compliance`（2013 旧生态 + 新证券法 2020 违法清单 + 仅作防范对象绝不操作）、`user_constraint`（A 股单边 / 不做空不期货 / 可转债不可平移）、`g14_disambiguation`（做空=A股口语≠融券期货）。**任何模块生成动作前必须先过这三键**。
3. **判据4 的重新解释**：本批五判据第 4 条「actionable」对识别类一律记为 **「actionable 于识别与防范」**，并在每条 verdict 理由里显式标注「仅识别防范 / 绝不作为操作」（见 p15/p38/p42、ce09/ce10、g11 等）。因此「晋级」对识别类只意味着「做成一张可读的防范卡」，**不意味着「做成可照做的动作」**。
4. **动作黑名单硬拦截**：涉及对倒/对敲/虚假申报/连续交易/约定交易/自买自卖/多账户分仓/散布消息/涨停板撤单/挂撤单做量、以及「做空/诱空/逼空/反手做空/融券/期货/双向/杠杆」的条目，B 段一律写死禁作动作；g14 消歧作为全局卡被所有模块引用，**从词源上切断下游把「做空」翻译成融券/期货做空的可能**。

**分界结果一览**：
- 可晋级为「可执行动作」的只有 A 股单边做多框架内、散户对自身的合规动作：预设退出触发器、跌破关键位卖出、止损不补仓、中间仓位分批、弱市不介入、等确认再进场。全部集中在 `zhuli-exit-discipline`（+ `washout-distribution` 卖出触发器、`intent-inference`/`follow-playbook` 的等待/空仓动作）。
- 其余 6 个 promoted 模块 + 2 个 router 卡全部是「识别-防范 / 识别-推理」，**零主力手法操作输出**。
- 用户约束（不做空/不期货/可转债不可平移）不是靠「不提取」实现，而是靠**每个模块 B 段 + g14 全局卡 + 动作白名单**共同实现，确保下游 skill 即便被单独触发也不会生成禁用动作。

---

## 七、需主代理决策的分歧点 / 标注项

1. **簇② 与簇③ 是否共享 `deception-defense`**：本批按 1.6 硬规则（输出契约不同不强行合并）把「洗盘vs出货判别」与「骗术防范」拆成 2 张 promoted，但 f14 / ce19–ce27 在两簇间交叉。已在 `destinations.json` 用 `canonical_card` + `also_read` 语义（note 标注）保留交叉链接，不重复建卡。若主代理希望省出 1 个入口，可把 `market-regime-filter`（仅 f18/p26/ce34 三条 GO）降为 router 卡、把 `follow-playbook` 提升为第 8 个 promoted —— 本批按用户建议的 8 模块名保持现状。
2. **V2 全量命中（100%）是否直接采信**：本批引文为 OCR 原貌照抄、去空白后 399/399 逐字命中，无一条 needs_review，与 085 的「6 条修 quote + 2 条 needs_review」形成对比。建议阶段 2 保留 OCR 原貌错字（为可定位故不修订），仅在展示层做「校勘注」。
3. **`rejected/` 为空的确认**：因 V1 全过、V2 无编造，按 1.6 硬规则所有 NO 均为 `status: reference`（术语卡/案例卡），不进入 rejected/。请阶段 2 不要把这些卡当「淘汰垃圾」清理 —— 它们是 A1/B 段证据与消歧来源，失联会破坏下游边界。
4. **g14 全局化**：本批把 g14 主去向设为来源路由入口 `zhuli`（而非某张 promoted 卡），并要求所有 10 个模块 B 段引用。请阶段 2 在生成各 skill 的 B 段时**逐一注入**该消歧，不要只在路由入口写一次。
