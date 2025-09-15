# Week 6-10 進階應用

## Week 6: 建築元素參數化

### 目標
不是做花俏的造型，是解決真實問題。

### 範例：智慧樓梯
```python
# 輸入：起點、終點、樓高
import Rhino.Geometry as rg

steps = int(height / 0.15)  # 15cm踏高
tread = 0.28  # 28cm踏深

stairs = []
for i in range(steps):
    z = i * (height / steps)
    x = i * tread

    # 踏板
    corner = rg.Point3d(x, 0, z)
    step = rg.Rectangle3d(
        rg.Plane(corner, rg.Vector3d.ZAxis),
        tread, width
    )
    stairs.append(step.ToNurbsCurve())
```

### 分組任務（選一）
1. **樓梯組**：加扶手、平台、轉折
2. **立面組**：遮陽系統，根據方位調整
3. **結構組**：柱樑系統，自動避開

### AI協作提示
```
我的樓梯程式碼：[貼上]
建築規範：[當地規範]
請幫我檢查：
1. 是否符合規範
2. 如何加入無障礙設計
3. 結構合理性
```

---

## Week 7: 環境回應設計

### 核心：別做無意義的分析

### 日照驅動立面
```python
# 簡化版日照分析
sun_vector = rg.Vector3d(1, 1, -2)  # 夏季下午

shade_angles = []
for point in facade_points:
    # 計算需要的遮陽角度
    angle = rg.Vector3d.VectorAngle(
        sun_vector,
        rg.Vector3d.ZAxis
    )
    shade_angles.append(angle)

# 根據角度調整百葉
```

### 實戰任務
1. 南向立面：最大遮陽
2. 北向立面：最大採光
3. 東西向：可調節系統

---

## Week 8: 資料視覺化

### 別做花哨的圖表，做有用的

### 範例：結構應力視覺化
```python
# 把數據映射到顏色/大小
def map_value(value, min_val, max_val):
    normalized = (value - min_val) / (max_val - min_val)
    return normalized

# 應用到幾何
for i, beam in enumerate(beams):
    stress = stress_values[i]
    color_value = map_value(stress, min_stress, max_stress)

    # 紅色=危險，綠色=安全
    color = rg.ColorHSL(
        0.3 - color_value * 0.3,  # 色相從綠到紅
        0.8,  # 飽和度
        0.5   # 亮度
    )
```

---

## Week 9: 演算法優化

### 原則：能用簡單方法就別用複雜的

### 遺傳演算法接入
```python
# Galapagos的基因解碼
def decode_genes(genes):
    # genes是0-1的列表
    floor_count = int(genes[0] * 10) + 10
    floor_height = genes[1] * 2 + 3
    rotation = genes[2] * 90

    return floor_count, floor_height, rotation

# 評估函數
def evaluate(building):
    score = 0
    score += building.floor_area * 0.5
    score -= building.structure_cost * 0.3
    score += building.daylight * 0.2
    return score
```

### 別優化假問題
- 真的需要最優解？
- 80分方案夠不夠？
- 優化的代價值得嗎？

---

## Week 10: 外部整合

### 連接真實資料

### CSV資料讀取
```python
import csv

# 讀取場地資料
with open(file_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        x = float(row['x'])
        y = float(row['y'])
        value = float(row['pollution'])

        # 根據資料生成幾何
```

### API連接（選做）
```python
import urllib.request
import json

# 取得即時資料
url = "https://api.weather.com/..."
response = urllib.request.urlopen(url)
data = json.loads(response.read())

# 轉換為設計參數
wind_speed = data['wind']['speed']
temperature = data['main']['temp']
```

---

## 期中專案（Week 10）

### 要求
1. 解決一個真實建築問題
2. 至少用3個週次的技術
3. 能說明為什麼這樣做

### 評分重點
- 問題定義清楚 30%
- 技術實現合理 40%
- 可以實際使用 30%

### 反面教材
- 做個很炫但沒用的造型
- 堆砌技術不解決問題
- 複雜到自己都不懂

### 範例題目
1. 停車場自動配置系統
2. 公寓平面自動生成
3. 結構柱位優化
4. 立面開窗優化
5. 逃生路線檢查