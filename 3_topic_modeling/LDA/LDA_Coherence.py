# -*- coding: utf-8 -*-
import re
import numpy as np
import warnings
import jieba
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

from Occur_Of_Words import chinese_word_cut

warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
PATH = r'E:\python_code\LDA\excel\评论情感值_总文本.xlsx'

# 停用词
stop_words_path = "E:/python_code/LDA/data/stop_words.txt"
stop_words = []

# 保留词文本路径
# 文本格式： 词语 词频（可省略） 词性（可省略）
# 一个词一行
reserved_words_path = "E:/python_code/LDA/data/自定义词典.txt"

with open(stop_words_path, encoding='utf-8') as f:
    for line in f.readlines():
        stop_words.append(line.strip())
f.close()


# 数据清洗, 可以根据自己的需求进行重载
def processing(text):
    text = re.sub("【.+?】", "", text)  # 去除 【xx】 (里面的内容通常都不是用户自己写的)
    text = re.sub("\n", "", text)
    text = re.sub(r'[\W]', "", text)  # 去除标点符号
    text = re.sub(r'[\d]', "", text)  # 去除数字
    return text


# 对句子进行中文分词
def seg_depart(sentence):

    # 加载用户自定义词典
    jieba.load_userdict(reserved_words_path)
    sentence_depart = jieba.cut(sentence.strip())
    out_str = ''  # 输出结果为out_str
    for word in sentence_depart:
        if word in stop_words:
            continue
        out_str += word
        out_str += " "
    return out_str


def get_data_set(path):
    data = pd.read_excel(path,usecols=['content'])
    kind_data = pd.read_excel(path,usecols=['kind'])

    # 根据分类情况 划出分类的coherencet图像

    data_set = []  # 建立存储分词的列表
    array = np.array(data)
    text_list = array.tolist()

    for item in text_list:
        s1=str(item)
        s2=s1.replace("['","")
        s3=s2.replace("']","")
        data_set.append(s3)

    array = np.array(kind_data)
    kind_list = array.tolist()

    # 统计出一共有多少类
    num = []
    for item in  kind_list:
        if item not in num:
            num.append(item)

    # 根据分类情况 划出分类的coherence图像
    for item in num:
        comment_list = []
        for index,number in enumerate(kind_list):
            if number==item:
                comment_list.append(data_set[index])
        print('============='+item[0]+'===================')
        print(comment_list)
        plt_pic(comment_list,item[0])
    return data_set


def get_fen_ci_data(data):

    output = []
    for line in data:
        s=chinese_word_cut(line)
        #line = processing(line)
        #line_seg = seg_depart(line)
        #output.append(line_seg.split())
        output.append(s.split())
    print("分词成功！！！")
    return output


"""
一般我们可以用指标来评估模型好坏，也可以用这些指标来确定最优主题数。
一般用来评价LDA主题模型的指标有困惑度（perplexity）和主题一致性（coherence），
困惑度越低或者一致性越高说明模型越好。一些研究表明perplexity并不是一个好的指标，
所以一般我用coherence来评价模型并选择最优主题
"""

'''
# 计算困惑度
def perplexity(topics_num):
    print("\n#######number of topics is {}#######\n".format(topics_num))
    lda_model = LdaModel(corpus, num_topics=topics_num, id2word=dictionary, passes=10)
    print(lda_model.print_topics(num_topics=topics_num, num_words=15))
    print(lda_model.log_perplexity(corpus))
    return lda_model.log_perplexity(corpus)
'''

# 计算coherence
def coherence(topics_num,corpus,dictionary,fen_ci_data):
    print("\n####### number of topics is {} #######\n".format(topics_num))
    lda_model = LdaModel(corpus, num_topics=topics_num, id2word=dictionary, passes=10, random_state=1)
    print(lda_model.print_topics(num_topics=topics_num, num_words=10))

    # 'c_v'相干性测量是最慢的方法，但可以获得最好的结果。
    # 您可以尝试使用'u_mass'来获得最快的性能。
    # 请注意，您只需要'u_mass'的模型、语料库和一致性参数。
    lda_cm = CoherenceModel(model=lda_model, texts=fen_ci_data, dictionary=dictionary, coherence='u_mass')
    print(lda_cm.get_coherence())
    return lda_cm.get_coherence()


# 打印LDA模型结果
def show_lda_result(fen_ci_data, topics_num, words_num):
    print("\n============== 主题数：{}  每个主题单词数： {} ==============".format(topics_num, words_num))
    dictionary = corpora.Dictionary(fen_ci_data)  # 构建词典
    corpus_ = [dictionary.doc2bow(text) for text in fen_ci_data]  # 表示为第几个单词出现了几次
    lda_model = LdaModel(corpus_, num_topics=topics_num, id2word=dictionary, passes=10, random_state=1)  # 分为10个主题
    out_put = lda_model.print_topics(num_topics=topics_num, num_words=words_num)  # 每个主题输出15个单词
    for i_ in out_put:
        print(i_)
    print("\n\n")


# 构建词典，画图
def plt_pic(input_data,kind_num):
    fen_ci_data = get_fen_ci_data(input_data)
    print("\n============ 分词结果 ==========\n")
    for i in fen_ci_data[:5]:
        print(i)
        print("\n######################\n")

    print("\n============ LDA模型 ==========\n")
    dictionary = corpora.Dictionary(fen_ci_data)  # 构建词典
    corpus = [dictionary.doc2bow(text) for text in fen_ci_data]  # 表示为第几个单词出现了几次
    for i in corpus[:5]:
        print(i)
        print("\n######################\n")

    num_words = 15  # 每个主题输出的单词个数
    num_topics = 5  # 主题数目
    show_lda_result(fen_ci_data, num_topics, num_words)

    num_topics = 13  # 主题数目
    show_lda_result(fen_ci_data, num_topics, num_words)

    #  画图主题数为1到15的图
    x = range(1, 15)
    #z = [perplexity(i) for i in x]  # 如果想用困惑度就选这个
    y = [coherence(i,corpus,dictionary,fen_ci_data) for i in x]
    plt.plot(x, y)
    plt.xlabel('Number of Topic')
    plt.ylabel('Coherence')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.title('主题-分类'+kind_num+' coherence变化情况')
    plt.show()


if __name__ == "__main__":
    print("Hello world!")
    print("当前停用词为： ", stop_words)

    # 获取数据
    input_data = get_data_set(PATH)
    #print("\n============ 读取数据 ==========\n")
    #for i in input_data[:5]:
        #print(i)
        #print("\n######################\n")
    '''
    # 获取分词数据
    fen_ci_data = get_fen_ci_data(input_data)
    print("\n============ 分词结果 ==========\n")
    for i in fen_ci_data[:5]:
        print(i)
        print("\n######################\n")

    print("\n============ LDA模型 ==========\n")
    dictionary = corpora.Dictionary(fen_ci_data)  # 构建词典
    corpus = [dictionary.doc2bow(text) for text in fen_ci_data]  # 表示为第几个单词出现了几次
    for i in corpus[:5]:
        print(i)
        print("\n######################\n")

    num_words = 15  # 每个主题输出的单词个数
    num_topics = 5  # 主题数目
    show_lda_result(fen_ci_data, num_topics, num_words)

    num_topics = 13  # 主题数目
    show_lda_result(fen_ci_data, num_topics, num_words)

    #  画图主题数为1到15的图
    x = range(1, 15)
    #z = [perplexity(i) for i in x]  #如果想用困惑度就选这个
    y = [coherence(i,corpus,dictionary,fen_ci_data) for i in x]
    plt.plot(x, y)
    plt.xlabel('Number of Topic')
    plt.ylabel('Coherence')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.title('主题-coherence变化情况')
    plt.show()'''

