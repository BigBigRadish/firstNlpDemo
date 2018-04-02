# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup#beautifulsoup
import requests
import urllib.request;
import time
import random
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', password='147258', db='netbasegenres', charset='utf8mb4')
cur=conn.cursor() 
select_sql = 'SELECT * FROM bigtype limit 36,71 '
cur.execute(select_sql)
result = cur.fetchall()
print(result)
list=[]
for r in result:
    bigtype=r[0]
    genres=r[1]
    genres_href=r[2]
    for n in range(0,5):
        t=35*n
        genres_url="http://music.163.com"+genres_href+'&limit=35&offset='+str(t)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent':user_agent}
        r = requests.get(genres_url,headers=headers)
        soup = BeautifulSoup(r.text,'html.parser')#html.parser
        content=[]
        print('当前爬取到'+genres+'的'+str(n)+'页')
        for i in soup.find_all(class_='msk'):
            playlist_url=i.get('href')
            print (playlist_url)
            connection  = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '147258',
                                  db = 'netbaseplaylist',
                                  charset = 'utf8mb4')
            try:
              #获取会话指针
                    with connection.cursor() as cursor:
                #创建sql语句
                        sql = "insert into `playlist` (`bigtype`,`genres`,`genres_href`,`playlist_url`) values (%s,%s,%s,%s)"

                #执行sql语句
                        cursor.execute(sql,(bigtype,genres,genres_href,playlist_url))

                #提交数据库
                        connection.commit()
            finally:
                        connection.close()
        time.sleep(random.randint(3,10))
cur.commit()
cur.close()
conn.close()