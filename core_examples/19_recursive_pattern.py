# 遞迴分形圖案
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

def recursive_squares(center, size, depth, squares):
    """遞迴生成正方形"""
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
