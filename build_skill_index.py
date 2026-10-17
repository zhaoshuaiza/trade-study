# -*- coding: utf-8 -*-
"""生成 doubao 技能包 → 交易库的映射索引。

doubao 项目（E:/doubao/电子书蒸馏项目/）已把 98 本书蒸成 243 个技能包，
但技能装在豆包目录，WorkBuddy 侧看不到。��工具把清单同步过来并建交叉引用。

用法: python build_skill_index.py
输出: wiki/meta/skills/doubao技能索引.md
"""
import io, os, re, glob

DB = 'E:/doubao/电子书蒸馏项目'
OUT = 'E:/Work Buddy/交易学习/wiki/meta/skills'

# 技能前缀 → 体系归类
FAMILY = {
    'cb': ('可转债', '用户主做'),
    'jj': ('基金', ''),
    'jjzd': ('基金', ''),
    'guaitie': ('乖离率', '缠论/威科夫'),
    'kanpan': ('看盘', '缠论'),
    'chan': ('缠论', '缠论'),
    'chanm': ('缠论', ''),
    'liangxue': ('量学', '黑马王子'),
    'wyckoff': ('威科夫', ''),
    'wkf': ('威科夫', '威科夫'),
    'vpa': ('威科夫', ''),
    'liangxue': ('量学', '黑马王子'),
    'turtle': ('海龟', '海龟'),
    'elder': ('埃尔德', '海龟'),
    'covel': ('趋势跟踪', ''),
    'sepa': ('SEPA', 'Minervini'),
    'wstn': ('温斯坦', ''),
    'siegel': ('西格尔', ''),
    'omaha': ('芒格', ''),
    'mun': ('芒格', ''),
    'taleb': ('塔勒布', ''),
    'swensen': ('史文森', ''),
    'montier': ('蒙蒂尔', '行为金融'),
    'douglas': ('道格拉斯', '交易心理'),
    'buf': ('巴菲特', ''),
    'jz': ('格雷厄姆/价值', ''),
    'tc': ('唐朝', ''),
    'lyn': ('彼得林奇', ''),
    'fis': ('费雪', ''),
    'jl': ('李杰', ''),
    'qgl': ('邱国鹭', ''),
    'manman': ('张居营', ''),
    'mk': ('霍华德马克斯', ''),
    'steinn': ('温斯坦', ''),
    'stein': ('温斯坦', ''),
    'wzj': ('', ''),
    'zwj': ('', ''),
    'caibao': ('财报', ''),
    'cw': ('财报/银行', '唐朝'),
    'gsy': ('股票四法', ''),
    'malkiel': ('马尔基尔', ''),
    'gann': ('江恩', ''),
    'livermore': ('利弗莫尔', ''),
    'larry': ('拉里威廉斯', ''),
    'longtou': ('龙头股', '游资'),
    'cgzh': ('成功者', '游资'),
    'jiucai': ('李笑来', ''),
    'meigu': ('美股', ''),
    'kangbo': ('康波', '周金涛'),
    'tujing': ('趋势跟踪', ''),
    'turtle': ('海龟', '海龟'),
    'cis': ('CIS', ''),
    'fenshi': ('分时图', ''),
    'xiaoao': ('笑傲股市', ''),
    'linyuan': ('林园', ''),
    'zulu': ('祖鲁法则', ''),
    'onell': ('欧奈尔', ''),
    'jrdg': ('金 rocks', ''),
    'mk': ('霍华德马克斯', ''),
    'jl': ('李杰', ''),
    'ghost': ('华尔街幽灵', ''),
    'wuhanzhong': ('乌合之众', '群体心理'),
    'dun': ('邓普顿', ''),
    'fsi': ('费雪', ''),
    'buf': ('巴菲特', ''),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    # 收集全部技能包（兼容 蒸馏_X/技能包/ 与 蒸馏_X/子目录/技能包/ 两种层级）
    paths = set()
    for root, dns, fns in os.walk(DB):
        if os.path.basename(root) != '技能包':
            continue
        for dn in dns:
            if os.path.exists(os.path.join(root, dn, 'SKILL.md')):
                paths.add(os.path.join(root, dn, 'SKILL.md'))

    skills = {}
    for p in sorted(paths):
        name = os.path.basename(os.path.dirname(p))
        rel = os.path.relpath(p, DB)
        batch = rel.split(os.sep)[0]
        txt = io.open(p, encoding='utf-8').read()
        desc = ''
        m = re.search(r'description:\s*(.+)', txt)
        if m:
            desc = m.group(1).strip()[:80]
        skills[name] = {'batch': batch, 'desc': desc,
                        'path': p.replace('\\', '/')}

    # 按体系分组
    fams = {}
    for name in skills:
        pre = name.split('-')[0]
        fam, note = FAMILY.get(pre, ('其他', ''))
        fams.setdefault(fam, []).append((name, note))

    L = ['# 📦 doubao 技能包索引（243 个）', '']
    L.append('> 来源：`E:/doubao/电子书蒸馏项目/蒸馏_*/技能包/`')
    L.append('> 该项目已把 98 本书蒸成技能包（SKILL.md 格式），**未装到 WorkBuddy**。')
    L.append(f'> 本页由 `python build_skill_index.py` 自动生成，共 **{len(skills)}** 个技能。')
    L.append('')
    L.append('## 与交易库的关系')
    L.append('')
    L.append('| | 交易库（本vault）| doubao 技能包 |')
    L.append('|---|---|---|')
    L.append('| 形态 | Obsidian 双链页面 | `SKILL.md` 带 frontmatter |')
    L.append('| 优势 | 可交叉引用、可存冲突、可辩论 | **可被 AI 直接调用执行** |')
    L.append('| 用途 | 学习和查证 | 实盘时直接调用判据 |')
    L.append('')
    L.append('⚠️ **两者互补而非替代**：技能包多了「怎么用」，但缺了「与其他体系的冲突」。')
    L.append('')

    for fam in sorted(fams, key=lambda x: -len(fams[x])):
        items = sorted(fams[fam])
        L.append(f'## {fam}（{len(items)}）')
        L.append('')
        L.append('| 技能 | 说明 | 批次 |')
        L.append('|---|---|---|')
        for name, note in items:
            d = skills[name]['desc'] or '—'
            b = skills[name]['batch'].replace('蒸馏_', '')
            L.append(f'| `{name}` | {d} | {b} |')
        L.append('')

    p = f'{OUT}/doubao技能索引.md'
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L))
    print(f'技能索引已生成: {p}')
    print(f'共 {len(skills)} 个技能，{len(fams)} 个体系')
    for f in sorted(fams, key=lambda x: -len(fams[x]))[:12]:
        print(f'  {f:14} {len(fams[f])}')


if __name__ == '__main__':
    main()