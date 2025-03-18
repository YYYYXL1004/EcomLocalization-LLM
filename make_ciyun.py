import pandas as pd
import jieba
from PIL import Image
import numpy as np
import wordcloud
from pathlib import Path

def generate_wordcloud(
        csv_path: str,
        output_path: str,
        mask_path: str,
        text_column: str = '评论',
        font_path: str = 'STKAITI.TTF',
        stopwords: set = None,
        width: int = 1000,
        height: int = 800,
        background_color: str = 'white'
) -> wordcloud.WordCloud:
    """
    生成词云图的封装函数

    参数:
    csv_path (str): 评论数据CSV文件路径
    output_path (str): 词云图输出路径
    mask_path (str): 形状模板图片路径
    text_column (str): 文本列名称（默认'评论'）
    font_path (str): 字体文件路径（默认'STKAITI.TTF'）
    stopwords (set): 停用词集合
    width (int): 图片宽度（默认1000）
    height (int): 图片高度（默认800）
    background_color (str): 背景颜色（默认'white'）

    返回:
    WordCloud: 生成的词云对象或None（如果发生错误）
    """
    try:
        # 确保输出目录存在
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # 读取数据
        df = pd.read_csv(csv_path, encoding='utf-8')
        content = '\n'.join(str(comment) for comment in df[text_column])

        # 默认停用词集合
        default_stopwords = {
            '的', '非常', '很', '了', '和', '是', '有', '在', '这',
            '有点', '也', '都', '就', '不', '还', '我', '你', '他',
            '她', '而且', '它', '不错', '感觉', '好', '喜欢', '不错', '买', '用'
        }

        # 合并默认停用词和用户提供的停用词
        final_stopwords = default_stopwords.union(stopwords) if stopwords else default_stopwords

        # 分词处理，过滤停用词
        text = ' '.join(word for word in jieba.cut(content) if word not in final_stopwords)

        # 加载形状模板
        shape_mask = np.array(Image.open(mask_path))

        # 生成词云
        wc = wordcloud.WordCloud(
            font_path=font_path,
            width=width,
            height=height,
            background_color=background_color,
            mask=shape_mask,
            stopwords=final_stopwords
        )
        wc.generate(text)
        wc.to_file(output_path)
        print(f"词云图已生成到：{output_path}")
        return wc

    except Exception as e:
        print(f"生成词云时出现错误：{str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    # 生成词云
    generate_wordcloud(
        csv_path=r'D:/PycharmProjects/PaChong/JD/data/comments/jd_cheongsam.csv',
        output_path=r'D:/PycharmProjects/PaChong/JD/data/ciyun/jd_cheongsam.png',
        mask_path=r'D:/PycharmProjects/PaChong/JD/work/cloud.png',
        stopwords={'然后', '这个', '但是', '款'}  # 可以添加自定义停用词
    )




# import pandas as pd
# import jieba
# from PIL import Image
# import numpy as np
# import wordcloud
# from pathlib import Path
#
#
# def generate_wordcloud(
#         csv_path: str,
#         output_path: str,
#         mask_path: str,
#         text_column: str = '评论',
#         font_path: str = 'STKAITI.TTF',
#         stopwords: set = None,
#         width: int = 1000,
#         height: int = 800,
#         background_color: str = 'white'
# ):
#     """
#     生成词云图的封装函数
#
#     参数：
#     csv_path: 评论数据CSV文件路径
#     output_path: 词云图输出路径
#     mask_path: 形状模板图片路径
#     text_column: 文本列名称（默认'评论'）
#     font_path: 字体文件路径（默认'STKAITI.TTF'）
#     stopwords: 停用词集合
#     width: 图片宽度（默认1000）
#     height: 图片高度（默认800）
#     background_color: 背景颜色（默认'white'）
#     """
#     try:
#         # 确保输出目录存在
#         Path(output_path).parent.mkdir(parents=True, exist_ok=True)
#
#         # 读取数据
#         df = pd.read_csv(csv_path, encoding='utf-8')
#         content = '\n'.join(str(i) for i in df[text_column])
#
#         default_stopwords = {'的', '非常', '很', '了', '和', '是', '有', '在', '这',
#          '有点', '也', '都', '就', '不', '还', '我', '你', '他',
#          '她', '而且', '它', '不错', '感觉', '好', '喜欢', '不错', '买', '用'}
#
#         # default_stopwords = {
#         #
#         #     # 基础虚词
#         #     '的', '地', '得', '了', '着', '过', '啊', '哦', '呢', '吧', '吗', '啦',
#         #     '很', '非常', '特别', '极其', '较', '挺', '真', '太', '更', '最', '超', '用', '不', '说', '买'
#         #
#         #     # 代词
#         #     '我', '你', '他', '她', '它', '我们', '你们', '他们', '自己', '这', '那',
#         #     '这个', '那个', '这些', '那些', '这里', '那里', '这么', '那么',
#         #
#         #     # 连词介词
#         #     '和', '与', '或', '而且', '但是', '虽然', '还是', '就', '也', '都', '又',
#         #     '再', '还', '在', '对', '给', '跟', '让', '被', '把', '从', '向',
#         #
#         #     # 判断词
#         #     '是', '有', '没有', '无', '没', '非', '是否',
#         #
#         #     # 常见评价虚词
#         #     '感觉', '觉得', '认为', '可能', '应该', '好像', '实在', '确实', '真的',
#         #     # '有点', '有些', '稍微', '比较', '相当', '非常', '特别', '一般', '不太',
#         #
#         #     # # 电商场景常见无效词
#         #     # '商品', '产品', '东西', '卖家', '店家', '客服', '物流', '快递', '包装',
#         #     # '价格', '质量', '服务', '购物', '体验', '使用', '收到', '购买', '下单',
#         #
#         #     # 情感词（需根据分析目标决定是否保留）
#         #     '好', '喜欢', '不错', '满意', '赞', '推荐', '差', '不好', '失望'
#         # }
#
#         # # 加载停用词
#         # default_stopwords = {'的', '非常', '很', '了', '和', '是', '有', '在', '这',
#         #                      '有点', '也', '都', '就', '不', '还', '我', '你', '他',
#         #                      '她', '而且', '它', '不错', '感觉', '好', '喜欢', '不错'}
#         final_stopwords = default_stopwords.union(stopwords) if stopwords else default_stopwords
#
#         # 分词处理
#         text = ' '.join(word for word in jieba.cut(content) if word not in final_stopwords)
#
#         # 加载形状模板
#         shape_mask = np.array(Image.open(mask_path))
#
#         # 生成词云
#         wc = wordcloud.WordCloud(
#             font_path=font_path,
#             width=width,
#             height=height,
#             background_color=background_color,
#             mask=shape_mask,
#             stopwords=final_stopwords
#         )
#         wc.generate(text)
#         wc.to_file(output_path)
#         print(f"词云图已生成到：{output_path}")
#         return wc
#
#     except Exception as e:
#         print(f"生成词云时出现错误：{str(e)}")
#         return None
#
#
# # 使用示例
# if __name__ == "__main__":
#     # 生成第一个词云
#     generate_wordcloud(
#         csv_path=r'D:\PycharmProjects\PaChong\JD\data\comments\jd_cheongsam.csv',
#         output_path=r'D:\PycharmProjects\PaChong\JD\work\cloud.png',
#         mask_path='work/cloud.png',
#         stopwords={'然后', '这个', '但是'}  # 可以添加自定义停用词
#     )
#
#     # # 生成第二个词云
#     # generate_wordcloud(
#     #     csv_path='jd_comments2.csv',
#     #     output_path='data/JD沐浴露评论词云图2.png',
#     #     mask_path='work/舒肤佳2.png',
#     #     background_color='#F0F8FF'  # 修改背景颜色
#     # )
#     #
#     # generate_wordcloud(
#     #     csv_path='jd_comments3.csv',
#     #     output_path='data/JD沐浴露评论词云图3.png',
#     #     mask_path='work/舒肤佳2.png',
#     #     stopwords={'然后', '这个', '但是'}  # 可以添加自定义停用词
#     # )
#
#
#
# # import pandas as pd
# # import jieba
# # from PIL import Image
# # import numpy as np
# #
# # df = pd.read_csv('jd_comments1.csv', encoding='gbk')
# # content = '\n'.join(i for i in df['评论'])
# # # 分词
# # text = ' '.join(jieba.cut(content))
# #
# # # shape_mask = np.array(Image.open("work/舒肤佳.png"))
# # # 词云图配置
# # import wordcloud
# #
# # # wc = wordcloud.WordCloud(
# # #     font_path='STKAITI.TTF',
# # #     width=1000,
# # #     height=800,
# # #     background_color='white',
# # #     mask=shape_mask,
# # #     stopwords=set(['的', '非常','很','了', '和', '是', '有', '在', '这', '有点', '也', '都', '就', '不', '还', '我', '你', '他', '她','而且','它','不错','感觉'])
# # # )
# # # wc.generate(text)
# # # wc.to_file('data/JD沐浴露评论词云图.png')
# #
# # shape_mask = np.array(Image.open("work/舒肤佳2.png"))
# # wc2 = wordcloud.WordCloud(
# #     font_path='STKAITI.TTF',
# #     width=1000,
# #     height=800,
# #     background_color='white',
# #     mask=shape_mask,
# #     stopwords=set(['的', '非常','很','了', '和', '是', '有', '在', '这', '有点', '也', '都', '就', '不', '还', '我', '你', '他', '她','而且','它','不错','感觉'])
# # )
# # wc2.generate(text)
# # wc2.to_file('data/JD沐浴露评论词云图1.png')