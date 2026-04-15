from gensim import corpora, models
import pandas as pd
import numpy as np



# 返回包含列表数据的列表

def ldamodel(num_topics):
    # cop = open(r'D:\p\lda\data\copus.txt', 'r', encoding='UTF-8')
    # 存储评论数据的地址
    excel_file = 'excel/评论情感值_总文本.xlsx'

    # 导入excel数据
    data = pd.read_excel(excel_file, usecols=['content'])

    array = np.array(data)
    text_list = array.tolist()



    train = []
    for line in text_list:
        print(line)

        line="".join(line)
        line = [word.strip() for word in line.split(' ')]
        train.append(line)  # list of list 格式

    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in
              train]  # corpus里面的存储格式（0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)
    corpora.MmCorpus.serialize('corpus.mm', corpus)
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, random_state=1,
                          num_topics=num_topics)  # random_state 等价于随机种子的random.seed()，使每次产生的主题一致

    topic_list = lda.print_topics(num_topics, 10)
    # print("主题的单词分布为：\n")
    # for topic in topic_list:
    #     print(topic)
    return lda, dictionary

