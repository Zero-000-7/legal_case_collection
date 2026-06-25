#!/usr/bin/env python3
"""法律案例数据采集、清洗与标准化 — 生成20个独立 .md 文件"""
import os, re, json
from datetime import date

OUTPUT_DIR = "/Users/lingpengfei/legal_case_collection/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text.strip())
    return text[:50]

def make_front_matter(case):
    lines = [
        "---",
        f'title: "{case["title"]}"',
        f'案号: "{case["ah"]}"',
        f'案由: "{case["ay"]}"',
        f'案件类别: "{case["ajlb"]}"',
        f'审理程序: "{case["spcx"]}"',
        f'法院层级: "{case["cj"]}"',
        f'审理法院: "{case["jbdw"]}"',
        f'地域: "{case["xzqh"]}"',
        f'裁判日期: "{case["ja_date"]}"',
        f'数据来源: "元典法律数据库（{case["db"]}）"',
        f'案例ID: "{case["scid"]}"',
    ]
    if case.get('laws'):
        lines.append("适用法律:")
        for l in case['laws']:
            lines.append(f'  - "{l}"')
    if case.get('issues'):
        lines.append("争议焦点:")
        for i in case['issues']:
            lines.append(f'  - "{i}"')
    if case.get('outcome'):
        lines.append(f'裁判结果: "{case["outcome"]}"')
    lines.extend([
        f'采集日期: "{date.today().isoformat()}"',
        f'脱敏状态: "主体名称已脱敏"',
        "---",
    ])
    return "\n".join(lines)

# 读取脱敏后的案例JSON数据
with open('/Users/lingpengfei/legal_case_collection/cases_data.json', 'r', encoding='utf-8') as f:
    CASES = json.load(f)

print(f"载入案例数据: {len(CASES)} 篇")
print(f"案由覆盖: {sorted(set(c['ay'] for c in CASES))}")
print()

# 生成独立 .md 文件
generated = []
for idx, case in enumerate(CASES, 1):
    slug = slugify(case['title'].split('与')[0])
    filename = f"{idx:02d}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    output = make_front_matter(case) + "\n\n" + case['content'].strip() + "\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)
    generated.append(filename)
    print(f"[✓] {filename}  ({case['ja_date']})  [{case['ay']}]")

print(f"\n共生成 {len(generated)} 个独立文件")
print(f"输出目录: {OUTPUT_DIR}")
