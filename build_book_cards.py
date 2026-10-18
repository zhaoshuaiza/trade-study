# -*- coding: utf-8 -*-
"""生成书籍卡片页骨架 —— 每本书一张，便于日后按书阅读。

卡片页放wiki/books/<分类>/<书名>.md
字段：存储位置（提取物 + 原始文件）+ 状态 + 留空区供精读填充

用法:
  python build_book_cards.py          # 只建骨架（已存在则跳过）
  python build_book_cards.py --force  # 重建（会覆盖已填内容，慎用）
"""
import io, os, re, json, csv

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
CARDS = f'{ROOT}/wiki/books'
SRCROOT = 'E:/电子书/202061010投资电子书'
MANIFEST = f'{BOOKS}/_manifest.json'

TPL = """---
type: book
status: skeleton
source_id: {sid}
category: {cat}
chars: {cjk}
source_files: [{files}]
read_at: {dir}
created: 2026-10-18
tags: [书籍卡片, {tag}]
---

# {title}

> 📍 **本文是这一本书的阅读入口。**
> 总结、判据、与本库其它页的关系，都收在这里。

---

## 一、📍 存储位置

| 项 | 位置 |
|---|---|
| **提取正文** | <br>`{txtpath}`（{cjk} 字）|
| **原始文件** | {srclines} |
| **元数据** | `{dir}_meta.json` |
| **隔离目录** | `raw/books/{cat}/` |

---

## 二、⏳ 精读总结（待填充）

> 精读后填写：这本书的核心判据、适用边界、坑在哪。

---

## 三、关联

- 概念页：
- 来源页：
- 冲突页：
"""

def slug(s):
    return re.sub(r'[\\/:*?"<>|]', '', s).strip()[:70]


def main():
    force = '--force' in os.sys.argv
    os.makedirs(CARDS, exist_ok=True)
    # 读 survey 拿原始文件路径
    sv = {}
    p = f'{BOOKS}/_survey.csv'
    if os.path.exists(p):
        for r in csv.DictReader(io.open(p, encoding='utf-8-sig')):
            sv.setdefault(r['book'], []).append(r['file'])

    n = 0
    made = []
    for cat in sorted(os.listdir(BOOKS)):
        cp = f'{BOOKS}/{cat}'
        if not os.path.isdir(cp):
            continue
        catname = cat.split('_', 1)[-1] if '_' in cat else cat
        for b in sorted(os.listdir(cp)):
            bd = f'{cp}/{b}'
            mp = f'{bd}/_meta.json'
            tp = f'{bd}/book.txt'
            if not os.path.exists(mp):
                continue
            m = json.load(io.open(mp, encoding='utf-8'))
            if not os.path.exists(tp):
                continue      # 无正文的不建卡
            txt = io.open(tp, encoding='utf-8', errors='ignore').read()
            cjk = len(re.findall(r'[一-鿿]', txt))
            card_dir = f'{CARDS}/{catname}'
            os.makedirs(card_dir, exist_ok=True)
            cpath = f'{card_dir}/{slug(b)}.md'
            if os.path.exists(cpath) and not force:
                continue
            title = m.get('book', b)
            files = sv.get(title, m.get('files', []))
            srclines = '\n'.join(
                f'  - `E:/电子书/202061010投资电子书/{f}`' for f in files) or '  —'
            txtpath = f'raw/books/{cat}/{b}/book.txt'
            dirdisplay = f'`raw/books/{cat}/{b}/`'
            page = TPL.format(
                sid=b, cat=catname, cjk=cjk,
                files=', '.join(files) if files else '',
                dir=f'raw/books/{cat}/{b}/',
                tag=catname, title=title,
                srclines=srclines, txtpath=txtpath, dirdisplay=dirdisplay)
            io.open(cpath, 'w', encoding='utf-8').write(page)
            made.append((catname, title, cjk, cpath))
            n += 1

    print(f'建立 {n} 张卡片 -> {CARDS}')
    for cat, title, cjk, cp in made[:6]:
        print(f'  {cat}/{title[:30]}  {cjk}字')
    if len(made) > 6:
        print(f'  ...共 {len(made)} 张')


if __name__ == '__main__':
    main()