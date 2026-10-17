# -*- coding: utf-8 -*-
"""建立每本书的独立工作文件夹 + 生成总进度台账。

目录结构:
  raw/books/<分类>/<书名slug>/
      book.txt        提取的正文（零OCR书=秒级，扫描件=OCR后写入）
      _meta.json      页数/来源/状态
用法: python init_book_dirs.py
"""
import io, os, csv, re, json

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
SURVEY = f'{BOOKS}/_survey.csv'


def slug(name):
    """书名 → 文件夹名：去掉(Z-Library)、括号补充说明、非法字符"""
    s = re.sub(r'\s*\([^)]*(?:Z-Library|ePUBw|etc\.)[^)]*\)', '', name)
    s = re.sub(r'[（(][^）)]*[）)]', lambda m: m.group(0), s)   # 保留中文括号
    s = re.sub(r'[\\/:*?"<>|]', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' .-')
    return s[:60]


def main():
    rows = list(csv.DictReader(io.open(SURVEY, encoding='utf-8-sig')))
    seen = {}
    made = 0
    for r in rows:
        cat = r['category'].split('_', 1)[-1] if '_' in r['category'] else r['category']
        name = r['book']
        # 同一本书常有 pdf+epub+pdf 三份，按书名去重，只建一个目录
        key = slug(name)
        if key in seen:
            r['dir'] = seen[key]
        else:
            d = f'{BOOKS}/{cat}/{key}'
            os.makedirs(d, exist_ok=True)
            meta = {
                'book': name, 'category': r['category'],
                'kind': r['kind'], 'pages': int(r['pages'] or 0),
                'verdict': r['verdict'], 'files': [r['file']],
            }
            json.dump(meta, io.open(f'{d}/_meta.json', 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=2)
            seen[key] = d
            r['dir'] = d
            made += 1
        # 同一本书的其它格式，登记进 _meta.json 的 files
        mp = f'{r["dir"]}/_meta.json'
        m = json.load(io.open(mp, encoding='utf-8'))
        if r['file'] not in m['files']:
            m['files'].append(r['file'])
            if r['kind'] == 'EPUB' and m['kind'] != 'EPUB':
                m['prefer'] = 'epub'          # 标记优先用零OCR格式
            json.dump(m, io.open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    with io.open(f'{BOOKS}/_dirs.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['category', 'book', 'kind', 'pages',
                                          'verdict', 'dir', 'file'])
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in
                        ['category', 'book', 'kind', 'pages', 'verdict', 'dir', 'file']})
    print(f'建立 {made} 个书目录 -> {BOOKS}')
    print(f'登记 {len(rows)} 个文件条目')


if __name__ == '__main__':
    main()