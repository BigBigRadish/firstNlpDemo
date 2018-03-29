# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup#用beautifulsoup爬取网页
import requests
import urllib.request;
import time
import pymysql
url="http://music.163.com/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD "
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers={'User-Agent':user_agent}
r = requests.get(url,headers=headers)
soup = BeautifulSoup(r.text,'html.parser')#html.parser
print(soup)
content=[]
for theme in soup.find_all(class_="f-cb"):
    big_type = theme.find('dt')
    if big_type!=None:
        bigtype = big_type.get_text()#获取标题
        print(bigtype)
        list=[]
        for a in theme.find('dd').find_all('a'):#获取所有的a标签中url和章节内容
            genres_href= a.get('href')
            print(genres_href)
            genres = a.get('data-cat')
            print(genres)

            connection  = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '147258',
                                  db = 'netbasegenres',
                                  charset = 'utf8mb4')
            try:
              #获取会话指针
                with connection.cursor() as cursor:
                #创建sql语句
                    sql = "insert into `bigtype` (`bigtype`,`genres`,`genres_href`) values (%s,%s,%s)"

                #执行sql语句
                    cursor.execute(sql,(bigtype,genres,genres_href))

                #提交数据库
                    connection.commit()
            finally:
                    connection.close()