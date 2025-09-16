# 變換操作
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
