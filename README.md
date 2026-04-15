# EcomLocalization-LLM
# 基于LLM实现跨境电商的本土化

> 利用主题模型（LDA/Top2Vec）与大语言模型（ChatGPT/DeepSeek），对跨境电商平台商品评论进行本土化主题挖掘与分析。  
> 数据来源：京东（JD.com），覆盖旗袍、水果、手机等多品类。

---

## 📁 项目结构

```
EcomLocalization-LLM/
│
├── 1_data_collection/        # 数据采集
│   ├── jd_packaged.py        # 京东评论爬虫（封装版，基于 DrissionPage）
│   ├── scrapy.py             # 另一种爬取方式
│   └── shujupaqu11.py        # 早期数据采集脚本
│
├── 2_preprocessing/          # 数据预处理
│   ├── data_process.py       # 数据清洗与格式化
│   ├── comment_preprocess.py  # 中文评论预处理（分词/去噪）
│   ├── Delete_NotHotWorde.py  # 删除非热门词
│   ├── merge_comment_labels.py # 评论标签合并
│   ├── Occur_Of_Words.py     # 词频统计
│   ├── UpdateTxt.py          # 文本更新工具
│   ├── NewExcel.py           # Excel 新建工具
│   ├── XlsxToXls.py          # Excel 格式转换
│   ├── sentencebert_mlm.py   # Sentence-BERT MLM 预处理
│   └── stopwords.txt         # 中文停用词表
│
├── 3_topic_modeling/         # 主题建模
│   ├── LDA/                  # LDA Python 脚本
│   │   ├── LDAsklearn_origin.py    # sklearn LDA 主实现
│   │   ├── LDA_Coherence.py        # 主题一致性评估
│   │   ├── TF_IDF.py               # TF-IDF 特征提取
│   │   ├── perplexity.py           # 困惑度计算
│   │   ├── lda_catch.py            # LDA 模型缓存
│   │   ├── mainhanshu.py           # 主函数入口
│   │   ├── util.py                 # 工具函数
│   │   ├── word2vec_ex.py          # Word2Vec 扩展
│   │   ├── sentiment_score.py       # 情感分析
│   │   ├── feature_negative_improvement.py # 负面特征改进
│   │   ├── run.py                   # 主运行入口
│   │   └── test.py                  # 测试脚本
│   └── notebooks/            # Jupyter 实验 Notebooks
│       ├── tfidf_lda.ipynb         # TF-IDF + LDA
│       ├── word2vec_lda.ipynb      # Word2Vec + LDA
│       ├── bert_lda.ipynb          # BERT Embedding + LDA
│       ├── sentencebert_lda.ipynb  # Sentence-BERT + LDA
│       ├── sentencebert_mlm_lda.ipynb # Sentence-BERT MLM + LDA
│       ├── ChatGpt_lda.ipynb       # ChatGPT 辅助 LDA
│       └── DeepSeek_lda.ipynb      # DeepSeek 辅助 LDA
│
├── 4_clustering/             # 聚类分析（Top2Vec + BERT K-Means）
│   ├── 1.top2vec_clothes.py      # 服装品类 Top2Vec
│   ├── 1.top2vec_fruit.py        # 水果品类 Top2Vec
│   ├── 1.top2vec_phone.py        # 手机品类 Top2Vec
│   ├── 2.bert_kmeans_clothes.py  # 服装 BERT + K-Means
│   ├── 2.bert_kmeans_fruit.py    # 水果 BERT + K-Means
│   ├── 2.bert_kmeans_phone.py    # 手机 BERT + K-Means
│   └── task_notes.txt            # 任务说明
│
├── 5_visualization/          # 可视化
│   ├── make_ciyun.py         # 中文词云生成
│   ├── make_ciyun_en.py      # 英文词云生成
│   ├── make_pie.py           # 饼图生成
│   ├── separate_comments.py  # 评论分类
│   ├── plot.ipynb            # 综合可视化 Notebook
│   └── data_analysis.ipynb   # 数据分析 Notebook
│
├── data/                     # 数据目录（不纳入版本控制）
│   ├── comments/             # 原始评论 CSV
│   └── ciyuntu/              # 词云输出图片
│
├── README.md
└── LICENSE
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install DrissionPage gensim scikit-learn transformers sentence-transformers top2vec jieba wordcloud
```

### 2. 数据采集

```bash
python 1_data_collection/jd_packaged.py
```
> 修改脚本中的 `product_id` 和 `output_file` 参数即可爬取目标商品评论。  
> 另可参考教程：[基于 Instant Data Scraper 爬取评论](https://www.yuque.com/fushengweixie-s2nxx/gkwq83/grspg94yp4pvzsa6)

### 3. 数据预处理

```bash
python 2_preprocessing/comment_preprocess.py
```

### 4. 主题建模

打开 `3_topic_modeling/notebooks/` 下对应的 Notebook 运行即可，各 Notebook 对应不同 Embedding 方法：

| Notebook | 方法 |
|---|---|
| `tfidf_lda.ipynb` | TF-IDF + LDA |
| `bert_lda.ipynb` | BERT + LDA |
| `sentencebert_lda.ipynb` | Sentence-BERT + LDA |
| `DeepSeek_lda.ipynb` | DeepSeek LLM 辅助 |
| `ChatGpt_lda.ipynb` | ChatGPT 辅助 |

### 5. 聚类分析

```bash
python 4_clustering/1.top2vec_clothes.py
python 4_clustering/2.bert_kmeans_clothes.py
```

### 6. 可视化

```bash
python 5_visualization/make_ciyun.py
```

---

## 📋 环境要求

- Python 3.8+
- Chrome 浏览器 + ChromeDriver（用于爬虫）
- 推荐使用 Jupyter Notebook 运行实验

---

## 📄 License

[MIT License](LICENSE)
