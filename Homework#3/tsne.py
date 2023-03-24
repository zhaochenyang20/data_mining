import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
import openTSNE

# Load data
data = pd.read_csv("/Users/zhaochen20/Git/THU_CST/2023_spring/数据挖掘/data_mining/Homework#3/100_word_vector.txt", header=None, index_col=0, sep=" ")

# t-SNE
tsne = openTSNE.TSNE(
    n_components=2,
    perplexity=30,
    metric="euclidean",
    n_jobs=-1,
    random_state=42,
    initialization="random",
    learning_rate=200,
)
data_tsne = tsne.fit(data)
colors = sns.color_palette("hls", 4)
colors_plot = np.repeat(np.arange(1, 101), 1)
colors_plot[0:20] = 1
colors_plot[20:40] = 2
colors_plot[40:60] = 3
colors_plot[60:100] = 4
for i in range(1, 5):
    plt.scatter(data_tsne[colors_plot == i, 0], data_tsne[colors_plot == i, 1], c=colors[i-1], label=["COMPUTER", "COUNTRY", "WEATHER", "--"][i-1])
plt.xlim(-6, 6)
plt.ylim(-8, 6)
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.title("t-SNE Plot")
plt.legend(["COMPUTER", "COUNTRY", "WEATHER", "--"])
plt.show()
