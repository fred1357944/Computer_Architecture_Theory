# 曲面基礎操作
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
