# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import requests
import urllib.request;
import time
import random
import json
import re
import redis
import pymysql 
from pymongo import MongoClient
import DBUtils
from DBUtils.PooledDB import PooledDB
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQ'
headers={'User-Agent':user_agent}
pool = PooledDB(pymysql,5,host='localhost',user='root',passwd='147258',db='songslist',port=3306,charset='utf8mb4') #5为连接池里的最少连接数
con=MongoClient('localhost', 27017)
L = threading.Lock() 
def task1():
    L.acquire()    # 加锁
    db = con.netbaseSongsLyrics
    collection=db.lyrics   #连接mydb数据库，没有则自动创建
    conn = pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
    cur=conn.cursor() 
    select_sql = 'SELECT * FROM songslist limit 192306,194570'
    cur.execute(select_sql)
    result = cur.fetchall()
    content=[];
    count=192306
    for r in result:
        count+=1
        bigtype=r[0]
        genres=r[1]
        playlistName=r[2]
        createUser=r[3]
        songName=r[5]
        songId=r[6].replace("/song?id=","");
        print('正在爬取第'+str(count)+'条链接')
        songurl='http://music.163.com/'+r[6]
        songdetail=requests.get(songurl,headers=headers); 
        soup = BeautifulSoup(songdetail.text,'html.parser')#html.parser  
        try:
            singer=soup.find(class_="u-btni u-btni-share ").get('data-res-author')
        except AttributeError:
            singer=""
        lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + songId + '&lv=1&kv=1&tv=-1'
        lyric = requests.get(lrc_url,headers=headers)
        json_obj = lyric.text
        j = json.loads(json_obj)
        try:
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, ",", lrc)
        except KeyError:
            lrc=""
        songDetail = {"歌曲ID":songId,"歌曲名":songName,"歌曲链接":songurl,"歌手":singer,"歌词":lrc,"主类型":bigtype,"流派":genres,"歌单名":playlistName,"创建人":createUser}
        collection.insert(songDetail)
def main():
    now = datetime.now()             #开始计时
    print(now)
    thread = [] 
    for i in range(0,10): 
        t = threading.Thread(target=task1)   
        thread.append(t)
    for i in range(0,10):
        thread[i].start()
    for i in range(0,10):
        thread[i].join()     
        end = datetime.now()    #结束计时
        print(end)
        print("程序耗时： " + str(end-now))
        print ("all over") 
        con.close()
        pool.close()
if __name__ == '__main__':
    main()
    print("结束")

    