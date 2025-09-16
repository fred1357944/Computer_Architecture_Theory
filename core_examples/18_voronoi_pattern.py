# Voronoi圖案生成
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
