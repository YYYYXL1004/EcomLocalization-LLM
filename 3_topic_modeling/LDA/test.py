from time import sleep

import jieba
from tqdm import tqdm
import os
import openpyxl
import pandas as pd
import jieba
import jieba.posseg as psg
import re

import Delete_NotHotWorde
import xlrd
import xlwt
import numpy as np
from xlutils.copy import copy
# In[4]:
import TF_IDF
from Delete_NotHotWorde import delete
from XlsxToXls import file_read, write_txt


# 自定义词典
dic_file = "E:/python_code/LDA/data/自定义词典.txt"

# 加载哈工大停用词表
stop_file = "E:/python_code/LDA/data/stop_words.txt"


# In[35]:


def chinese_word_cut(mytext):
    jieba.initialize()
    jieba.load_userdict(dic_file)
    try:
        stopword_list = open(stop_file, encoding='utf-8')
    except:
        stopword_list = []
        # print("error in stop_file")
    stop_list = []
    flag_list = ['n', 'nz', 'vn']  # ['n','nz','vn'] ['n','l','x','vn','an','nx','nz']
    for line in stopword_list:
        line = re.sub(u'\n|\\r', '', line)
        stop_list.append(line)

    word_list = []
    # jieba分词
    seg_list = psg.cut(mytext)
    for seg_word in seg_list:
        word = re.sub(u'[^\u4e00-\u9fa5]', '', seg_word.word)
        # word = seg_word.word  #如果想要分析英语文本，注释这行代码，启动下行代码
        find = 0
        for stop_word in stop_list:
            if stop_word == word or len(word) < 2:  # this word is stopword
                find = 1
                break
        if find == 0: # and seg_word.flag in flag_list
            word_list.append(word)

    bitrem=[]
    # 创建前后单词的联系
    for index, item in enumerate(word_list):
        l=len(word_list)
        if index<l-1:
            s=item+'_'+word_list[index+1]
            bitrem.append(s)
    word_list=word_list+bitrem
    return (" ").join(word_list)


#for i in tqdm(range(100)):
    #sleep(0.02)
    #print(i)
if __name__ == '__main__':
    word_list=chinese_word_cut('东西收到这么久，都忘了去好评，大品牌，值得信赖，东西整体来看，个人感觉还不错，没有出现什么问题，值得拥有！')
    print(word_list)
    list=TF_IDF.data_gram(False, True, '东西收到这么久，都忘了去好评，大品牌，值得信赖，东西整体来看，个人感觉还不错，没有出现什么问题，值得拥有！')
    print(list)