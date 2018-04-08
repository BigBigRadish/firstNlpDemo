# -*- coding: utf-8 -*-
'''
@author:Zhukun Luo
Jiangxi university of finance and economics
'''
import jieba
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
def testdata():#测试数据
    sentence = "原来你是 我最想留住的幸运,原来我们 和爱情曾经靠得那么近,那为我对抗世界的决定 那陪我淋的雨,一幕幕都是你 一尘不染的真心,与你相遇 好幸运,可我也失去 为你泪流满面的权利,但愿在我看不到的天际,你张开了双翼 遇见你的注定,她会有多幸运,我是被你囚禁的鸟,已经忘了天有多高,如果离开你给我的小小城堡,不知还有谁能依靠,我是被你囚禁的鸟,得到的爱越来越少,看着你的笑在别人眼中燃烧,我却要不到一个拥抱,我像是一个你可有可无的影子,冷冷地看着你说谎的样子,这撩乱的城市,容不下我的痴,是什么让你这样迷恋这样的放肆,我像是一个你可有可无的影子,和寂寞交换着悲伤的心事,对爱无计可施,这无味的日子,眼泪是唯一的奢侈"
    sentence=re.sub("[\s+\.\!\/_,$%^*(+\"\'：]+|[+——！，。？、~@#￥%……&*（）:】-一’()【-]+", " ",sentence) 
    sentence_seged = jieba.cut(sentence.strip(),cut_all = False)
    wordsCut=' '.join(sentence_seged)
    list=[]
    list.append(wordsCut)
    #print(wordsCut)
    return list
data=pd.read_csv(r"C:\Users\Agnostic\Desktop\netbaseLyrics\articleDetail.csv")
i=1
x = pd.DataFrame()
print(x)
data_process=[];
for i in range(1,72): 
    str1=str(data[:i]).lower()
    str1=re.sub("[0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", str1)
    print(str1)
    data_process.append(str1)    
#print(data_process)
#将文本中的词语转换为词频矩阵 
list=[] 
list= testdata()
vectorizer = CountVectorizer()  
tfidftransformer = TfidfTransformer()
#计算个词语出现的次数  
X = tfidftransformer.fit_transform(vectorizer.fit_transform(data_process))#训练集
X_test = tfidftransformer.transform(vectorizer.transform(list)) #测试集
#获取词袋中训练文本关键词    
#获取词袋中所有文本关键词  
#word = vectorizer.get_feature_names()
word = vectorizer.get_feature_names()
x_train=X.toarray()
x_test=X_test.toarray()
#print(word.__len__())
#word=str(word).encode(encoding='utf_8', errors='strict')
#df=pd.DataFrame(X.toarray(),columns=word)
#df.to_csv(r"C:\Users\Agnostic\Desktop\netbaseLyrics\wordVector.csv") 
#print (word) 
#查看词频结果  
#print (X.toarray())
result_list=[];
for i in range(0,71):
    result_list.append(i);
y_train=result_list
#clf = svm.SVC(C=1, kernel='linear', decision_function_shape='ovo')
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
clf.fit(x_train, y_train)
print (clf.score(x_train, y_train))  # 精度 
dec = clf.decision_function(x_train)
print(dec.shape[1]) # 4 classes: 4*3/2 = 6
predicted = clf.predict(x_test)
print(predicted)
#print ('decision_function:\n', clf.decision_function(x_train))
''' 
from sklearn.feature_extraction.text import TfidfTransformer  
  
#类调用  
transformer = TfidfTransformer()  
print transformer  
#将词频矩阵X统计成TF-IDF值  
tfidf = transformer.fit_transform(X)  
#查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重  
print tfidf.toarray()  
'''
# get the separating hyperplane
