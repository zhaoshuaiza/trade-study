# -*- coding: utf-8 -*-
"""生成交易学习库目录导航图 —— 绝对坐标版"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties

F = 'C:/Windows/Fonts/msyh.ttc'
def f(sz, bold=False):
    return FontProperties(fname=F, size=sz, weight='bold' if bold else 'normal')

C_BG   = '#FCFCFA'
C_RAW  = ('#E6F1FB', '#185FA5', '#0C447C')
C_WIKI = ('#E1F5EE', '#0F6E56', '#085041')
C_RULE = ('#FAEEDA', '#854F0B', '#633806')
C_TOOL = ('#F1EFE8', '#5F5E5A', '#2C2C2A')
C_OUT  = ('#EEEDFE', '#534AB7', '#3C3489')
C_KEY  = ('#FCEBEB', '#A32D2D', '#791F1F')

fig, ax = plt.subplots(figsize=(16, 19), dpi=110)
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.axis('off'); fig.patch.set_facecolor(C_BG)

def rect(x, y, w, h, colors, lw=1.1):
    face, edge, _ = colors
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle='round,pad=0,rounding_size=0.8',
                 facecolor=face, edgecolor=edge, linewidth=lw))

def txt(x, y, s, sz, color, bold=False, ha='center', va='center'):
    ax.text(x, y, s, ha=ha, va=va, fontproperties=f(sz, bold), color=color)

def arrow(x1, y1, x2, y2, color='#888780', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=color,
                                linewidth=lw, shrinkA=0, shrinkB=0))

# ══════════ 标题
txt(50, 98.4, '交易学习库 · 目录导航图', 22, '#2C2C2A', True)
txt(50, 96.6, '17 个目录 · 全部附 README 说明 · 三层架构', 11.6, '#5F5E5A')

# ══════════ 素材层
rect(4, 84.8, 92, 10.0, C_RAW)
txt(50, 93.2, '素材层 · 你放原始资料，不可修改', 12.4, '#0C447C', True)
txt(50, 91.6, '违反规则会破坏溯源能力 —— 蒸馏产物可重建，原始资料毁了就没了', 8.8, '#185FA5')

for i, (t, l1, l2) in enumerate([
        ('articles/', '网页文章', 'Web Clipper 剪这里'),
        ('clips/', '短片段', '自己的推测别放这'),
        ('academic/', '论文技术文档', '书籍 PDF 不放这'),
        ('distilled/', '中间产物', 'AI 写，可重建')]):
    x = 5.6 + i * 22.6
    rect(x, 85.6, 21.2, 4.6, C_RAW)
    txt(x + 10.6, 89.1, t, 10, '#0C447C', True)
    txt(x + 10.6, 87.7, l1, 7.8, '#185FA5')
    txt(x + 10.6, 86.5, l2, 7.4, '#185FA5')

# ══════════ 库外书籍 + 编译
rect(4, 79.6, 44, 4.2, C_OUT)
txt(26, 82.7, '书籍 PDF（库外）', 11, '#3C3489', True)
txt(26, 81.2, 'E:\\笔记Obsidian\\电子书\\ · 11 本 1.2GB · 只索引不复制', 8.2, '#534AB7')

rect(52, 79.6, 44, 4.2, C_RULE)
txt(74, 82.7, '编译：说「读 CLAUDE.md，编译 raw/」', 11, '#633806', True)
txt(74, 81.2, '检索 → 提取增量 → 更新 wiki → 建双链 → 记 log', 8.2, '#854F0B')

arrow(26, 84.8, 26, 83.9)
txt(27.2, 84.3, '放这', 8.6, '#888780', True, ha='left')
arrow(48, 81.7, 52, 81.7)

# ══════════ 知识层
rect(4, 50.2, 92, 27.0, C_WIKI)
txt(50, 74.9, '知识层 · 提炼后的成品，按「这是什么东西」分八类', 12.4, '#085041', True)
txt(50, 73.3, '共同要求：必须建双链（孤立页面等于没写）· 参数原样保留 · 冲突只暴露不选边站', 8.8, '#0F6E56')

cats = [
    ('entities/', '具体对象', '能指着说「它就是」', 5.6),
    ('concepts/', '抽象概念', '中枢、背驰、ATR', 28.2),
    ('sources/', '原始资料', '一本一页 · 溯源入口', 50.8),
    ('claims/', '有争议主张', '须标证据强度', 73.4),
    ('comparisons/', '对比', 'A 和 B 的差异', 5.6),
    ('syntheses/', '跨体系综合', '需 2 套以上', 28.2),
    ('questions/', '问答存档', '必须有依据段', 50.8),
    ('meta/ + lint/', '体检报告', '不放知识', 73.4),
]
for t, s1, s2, x in cats:
    rect(x, 62.4, 21.2, 7.4, C_WIKI)
    txt(x + 10.6, 68.2, t, 10, '#085041', True)
    txt(x + 10.6, 65.8, s1, 8.6, '#0F6E56')
    txt(x + 10.6, 63.8, s2, 7.8, '#0F6E56')

for i, (t, s) in enumerate([('index.md', '总索引 · 学习路径'),
                           ('hot.md', '近期缓存（会被覆盖）'),
                           ('log.md', '只追加')]):
    x = 5.6 + i * 30.5
    rect(x, 52.6, 29, 6.0, C_WIKI)
    txt(x + 14.5, 56.4, t, 10, '#085041', True)
    txt(x + 14.5, 54.4, s, 8, '#0F6E56')

arrow(50, 79.4, 50, 77.3, '#0F6E56')
txt(51.4, 78.4, '编译', 9.4, '#0F6E56', True, ha='left')

# ══════════ 三问
rect(4, 42.6, 92, 6.0, C_TOOL)
txt(50, 46.6, '分不清放哪？三问定去向', 11.6, '#2C2C2A', True)
txt(50, 45.1, '① 能指着它说「它就是这个东西」吗？      ② 这话对错有争议吗？      ③ 跨 2 套体系或 2 份资料了吗？', 9.2, '#5F5E5A')
txt(50, 43.5, '能 → entities              有争议 → claims              跨 2 套 → syntheses', 9.8, '#2C2C2A', True)

# ══════════ 五套体系
rect(4, 25.4, 92, 15.8, C_RAW)
txt(50, 38.6, '五套体系 · 不是并行方法，是两条脉络 + 一个变体', 12.4, '#0C447C', True)
txt(50, 37.0, '道氏 → 波浪 → 缠论是同一件事的三个阶段，缠论不是波浪的改良', 8.8, '#185FA5')

for i, (t, s1, s2) in enumerate([
        ('道氏理论', '趋势是可观测的', '不是可预测的'),
        ('波浪理论', '价值是排除', '不可能的数法'),
        ('缠论', '定义走势', '完成的判据')]):
    x = 5.6 + i * 16.6
    rect(x, 28.2, 15.4, 6.2, C_RAW)
    txt(x + 7.7, 32.6, t, 10, '#0C447C', True)
    txt(x + 7.7, 30.8, s1, 7.9, '#185FA5')
    txt(x + 7.7, 29.4, s2, 7.9, '#185FA5')
    if i < 2:
        arrow(x + 15.6, 31.3, x + 16.4, 31.3)

rect(55.4, 28.2, 18.4, 6.2, C_RULE)
txt(64.6, 32.6, '海龟法则', 10, '#633806', True)
txt(64.6, 30.8, '90% 是风险控制', 7.9, '#854F0B')
txt(64.6, 29.4, '唯一完全机械化', 7.9, '#854F0B')

rect(77.4, 28.2, 17.2, 6.2, C_TOOL)
txt(86, 32.6, '黑马王子', 10, '#2C2C2A', True)
txt(86, 30.8, '量价短线', 7.9, '#5F5E5A')
txt(86, 29.4, '周期最短', 7.9, '#5F5E5A')

txt(50, 26.6, '方法论分野：道氏 / 波浪 = 主观画线派        缠论 / 海龟 = 判据化派（可机械执行）', 10, '#2C2C2A', True)

# ══════════ 学习路径
rect(4, 17.6, 92, 6.2, C_KEY)
txt(50, 22.2, '学习路径 · 动手前先看这', 11.6, '#791F1F', True)
txt(50, 20.7, '不要从缠论开始（186MB，且依赖前两套基础概念）', 8.8, '#A32D2D')
txt(50, 19.0, '顺脉演进：道氏 → 波浪 → 缠论    ｜    风险优先：海龟优先    ｜    只学一套：海龟', 10, '#791F1F', True)

# ══════════ 规则层与工具
rect(4, 10.4, 46, 6.0, C_RULE)
txt(27, 14.5, '规则层 CLAUDE.md', 11, '#633806', True)
txt(27, 12.6, 'AI 动手前必读的库规则', 8.4, '#854F0B')

rect(50, 10.4, 46, 6.0, C_TOOL)
txt(73, 14.5, '工具 templates/ · .attachments/', 11, '#2C2C2A', True)
txt(73, 12.6, '七类页面模板 ｜ 图片附件不参与知识层', 8.4, '#5F5E5A')

# ══════════ 硬性约束
rect(4, 1.8, 92, 7.8, C_KEY)
txt(50, 8.2, '硬性约束 · 违反即为错误', 11.4, '#791F1F', True)

for i, (l1, l2) in enumerate([('参数原样保留', '禁止优化'), ('方法必须', '落成动作'),
        ('冲突只暴露', '取舍你拍板'), ('回测/模拟/实盘', '分开标注'), ('不给', '投资建议')]):
    x = 5.6 + i * 18.2
    txt(x + 8.5, 6.2, l1, 9.2, '#791F1F', True)
    txt(x + 8.5, 4.8, l2, 9.2, '#791F1F', True)

txt(50, 2.9, '判断标准：这条信息以后遇到真实问题时，会不会回来看这一页？    会 → 沉淀    不会 → 留在素材层', 9.2, '#A32D2D')

plt.savefig('E:/Work Buddy/交易学习/.attachments/目录导航图.png',
            dpi=110, bbox_inches='tight', facecolor=C_BG)
print('✓ 已生成')
