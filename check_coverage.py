# -*- coding: utf-8 -*-
"""源书覆盖率体检：找出源书里高频出现、但库内尚无对应页面的术语。

方法（保守，宁可漏报不可误报）：
1. 从源书全文统计候选术语（中文 3~6 字、频率高）
2. 用「去停用词 + 去除已在库内出现的词」筛出候选
3. 人工/agent 复核后决定是否建页

⚠️ 本脚本只【报候选】，不自动建页（建页需人工判断，避免制造垃圾页）。
"""
import io, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'raw', 'distilled')
WIKI = os.path.join(ROOT, 'wiki')

SOURCES = {
    '量柱擒涨停': '量柱擒涨停-OCR-简体.txt',
    '量线捉涨停': '量线捉涨停-OCR-简体.txt',
    '操盘手记1': '操盘手记-OCR-简体.txt',
    '操盘手记2': '操盘手记2-2-OCR-简体.txt',
    '操盘手记3': '操盘手记3-3-OCR-简体.txt',
    '操盘手记4': '操盘手记4-4-OCR-简体.txt',
    '操盘手记5': '操盘手记5-5-OCR-简体.txt',
    '盘口解读': '盘口解读-OCR-简体.txt',
    '缠论108课': '缠论108课详解-OCR-简体.txt',
    '战胜华尔街': '战胜华尔街-OCR-简体.txt',
}

# 广告模板行，必须先剔除，否则全是噪声
NOISE = re.compile(r'全国最低交易手续费|任何地方费用比我们低|期货开户和书籍下载|'
                   r'客服QQ微信|^=== 第\d+页 ===$|^\d{3}$')

MIN_FREQ = 30
MAXLEN = 6


def load_all_wiki_text():
    buf = []
    for dp, dn, fn in os.walk(WIKI):
        for f in fn:
            if f.endswith('.md'):
                try:
                    buf.append(io.open(os.path.join(dp, f), encoding='utf-8').read())
                except Exception:
                    pass
    return '\n'.join(buf)


def main():
    wiki = load_all_wiki_text()
    print('=' * 60)
    print('源书术语覆盖率体检（候选：源书高频 + 库内未见）')
    print('=' * 60)
    report = {}
    for name, fn in SOURCES.items():
        p = os.path.join(DIST, fn)
        if not os.path.exists(p):
            print(f'\n[{name}] ⚠ 文件不存在，跳过: {fn}')
            continue
        raw = io.open(p, encoding='utf-8').read()
        lines = [l for l in raw.split('\n') if not NOISE.search(l)]
        text = '\n'.join(lines)
        # 只保留中文串
        cands = Counter(re.findall(r'[\u4e00-\u9fff]{3,%d}' % MAXLEN, text))
        missing = []
        for term, n in cands.items():
            if n < MIN_FREQ:
                continue
            # 库内已出现（含页面标题、frontmatter、正文）→ 视为已覆盖
            if term in wiki:
                continue
            missing.append((term, n))
        missing.sort(key=lambda x: -x[1])
        report[name] = missing
        print(f'\n[{name}] 源书 {len(text)} 字，候选未覆盖术语 {len(missing)} 个：')
        for t, n in missing[:25]:
            print(f'   {n:>4}次  {t}')
    out = os.path.join(ROOT, 'wiki', 'meta', 'lint', '术语覆盖率报告.md')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    lines = ['# 源书术语覆盖率报告', '',
             f'> 由 `check_coverage.py` 生成于 {time_str()}',
             '> ⚠️ 本报告只列**候选**，需人工/Agent 复核后决定是否建页。', '']
    for name, missing in report.items():
        lines.append(f'## {name}（{len(missing)} 个候选）')
        lines.append('')
        lines.append('| 词 | 源书频次 |')
        lines.append('|---|---|')
        for t, n in missing[:40]:
            lines.append(f'| {t} | {n} |')
        lines.append('')
    io.open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'\n✓ 报告已写出: {out}')


def time_str():
    import datetime
    return datetime.date.today().isoformat()


if __name__ == '__main__':
    main()