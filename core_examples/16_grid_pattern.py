# 參數化網格圖案
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
