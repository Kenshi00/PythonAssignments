#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
import requests
from tqdm import tqdm
import json
from collections import Counter
import random

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
#(1,5)->1~5회차까지의 데이터를 본다.

def getInfo1(minNo, maxNo):
    drwtNo1 = []
    drwtNo2 = []
    drwtNo3 = []
    drwtNo4 = []
    drwtNo5 = []
    drwtNo6 = []
    bnusNo = []
    totSellamnt = []
    drwNoDate = []
    firstAccumamnt = []
    firstPrzwnerCo = []
    firstWinamnt = []
    roundNo=[]
    #tqdm은 반복문의 진행상황을 알려준다.
    for i in tqdm(range(minNo, maxNo+1, 1)): #(1,5)면 -> 1부터 5까지 1씩 증가하며 i에 넣는것
        #No=숫자 입력 시 그 회차 요청
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)
        requestlotto = requests.get(url)
        lotNum = requestlotto.json()
        
        drwtNo1.append(lotNum['drwtNo1'])
        drwtNo2.append(lotNum['drwtNo2'])
        drwtNo3.append(lotNum['drwtNo3'])
        drwtNo4.append(lotNum['drwtNo4'])
        drwtNo5.append(lotNum['drwtNo5'])
        drwtNo6.append(lotNum['drwtNo6'])
        bnusNo.append(lotNum['bnusNo'])
        roundNo.append(i)
        drwNoDate.append(lotNum['drwNoDate'])
        
        dataset = { "round":roundNo,"date":drwNoDate, "Num1":drwtNo1, "Num2":drwtNo2, "Num3":drwtNo3, "Num4":drwtNo4, "Num5":drwtNo5, "Num6":drwtNo6,
                      "bnsNum":bnusNo}
        
    df = pd.DataFrame(dataset)
        
    return df

num=100
#Task 1
df1_1=getInfo1(1,num)
totalNumlist = list(df1_1['Num1']) + list(df1_1['Num2']) + list(df1_1['Num3']) + list(df1_1['Num4']) + list(df1_1['Num5']) + list(df1_1['Num6'])
count=Counter(totalNumlist)
countSet=count.most_common(45)
df1_2=pd.DataFrame(countSet,columns=['num','times'])
df1_2.to_csv("getTimes1.csv",index=False)
pd.read_csv("getTimes1.csv")


# #Task 4
x=[]
y=[]
df4=pd.DataFrame(columns=['x','y'])
for i in range(num):
    # 1~3번 숫자의 평균을 x, 4~6번 숫자의 평균을 y로 놓았다.
    x.append((list(df1_1['Num1'])[i]+list(df1_1['Num2'])[i]+list(df1_1['Num3'])[i])/3)
    y.append((list(df1_1['Num4'])[i]+list(df1_1['Num5'])[i]+list(df1_1['Num6'])[i])/3)
for i in range(num):
    df4.loc[i]=[x[i],y[i]]
df4.head(10)

# visualize data point
sns.lmplot('x', 'y', data=df4, fit_reg=False, scatter_kws={"s": 200}) # x-axis, y-axis, data, no line, marker size
# title
plt.title('kmean plot')
# x-axis label
plt.xlabel('x')
# y-axis label
plt.ylabel('y')
# convert dataframe to numpy array
data_points = df4.values
kmeans = KMeans(n_clusters=5).fit(data_points)
# cluster id for each data point
kmeans.labels_
# this is final centroids position
kmeans.cluster_centers_
df4['cluster_id'] = kmeans.labels_
df4.head(12)
sns.lmplot('x', 'y', data=df4, fit_reg=False,  # x-axis, y-axis, data, no line
           scatter_kws={"s": 150}, # marker size
           hue="cluster_id") # color

# title
plt.title('after kmean clustering')


# In[88]:



#Task 2
def getInfo2(minNo, maxNo):
    drwtNo1 = []
    drwtNo2 = []
    drwtNo3 = []
    drwtNo4 = []
    drwtNo5 = []
    drwtNo6 = []
    bnusNo = []
    drwNoDate = []
    roundNo=[]
    win=[]
    #tqdm은 반복문의 진행상황을 알려준다.
    for i in tqdm(range(minNo, maxNo+1, 1)): #(1,5)면 -> 1부터 5까지 1씩 증가하며 i에 넣는것
        #No=숫자 입력 시 그 회차 요청
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)
        requestlotto = requests.get(url)
        lotNum = requestlotto.json()
        
        # win=1
        roundNo.append(i)
        drwNoDate.append(lotNum['drwNoDate'])
        drwtNo1.append(lotNum['drwtNo1'])
        drwtNo2.append(lotNum['drwtNo2'])
        drwtNo3.append(lotNum['drwtNo3'])
        drwtNo4.append(lotNum['drwtNo4'])
        drwtNo5.append(lotNum['drwtNo5'])
        drwtNo6.append(lotNum['drwtNo6'])
        bnusNo.append(lotNum['bnusNo'])
        win.append("1")
        dataset = { "round":roundNo,"date":drwNoDate, "Num1":drwtNo1, "Num2":drwtNo2, "Num3":drwtNo3, "Num4":drwtNo4, "Num5":drwtNo5, "Num6":drwtNo6,
                      "bnsNum":bnusNo,"win":win}
        real=[lotNum['drwtNo1'],lotNum['drwtNo2'],lotNum['drwtNo3'],
             lotNum['drwtNo4'],lotNum['drwtNo5'],lotNum['drwtNo6']]
        # win=0
        fake=random.sample(range(1,46),7)
        roundNo.append(i)
        drwNoDate.append(lotNum['drwNoDate'])
        drwtNo1.append(fake[0])
        drwtNo2.append(fake[1])
        drwtNo3.append(fake[2])
        drwtNo4.append(fake[3])
        drwtNo5.append(fake[4])
        drwtNo6.append(fake[5])
        bnusNo.append(fake[6])
        if(real==fake):
            win.append("1")
        else:
            win.append("0")
        dataset = { "round":roundNo,"date":drwNoDate, "Num1":drwtNo1, "Num2":drwtNo2, "Num3":drwtNo3, "Num4":drwtNo4, "Num5":drwtNo5, "Num6":drwtNo6,
                      "bnsNum":bnusNo,"win":win}
    df = pd.DataFrame(dataset)
        
    return df
#Task 2
df2_1=getInfo2(1,num)
df2_1.to_csv("getInfo2.csv",index=False)
pd.read_csv("getInfo2.csv")


#Task 3
#totalFakeList=list(df2_1['Num1']) + list(df2_1['Num2']) + list(df2_1['Num3']) + list(df2_1['Num4']) + list(df2_1['Num5']) + list(df2_1['Num6'])
#totalFakeList=totalFakeList[1::2]

#count2=Counter(totalFakeList)
#countSet2=count2.most_common(45)
#df2_2=pd.DataFrame(countSet2,columns=['num','times'])
#df2_2.to_csv("getTimes2.csv",index=False)
#pd.read_csv("getTimes2.csv")


# In[34]:





# In[25]:





# In[ ]:




