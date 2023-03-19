from typing import Counter
import xml.etree.cElementTree as et
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
import matplotlib.pyplot as plt
import wordcloud
import re
from tqdm import tqdm

df = pd.DataFrame(columns=["day", "month", "year", "classes", "content"])
files_list = os.listdir("./nyt_corpus/samples_500")
classes_step7 = []
for file_name in tqdm(files_list):
    eletree = et.ElementTree(file="./nyt_corpus/samples_500/" + file_name)
    content = ""
    for elem in eletree.iter(tag="block"):
        if elem.attrib["class"] == "full_text":
            for i in elem:
                content += " " + i.text
    if len(content) == 0:
        content = pd.NA
    class_list = []
    for elem in eletree.iter(tag="classifier"):
        if elem.attrib["type"] == "taxonomic_classifier":
            if "Top/News/" in elem.text:
                x = elem.text.split("/")
                if len(x) > 2:
                    class_list.append(x[2])
            if "Top/Features/" in elem.text:
                x = elem.text.split("/")
                if len(x) > 2:
                    class_list.append(x[2])
    class_list = list(set(class_list))
    classes = str(class_list)
    if len(classes) == 2:
        classes = pd.NA
    classes_step7.extend(class_list)
    for elem in eletree.iter(tag="meta"):
        if elem.attrib["name"] == "publication_day_of_month":
            day = elem.attrib["content"]
            if (len(str(day))) == 0:
                day = pd.NA
        if elem.attrib["name"] == "publication_month":
            month = elem.attrib["content"]
            if (len(str(month))) == 0:
                month = pd.NA
        if elem.attrib["name"] == "publication_year":
            year = elem.attrib["content"]
            if (len(str(year))) == 0:
                year = pd.NA
    data = {
        "day": day,
        "month": month,
        "year": year,
        "classes": classes,
        "content": [content],
    }
    df_new = pd.DataFrame(data)
    df = pd.concat([df_new, df])
print(df)
all_file_content = df.content.tolist()
all_words_step2 = []
for content in tqdm(all_file_content):
    stemmer_word = nltk.stem.SnowballStemmer("english")
    stop_words = set(stopwords.words("english"))
    punctuations = "[0-9’!\"#$%&'()*+./,-:;><=?【】《》？@，。?★、…“”‘’！[\\]^_`{|}~]+"
    content1 = re.sub(punctuations, "", str(content))
    content2 = content1.lower()
    content3 = word_tokenize(content2)
    content4 = [word for word in content3 if word not in stop_words]
    content5 = [stemmer_word.stem(word) for word in content4]
    all_words_step2.extend(content5)
# print(all_words_step2)
all_words_step2_set = []
for i in all_words_step2:
    if i not in all_words_step2_set:
        all_words_step2_set.append(i)
bag_of_words_step3 = []
for content in tqdm(all_file_content):
    stemmer_word = nltk.stem.SnowballStemmer("english")
    stop_words = set(stopwords.words("english"))
    punctuations = "[0-9’!\"#$%&'()*+./,-:;><=?【】《》？@，。?★、…“”‘’！[\\]^_`{|}~]+"
    content1 = re.sub(punctuations, "", str(content))
    content2 = content1.lower()
    content3 = word_tokenize(content2)
    content4 = [word for word in content3 if word not in stop_words]
    content5 = [stemmer_word.stem(word) for word in content4]
    bag_of_words = []
    bag_of_words = np.zeros(len(all_words_step2_set))
    for word in all_words_step2_set:
        for w in content5:
            if word == w:
                bag_of_words[all_words_step2_set.index(word)] += 1
    bag_of_words_step3.append(bag_of_words)
print(bag_of_words_step3)
all_str_words = " ".join(all_words_step2)
wc = wordcloud.WordCloud(max_words=100, scale=10, background_color="black")
words_top = Counter(all_words_step2)
print(words_top.most_common(100))
wc.generate(all_str_words)
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
word_length = np.zeros(32)
for i in all_words_step2:
    word_length[len(i)] += 1
X = []
for i in range(32):
    X.append(i)
plt.bar(X, word_length)
plt.show()
print(word_length)
file_word_fre = np.zeros(500)
for i in range(500):
    if len(str(all_file_content[i])) > 5:
        word_num = all_file_content[i].split()
        file_word_fre[i] = len(word_num)

width = pd.cut(file_word_fre, 10).value_counts()
plt.bar(range(len(width)), list(width), tick_label=width.index)
plt.xticks(rotation=45)
plt.show()
height = pd.qcut(file_word_fre, 10).value_counts()
plt.bar(range(len(height)), list(height), tick_label=height.index)
plt.xticks(rotation=45)
plt.show()
classes_step7_set = list(set(classes_step7))
class_fre = np.zeros(len(classes_step7_set))
for j in range(len(classes_step7_set)):
    class_fre[j] = classes_step7.count(classes_step7_set[j])
plt.bar(classes_step7_set, class_fre)
plt.xticks(rotation=45)
plt.show()
month = np.zeros(12)
for i in range(12):
    month[i] = i + 1
month_file = df.month.tolist()
month_fre = np.zeros(12)
for i in range(len(month_file)):
    month_fre[int(month_file[i]) - 1] += 1
plt.bar(month, month_fre)
plt.show()
