# -*- coding: utf-8 -*-
"""汇总 8 段精读的三张专名表，生成全书复核版索引（只增不改、不覆盖底稿）。"""
import io, os, re, glob, collections

BASE = r'E:/Work Buddy/交易学习/raw/distilled'
SEG = BASE + '/月风-精读段'
DRAFT = BASE + '/月风-全书提及书目与人物索引.md'
OUT = BASE + '/月风-全书提及书目与人物索引-复核版.md'

TABLE_NAMES = ['书籍 / 著作 / 理论', '人物', '机构与其它专名']


def norm(s):
    return re.sub(r'[《》〈〉「」『』\s·．.、,，:：;；()（）\-—_"\'\*]', '', s)


def clean(s):
    return s.strip().replace('|', r'\|').replace('\n', ' ')


rows = [collections.OrderedDict() for _ in range(3)]   # 每张表: name -> record
raw_counts = [0, 0, 0]
per_seg = {}

for f in sorted(glob.glob(SEG + '/段*-精读.md')):
    seg = os.path.basename(f)[:3]
    t = io.open(f, encoding='utf-8').read()
    sec = t.split('## 三、', 1)[1].split('## 四、', 1)[0]
    blocks = re.split(r'^### ', sec, flags=re.M)[1:]
    assert len(blocks) == 3, (seg, len(blocks))
    counts = []
    for ti, blk in enumerate(blocks):
        n = 0
        for line in blk.splitlines():
            line = line.strip()
            if not line.startswith('|'):
                continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) < 4 or cells[0] in ('名称', '') or set(cells[0]) <= set('-: '):
                continue
            name, quote, page, role = cells[0], cells[1], cells[2], cells[3]
            n += 1
            rec = rows[ti].setdefault(name, {'quotes': [], 'pages': [], 'roles': []})
            if quote not in rec['quotes']:
                rec['quotes'].append(quote)
            rec['pages'].append('%s:%s' % (seg, page))
            if role not in rec['roles']:
                rec['roles'].append(role)
        raw_counts[ti] += n
        counts.append(n)
    per_seg[seg] = counts

# 疑似异文：规范化后同名但不完全同字，仅提示不合并
alias = []
for ti in range(3):
    g = collections.defaultdict(list)
    for nm in rows[ti]:
        g[norm(nm)].append(nm)
    for k, v in g.items():
        if len(v) > 1:
            alias.append((ti, sorted(v)))

# 底稿对照
draft_names = collections.defaultdict(set)
if os.path.exists(DRAFT):
    dt = io.open(DRAFT, encoding='utf-8').read()
    cur = None
    for line in dt.splitlines():
        m = re.match(r'^##\s+(.*)', line.strip())
        if m:
            h = m.group(1)
            if h.startswith('一') or '书籍' in h or '著作' in h:
                cur = 0
            elif h.startswith('二') or '人物' in h:
                cur = 1
            elif h.startswith('三') or '机构' in h or '专名' in h:
                cur = 2
            else:
                cur = None
        if cur is not None and line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells and cells[0] not in ('名称', '项', '') and not re.fullmatch(r'[-: |]*', cells[0]):
                draft_names[cur].add(cells[0])

allnorm = [set(norm(n) for n in rows[ti]) for ti in range(3)]
unmatched = [[n for n in sorted(draft_names[ti]) if norm(n) not in allnorm[ti]] for ti in range(3)]

buf = []
buf.append('---')
buf.append('title: 月风《股市投机战法》全书提及书目与人物索引（复核版）')
buf.append('material_level: 原书 OCR 全文逐页精读（914 页全覆盖）')
buf.append('status: draft')
buf.append('核验级别: 已回 OCR 全文页核验；**未逐条对照原始扫描页图**')
buf.append('生成方式: 由 8 段逐页精读文件的三张专名表机械汇总，同名精确合并出处，异文不合并')
buf.append('---')
buf.append('')
buf.append('# 月风《股市投机战法》全书提及书目与人物索引 · 复核版')
buf.append('')
buf.append('> 来源：`raw/distilled/月风-精读段/段01~08-精读.md`，覆盖上册 PDF p1-458 + 下册 p1-456，共 914 页逐页精读。')
buf.append('> 与底稿 `月风-全书提及书目与人物索引.md`（97 条，来自抽样精读笔记）**并存不覆盖**。')
buf.append('> 铁律：原文摘录逐字照录；原文未载即写「原文未载」；**不用训练数据补作者/身份/出版信息**；书名/译名异文分行不合并、不做同一性判定；不裁决观点冲突；不给投资建议。')
buf.append('> ⚠️ 核验级别说明：每条已能定位到具体 PDF 页并附原书摘录，属 **OCR 全文级**；图内文字、手写批注、OCR 错字可能影响识别，尚未逐条回原始扫描页图复核。')
buf.append('')

for ti, tname in enumerate(TABLE_NAMES):
    buf.append('## %s %s' % ('①②③'[ti], tname))
    buf.append('')
    buf.append('| 名称 | 原文摘录（逐字） | 出现位置（段:PDF页） | 原书定位（只用原文措辞） |')
    buf.append('| --- | --- | --- | --- |')
    for nm, rec in rows[ti].items():
        q = max(rec['quotes'], key=len) if rec['quotes'] else '原文未载'
        pages = '、'.join(dict.fromkeys(rec['pages']))
        role = '；'.join(dict.fromkeys(rec['roles']))
        buf.append('| %s | %s | %s | %s |' % (clean(nm), clean(q), clean(pages), clean(role)))
    buf.append('')
    buf.append('小计：**%d** 个名称（异文分行计），来自 8 段共 %d 条登记。' % (len(rows[ti]), raw_counts[ti]))
    buf.append('')

buf.append('## 四、统计')
buf.append('')
buf.append('| 表 | 唯一名称数（异文分行） | 8 段登记总条数 |')
buf.append('| --- | --- | --- |')
for ti, tname in enumerate(TABLE_NAMES):
    buf.append('| %s %s | %d | %d |' % ('①②③'[ti], tname, len(rows[ti]), raw_counts[ti]))
buf.append('| **合计** | **%d** | **%d** |' % (sum(len(r) for r in rows), sum(raw_counts)))
buf.append('')
buf.append('各段登记条数（书籍 / 人物 / 机构专名）：')
buf.append('')
buf.append('| 段 | 册 | PDF 页范围 | 书籍 | 人物 | 机构专名 |')
buf.append('| --- | --- | --- | --- | --- | --- |')
segmeta = [('01', '上', 'p1-114'), ('02', '上', 'p115-229'), ('03', '上', 'p230-343'),
           ('04', '上', 'p344-458'), ('05', '下', 'p1-114'), ('06', '下', 'p115-228'),
           ('07', '下', 'p229-342'), ('08', '下', 'p343-456')]
for s, b, rng in segmeta:
    c = per_seg.get('段' + s, [0, 0, 0])
    buf.append('| %s | %s | %s | %d | %d | %d |' % (s, b, rng, c[0], c[1], c[2]))
buf.append('')

buf.append('## 五、疑似异文（仅提示，**不合并、不做同一性判定**）')
buf.append('')
buf.append('规则：去除书名号与标点后字面相同。是否同指一书/一人，留待单独讨论。')
buf.append('')
for ti, group in alias:
    buf.append('- %s：%s' % (TABLE_NAMES[ti], ' ／ '.join(group)))
if not alias:
    buf.append('- 无')
buf.append('')

buf.append('## 六、底稿对照（底稿 97 条 → 全书 OCR 复核）')
buf.append('')
buf.append('下列为**底稿中出现、但全书 OCR 全文三表未以同名命中**的条目。⚠️ 主要成因是**登记口径差异**：底稿把异文合并成一条（如「杰西·利弗莫尔（利弗莫尔／杰西）」），复核版按原文写法分行登记，故字面无法同名命中；另有 OCR 错字、底稿为二手转述或图内文字未识别等可能。**只登记，不判错、不删除、不等于漏抽**。')
buf.append('')
for ti, tname in enumerate(TABLE_NAMES):
    buf.append('### %s %s（%d 条未同名命中）' % ('①②③'[ti], tname, len(unmatched[ti])))
    buf.append('')
    if unmatched[ti]:
        for n in unmatched[ti]:
            buf.append('- %s' % n)
    else:
        buf.append('- 无')
    buf.append('')

buf.append('## 七、后记推荐书单（用户专门要研究的索引）')
buf.append('')
buf.append('完整书单见 `段08-精读.md`「后记 / 推荐书单」节：下册 p456（印刷页 906），共 28 本书 + 1 条异文《大作手回忆录》、15 位作者，【重点】12 处、【重中之重】2 处，已逐条照录含作者括注。')
buf.append('本表已按「① 书籍 / 著作 / 理论」汇总收录，可用 PDF 页码 `段08:p456` 筛选。')
buf.append('')
buf.append('## 八、待办')
buf.append('')
buf.append('- 逐条回原始扫描页图核验（尤其图内文字、OCR 错字、推荐书单作者名）。')
buf.append('- 书目逐本对照库内已有 sources 页，出「已入库 / 缺书」清单（待用户拍板）。')
buf.append('- 与库内既有结论的冲突单独讨论，本文件不裁决。')

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(buf) + '\n')
print('输出', OUT)
print('唯一名称', [len(r) for r in rows], '登记总条数', raw_counts)
print('疑似异文组', len(alias))
print('底稿未同名命中', [len(x) for x in unmatched])
