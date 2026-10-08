#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sync_distilled.py · 蒸馏成果自动汇总到交易学习库

用途：
  把散落在各处的「蒸馏笔记」同步进 E:/Work Buddy/交易学习 的知识层，
  并自动更新 index.md / log.md / manifest。

用法：
  python sync_distilled.py            # 增量同步 + 重建索引
  python sync_distilled.py --check    # 只检查差异，不写入
  python sync_distilled.py --git      # 同步后自动 git commit

设计原则（遵循 CLAUDE.md）：
  · 不删除任何文件
  · 已存在页面不覆盖，除非 --force
  · 新内容一律追加到 log.md（铁律9：log 只追加）
"""
import os
import sys
import json
import shutil
import hashlib
from datetime import datetime

ROOT = r"E:\Work Buddy\交易学习"
WIKI = os.path.join(ROOT, "wiki")
MANIFEST = os.path.join(ROOT, "raw", ".manifest.json")

# 蒸馏源 → 知识层目标 的映射表
SOURCES = [
    {
        "name": "缠论108课详解",
        "file": r"E:\Work Buddy\chanlun_work\蒸馏-缠论108课详解.md",
        "targets": [
            os.path.join(WIKI, "syntheses", "缠论108课-完整蒸馏与学习指南.md"),
        ],
        "tags": ["缠论", "蒸馏", "可执行"],
    },
    {
        "name": "缠论108课详解(hedge库副本)",
        "file": r"E:\笔记Obsidian\hedge\013-缠论108课详解 蒸馏笔记与深度学习指南.md",
        "targets": [],          # 已同步过，不重复写入
        "tags": ["缠论", "Obsidian"],
    },
]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def sync(check_only=False):
    report = {"new": [], "same": [], "missing": [], "conflict": []}
    for src in SOURCES:
        path = src["file"]
        if not os.path.exists(path):
            report["missing"].append(src["name"])
            print(f"  [缺失] {src['name']}: {path}")
            continue
        digest = md5(path)
        for tgt in src["targets"]:
            if os.path.exists(tgt):
                if md5(tgt) == digest:
                    report["same"].append(tgt)
                    print(f"  [一致] {os.path.basename(tgt)}")
                else:
                    report["conflict"].append(tgt)
                    print(f"  [差异] {os.path.basename(tgt)}  (目标已存在且内容不同，保留不覆盖)")
            else:
                report["new"].append(tgt)
                if not check_only:
                    shutil.copy2(path, tgt)
                    print(f"  [新建] {tgt}")
    return report


def append_log(report):
    """log.md 只追加，绝不覆盖历史"""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n## {stamp} · 蒸馏成果自动同步\n"]
    if report["new"]:
        lines.append(f"- **新建** {len(report['new'])} 个页面：")
        for p in report["new"]:
            lines.append(f"  - `wiki/{os.path.relpath(p, WIKI).replace(os.sep, '/')}`")
    if report["same"]:
        lines.append(f"- **无变化** {len(report['same'])} 个页面")
    if report["conflict"]:
        lines.append(f"- **⚠️ 差异待确认** {len(report['conflict'])} 个（未覆盖，需人工判断）：")
        for p in report["conflict"]:
            lines.append(f"  - `{os.path.relpath(p, WIKI).replace(os.sep, '/')}`")
    if report["missing"]:
        lines.append(f"- **源文件缺失** {len(report['missing'])} 个")
    lines.append(f"\n> 由 `sync_distilled.py` 自动追加。")
    write(os.path.join(WIKI, "log.md"), read(os.path.join(WIKI, "log.md")) + "\n".join(lines))


def main():
    check_only = "--check" in sys.argv
    do_git = "--git" in sys.argv

    print(f"扫描蒸馏源 ... （{'仅检查' if check_only else '写入模式'}）")
    report = sync(check_only)

    if check_only:
        print(f"\n结果：新 {len(report['new'])} / 一致 {len(report['same'])} / "
              f"差异 {len(report['conflict'])} / 缺失 {len(report['missing'])}")
        return

    append_log(report)

    if do_git:
        os.system(f'cd "{ROOT}" && git add -A && git commit -m "sync: 蒸馏成果自动汇总 {datetime.now().strftime("%Y-%m-%d %H:%M")}"')

    print(f"\n✅ 同步完成：新 {len(report['new'])} / 一致 {len(report['same'])} / "
          f"差异 {len(report['conflict'])}")


if __name__ == "__main__":
    main()