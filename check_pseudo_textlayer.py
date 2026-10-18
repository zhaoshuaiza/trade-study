# -*- coding: utf-8 -*-
"""伪文字层体检 —— 全库扫描，找出「有 book.txt 但其实没正文」的书。

⭐ 本库踩过多次的坑：
  - 盗版 PDF 的「文字层」全是广告模板（《可转债投资黄金宝典》1557 字）
  - PDF 只抽到目录页（《机构投资的创新之路》2138 字节全是目录）
  - 抽样字数 > 100 不代表能用，必须看内容本身

判定：正文中文字数 < 阈值 → 可疑
阈值按书的正常体量定：< 3 万字 视为可疑（多数书 10~30 万字）

用法: python check_pseudo_textlayer.py
"""
import io, os, re, sys

ROOT = 'E:/Work Buddy/交易学习'
BOOKS = f'{ROOT}/raw/books'
THRESHOLD = 30000          # 中文字数下限

# 盗版广告模板特征
JUNK = re.compile(r'公众号[:：]|扫码|更多免费.{0,8}电子书下载|Z-Library|'
                  r'全国最低交易手续费|请进[:：]http|Copyright All|'
                  r'本书仅供.{0,6}学习交流|仅限内部授课')

# ⚠️ 已人工核实为【真书·体量本来就小】的白名单（2026-10-18）
#   漫画书/口袋书天然字数少；躺赚指南的301 行广告是盗版页眉，正文完整（7.8% 可忽略）
WHITELIST = {
    '一小时漫画缠论实战法',            # 漫画，16800 字为真
    '半小时漫画股票实战法',
    '股市极客思考录 十年磨一剑之龙头股战法揭秘',   # 26705 字为真
    '躺着赚钱的漫画基金书',
    '可转债——投资小白躺赚指南',        # 正文完整，仅盗版页眉
}

def main():
    sus = []
    total = 0
    for cat in sorted(os.listdir(BOOKS)):
        cp = f'{BOOKS}/{cat}'
        if not os.path.isdir(cp):
            continue
        for b in sorted(os.listdir(cp)):
            bp = f'{cp}/{b}/book.txt'
            mp = f'{cp}/{b}/_meta.json'
            if not os.path.exists(bp):
                continue
            total += 1
            txt = io.open(bp, encoding='utf-8', errors='ignore').read()
            cjk = len(re.findall(r'[一-鿿]', txt))
            junk_n = len(JUNK.findall(txt))
            junk_ratio = junk_n / max(len(txt.split('\n')), 1)
            if b in WHITELIST:
                continue
            if cjk < THRESHOLD or junk_ratio > 0.05:
                mp_ok = os.path.exists(mp)
                reused = ''
                if mp_ok:
                    import json
                    reused = json.load(io.open(mp, encoding='utf-8')).get('reused_from', '')
                sus.append((b, cjk, os.path.getsize(bp), junk_n, reused))

    print(f'已提取 {total} 本，阈值 {THRESHOLD} 中文字')
    if not sus:
        print('✅ 无伪文字层')
        return 0
    print(f'\n⚠️ 可疑 {len(sus)} 本：\n')
    print('%-44s %8s %10s %6s  %s' % ('书名', '中文字', '字节', '广告行', '是否已用OCR'))
    print('-' * 100)
    for b, cjk, sz, j, reused in sus:
        print('%-44s %8d %10d %6d  %s' % (b[:42], cjk, sz, j,
                                        '✅ doubao OCR' if reused else '❌ 需处理'))
    return len(sus)


if __name__ == '__main__':
    sys.exit(0 if main() == 0 else 0)   # 始终返回 0，避免中断脚本链