import math
import string
from functools import partial
from multiprocessing import Pool, cpu_count
import multiprocessing as mp
from pathlib import Path
from nltk.corpus import stopwords
from tqdm import tqdm
import numpy as np
from collections import defaultdict
from itertools import combinations

dir_path = Path.cwd()


# 构造词典

def process_text(text):
    # 全部转化为小写字母
    text = text.lower()
    # 去掉标点符号
    text = text.translate(str.maketrans("", "", string.punctuation))
    # &转“and”
    text = text.replace("&", "and")
    # .的转与留
    text = list(text)
    for i in range(2, len(text)):
        if text[i] == "." and (
            48 <= ord(text[i - 2]) <= 57 or 97 <= ord(text[i - 2]) <= 122
        ):
            text[i] = " "
    text = "".join(text)
    # 去掉空词
    text = [word for word in text.split() if word]
    # 去掉英文停用词
    stops = set(stopwords.words("english"))
    text = [word for word in text if word not in stops]
    return text

def dict_construct():
    all_words = []
    all_pages = []
    corpus_dir = dir_path / "nyt_corp0"
    for file in corpus_dir.iterdir():
        # 读取新闻语料文件
        with open(str(file), "r", encoding="utf-8") as f:
            lang_material = f.read()
            pro_list = process_text(lang_material)
            all_pages.append(pro_list)
            all_words.extend(pro_list)
    # 去重
    all_words = list(set(all_words))
    return all_pages, all_words


# 表示为 tf-idf 向量

def tf_idf_cal(page, all_words, all_pages):
    tf_idf = []
    for word in all_words:
        # tf：某个词在文章中出现的次数/文章总词数
        tf = page.count(word) / len(page)
        #! idf：log(语料库的文档总数/(包含该词的文档数))
        include = 0
        for passage in all_pages:
            if passage.count(word) != 0:
                include += 1
        idf = math.log(len(all_pages) / (include))
        # tf-idf = tf * idf
        tfidf = tf * idf
        tf_idf.append(tfidf)
    return tf_idf


def cal_co_exist(words_to_index):
    co_exist_matrix = np.zeros((len(words_to_index), len(words_to_index)), dtype=int)
    for page in all_pages:
        for word1, word2 in combinations(list(set(page)), 2):
            co_exist_matrix[words_to_index[word1], words_to_index[word2]] += 1
            co_exist_matrix[words_to_index[word2], words_to_index[word1]] += 1
    return co_exist_matrix

def compute_distance(array_1, array_2):
    array_1, array_2 = np.array(array_1), np.array(array_2)
    euclidean_distance = np.linalg.norm(array_1 - array_2)
    cosine_similarity = np.dot(array_1, array_2) / (np.linalg.norm(array_1) * np.linalg.norm(array_2))
    return euclidean_distance, cosine_similarity

if __name__ == '__main__':
    if not (dir_path / "pages.npy").exists():
        print("constructing dictionary...")
        all_pages, all_words = dict_construct()
        np.save(str(dir_path / "pages"), np.array({"all_pages": all_pages, "all_words": all_words}))
    else:
        all_pages, all_words = np.load(str(dir_path / "pages.npy"), allow_pickle=True).item().values()

    words_to_index = {word: index for index, word in enumerate(all_words)}

    print("calculating tf-idf...")
    if not (dir_path / "tf_idf.npy").exists():
        tf_idf_cal_passage = partial(tf_idf_cal, all_words=all_words, all_pages=all_pages)
        with Pool() as p:
            tf_idf_vector = list(tqdm(p.imap(tf_idf_cal_passage, all_pages), total=len(all_pages)))
        np.save(str(dir_path / "tf_idf"), np.array(tf_idf_vector))
    else:
        tf_idf_vector = np.load(str(dir_path / "tf_idf.npy"), allow_pickle=True)

    print("calculating co-exist matrix...")
    if not (dir_path / "co_exist.npy").exists():
        co_exist_matrix = cal_co_exist(words_to_index)
        np.save(str(dir_path / "co_exist"), co_exist_matrix)
    else:
        co_exist_matrix = np.load(str(dir_path / "co_exist.npy"), allow_pickle=True)

    doc_index = 132
    doc_dict = {}
    for index in range(len(all_pages)):
        euclidean_distance, cosine_similarity = compute_distance(tf_idf_vector[doc_index], tf_idf_vector[index])
        doc_dict[index] = (euclidean_distance, cosine_similarity)
    sorted_doc_dict = sorted(doc_dict.items(), key=lambda x: x[1][0])
    print("top 10 similar documents in euclidean distance:")
    print(sorted_doc_dict[:10])
    sorted_doc_dict = sorted(doc_dict.items(), key=lambda x: x[1][1], reverse=True)
    print("top 10 similar documents in cosine similarity:")
    print(sorted_doc_dict[:10])

    word = "school"
    word_dict = {}
    for term in all_words:
        euclidean_distance, cosine_similarity = compute_distance(co_exist_matrix[words_to_index[word]], co_exist_matrix[words_to_index[term]])
        word_dict[term] = (euclidean_distance, cosine_similarity)
    sorted_word_dict = sorted(word_dict.items(), key=lambda x: x[1][0])
    print("top 10 similar words in euclidean distance:")
    print(sorted_word_dict[:10])
    sorted_word_dict = sorted(word_dict.items(), key=lambda x: x[1][1], reverse=True)
    print("top 10 similar words in cosine similarity:")
    print(sorted_word_dict[:10])