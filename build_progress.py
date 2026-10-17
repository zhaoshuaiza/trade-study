# -*- coding: utf-8 -*-
"""蒸馏进度总台账 —— 自动扫raw/books/*/*/ 生成 wiki/meta/progress/书籍蒸馏进度.md

四态判定（依 _meta.json 的 extract_status + book.txt 是否存在 + 库内是否已有来源页）:
  待提取 → 已提取 → 待编译 → 已编译

用法: python build_progress.py
"""
import io, os, re, json, csv
from datetime import datetime

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
OUT = f'{ROOT}/wiki/meta/progress'
os.makedirs(OUT, exist_ok=True)


def norm(s):
    return re.sub(r'[^\w一-鿿]', '', s)


def load_wiki_blob():
    blob = []
    for dp, dn, fn in os.walk(f'{ROOT}/wiki'):
        for f in fn:
            if f.endswith('.md'):
                blob.append(norm(f[:-3]))
                try:
                    blob.append(norm(io.open(os.path.join(dp, f),
                                            encoding='utf-8').read()[:4000]))
                except Exception:
                    pass
    return '\n'.join(blob)


def in_wiki(blob, name, extra):
    """库内是否已有该书的来源页/概念页提及"""
    key = norm(name)[:8]
    if key and key in blob:
        return True
    for e in extra:
        if e and norm(e)[:8] in blob:
            return True
    return False


def main():
    blob = load_wiki_blob()
    rows = []
    for cat in sorted(os.listdir(BOOKS)):
        cp = f'{BOOKS}/{cat}'
        if not os.path.isdir(cp):
            continue
        for b in sorted(os.listdir(cp)):
            mp = f'{cp}/{b}/_meta.json'
            if not os.path.exists(mp):
                continue
            m = json.load(io.open(mp, encoding='utf-8'))
            bp = f'{cp}/{b}/book.txt'
            has_txt = os.path.exists(bp)
            chars = m.get('chars', 0)
            cjk = m.get('cjk', 0)
            est = m.get('extract_status', '')
            # 作者名/别名，便于匹配库内已有页
            aliases = []
            if 'series' in m:
                aliases.append(m['series'])
            done_wiki = in_wiki(blob, m.get('book', b), aliases)

            if done_wiki:
                state = '已编译'
            elif has_txt and cjk > 2000:
                state = '待编译'
            elif has_txt:
                state = '待编译(字少)'
            elif est == 'fail':
                state = '提取失败'
            elif m.get('kind') == '扫描PDF' or m.get('verdict') == '需OCR':
                state = '待OCR'
            else:
                state = '待提取'
            rows.append({
                'cat': cat, 'dir': b, 'book': m.get('book', b),
                'kind': m.get('kind', ''), 'pages': m.get('pages', 0),
                'cjk': cjk, 'state': state,
                'note': m.get('extract_error', '') or '',
            })

    ORDER = ['待OCR', '待提取', '提取失败', '待编译', '待编译(字少)', '已编译']
    # ⭐ 已按CLAUDE.md 零之二判定为「非交易内容，应进hedge 库」的书
    DIVERTED = {
        '乌合之众', '小狗钱钱', '小岛经济学', '繁荣与衰退',
        '赢 有钱人和你想的不一样', '伟大的博弈', '大癫狂', '客户的游艇在哪里',
    }
    cnt = {}
    for r in rows:
        cnt[r['state']] = cnt.get(r['state'], 0) + 1
    # 分流计数
    div = [r for r in rows if any(d in r['book'] for d in DIVERTED)]

    L = []
    L.append('# 📊 书籍蒸馏进度总台账')
    L.append('')
    L.append(f'> 自动生成：`python build_progress.py`　最后更新 {datetime.now():%Y-%m-%d %H:%M}')
    L.append(f'> 源目录：`E:/电子书/202061010投资电子书`　隔离目录：`raw/books/<分类>/<书名>/`')
    L.append('')
    L.append('## 总览')
    L.append('')
    L.append('| 状态 | 本数 | 含义 |')
    L.append('|---|---|---|')
    MEAN = {
        '待OCR': '扫描版 PDF，必须 OCR 才能提文本',
        '待提取': '有零OCR格式（epub/mobi），尚未提取',
        '提取失败': '提取报错，需人工介入',
        '待编译': '文本已就绪，等读完后建概念页',
        '待编译(字少)': '文本偏少，可能是公版/目录型书，需人工判断',
        '已编译': '库内已有对应来源页或概念页',
    }
    for s in ORDER:
        L.append(f'| {s} | {cnt.get(s,0)} | {MEAN[s]} |')
    L.append(f'| **已分流 hedge** | **{len(div)}** | 非交易内容，按 `CLAUDE.md` 零之二不入交易库 |')
    L.append(f'| **合计** | **{len(rows)}** | — |')
    L.append('')
    done = cnt.get('已编译', 0)
    real = done + len(div)
    L.append(f'**完成率：{real}/{len(rows)} = {real*100//max(len(rows),1)}%**'
             f'（已编译 {done} + 已分流 {len(div)}）')
    L.append('')
    if div:
        L.append('### 已分流到 hedge 库的书（判定依据：不能落成「看盘时用得上的动作」）')
        L.append('')
        for r in div:
            L.append(f'- {r["book"]}')
        L.append('')

    for s in ORDER:
        sub = [r for r in rows if r['state'] == s]
        if not sub:
            continue
        L.append(f'## {s}（{len(sub)}）')
        L.append('')
        bycat = {}
        for r in sub:
            bycat.setdefault(r['cat'], []).append(r)
        for cat in sorted(bycat):
            L.append(f'### {cat}')
            L.append('')
            L.append('| 书名 | 格式 | 页数 | 字数 | 目录 |')
            L.append('|---|---|---|---|---|')
            for r in sorted(bycat[cat], key=lambda x: x['book']):
                rel = r['dir'].replace('\\', '/')
                L.append(f"| {r['book']} | {r['kind']} | {r['pages'] or '-'} | "
                         f"{r['cjk'] or '-'} | `{rel}` |")
            L.append('')

    p = f'{OUT}/书籍蒸馏进度.md'
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L))

    with io.open(f'{BOOKS}/_progress.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f'台账已更新: {p}')
    for s in ORDER:
        if cnt.get(s):
            print(f'  {s:12} {cnt[s]}')
    print(f'  完成率 {done}/{len(rows)} = {done*100//max(len(rows),1)}%')


if __name__ == '__main__':
    main()