#!/usr/bin/env python3
"""
批次提取測試範例
基於手動觀察的模式快速生成
"""

# 範例1: 基礎變數 (p10-11)
code_001 = """# 基礎變數與輸出
x = 10
y = 20
z = x + y
print(z)  # 30
"""

# 範例2: 字串操作 (p13-14)
code_002 = """# 字串基礎操作
name = "Grasshopper"
greeting = "Hello, " + name
print(greeting)
"""

# 範例3: 簡單運算 (p19-20)
code_003 = """# 簡單數學運算
a = 5
result = a * 2
print(result)  # 10
"""

# 範例5: 條件判斷 (p27-28)
code_005 = """# 0.4.5 條件與判斷 Condition and Decision Making

x = 10

if x > 5:
    print("x is greater than 5")
else:
    print("x is less than or equal to 5")

# 多重條件判斷
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

print(grade)  # B
"""

# 範例6: 迴圈運算 (p29-30)
code_006 = """# 0.4.6 迴圈運算 Loop

# for 迴圈
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# while 迴圈
count = 0
while count < 5:
    print(count)
    count += 1

# 迴圈中的 break 和 continue
for i in range(10):
    if i == 5:
        break  # 跳出迴圈
    if i == 3:
        continue  # 跳過本次迴圈
    print(i)
"""

# 範例8: 序列切片 (p33-34)
code_008 = """# 序列切片操作

List = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 基本切片
print(List[2:5])   # [2, 3, 4]
print(List[:3])    # [0, 1, 2]
print(List[7:])    # [7, 8, 9]
print(List[::2])   # [0, 2, 4, 6, 8]
print(List[::-1])  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
"""

# 範例9: 函數定義 (p42)
code_009 = """# 0.4.9 創建函數 Function

def add(a, b):
    \"\"\"加法函數\"\"\"
    return a + b

def multiply(x, y):
    \"\"\"乘法函數\"\"\"
    result = x * y
    return result

# 使用函數
sum_result = add(3, 5)
print(sum_result)  # 8

product = multiply(4, 6)
print(product)  # 24
"""

# 範例10: RhinoScriptSyntax基礎 (p43-44)
code_010 = """# 0.5 RhinoScriptSyntax and Rhino.Geometry

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# 創建點
pt1 = rs.AddPoint(0, 0, 0)
pt2 = rs.AddPoint(10, 0, 0)
pt3 = rs.AddPoint(10, 10, 0)

# 創建線
line1 = rs.AddLine(pt1, pt2)
line2 = rs.AddLine(pt2, pt3)

# 創建曲線
points = []
for i in range(10):
    pt = rs.AddPoint(i, i**2/10, 0)
    points.append(pt)

curve = rs.AddCurve(points)

# 使用 Rhino.Geometry
# 創建圓
center = rg.Point3d(0, 0, 0)
radius = 5.0
circle = rg.Circle(center, radius)

# 創建矩形
plane = rg.Plane.WorldXY
width = 10.0
height = 5.0
rectangle = rg.Rectangle3d(plane, width, height)

# 輸出到 Grasshopper
a = circle
b = rectangle
"""

# 保存所有範例
examples = {
    "code_001_p10.py": code_001,
    "code_002_p13.py": code_002,
    "code_003_p19.py": code_003,
    "code_005_p27.py": code_005,
    "code_006_p29.py": code_006,
    "code_008_p33.py": code_008,
    "code_009_p42.py": code_009,
    "code_010_p43.py": code_010
}

if __name__ == "__main__":
    from pathlib import Path

    output_dir = Path("test_extractions")
    output_dir.mkdir(exist_ok=True)

    for filename, code in examples.items():
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✅ 已生成: {filename}")

    print(f"\n完成！已生成 {len(examples)} 個測試範例")