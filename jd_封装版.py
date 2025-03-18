from DrissionPage import ChromiumPage
import csv
import time
import random
from typing import Optional


class JDCommentScraper:
    def __init__(self, product_id: str, output_file: str, max_pages: int = 100):
        """
        初始化京东商品评论爬虫
        param product_id: 商品ID（如："100007961027"）
        param output_file: 输出文件名（默认：jd_comments.csv）
        param max_pages: 最大爬取页数（默认：100）
        """
        self.product_id = product_id
        self.output_file = output_file
        self.max_pages = max_pages
        self.dp = ChromiumPage()
        self._init_csv()

    def _init_csv(self):
        """初始化CSV文件并写入表头"""
        with open(self.output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['昵称', '地区', '日期', '产品', '评论', '评分'])
            writer.writeheader()

    def _save_comments(self, comments: list):
        """将评论列表保存到CSV文件"""
        with open(self.output_file, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['昵称', '地区', '日期', '产品', '评论', '评分'])
            writer.writerows(comments)
            print(f"已保存{len(comments)}条评论")

    def _parse_comment_data(self, json_data: dict) -> Optional[list]:
        """解析接口返回的JSON数据"""
        try:
            comments = json_data.get('comments', [])
            parsed = []
            for comment in comments:
                parsed.append({
                    '昵称': comment.get('nickname', '匿名'),
                    '地区': comment.get('location', '未知'),
                    '日期': comment.get('creationTime', ''),
                    '产品': comment.get('productColor', '无'),
                    '评论': comment.get('content', '').strip(),
                    '评分': comment.get('score', 5)
                })
            return parsed
        except Exception as e:
            print(f"数据解析失败: {str(e)}")
            return None

    def _handle_pagination(self, current_page: int) -> bool:
        """执行翻页操作"""
        try:
            next_btn = self.dp.ele('css:.ui-pager-next', timeout=10)
            if next_btn:
                next_btn.run_js('this.click()')
                # 等待新评论加载
                self.dp.wait.ele_displayed('css:.comment-item', timeout=15)
                time.sleep(random.uniform(1, 3))  # 随机延时防检测
                print(f"成功跳转到第 {current_page + 1} 页")
                return True
            print("已到达最后一页")
            return False
        except Exception as e:
            print(f"翻页失败: {str(e)}")
            return False

    def scrape(self):
        """执行爬取主流程"""
        try:
            # 启动监听
            self.dp.listen.start('api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments')

            # 访问目标页面
            url = f'https://item.jd.com/{self.product_id}.html#comment'
            self.dp.get(url)
            print(f"开始爬取商品 {self.product_id} 的评论...")

            current_page = 1
            while current_page <= self.max_pages:
                print(f"正在获取第 {current_page}/{self.max_pages} 页...")

                if current_page == 1:
                    time.sleep(15)
                # 滚动到底部触发加载
                self.dp.scroll.to_bottom()
                time.sleep(1.5)

                # 获取数据包
                resp = self.dp.listen.wait(timeout=15)
                if not resp:
                    print("未捕获到数据包，可能接口已变更")
                    break

                # 解析并保存数据
                data = resp.response.body
                if not isinstance(data, dict):
                    print("收到非JSON响应，可能页面结构已变化")
                    break

                comments = self._parse_comment_data(data)
                if comments:
                    self._save_comments(comments)
                else:
                    print("未解析到有效评论数据")
                    break

                # 翻页操作
                if not self._handle_pagination(current_page):
                    break
                current_page += 1

        except Exception as e:
            print(f"爬取过程中发生异常: {str(e)}")
        finally:
            self.dp.quit()
            print("爬取结束，浏览器已关闭")


# 使用示例
if __name__ == "__main__":
    scraper = JDCommentScraper(
        product_id="10098514379443",  # 替换需要爬取的商品ID
        output_file="data/comments/jd_cheongsam.csv",
        max_pages=10  # 测试时爬取5页
    )
    scraper.scrape()