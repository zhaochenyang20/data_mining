import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import openTSNE
from pathlib import Path


def main():
    # Load data
    data = pd.read_csv(str(Path.cwd() / "100_word_vector.txt"), header=None, index_col=0, sep=" ")

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
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()