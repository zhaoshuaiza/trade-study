# 《慢即是快：一个投资者20年的思考与实践（三年一倍）》阶段 1.5 + 1.6 验证与晋级清单

> 书 slug：`085-manzaikuai` · 来源：`source.txt`（全书 6073 行 / 403 页，带 `===== 第N页 =====` 标记，**固定列宽硬换行**文本）
> 验证者：cangjie stage 1.5（三重验证）+ stage 1.6（五判据晋级门）执行器
> 候选池：frameworks(f01–f32) / principles(p01–p45，含 11 条 checklist) / glossary(g01–g27) / cases(c01–c30) / counter-examples(ce01–ce39)，共 **173** 条
> 格式对齐：`books/083-jinrongxinlixue/verified.md`、`destinations.json`（同批已完成书，直接对齐其结构与命名风格）
> 段归属：本批按 stage 2 的 **R / I / A1 / A2 / E / B 六段**（R 原文 · I 自述 · A1 书中案例 · A2 触发与操作规则 · E 可执行步骤 · B 边界）标注；样板 083 用简化五段 R/I/A/E/B，本批按用户要求把 A 拆为 A1/A2，其余结构不变。

---

## 一、三重验证结论（V1 / V2 / V3）

### V1 自洽校验（字段完整 / 引用闭合 / id 连续无重）
- **字段完整**：frameworks / principles 含 `id/title/type/source_chapter/source_quote/summary/tags`；cases 含 `bound_to/outcome`；counter-examples 含 `failure_mode/mechanism/warning_signs/bound_to/source_quote/summary/tags`。全部齐整。
- **glossary 结构差异（非缺字段）**：本批 glossary 用 `term/author_definition/key_distinction/why_it_matters/tags`（引文落在 `author_definition`，并附页码），与样板 083 的 `source_quote/summary` 结构不同；但 27 条内部一致、无空字段，判为**自洽**。V2 溯源对 glossary 取 `author_definition`。
- **source_quote 闭合**：全部 YAML `|` 块闭合正常；cases / counter-examples / glossary 的 `"…"` 成对闭合；未发现截断或未闭合引号。
- **id 连续无重**：f01–f32(32) / p01–p45(45，checklist 为 p04/p05/p06/p15/p16/p17/p18/p19/p22/p33/p34 共 11 条) / c01–c30(30) / ce01–ce39(39) / g01–g27(27) = **173**，各类连续、无重复、无缺号。
- **V1 结论：173 条全部通过**（无需淘汰）。登记 2 处轻微标注项（见下）。
- **标注项①（引用标签漂移）**：`c08` 的 `bound_to` 写作「p01 七亏二平一赢的残酷性」，而 p01 实际标题为「一般不要踏入股市这个人博弈的市场」（编号 p01 正确、文字标签不符）。不影响绑定有效性，建议阶段 2 同步 bound_to 文本。
- **标注项②（字段结构差异）**：见上 glossary 条；不影响 V2/V3 判定。

### V2 溯源校验（≥30% 抽样 grep 原文）
采用双层核验，覆盖强度远超 ≥30% 要求：
1. **全文 173 条逐条归一化核验（100% 覆盖）**：因 `source.txt` 为固定列宽硬换行（例：第 888 行「…主人就是内在价值。我们价」被截断，接下行），完整长引文用 `grep -F` 必然 MISSING。故先对原文与引文做「去换行 / 去标点 / 去引号」归一化，再按句切分逐句做 `grep -F` 语义匹配，共 **484 个句子探针**。
2. **`grep -F` 逐字抽样交叉验证 45 条短探针**（跨全部 5 类），另对疑点项做定向核查。

- **结果**：**150 / 173 条全句命中**；23 条存在未命中句，**全部复核确认原文确实存在、未断章取义**，命中探针 452 / 484（**93.4%**）。未命中原因分三类：
  - **跨行断行 / 格式重排**（窗口相似度 0.38–1.00）：如 f05/f12/f15/f22/f24/p24/p35/p41/c10/c21/c27/c30/ce26/ce37/c08/c12/c15，「仓位控制问题」「唯一需要担心的风险」「非常微弱的声音」等短探针 `grep -F` 均命中，长串 MISS 仅因硬换行切断或抽取器把不相邻句拼成一行。
  - **抽取器局部概括 / 序号重排**：f30（「暗示机会…积极做多」原文有「积极做多」「暂时退出」，但「暗示机会」为改写）、c09（五次破 11 倍 PE 的图表被整理成 `(1)…(2)…` 文字）、c23（「保守型80/20…」为归纳简写，原文为「80%的核心资产和20%的卫星资产」）。
  - **异体字 / 漏字**：p12「来説」→原文「来说」(`grep -F`：「来説」0、「来说」44)；c08「上海证券交所」漏「易」字（原文「上海证券交易所」）。
- **无编造、无断章取义**：逐句均能在标注的同章节原文定位；带省略号拼接的引文（f11 双腰斩、c12 泡沫史、g08 三年一倍）前后句各自命中，且均出自所标章节。
- **需修订 6 条（标 CONDITIONAL-修 quote，均可修）**：`p12`（説→说）、`c08`（补「易」）、`f27`（生钱/保本升值比例表述）、`f30`（概括词回改原文）、`c09`（序号列表回改图表原文）、`c23`（比例简写回改 p35 原文）。另 `p19/p33/p35/p37` 有短句措辞漂移，一并列入修 quote 清单。
- **标 `status: needs_review` 2 条**：`f30`、`c23` —— 引文为抽取器概括改写、原文无完全逐字对应，核心词真实但「引用」形态不合规，需主代理定夺（见第六节分歧点①）。
- **V2 结论：通过**（抽样无编造；6 条 CONDITIONAL 修 quote，2 条 needs_review）。

### V3 跨域校验（是否真可迁移到投资以外场景）
- **强跨域（可迁移到组织 / 舆情 / 职业 / 个人决策 / 复杂系统）**：
  - frameworks：f01/f02/f04/f05/f06/f08/f09/f12/f13/f14/f15/f16/f18/f19/f20/f21/f23/f24/f25/f28/f29/f31/f32（23 条），f07/f10/f22/f26/f30 为中等可迁移。
  - principles：p02/p20/p21/p22/p24/p25/p26/p28/p32/p37/p38/p40/p43/p44（14 条）。
  - counter-examples：ce04/ce05/ce10/ce11/ce12/ce19/ce21/ce22/ce23/ce24/ce25/ce26/ce30/ce32–ce36/ce38/ce39（约 21 条，人性弱点 / 认知误区 / 过度自信 / 从众 / 反事实思维类）。
- **弱跨域（交易语境限定）**：
  - frameworks：f03（戴维斯双击时机）、f11（双腰斩跌幅刻度）、f17（指数波段操作）、f27（家庭资产分层，半通用）。
  - principles：p01/p04/p05/p06/p07/p08/p09/p10/p11/p14/p15/p16/p17/p18/p19/p23/p27/p30/p31/p33/p34/p35/p36/p39/p41/p42/p45（红线比例 / 估值分位 / 技术指标 / 基金筛选 / 排雷清单等**纯技术规则**）。
  - glossary **全类 27 条**（作者私有术语定义/辨析）、cases **全类 30 条**（个股/历史/统计实证）。
  - counter-examples：ce01–ce03/ce06–ce09/ce13–ce18/ce20/ce27/ce28/ce31/ce37（融资爆仓 / 单行业红线 / 技术唯上 / 注册制退市等交易细则）。
- **V3 结论**：框架层约 3/4 具备真实跨域价值；原则层约 1/3 强跨域、其余为交易语境资产；反例层「人性/认知」类强跨域、「操作细则」类交易限定；**术语与案例两类整体为交易语境限定，标 `status: reference` 降级保留**。

---

## 二、五判据晋级门（GO / CONDITIONAL / NO）

> 判据1 源自原话原意 · 判据2 原子化可独立 · 判据3 不重复(重复则合并) · 判据4 对交易者 actionable · 判据5 不矛盾
> **GO** = 五判据基本全过，建议进入独立 skill / 核心卡；**CONDITIONAL** = 有价值但须合并或仅作子卡/边界卡；**NO** = 不晋级为独立 skill（降级为术语卡/案例卡，`status: reference`，保留为 router 卡，不失联）。

### 2.1 去重与合并总纲（先读这段，避免重复计数）

本批 173 条经合并后收敛为 **10 张 canonical 卡**（8 张 promoted + 2 张 router 卡），而非 173 个 skill。用户点名的 5 个高重叠簇处理如下：

| 簇 | 成员 | 合并建议 | canonical 卡数 |
|----|------|----------|----------------|
| **① 均值回归/遛狗/双腰斩/情绪钟摆** | f01/f09/f10/f11 + g01/g07/g21 + p28/p20 + c09/c15/c29 + ce21(交叉) | **合并为 1 张** `manzai-mean-reversion`（promoted）。g01 双腰斩「并非铁律、对个股无效」与 g07「主人错了」入 B 段；f07 情绪钟摆与簇②交叉，归 P2 但保留到 P1 的 `also_read` 链接 | **1** |
| **② 周期/这次不一样/逆向** | f06/f07/f08/f20/f29/f30 + g02/g22/g26 + p11/p22 + c10/c12/c30 + ce21 | **拆为 2 张**：`manzai-cycle-thinking`（周期位置/这次不一样/大周期/政策信号）+ `manzai-inverted-thinking`（逆向/第二层次/预期差/市场先生/羊群锚定）。二者输出契约不同（前者「判断周期位置」的状态识别，后者「与共识反向」的决策动作），按 1.6 硬规则不强行拼成一个模糊 Skill | **2** |
| **③ 杠杆仓位** | f24 + p07/p29/p30/p44 + ce01–ce10 + f04/f05/f15/f25/f26/f27 + p02/p08/p31/p32/p37 + g10/g14/g20/g23 | **拆为 2 张**：`manzai-risk-no-leverage`（绝对禁令/本金永久性损失/闲钱/承受力/排雷）+ `manzai-position-control`（仓位红线/凯利/分批建仓/分散集中/四笔钱/再平衡）。前者「不做什么」，后者「做多少」，意图与契约不同 | **2** |
| **④ 好公司好价格/戴维斯双击** | f02/f03/f16 + g11/g12/g13/g18 + p03/p14/p23 + f12/f13 + ce16/ce27/ce31 + p41/p42 | **拆为 2 张**：`manzai-davis-double`（市值=净利×PE/双击双杀/三年一倍公式）+ `manzai-quality-price`（三位一体/安全边际/ROE杜邦/波特五力）。前者「收益来源乘数分解与拐点识别」，后者「标的质地筛选三关」，输入/输出不同 | **2** |
| **⑤ 认知变现/耐心/知行合一** | f18/f23/f31 + g06 + ce23 + f14/f21/f28 + p22/p24/p25/p26/p38 + ce22/ce24/ce29 | **合并为 1 张** `manzai-patience-discipline`（promoted）。B 段吸纳 ce23 认知缺陷、ce22 股龄≠能力、ce24 错误归因 | **1** |

- **簇外补充簇**（不新增 promoted，折叠进 router 卡）：
  1. **估值操作手册簇**：g03/g04/g05/g19/g24 + p04/p05/p06/p08/p09/p10/p27/p34 + f17/f26 + ce11/ce13/ce14/ce17/ce19/ce20 → `manzai-value-toolkit`（**router 卡**）。
  2. **选股排雷/防骗簇**：f12/f13 + p14/p15/p16/p17/p18/p33/p41/p42/p43/p45 + g16/g17 + ce15/ce18/ce25/ce26/ce28/ce31 → `manzai-screening-playbook`（**router 卡**）。
  3. **六维共振/宏观信号簇**：f04/f05→`manzai-position-control`；f30/p11/c16/c28→`manzai-cycle-thinking`。
- **案例 c01–c30**：全部作为 A1 段证据卡，按 `bound_to` 绑定到对应框架/原则所在卡，**不晋级为独立 skill**。
- **术语 g01–g27**：全部作为定义卡，`status: reference`，并入对应框架卡的 R/I（g14/g27 一词两义归 B 段），**不晋级为独立 skill**。
- **checklist 11 条**：p04/p05/p15/p22 为高价值独立清单给 GO；其余与同构清单合并为 CONDITIONAL。

---

### 2.2 Frameworks（f01–f32）

| id | 标题 | verdict | 一句话理由（五判据） |
|----|------|---------|----------------------|
| f01 | 遛狗理论 | **GO** | 原话+原子+强跨域(表象vs本质)；簇①锚点，合并 g07/g21/p28 |
| f02 | 市值 = 净利润 × PE | **GO** | 原话+原子+可跨域(收益拆两乘数)；簇④公式基础，入 davis-double |
| f03 | 戴维斯双击 | **GO** | 原话+原子+乘数效应独特；合并 g11/g12/ce27，入 davis-double |
| f04 | 六维共振 | **GO** | 原话+原子+强跨域(独立证据清单)；入 position-control I |
| f05 | 资产配置权益仓位模型 | **GO** | 原话+原子+可跨域(打分→阈值触发行动)；入 position-control I |
| f06 | 周期思维 | **GO** | 原话+原子+强跨域(万物兴衰)；簇②锚点，合并 g22 |
| f07 | 情绪周期钟摆 | CONDITIONAL | 真实但属周期/均值回归子论点，并入 cycle-thinking，与 P1 交叉链接 |
| f08 | 逆向投资与第二层次思维 | **GO** | 原话+原子+反直觉；簇②，独立 inverted-thinking 卡 |
| f09 | 均值回归 | **GO** | 原话+原子+强跨域(方向确定/时间随机)；簇①核心，合并 g21 |
| f10 | 低买高卖第一性原理 | CONDITIONAL | 与 f01/f09/f16 价值回归重复，并入 mean-reversion 卡 |
| f11 | 双腰斩理论 | CONDITIONAL | 专属抄底判据且作者自划「并非铁律」，并入 mean-reversion 卡 B 段(含 g01) |
| f12 | ROE 杜邦三因子 | **GO** | 原话+原子+强跨域(利润来源三路径)；入 quality-price I |
| f13 | 波特五力 | **GO** | 原话+原子+强跨域(赛道/职业选择)；入 quality-price I |
| f14 | 鳄鱼潜伏模型 | **GO** | 原话+原子+可跨域(等待为主动策略)；簇⑤，入 patience-discipline |
| f15 | 凯利公式 | **GO** | 原话+原子+强跨域(概率×赔率下注)；入 position-control I |
| f16 | 好行业+好公司+好价格 | **GO** | 原话+原子+强跨域(三关放行)；簇④，独立 quality-price 卡 |
| f17 | 大周期波段操作 | CONDITIONAL | 操作闭环非独立框架，并入 value-toolkit(router) E 段 |
| f18 | 耐心持有/坚持不动 | **GO** | 原话+原子+反直觉(不操作为默认)；簇⑤核心 |
| f19 | 市场先生 | **GO** | 原话+原子+强跨域(外部评价vs真实价值)；入 inverted-thinking |
| f20 | 这次不一样=每次都一样 | **GO** | 原话+原子+反直觉；簇②，入 cycle-thinking |
| f21 | 延迟满足 | **GO** | 原话+原子+强跨域(三年长轴)；簇⑤ |
| f22 | 投资就是投预期差 | CONDITIONAL | 与 f08 第二层次/g15 重叠，并入 inverted-thinking 卡 |
| f23 | 认知变现 | **GO** | 原话+原子+强跨域(收益上限由认知决定)；簇⑤核心，合并 g06/ce23 |
| f24 | 永远不要上杠杆 | **GO** | 原话+原子+反直觉(绝对禁令)；簇③核心，独立 risk-no-leverage 卡 |
| f25 | 合理分散、适度集中 | **GO** | 原话+原子+可跨域(防错vs抓机会)；入 position-control |
| f26 | 股债动态再平衡 | CONDITIONAL | 操作型策略，并入 position-control 卡 E 段 |
| f27 | 标准普尔四笔钱 | CONDITIONAL | 操作分层细则 + V2 需修 quote，并入 position-control A2 |
| f28 | 二八定律/少即是多 | **GO** | 原话+原子+强跨域(聚焦少数关键)；簇⑤，合并 p25 |
| f29 | 用大周期思维 | **GO** | 原话+原子+强跨域(拉长尺度滤噪音)；簇②，入 cycle-thinking |
| f30 | 跟政策走 + 资产比价 | CONDITIONAL | V2 引文为概括改写(needs_review)，并入 cycle-thinking，待主代理定夺 |
| f31 | 知行合一与纪律执行 | **GO** | 原话+原子+强跨域(体系对抗人性)；簇⑤核心 |
| f32 | 本金永久性损失是唯一该担心的风险 | **GO** | 原话+原子+强跨域(可逆vs不可逆)；簇③，入 risk-no-leverage |

### 2.3 Principles（p01–p45）

| id | 标题 | verdict | 一句话理由 |
|----|------|---------|-----------|
| p01 | 一般不要踏入股市这个人博弈的市场 | CONDITIONAL | 原话+全书两次复现，但属入场闸门/心态注脚，并入 risk-no-leverage |
| p02 | 投资一定要用闲钱 | **GO** | 原话+原子+actionable(资金属性前置检查)；入 risk-no-leverage R |
| p03 | 任何好公司都不值得不计成本买入 | **GO** | 原话+全书复现≥3+actionable；簇④，入 quality-price A2 |
| p04 | 好价格/好买点四种情形(checklist) | **GO** | 原话+清单+actionable；入 value-toolkit A2 |
| p05 | 股票卖出三原则(checklist) | **GO** | 原话+清单+actionable；入 value-toolkit A2 |
| p06 | 基金卖出三原则(checklist) | CONDITIONAL | 与 p05 同构(仅替换一条)，并入 value-toolkit A2，不单列 |
| p07 | 仓位红线 单行业≤30%/单只≤20% | **GO** | 原话+硬红线+actionable；簇③，入 position-control A2 |
| p08 | 分批建仓四法 | **GO** | 原话+原子+actionable；入 position-control E |
| p09 | 先看大周期再用小周期找买卖点 | CONDITIONAL | 技术操作细则，并入 value-toolkit A2 |
| p10 | 小周期指标不准、不必看 | CONDITIONAL | 与 f29/g09 重复，并入 value-toolkit A2 |
| p11 | 政策提示风险必须听话撤退 | **GO** | 原话+actionable(政策开关)；簇②，入 cycle-thinking A2 |
| p12 | 没有必要天天看盘 | CONDITIONAL | 原话但偏行为细则 + V2 异体字「説→说」需修，并入 patience-discipline |
| p13 | 扛不住一天波动就别炒股 | CONDITIONAL | 与 p12/ce11 重复，并入 patience-discipline B |
| p14 | ROE<15~20% 一律不看 | **GO** | 原话+全书复现≥3+排除法；入 screening-playbook A2 |
| p15 | 基本面排雷排除清单(checklist) | **GO** | 原话+清单+actionable；入 screening-playbook A2 |
| p16 | 防范局部风险三措施(checklist) | CONDITIONAL | 与 f04/f25 重复，并入 position-control A2 |
| p17 | 系统性风险两条应对(checklist) | CONDITIONAL | 与 f25/ce08 重复，并入 position-control A2 |
| p18 | 防范股市诈骗清单(checklist) | CONDITIONAL | 与 p45/ce25/ce26 重复，并入 screening-playbook B |
| p19 | 五种本金永久性损失情形(checklist) | **GO** | 原话+清单+actionable；簇③，入 risk-no-leverage (V2 需修 quote) |
| p20 | 买入前自问「下跌后敢加仓吗」 | **GO** | 原话+自检+actionable；入 inverted-thinking A2 |
| p21 | 众人夺路而逃，不挡路不跟随 | **GO** | 原话+行动准则；入 inverted-thinking A2 |
| p22 | 必须克服的六种人性弱点(checklist) | **GO** | 原话+清单+强跨域；簇⑤，入 patience-discipline B |
| p23 | 三年一倍实操法则(PE<30/增速>30%) | **GO** | 原话+可量化+actionable；簇④，入 davis-double A2 |
| p24 | 看得准、下重手、拿得住 | **GO** | 原话+口诀+actionable；簇⑤，入 patience-discipline A2 |
| p25 | 只搞懂少数龙头，弱水三千只取一瓢 | **GO** | 原话+全书复现≥3；与 f28 合并，入 patience-discipline |
| p26 | 找到适合自己的策略然后重复 | **GO** | 原话+强跨域(反馈闭环)；簇⑤，入 patience-discipline |
| p27 | 高估区域必须止盈否则坐过山车 | **GO** | 原话+全书复现≥3+actionable；入 value-toolkit A2 |
| p28 | 顶部体感风险低、真实风险高 | **GO** | 原话+反直觉+强跨域；簇①，入 mean-reversion A2 |
| p29 | 千万不能用融资上杠杆 | **GO** | 原话+全书复现≥3+第一铁律；簇③，入 risk-no-leverage A2 |
| p30 | 不要单吊一只股票 | **GO** | 原话+actionable；簇③，入 position-control A2 |
| p31 | 不要在下跌趋势中加仓 | CONDITIONAL | 与 ce02/p20 重复，并入 position-control B |
| p32 | 不要高估承受力、不要低估市场极端 | **GO** | 原话+强跨域(过度自信/尾部风险)；入 risk-no-leverage B |
| p33 | 选主动基金三个硬指标(checklist) | **GO** | 原话+清单+actionable；入 screening-playbook (V2 需修 quote) |
| p34 | 选指数基金四个维度(checklist) | CONDITIONAL | 与 p33 同构，并入 screening-playbook A2 |
| p35 | 核心卫星策略比例建议 | CONDITIONAL | 与 c23/f25 重复 + V2 需修 quote，并入 position-control A2 |
| p36 | 激进资产比例 = 100 − 年龄 | CONDITIONAL | 单一公式细则，并入 position-control A2 |
| p37 | 亏损回本难度警示 | CONDITIONAL | 数学注脚 + V2 需修 quote，并入 position-control B |
| p38 | 投资最大的敌人是自己，心态占85% | **GO** | 原话+强跨域(自我认知)；簇⑤，入 patience-discipline I |
| p39 | 信心比黄金更重要 | CONDITIONAL | 原话但偏信念化/近常识，作 cycle/心态注脚，不单列 |
| p40 | 不要被股市所累，否则不如销户 | CONDITIONAL | 原话但属退出型生活边界，并入 patience-discipline B |
| p41 | 研究主营产品需求是否快速增加 | **GO** | 原话+actionable(选股第一因)；入 screening-playbook A2 |
| p42 | 优先选非周期行业龙头 | **GO** | 原话+actionable；入 screening-playbook A2 |
| p43 | 收益主要来自择股而非择时 | **GO** | 原话+上交所统计佐证+actionable；入 screening-playbook I |
| p44 | 真正最致命的问题是仓位控制 | **GO** | 原话+全书复现≥3；簇③，入 position-control I |
| p45 | 荐股承诺高收益皆骗子 | **GO** | 原话+底线规则+actionable；入 screening-playbook B |

### 2.4 Glossary（g01–g27）→ 全部 **NO**（`status: reference`，术语定义卡，不晋级独立 skill）

| id | 术语 | verdict | 一句话理由（并入去向 / 段） |
|----|------|---------|---------------------------|
| g01 | 双腰斩理论 | **NO** | 定义卡；并入 `manzai-mean-reversion` R，其「并非铁律/对个股无效」入 B |
| g02 | 这次不一样 / 这次还一样 | **NO** | 定义卡(作者自造成对词)；并入 `manzai-cycle-thinking` R |
| g03 | 危险值·机会值 | **NO** | 定义卡(私有估值表列头)；并入 `manzai-value-toolkit` R |
| g04 | 估值分位数（近10年分位） | **NO** | 定义卡(买卖信号口径)；并入 `manzai-value-toolkit` R |
| g05 | 低估区域 / 高估区域 | **NO** | 定义卡(三态状态机)；并入 `manzai-value-toolkit` R |
| g06 | 认知变现 | **NO** | 定义卡(因果律)；并入 `manzai-patience-discipline` I |
| g07 | 遛狗理论（小狗与主人） | **NO** | 定义卡；并入 `manzai-mean-reversion` R |
| g08 | 三年一倍 | **NO** | 定义卡(目标+筛选公式)；并入 `manzai-davis-double` I |
| g09 | 大周期 | **NO** | 定义卡(月线尺度)；并入 `manzai-cycle-thinking` R |
| g10 | 本金永久性损失 | **NO** | 定义卡(可逆性判据)；并入 `manzai-risk-no-leverage` I |
| g11 | 戴维斯双击 | **NO** | 定义卡(作者改写的低PE+低EPS)；并入 `manzai-davis-double` I |
| g12 | 戴维斯双杀 | **NO** | 定义卡(双击镜像)；并入 `manzai-davis-double` I |
| g13 | 安全边际 | **NO** | 定义卡(动态双向持有条件)；并入 `manzai-quality-price` I |
| g14 | 杠杆（一词两义） | **NO** | 定义卡+消歧边界(must-disambiguate)；并入 `manzai-risk-no-leverage` B |
| g15 | 预期差 | **NO** | 定义卡(两分法)；并入 `manzai-inverted-thinking` I |
| g16 | 择股与择时 | **NO** | 定义卡(带结论对偶词)；并入 `manzai-screening-playbook` I |
| g17 | 系统性风险 | **NO** | 定义卡(大盘vs局部二分)；并入 `manzai-screening-playbook` I |
| g18 | 内在价值 | **NO** | 定义卡(概念DCF/实操分位)；并入 `manzai-quality-price` I |
| g19 | 定投 | **NO** | 定义卡(有起止开关的建仓工具)；并入 `manzai-value-toolkit` I |
| g20 | 闲钱 | **NO** | 定义卡(风险承受属性前置条件)；并入 `manzai-risk-no-leverage` I |
| g21 | 均值回归 | **NO** | 定义卡(第一原理)；并入 `manzai-mean-reversion` I |
| g22 | 周期 | **NO** | 定义卡(反线性外推开关)；并入 `manzai-cycle-thinking` I |
| g23 | 仓位模型 | **NO** | 定义卡(六维汇总+阈值)；并入 `manzai-position-control` I |
| g24 | 波段抄底逃顶指标 | **NO** | 定义卡(作者私有指标)；并入 `manzai-value-toolkit` I |
| g25 | 资产比价 | **NO** | 定义卡(跨大类资产相对贵贱)；并入 `manzai-cycle-thinking` I |
| g26 | 逆向投资 | **NO** | 定义卡(有估值锚的反向)；并入 `manzai-inverted-thinking` I |
| g27 | 核心资产（一词两义） | **NO** | 定义卡+消歧边界；并入 `manzai-value-toolkit` B |

> 理由总纲：本类是作者术语的「定义/辨析」资产，不具备独立意图与契约（判据1/2 不达标），**不进 rejected/**，按 1.6 硬规则降级为 `status: reference` 定义卡并入对应卡，不失联。映射见上表，`destinations.json` 中逐条登记。

### 2.5 Cases（c01–c30）→ 全部 **NO**（`status: reference`，A1 段案例证据卡，不晋级独立 skill）

| id | 案例 | verdict | 一句话理由（绑定去向） |
|----|------|---------|----------------------|
| c01 | 新城控股三年五倍 | **NO** | 案例卡(A1)；绑定 f18/p24 → `manzai-patience-discipline` |
| c02 | 作者21年五阶段进化 | **NO** | 案例卡(A1)；绑定 f23/p26/f31 → `manzai-patience-discipline` |
| c03 | 混沌阶段亏得昏天暗地 | **NO** | 案例卡(A1)；绑定 p01/f31 → `manzai-patience-discipline` |
| c04 | 茅台塑化剂错杀后暴涨 | **NO** | 案例卡(A1)；绑定 p04/f10/p03 → `manzai-value-toolkit` |
| c05 | 中信证券2018底PB 5%分位反转 | **NO** | 案例卡(A1)；绑定 p04/p42 → `manzai-value-toolkit` |
| c06 | 只做伊利一只股的投资者 | **NO** | 案例卡(A1)；绑定 p25/f28 → `manzai-patience-discipline` |
| c07 | 伊利跌50.47%、PE 3%分位底部机会 | **NO** | 案例卡(A1)；绑定 p04/p27 → `manzai-value-toolkit` |
| c08 | 上交所2016–2019散户全亏损统计 | **NO** | 案例卡(A1)；绑定 p43/p44 → `manzai-screening-playbook`（V2 漏「易」字、bound_to 标签需修） |
| c09 | 沪深300五次跌破11倍PE | **NO** | 案例卡(A1)；绑定 f09/f06 → `manzai-mean-reversion`（V2 序号重排需修） |
| c10 | 沪深300年线三连阴、连跌不超四年 | **NO** | 案例卡(A1)；绑定 f06/f20 → `manzai-cycle-thinking` |
| c11 | 中证白酒塑化剂跌64%后十年二十倍 | **NO** | 案例卡(A1)；绑定 f03/p04 → `manzai-davis-double` |
| c12 | 「这次不一样」泡沫史 | **NO** | 案例卡(A1)；绑定 f20/f06/f07 → `manzai-cycle-thinking` |
| c13 | 2021核心资产戴维斯双杀 | **NO** | 案例卡(A1)；绑定 f03/f20/p19 → `manzai-davis-double` |
| c14 | 重庆啤酒黑天鹅（分散引例） | **NO** | 案例卡(A1)；绑定 f25/p30 → `manzai-position-control` |
| c15 | 腾讯控股双腰斩见底 | **NO** | 案例卡(A1)；绑定 f11/p30 → `manzai-mean-reversion` |
| c16 | 2015.6去杠杆政策信号撤退 | **NO** | 案例卡(A1)；绑定 p11/f30/f24 → `manzai-cycle-thinking` |
| c17 | 2008系统性风险6124→1664跌73% | **NO** | 案例卡(A1)；绑定 p17/f32/p19 → `manzai-risk-no-leverage` |
| c18 | 2015流动性风险5178→2638跌49% | **NO** | 案例卡(A1)；绑定 p17/p44 → `manzai-position-control` |
| c19 | 鳄鱼潜伏动物世界类比 | **NO** | 案例卡(A1)；绑定 f14/f18 → `manzai-patience-discipline` |
| c20 | 茅台高ROE高净利率标杆 | **NO** | 案例卡(A1)；绑定 f12/p14 → `manzai-quality-price` |
| c21 | 凯利公式中证医疗仓位测算 | **NO** | 案例卡(A1)；绑定 f15/p07 → `manzai-position-control`（V2 公式表述需修） |
| c22 | 股债50/50再平衡回测381% | **NO** | 案例卡(A1)；绑定 f26/f25 → `manzai-position-control` |
| c23 | 核心卫星策略示范 | **NO** | 案例卡(A1)；绑定 p35/f25 → `manzai-position-control`（V2 needs_review） |
| c24 | 99%个股不值得+0.5~99.5分布 | **NO** | 案例卡(A1)；绑定 f28/p25 → `manzai-patience-discipline` |
| c25 | 公募基金2022–23连亏中位-34% | **NO** | 案例卡(A1)；绑定 p33/p44 → `manzai-screening-playbook` |
| c26 | 1997入市27年剩20万反面帖 | **NO** | 案例卡(A1)；绑定 p01/f23 → `manzai-patience-discipline` |
| c27 | 持有到100元痛苦 anecdote | **NO** | 案例卡(A1)；绑定 f18/p38 → `manzai-patience-discipline` |
| c28 | 政策底2018.10 / 2023底 | **NO** | 案例卡(A1)；绑定 f30/p11 → `manzai-cycle-thinking` |
| c29 | 均值回归历史教训(2007/2015/2021…) | **NO** | 案例卡(A1)；绑定 f09/p28/f06 → `manzai-mean-reversion` |
| c30 | A股1990–2024六轮牛熊轮回 | **NO** | 案例卡(A1)；绑定 f06/f07/f20 → `manzai-cycle-thinking` |

> 理由总纲：案例是框架/原则的实证证据（判据2 不达标：无独立契约，只有叙事），经 `bound_to` 绑定到对应卡的 **A1 段**；判据1/4 均过但按 1.6 硬规则不单独发现，降级 `status: reference`，不失联。

### 2.6 Counter-examples（ce01–ce39）

| id | 标题 | verdict | 一句话理由 |
|----|------|---------|-----------|
| ce01 | 融资上杠杆爆仓归零 | **GO** | 原话+头号红线+actionable；簇③，入 risk-no-leverage B |
| ce02 | 下跌趋势中过早加仓 | **GO** | 原话+机制清晰；入 position-control B |
| ce03 | 单吊一只股票 | **GO** | 原话+黑天鹅边界；入 position-control B |
| ce04 | 高估承受力、低估市场极端 | **GO** | 原话+强跨域(过度自信/尾部)；入 risk-no-leverage B |
| ce05 | 重仓/满仓：仓位控制最致命 | **GO** | 原话+回本数学；入 position-control B |
| ce06 | 用非闲钱入市 | **GO** | 原话+前置条件失效；入 risk-no-leverage B |
| ce07 | 牛市后期倒金字塔追加资金 | **GO** | 原话+散户标准亏钱路径；入 position-control B |
| ce08 | 政策三番五次提示风险仍不撤退 | **GO** | 原话+2015股灾；入 cycle-thinking B |
| ce09 | 全仓单一行业突破30%红线 | **GO** | 原话+凯利须被红线截断；入 position-control B |
| ce10 | 过度分散导致收益下降 | **GO** | 原话+「分散」另一侧边界；入 position-control B |
| ce11 | 天天看盘被单日涨跌牵着走 | CONDITIONAL | 与 p12/ce12 同簇细则，并入 patience-discipline B |
| ce12 | 频繁交易、佣金贡献给券商 | **GO** | 原话+负期望值；入 patience-discipline B |
| ce13 | 迷信小周期技术指标 | **GO** | 原话+技术分析死穴；入 value-toolkit B |
| ce14 | 把技术分析当唯一依据 | **GO** | 原话+「不可单独使用」边界；入 value-toolkit B |
| ce15 | 追逐题材热点/听股评买低价股 | **GO** | 原话+完整失败样本；入 quality-price B |
| ce16 | 好公司/好基金不计成本追高 | **GO** | 原话+全书复现≥3(中石油/沪深300)；入 quality-price B |
| ce17 | 高估区域不止盈、坐过山车 | **GO** | 原话+「长期持有≠永不卖」边界；入 value-toolkit B |
| ce18 | 靠股评、小道消息买卖 | CONDITIONAL | 与 ce25/p45 防骗簇重叠，并入 screening-playbook B |
| ce19 | 试图精准择时(统计为负) | **GO** | 原话+上交所统计；入 value-toolkit B |
| ce20 | 误用行业轮动/网格策略 | **GO** | 原话+策略适用前提边界；入 value-toolkit B |
| ce21 | 「这次不一样」与线性外推 | **GO** | 原话+专章头号认知陷阱；簇②，入 cycle-thinking B |
| ce22 | 误以为股龄长等于能力强 | **GO** | 原话+学习闭环；簇⑤，入 patience-discipline B |
| ce23 | 靠运气赚的钱靠实力亏回去 | **GO** | 原话+全书认知总纲；簇⑤，入 patience-discipline B |
| ce24 | 把亏损错误归因于「技术不行」 | **GO** | 原话+「在错误层级努力」；入 patience-discipline B |
| ce25 | 相信专家荐股、承诺高收益 | **GO** | 原话+防骗底线；入 screening-playbook B |
| ce26 | 轻信盈利截图/投资群(杀猪盘) | CONDITIONAL | 与 ce25/p18 重叠 + V2 需修 quote，并入 screening-playbook B |
| ce27 | 周期顶业绩最好时买入(双杀) | **GO** | 原话+双击翻转为双杀；簇④，入 davis-double B |
| ce28 | 被套卧倒装死(注册制下失效) | **GO** | 原话+最硬边界(仅对宽基成立)；入 risk-no-leverage B |
| ce29 | 以为股市能快速致富 | **GO** | 原话+延迟满足缺失；簇⑤，入 patience-discipline B |
| ce30 | 广撒网研究平庸股票 | **GO** | 原话+99%不值得；入 patience-discipline B |
| ce31 | 把「高杠杆模式」高ROE当好公司 | CONDITIONAL | 与 ce27/f12 同类细则，并入 quality-price B |
| ce32 | 贪婪：顶部怕踏空追高 | **GO** | 原话+六弱点之首；入 patience-discipline B |
| ce33 | 恐惧：底部反向割肉 | **GO** | 原话+与贪婪对称；入 patience-discipline B |
| ce34 | 羊群效应：从众盲从 | **GO** | 原话+逆向的反面；入 inverted-thinking B |
| ce35 | 锚定效应：被成本价绑住 | **GO** | 原话+清除估值心理噪声；入 inverted-thinking B |
| ce36 | 自负与固执自信、拒绝反面意见 | CONDITIONAL | 与 ce04 过度自信重叠，并入 patience-discipline B |
| ce37 | 持有阶段心理煎熬拿不住牛股 | **GO** | 原话+「持有比买入更难」边界；入 patience-discipline B |
| ce38 | 被股市所累：焦虑抑郁家庭不和 | **GO** | 原话+退出型边界；入 patience-discipline B |
| ce39 | 后悔情绪驱动仓位 | CONDITIONAL | 与 ce32/ce33 情绪簇重叠，并入 patience-discipline B |

---

## 三、未晋级（NO）汇总段

- **Glossary g01–g27（27 条）**：全部 NO。非独立 skill，降级为 **术语定义卡**（`status: reference`），并入对应框架卡的 R/I（g14 杠杆、g27 核心资产两义归 B 段）。映射见 2.4。不失联。
- **Cases c01–c30（30 条）**：全部 NO。非独立 skill，降级为 **案例证据卡（A1 段）**（`status: reference`），经 `bound_to` 绑定到对应框架/原则卡。映射见 2.5。不失联。
- **Frameworks 中 CONDITIONAL（8 条）**：f07/f10/f11/f17/f22/f26/f27/f30，折叠进对应 canonical 卡，不单列。
- **Principles 中 CONDITIONAL（16 条）**：p01/p06/p09/p10/p12/p13/p16/p17/p18/p31/p34/p35/p36/p37/p39/p40，折叠进操作手册/风控/心态 canonical 卡，不单列。
- **Counter-examples 中 CONDITIONAL（6 条）**：ce11/ce18/ce26/ce31/ce36/ce39，折叠进对应 B 段卡（与相邻反例或正面卡重叠，不单列）。
- **需修订项清单（V2）**：`p12`(説→说)、`c08`(补「易」)、`f27`(比例表述)、`f30`(概括词)、`c09`(序号重排)、`c23`(比例简写)、`p19/p33/p35/p37`(短句措辞漂移) → 标 CONDITIONAL-修 quote。
- **`status: needs_review`（2 条）**：`f30`、`c23` —— 引文为抽取器概括改写、原文无逐字对应，需主代理/阶段 2 决定改写 quote 或降级为 summary（见第六节）。
- **V1 标注项**：`c08` 的 `bound_to` 文字标签与 p01 实际标题不符（编号正确），建议阶段 2 同步。

> 按 stage 1.6 硬规则：**未晋级候选不进 `rejected/`，而是降级为 `status: reference` 能力卡/术语卡/案例卡，保留在来源路由入口（`manzaikuai`）内，不会失联**。`rejected/` 仅留给「知识验证未过」者 —— 本次 V1 全过、V2 无编造，故 `rejected/` 为空。

---

## 四、晋级统计（供主代理）

| type | 总数 | GO | CONDITIONAL | NO |
|------|-----|----|-----------|----|
| frameworks | 32 | 24 | 8 | 0 |
| principles | 45 | 29 | 16 | 0 |
| glossary | 27 | 0 | 0 | 27 |
| cases | 30 | 0 | 0 | 30 |
| counter-examples | 39 | 33 | 6 | 0 |
| **合计** | **173** | **86** | **30** | **57** |

- 经 2.1 合并后，**实际新增 canonical 能力卡 = 10 张**（8 张 promoted + 2 张 router 卡），而非 173：mean-reversion、cycle-thinking、inverted-thinking、risk-no-leverage、position-control、davis-double、quality-price、patience-discipline、value-toolkit、screening-playbook。
- 通过率（GO + CONDITIONAL / 总数）= 116 / 173 ≈ **67.1%**，与同批 083 的 67% 一致，符合方法论「30–80%」健康区间（高通过率源于本书方法论密集 + 抽取已去重）。
- 降级率 57 / 173 ≈ 32.9%，全部为术语卡(27) + 案例卡(30)，均 `status: reference` 保留、无失联。

## 五、推荐进入 dist/pack 的 Top 模块（manzai-*）

按「最少可发现入口覆盖最多高价值意图」+ 软预算 **8**：

| 优先级 | 模块(skill pack) | 吸纳 canonical 卡 / 主题 | 段(R/I/A1/A2/E/B) | 晋级定位 |
|-------|------------------|--------------------------|--------------------|----------|
| 1 | `manzai-mean-reversion` | 簇①：遛狗理论/均值回归/双腰斩/情绪钟摆/体感风险与真实风险 | R·I·A1·A2·B | **promoted** |
| 2 | `manzai-quality-price` | 簇④：好行业+好公司+好价格/三位一体/安全边际/ROE杜邦/波特五力 | R·I·A1·A2·B | **promoted** |
| 3 | `manzai-risk-no-leverage` | 簇③前半：永不上杠杆/本金永久性损失/闲钱/承受力/装死边界 | R·I·A1·A2·B | **promoted** |
| 4 | `manzai-position-control` | 簇③后半：仓位红线/凯利/分批建仓/分散集中/四笔钱/再平衡/六维共振 | R·I·A1·A2·E·B | **promoted** |
| 5 | `manzai-cycle-thinking` | 簇②前半：周期/这次不一样/大周期/政策信号/资产比价 | R·I·A1·A2·B | **promoted** |
| 6 | `manzai-inverted-thinking` | 簇②后半：逆向/第二层次/预期差/市场先生/羊群锚定 | R·I·A1·A2·B | **promoted** |
| 7 | `manzai-davis-double` | 簇④前半：市值=净利×PE/双击双杀/三年一倍公式 | R·I·A1·A2·B | **promoted** |
| 8 | `manzai-patience-discipline` | 簇⑤：耐心持有/认知变现/知行合一/延迟满足/心态85%/六大人性弱点 | R·I·A1·A2·B | **promoted** |
| 9（超预算） | `manzai-value-toolkit` | 估值分位/危险值机会值/低估高估三态/好价格四情形/卖出三原则/定投/大周期波段/技术面边界 | R·I·A1·A2·E·B | **served_by(router 卡)** |
| —（超预算） | `manzai-screening-playbook` | 选股排雷清单/ROE排除/基金筛选/择股优于择时/防骗/注册制退市 | R·I·A1·A2·B | **served_by(router 卡)** |
| — | `manzaikuai`（来源路由入口） | 其余全部术语卡/案例卡/边界注脚统一入口 | R·I·A1·A2·E·B | **router** |

> 说明：预算内 8 个 promoted skill 恰好覆盖 5 个高重叠簇经拆分后的 8 张 canonical 卡（簇①1 + 簇②2 + 簇③2 + 簇④2 + 簇⑤1 = 8）；估值操作手册与选股排雷手册作为 router 卡保留（split-on-evidence 后可升级为第 9/10 个 promoted）。所有 GO/CONDITIONAL 条目在 `destinations.json` 中逐一映射，NO 条目以 `status: reference` 映射，**无遗漏、无失联**。

## 六、需主代理决策的分歧点

1. **`f30` / `c23` 的 `needs_review` 处置**：这两条 `source_quote` 是抽取器**概括改写**（「如果宏观政策面强烈支持并暗示机会，我们就积极做多…」「保守型80/20、稳健型70/30…」），`grep -F` 核实核心词（「积极做多」「暂时退出」「80%的核心资产和20%的卫星资产」）真实存在，但整句原文无逐字对应。样板 083 中所有 V2 问题都判「可修」，本批是首例「非逐字引文」。**请定夺**：(A) 阶段 2 按原文重写 quote 后保留 GO/CONDITIONAL，或 (B) 维持 `status: needs_review`、本批不纳入晋级、留人工复核。
2. **簇②是否拆成 2 个 promoted（8 槽位分配）**：用户建议模块已含 `manzai-cycle-thinking` 与 `manzai-inverted-thinking` 两个，本批按 1.6 硬规则（输出契约不同不强行合并）拆为 2 张 promoted；但「逆向投资」与「周期/这次不一样」在书中高度同章共现，也可合并为 1 张以省出 1 个入口、把当前只能作 router 卡的 `manzai-value-toolkit`（估值分位/危险值机会值/卖出三原则，操作价值高）提升为第 8 个 promoted。**请主代理在「8 槽位分配」上拍板**：是保持 8 卡现状，还是「合并簇②→腾位给 value-toolkit」。
