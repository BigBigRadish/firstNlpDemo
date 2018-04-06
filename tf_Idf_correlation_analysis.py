# -*- coding: utf-8 -*-
'''
@author:Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn import svm
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
vectorizer = CountVectorizer()  
#计算个词语出现的次数  
X = vectorizer.fit_transform(data_process)  
#获取词袋中所有文本关键词  
word = vectorizer.get_feature_names()
x_train=X.toarray()
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
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovo')
clf.fit(x_train, y_train)
print (clf.score(x_train, y_train))  # 精度 
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

