# 0.4.8 序列運算 List Functions
# 頁碼：31-32

# 插入序列：
List = [75, 32, 10, 64, 53]
List.insert(2, 105)
print(List)  # [75, 32, 105, 10, 64, 53]

# Line Description:
# 2  將 105 插入 List 內編號為 2 的位置
# 3  輸出 List

# 附加數據於序列尾端：
List = [75, 32, 10, 64, 53]
List.append(105)
print(List)  # [75, 32, 10, 64, 53, 105]

# Line Description:
# 2  將 105 附加於 List 內的尾端
# 3  輸出 List

# 移除序列中的一個數據：
List = [75, 32, 10, 64, 53]
del List[1]
print(List)  # [75, 10, 64, 53]

# Line Description:
# 2  移除 List 內編號為 1 的數據
# 3  輸出 List

# 移除序列中的一個數據並回傳此數據：
List = [75, 32, 10, 64, 53]
print(List.pop(1))  # 32
print(List)  # [75, 10, 64, 53]

# Line Description:
# 2  移除 List 內編號為 1 的數據並回傳此數據
# 3  輸出 List

# ============================================
# 複製序列：
List = [75, 32, 10, 64, 53]
List2 = List[:]
print(List2)  # [75, 32, 10, 64, 53]

# Line Description:
# 2  複製序列 List，並命名為 List2
# 3  輸出 List

# 序列運算 append 與 extend 比較：
# append 僅為附加，extend 稱為擴增，同樣都是將數據加到單一個序列的尾端，運算有著些許的不同
# 差別在於若附加的數據為一組序列時，就會產生資料結構上的不同

# 以下用兩個範例作為比較，對比兩者輸出的資料結構：

ListA = [1, 3, 9]
ListB = [4, 5, 6]
ListA.append(ListB)
print(ListA)  # [1, 3, 9, [4, 5, 6]]

ListA = [1, 3, 9]
ListB = [4, 5, 6]
ListA.extend(ListB)
print(ListA)  # [1, 3, 9, 4, 5, 6]