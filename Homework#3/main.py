import os
import re
from tqdm import tqdm
import xml.etree.cElementTree as et
from collections import Counter
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wordcloud
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from pathlib import Path
root = Path.cwd()


def get_content_and_classes_from_file(file_path: str) -> tuple:
    tree = et.ElementTree(file=file_path)
    content = ""
    class_list = []

    for elem in tree.iter(tag="block"):
        if elem.attrib["class"] == "full_text":
            for i in elem:
                content += " " + i.text

    for elem in tree.iter(tag="classifier"):
        if elem.attrib["type"] == "taxonomic_classifier":
            for prefix in ["Top/News/", "Top/Features/"]:
                if prefix in elem.text:
                    x = elem.text.split("/")
                    if len(x) > 2:
                        class_list.append(x[2])

    content_and_classes = (
        content if content != "" else None,
        class_list if class_list != [] else None,
    )

    return content_and_classes


def get_date_from_file(tree: et.ElementTree) -> tuple:
    for elem in tree.iter(tag="meta"):
        if elem.attrib["name"] == "publication_day_of_month":
            day = elem.attrib["content"] or pd.NA
        if elem.attrib["name"] == "publication_month":
            month = elem.attrib["content"] or pd.NA
        if elem.attrib["name"] == "publication_year":
            year = elem.attrib["content"] or pd.NA

    return day, month, year


def process_content(
    content: str, stemmer: SnowballStemmer, stop_words: set, punctuations: str
) -> List[str]:
    content_clean = re.sub(punctuations, "", content).lower()
    tokens = word_tokenize(content_clean)
    tokens_no_stopwords = [word for word in tokens if word not in stop_words]
    return [stemmer.stem(word) for word in tokens_no_stopwords]


def create_bag_of_words(
    processed_content: List[str], all_unique_words: List[str]
) -> np.ndarray:
    bag_of_words = np.zeros(len(all_unique_words))
    for word in processed_content:
        if word in all_unique_words:
            bag_of_words[all_unique_words.index(word)] += 1
    return bag_of_words

def main():
    # Initial setup
    df = pd.DataFrame(columns=["day", "month", "year", "classes", "content", "processed_content"])
    files_list = os.listdir("./nyt_corpus/samples_500")
    all_words = []
    all_classes = []

    stemmer = SnowballStemmer("english")
    stop_words = set(stopwords.words("english"))
    punctuations = r"[0-9’!\"#$%&'()*+./,-:;><=?【】《》？@，。?★、…“”‘’！[\]^_`{|}~]+"

    # Data extraction and processing
    if not (root / "df.npy").exists():
        for file_name in tqdm(files_list):
            file_path = os.path.join("./nyt_corpus/samples_500", file_name)
            tree = et.ElementTree(file=file_path)

            day, month, year = get_date_from_file(tree)
            content, classes = get_content_and_classes_from_file(file_path)

            all_classes.extend(classes) if classes != None else None
            if content != None:
                processed_content = process_content(
                    content, stemmer, stop_words, punctuations
                )
                all_words.extend(processed_content)

            data = {
                "day": day,
                "month": month,
                "year": year,
                "classes": str(classes) if classes else pd.NA,
                "content": str(content) if content else pd.NA,
                "processed_content": process_content(
                    content, stemmer, stop_words, punctuations
                ) if content else None,
            }
            df = df.append(data, ignore_index=True)
        np.save(str(root / "df"), np.array(df))
        np.save(str(root / "all_words_and_classes"), np.array({"all_words": all_words, "all_classes": all_classes}))
    else:
        df = pd.DataFrame(np.load(str(root / "df.npy"), allow_pickle=True))
        name_dict = {
            0: "day",
            1: "month",
            2: "year",
            3: "classes",
            4: "content",
            5: "processed_content",
        }
        df.rename(columns=name_dict, inplace=True)
        all_words, all_classes = np.load(str(root / "all_words_and_classes.npy"), allow_pickle=True).item().values()
    # Analyzing data
    all_unique_words = list(set(all_words))
    if not (root / "bow.npy").exists():
        bag_of_words_all = np.asarray([create_bag_of_words(processed_content, all_unique_words) for processed_content in tqdm(df.processed_content) if processed_content != None])
        np.save(str(root / "bow"), bag_of_words_all)
    else:
        bag_of_words_all = np.load(str(root / "bow.npy"))
    print(bag_of_words_all)

    top_words = Counter(all_words).most_common(100)
    print(top_words)

    word_lengths = np.zeros(32)
    for word in all_words:
        word_lengths[len(word)] += 1

    file_word_freq = np.asarray([len(content.split()) for content in df.content if not pd.isna(content)])

    month_freq = np.zeros(12)
    for i in df.month:
        month_freq[int(i) - 1] += 1

    classes_freq = Counter(all_classes)

    # Visualization
    wc = wordcloud.WordCloud(max_words=100, scale=10, background_color="black")
    wc.generate(" ".join(all_words))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    plt.bar(range(32), word_lengths)
    plt.show()

    width_counts = pd.cut(file_word_freq, 10).value_counts()
    plt.bar(range(len(width_counts)), list(width_counts), tick_label=width_counts.index)
    plt.xticks(rotation=45)
    plt.show()

    height_counts = pd.qcut(file_word_freq, 10).value_counts()
    plt.bar(
        range(len(height_counts)), list(height_counts), tick_label=height_counts.index
    )
    plt.xticks(rotation=45)
    plt.show()

    plt.bar(classes_freq.keys(), classes_freq.values())
    plt.xticks(rotation=45)
    plt.show()

    plt.bar(range(1, 13), month_freq)
    plt.show()


if __name__ == "__main__":
    main()
