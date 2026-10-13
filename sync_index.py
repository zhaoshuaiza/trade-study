# -*- coding: utf-8 -*-
"""把 wiki/ 下所有页面自动登记进 index.md 的「自动页面清单」区块（幂等）。

规则：
- 只替换 <!-- AUTO_PAGES:START --> 与 <!-- AUTO_PAGES:END --> 之间的内容
- 区块不存在则追加到文件末尾
- 永不删除 index.md 中的手写内容
- 每次写盘前先校验将写入的条目数 > 0，否则 sys.exit(1)
"""
import os, io, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(ROOT, 'wiki')
START = '<!-- AUTO_PAGES:START -->'
END = '<!-- AUTO_PAGES:END -->'

# 目录展示顺序（与 CLAUDE.md 八类分层一致）
ORDER = [
    ('concepts', '抽象概念'),
    ('entities', '具体体系'),
    ('sources', '一本资料一页'),
    ('claims', '方法论冲突'),
    ('comparisons', '差异'),
    ('syntheses', '跨体系'),
    ('questions', '问答'),
    ('meta', '治理/体检'),
]

# lint 报告页在 wiki/meta/lint/ 下，单独一组登记
EXTRA = [('meta/lint', '治理 / lint 报告')]

def collect():
    buckets = {}
    for sub, label in ORDER + EXTRA:
        d = os.path.join(WIKI, sub)
        if not os.path.isdir(d):
            continue
        items = []
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.md') or fn == 'README.md':
                continue
            items.append(fn[:-3])
        if items:
            buckets[sub] = (label, items)
    # 库根目录的上手指南（非模板、非规则文件）
    roots = [fn[:-3] for fn in sorted(os.listdir(ROOT))
             if fn.endswith('.md') and fn not in ('CLAUDE.md', 'README.md')]
    if roots:
        buckets['_root'] = ('入口页', roots)
    return buckets

def main():
    buckets = collect()
    lines = [START, '',
             '> 本区块由 `sync_index.py` 自动生成，**不要手工编辑**。',
             '']
    total = 0
    for sub, (label, items) in buckets.items():
        lines.append(f'### {label}（`{sub}/`，{len(items)} 页）')
        lines.append('')
        for stem in items:
            lines.append(f'- [[{sub}/{stem}]]')
        lines.append('')
        total += len(items)
    if total == 0:
        print('✗ 未找到任何页面，中止写入')
        sys.exit(1)
    lines.append(END)
    block = '\n'.join(lines)

    p = os.path.join(WIKI, 'index.md')
    txt = io.open(p, encoding='utf-8').read() if os.path.exists(p) else '# 交易学习库索引\n'
    if START in txt and END in txt:
        i, j = txt.index(START), txt.index(END) + len(END)
        new = txt[:i] + block + txt[j:]
        mode = '替换'
    else:
        new = txt.rstrip() + '\n\n---\n\n## 自动页面清单\n\n' + block + '\n'
        mode = '追加'
    if len(block) < 50:
        print('✗ 生成的区块异常短，中止')
        sys.exit(1)
    io.open(p, 'w', encoding='utf-8').write(new)
    print(f'✓ index.md 已{mode}自动清单：{total} 页')

if __name__ == '__main__':
    main()