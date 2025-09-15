# Week 1 作業：AI輔助程式碼分析

## 作業目標
學習使用AI工具（Claude/ChatGPT）來理解Grasshopper Python程式碼

## 作業內容

### Part 1: 基礎分析（30分）
從以下三個範例中，每個使用不同的AI提示詞進行分析：

#### 範例1：點陣列生成
```python
import Rhino.Geometry as rg

# 輸入參數
# x_count: X方向的點數量
# y_count: Y方向的點數量
# spacing: 點之間的間距

points = []
for i in range(x_count):
    for j in range(y_count):
        pt = rg.Point3d(i * spacing, j * spacing, 0)
        points.append(pt)

# 輸出
a = points
```

#### 範例2：圓形陣列
```python
import Rhino.Geometry as rg
import math

# 輸入參數
# center: 中心點
# radius: 半徑
# count: 點的數量

points = []
circles = []

for i in range(count):
    angle = (math.pi * 2 / count) * i
    x = center.X + radius * math.cos(angle)
    y = center.Y + radius * math.sin(angle)
    pt = rg.Point3d(x, y, center.Z)
    points.append(pt)

    circle = rg.Circle(pt, radius * 0.1)
    circles.append(circle)

# 輸出
a = points
b = circles
```

#### 範例3：簡單曲線分割
```python
import Rhino.Geometry as rg

# 輸入參數
# curve: 輸入曲線
# divisions: 分割數量

points = []
parameters = curve.DivideByCount(divisions, True)

if parameters:
    for t in parameters:
        pt = curve.PointAt(t)
        points.append(pt)

# 輸出
a = points
```

### Part 2: 深入理解（40分）

針對每個範例，使用AI完成以下任務：

1. **初步理解**
   - 使用「程式碼初步理解」提示詞
   - 記錄AI的解釋

2. **逐行分析**
   - 使用「逐行解析」提示詞
   - 整理成表格

3. **視覺化描述**
   - 詢問AI這些程式碼會產生什麼視覺效果
   - 嘗試畫出簡單示意圖

### Part 3: 創意改寫（30分）

選擇一個範例，使用AI協助你：

1. **加入隨機性**
   - 詢問如何加入隨機變化
   - 實作並測試

2. **參數化控制**
   - 增加更多控制參數
   - 讓圖案更有變化

3. **錯誤處理**
   - 詢問可能的錯誤情況
   - 加入錯誤處理機制

## 繳交內容

### 1. 分析報告（Word/PDF）
包含：
- 三個範例的AI對話記錄（截圖）
- 你的理解總結（每個範例100字）
- 遇到的問題與解決方式

### 2. 改寫程式碼（.py檔案）
- 原始碼
- 改寫後的程式碼
- 註解說明改動的地方

### 3. Grasshopper檔案（.gh）
- 包含原始和改寫後的Python元件
- 簡單的測試案例

### 4. 學習反思（200字）
- 使用AI學習的心得
- 哪些提示詞最有幫助？
- 下週想要學習的方向

## 評分標準

| 項目 | 配分 | 說明 |
|------|------|------|
| AI對話品質 | 30% | 提示詞使用是否恰當 |
| 理解深度 | 30% | 是否真正理解程式邏輯 |
| 創意改寫 | 25% | 改寫是否有創意且可執行 |
| 文件完整性 | 15% | 繳交內容是否完整清楚 |

## 加分項目
- 使用多個不同的AI工具比較結果（+5分）
- 幫助同學解決問題並記錄（+5分）
- 提出AI回答中的錯誤並修正（+10分）

## 繳交期限
下週上課前上傳至課程平台

## 提醒事項
1. 誠實記錄AI的協助
2. 不要只複製貼上，要理解後用自己的話總結
3. 遇到問題先嘗試用不同提示詞，真的不行才問同學或老師
4. 保留所有對話記錄，期末可能會用到

---

### 有用資源
- [Rhino.Geometry 命名空間文件](https://developer.rhino3d.com/api/RhinoCommon/html/N_Rhino_Geometry.htm)
- [Grasshopper Python入門](https://developer.rhino3d.com/guides/rhinopython/)
- 課程Discord群組（問問題用）