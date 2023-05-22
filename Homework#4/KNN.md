# K-Means

## 实现思路

1. 构造 TF-IDF 矩阵：首先读取新闻标题，去除标题末尾的换行符。使用 `TfidfVectorizer` 类，将新闻标题转换为 TF-IDF 矩阵。该类将自动执行文本预处理步骤，例如分词和停用词去除，而后生成词语的 TF-IDF 权重值，表示每个新闻标题的特征。

2. K-means 聚类：使用 `KMeans` 类，对新闻标题的 TF-IDF 矩阵进行聚类，得到 k 个聚类。

3. 输出聚类特征：对于每个聚类，计算该聚类中每个词语的平均 TF-IDF 权重值，并选择权重最高的 3 个词语作为该聚类的关键词。最后，输出每个聚类的关键词，以便进一步分析和理解聚类的结果。

## 结果与分析

```py
Cluster analysis with k=2
Cluster 1 keywords: make, police, man
Cluster 2 keywords: best, recipes, instagram
Cluster analysis with k=3
Cluster 1 keywords: make, police, man
Cluster 2 keywords: best, recipes, instagram
Cluster 3 keywords: winter, foods, olympics
Cluster analysis with k=4
Cluster 1 keywords: police, shooting, man
Cluster 2 keywords: mlb, games, cancels
Cluster 3 keywords: make, need, world
Cluster 4 keywords: best, foods, recipes
```

根据这些聚类结果，我们可以得到以下分析：

1. 当 k=2 时，新闻标题被分成了两个聚类。第一个聚类的关键词是"make", "police", "man"，而第二个聚类的关键词是"best", "recipes", "Instagram"。这表明新闻标题涉及了不同的主题，一部分是关于警察和犯罪的报道，另一部分则是关于最佳食谱和社交媒体的报道。

2. 当 k=3 时，新闻标题被分成了三个聚类。第一个聚类与 k=2 时相同，关键词是"make", "police", "man"，第二个聚类也与 k=2 时相同，关键词是 "best", "recipes", "instagram"。而第三个聚类的关键词是 "winter", "foods", "olympics"。这表明新闻标题涉及了更广泛的主题，一部分是关于警察和犯罪的报道，一部分是关于最佳食谱和社交媒体的报道，另一部分则是关于冬季食物和奥运会的报道。

3. 当k=4时，新闻标题被分成了四个聚类。第一个聚类的关键词是 "police", "shooting", "man"，第二个聚类的关键词是 "mlb", "games", "cancels"，第三个聚类的关键词是 "make", "need", "world"，第四个聚类的关键词是 "best", "foods", "recipes"。这表明新闻标题涉及了更多的主题，包括警察和犯罪、美国职业棒球比赛的取消、全球的制造需求以及最佳食谱。

总的来说，这些聚类结果表明新闻标题涉及了多个主题和话题，包括警察和犯罪、美国职业棒球比赛的取消、最佳食谱和社交媒体、冬季食物和奥运会等。通过进一步分析这些聚类结果，我们可以更深入地了解新闻标题所涉及的内容和趋势，并为相关领域的研究提供有用的信息。

此外，从给出的聚类结果来看，随着聚类数目增加，分类效果可能有所提高，但并不是每次增加聚类数目都能获得更好的结果。

当聚类数目从 2 增加到 3 时，聚类结果的准确性有所提高，因为新闻标题被分为了 3 个主题较为明确的聚类。而当聚类数目从 3 增加到 4 时，分类效果则有所下降，因为其中一个聚类的关键词没有明确的主题。

可见，增加聚类数目的影响不是单调的，而是受到多种因素的影响，例如聚类方法、聚类特征的选择、数据集大小等等。在实际应用中，需要根据具体问题和需求来选择合适的聚类数目，并进一步优化聚类方法和特征，以达到更好的分类效果。
