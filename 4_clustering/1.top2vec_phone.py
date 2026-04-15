#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：
@Date    ：2024/01/01 00:00 
@Note    ：
'''
import pandas as pd
import os, re
import matplotlib.pyplot as plt
from top2vec import Top2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from sklearn.manifold import TSNE
import seaborn as sns
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
import jieba

# 中文分词
def chinese_tokenizer(text):
    return [word for word in jieba.cut(text) if len(word.strip()) > 1]

def calculate_coherence(model, texts, coherence_type='c_v'):
    dictionary = Dictionary(texts)

    # 获取主题关键词
    topic_words, _, _ = model.get_topics()
    topics = [words[:10].tolist() for words in topic_words]  # 取每个主题前10个关键词
    # print(topics)
    # 计算一致性
    coherence_model = CoherenceModel(
        topics=topics,
        texts=texts,
        dictionary=dictionary,
        coherence=coherence_type
    )
    return coherence_model.get_coherence()

if __name__ == "__main__":
    # 数据加载和预处理
    df = pd.read_excel("./data/手机.xlsx", names=["类型", "评价", "内容"])

    # 中文分词处理
    # jieba.enable_paddle()  # 启用paddle模式提高分词精度
    texts = [chinese_tokenizer(str(doc)) for doc in df["内容"]]

    model = Top2Vec(documents=df["内容"].tolist(),
                    speed="learn",
                    workers=4,
                    embedding_model='universal-sentence-encoder',
                    embedding_model_path='./model/')

    # 计算三种主题一致性
    cv_score = calculate_coherence(model, texts, 'c_v')
    umass_score = calculate_coherence(model, texts, 'u_mass')

    topics, topic_sizes, topic_nums = model.get_topics()
    # 计算不同主题间的余弦相似度
    unique_topics = np.unique(topics)
    cosine_similarities = []
    for i in range(len(unique_topics)):
        for j in range(i + 1, len(unique_topics)):
            topic_i = model.topic_vectors[i]
            topic_j = model.topic_vectors[j]
            cosine_sim = cosine_similarity([topic_i], [topic_j])[0][0]
            cosine_similarities.append(cosine_sim)
    average_cosine_similarity = np.mean(cosine_similarities)

    # 获取文档主题分配数组（形状：num_docs）
    doc_topics = model.doc_top

    # 生成主题文档存在矩阵（二进制表示）
    topic_doc_binary = np.zeros((len(model.topic_sizes), len(doc_topics)), dtype=int)
    for topic_num in range(len(model.topic_sizes)):
        topic_doc_binary[topic_num] = (doc_topics == topic_num).astype(int)

    # 计算Jaccard相似度
    jaccard_similarities = []
    for i in range(len(model.topic_sizes)):
        for j in range(i + 1, len(model.topic_sizes)):
            sim = jaccard_score(topic_doc_binary[i], topic_doc_binary[j])
            jaccard_similarities.append(sim)

    average_jaccard = np.mean(jaccard_similarities)

    # 聚类可视化
    tsne = TSNE(n_components=2, random_state=42)
    tsne_results = tsne.fit_transform(model.document_vectors)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=tsne_results[:, 0], y=tsne_results[:, 1], hue=model.doc_top, palette='viridis')
    plt.title('Top2vec Phone')
    plt.savefig("./pic/top2vec_phone.png")

    # 输出结果
    print(f"C_v 一致性: {cv_score:.4f}")
    print(f"u_mass 一致性: {umass_score:.4f}")
    print("簇中心余弦相似度平均值：", average_cosine_similarity)
    print("关键词Jaccard相似度平均值：", average_jaccard)
