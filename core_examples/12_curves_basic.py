# 曲線基礎操作
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
