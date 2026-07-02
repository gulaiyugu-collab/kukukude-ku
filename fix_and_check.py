import sys, json, re, subprocess, os
sys.stdout.reconfigure(encoding="utf-8")
p = r"G:\Workspace\Projects\项目006_酷酷的库\工作文件\app_template.html"
c = open(p, "r", encoding="utf-8").read()
c = c.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js" defer></script>'
)
print("1 CDN defer done")
with open(r"G:\Workspace\Projects\项目006_酷酷的库\工作文件\questions.json", "r", encoding="utf-8") as f:
    q = json.load(f)
qj = json.dumps(q, ensure_ascii=False)
html = c.replace("__QUESTIONS_DATA__", qj)
for o in [r"G:\Workspace\Projects\项目006_酷酷的库\index.html", r"G:\Workspace\Projects\项目006_酷酷的库\产出\index.html"]:
    open(o, "w", encoding="utf-8").write(html)
print(f"2 Rebuilt {len(html)} bytes")
# Self check
fails = 0
if html[0] != "<": print("FAIL doctype"); fails += 1
else: print("PASS doctype")
if "Object.values" in html: print("FAIL Object.values"); fails += 1
else: print("PASS no Object.values")
m = list(re.finditer(r"<script>([\s\S]*?)</script>", html))
if m:
    tmp = "C:/Users/Administrator/Desktop/_sc.js"
    open(tmp, "w", encoding="utf-8").write(m[-1].group(1))
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode == 0: print("PASS JS syntax")
    else: print("FAIL JS syntax"); fails += 1
    os.unlink(tmp)
for f in ["speakQuestion","startExam","searchQuestions","showStats","editGoal"]:
    if f not in html: print(f"FAIL {f}"); fails += 1
else: print("PASS all features")
if fails == 0: print("\nAll checks PASSED!")
else: print(f"\n{fails} check(s) FAILED!")
