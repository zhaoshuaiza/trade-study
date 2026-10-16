#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按页号合并 OCR 分片，容忍分片区间重叠。

事故背景（2026-10-16）：ocr_book.py 断点续传时起点会 +1 偏移，
导致分片名变成 p0001-0010 / p0002-0011 / p0011-0020 ...，
相邻分片重叠 1 页，ocr_book.py 自带的重复页检查正确中止、未写出错误全文。

本脚本按「页号」而非「文件名」归并，因此对任意重叠都安全：
  同一页出现在多个分片时，取正文最长的一份。

⭐ 铁律：写入前必须校验非空，且打印重叠/缺失统计。绝不在空输入时写出文件。
用法: python merge_shards_safe.py <分片目录> <输出txt>
"""
import os, re, sys, glob

PAGE_RE = re.compile(r'===\s*第\s*(\d+)\s*页\s*===')

def parse_shard(path):
    """返回 {pageno: text}"""
    t = open(path, encoding='utf-8', errors='ignore').read()
    parts = PAGE_RE.split(t)
    # parts = [前导, 页号1, 内容1, 页号2, 内容2, ...]
    pages = {}
    for i in range(1, len(parts) - 1, 2):
        try:
            no = int(parts[i])
        except ValueError:
            continue
        pages[no] = parts[i + 1]
    return pages

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    sdir, out = sys.argv[1], sys.argv[2]
    if not os.path.isdir(sdir):
        print(f"⛔ 分片目录不存在: {sdir}")
        sys.exit(1)

    files = sorted(glob.glob(os.path.join(sdir, "*.txt")))
    if not files:
        print(f"⛔ 分片目录为空: {sdir}")
        sys.exit(1)

    merged = {}      # pageno -> text
    dup = 0          # 重复页计数
    conflict = 0     # 重复页内容长度不一致的计数
    for fp in files:
        for no, txt in parse_shard(fp).items():
            if no in merged:
                dup += 1
                if len(txt) != len(merged[no]):
                    conflict += 1
                if len(txt) > len(merged[no]):
                    merged[no] = txt   # 取更完整的一份
            else:
                merged[no] = txt

    if not merged:
        print("⛔ 解析结果为空，拒绝写出（这是防零内容事故的闸门）")
        sys.exit(1)

    total_chars = sum(len(v) for v in merged.values())
    print(f"分片数   : {len(files)}")
    print(f"解析页数 : {len(merged)}")
    print(f"重复页数 : {dup}" + (f"（⚠️ 其中 {conflict} 页内容长度不一致，已取最长）" if conflict else ""))
    if merged:
        lo, hi = min(merged), max(merged)
        missing = [n for n in range(lo, hi + 1) if n not in merged]
        print(f"页号范围 : {lo}~{hi}")
        print(f"缺失页   : {len(missing)}" + (f" -> {missing[:30]}" if missing else ""))

    if total_chars < 5000:
        print(f"⛔ 总字数仅 {total_chars}，判定为异常，拒绝写出")
        sys.exit(1)

    buf = []
    for no in sorted(merged):
        buf.append(f"\n\n===== 第{no}页 =====\n" + merged[no])
    text = "".join(buf)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✅ 已写出: {out}  共 {len(text)} 字符 / {len(merged)} 页")

if __name__ == '__main__':
    main()