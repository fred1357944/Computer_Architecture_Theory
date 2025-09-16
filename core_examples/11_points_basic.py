# 點的基礎操作
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
