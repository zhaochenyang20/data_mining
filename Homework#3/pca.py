import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Load data
data = pd.read_csv("/Users/zhaochen20/Git/THU_CST/2023_spring/数据挖掘/data_mining/Homework#3/100_word_vector.txt", header=None, index_col=0, sep=" ")

# PCA
pca = PCA(n_components=2, random_state=42)
data_pca = pca.fit_transform(data)
colors = sns.color_palette("hls", 4)
colors_plot = np.repeat(np.arange(1, 101), 1)
colors_plot[0:20] = 1
colors_plot[20:40] = 2
colors_plot[40:60] = 3
colors_plot[60:100] = 4
for i in range(1, 5):
    plt.scatter(data_pca[colors_plot == i, 0], data_pca[colors_plot == i, 1], c=colors[i-1], label=["COMPUTER", "COUNTRY", "WEATHER", "--"][i-1])
plt.xlabel("PC 1")
plt.ylabel("PC 2")
plt.title("PCA Plot")
plt.legend()
plt.show()

