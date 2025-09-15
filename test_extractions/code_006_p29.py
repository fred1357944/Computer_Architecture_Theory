# 0.4.6 迴圈運算 Loop

# for 迴圈
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# while 迴圈
count = 0
while count < 5:
    print(count)
    count += 1

# 迴圈中的 break 和 continue
for i in range(10):
    if i == 5:
        break  # 跳出迴圈
    if i == 3:
        continue  # 跳過本次迴圈
    print(i)
