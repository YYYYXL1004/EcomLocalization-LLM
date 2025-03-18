import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

file_path = 'jd_comments.csv'
# 读取数据
df = pd.read_csv(file_path, encoding='utf-8-sig')
x = df['地区'].value_counts().index.tolist()
y = df['地区'].value_counts().tolist()

c = (
    Pie(init_opts=opts.InitOpts(  # 新增初始化配置
        width="1600px",          # 容器宽度
        height="800px",          # 容器高度
        theme="light",           # 主题
        bg_color="white"         # 背景颜色
    ))
    .add(
        series_name="地区分布",
        data_pair=[list(z) for z in zip(x, y)],
        radius=["35%", "70%"],
        center=["50%", "50%"],    # 关键修改：设置饼图中心点
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="京东某沐浴露评论用户地区分布图",
            pos_left="center",    # 标题居中
            pos_top="20"          # 标题距离顶部距离
        ),
        legend_opts=opts.LegendOpts(
            pos_left="center",    # 图例居中
            pos_bottom="1%",      # 图例距离底部距离
            orient="horizontal"   # 图例横向排列
        )
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(formatter="{b}: {c}")
    )
    .render("data/京东某沐浴露评论用户地区分布图.html")
)

