#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新素材编译进度台账（机器可读 + 自动报告）
台账文件: wiki/meta/新素材编译台账.json
用法:
  python progress_new.py            # 打印进度报告
  python progress_new.py --set 12 done      # 标记第12本已完成
  python progress_new.py --set 12 ocr       # 标记需OCR
  python progress_new.py --set 12 blocked   # 标记阻塞
⭐ 进度由台账算出，不手写数字，避免口径漂移。
"""
import io, os, json, sys, argparse
from collections import Counter, OrderedDict

ROOT = r"E:/Work Buddy/交易学习"
LEDGER = os.path.join(ROOT, "wiki/meta/新素材编译台账.json")
NEWRAW = os.path.join(ROOT, "raw/distilled/新素材")

# ⭐⭐ 批次定义：按「边际价值 × 成本」排序，批次内可并行
# tier: 0=已结案(分流/不入库) 1=P0 2=P1 3=P2 4=P3
BATCHES = OrderedDict([
    ("B0", dict(tier=0, name="分流结案（不编译正文）",
                note="B类hedge + C类不入库，已实测判定")),
    ("B1", dict(tier=1, name="P0 同作者续作与转债（0 OCR）",
                note="黑马王子6-9/伏击涨停/攻守转债 —— 直接可用")),
    ("B2", dict(tier=2, name="P1 本库完全缺失的体系（0 OCR）",
                note="威科夫三书/蒙蒂尔行为金融/埃尔德三本/温斯坦/拉里威廉斯")),
    ("B3", dict(tier=3, name="P2 转债深度与龙头（少量OCR）",
                note="可转债黄金宝典+躺赢指南518页/龙头股战法已抽")),
    ("B4", dict(tier=4, name="P3 价值投资体系（先抽样再定）",
                note="护城河/聪明的投资者/祖鲁法则等 —— 量大但可落成判据")),
    ("B5", dict(tier=5, name="P4 复盘史实与基金（低优先）",
                note="追寻价值之路/美股70年需OCR；基金3本可秒抽")),
])

# ⭐ 书名关键词 → (批次, 状态, 备注)
#状态: pending / ocr / done / skip / blocked
TASKS = [
    # ── B1 P0 ──
    ("黑马王子操盘手记(六-九)", "B1", "done", "已提取12术语+5矛盾，见 _黑马王子6-9册"),
    ("伏击涨停+涨停密码", "B1", "pending", "凹底淘金正式出处；待编《涨停密码》黄金三角"),
    ("攻守：可转债投资实用手册", "B1", "done", "已出转债四大策略页；第五章88问答待编"),
    ("可转债投资魔法书(第2版)", "B1", "pending", "需先核实与旧版是否同书"),
    ("一本书搞懂龙头股战法", "B1", "pending", "已抽全文，222页PDF有文字层"),
    ("股市极客思考录", "B1", "pending", "已抽，3.4万字，短"),
    ("cisの股票交易术", "B1", "pending", "已抽，与主力的思维同源"),
    ("主力的思維", "B1", "pending", "已抽"),
    ("华尔街幽灵", "B1", "pending", "已抽"),
    # ── B2 P1 本库完全缺失 ──
    ("量价分析 量价分析创始人威科夫", "B2", "pending", "威科夫1，已抽8.3万字"),
    ("新威科夫操盘法", "B2", "done", "已抽152545字，待精读编译"),
    ("威科夫操盘理论在中国股市的实战", "B2", "ocr", "258页需OCR"),
    ("行为金融学：洞察非理性投资心理", "B2", "pending", "蒙蒂尔，已抽，本库0页"),
    ("行为投资学手册", "B2", "pending", "蒙蒂尔，已抽，本库0页"),
    ("以交易为生（原书第2版）", "B2", "pending", "埃尔德，已抽真文本"),
    ("以交易为生II：卖出的艺术", "B2", "pending", "埃尔德，已抽"),
    ("走进我的交易室", "B2", "pending", "埃尔德，已抽"),
    ("史丹•温斯坦称傲牛熊市的秘密", "B2", "pending", "已抽，量价可与黑马王子对照"),
    ("短线交易秘诀（原书第2版）", "B2", "pending", "拉里威廉斯，已抽"),
    ("笑傲股市(原書第4版", "B2", "pending", "已抽，与利弗莫尔并读"),
    ("股票大作手操盘术", "B2", "pending", "利弗莫尔，已抽"),
    ("股市趋势技术分析（原书第10版", "B2", "pending", "已抽"),
    ("分时图实战", "B2", "pending", "已抽，日内形态"),
    ("看盘方法与技巧一本通", "B2", "pending", "已抽"),
    ("交易之路：如何构建", "B2", "pending", "已抽"),
    ("交易圣经：系统交易赢利要诀", "B2", "pending", "已抽"),
    ("一小时漫画缠论实战法", "B2", "pending", "已抽2.2万字，缠论补充"),
    ("100倍超级强势股", "B2", "pending", "已抽"),
    ("股票魔法师纵横天下股市的奥秘", "B2", "pending", "记忆记为伪文字层，mobi可秒抽→需重验"),
    ("股票魔法师Ⅱ", "B2", "ocr", "278页"),
    ("股票魔法师3趋势交易圆桌访谈", "B2", "pending", "已抽"),
    ("日本蜡烛图技术（第二版）", "B2", "pending", "已抽，K线经典"),
    ("海龟交易法则（珍藏版）", "B2", "skip", "⭐用户约束不能做期货→只登记思想"),
    ("趋势跟踪（原书第5版）", "B2", "skip", "⭐期货为主→只登记动量思想"),
    ("趋势永存：打败市场的动量策略", "B2", "pending", "动量思想可登记"),
    ("构建量化动量选股系统", "B2", "pending", "已抽"),
    ("期货狙击手", "B2", "skip", "⭐期货→挂起"),
    # ── B3 转债与基金 ──
    ("可转债投资黄金宝典", "B3", "ocr", "218页，与转债策略互补"),
    ("可转债：投资小白躺赚指南", "B3", "ocr", "300页"),
    ("指数基金投资指南", "B3", "pending", "已抽"),
    ("躺着赚钱的漫画基金书", "B3", "pending", "已抽"),
    ("白话投资：基金入门与进阶", "B3", "ocr", "298页"),
    # ── B4 价值投资 ──
    ("巴菲特的护城河", "B4", "pending", "⭐交易词169次最高，本库0页"),
    ("聪明的投资者(投资圣经)", "B4", "pending", "⭐安全边际+防御/进攻组合"),
    ("祖鲁法则", "B4", "pending", "⭐阙值+增长率选股法，本库无"),
    ("投资最重要的事", "B4", "pending", "⭐周期钟、风险是赚来的"),
    ("周期 (霍华德·马克斯", "B4", "done", "已抽221729字，待精读"),
    ("邓普顿教你逆向投资", "B4", "pending", "逆向择时可落成动作"),
    ("戴维斯王朝", "B4", "pending", "估值扩张/收缩"),
    ("大钱细思", "B4", "done", "已抽，林奇+卡拉曼+米勒"),
    ("投资中最简单的事", "B4", "pending", "邱国鹭估值判据"),
    ("价值投资实战手册", "B4", "pending", "唐朝，财报造假识别"),
    ("手把手教你读财报2", "B4", "pending", "唐朝"),
    ("学会估值，轻松投资", "B4", "pending", "达摩达兰"),
    ("漫步华尔街（原书第11版）", "B4", "pending", "有效市场→影响择时有效性"),
    ("林园炒股秘籍", "B4", "pending", "有仓位判据"),
    ("股市进阶之道", "B4", "pending", "李杰，散户自我修养"),
    ("复利信徒", "B4", "pending", "李杰"),
    ("慢慢变富", "B4", "pending", "张居营"),
    ("一个投资家的20年", "B4", "pending", "杨天南实战札记"),
    ("彼得林奇投资经典全集", "B4", "pending", "⚠含战胜华尔街(已有)→只补另两册"),
    ("怎样选择成长股", "B4", "pending", "费舍，交易词6次偏低"),
    ("价值 (张磊", "B4", "pending", "交易词7次偏低"),
    # ── B5 其他 ──
    ("证券投机的艺术", "B5", "pending", "科斯托拉尼"),
    ("金融怪杰", "B5", "pending", "已抽"),
    ("韭菜的自我修养", "B5", "pending", "交易词28次高密度"),
    ("周金涛理论大集", "B5", "pending", "已抽94万字，周期理论"),
    ("追寻价值之路", "B5", "ocr", "532页"),
    ("美股70年", "B5", "ocr", "496页"),
    ("江恩华尔街45年", "B5", "ocr", "244页，本库完全缺失江恩体系"),
    ("股票魔法师纵横天下股市的奥秘.重复", "B5", "skip", "占位"),
    # ── B0 分流结案 ──
    ("乌合之众", "B0", "skip", "实测0次交易词→hedge"),
    ("小狗钱钱", "B0", "skip", "实测0次→hedge"),
    ("小岛经济学", "B0", "skip", "实测0次→hedge"),
    ("繁荣与衰退", "B0", "skip", "实测0次→hedge"),
    ("赢：有钱人", "B0", "skip", "实测1次→hedge"),
    ("伟大的博弈", "B0", "skip", "实测1次→hedge"),
    ("大癫狂", "B0", "skip", "实测1次→hedge"),
    ("一本书掌握财务技巧", "B0", "skip", "会计教材→hedge"),
    ("穷查理宝典", "B0", "skip", "思维模型→hedge"),
    ("价值投资之茅台大博弈", "B0", "skip", "单一案例→hedge"),
    ("奥马哈之雾", "B0", "pending", "交易词97次，需再判归属"),
    ("巴菲特致股东的信", "B4", "pending", "已抽，偏向阅读"),
    ("财报就像一本故事书", "B0", "skip", "财报科普→不入库"),
    ("非对称风险", "B0", "skip", "塔勒布思维模型→hedge"),
    ("机构投资的创新之路", "B0", "skip", "机构配置→落不到看盘动作"),
    ("赌客信条", "B0", "skip", "科普且与蒙蒂尔重复"),
    ("价值评估 公司价值的衡量与管理", "B4", "ocr", "640页，价值评估权威"),
    ("价值投资从格雷厄姆到巴菲特", "B4", "ocr", "264页"),
    ("像欧奈尔信徒一样交易", "B2", "ocr", "355页"),
    ("像欧奈尔信徒一样交易（二）", "B2", "ocr", "315页"),
    ("半小时漫画股票实战法", "B2", "ocr", "628页"),
    ("交易心理分析", "B2", "ocr", "272页，道格拉斯，⭐重要"),
]


def load():
    if os.path.exists(LEDGER):
        return json.load(io.open(LEDGER, encoding="utf-8"))
    return {}


def save(d):
    io.open(LEDGER, "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", nargs=2, metavar=("IDX", "STATUS"))
    ap.add_argument("--note", default="")
    ap.add_argument("--init", action="store_true")
    a = ap.parse_args()

    led = load()
    if a.init or not led:
        led = {}
        for i, (name, batch, st, note) in enumerate(TASKS, 1):
            led[str(i)] = dict(idx=i, name=name, batch=batch,
                               status=st, note=note, done_date="")
        save(led)
        print(f"✅ 台账已初始化：{len(led)} 条")

    if a.set:
        k, v = a.set
        if k not in led:
            print(f"❌ 无此编号 {k}"); return
        led[k]["status"] = v
        if a.note:
            led[k]["note"] = a.note
        if v == "done":
            led[k]["done_date"] = "2026-10-14"
        save(led)
        print(f"✅ #{k} {led[k]['name'][:30]} → {v}")

    # ── 报告 ──
    st = Counter(v["status"] for v in led.values())
    total = len(led)
    done = st["done"]
    skip = st["skip"]
    ocr = st["ocr"]
    pend = st["pending"]
    blocked = st["blocked"]
    effective = total - skip
    pct = done / effective * 100 if effective else 0

    print("\n" + "=" * 62)
    print("📊 新素材编译进度（101 本素材库）")
    print("=" * 62)
    print(f"  台账总数   {total}")
    print(f"  ✅ 已完成   {done:>3}    ⏭️ 跳过(分流/挂起) {skip:>3}")
    print(f"  ⏳ 待编译   {pend:>3}    🔍 需OCR {ocr:>3}   ⛔ 阻塞 {blocked:>3}")
    print(f"\n  📈 有效进度 {done}/{effective} = {pct:.1f}%（已剔除跳过项）")
    print("=" * 62)

    for bid, meta in BATCHES.items():
        rows = [v for v in led.values() if v["batch"] == bid]
        if not rows:
            continue
        c = Counter(r["status"] for r in rows)
        eff = len(rows) - c["skip"]
        bar_w = 22
        f = (c["done"] / eff * bar_w) if eff else bar_w
        bar = "█" * int(f) + "░" * (bar_w - int(f))
        print(f"\n【{bid}】{meta['name']}  ({c['done']}/{eff} ⏭{c['skip']})")
        print(f"  {bar}")
        print(f"  ⏳{c['pending']} 待编译  🔍{c['ocr']} 需OCR  ⛔{c['blocked']} 阻塞")
        print(f"  ⓘ {meta['note']}")
        todo = [r for r in rows if r["status"] in ("pending", "ocr", "blocked")]
        for r in todo[:12]:
            mark = {"pending": "⏳", "ocr": "🔍", "blocked": "⛔"}[r["status"]]
            print(f"     {mark} #{r['idx']:<3} {r['name'][:44]}")
        if len(todo) > 12:
            print(f"     …… 另有 {len(todo)-12} 本")


if __name__ == "__main__":
    main()