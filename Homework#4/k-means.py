import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Download stop words if not already downloaded
nltk.download("stopwords")

# Load news headlines from file
with open("news.txt", "r") as f:
    headlines = f.readlines()

# Remove newline characters
headlines = [headline.strip() for headline in headlines]

# Define vectorizer to create TF-IDF matrix
vectorizer = TfidfVectorizer(stop_words="english")

# Create TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(headlines)
# tfidf_matrix.shape = (300, 1445)

# Cluster headlines using K-means with k=2, 3, and 4
for k in [2, 3, 4]:
    # Create K-means model
    kmeans_model = KMeans(n_clusters=k, random_state=42)

    # Fit model to TF-IDF matrix
    kmeans_model.fit(tfidf_matrix)

    # Print keywords for each cluster
    print(f"Cluster analysis with k={k}")
    for i in range(k):
        print(f"Cluster {i+1} keywords:", end=" ")
        # Get indices of headlines in current cluster
        cluster_indices = (kmeans_model.labels_ == i).nonzero()[0]
        # Get top 5 words by TF-IDF score in current cluster
        current_cluster_mean = tfidf_matrix[cluster_indices, :].mean(axis=0).tolist()[0]
        top_words_indices = np.array(current_cluster_mean).argsort()[-3:][::-1]
        # Map top word indices to actual words using vectorizer
        top_words = [vectorizer.get_feature_names_out()[i] for i in top_words_indices]
        print(", ".join(top_words))
