# 1.3.5 螺旋圖形 Spiral Graphic
# 頁碼：64-65（跨頁範例）

import rhinoscriptsyntax as rs

pt2D = []
curveList = []

for i in range(n):
    for j in range(n):
        pt2D.append(rs.AddPoint(size*i, size*j, 0))

for k in range(len(pt2D)):
    IPCPts = []
    for a in range(degree):
        tmpVector = rs.VectorCreate(attPt, pt2D[k])
        unitVector = rs.VectorUnitize(tmpVector)
        vector = rs.VectorScale(unitVector, mult)
        vector = rs.VectorRotate(vector, angle*[0, 0, 1])
        newPt = rs.CopyObject(pt2D[k], vector)
        IPCPts.append(newPt)
        pt2D[k] = newPt

    curve = rs.AddInterCurve(IPCPts, 1)
    curveList.append(curve)

pt2D_out = pt2D
curveList_out = curveList

# Line Description（頁65）:
# 3   創建名為 pt2D 的序列，用來存放二維矩陣點
# 4   創建名為 curveList 的序列，用來存放曲線
# 6-8  創建圖像為 size 的 n*n 二維矩陣點，並儲存到 pt2D 裡
# 10   利用圖像矩陣二維矩陣點所有的一個個點執行
# 11   創建名為 IPCPts 的序列，用來做暫時儲存中的點執行
# 12   利用圖像範圍，複製為 degree，創建內點循環圈讓內級執行數量
# 13   建置下述 attPt 到當前點 pt2D[k] 的向量，命名為 tmpVector
# 14   將向量 tmpVector 單位化運算，命名為 unitVector
# 15   將向量 unitVector 進以 scale，命名為 vector
# 16   以 Z 軸為軸心，旋轉向量 vector，角度為 angle
# 17   將當前點貢獻 vector 得到新的點位置，將新的這點取名為 newPt
# 18   將 newPt 用臨時 IPCPts 儲存
# 19   以 newPt 取代第一次的圖像點矩陣執行下一次的迴圈運算，直到迴圈運算結束為止
# 21   將 IPCPts 內的這些點繪製由內級點繪畫，命名為 curve
# 22   將 curve 用順次 curveList 儲存
# 24   將 pt2D 設於 GhPython 元件的輸出端
# 25   將 curveList 設於 GhPython 元件的輸出端