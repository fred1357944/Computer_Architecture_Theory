# 範例 01: conditional_point_array

## 程式碼

```python
import rhinoscriptsyntax as rs

pts = []

for i in range(x):
    if i < y:
        pt = rs.AddPoint(i,0,0)
        pts.append(pt)
    else:
        pt = rs.AddPoint(i,10,0)
        pts.append(pt)

pts_out = pts
```

## 說明

待補充...

## AI分析提示詞

```
請分析這段Grasshopper Python程式碼：
[貼上程式碼]
1. 主要功能是什麼？
2. 使用了哪些Rhino.Geometry方法？
3. 如何改進？
```
