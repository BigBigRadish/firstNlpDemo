# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime#��beautifulsoup��ȡ��ҳ
import requests
import urllib.request;
import time
import random
import pymysql
import threading
conn = pymysql.connect(host='127.0.0.1', user='root', password='147258', db='netbaseplaylist', charset='utf8mb4')
cur=conn.cursor() 
select_sql = 'SELECT * FROM playlist limit 9086,11200'
cur.execute(select_sql)
result = cur.fetchall()
print(result)
list=[]
count=9085
for r in result:
    bigtype=r[0]
    genres=r[1]
    playlist_url=r[3]
    count+=1
    playlist_url="http://music.163.com"+playlist_url
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent':user_agent}
    r = requests.get(playlist_url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')#html.parser
    content=[]
    print('当前爬取到第'+str(count)+'个链接：'+'流派为：'+genres)
    playlistName=soup.find("title").string
    #print(playlistName)
    createUser=soup.find(class_="s-fc7").get_text()
    #print(createUser)
    createuser_href=soup.find(class_="s-fc7").get('href')
    #print(createuser_href)
    j=0
    for i in soup.find(class_='f-hide').find_all('a'):
        if(j<=25):
            song_url=i.get('href')
            song_name=i.get_text()
            #print (song_url,song_name)
            j+=1
            connection  = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '147258',
                                  db = 'songslist',
                                  charset = 'utf8mb4')
            try:
              #获取会话指针
                    with connection.cursor() as cursor:
                #创建sql语句
                        sql = "insert into `songslist` (`bigtype`,`genres`,`playlistName`,`createUser`,`createuser_href`,`song_name`,`song_url`) values (%s,%s,%s,%s,%s,%s,%s)"

                #执行sql语句
                        cursor.execute(sql,(bigtype,genres,playlistName,createUser,createuser_href,song_name,song_url))

                #提交数据库
                        connection.commit()
            finally:
                        connection.close()            
        else:
            break
time.sleep(random.randint(1,2))  
cur.commit()
cur.close()
conn.close()