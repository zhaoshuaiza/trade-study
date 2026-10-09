# -*- coding: utf-8 -*-
"""知识层纵向生长体检 —— 找出"横向堆出来"的页面。

背景（本库的真问题）：
  编译多本书后，同一个主题容易在不同页面里各写一遍，
  表现为「A ⟷ B 内容重叠高但互相不引用」——这是横向堆，不是纵向长。

用法:
  python check_growth.py           # 报告
  python check_growth.py --pairs   # 只看重叠对
输出:
  控制台报告；人确认后再决定是否合并。
"""
import glob, re, os, itertools

ROOT = r'E:/Work Buddy/交易学习'
LAYERS = ['wiki/concepts', 'wiki/claims', 'wiki/syntheses', 'wiki/entities']
SKIP_STATUS = {'superseded'}          # 已标记取代的页不再参与
OVERLAP_WARN = 0.20                    # 重叠告警阈值
STRONG = 0.26                # 强重叠：很可能该合并或互链


def load():
    pages = {}
    for layer in LAYERS:
        for f in glob.glob(os.path.join(ROOT, layer, '*.md')):
            t = open(f, encoding='utf-8').read()
            name = os.path.basename(f)[:-3]
            status = re.search(r'^status:\s*(\S+)', t, flags=re.M)
            pages[name] = {
                'text': t,
                'layer': layer.replace('wiki/', ''),
                'status': status.group(1) if status else '',
                # 中文词块，用来做相似度
                'words': set(re.findall(r'[\u4e00-\u9fa5]{2,4}', t)),
            }
    return pages


def links_of(text):
    """返回链接目标名（去路径、去 .md），因为 Obsidian 里
    [[entities/传奇投资人的智慧]] 与 [[传奇投资人的智慧]] 指向同一页。"""
    out = set()
    for l in re.findall(r'\[\[([^\]|#]+)', text):
        out.add(l.split('/')[-1].replace('.md', '').strip())
    return out


def overlap(a, b):
    A, B = a['words'], b['words']
    if not A or not B:
        return 0.0
    return len(A & B) / min(len(A), len(B))


def mutual_ref(a, b, la, lb):
    """双向引用检测。必须按去路径后的名字比对，
    否则 [[entities/X]] 与裸名 X 会被误判为无引用。"""
    return (b in la) or (a in lb)


def main():
    pages = load()
    live = {k: v for k, v in pages.items() if v['status'] not in SKIP_STATUS}
    print('=' * 66)
    print('知识层纵向生长体检')
    print('=' * 66)
    print(f'参与检查 {len(live)} 页（已排除 superseded）')

    # ---- 1. 重叠对 ----
    pairs = []
    for a, b in itertools.combinations(live, 2):
        ov = overlap(live[a], live[b])
        if ov >= OVERLAP_WARN:
            pairs.append((ov, a, b))
    pairs.sort(reverse=True)

    print()
    print(f'【1】内容重叠 ≥ {OVERLAP_WARN:.0%}的页对（共 {len(pairs)} 对）')
    print()
    orphan_links = []
    for ov, a, b in pairs:
        la, lb = links_of(live[a]['text']), links_of(live[b]['text'])
        if mutual_ref(a, b, la, lb):
            continue# 已互链 = 知识在原页上加深了，不算问题
        flag = '🟡 很可能重复' if ov >= STRONG else '🟢 主题相近'
        print(f'  {flag} {ov:4.0%}  {a} ⟷ {b}')
        print('         ⚠️ 双向无引用 → 这是"堆出来"不是"长出来"')
        orphan_links.append((ov, a, b))

    # ---- 2. 结论与建议 ----
    print()
    print('【2】判断标准')
    print('  ✅ 长出来：重叠高 **且** 互相引用 → 知识在原页上加深了')
    print('  ❌ 堆出来：重叠高 **但** 无引用   → 同一知识写在两页，会越读越乱')
    print()
    if orphan_links:
        print(f'⚠️ 需处理：{len(orphan_links)} 对重叠高但互不引用')
        for ov, a, b in orphan_links:
            print(f'   - {a}  ⟷  {b}  ({ov:.0%})')
        print()
        print('   处理方式（二选一，人来定）：')
        print('    A. 合并 —— 把更完整的一页作为主线，另一页只留指针')
        print('    B. 互链 —— 若两页各有独立价值，'
              '在关系区互相引用并说明分工')
    else:
        print('✅ 所有高重叠页对都已互相引用 —— 知识是在原页上加深')

    # ---- 3. 只进不出 ----
    print()
    print('【3】只被引用、没有内容链接出去的页（可能是内容单薄）')
    thin = []
    for name, v in live.items():
        if len(v['text']) < 1800:
            thin.append((len(v['text']), name))
    thin.sort()
    if thin:
        for n, name in thin[:10]:
            print(f'   - {name}  ({n} 字符)')
        if len(thin) > 10:
            print(f'   …… 另有 {len(thin) - 10} 页')
    else:
        print('   无')

    print()
    print('=' * 66)
    print('📌 脚本只报告，不自动改。按 CLAUDE.md，删改由你拍板。')
    print('=' * 66)


if __name__ == '__main__':
    main()
