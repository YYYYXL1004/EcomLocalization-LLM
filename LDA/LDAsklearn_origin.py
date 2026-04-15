#!/usr/bin/env python
# coding: utf-8
# # sklearn-LDA
# 代码示例：https://mp.weixin.qq.com/s/hMcJtB3Lss1NBalXRTGZlQ （玉树芝兰） <br>
# 可视化：https://blog.csdn.net/qq_39496504/article/details/107125284  <br>
# sklearn lda参数解读:https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html
# <br>中文版参数解读：https://blog.csdn.net/TiffanyRabbit/article/details/76445909
# <br>LDA原理-视频版：https://www.bilibili.com/video/BV1t54y127U8
# <br>LDA原理-文字版：https://www.jianshu.com/p/5c510694c07e
# <br>score的计算方法：https://github.com/scikit-learn/scikit-learn/blob/844b4be24d20fc42cc13b957374c718956a0db39/sklearn/decomposition/_lda.py#L729
# <br>主题困惑度1：https://blog.csdn.net/weixin_43343486/article/details/109255165
# <br>主题困惑度2：https://blog.csdn.net/weixin_39676021/article/details/112187210
# ## 1.预处理

import os

import matplotlib
import openpyxl
import pandas as pd
import jieba
import jieba.posseg as psg
import re

from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
from matplotlib import pyplot as plt

import Delete_NotHotWorde
import xlrd
import xlwt
import numpy as np
from xlutils.copy import copy
# In[4]:
import TF_IDF
from Delete_NotHotWorde import delete
from LDA_Coherence import get_data_set, get_fen_ci_data, show_lda_result
from Occur_Of_Words import chinese_word_cut
from XlsxToXls import file_read, write_txt
from 画图 import printme

output_path = "E:/python_code/LDA/result"
file_path = 'E:/python_code/LDA/excel'
os.chdir(file_path)
data=pd.read_excel("评论情感值_总文本.xlsx")#content type
print(len(data))

os.chdir(output_path)
PATH = r"E:\python_code\LDA\excel\评论情感值_总文本.xlsx"
# 自定义词典
dic_file = "E:/python_code/LDA/data/自定义词典.txt"

# 加载哈工大停用词表
stop_file = "E:/python_code/LDA/data/stop_words.txt"


# In[35]:

data["content_cutted"] = data.content.apply(chinese_word_cut)
# 调用TF-IDF函数进行关键词过滤

# ## 2.LDA分析

# In[37]:
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# In[38]:
# 打印主题单词
def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword


# In[39]:
n_features = 1000 #提取1000个特征词语
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                # 用于描述单词在文档中的最高出现率，取值范围为 [0.0~1.0]。
                                # 比如 max_df=0.6，表示一个单词在 60%
                                # 的文档中都出现过，那么认为它只携带了非常少的信息，因此就不作为分词统计。
                                max_df = 0.5,
                                min_df = 10)

# 在此进行使用分词后的content_cutted列
# 进行n-gram，使短文本词频字典得到扩充
print(type(data.content_cutted),data.content_cutted)

# 将data.content_cutted Series类转化为list
content_cutted_list=data.content_cutted.tolist()
print(content_cutted_list)

# 可在此之前进行TF-IDF阀值计算，去除高频低区分度的词语
data.content_cutted=TF_IDF.tf_idf_sum(content_cutted_list, 0.1)

print('------------------1---------')
tf = tf_vectorizer.fit_transform(data.content_cutted)
print('------------------2---------')

# In[40]:
# 修改模型主题数
n_topics = 5
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,   # n_components文章生成n_topics维向量  EM算法的最大迭代次数
                                learning_method='batch',
                                learning_offset=50,

                                # α =50/K，β =0.1
                                # 主题分布θi由超参数为α
                                # 词语分布超参数为B
                                doc_topic_prior=(0.1),
                                topic_word_prior=(50/n_topics),
                               random_state=0)
lda.fit(tf)


print('=================生成Coherence一致性图像')
# 获取数据
input_data = get_data_set(PATH)

# 获取分词数据
fen_ci_data = get_fen_ci_data(input_data)
print(fen_ci_data)
print("\n============ 分词结果 ==========\n")
for i in fen_ci_data[:5]:
    print(i)
    print("\n######################\n")



# 计算coherence
def coherence(topics_num,corpus):
    print("\n####### number of topics is {} #######\n".format(topics_num))
    lda_model = LdaModel(corpus, num_topics=topics_num, id2word=dictionary, passes=10, random_state=1)
    print(lda_model.print_topics(num_topics=topics_num, num_words=10))

    # 'c_v'相干性测量是最慢的方法，但可以获得最好的结果。
    # 您可以尝试使用'u_mass'来获得最快的性能。
    # 请注意，您只需要'u_mass'的模型、语料库和一致性参数。
    lda_cm = CoherenceModel(model=lda_model, texts=fen_ci_data, dictionary=dictionary, coherence='u_mass')
    print(lda_cm.get_coherence())
    return lda_cm.get_coherence()

# 计算困惑度
def perplexity(topics_num,corpus):
    print("\n#######number of topics is {}#######\n".format(topics_num))
    lda_model = LdaModel(corpus, num_topics=topics_num, id2word=dictionary, passes=10)
    print(lda_model.print_topics(num_topics=topics_num, num_words=15))
    print(lda_model.log_perplexity(corpus))
    return lda_model.log_perplexity(corpus)





print("\n============ LDA模型 ==========\n")
dictionary = corpora.Dictionary(fen_ci_data)  # 构建词典
corpus = [dictionary.doc2bow(text) for text in fen_ci_data]  # 表示为第几个单词出现了几次  doc2bow将文本转为词袋模型
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
z = [perplexity(i,corpus) for i in x]  #如果想用困惑度就选这个
y = [coherence(i,corpus) for i in x]
plt.plot(x, z)
plt.xlabel('Number of Topic')
plt.ylabel('Perplexity')
plt.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
plt.title('主题-perplexity变化情况')
plt.show()

plt.plot(x, y)
plt.xlabel('Number of Topic')
plt.ylabel('Coherence')
plt.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
plt.title('主题-coherence变化情况')
plt.show()

# ### 2.1输出每个主题对应词语
# In[11]:
n_top_words = 15
tf_feature_names = tf_vectorizer.get_feature_names()
print('===============55555===========')
print(len(tf_feature_names))
print(tf_feature_names)
print(type(tf_feature_names))

topic_word = print_top_words(lda, tf_feature_names, n_top_words)
print('======================')
print(topic_word)
print(type(topic_word))
# 利用词共现算法对每一个主题词进行过滤
# 读取词共现文件，将文件读取成文段和贡献次数两个数组，利用下标对齐
'''
edge_path=r'E:\python_code\LDA\csv\edge.txt'
word_occur,occur_num=file_read(edge_path)

#创建列表对象保存每一个主题的对象
topic_occur_obj=[]

word_list=[]
for item in topic_word:
    # 将每一个item按照空格分割成数组
    word_list=item.split()
    # 创建字典记录每一个topic下的共现词组和次数
    dict_occur_word = {}

    # 根据词共现文件对关键词进行排序
    for index,h_value in enumerate(word_list):
        for i,e_value in enumerate(word_list):
            if i>index:
                # 只有当后边索引大于前边索引是才和edge文件中数组比较
                s_mix1=h_value+','+e_value
                s_mix2=e_value+','+h_value
                # 获取在词共现文件中的下标位置，用于得出次数
                for index,t in enumerate(word_occur):
                    if s_mix1==t or s_mix2==t:
                        dict_occur_word[t]=occur_num[index]
                        break
    topic_occur_obj.append(dict_occur_word)
print(topic_occur_obj)
# 将文件写入到txt文件中
path=r'E:\python_code\LDA\csv\1.txt'
write_txt(path,topic_occur_obj)

'''
printme()






# ### 2.2输出每篇文章对应主题
# In[12]:
import numpy as np

# In[13]:
topics=lda.transform(tf)

# In[28]:
topic = []
for t in topics:
    topic.append("Topic #"+str(list(t).index(np.max(t))))
data['概率最大的主题序号']=topic
data['每个主题对应概率']=list(topics)
data.to_excel("data_topic.xlsx",index=False)

# 对data_topic文件删除关键字为零的行
Delete_NotHotWorde.delete('E:\\python_code\\LDA\\result\\data_topic.xlsx','E:\\python_code\\LDA\\result\\data_topic.xls',False)


# 创建字典记录 计算每一主题下的情感值总和
# 读取文件 获取每条评论文本下topic和emotion列

import pandas as pd
import numpy as np

excel_file = 'E:/python_code/LDA/result/data_topic.xlsx'

# 导入excel数据
data_emo = pd.read_excel(excel_file, usecols=['emotion'])
data_topic = pd.read_excel(excel_file, usecols=['概率最大的主题序号'])
data_label = pd.read_excel(excel_file, usecols=['label'])

# 转化为list列表
array_emo = np.array(data_emo)
emo_list = array_emo.tolist()


array_topic = np.array(data_topic)
topic_list = array_topic.tolist()

array_label = np.array(data_label)
label_list = array_label.tolist()

# 记录主题情感值总和
#dict_count = {}
dict_count_label0 = {}
dict_count_label1 = {}
# 创建字典记录每一个Topic主题的数量
dict_topic_number={}
dict_topic_number_label0={}
dict_topic_number_label1={}

for i in range(0, n_topics):
    #dict_count['Topic #' + str(i)] = 0.0
    dict_count_label0['Topic #' + str(i)] = 0.0
    dict_count_label1['Topic #' + str(i)] = 0.0
    #dict_topic_number['Topic #' + str(i)]=0
    dict_topic_number_label0['Topic #' + str(i)] = 0
    dict_topic_number_label1['Topic #' + str(i)] = 0

for index, item in enumerate(topic_list):
    

    if str(label_list[index])=='[0]':
        if "".join(item) in dict_count_label0:
            s1 = str(emo_list[index])
            s2 = s1.replace('[', '')
            s3 = s2.replace(']', '')
            dict_count_label0["".join(item)] += float(s3)
            dict_topic_number_label0["".join(item)] += 1
    else:
        if "".join(item) in dict_count_label1:
            s1 = str(emo_list[index])
            s2 = s1.replace('[', '')
            s3 = s2.replace(']', '')
            dict_count_label1["".join(item)] += float(s3)
            dict_topic_number_label1["".join(item)] += 1

# 计算所有主题情感值的平均值
emo_sum_label0=0.0
for key in dict_count_label0:
    emo_sum_label0=emo_sum_label0+dict_count_label0[key]
avg_label0=emo_sum_label0/n_topics

emo_sum_label1=0.0
for key in dict_count_label1:
    emo_sum_label1=emo_sum_label1+dict_count_label1[key]
avg_label1=emo_sum_label1/n_topics

print('label0 情感平均值：{}'.format(avg_label0))
print('label1 情感平均值：{}'.format(avg_label1))
print('label0 各个主题的情感强度值：{}'.format(dict_count_label0))
print('label1 各个主题的情感强度值：{}'.format(dict_count_label1))

# 计算不同标签的评论个数
data_label0=0.0
data_label1=0.0

for key in dict_topic_number_label0:
    data_label0=data_label0+dict_topic_number_label0[key]
for key in dict_topic_number_label1:
    data_label1=data_label1+dict_topic_number_label1[key]


print(data_label0)
print(data_label1)
# 每一个topic的占比情况
print('label0 各个主题占比情况')
print(dict_topic_number_label0)
for key in dict_topic_number_label0:
    print("{} 主题的占比：{}".format(key,(dict_topic_number_label0[key]/data_label0)))

print('label1 各个主题占比情况')
print(dict_topic_number_label1)
for key in dict_topic_number_label1:
    print("{} 主题的占比：{}".format(key,(dict_topic_number_label1[key]/data_label1)))

# IPA模型重要度和绩效值计算
# 每个主题的重要度=每个评论中当前主题概率的和
# 落在[0,1]之间，当前主题概率之和/所有主题概率之和
#创建字典存储主题概率之和
# 创建字典记录每一个Topic主题的数量
dict_topic_odd_label0={}
dict_topic_odd_label1={}

for i in range(0, n_topics):
    dict_topic_odd_label0['Topic #' + str(i)]=0.0
    dict_topic_odd_label1['Topic #' + str(i)]=0.0


# 利用data_topic文件计算重要度，取出每条评论的
data_topic_odd = pd.read_excel(excel_file, usecols=['每个主题对应概率'])

# 转化为list列表
array_topic_odd = np.array(data_topic_odd)
topic_odd_list = array_topic_odd.tolist()
#print(topic_odd_list)
#print(type(topic_odd_list))

pattern=re.compile('\ +')

for index,item in enumerate(topic_odd_list):
    #print(item)
    #print(type(item))
    if str(label_list[index])=='[0]':
        for i in item:
            # print(i)
            # print(type(i))
            # 对提取excel中每个主题概率进行字符串处理
            s1 = i.replace('[', '')
            s2 = s1.replace(']', '')
            s3 = s2.strip()
            s4 = re.sub(pattern, ' ', s3)
            str_list = s4.split(' ')

            for index, topic_odd in enumerate(str_list):
                j = float(topic_odd)
                # print(j,type(j),index)
                # print(str(index))
                # 统计每个主题的评论概率之和
                dict_topic_odd_label0['Topic #' + str(index)] += j
    else:
        for i in item:
            # print(i)
            # print(type(i))
            # 对提取excel中每个主题概率进行字符串处理
            s1 = i.replace('[', '')
            s2 = s1.replace(']', '')
            s3 = s2.strip()
            s4 = re.sub(pattern, ' ', s3)
            str_list = s4.split(' ')

            for index, topic_odd in enumerate(str_list):
                j = float(topic_odd)
                # print(j,type(j),index)
                # print(str(index))
                # 统计每个主题的评论概率之和
                dict_topic_odd_label1['Topic #' + str(index)] += j

# 记录各个主体概率之和的字典
print('label0 各评论主题概率之和：')
print(dict_topic_odd_label0)
print('label1 各评论主题概率之和：')
print(dict_topic_odd_label1)

# 进行落在[0,1]之间的处理
dict_topic_odd_label0_normal={}
dict_topic_odd_label1_normal={}

for i in range(0, n_topics):
    dict_topic_odd_label0_normal['Topic #' + str(i)]=0.0
for i in range(0, n_topics):
    dict_topic_odd_label1_normal['Topic #' + str(i)] = 0.0

# 遍历字典进行计算总概率值并计算每一概率在[0,1]之间的占比
odd_label0_sum=0.0
odd_label1_sum=0.0
for key in dict_topic_odd_label0:
    odd_label0_sum+=dict_topic_odd_label0[key]
print('label0 所有主题总概率值：' + str(odd_label0_sum))
for key in dict_topic_odd_label1:
    odd_label1_sum+=dict_topic_odd_label1[key]
print('label1 所有主题总概率值：' + str(odd_label1_sum))

dict_topic_odd_label0_normal_sum=0.0
for key in dict_topic_odd_label0:
    # 记录每一主题概率比值
    dict_topic_odd_label0_normal[key]=dict_topic_odd_label0[key]/odd_label0_sum
    dict_topic_odd_label0_normal_sum+=dict_topic_odd_label0_normal[key]

dict_topic_odd_label1_normal_sum=0.0
for key in dict_topic_odd_label1:
    # 记录每一主题概率比值
    dict_topic_odd_label1_normal[key]=dict_topic_odd_label1[key]/odd_label1_sum
    dict_topic_odd_label1_normal_sum+=dict_topic_odd_label1_normal[key]

dict_topic_odd_label0_normal_avg=dict_topic_odd_label0_normal_sum/n_topics
dict_topic_odd_label1_normal_avg=dict_topic_odd_label1_normal_sum/n_topics

print('label0 各个主题概率归一化结果：',dict_topic_odd_label0_normal)
print('label1 各个主题概率归一化结果：',dict_topic_odd_label1_normal)
print('label0 各个主题概率归一化结果平均值',dict_topic_odd_label0_normal_avg)
print('label0 各个主题概率归一化结果平均值',dict_topic_odd_label1_normal_avg)

# 每个主题绩效值=当前主题下的情感值之和
# 落在[0,1]之间，当前主题情感值之和/所有主题情感值之和

# 创建字典记录归一化的主题情感值
dict_topic_emo_normal_label0={}
dict_topic_emo_normal_label1={}

for i in range(0, n_topics):
    dict_topic_emo_normal_label0['Topic #' + str(i)]=0.0
    dict_topic_emo_normal_label1['Topic #' + str(i)]=0.0

dict_topic_emo_normal_label0_sum=0.0
dict_topic_emo_normal_label1_sum=0.0
for key in dict_count_label0:
    dict_topic_emo_normal_label0[key]=dict_count_label0[key]/emo_sum_label0
    dict_topic_emo_normal_label0_sum+=dict_topic_emo_normal_label0[key]
for key in dict_count_label1:
    dict_topic_emo_normal_label1[key]=dict_count_label1[key]/emo_sum_label1
    dict_topic_emo_normal_label1_sum+=dict_topic_emo_normal_label1[key]

dict_topic_emo_normal_label0_avg=dict_topic_emo_normal_label0_sum/n_topics
dict_topic_emo_normal_label1_avg=dict_topic_emo_normal_label1_sum/n_topics
print('label0 各个主题的情感值归一化结果：',dict_topic_emo_normal_label0)
print('label0 各个主题的情感值归一化结果平均值：',dict_topic_emo_normal_label0_avg)
print('label1 各个主题的情感值归一化结果：',dict_topic_emo_normal_label1)
print('label1 各个主题的情感值归一化结果平均值：',dict_topic_emo_normal_label1_avg)


# 生成Excel表格记录个主题的重要度（主题下概率归一化值）
# 绩效度（主题下情感值归一化值）
# 将处理后的重要度和绩效值的数据封装进数组
'''
topic_odd_normal_list=[]
topic_emo_normal_list=[]

for key in dict_topic_odd_normal:
    topic_odd_normal_list.append(dict_topic_odd_normal[key])
    topic_emo_normal_list.append(dict_topic_emo_normal[key])

print(topic_emo_normal_list)
print(topic_odd_normal_list)
'''

# 创建表格
'''
excel1 = '重要度绩效值.xlsx' # 表名


# 想写入哪个表格后面就跟哪个表格
excel_name = 'C:/Users/34278/Desktop/重要度绩效值.xlsx'  # 记得新建一个文件夹“excel”（在项目下面）

# sheet名称
sheet_name = '测试'

# 表头
t = ['重要度', '绩效值']

# 新建表格
NewExcel.excel_int(excel_name, sheet_name)

# 写入表头
NewExcel.excel_write_title(excel_name, t)

# 写入两列数据
NewExcel.excel_write_array_str(excel_name, topic_odd_normal_list, 0)
NewExcel.excel_write_array(excel_name, topic_emo_normal_list, 1)
'''
