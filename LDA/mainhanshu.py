from gensim import corpora, models
import matplotlib.pyplot as plt
import perplexity
import lda_catch


def graph_draw(topic, perplexity):  # 做主题数与困惑度的折线图
    x = topic
    y = perplexity
    plt.plot(x, y, color="red", linewidth=2)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()


if __name__ == '__main__':
    #for i in range(20, 300, 1):  # 多少文档中抽取一篇（这里只是为了调试最优结果，可以直接设定不循环）
        #print("抽样为" + str(i) + "时的perplexity")
    a = range(1, 20, 1)  # 主题个数
    p = []
    for num_topics in a:

        lda, dictionary = lda_catch.ldamodel(num_topics)
        corpus = corpora.MmCorpus('corpus.mm')
        testset = []
        for c in range(int(corpus.num_docs)):
            print(c)
            testset.append(corpus[c])
        prep = perplexity.perplexity(lda, testset, dictionary, len(dictionary.keys()), num_topics)
        p.append(prep)

    graph_draw(a, p)
