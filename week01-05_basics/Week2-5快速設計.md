# Week 2-5 快速設計

## Week 2: 幾何基礎
### 核心範例
```python
# 曲線等分 + 垂直構造
import Rhino.Geometry as rg

pts = curve.DivideByCount(count, True)
frames = []
for t in pts:
    frame = curve.FrameAt(t)[1]
    frames.append(frame)

# 在每個frame上建構造
```

### 作業
改寫成：沿曲線的欄杆系統

### AI提示詞
```
這段程式碼建立曲線上的參考框架。
如何用這些框架建立：
1. 垂直的欄杆
2. 旋轉的百葉
3. 變化的截面
```

---

## Week 3: DataTree
### 核心範例
```python
# 理解樹狀資料
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

tree = DataTree[object]()
for i in range(branches):
    path = GH_Path(i)
    for j in range(items):
        tree.Add(data[i][j], path)
```

### 作業
建立分層的立面系統（樓層→開間→窗戶）

### AI提示詞
```
DataTree就像建築的階層：
大樓→樓層→房間→家具
請解釋如何用DataTree組織立面元素
```

---

## Week 4: 圖案生成
### 核心範例
```python
# 參數化圖案
import math

pattern = []
for u in range(u_count):
    for v in range(v_count):
        # 基礎網格
        x = u * spacing
        y = v * spacing

        # 加入變化
        offset = math.sin(u * 0.5) * amplitude
        z = offset

        pt = rg.Point3d(x, y, z)
        pattern.append(pt)
```

### 作業
三個變化：
1. 漸變密度
2. 旋轉變化
3. 尺寸變化

### AI提示詞
```
分析這個圖案的變化邏輯。
建議5種不同的數學函數來控制：
- 疏密
- 大小
- 旋轉
給出具體程式碼
```

---

## Week 5: 曲面操作
### 核心範例
```python
# 曲面細分與重建
u_count = 10
v_count = 10

points = []
for i in range(u_count):
    u = i / (u_count - 1.0)
    for j in range(v_count):
        v = j / (v_count - 1.0)
        pt = surface.PointAt(u, v)

        # 法線偏移
        normal = surface.NormalAt(u, v)
        offset_pt = pt + normal * height
        points.append(offset_pt)
```

### 作業
曲面開窗系統

### AI提示詞
```
我有一個曲面，想要：
1. 均勻開窗
2. 窗戶垂直於曲面
3. 窗戶大小隨曲率變化
請給出實現思路和程式碼
```

---

## 通用規則

### 每週必做
1. 讀懂範例（用AI）
2. 改寫一個版本
3. 解決一個真實問題

### 禁止
- 不測試就交
- 看不懂就用
- 沒有錯誤處理

### 加分
- 幫同學debug（+5）
- 找出更簡單的寫法（+10）
- 做出超出預期的效果（+15）