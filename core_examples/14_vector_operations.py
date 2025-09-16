# 向量操作
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
