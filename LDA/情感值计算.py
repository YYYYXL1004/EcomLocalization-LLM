from collections import defaultdict
import os
import re
import jieba
import codecs

# 生成stopword表，需要去除一些否定词和程度词汇
import numpy as np

import NewExcel

stopwords = set()
fr = open('data/stop_words.txt', 'r', encoding='utf-8')
for word in fr:
    stopwords.add(word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
# 读取否定词文件
not_word_file = open('./data/否定词.txt', 'r+', encoding='utf-8')
not_word_list = not_word_file.readlines()
not_word_list = [w.strip() for w in not_word_list]
# 读取程度副词文件
degree_file = open('./data/程度副词.txt', 'r+',encoding='utf-8')
degree_list = degree_file.readlines()
degree_list = [item.split(',')[0] for item in degree_list]
# 生成新的停用词表
with open('stopwords.txt', 'w', encoding='utf-8') as f:
    for word in stopwords:
        if (word not in not_word_list) and (word not in degree_list):
            f.write(word + '\n')


# jieba分词后去除停用词
def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    stopwords = set()

    # 加载停用词表
    with open('./data/stop_words.txt', 'r',encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    return list(filter(lambda x: x not in stopwords, seg_result))


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):



    # 读取情感词典文件
    sen_file = open(r"E:\python_code\LDA\data\BosonNLP_sentiment_score.txt", 'r+', encoding='utf-8')
    # 获取词典文件内容
    sen_list = sen_file.readlines()
    # 创建情感字典
    sen_dict = defaultdict()
    # 读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
    for i in sen_list:
        if len(i.split(' ')) == 2:
            sen_dict[i.split(' ')[0]] = i.split(' ')[1]

    '''
    # 使用知网情感词典进行情感值计算
    # 读取负面情感词典文件
    neg_file = open('./data/知网负面情感词典.txt', 'r+', encoding='utf-8')

    # 读取正面情感词典文件
    pos_file = open('./data/知网正面情感词典.txt', 'r+', encoding='utf-8')

    # 获取负面词典文件内容
    neg_list = neg_file.readlines()

    # 获取正面词典文件内容
    pos_list = pos_file.readlines()

    # 创建记录情感词的字典
    sen_dict = defaultdict()

    # 为正面情感词赋值为 1，负面情感词赋值为 -1
    for item in neg_list:
        sen_dict[item] = -1

    for item in pos_list:
        sen_dict[item] = 1
    '''
    #print(sen_dict)
    # 读取否定词文件
    not_word_file = open('./data/否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    # 读取程度副词文件
    degree_file = open('./data/程度副词.txt', 'r+',encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_dict = defaultdict()
    for i in degree_list:
        degree_dict[i.split(',')[0]] = i.split(',')[1]

    sen_word = dict()
    not_word = dict()
    degree_word = dict()
    # 分类
    for i in range(len(word_list)):
        word = word_list[i]
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_dict.keys():
            # 找出分词结果中在情感字典中的词
            sen_word[i] = sen_dict[word]
        elif word in not_word_list and word not in degree_dict.keys():
            # 分词结果中在否定词列表中的词
            not_word[i] = -1
        elif word in degree_dict.keys():
            # 分词结果中在程度副词中的词
            degree_word[i] = degree_dict[word]

    # 关闭打开的文件
    sen_file.close()
    not_word_file.close()
    degree_file.close()
    # 返回分类结果
    return sen_word, not_word, degree_word


# 计算情感词的分数
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    # 权重初始化为1
    W = 1
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    # 遍历分词结果
    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            # 权重*情感词得分
            score =score+(W * float(sen_word[i]))
            # 情感词下标加一，获取下一个情感词的位置
            sentiment_index += 1
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，权重取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        W *= float(degree_word[j])
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


# 计算得分
def sentiment_score(sentence):
    # 1.对文档分词
    seg_list = seg_word(sentence)
    # 2.将分词结果转换成字典，找出情感词、否定词和程度副词
    sen_word, not_word, degree_word = classify_words(seg_list)
    # 3.计算得分
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score



# 从excel文件中读取评论
import pandas as pd
text=pd.read_excel('./excel/0.85_comment_kind.xlsx',usecols=['content'])
label=pd.read_excel('./excel/0.85_comment_kind.xlsx',usecols=['label'])
kind=pd.read_excel('./excel/0.85_comment_kind.xlsx',usecols=['kind'])


# 将DataFrame类型转化为list类型
array=np.array(text)
text_list=array.tolist()
label_array=np.array(label)
label_list=label_array.tolist()
kind_array=np.array(kind)
kind_int=kind_array.tolist()

kind_list=[]
for item in kind_int:
    kind_list.append(str(item))

#print(text_list)
#print(type(text_list))

sentences=[]
emotion=[]
label_str=[]

for item in label_list:
    s1 = str(item)
    s2 = s1.replace('[', '')
    s3 = s2.replace(']', '')
    label_str.append(s3)

for str in text_list:
    # 每一条评论计算情感值
    print(''.join(str), sentiment_score(''.join(str)))

    # 将句和计算情感值保存在数组中
    sentences.append(''.join(str))
    emotion.append(sentiment_score(''.join(str)))
    # print(sentences)
    #　print(emotion)


# coding=UTF-8
import xlrd
import xlwt
import numpy as np
from xlutils.copy import copy

# 创建表格
excel1 = '评论情感值_总文本.xlsx' # 表名


# 想写入哪个表格后面就跟哪个表格
excel_name = 'excel/' + excel1 # 记得新建一个文件夹“excel”（在项目下面）

# sheet名称
sheet_name = '测试数据'

# 表头
t = ['content', 'emotion','label','kind']


# 新建表格
NewExcel.excel_int(excel_name, sheet_name)

# 写入表头
NewExcel.excel_write_title(excel_name, t)

# 写入三列数据
NewExcel.excel_write_array_str(excel_name, sentences, 0)
NewExcel.excel_write_array(excel_name, emotion, 1)
NewExcel.excel_write_array_str(excel_name, label_str, 2)
NewExcel.excel_write_array_str(excel_name, kind_list, 3)









'''
# 进行评论分句情感值的计算
with open('./data/copus.txt', 'r', encoding='utf-8') as fr:
    text_line = fr.readlines()

print(type(text_line))

# 计算每一条分句评论情感值
for line in text_list:
    print(line, sentiment_score(line))

'''

