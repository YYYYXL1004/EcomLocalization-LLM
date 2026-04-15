import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import style #自定义图表风格
from IPython.core.interactiveshell import InteractiveShell
import re
import NewExcel

InteractiveShell.ast_node_interactivity = "all"
plt.rcParams['font.sans-serif'] = ['Simhei'] # 解决中文乱码问题

# 导入数据
raw_data=pd.read_excel('E:/python_code/LDA/data/美的清洗后子句.xlsx')
raw_data.head()
raw_data.info()
raw_data.columns

# 去除每一条评论前后的 [' ']
info = re.compile('\[|\]|\'')

# 读取第一种商品预处理后的文件content列
y = raw_data[['content']]#读取某一列
array=np.array(y)
y=array.tolist()

str=[]
label=[]


# 对每一条文本进行去除
for item in y:
    s1=re.sub(info,'',''.join(item))
    str.append(s1)
    label.append(''.join('0'))
    print(s1)

# 读取第二种商品评论处理后content列，并标记为1
raw_data=pd.read_excel('E:/python_code/LDA/data/海尔清洗后子句.xlsx')

x = raw_data[['content']]#读取某一列
array=np.array(x)
x=array.tolist()

# 对每一条文本进行去除
for item in x:
    s1=re.sub(info,'',''.join(item))
    str.append(s1)
    label.append(''.join('1'))
    print(s1)

print(str)
print(label)


# 创建新表保存标记文件
excel1 = '商品评论总和.xlsx' # 表名
# 想写入哪个表格后面就跟哪个表格
excel_name = 'excel/' + excel1 # 记得新建一个文件夹“excel”（在项目下面）

# sheet名称
sheet_name = '测试数据'

# 表头
t = ['content', 'label']

# 新建表格
NewExcel.excel_int(excel_name, sheet_name)

# 写入表头
NewExcel.excel_write_title(excel_name, t)

# 写入两列数据
NewExcel.excel_write_array_str(excel_name, str, 0)
NewExcel.excel_write_array_str(excel_name, label, 1)



