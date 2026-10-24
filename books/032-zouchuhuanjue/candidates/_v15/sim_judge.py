# -*- coding: utf-8 -*-
"""阶段4 fallback 路由模拟判卷：无独立 sub-agent 盲测时，用 verified.yaml 中晋级能力的
intents+keywords 做关键词重叠打分，模拟路由对 56 条 test-prompts 的判决，对照 expected_behavior 判定通过/失败。
可信度低于独立盲测，仅作自测与回归基线。"""
import os, json, glob, yaml

BASE = "E:/Work Buddy/交易学习/books/032-zouchuhuanjue"
CAP = os.path.join(BASE, ".cangjie/capabilities/verified.yaml")
TESTDIR = os.path.join(BASE, "tests")

d = yaml.safe_load(open(CAP, encoding="utf-8"))
# 晋级能力 -> 关键词集合（intents + keywords 原文子串）
skill_kw = {}
for c in d["capabilities"]:
    if c.get("promotion", {}).get("destination") == "promoted":
        s = c.get("promotion", {}).get("promoted_to") or c.get("slug")
        toks = list(c.get("intents", [])) + list(c.get("keywords", []))
        skill_kw[s] = [t for t in toks if t]

def score(prompt, toks):
    return sum(1 for t in toks if t and t in prompt)

total = 0
passed = 0
fails = []
for fp in sorted(glob.glob(os.path.join(TESTDIR, "*", "test-prompts.json"))):
    data = json.load(open(fp, encoding="utf-8"))
    skill = data["skill"]
    for tc in data["test_cases"]:
        total += 1
        p = tc["prompt"]
        ttype = tc["type"]
        # 对所有晋级能力打分
        ranked = sorted(((score(p, toks), s) for s, toks in skill_kw.items()), reverse=True)
        top_score, top_skill = ranked[0]
        # 判定规则 + edge_case 极性（按 expected_behavior 文本推断）
        exp = tc.get("expected_behavior", "")
        positive = True  # 是否期望命中本 Skill
        if ttype == "should_trigger":
            positive = True
        elif ttype == "should_not_trigger":
            positive = False
        elif ttype == "edge_case":
            # expected_behavior 含"不调用"为负向边界，含"调用"为正向边界
            positive = ("不调用" not in exp) and ("调用" in exp)
        ok = (positive and top_skill == skill and top_score > 0) or (not positive and top_skill != skill)
        # 记录并列（top 与次高同分且都>0）
        tie = (len(ranked) > 1 and ranked[1][0] == top_score and top_score > 0)
        if ok:
            passed += 1
        else:
            fails.append((skill, tc["id"], ttype, top_skill, top_score, tie))
        if tie:
            print(f"[TIE] {skill}/{tc['id']} 并列 top={top_skill}({top_score}) 次高={ranked[1][1]}({ranked[1][0]})")

print(f"\n总计 {total} 条，通过 {passed} 条，失败 {len(fails)} 条，通过率 {passed/total*100:.1f}%")
if fails:
    print("\n失败明细：")
    for f in fails:
        print(" ", f)
