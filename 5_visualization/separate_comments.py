import pandas as pd

# 加载数据集
df = pd.read_csv('jd_comments.csv')

# 将评论列转换为字符串类型
comments = df['评论'].astype(str)

# 使用三重反引号分隔评论
comments_with_quotes = '```\n' + '\n```\n'.join(comments) + '\n```'

# 将结果保存为文本文件
file_path = 'data/jd_comments_separated.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(comments_with_quotes)