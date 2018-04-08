# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn import svm
import re 
import threading
import jieba,math
import jieba.analyse
sentence = "原来你是 我最想留住的幸运,原来我们 和爱情曾经靠得那么近,那为我对抗世界的决定 那陪我淋的雨,一幕幕都是你 一尘不染的真心,与你相遇 好幸运,可我也失去 为你泪流满面的权利,但愿在我看不到的天际,你张开了双翼 遇见你的注定,她会有多幸运,我是被你囚禁的鸟,已经忘了天有多高,如果离开你给我的小小城堡,不知还有谁能依靠,我是被你囚禁的鸟,得到的爱越来越少,看着你的笑在别人眼中燃烧,我却要不到一个拥抱,我像是一个你可有可无的影子,冷冷地看着你说谎的样子,这撩乱的城市,容不下我的痴,是什么让你这样迷恋这样的放肆,我像是一个你可有可无的影子,和寂寞交换着悲伤的心事,对爱无计可施,这无味的日子,眼泪是唯一的奢侈"
sentence=re.sub("[\s+\.\!\/_,$%^*(+\"\'：]+|[+——！，。？、~@#￥%……&*（）:】-一’()【-]+", " ",sentence) 
sentence_seged = jieba.cut(sentence.strip(),cut_all = False)
wordsCut=' '.join(sentence_seged)
list=[]
list.append(wordsCut)
print(wordsCut)
vectorizer = CountVectorizer()
X_test = vectorizer.fit_transform(list)  
#获取词袋中所有文本关键词  
word = vectorizer.get_feature_names()
x_test=X_test.toarray()
print (x_test)