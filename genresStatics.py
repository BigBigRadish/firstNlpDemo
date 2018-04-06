# -*- coding: utf-8 -*-
from datetime import datetime
import re 
import threading
import jieba,math
import jieba.analyse
import nltk
import jieba.posseg as psg
#from nltk.tokenize import WordPunctTokenizer  
from pymongo import MongoClient
con=MongoClient('localhost', 27017)
db = con.netbaseSongsLyrics
collection=db.wordCut   #连接mydb数据库，没有则自动创建
collection1=db.wordsCut
#lyricsObj=collection.find_one();
#obj_lyrics=lyricsObj["歌词"];
#print(obj_lyrics)

def wordcount(words):
    #words = jieba.cut(obj_lyrics, cut_all =True)
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    freq_word = []
    for word, freq in word_freq.items():
        freq_word.append((word, freq))
    freq_word.sort(key = lambda x: x[1], reverse = True)
    max_number = int(input())
    for word, freq in freq_word[: max_number]:
        print (word, freq)
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'rb').readlines()]  
    return stopwords  
# 对句子进行分词  ,并统计词性和频数
def seg_sentence(sentence,i):  
    sentence_seged = psg.cut(sentence.strip())  
    stopwords = stopwordslist('C:/Users/Agnostic/Desktop/netbaseLyrics/哈工大停用词表.txt')  # 这里加载停用词的路径  
    outstr = ''
    word_freq = {}  
    for ele in sentence_seged:  
        if ele.word not in stopwords:  
            if ele in word_freq:
                word_freq[ele] += 1
            else:
                word_freq[ele] = 1
    freq_word = []
    for ele, freq in word_freq.items():
        freq_word.append((ele.word, ele.flag,freq))
    freq_word.sort(key = lambda x: x[1], reverse = True)
    for ele.word, ele.flag,freq in freq_word:
        genres=i;
        word=ele.word;
        flag=ele.flag
        freq=freq;
        wordDetail = {"genres":genres,"word":word,"flag":flag,"freq":freq}
        collection.insert(wordDetail)
#分词1
def seg_sentence1(sentence,i):  
    sentence_seged = jieba.cut(sentence.strip(),cut_all = False)  
    genres=i
    wordsCut=' '.join(sentence_seged)
    wordDetail = {"genres":i,"words":wordsCut}
    collection1.insert(wordDetail)
#分词
'''
genres =collection.distinct("流派",{});
print(genres)
'''
genres=['华语', '欧美', '日语', '韩语', '粤语', '小语种', '流行', '摇滚', '民谣', '电子', '舞曲', '说唱', '轻音乐', '爵士', '乡村', 'R&BandSoul', '古典', '民族', '英伦', '金属', '朋克', '蓝调', '雷鬼', '世界音乐', '拉丁', '另类独立', 'New Age', '古风', '后摇', 'Bossa Nova', '清晨', '夜晚', '学习', '工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧', '怀旧', '清新', '浪漫', '性感', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念', '影视原声', 'ACG', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '儿童', '榜单', '00后']
for i in genres:
    file = open("C:/Users/Agnostic/Desktop/netbaseLyrics/riginalData/"+i+".txt",encoding='utf-8') 
    txt = file.read()
    txt1=re.sub("[\s+\.\!\/_,$%^*(+\"\'：]+|[+——！，。？、~@#￥%……&*（）:】-一’()【-]+", " ",txt)  
#text='狗尾巴牛尾巴尾巴'  
#sent_tokenize_list = WordPunctTokenizer().tokenize(text) 
#print(sent_tokenize_list) 

    print(txt1)
    seg_sentence1(txt1,i)

        
   # with open("C:/Users/Agnostic/Desktop/netbaseLyrics/分词文件/游戏_1.txt","a",encoding='utf-8') as f:
        #f.write(outstr)
'''
将每一个类别存储为文件 
#y=[  '影视原声', 'ACG', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '儿童', '榜单', '00后']
genres =collection.distinct("流派",{});
print(genres)
#for i in y:
lyricsObj1=collection.find({"流派":"古典"},{"歌词":-1});
for obj_lyrics1 in lyricsObj1:
    with open("C:/Users/Agnostic/Desktop/netbaseLyrics/古典.txt","a",encoding='utf-8') as f:
        f.write(obj_lyrics1["歌词"])
    print(obj_lyrics1["歌词"])
'''   

    