# -*- coding: utf-8 -*-
"""交易学习库 lint —— 按 CLAUDE.md 第五节 3. 检查七类问题。

用法: python lint_vault.py
输出: 控制台报告（人看过后再决定是否写入 wiki/meta/lint/）
"""
import io, os, re, json, glob
from collections import defaultdict

ROOT = r'E:/Work Buddy/交易学习'
WIKI = os.path.join(ROOT, 'wiki')

# ⭐ 只查知识层，不查 raw/ 素材层（2026-10-10 修正）
# 原因：raw/ 是只读原始资料，没有双链是正常的。
#把它算进来会让"孤立页面"被几十篇原始资料刷屏，真正的孤立知识页被淹没。
EXCLUDE_DIRS = {'.obsidian', '.git', 'raw', '.raw'}
# ⭐ 蒸馏流水线产物目录：与 raw/ 同理——是只读素材/缓存，没有双链是正常的。
#   .cangjie/ 已在 .gitignore 声明为「蒸馏流水线缓存，不入库」；
#   books/<id>/{candidates,dist,tests,rejected,snapshots}/ 是女娲/蒸馏技能
#   的构建产物（2026-10-27 巡检：它们把页面总数从 ~460 顶到 789，淹没真实问题）。
SKIP_DIRS = {'交易学习'}
ARTIFACT_SUBDIRS = {'.cangjie', 'candidates', 'dist', 'tests',
                    'rejected', 'snapshots', 'references', 'pack'}
pages = {}
unreadable = []
for base_dir in (WIKI, ROOT):
    for dirpath, dirnames, filenames in os.walk(base_dir):
        dirnames[:] = [d for d in dirnames
                       if d not in EXCLUDE_DIRS and d not in SKIP_DIRS]
        if base_dir == WIKI and ROOT in dirpath:
            continue  # 根目录已扫过
        # 流水线构建产物子目录（books/<id>/candidates 等）不计入知识层
        dirnames[:] = [d for d in dirnames if d not in ARTIFACT_SUBDIRS]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace('\\', '/')
            if rel in pages:
                continue
            try:
                pages[rel] = io.open(full, encoding='utf-8').read()
            except OSError as e:
                unreadable.append((rel, e))

RESOURCE_STEMS = set()

# ⭐ 收集非md 资源（2026-10-10 修正）
# .attachments/ 是点开头的附件目录，原先没登记，
# 导致 [[目录导航图.png]] 这类图片链接被误判为死链。
# 注意：只登记进 resources（供死链判定），**不登记进 pages**——
# 否则 png 会被当成 md 页面，进而误报"无 frontmatter"和"孤立页面"。
for _attach in (os.path.join(ROOT, '.attachments'),):
    if os.path.isdir(_attach):
        for _fn in os.listdir(_attach):
            if _fn.endswith('.md'):
                _p = os.path.join(_attach, _fn)
                _rel = f'.attachments/{_fn}'
                if _rel not in pages:
                    try:
                        pages[_rel] = io.open(_p, encoding='utf-8').read()
                    except Exception:
                        pass
            else:
                assets_names = os.path.splitext(_fn)[0]
                RESOURCE_STEMS.add(assets_names)

# 非 md 资源（图片等），链接到它们不算死链
assets = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames
                   if d not in EXCLUDE_DIRS and d not in SKIP_DIRS
                   and d not in ARTIFACT_SUBDIRS]
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
    # ⭐ 图片等资源：Obsidian 里写作 [[目录导航图.png]]（2026-10-10 修正）
    # 原先只比对 assets（assets 存的是不带扩展名的 stem），
    # 导致 [[xxx.png]] 这种带扩展名的写法一律判成死链。
    for ext in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.pdf'):
        if base.lower().endswith(ext):
            if base[:-len(ext)] in assets:
                return 'ASSET'
            break
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

# ⭐ 不参与死链判定的文件（2026-10-10 修正）
# log.md 是操作流水，里面写的 [[xxx]] 是"我修了哪些链接"的记录文本，
# 不是真实链接；把它算进死链会让报告被自己的修复记录刷屏。
# 同理 wiki/meta/lint/ 是体检报告本身。
# ⭐ 无需 frontmatter 的操作性文件（2026-10-10）
# 这些是规则/流水/报告文件，不是知识页，不该被要求带元信息。
NO_FRONTMATTER_CHECK = {
    'CLAUDE.md', 'wiki/log.md',
    '从这里开始.md', '新手上手指南.md',
    'wiki/目录英文名对照表.md', 'wiki/index.md', 'wiki/hot.md',
}

NO_DEADLINK_CHECK = {'wiki/log.md'}
for _rel in pages:
    if _rel.startswith('wiki/meta/lint/'):
        NO_DEADLINK_CHECK.add(_rel)

# ⭐ 工具产出/历史页，不是知识页（2026-10-10 修正）
# meta/lint/ 是体检报告本身；superseded 页是历史存档。
# 两者都不该被要求"无孤立""有 frontmatter""登记进索引"。
NO_KNOWLEDGE_CHECK = {'wiki/log.md', 'wiki/hot.md'}
def is_tool_output(rel):
    return rel.startswith('wiki/meta/lint/')

outlinks = defaultdict(set)
deadlinks = defaultdict(list)
for rel, txt in pages.items():
    if not rel.startswith('wiki/'):
        continue
    if rel in NO_DEADLINK_CHECK:
        continue
    for m in LINK.finditer(txt):
        target = m.group(1)
        # 省略号占位（[[...]]、[[concepts/…]]）—— 记录里的示意，不是链接
        if '…' in target or target.strip() == '...':
            continue
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
if unreadable:
    print(f'（跳过 {len(unreadable)} 个不可读文件）')
    for rel, e in unreadable[:10]:
        print(f'  ⚠ {rel} — {e}')

# 1 孤立页面
print('\n【1】孤立页面（无入链且无出链）')
iso = []
for rel in pages:
    if os.path.basename(rel) == 'README.md':
        continue
    # ⭐ 工具产出/历史页/模板 不是知识页，孤立是正常的（2026-10-10）
    if is_tool_output(rel) or rel in NO_FRONTMATTER_CHECK or rel.startswith('templates/'):
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
    # ⭐ 操作性文件不是知识页，不要求带元信息（2026-10-10）
    if rel in NO_FRONTMATTER_CHECK or rel.startswith('templates/') or is_tool_output(rel):
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
# ⭐ 2026-10-14 精确化：区分「真占位」与「引用旧错的说明文字」
#    真占位 = 未完成清单里的 - [ ] xxx 待编译  或  明确的「待编译：」段落
#    误报   = 正文在引用/更正一个历史上的错误标注（如现场直憨页引用旧错）
print('\n【4】真占位页（存在未完成的待编译项）')
ph = []
# 4-1 未勾选的待编译任务项
pat_task = re.compile(r'^\s*-\s*\[\s\]\s*.*待编译', flags=re.M)
# 4-2 明确的待编译汇总行
pat_sum = re.compile(r'^\s*待编译[:：]', flags=re.M)
# 4-3 frontmatter 标记
pat_fm = re.compile(r'compiled_from:\s*pending', flags=re.M)
for rel, txt in pages.items():
    if re.search(r'^status:\s*superseded', txt, flags=re.M):
        continue
    if is_tool_output(rel):
        continue
    if rel in ('从这里开始.md', 'wiki/index.md', 'wiki/log.md'):
        continue
    if pat_task.search(txt) or pat_sum.search(txt) or pat_fm.search(txt):
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
    # 以下不是内容页，不应登记进索引
    # ⭐ meta/ 是台账与计划类（progress/skills/进度报告），它们会随每次运行重生成，
    #   登记进 index 只会造成永久性漂移噪音。2026-10-17 起排除。
    if rel.startswith('templates/') or rel == 'wiki/hot.md':
        continue
    if rel.startswith('wiki/meta/'):
        continue
    # ⭐ wiki/books/ 是 96 张阅读入口卡片，按分类目录自组织，
    #   逐条登记进 index.md 只会造成永久性漂移噪音（与 meta/ 同逻辑）。2026-10-19 起排除。
    if rel.startswith('wiki/books/'):
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