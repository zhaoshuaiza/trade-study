# -*- coding: utf-8 -*-
"""转债持仓风险自检 —— 每次买之前 / 每天收盘后跑一次。

用法:
  python check_bond.py                 # 读 raw/bonds.txt 里的持仓
  python check_bond.py 123107 128013   # 直接指定代码
  python check_bond.py --set123107 12.5 # 记录转股价
  python check_bond.py --list          # 列出当前持仓与触发距离

⚠️ 本脚本只做「距离触发线有多远」的提醒，**不做买卖建议**。
"""
import sys, os, json, io

BASE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(BASE, 'raw', 'bonds.json')

# 转债代码 → 名称（可手工补）
DEFAULT_NAMES = {
    '123107': '温氏转债', '128013': '洪涛转债', '113050': '南银转债',
    '110059': '浦发转债', '113052': '兴业转债', '128142': '新axon转债',
}


def load():
    if os.path.exists(STORE):
        return json.load(io.open(STORE, encoding='utf-8'))
    return {}


def save(d):
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    json.dump(d, io.open(STORE, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


def ask(prompt):
    try:
        return input(prompt).strip()
    except Exception:
        return ''


def main():
    args = sys.argv[1:]
    store = load()

    # --set：记录转股价
    if args and args[0].startswith('--set'):
        code = args[0][5:]
        if not code or len(args) < 2:
            print('用法: python check_bond.py --set<代码> <转股价>')
            return
        conv = float(args[1])
        store[code] = {'conv': conv, 'name': store.get(code, {}).get('name', '')}
        save(store)
        line = conv * 1.30
        print(f'✓ 已记录 {code} 转股价 = {conv:.2f} 元')
        print(f'  ⭐ 强赎触发线 = {conv:.2f} × 130% = **{line:.2f} 元**')
        print(f'  📌 正股价距离 {line:.2f} 元的 <20% 处 → 需每日关注公告')
        return

    # --list
    if args and args[0] == '--list':
        if not store:
            print('当前无记录。用 --set<代码> <转股价> 添加。')
            return
        print('当前记录的转债：')
        for c, v in store.items():
            line = v['conv'] * 1.30
            print(f"  {c} {v.get('name') or DEFAULT_NAMES.get(c, '')}"
                  f"  转股价 {v['conv']:.2f} → 触发线 {line:.2f}")
        return

    # 取代码
    codes = [a for a in args if not a.startswith('-')]
    if not codes:
        codes = list(store.keys())
    if not codes:
        print('没有可检查的转债。')
        print('用法: python check_bond.py 123107128013')
        return

    print('=' * 60)
    print('转债风险自检（⛔ 强赎永远是第一优先级）')
    print('=' * 60)
    print()
    for c in codes:
        name = DEFAULT_NAMES.get(c, store.get(c, {}).get('name', ''))
        conv = store.get(c, {}).get('conv')
        print(f'【{c} {name}】')
        if conv is None:
            r = ask(f'  {c} 的转股价（元）是多少？直接回车跳过：')
            if r:
                conv = float(r)
                store[c] = {'conv': conv, 'name': name}
                save(store)
            else:
                print('  ⚠️ 未填转股价 → ⛔ **无法算强赎触发线，不要建仓**')
                print('     先查募集说明书或券商软件')
                print()
                continue
        line = conv * 1.30
        print(f'  转股价     = {conv:.2f} 元')
        print(f'  ⭐ 触发线   = {conv:.2f} × 130% = **{line:.2f} 元**')
        r = ask(f'  正股现价（元，回车跳过）：')
        if r:
            px = float(r)
            dist = (px - line) / line * 100
            print(f'  正股价     = {px:.2f} 元')
            print(f'  距触发线   = {dist:+.1f}%')
            if px >= line:
                print('  ⛔⛔⛔ **正股已超触发线**')
                print('       → **每日查公告**，等发行人决定是否行使赎回权')
                print('       → 发行人公告赎回 → **立即卖出或转股**')
            elif dist > -20:
                print('  ⚠️ **距触发线不足 20%** → 开始每日看公告')
            elif dist > -40:
                print('  ⚠️ 距触发线 20~40% → 纳入日常观察')
            else:
                print('  ✅ 距触发线尚远')
        print(f'  ⛔ 其他必查：溢价率 ____%（>30% 警惕）| '
              f'债底距离 ____% | 成交额 ____ 万')
        print()
    print('=' * 60)
    print('⭐ 离场优先级：强赎 > 溢价率压缩 > 双阴 > 黄金线 > 缩量柱')
    print('⚠️ 本脚本仅作提醒，不构成投资建议。')


if __name__ == '__main__':
    main()
