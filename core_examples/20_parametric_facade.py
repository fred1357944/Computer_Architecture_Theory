# 參數化立面系統
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math

# 立面尺寸
width = 30
height = 20
floors = 5
bays = 8

# 建立立面網格
facade_points = []
panels = []

floor_height = height / floors
bay_width = width / bays

for i in range(bays):
    for j in range(floors):
        # 面板角點
        x = i * bay_width
        y = 0
        z = j * floor_height

        # 建立面板
        pt1 = rg.Point3d(x, y, z)
        pt2 = rg.Point3d(x + bay_width, y, z)
        pt3 = rg.Point3d(x + bay_width, y, z + floor_height)
        pt4 = rg.Point3d(x, y, z + floor_height)

        # 根據高度調整開窗
        window_ratio = 0.3 + 0.4 * (j / floors)  # 越高開窗越大

        # 內縮建立窗戶
        offset = bay_width * (1 - window_ratio) * 0.5
        w1 = rg.Point3d(x + offset, y, z + offset)
        w2 = rg.Point3d(x + bay_width - offset, y, z + offset)
        w3 = rg.Point3d(x + bay_width - offset, y, z + floor_height - offset)
        w4 = rg.Point3d(x + offset, y, z + floor_height - offset)

        window = rg.PolylineCurve([w1, w2, w3, w4, w1])
        panels.append(window)

# 輸出
a = panels
