#!/usr/bin/env python3
"""自检脚本 - 修改代码后运行此脚本确认没问题再汇报"""
import sys, subprocess, re, os, json
sys.stdout.reconfigure(encoding="utf-8")
fails = 0

targets = [
    r"G:\Workspace\Projects\项目006_酷酷的库\index.html",
    r"G:\Workspace\Projects\项目006_酷酷的库\产出\index.html"
]

for path in targets:
    if not os.path.exists(path):
        print(f"SKIP: {path} not found")
        continue
    
    c = open(path, "r", encoding="utf-8").read()
    
    # 1. DOCTYPE first byte
    if c[0] != "<":
        print(f"FAIL: {path} - DOCTYPE has leading space")
        fails += 1
    
    # 2. No Object.values (ES2017, not supported on some phones)
    if "Object.values" in c:
        print(f"FAIL: {path} - Object.values found")
        fails += 1
    
    # 3. JS syntax check
    m = list(re.finditer(r"<script>([\s\S]*?)</script>", c))
    if m:
        tmp = os.path.join(os.environ.get("TMP", "."), "_check.js")
        open(tmp, "w", encoding="utf-8").write(m[-1].group(1))
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAIL: {path} - JS syntax error")
            fails += 1
        os.unlink(tmp)
    
    # 4. Features check
    for feature in ["speakQuestion", "startExam", "searchQuestions", "showStats"]:
        if feature not in c:
            print(f"FAIL: {path} - {feature} missing")
            fails += 1

if fails == 0:
    print(f"✅ 全部通过 ({len(targets)} 文件)")
    sys.exit(0)
else:
    print(f"❌ {fails} 个检查未通过")
    sys.exit(1)
