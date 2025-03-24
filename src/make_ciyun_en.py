import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string


def preprocess_text(text):
    # 转换为小写
    text = text.lower()
    # 去除标点符号
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    # 去除停用词
    words = text.split()
    filtered_words = [word for word in words if word not in ENGLISH_STOP_WORDS]
    # 重新组合成文本
    processed_text = ' '.join(filtered_words)
    return processed_text


def generate_wordcloud(file_path):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)

        # 检查数据框列数
        if df.shape[1] < 3:
            print(f"数据框列数不足，只有 {df.shape[1]} 列，无法访问第三列。")
            return

        # 打印数据框基本信息和前几行
        print("数据框基本信息：")
        df.info()
        print("数据框前几行：")
        print(df.head().to_csv(sep='\t', na_rep='nan'))

        # 提取第三列数据
        third_column = df.iloc[:, 2]
        all_text = ' '.join([preprocess_text(str(row)) for row in third_column])

        # 生成词云
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

        # 显示词云图
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        plt.savefig('../JD/data/ciyun/shopee_cheongsam.png')
    except FileNotFoundError:
        print("未找到指定的文件，请检查文件路径。")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    file_path = '../JD/data/comments/shopee_Modern Style Cheongsam_sum.xlsx'  # 请替换为实际的 Excel 文件路径
    generate_wordcloud(file_path)
