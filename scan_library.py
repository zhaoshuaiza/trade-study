#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scan_library.py · 电子书目录扫描器

用途：
  扫描 E:/笔记Obsidian/电子书/，对比 raw/.manifest.json，
  找出「新增的书」「已登记但文件不在了」，并按CLAUDE.md 的
  library_scope 规则给出分流建议。

用法：
  python scan_library.py           扫描并显示结果
  python scan_library.py --json    输出 JSON（供其他脚本消费）
  python scan_library.py --add     把未登记的新书写入 manifest

注意：
  · 本脚本**只索引，不复制 PDF**，也不修改任何原始文件
  · 只写 raw/.manifest.json，不动 wiki/ 知识层
  · 分流判断是**建议**，最终由用户拍板
"""
import os
import sys
import json
from datetime import datetime

LIBRARY = r"E:\笔记Obsidian\电子书"
MANIFEST = r"E:\Work Buddy\交易学习\raw\.manifest.json"
TRADING_LIB = r"E:\Work Buddy\交易学习"
SIBLING_LIB = r"E:\笔记Obsidian\hedge"

# 文件扩展名 → 类型
EXT_TYPE = {
    ".pdf": "pdf", ".epub": "epub", ".mobi": "mobi",
    ".azw3": "azw3", ".doc": "doc", ".docx": "docx",
    ".txt": "txt", ".html": "html",
}

# 关键词 → 交易库收录建议（命中即标为"疑似交易类"）
TRADING_HINTS = [
    "交易", "炒股", "股票", "期货", "股市", "海龟", "缠论", "道氏", "波浪",
    "投资", "投机", "盈利", "涨停", "量价", "筹码", "盘口", "操盘", "选股",
    "止盈", "止损", "仓位", "技术分析", "行情", "A股", "港股", "美股",
]

# 关键词 → 建议分流到 hedge 库（个人成长类）
SIBLING_HINTS = [
    "人性", "传记", "权谋", "法律", "职场", "决策", "心智", "成长", "哲学",
    "小说", "故事", "传记", "品格", "习惯",
]

# 明确排除的非交易内容
EXCLUDE_HINTS = ["小说集", "散文", "随笔"]


def guess_scope(filename):
    """判断这本书该进哪个库，返回 (建议, 理由)"""
    name = filename
    for kw in EXCLUDE_HINTS:
        if kw in name:
            return "hedge", f"含「{kw}」，属个人成长内容"
    trading = [kw for kw in TRADING_HINTS if kw in name]
    sibling = [kw for kw in SIBLING_HINTS if kw in name]
    if trading:
        return "交易库", f"命中交易类关键词：{'/'.join(trading[:3])}"
    if sibling:
        return "hedge", f"命中成长类关键词：{'/'.join(sibling[:3])}"
    return "待判定", "无明显关键词，需人工判断"


def scan_dir():
    """扫描电子书目录（递归，深度 2 层）"""
    found = []
    if not os.path.isdir(LIBRARY):
        print(f"❌ 目录不存在：{LIBRARY}")
        return found

    for root, dirs, files in os.walk(LIBRARY):
        depth = root[len(LIBRARY):].count(os.sep)
        if depth >= 3:
            dirs[:] = []
            continue
        for fn in files:
            if fn.startswith("."):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext not in EXT_TYPE:
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, LIBRARY).replace("\\", "/")
            found.append({
                "name": fn,
                "rel_path": rel,
                "path": full.replace("\\", "/"),
                "type": EXT_TYPE[ext],
                "size": os.path.getsize(full),
                "in_subdir": depth > 0,
                "subdir": os.path.relpath(root, LIBRARY).replace("\\", "/") if depth else "",
            })
    return found


def load_manifest():
    if os.path.exists(MANIFEST):
        with open(MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    do_add = "--add" in args

    books = scan_dir()
    man = load_manifest()
    sources = man.get("sources", {})
    compiled = man.get("compiled", {})
    diverted = man.get("library_scope", {}).get("diverted", {})

    # 已登记的：rel_path 和绝对路径都算
    registered = set()
    for v in sources.values():
        registered.add(v.get("path", "").replace("\\", "/"))
    diverted_names = set(diverted.keys())

    new_books, known_books = [], []
    for b in books:
        if b["path"] in registered or b["name"] in diverted_names:
            known_books.append(b)
        else:
            new_books.append(b)

    # 登记了但文件不在了
    # 注意：manifest 里的 path 可能是**目录**（以 / 结尾）或**截断的标题**，
    # 不能只做字符串相等判断，否则会大量误报。改为按"文件名/目录名"二次核对。
    on_disk_paths = {b["path"] for b in books}
    on_disk_names = {b["name"] for b in books}
    on_disk_dirs = {b["subdir"].split("/")[0] for b in books if b["in_subdir"]}
    on_disk_dirs |= {os.path.basename(b["subdir"]) for b in books if b["in_subdir"]}

    missing = []
    for k, v in sources.items():
        p = v.get("path", "").replace("\\", "/")
        if not p:
            continue
        base = os.path.basename(p.rstrip("/"))
        # 三重核对：完整路径 / 文件名 / 顶层目录名，任一命中即视为存在
        if p in on_disk_paths or k in on_disk_names or base in on_disk_names:
            continue
        if base in on_disk_dirs:
            continue
        # 标题截断（"...等多个文件"）→ 用前缀匹配
        stem = base.split("等多个文件")[0]
        if stem and any(stem in n or n.startswith(stem[:12]) for n in on_disk_names):
            continue
        missing.append({"name": k, "path": p})

    if as_json:
        print(json.dumps({
            "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_on_disk": len(books),
            "registered": len(known_books),
            "new": new_books,
            "missing": missing,
        }, ensure_ascii=False, indent=2))
        return

    print("=" * 64)
    print(f"  电子书目录扫描 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 64)
    print(f"  目录：{LIBRARY}")
    print(f"  磁盘上共{len(books)} 个文件 · 已登记 {len(known_books)} · **未登记 {len(new_books)}**\n")

    if new_books:
        print("-" * 64)
        print("📕 未登记的新文件")
        print("-" * 64)
        for b in sorted(new_books, key=lambda x: x["name"]):
            scope, reason = guess_scope(b["name"])
            mark = {"交易库": "🟢", "hedge": "🟡", "待判定": "⚪"}[scope]
            loc = f"（{b['subdir']}/）" if b["in_subdir"] else ""
            print(f"{mark} {b['name'][:58]}")
            print(f"     {human_size(b['size'])} · {b['type']}{loc}")
            print(f"     → 建议进：**{scope}**（{reason}）")
            print()

    if missing:
        print("-" * 64)
        print("⚠️ 已登记但文件不在了")
        print("-" * 64)
        for m in missing:
            print(f"  · {m['name']}")
        print()

    if not new_books and not missing:
        print("✅ 全部已登记，没有新文件，也没有失效记录。\n")

    print("=" * 64)
    print("下一步：")
    print("  1. 确认分流建议（🟢交易库 / 🟡hedge库 / ⚪需人工判断）")
    print("  2. 确认后执行登记：python scan_library.py --add")
    print("  3. 然后跟我说「编译《书名》」，我会走OCR → 编译流程")
    print("=" * 64)

    if do_add:
        print("\n⚠️ --add 需要逐本确认分流，暂不批量写入。")
        print("   请告诉我哪些进交易库、哪些进 hedge，我再逐本登记。\n")


if __name__ == "__main__":
    main()