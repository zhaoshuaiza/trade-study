# -*- coding: utf-8 -*-
"""建立精读/蒸馏分类目录，归位产物。"""
import os, shutil

base = r'E:\Work Buddy\交易学习'
jingdu = os.path.join(base, '精读')
zhengliu = os.path.join(base, '蒸馏')
os.makedirs(jingdu, exist_ok=True)
os.makedirs(zhengliu, exist_ok=True)

# 1. 把4个概念页从 wiki/concepts/ 移到 精读/
concepts = [
    '止损纪律的心理基础.md',
    '亚当理论十大交易守则.md',
    'MACD实战原则.md',
    '波浪理论的实用边界.md',
]
for c in concepts:
    src = os.path.join(base, 'wiki', 'concepts', c)
    dst = os.path.join(jingdu, c)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f'  精读 <- {c}')

# 2. 蒸馏/ README
books = [
    ('止损：如何克服贪婪和恐惧', 226, 123246, '止损 如何克服贪婪和恐惧-OCR-简体.txt'),
    ('亚当理论', 193, 68322, '亚当理论-OCR-简体.txt'),
    ('MACD指标精讲', 253, 120102, 'MACD指标精讲-OCR-简体.txt'),
    ('股市波浪派手册', 141, 52012, '股市波浪派手册-OCR-简体.txt'),
    ('股市稳赚', 128, 72681, '股市稳赚-OCR-简体.txt'),
]
lines = ['# 蒸馏目录', '', 'PDF→文本蒸馏阶段的产物索引。', '',
         '## 实际文本位置',
         '- OCR全文：raw/distilled/*-OCR-简体.txt',
         '- 零OCR直抽全文：raw/distilled/*-全文.txt',
         '- cangjie工作目录：books/{编号}-{拼音}/', '',
         '## 本批次已蒸馏书目']
for name, pages, chars, fn in books:
    lines.append(f'- **{name}**（{pages}页/{chars}字符）→ raw/distilled/{fn}')
with open(os.path.join(zhengliu, 'README.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

# 3. 精读/ README
jdlines = ['# 精读目录', '', '文本→知识精读阶段的产物（概念页、判据页）。', '',
           '## 本批次已精读书目']
for c in concepts:
    jdlines.append(f'- [[{c[:-3]}]]')
with open(os.path.join(jingdu, 'README.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(jdlines))

print('\n✅ 归位完成')
print('精读/:', os.listdir(jingdu))
print('蒸馏/:', os.listdir(zhengliu))
