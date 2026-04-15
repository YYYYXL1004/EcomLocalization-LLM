import os

# 评论预处理
os.system("python ./评论预处理.py")

# 评论情感值计算
os.system("python ./情感值计算.py")

# 困惑度图像
os.system("python ./mainhanshu.py")

# 一致性图像
os.system("python ./LDA_Coherence.py")

# os.system("python ./LDAsklearn_origin.py")