# 0.5 RhinoScriptSyntax and Rhino.Geometry

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
