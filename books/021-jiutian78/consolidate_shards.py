# -*- coding: utf-8 -*-
"""021 酒田78条：OCR 分片合并为 source.txt（OCR 全部完成后运行）。
分片命名 p0001-0010.txt ... p0371-0380.txt，按页码数值排序拼接。
用法: python consolidate_shards.py            # 全部就位则合并
      python consolidate_shards.py --check    # 只检查缺哪些分片
"""
import io, os, re, sys

BASE = "E:/Work Buddy/交易学习/raw/distilled"
SHARD_DIR = os.path.join(BASE, "jiutian78_shards")
OUT = "E:/Work Buddy/交易学习/books/021-jiutian78/source.txt"
TOTAL_PAGES = 375
CHUNK = 10

def expected_shards():
    out = []
    for s in range(1, TOTAL_PAGES + 1, CHUNK):
        e = min(s + CHUNK - 1, TOTAL_PAGES)
        out.append(f"p{s:04d}-{e:04d}.txt")
    return out

def page_of(name):
    m = re.match(r"p(\d+)-\d+\.txt", name)
    return int(m.group(1)) if m else -1

def main():
    check = "--check" in sys.argv
    have = {f for f in os.listdir(SHARD_DIR) if re.match(r"p\d{4}-\d{4}\.txt", f)} if os.path.isdir(SHARD_DIR) else set()
    exp = expected_shards()
    missing = [f for f in exp if f not in have]
    extra = sorted(have - set(exp))
    print(f"分片目录: {SHARD_DIR}")
    print(f"已有 {len(have)}/{len(exp)} 个分片；缺 {len(missing)} 个")
    if missing:
        print("缺失:", ", ".join(missing))
    if extra:
        print("额外(不在预期范围):", ", ".join(extra))
    if check or missing:
        return
    parts = [f"=== 分片来源: {f} ===" for f in []]
    buf = []
    for f in sorted(have, key=page_of):
        with io.open(os.path.join(SHARD_DIR, f), encoding="utf-8") as fh:
            buf.append(fh.read())
    text = "\n\n".join(buf)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"\n已合并 -> {OUT}（{len(text)} 字符）")

if __name__ == "__main__":
    main()
