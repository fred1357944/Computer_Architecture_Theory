# 吸引點圖案
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
