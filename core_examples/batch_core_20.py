#!/usr/bin/env python3
"""
20個核心範例快速生成
根據PDF內容整理的關鍵教學範例
"""

import os
from pathlib import Path

# 建立目錄結構
output_dir = Path("core_examples")
output_dir.mkdir(exist_ok=True)

# 核心範例字典
core_examples = {}

# ============ 基礎語法 (已完成4個) ============

# ============ Rhino.Geometry 基礎 (5個) ============

# 範例11: 點的建立與操作
core_examples['11_points_basic.py'] = """# 點的基礎操作
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# 方法1: 使用 rhinoscriptsyntax
pt1 = rs.AddPoint(0, 0, 0)
pt2 = rs.AddPoint(10, 5, 0)
pt3 = rs.AddPoint(5, 10, 0)

# 方法2: 使用 Rhino.Geometry
pt_a = rg.Point3d(0, 0, 0)
pt_b = rg.Point3d(10, 0, 0)
pt_c = rg.Point3d(10, 10, 0)

# 點的運算
distance = pt_a.DistanceTo(pt_b)
midpoint = (pt_a + pt_b) / 2

# 輸出
a = [pt_a, pt_b, pt_c]
"""

# 範例12: 曲線建立
core_examples['12_curves_basic.py'] = """# 曲線基礎操作
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# 從點建立曲線
points = []
for i in range(10):
    pt = rg.Point3d(i, i**2/10, 0)
    points.append(pt)

# 建立內插曲線
curve = rg.Curve.CreateInterpolatedCurve(points, 3)

# 曲線分割
params = curve.DivideByCount(20, True)
division_points = []
for t in params:
    division_points.append(curve.PointAt(t))

# 輸出
a = curve
b = division_points
"""

# 範例13: 曲面建立
core_examples['13_surface_basic.py'] = """# 曲面基礎操作
import Rhino.Geometry as rg

# 建立平面曲面
plane = rg.Plane.WorldXY
width = 10.0
height = 5.0
interval_u = rg.Interval(0, width)
interval_v = rg.Interval(0, height)
surface = rg.PlaneSurface(plane, interval_u, interval_v)

# 曲面細分
u_count = 10
v_count = 5
points = []

for i in range(u_count):
    for j in range(v_count):
        u = i / (u_count - 1.0)
        v = j / (v_count - 1.0)
        pt = surface.PointAt(u, v)
        points.append(pt)

# 輸出
a = surface
b = points
"""

# 範例14: 向量操作
core_examples['14_vector_operations.py'] = """# 向量操作
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# 建立向量
vector1 = rg.Vector3d(1, 0, 0)
vector2 = rg.Vector3d(0, 1, 0)

# 向量運算
# 加法
vec_add = vector1 + vector2

# 縮放
vec_scaled = vector1 * 5.0

# 單位化
vec_unit = rg.Vector3d(3, 4, 0)
vec_unit.Unitize()

# 旋轉
angle = 45  # 度
radians = math.radians(angle)
vec_rotated = rg.Vector3d(vector1)
vec_rotated.Rotate(radians, rg.Vector3d.ZAxis)

# 叉積與點積
dot_product = vector1 * vector2  # 點積
cross_product = rg.Vector3d.CrossProduct(vector1, vector2)  # 叉積

# 輸出
a = [vec_add, vec_scaled, vec_unit, vec_rotated, cross_product]
"""

# 範例15: 變換操作
core_examples['15_transformations.py'] = """# 變換操作
import Rhino.Geometry as rg
import math

# 建立基礎幾何
circle = rg.Circle(rg.Point3d.Origin, 5)
curve = circle.ToNurbsCurve()

# 平移
translation = rg.Transform.Translation(10, 0, 0)
moved_curve = curve.Duplicate()
moved_curve.Transform(translation)

# 旋轉
rotation = rg.Transform.Rotation(math.radians(45), rg.Point3d.Origin)
rotated_curve = curve.Duplicate()
rotated_curve.Transform(rotation)

# 縮放
scale = rg.Transform.Scale(rg.Point3d.Origin, 2.0)
scaled_curve = curve.Duplicate()
scaled_curve.Transform(scale)

# 鏡射
mirror_plane = rg.Plane.WorldYZ
mirror = rg.Transform.Mirror(mirror_plane)
mirrored_curve = curve.Duplicate()
mirrored_curve.Transform(mirror)

# 輸出
a = [curve, moved_curve, rotated_curve, scaled_curve, mirrored_curve]
"""

# ============ 參數化圖案 (5個) ============

# 範例16: 網格圖案
core_examples['16_grid_pattern.py'] = """# 參數化網格圖案
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math

# 參數
rows = 10
cols = 10
spacing = 5
amplitude = 2

points = []
curves = []

for i in range(rows):
    row_points = []
    for j in range(cols):
        # 基礎位置
        x = i * spacing
        y = j * spacing

        # 加入波動
        z = amplitude * math.sin(i * 0.5) * math.cos(j * 0.5)

        pt = rg.Point3d(x, y, z)
        row_points.append(pt)
        points.append(pt)

    # 建立橫向曲線
    if len(row_points) > 1:
        curve = rg.Curve.CreateInterpolatedCurve(row_points, 3)
        curves.append(curve)

# 輸出
a = points
b = curves
"""

# 範例17: 吸引點圖案
core_examples['17_attractor_pattern.py'] = """# 吸引點圖案
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# 建立基礎網格
grid_points = []
for i in range(20):
    for j in range(20):
        pt = rg.Point3d(i, j, 0)
        grid_points.append(pt)

# 吸引點
attractor = rg.Point3d(10, 10, 0)

# 根據距離調整大小
circles = []
for pt in grid_points:
    # 計算到吸引點的距離
    distance = pt.DistanceTo(attractor)

    # 反比例計算半徑
    max_radius = 0.5
    min_radius = 0.05
    radius = max_radius - (distance / 30) * (max_radius - min_radius)
    radius = max(min_radius, min(max_radius, radius))

    # 建立圓
    circle = rg.Circle(pt, radius)
    circles.append(circle)

# 輸出
a = circles
"""

# 範例18: Voronoi圖案
core_examples['18_voronoi_pattern.py'] = """# Voronoi圖案生成
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import random

# 生成隨機點
points = []
for i in range(25):
    x = random.uniform(0, 50)
    y = random.uniform(0, 50)
    pt = rg.Point3d(x, y, 0)
    points.append(pt)

# 建立邊界
boundary = rg.Rectangle3d(rg.Plane.WorldXY, 50, 50)

# 注意：實際Voronoi需要使用特殊函數
# 這裡簡化為點和圓的關係展示
cells = []
for pt in points:
    # 為每個點建立影響範圍
    circle = rg.Circle(pt, 5)
    cells.append(circle)

# 輸出
a = points
b = cells
c = boundary.ToNurbsCurve()
"""

# 範例19: 遞迴圖案
core_examples['19_recursive_pattern.py'] = """# 遞迴分形圖案
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

def recursive_squares(center, size, depth, squares):
    \"\"\"遞迴生成正方形\"\"\"
    if depth <= 0 or size < 0.1:
        return

    # 建立當前正方形
    plane = rg.Plane(center, rg.Vector3d.ZAxis)
    rect = rg.Rectangle3d(plane, size, size)
    rect.RecenterToPoint(center)
    squares.append(rect)

    # 遞迴建立四個小正方形
    new_size = size * 0.5
    offset = size * 0.25

    # 四個角的新中心點
    centers = [
        center + rg.Vector3d(-offset, -offset, 0),
        center + rg.Vector3d(offset, -offset, 0),
        center + rg.Vector3d(offset, offset, 0),
        center + rg.Vector3d(-offset, offset, 0)
    ]

    for c in centers:
        recursive_squares(c, new_size, depth - 1, squares)

# 執行遞迴
squares = []
start_center = rg.Point3d(0, 0, 0)
recursive_squares(start_center, 10, 4, squares)

# 輸出
a = squares
"""

# 範例20: 參數化立面
core_examples['20_parametric_facade.py'] = """# 參數化立面系統
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math

# 立面尺寸
width = 30
height = 20
floors = 5
bays = 8

# 建立立面網格
facade_points = []
panels = []

floor_height = height / floors
bay_width = width / bays

for i in range(bays):
    for j in range(floors):
        # 面板角點
        x = i * bay_width
        y = 0
        z = j * floor_height

        # 建立面板
        pt1 = rg.Point3d(x, y, z)
        pt2 = rg.Point3d(x + bay_width, y, z)
        pt3 = rg.Point3d(x + bay_width, y, z + floor_height)
        pt4 = rg.Point3d(x, y, z + floor_height)

        # 根據高度調整開窗
        window_ratio = 0.3 + 0.4 * (j / floors)  # 越高開窗越大

        # 內縮建立窗戶
        offset = bay_width * (1 - window_ratio) * 0.5
        w1 = rg.Point3d(x + offset, y, z + offset)
        w2 = rg.Point3d(x + bay_width - offset, y, z + offset)
        w3 = rg.Point3d(x + bay_width - offset, y, z + floor_height - offset)
        w4 = rg.Point3d(x + offset, y, z + floor_height - offset)

        window = rg.PolylineCurve([w1, w2, w3, w4, w1])
        panels.append(window)

# 輸出
a = panels
"""

# 保存所有範例
def save_examples():
    for filename, code in core_examples.items():
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✅ {filename}")

    print(f"\n完成！生成了 {len(core_examples)} 個核心範例")
    print(f"位置：{output_dir}")

if __name__ == "__main__":
    save_examples()