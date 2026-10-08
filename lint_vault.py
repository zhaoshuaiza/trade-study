# -*- coding: utf-8 -*-
"""交易学习库 lint —— 按 CLAUDE.md 第五节 3. 检查七类问题。

用法: python lint_vault.py
输出: 控制台报告（人看过后再决定是否写入 wiki/meta/lint/）
"""
import io, os, re, json, glob
from collections import defaultdict

ROOT = r'E:/Work Buddy/交易学习'
WIKI = os.path.join(ROOT, 'wiki')

# 收集所有 md（含库根目录，CLAUDE.md / 从这里开始.md 等真实存在）
EXCLUDE_DIRS = {'.obsidian', '.git'}
pages = {}
for base_dir in (WIKI, ROOT):
    for dirpath, dirnames, filenames in os.walk(base_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        if base_dir == WIKI and ROOT in dirpath:
            continue  # 根目录已扫过
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace('\\', '/')
            if rel in pages:
                continue
            pages[rel] = io.open(full, encoding='utf-8').read()

# 非 md 资源（图片等），链接到它们不算死链
assets = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fn in filenames:
        if not fn.endswith('.md'):
            assets.add(os.path.splitext(fn)[0])

# 页面名集合（用于死链判定）
stems = set()
for rel in pages:
    stem = os.path.splitext(os.path.basename(rel))[0]
    stems.add(stem)
    stems.add(rel[:-3])
    stems.add(rel.replace('.md', ''))

LINK = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')

def resolve(target):
    t = target.strip()
    if t.endswith('.md'):
        t = t[:-3]
    base = os.path.basename(t)
    # 非 md 资源（图片等）视为存在
    if base in assets:
        return 'ASSET'
    for rel in pages:
        noext = rel[:-3]
        if noext == t or noext.endswith('/' + t) or os.path.basename(noext) == base:
            return rel
    return None

# 说明性占位符，不算死链（如"[[页面名]]"示例）
PLACEHOLDER = {'页面名', '某页面', '双向链接', 'claims', 'concepts', 'entities',
               'sources', 'wiki/questions', '从这里开始'}

outlinks = defaultdict(set)
deadlinks = defaultdict(list)
for rel, txt in pages.items():
    if not rel.startswith('wiki/'):
        continue
    for m in LINK.finditer(txt):
        target = m.group(1)
        if target.strip() in PLACEHOLDER:
            continue
        r = resolve(target)
        if r:
            if r != 'ASSET':
                outlinks[rel].add(r)
        else:
            deadlinks[rel].append(target)

inlinks = defaultdict(set)
for rel, targets in outlinks.items():
    for t in targets:
        inlinks[t].add(rel)

print('=' * 72)
print('交易学习库 lint 报告')
print('=' * 72)
print(f'页面总数：{len(pages)}')

# 1 孤立页面
print('\n【1】孤立页面（无入链且无出链）')
iso = []
for rel in pages:
    if os.path.basename(rel) == 'README.md':
        continue
    if not inlinks.get(rel) and not outlinks.get(rel):
        iso.append(rel)
if iso:
    for r in iso:
        print('  ⚠ ' + r)
else:
    print('  ✅ 无')

# 2 死链接
print('\n【2】死链接（[[目标]] 不存在）')
if deadlinks:
    total = 0
    for rel, ts in sorted(deadlinks.items()):
        uniq = sorted(set(ts))
        total += len(uniq)
        print(f'  ⚠ {rel}  ({len(uniq)} 个)')
        for t in uniq[:8]:
            print(f'      [[{t}]]')
        if len(uniq) > 8:
            print(f'      ... 另 {len(uniq)-8} 个')
    print(f'  合计死链：{total}')
else:
    print('  ✅ 无')

# 3 元信息缺失
print('\n【3】frontmatter 必填字段')
REQ = ['type']
missing = []
for rel, txt in pages.items():
    if os.path.basename(rel) == 'README.md':
        continue
    if not txt.startswith('---'):
        missing.append((rel, '无 frontmatter'))
        continue
    fm = txt.split('---', 2)[1]
    miss = [k for k in REQ if f'{k}:' not in fm]
    if miss:
        missing.append((rel, '缺 ' + ','.join(miss)))
if missing:
    for r, m in missing:
        print(f'  ⚠ {r} — {m}')
else:
    print('  ✅ 全部具备')

# 4 占位页
print('\n【4】占位页（仍有"待编译"）')
ph = []
for rel, txt in pages.items():
    if '待编译' in txt or 'compiled_from: pending' in txt:
        ph.append(rel)
if ph:
    for r in ph:
        print('  ⚠ ' + r)
else:
    print('  ✅ 无')

# 5 claims 空目录
print('\n【5】claims/ 目录（CLAUDE.md 要求承载冲突页）')
claims = [r for r in pages if r.startswith('wiki/claims/') and os.path.basename(r) != 'README.md']
if not claims:
    print('  ⚠ 空——冲突无处承接')
else:
    for r in claims:
        print('  ✅ ' + r)

# 6 索引漂移
print('\n【6】索引漂移（页面未登记进 index.md）')
idx = io.open(os.path.join(WIKI, 'index.md'), encoding='utf-8').read()
drift = []
for rel in pages:
    if rel in ('wiki/index.md',):
        continue
    stem = os.path.splitext(os.path.basename(rel))[0]
    if stem in ('README',):
        continue
    if stem not in idx:
        drift.append(rel)
if drift:
    for r in drift:
        print('  ⚠ ' + r)
else:
    print('  ✅ 全部已登记')

# 7 编译来源缺失
print('\n【7】概念页缺 compiled_from（不可溯源）')
nosrc = []
for rel, txt in pages.items():
    if not rel.startswith('wiki/concepts/'):
        continue
    if os.path.basename(rel) == 'README.md':
        continue
    if 'compiled_from' not in txt or 'pending' in txt.split('compiled_from:')[1][:20] if 'compiled_from:' in txt else True:
        nosrc.append(rel)
if nosrc:
    for r in nosrc:
        print('  ⚠ ' + r)
else:
    print('  ✅ 全部可溯源')

print('\n' + '=' * 72)