# -*- coding: utf-8 -*-
"""从 doubao 项目复用已完成的 OCR 文本，填到raw/books/ 各书目录的 book.txt

⭐ 为什么复用：E:/doubao/电子书蒸馏项目/转换文字版/OCR/ 已有 17 本 OCR 全文，
   且那边已把 98 本蒸馏成 323 个技能包并记录了跳过理由。
   重跑 OCR 是纯浪费。

用法: python reuse_doubao.py
"""
import io, os, re, json, shutil, glob

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
DONBAO = 'E:/doubao/电子书蒸馏项目/转换文字版/OCR'


def norm(s):
    return re.sub(r'[^\w一-鿿]', '', s)


def main():
    if not os.path.isdir(DONBAO):
        print(f'❌ 源目录不存在: {DONBAO}')
        return

    # 载入 doubao OCR 文本，按规范化名索引
    pool = []
    for f in os.listdir(DONBAO):
        if not f.endswith('.txt') or f.startswith('_'):
            continue
        p = os.path.join(DONBAO, f)
        cjk = len(re.findall(r'[一-鿿]', io.open(p, encoding='utf-8', errors='ignore').read()))
        pool.append({'key': norm(f[:-4])[:14], 'name': f, 'path': p, 'cjk': cjk})
    print(f'源 OCR 文本 {len(pool)} 本\n')

    hit, miss = [], []
    for cat in sorted(os.listdir(BOOKS)):
        cp = f'{BOOKS}/{cat}'
        if not os.path.isdir(cp):
            continue
        for b in sorted(os.listdir(cp)):
            mp = f'{cp}/{b}/_meta.json'
            if not os.path.exists(mp):
                continue
            m = json.load(io.open(mp, encoding='utf-8'))
            if os.path.exists(f'{cp}/{b}/book.txt'):
                continue                      # 已有正文
            kb = norm(m.get('book', b))[:14]
            # ⭐ 必须唯一匹配：多候选时判为歧义，拒绝复用（防两本不同的书记同一份文本）
            exact = [x for x in pool if x['key'] == kb]
            loose = [x for x in pool if x not in exact and (kb[:8] in x['key'] or x['key'][:8] in kb)]
            cand_list = exact or loose
            uniq = {x['path'] for x in cand_list}
            if len(uniq) > 1:
                miss.append(f"{m.get('book')}（{len(uniq)}个候选，歧义）")
                continue
            if not cand_list:
                miss.append(m.get('book', b))
                continue
            cand = cand_list[0]
            # ⭐ 防清零铁律：复制前校验非空
            if cand['cjk'] < 2000:
                miss.append(f"{m.get('book')}（源仅{cand['cjk']}字）")
                continue
            shutil.copyfile(cand['path'], f'{cp}/{b}/book.txt')
            m.update({'chars': os.path.getsize(cand['path']), 'cjk': cand['cjk'],
                      'extract_status': 'ok', 'reused_from': cand['path'],
                      'note': '复用 doubao 已完成 OCR，未重跑'})
            json.dump(m, io.open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            hit.append((m.get('book', b), cand['cjk']))
            print(f'  ✅ {m.get("book", b)[:40]:42} ← {cand["cjk"]}字')

    print(f'\n复用 {len(hit)} 本')
    if miss:
        print(f'仍缺 {len(miss)} 本：')
        for x in miss:
            print(f'   - {x}')


if __name__ == '__main__':
    main()