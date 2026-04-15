import pandas  as pd
import os
import jieba
import json
import re
from collections import Counter
# 使用正则表达式匹配表情符号
def clean_emoji(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # 表情符号
        u"\U0001F300-\U0001F5FF"  # 符号和象形文字
        u"\U0001F680-\U0001F6FF"  # 运输和地图符号
        u"\U0001F700-\U0001F77F"  # 神秘符号
        u"\U0001F780-\U0001F7FF"  # 装饰符号
        u"\U0001F800-\U0001F8FF"  # 补充符号
        u"\U0001F900-\U0001F9FF"  # 手势与脸
        u"\U0001FA00-\U0001FA6F"  # 补充符号
        u"\U0001FA70-\U0001FAFF"  # 补充符号
        u"\u2600-\u26FF"          # 各种符号
        u"\u2700-\u27BF"          # Dingbats
        "]+", 
        flags=re.UNICODE
    )
    cleaned_text = emoji_pattern.sub(r'', text)
    return cleaned_text

def combine(num_per_label=250):
    # 合并数据集
    product_id_dict = {
        # 生活用品
        '100012545121':'牙膏',
        '100003140591':'牙刷',
        '100013012300':'拖鞋',
        '100080139592':'毛巾',
        '100050648373':'杯子',
        '100052638972':'枕头',
        '2768769':'垃圾袋',
        '100055962974':'垃圾桶',
        '100061099496':'鞋架',
        '100018236566':'衣架',
        '3521615':'避孕套',
        '2828950':'纸巾',
        # 食物
        '100012930118':'面包',
        '100016141377':'香肠',
        '100045759613':'鸡蛋',
        '100056753776':'坚果',
        '100034306223':'茶叶',
        '5327144':'果汁',
        '100029838442':'鸡肉',
        '100011349127':'猫粮',
        '100014769863':'红酒',
        '10087882236816':'啤酒',
        '100058137517':'咖啡',
        '100021684312':'蚕豆',
        '1205781':'麦片',
        # 服饰
        '100046165248':'短袖',
        '100051926081':'长袖',
        '100086539069':'短裤',
        '100100029082':'长裤',
        '100010445178':'帽子',
        '100044614005':'鞋子',
        '100064573419':'手套',
        '100021809493':'背包',
        '7802298':'皮带',
        '100012208534':'行李箱',
        '100066186011':'帽衫',
        '10069772807376':'皮衣',
        '10086559609886':'羽绒服',
        # 电子器件
        '100088789712':'主板',
        '100011575915':'电源',
        '100060502735':'显卡',
        '100021043464':'显示器',
        '100086246340':'笔记本电脑',
        '100024102298':'充电宝',
        '100040185503':'cpu',
        '100074912125':'相机',
        '100036659879':'固态硬盘',
        '100092807821':'内存条',
        '100012720890':'鼠标',
        '5028795':'键盘',
    }

    all_csv = []
    comment_id = 0
    for k ,v in product_id_dict.items():
        items = json.load(open(f'data/product_json/{k}.json'))[:num_per_label]
        for item in items:
            item['label'] = v
            item['comment_id'] = comment_id
            comment_id +=1
        all_csv.extend(items)
    all_csv = pd.DataFrame(all_csv)
    print(f'all_csv : {all_csv.shape}')
    all_csv.to_csv('data/all.csv',index=False)

def clear_text():
    with open('data/cn_stopwords.txt','r') as file:
        stopwords = [line.strip() for line in file.readlines()]

    # 读取数据集
    df = pd.read_csv('data/all.csv')
    lines = df['comment'].values.tolist()
    comment_ids = df['comment_id'].values.tolist()
    # 开始分词
    sentences = []
    for comment_id , line in zip(comment_ids,lines):
        try:
            segs = jieba.lcut(line)
            segs = [v for v in segs if not str(v).isdigit()]  # 去数字
            segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
            segs = list(filter(lambda x: x not in stopwords, segs))  # 去掉停用词
            sent = ' '.join(segs)
            sent = clean_emoji(sent)            
            sentences.append(f'{int(comment_id)},{sent}')
        except Exception as error:
            print(f'{error} ',line)
            continue
    with open('data/clean_sentence.txt','w') as file:
        file.write('\n'.join(sentences))

def clean_top_word():
    # 统计高频字
    with open('data/clean_sentence.txt','r') as file:
        lines = [line.strip() for line in file.readlines()]
    word_counts = Counter()
    comment_ids = []
    for line in lines:
        items = line.split(',')
        comment_id = items[0]
        words = items[1]
        words = words.split(' ')
        word_counts.update(words)
    # 提取前50个高频词及其数量
    top_words = word_counts.most_common(50)
    words, counts = zip(*top_words)
    top_words = words[:20] # 剔除前20个高频词
    new_documents = []
    for line in lines:
        item = line.split(',')
        comment_id = item[0]
        words = item[1]
        words = words.split(' ')
        words = [word for word in words if word not in top_words]
        if len(words) == 0 :
            print(line)
            continue
        sent = ' '.join(words)

        new_documents.append(f'{comment_id},{sent}')
    with open('data/clean_sentence_v2.txt','w') as file:
        file.write('\n'.join(new_documents))
    
if __name__ == '__main__':
    # 把scrapy.py得到的商品json评论汇总成一个csv文件
    # combine()
    # 对上面得到的csv文件进行文本清洗
    # clear_text()
    # 去除一些高频词汇
    clean_top_word()
    