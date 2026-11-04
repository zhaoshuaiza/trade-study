import re
p = 'counter-examples.md'
s = open(p, encoding='utf-8').read()

# 1) remove trailing single quote on id lines: "- id: ceNN'" -> "- id: ceNN"
s = re.sub(r"- id: (ce\d+)'", r"- id: \1", s)

# 2) fix summary line that starts with a double quote (plain scalar ambiguity)
s = s.replace(
    '  summary: "专家能预测"是本书列为错误信念的核心之一。',
    "  summary: '\"专家能预测\"是本书列为错误信念的核心之一。'"
)

# 3) safety: any other line "  key: \"...\"rest" where a plain scalar starts with '"'
#    wrap whole value in single quotes
def fix_plain(m):
    key, val = m.group(1), m.group(2)
    return "  %s: '%s'" % (key, val)
s = re.sub(r'^  ([a-z_]+): "([^"]*".*)$', fix_plain, s, flags=re.M)

open(p, 'w', encoding='utf-8').write(s)
print('fixed')
