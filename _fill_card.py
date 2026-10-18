# -*- coding: utf-8 -*-
"""替换书籍卡片中「## 二、⏳ 精读总结（待填充）」到文件结尾的整节内容。
用法：python _fill_card.py <书名md> <新内容.md>
新内容.md 需包含「## 二、精读总结」及之后的全部内容（含 ## 三、关联）。
"""
import sys, os

BOOKS = os.path.join(os.path.dirname(__file__), 'wiki', 'books', '01价值投资')
MARK = '## 二、⏳ 精读总结（待填充）'

card = os.path.join(BOOKS, sys.argv[1])
new = open(sys.argv[2], encoding='utf-8').read().strip()

s = open(card, encoding='utf-8').read()
i = s.index(MARK)
# 保留到 MARK 之前的内容（含分隔线），其后全部替换
head = s[:i].rstrip()
# 去掉 head 结尾多余的 "---"
if head.endswith('---'):
    head = head[:-3].rstrip()
out = head + '\n\n---\n\n' + new + '\n'
open(card, 'w', encoding='utf-8').write(out)
print('filled:', sys.argv[1])
