import numpy as np
import pandas as pd
import jieba
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
import matplotlib.pyplot as plt


df = pd.read_excel("./data/水果数据_deal.xlsx")
comments = df["content"].tolist()

# 1. 数据预处理
def preprocess(texts):
    return [text.replace(" ", "").strip() for text in texts]

processed_comments = preprocess(comments)

# 2. 加载BERT模型
tokenizer = BertTokenizer.from_pretrained('./bert-base-chinese')
model = BertModel.from_pretrained('./bert-base-chinese')

def get_embeddings(texts):
    embeddings = []
    for text in texts:
        inputs = tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)

        if hasattr(outputs, 'last_hidden_state'):
            hidden_state = outputs.last_hidden_state
        else:
            hidden_state = outputs[0]

        cls_embedding = hidden_state[:, 0, :].cpu().numpy()
        embeddings.append(cls_embedding)
    return np.concatenate(embeddings, axis=0)

embeddings = get_embeddings(processed_comments)

n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(embeddings)

def get_cluster_keywords(comments, clusters, n_clusters):
    cluster_texts = [' '.join([comments[i] for i in np.where(clusters == j)[0]]) for j in range(n_clusters)]
    tfidf = TfidfVectorizer(max_features=20)
    tfidf_matrix = tfidf.fit_transform(cluster_texts)
    return [tfidf.get_feature_names_out()[np.argsort(tfidf_matrix[j].toarray().flatten())[-10:][::-1]] 
            for j in range(n_clusters)]

keywords_per_cluster = get_cluster_keywords(processed_comments, clusters, n_clusters)

tokenized_comments = [list(jieba.cut(comment)) for comment in processed_comments]
dictionary = Dictionary(tokenized_comments)
corpus = [dictionary.doc2bow(text) for text in tokenized_comments]

topics = []
for keywords in keywords_per_cluster:
    topic = [dictionary.token2id[word] for word in keywords if word in dictionary.token2id]
    topics.append(topic)

cm_u = CoherenceModel(topics=topics, texts=tokenized_comments, dictionary=dictionary, coherence='u_mass')
cm_cv = CoherenceModel(topics=topics, texts=tokenized_comments, dictionary=dictionary, coherence='c_v')

centroid_similarity = cosine_similarity(kmeans.cluster_centers_)
centroid_similarity_average = centroid_similarity.mean()

jaccard_matrix = np.zeros((n_clusters, n_clusters))
for i in range(n_clusters):
    for j in range(n_clusters):
        set_i = set(keywords_per_cluster[i])
        set_j = set(keywords_per_cluster[j])
        intersection = len(set_i & set_j)
        union = len(set_i | set_j)
        jaccard_matrix[i][j] = intersection / union if union != 0 else 0
jaccard_matrix_average = jaccard_matrix.mean()

tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(embeddings_2d[:,0], embeddings_2d[:,1], c=clusters, cmap='tab10', alpha=0.7)
plt.title('BERT KMeans Fruit')
plt.legend(*scatter.legend_elements())
plt.savefig("./pic/BERT_KMeans_fruit.png")

print(f"C_v 一致性: {cm_cv.get_coherence():.4f}")
print(f"u_mass 一致性: {cm_u.get_coherence():.4f}")
print("簇中心余弦相似度平均值：", centroid_similarity_average)
print("关键词Jaccard相似度平均值：", jaccard_matrix_average)

