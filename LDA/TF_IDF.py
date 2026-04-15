# 利用tf-idf进行主题关键词的过滤
import null
from numpy import nan
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from XlsxToXls import update_excel
import gensim
'''

def TF_IDF_Sum():
    corpus = []

    # 读取预料 一行预料为一个文档


    corpus = ["我 来到 北京 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
    "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
    "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
    "我 爱 北京 天安门"]  # 第四类文本的切词结果
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])
'''



# 读取文件中content_cutted列 进行关键词过滤

import pandas as pd
import numpy as np


'''
    # 对topic_words进行改造
    for item in topic_words:
        #print(item)
        #print(type(item))
        word_list=item.split()
        print(word_list)
        words.extend(word_list)

    print(words)
'''

# TF-IDF进行主题关键词的筛选
# 传入处理后的word_list的数据和主题分析后各个主题的关键词数组
def tf_idf_sum(content_cutted_list,threshold):
    corpus = []
    words=[]
    update_list=[]
    # 导入excel数据
    #data_cutted = pd.read_excel(excel_file, usecols=['content_cutted'])

    # 转化为list列表
    #content = np.array(data_cutted)
    #content_cutted_list = content.tolist()

    # 对content_cutted_list进行改造
    for word in content_cutted_list:
        print(word)
        str = "".join(word)
        corpus.append(str)
    print(corpus)

    
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        str=''
        # 利用数组存储筛选后的单词
        # 进行data_topic.excel内content_cutted列内容的修改
        for j in range(len(word)):
            if float(weight[i][j])>threshold:
                print(word[j], weight[i][j])
                str=str+' '+word[j]
                str=str.strip()
        print(str)
        update_list.append(str)
    print(update_list)


    print('计算完成')

    # 将list转化为pd Series对象
    update_data = pd.Series(data=update_list)  # Series本身有一个参数
    print(type(update_data))
    return update_data
    # 进行excel内容的更新
    #update_excel(excel_file,'Sheet1',update_list,'content_cutted')

# 相当于BTM的实现创建单词之间的联系，扩充单词列表
def data_gram(bigram,trigram,train_st_text):  #train_st_text处理后的单词列表
    if bigram and trigram:
        #logger.warning("bigram 与 trigram 同时为 True，按 trigram 处理")
        bigram = False

    if bigram:
        bigram = gensim.models.Phrases(train_st_text, min_count=5, threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        data_words_bigrams = [bigram_mod[doc] for doc in train_st_text]
        #logger.info("bigram 处理完成，示例为：{}".format(data_words_bigrams[0]))
        return data_words_bigrams

    if trigram:
        bigram = gensim.models.Phrases(train_st_text, min_count=5, threshold=100)
        trigram = gensim.models.Phrases(bigram[train_st_text], threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        data_words_trigrams = [trigram_mod[bigram_mod[doc]] for doc in train_st_text]
        #logger.info("trigram 处理完成，示例为：{}".format(data_words_trigrams[0]))
        return data_words_trigrams
