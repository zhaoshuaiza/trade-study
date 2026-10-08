#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
compile_raw.py · 素材编译助手（raw/ → wiki/）

用途：
  把 raw/ 下新收录的素材，整理成「待编译清单」并给出可执行的编译指引。
  真正的知识提炼由 AI 按 CLAUDE.md 规则完成，本脚本负责：
    1. 扫描新素材（对比 .manifest.json 记录）
    2. 输出待编译清单（含优先级判断建议）
    3. 检查该素材可能影响哪些已有页面（提示潜在冲突/补充点）

用法：
  python compile_raw.py--list       只看有什么新素材
  python compile_raw.py --scan      扫描 + 打印待编译清单
  python compile_raw.py --paths <文件路径>  查某个素材该更新哪些页面
"""
import os
import sys
import json
from datetime import datetime

ROOT = r"E:\Work Buddy\交易学习"
RAW = os.path.join(ROOT, "raw")
WIKI = os.path.join(ROOT, "wiki")
MANIFEST = os.path.join(RAW, ".manifest.json")

# 关键词 → 建议影响的已有页面（提示 AI 去核对，不是硬规则）
ROUTE_HINTS = {
    "海龟": ["concepts/ATR与N值", "concepts/唐奇安通道", "concepts/仓位管理",
             "entities/海龟法则", "comparisons/五套体系总览对比"],
    "唐奇安": ["concepts/唐奇安通道"],
    "ATR": ["concepts/ATR与N值", "concepts/仓位管理"],
    "止损": ["concepts/仓位管理", "claims/止损方法对比(待建)"],
    "加仓": ["concepts/仓位管理"],
    "中枢": ["concepts/走势中枢", "concepts/三类买卖点"],
    "背驰": ["concepts/背驰与转折", "concepts/背驰与力度比较"],
    "分型": ["concepts/分型笔与线段"],
    "笔": ["concepts/分型笔与线段"],
    "线段": ["concepts/分型笔与线段"],
    "买点": ["concepts/三类买卖点", "concepts/获利机会的绝对分类"],
    "级别": ["concepts/走势级别与递归"],
    "量化": ["concepts/走势的多义性", "comparisons/五套体系总览对比"],
    "道氏": ["concepts/道氏的三种运动", "concepts/道氏理论的适用边界"],
    "波浪": ["concepts/波浪嵌套与级别", "concepts/斐波那契比率"],
    "均线": ["concepts/均线吻与转折"],
    "心理": ["concepts/仓位管理", "concepts/你不可不知的人性(待建)"],
    "人性": ["concepts/你不可不知的人性(待建)"],
    "成交量": ["concepts/量价关系与陷阱", "concepts/主力控盘与对敲识破"],
    "涨停": ["concepts/组合热度", "concepts/量价关系与陷阱"],
    "主力": ["concepts/主力控盘与对敲识破"],
}


def load_manifest():
    if os.path.exists(MANIFEST):
        with open(MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_manifest(m):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)


def scan_materials():
    """扫描 raw/ 下的素材（不含 distilled/ 中间产物）"""
    found = []
    for entry in ("articles", "clips", "academic"):
        d = os.path.join(RAW, entry)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.startswith("README") or fn.startswith("."):
                continue
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                found.append({
                    "entry": entry,
                    "file": fn,
                    "path": p,
                    "size": os.path.getsize(p),
                })
    return found


def guess_targets(text):
    """按关键词猜可能相关的已有页面"""
    hits = []
    for kw, pages in ROUTE_HINTS.items():
        if kw in text:
            hits.extend(pages)
    seen, out = set(), []
    for p in hits:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def read_head(path, n=1500):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(n)
    except Exception:
        return ""


def main():
    args = sys.argv[1:]

    if "--paths" in args:
        i = args.index("--paths")
        target = args[i + 1] if i + 1 < len(args) else ""
        print(f"=== {os.path.basename(target)} 可能影响以下页面 ===\n")
        text = read_head(target)
        for p in guess_targets(text):
            exists = os.path.exists(os.path.join(WIKI, p.replace("/", os.sep) + ".md"))
            mark = "✅存在" if exists else "⚠️ 待建"
            print(f"  {mark}  {p}")
        return

    mats = scan_materials()
    man = load_manifest()
    known = man.get("compiled", {})

    new, old = [], []
    for m in mats:
        key = f"{m['entry']}/{m['file']}"
        (old if key in known else new).append((key, m))

    if "--list" in args:
        for k, m in new:
            print(f"  [新] {k}")
        print(f"\n新素材 {len(new)} / 已编译 {len(old)}")
        return

    print("=" * 60)
    print(f"  待编译素材：{len(new)} 个")
    print("=" * 60)

    if not new:
        print("\n✅ 没有新素材。想收录文章 → 用 Web Clipper 剪藏到 raw/articles/")
        print("   剪藏后跟我说「编译 raw/」即可。\n")
        return

    for k, m in new:
        text = read_head(m["path"])
        print(f"\n📄 {k}")
        print(f"   大小：{m['size']} 字节")
        # 尝试读标题
        for line in text.split("\n")[:12]:
            if line.startswith("# "):
                print(f"   标题：{line[2:].strip()[:60]}")
                break
        tg = guess_targets(text)
        if tg:
            print(f"   📎 可能需要核对/更新的页面：")
            for p in tg[:6]:
                exists = os.path.exists(os.path.join(WIKI, p.replace("/", os.sep) + ".md"))
                print(f"      {'✅' if exists else '⚠️ '} {p}")

    print("\n" + "=" * 60)
    print("下一步：对每个素材执行")
    print("  1. 读 raw/ 下该文件全文")
    print("  2. 检索 wiki/ 已有知识（先读 hot.md → index.md）")
    print("  3. 提取真正新增/修正的信息 → 更新已有页面（备份后）")
    print("  4. 建/补 [[双链]]")
    print("  5. 更新 index.md、log.md（只追加）")
    print("  6. 在 .manifest.json 记录该素材为已编译")
    print("=" * 60)


if __name__ == "__main__":
    main()