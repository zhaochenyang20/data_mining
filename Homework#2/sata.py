import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 读入浮点数组
arr = np.array(
    [
        9.0,
        26.5,
        7.8,
        17.8,
        31.4,
        26.5,
        27.4,
        26.5,
        34.6,
        43.0,
        28.8,
        33.4,
        27.4,
        34.1,
        32.9,
        41.2,
    ]
)

# 对数组进行排序
arr_sorted = np.sort(arr)
print(arr_sorted)

# 计算均值、中位数和众数
mean = np.mean(arr_sorted)
median = np.median(arr_sorted)
mode = stats.mode(arr_sorted)[0][0]

# 计算五数概括
q1, q2, q3 = np.percentile(arr_sorted, [25, 50, 75])
min = np.min(arr_sorted)
max = np.max(arr_sorted)

# 绘制盒图
fig, ax = plt.subplots()
ax.boxplot(arr_sorted, vert=True)
ax.set_xlabel("Value")
ax.set_title("Box plot")
plt.show()

# 输出结果
print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Mode: {mode:.2f}")
print(f"Min: {min:.2f}")
print(f"Q1: {q1:.2f}")
print(f"Q2: {q2:.2f}")
print(f"Q3: {q3:.2f}")
print(f"Max: {max:.2f}")
