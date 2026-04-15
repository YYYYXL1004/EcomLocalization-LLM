import requests
import json
import random
import time
from tqdm import tqdm

# 选择要爬去的商品id



def search_product_id(product_id):
    print(f'current {product_id}')
    url=f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={product_id}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    head = {}
    head['Uxer-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.50'
    out_json = []
    for count in tqdm(range(250)):
        if count!=0:
            url=f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={product_id}&score=0&sortType=5&page='+str(count)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
        proxies = [{'http':'socks5://117.69.13.180'},{'http':'socks5://113.194.130.117'},{'http':'socks5://110.243.15.253'},
                {'http':'socks5://125.108.72.92'},{'http':'socks5://110.243.15.253'},{'http':'socks5://171.35.149.223'},
                {'http':'socks5://125.108.108.150'},{'http':'socks5://123.163.116.56'},{'http':'socks5://123.54.52.37'},
                {'http':'socks5://113.124.87.85'},{'http':'socks5://171.11.29.66'},{'http':'socks5://163.204.92.79'},
                {'http':'socks5://117.57.48.102'},{'http':'socks5://125.108.110.245'},{'http':'socks5://115.218.6.85'},
                {'http':'socks5://219.146.127.6'},{'http':'socks5://120.83.101.249'},{'http':'socks5://223.242.225.19'},
                {'http':'socks5://121.8.146.99'},{'http':'socks5://110.243.7.237'},{'http':'socks5://115.218.2.104'},
                {'http':'socks5://183.195.106.118'},{'http':'socks5://49.86.176.16'},{'http':'socks5://222.89.32.141'},
                {'http':'socks5://1.198.73.202'},{'http':'socks5://136.228.128.6'},{'http':'socks5://136.228.128.6'},]
        n = 0
        while n == 0:   
            try:
                proxies1 = random.choice(proxies)
                html= requests.get(url,head,proxies=proxies1).text
                n += 1
            except:
                n = 0
        html=html[20:-2]
        html=json.loads(html)
        html=html['comments']
        for i in html:
            # file=open(f"comment_{product_id}.txt", 'a')
            # file.writelines('用户id: '+str(i['id'])+'\n'+'评分：  '+str(i['score'])+'颗星'+'\n'+'评论:   '+i['content']+'\n\n')
            out_json.append({
                'user_id':str(i['id']),
                'score':str(i['score']),
                'comment':i['content'],
            })
        # file.close()
        time.sleep(1)
    with open(f'data/{product_id}.json','w') as file:
        json.dump(out_json,file,indent=4,ensure_ascii=False)

if __name__ == '__main__':
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

    wrong_product_id = []
    for k,v in product_id_dict.items():
        try:
            search_product_id(k)
        except BaseException as error:
            print(f'error : ',k)
            wrong_product_id.append(k)
    print(f'爬去失败的id',wrong_product_id)
    with open(f'data/product_json/wrong.txt','w') as file:
        file.write('\n'.join(wrong_product_id))


