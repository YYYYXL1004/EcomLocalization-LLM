# -- coding: utf-8 --
import requests  as re
import json
import xlwt
import random
import pandas as pd
from pandas.io.json import json_normalize
headers = {'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Request Method':'Get',
            'callback':'fetchJSON_comment98'}
content=[]
usefulVoteCount=[]
replyCount=[]
score=[]
creationTime=[]
shopreply=[]
Plus=[]
imageCount=[]
reply=[]
afterusercount=[]
afterusercomment=[]
afterdays=[]
j=1
pd.set_option('display.max_columns',None)
#显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.max_colwidth',1000)
def crawler(url):
    global j
    req=re.get(url,timeout=random.uniform(30, 50),headers=headers)  # 获取网页信息
    jd=json.loads(req.text.lstrip("fetchJSON_comment98vv375(").rstrip(");"))
    for i in jd['comments']:
        print(str(j)+"、"+i['content'])
        print(i['usefulVoteCount'])
        print(i['replyCount'])
        print(i['score'])
        content.append(i['content'])
        usefulVoteCount.append(i['usefulVoteCount'])
        replyCount.append(i['replyCount'])
        score.append(i['score'])
        creationTime.append(i['creationTime'])
        if( 'replies' in i and i['replies']):
            shopreply.append(1)
            # x=i['replies']
            # x1=x[3]['content']
            x=pd.json_normalize(i,record_path=['replies'])
            # print(x)
            x1=x['content']
            # print(x1)
            reply.append(x1)
        else:
            shopreply.append(0)
            reply.append('无')
        if(i['plusAvailable']==0):
            Plus.append(0)
        else:
            Plus.append(1)
        if('imageCount' in i):
            imageCount.append(i['imageCount'])
        else:
            imageCount.append(0)
        if('afterUserComment' in i):
            afterusercount.append(1)
            y=i['afterUserComment']
            y1=y['content']
            # y=pd.json_normalize(i,record_path=['afterUserComment'])
            # y1=y['content']
            afterusercomment.append(y1)
        else:
            afterusercount.append(0)
            afterusercomment.append('无')
        afterdays.append(i['afterDays'])
        j=j+1
for i in range(0,70):
    # url="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100035225788&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1"
    # url="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100011493273&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1"
    # url="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100033901461&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1"
    url="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100015394629&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1"
    url=url.format(i)
    crawler(url)
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = book.add_sheet('京东redmi9A手机评论',cell_overwrite_ok=True)
col = ('评论内容','评论点赞数','评论回复数','星级','发布时间','商家回复','回复内容','Plus会员','是否追加评论','追加评论内容','追加评论时间','图片数')
for i in range(0,12):
	sheet.write(0,i,col[i])
for i in range(1,700):
        sheet.write(i,0,label=content[i])
        sheet.write(i,1,label=usefulVoteCount[i])
        sheet.write(i,2,label=replyCount[i])
        sheet.write(i,3,label=score[i])
        sheet.write(i,4,label=creationTime[i])
        sheet.write(i,5,label=str(shopreply[i]))
        sheet.write(i,6,label=str(reply[i]))
        sheet.write(i,7,label=str(Plus[i]))
        sheet.write(i,8,label=str(afterusercount[i]))
        sheet.write(i,9,label=str(afterusercomment[i]))
        sheet.write(i,10,label=str(afterdays[i]))
        sheet.write(i,11,label=str(imageCount[i]))

book.save('实验数据集43.xls')