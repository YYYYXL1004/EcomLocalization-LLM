# 显示python的默认安装路径
import sys
print(sys.executable)

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import style #自定义图表风格
style.use('ggplot')
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
plt.rcParams['font.sans-serif'] = ['Simhei'] # 解决中文乱码问题



import re
import jieba.posseg as psg
import itertools

from gensim import corpora,models #主题挖掘，提取关键信息
from collections import Counter

from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import graphviz

# 导入数据
raw_data=pd.read_excel(r'./data/洗发水数据.xlsx')
raw_data.head()

raw_data.info()

raw_data.columns
#读取一列值存入数组中
# 只保留内容和该句评论的原始极性

y = raw_data[['content']]#读取某一列

# 清洗之后，将数字、字母、京东美的电热水器字样都删除
info = re.compile('[0-9a-zA-Z]|京东|美的|万和|海尔|电热水器|热水器|\&|\“|\”|\[|\]|\'')
#content = y.apply(lambda x: info.sub('', x))  # 替换所有匹配项

array=np.array(y)
y=array.tolist()
print(type(y))
print(y)

s=[]
# 对每一条文本进行字母数字的去除
for item in y:
    print(item)
    s1=re.sub(info,'',str(item))
    print(s1)
    s.append(s1)

print(s)

# 进行平路语句的子句分割
# 传入句子列表content，每一行代表一条评论
def cut_sentences(content):
    # 结束符号，包含中文和英文的
    end_flag = ['?', '!', '.', '？', '！', '。', '…', '\n']

    content_len = len(content)

    tmp_char = ''
    for idx, char in enumerate(content):
        # 拼接字符
        tmp_char += char
        # 判断是否已经到了最后一位
        if (idx + 1) == content_len:
            sentences.append(tmp_char)
            break

        # 判断此字符是否为结束符号
        if char in end_flag:
            # 再判断下一个字符是否为结束符号，如果不是结束符号，则切分句子
            next_idx = idx + 1
            if next_idx > content_len:
                break

            if not content[next_idx] in end_flag:
                sentences.append(tmp_char)
                tmp_char = ''
    return tmp_char
# 子句的保存数组
sentences = []
for c in s:
    s_all = "".join(c)
    cut_sen=cut_sentences(s_all)
    sentences.append(cut_sen)

filtered_strings = [s for s in sentences if len(s) >= 7]
print(filtered_strings)

# 将分割子句从新存入csv文件中

# 长度必须保持一致，否则报错
a = [x for x in filtered_strings]

# 字典中的key值即为csv中列名
dataframe = pd.DataFrame({'分割子句': a})

# 将DataFrame存储为csv
dataframe.to_csv("E:/python_code/LDA/data/分割子句.csv", index=False)

# 读取文件并展示
sub_sentences = pd.read_csv('E:/python_code/LDA/data/分割子句.csv')
print(sub_sentences)

# 删除系统自动为客户做出的评论
raw_data=pd.read_csv('E:/python_code/LDA/data/分割子句.csv')
reviews=raw_data.copy()
print('去重之前：',reviews.shape[0])
reviews=reviews.drop_duplicates()
print('去重之后：',reviews.shape[0])
print(reviews)

# 数据清洗
# 清洗之前
content=reviews['分割子句']
#for i in range(0,20):
    #print(content[i])
    #print('-----------')

# 将进行清洗之后的数据保存在Excel文件中
# 将分割子句从新存入csv文件中

# 长度必须保持一致，否则报错
subStr = [x for x in content]

# 字典中的key值即为csv中列名
dataframe = pd.DataFrame({'content': subStr})

# 将DataFrame存储为Excel文件中

dataframe.to_csv("E:/python_code/LDA/data/美的清洗后子句.csv")
dataframe.to_excel("E:/python_code/LDA/data/美的清洗后子句.xlsx")

# 将评论文本数据小于7的文本数据进行删除




# 读取文件并展示
sub_clear_sentences = pd.read_excel('E:/python_code/LDA/data/美的清洗后子句.xlsx')
print(sub_clear_sentences)




