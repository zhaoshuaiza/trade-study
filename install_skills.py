# -*- coding: utf-8 -*-
"""把 doubao 的技能包安装到 WorkBuddy 用户技能目录。

为什么装：doubao 项目已把 98 本书蒸成 285 个 SKILL.md，
但只装进了豆包自己的技能目录，WorkBuddy 侧完全看不到。
技能包是实盘判据的最佳载体（带 frontmatter、可被 AI 直接调用），
交易库的价值是交叉引用与冲突辩论——两者互补。

用法:
  python install_skills.py             # 装全部
  python install_skills.py cb-* guaitie # 只装匹配项
"""
import io, os, re, sys, glob, shutil

DB = 'E:/doubao/电子书蒸馏项目'
DEST = 'C:/Users/admi/.workbuddy/skills'

# 只装交易相关（剔除理财启蒙/群体心理/励志等非交易主题）
SKIP_PREFIX = ('wuhanzhong', 'youting')   # 乌合之众、赢


def collect():
    out = {}
    for root, dns, fns in os.walk(DB):
        if os.path.basename(root) != '技能包':
            continue
        for dn in dns:
            sp = os.path.join(root, dn, 'SKILL.md')
            if os.path.exists(sp):
                out[dn] = sp
    return out


def main():
    pats = sys.argv[1:]
    skills = collect()
    if not skills:
        print('❌ 未找到技能包')
        return
    os.makedirs(DEST, exist_ok=True)

    n_ok = n_skip = n_exist = 0
    for name in sorted(skills):
        if any(name.startswith(p) for p in SKIP_PREFIX):
            n_skip += 1
            continue
        if pats and not any(fnmatch(name, p) for p in pats):
            continue
        d = f'{DEST}/{name}'
        if os.path.exists(f'{d}/SKILL.md'):
            n_exist += 1
            continue
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(skills[name], f'{d}/SKILL.md')
        # 带附属文件的也一并复制
        for f in os.listdir(os.path.dirname(skills[name])):
            if f == 'SKILL.md':
                continue
            src = os.path.join(os.path.dirname(skills[name]), f)
            if os.path.isfile(src):
                shutil.copyfile(src, f'{d}/{f}')
        n_ok += 1

    print(f'安装完成：新装 {n_ok}，已存在 {n_exist}，按主题跳过 {n_skip}')
    print(f'目标目录: {DEST}')
    print(f'当前技能总数: {len([x for x in os.listdir(DEST) if os.path.isdir(f"{DEST}/{x}")])}')


def fnmatch(name, pat):
    import fnmatch as fm
    return fm.fnmatch(name, pat)


if __name__ == '__main__':
    main()