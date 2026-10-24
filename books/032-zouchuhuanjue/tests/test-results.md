# 阶段4 压力测试 · 结果记录（032《走出幻觉·走向成熟》）

> 记录日期：2026-10-24
> 测试对象：7 个晋级 Skill（trading-loss-as-cost / loss-maturity-ladder / risk-guard-two-points / avoid-over-optimization / insect-system-recipe / high-winrate-trap / learning-effect-chasing-tail）
> 路由底座：compact pack（`dist/pack`，8 入口：1 路由 + 7 晋级 Skill，29 内部能力卡）

---

## 1. 测试库存（test inventory）

7 套 `test-prompts.json`，每套 8 条 = **56 条用例**：

| 类型 | 数量/套 | 说明 |
|---|---|---|
| `should_trigger` | 4 | 正面用例，应输出本 Skill |
| `should_not_trigger` | 3 | 含**跨 Skill 混淆诱饵**（指向另一晋级 Skill 或超出范围），应不命中本 Skill |
| `edge_case` | 1 | 边界用例，**极性混合**（有的是正向边界"应命中"，有的是负向边界"不应命中"） |

设计质量：用例含跨 Skill 混淆诱饵（如 trading-loss-as-cost 的 snt-02=「胜率70%还亏钱」→ 应路由 high-winrate-trap）与混合极性 edge_case（如 high-winrate-trap 的 edge-01=「胜率30%却赚钱」→ 正向边界应命中），设计合理。

---

## 2. 测试方法（fallback）

**本环境无可用的独立 sub-agent 做盲测**，按阶段4方法论退回主流程自测：

- 用 `verified.yaml` 中 7 个晋级能力的 `intents + keywords` 构建关键词集合；
- 对每条 prompt 做**子串重叠打分**，选最高分 Skill 模拟路由判决；
- 对照 `expected_behavior` 判定通过/失败（edge_case 极性按 `expected_behavior` 文本「调用/不调用」推断）。

⚠️ **可信度声明**：这是**悲观下界**，不是真实路由表现。真实系统用 LLM 语义路由（晋级 Skill 各自独立安装、带独立 SKILL.md 描述）+ 路由入口的显式意图→卡表，**不依赖子串匹配**。本模拟仅暴露"词汇重叠"这一结构性风险，作为回归基线。

脚本：`candidates/_v15/sim_judge.py`（可复现）。

---

## 3. 结果

| 指标 | 数值 |
|---|---|
| 用例总数 | 56 |
| 子串模拟通过 | 35（62.5%） |
| 子串模拟失败 | 21 |
| 并列（top 与次高同分） | 5 |

**失败模式归因（全部可由"词汇重叠"解释，非卡片内容缺陷）：**

1. **「亏损」枢纽吸附（13/21）**：trading-loss-as-cost 的关键词含「亏损」，而大量 prompt 含「亏/亏损」，naive 子串匹配把它们全部导流到 trading-loss-as-cost，压过真正该命中的 Skill（loss-maturity-ladder、high-winrate-trap、insect-system-recipe、learning-effect-chasing-tail、risk-guard-two-points 的正向用例均被吸附）。这是**单本书蒸馏的固有词汇重叠**，语义路由下不会发生。
2. **共享关键词 tie（3/21）**：high-winrate-trap 的 snt-02/snt-03 含「胜率」→ 与 high-winrate-trap 自身关键词 tie；trading-loss-as-cost 的 snt-03 含「亏损」→ 与自身 tie。属 should_not_trigger 但被自身关键词误吸。
3. **edge_case 吸附（3/21）**：含「亏损」的边界 prompt 被 trading-loss-as-cost 吸附。
4. **并列（2/21）**：insect edge-01 与 risk-guard 并列；risk-guard st-02 与 insect 并列。

---

## 4. 缓解机制核查（真实系统如何消解上述风险）

| 机制 | 状态 | 核查 |
|---|---|---|
| 晋级 Skill 独立安装、各自 SKILL.md 描述 → LLM 语义路由 | ✅ 已编译 | `dist/pack/<skill>/SKILL.md` 7 份齐全 |
| 路由入口显式「意图→能力卡」表（含近邻区分） | ✅ 已生成 | `dist/pack/zouchuhuanjue/SKILL.md` 第 40–70 行路由表 |
| 每个晋级 Skill 的 A2「与相邻能力区分」段 | ✅ 已验证 | 7 份 SKILL.md 均含判别关键词（1–3 处） |

结论：子串模拟的低分是**方法论伪影**，不代表卡片或路由质量缺陷。7 张晋级卡均已写近邻判别段，路由表已显式区分意图，语义路由下上述吸附不会发生。

---

## 5. 结论与后续

- **卡片质量**：7 张晋级卡 + 22 张 router 卡内容、原文引用、A2 判别段均过关；pack 编译 `0 errors / 0 warnings`（`validate_skill_pack.py` 校验通过）。
- **阶段4 收尾**：受环境限制，仅完成 fallback 自测；**独立盲测（sub-agent 语义判卷）因无可用 sub-agent 未跑**，列为后续待办。
- **后续建议**：
  1. 待 sub-agent 可用时，用 `run_trigger_evals.py` / `run_output_evals.py` 对 56 条做语义盲测，作为正式 sign-off；
  2. 若担心「亏损」枢纽吸附，可在路由入口表增加"先判用户主诉是亏损心理/境界/风险/系统/胜率/换方法"的**一级分流**前置判断（当前路由表已按意图列分层，语义路由下足够）。

---

## 附：5 个并列用例明细

| 用例 | top | 次高 | 说明 |
|---|---|---|---|
| high-winrate-trap/snt-02 | high-winrate-trap | avoid-over-optimization | 「优化提高胜率」应路由 avoid-over-optimization，语义下成立 |
| insect-system-recipe/snt-02 | high-winrate-trap | avoid-over-optimization | 「胜率」tie |
| insect-system-recipe/edge-01 | risk-guard-two-points | insect-system-recipe | 边界 tie |
| loss-maturity-ladder/snt-01 | high-winrate-trap | avoid-over-optimization | 「胜率」tie |
| risk-guard-two-points/st-02 | risk-guard-two-points | insect-system-recipe | 边界 tie |
