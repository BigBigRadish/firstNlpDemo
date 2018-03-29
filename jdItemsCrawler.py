# -*- coding: utf-8 -*-
"""
Created on 12th Mar 12 19:19:04 2018

@author: Agnostic
"""

import urllib.request
import json
import time
import random
import pymysql.cursors

def crawlProductComment(url,page):
   
    #读取原始数据(注意选择gbk编码方式)
    html = urllib.request.urlopen(url).read().decode('gbk')
    print(html)
    #从原始数据中提取出JSON格式数据(分别以'{'和'}'作为开始和结束标志)
    jsondata = html[25:-2] 
    print(jsondata)
    data = json.loads(jsondata)
    print(data['comments'])
    #print(data['comments'][0]['content'])
    #遍历商品评论列表
    for i in data['comments']:
        productName = i['referenceName']
        commentTime = i['creationTime']
        content = i['content']

        #输出商品评论关键信息
        print("商品全名:{}".format(productName))
        print("用户评论时间:{}".format(commentTime))
        print("用户评论内容:{}".format(content))
        print("-----------------------------")

        '''
        数据库操作
        '''

        #获取数据库链接
        connection  = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '147258',
                                  db = 'jdcoments',
                                  charset = 'utf8mb4')
        try:
            #获取会话指针
            with connection.cursor() as cursor:
                #创建sql语句
                sql = "insert into `itemDetails` (`productName`,`commentTime`,`content`) values (%s,%s,%s)"

                #执行sql语句
                cursor.execute(sql,(productName,commentTime,content))

                #提交数据库
                connection.commit()
        finally:
            connection.close()


for i in range(0,100):
    print("正在获取第{}页评论数据!".format(i+1))
    #小米6评论链接,通过更改page参数的值来循环读取多页评论信息
    url = 'https://sclub.jd.com/comment/productPageComments.action?productId=12128543&score=0&sortType=3&page='+str(i)+'&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv310 '
    crawlProductComment(url,i)
    #设置休眠时间
    time.sleep(random.randint(3,10))