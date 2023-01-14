#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
df=pd.read_csv('C:/Users/dlwld/Desktop/인공지능 중간/2019-05-trade.csv')

#Task1
def findExactProfit():
    i=0
    Sell=0
    Buy=0
    while(i<len(df)):
        if df['side'][i]==1:
            Sell+=df['quantity'][i]*df['price'][i]
        if df['side'][i]==0:
            Buy+=df['quantity'][i]*df['price'][i]    
        i+=1
    Total=Sell-Buy
    Total=math.floor(Total*10000)/10000
    return Total
print(findExactProfit())


# In[30]:


#Task2
def findSellCount(a):
    l=[]
    for i in range(0,len(a)):
        j=0
        s=0
        while(j<len(df)):
            if(df['timestamp_days'][j]==a[i])&(df['side'][j]==1):
                s+=1
            j+=1
        l.append(s)
    return l
        
def findBuyCount(a):
    l=[]
    for i in range(0,len(a)):
        j=0
        s=0
        while(j<len(df)):
            if (df['timestamp_days'][j]==a[i])&(df['side'][j]==0):
                s+=1
            j+=1
        l.append(s)
    return l  

df['timestamp_days']=pd.to_datetime(df['timestamp']).dt.day
days=[16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
Sell=findSellCount(days)
Buy=findBuyCount(days)
Transaction=[x+y for x,y in zip(Sell, Buy)]

task2_list=[
    ['timestamp_days',days],
    ['Sell',Sell],
    ['Buy',Buy],
    ['Sum',Transaction]
]
df2=pd.DataFrame.from_dict(dict(task2_list))
df2
plt.title('daily transaction count')
plt.plot(days,Sell,'r',label='SellCount')
plt.plot(days,Buy,'g',label='BuyCount')
plt.plot(days,Transaction,'b',label='DailyCount')
plt.xlabel('Timestamp_day')
plt.ylabel('')
plt.legend()
plt.show


# In[54]:


#Task3
#orderbook
dfo=pd.read_csv('C:/Users/dlwld/Desktop/인공지능 중간/2019-05-17-BTC-orderbook.csv')
df=pd.read_csv('C:/Users/dlwld/Desktop/인공지능 중간/2019-05-trade.csv')

#trade에서 17일만 뽑기
df['timestamp_days']=pd.to_datetime(df['timestamp']).dt.day
l=[]
for i in range(0,len(df)):
    if df['timestamp_days'][i]==17:
        l.append(i)
df2=df.loc[l]
# 17일 중에서도 timestamp기준으로 중복되는애 지우기
# df2=df1.drop_duplicates(['timestamp'])
df2=df2.drop(['fee','timestamp_days','amount'],axis='columns')


# 행 번호 초기화
df2=df2.reset_index()
df2=df2.drop('index',axis=1)

dfo['timestamp'] = pd.to_datetime(dfo['timestamp'])
dfo1=dfo[dfo['timestamp'].dt.second==0]

# df2timestamp 문자열리스트로 저장 (2019-05-17 00:00:00)

tmp=df2['timestamp']
tmp_val=tmp.values
timestamp_df2=tmp_val.tolist()

# dfo1timestamp 문자열리스트로 변환해서 저장 (2019-05-17 00:00:00)
ts=[]
dfo1=dfo1.reset_index(drop=True)
for i in range(0,len(dfo1)):
    tp=dfo1['timestamp'][i]
    ts.append(tp.strftime('%Y-%m-%d %H:%M'))
timestamp_dfo1=ts

dfo1['timestamp']=timestamp_dfo1


# # MidPrice 구하기

MidPrice=[]
TopLevelBuy=[]
TopLevelSell=[]
# top_buy_price
for i in range(0,len(df2)):
    for j in range(0,len(dfo1)):
        if timestamp_df2[i]==timestamp_dfo1[j]:
            if dfo1['type'][j]==0:
                TopLevelBuy.append(dfo1['price'][j])
                break
                
# top_sell_price
for i in range(0,len(df2)):
    for j in range(0,len(dfo1)):
        if timestamp_df2[i]==timestamp_dfo1[j]:
            if dfo1['type'][j]==1:
                TopLevelSell.append(dfo1['price'][j])
                break                
MidPrice=[(x+y)/2 for x,y in zip(TopLevelBuy,TopLevelSell)]
df2['midprice']=MidPrice

# Bfeature,Alpha 구하기

# askQty,bidQty,bidPx,book_price 구하기
# groupy를 이용해서 값을 확인 후, 저장
dfo_group=dfo.groupby('type').mean()

askQty=dfo_group['quantity'][1]
bidQty=dfo_group['quantity'][0]
bidPx=dfo_group['price'][0]
book_price=(askQty*bidPx)/bidQty
bfeature=[]
for i in range(0,len(MidPrice)):
    bfeature.append(book_price-MidPrice[i])

df2['bfeature']=bfeature


alpha=[(x*y) for x,y in zip(bfeature,MidPrice)]
df2['alpha']=alpha
df2=df2[['timestamp','quantity','price','midprice','bfeature','alpha','side']]

# 파일 저장
df2.to_csv(" new_2019_05_trade.csv", mode='w')

df2.head(20)


# In[55]:


df2.tail(20)


# In[31]:


#Task3 (other version - askQty,bidQty's definition is too ambiguous (average
# quantity of all levels for Sell). 오더북 전체 데이터에서 값을 추출하라는 것인지,
# 각 시간마다 해당되는 오더북의 데이터에서만 값을 추출하라는 말인지 워딩이 조금
# 헷갈리게 되어있는 것 같습니다.))

dfo=pd.read_csv('C:/Users/dlwld/Desktop/인공지능 중간/2019-05-17-BTC-orderbook.csv')
df=pd.read_csv('C:/Users/dlwld/Desktop/인공지능 중간/2019-05-trade.csv')

#trade에서 17일만 뽑기
df['timestamp_days']=pd.to_datetime(df['timestamp']).dt.day
l=[]
for i in range(0,len(df)):
    if df['timestamp_days'][i]==17:
        l.append(i)
df2=df.loc[l]
# 17일 중에서도 timestamp기준으로 중복되는애 지우기
# df2=df1.drop_duplicates(['timestamp'])
df2=df2.drop(['fee','timestamp_days','amount'],axis='columns')


# 행 번호 초기화
df2=df2.reset_index()
df2=df2.drop('index',axis=1)

dfo['timestamp'] = pd.to_datetime(dfo['timestamp'])
dfo1=dfo[dfo['timestamp'].dt.second==0]

# df2timestamp 문자열리스트로 저장 (2019-05-17 00:00:00)

tmp=df2['timestamp']
tmp_val=tmp.values
timestamp_df2=tmp_val.tolist()

# dfo1timestamp 문자열리스트로 변환해서 저장 (2019-05-17 00:00:00)
ts=[]
dfo1=dfo1.reset_index(drop=True)
for i in range(0,len(dfo1)):
    tp=dfo1['timestamp'][i]
    ts.append(tp.strftime('%Y-%m-%d %H:%M'))
timestamp_dfo1=ts

dfo1['timestamp']=timestamp_dfo1


# # MidPrice 구하기

MidPrice=[]
TopLevelBuy=[]
TopLevelSell=[]
# top_buy_price
for i in range(0,len(df2)):
    for j in range(0,len(dfo1)):
        if timestamp_df2[i]==timestamp_dfo1[j]:
            if dfo1['type'][j]==0:
                TopLevelBuy.append(dfo1['price'][j])
                break
                
# top_sell_price
for i in range(0,len(df2)):
    for j in range(0,len(dfo1)):
        if timestamp_df2[i]==timestamp_dfo1[j]:
            if dfo1['type'][j]==1:
                TopLevelSell.append(dfo1['price'][j])
                break                
MidPrice=[(x+y)/2 for x,y in zip(TopLevelBuy,TopLevelSell)]
df2['midprice']=MidPrice


# Bfeature,Alpha 구하기

# askQty,bidQty,bidPx,book_price
askQty=[]
bidQty=[]
bidPx=[]
book_price=[]
Bfeature=[]
for i in range(0,len(df2)):
    Sum1=0
    Sum2=0
    Sum3=0
    Sum1_Count=0
    Sum2_Count=0
    for j in range(0,len(dfo1)):
        if timestamp_df2[i]==timestamp_dfo1[j]:
            if dfo1['type'][j]==1:
                Sum1+=dfo1['quantity'][j]
                Sum1_Count+=1
            else:
                Sum2+=dfo1['quantity'][j]
                Sum3+=dfo1['price'][j]
                Sum2_Count+=1
    askQty.append(Sum1/Sum1_Count)
    bidQty.append(Sum2/Sum2_Count)
    bidPx.append(Sum3/Sum2_Count)
    book_price.append(((Sum1/Sum1_Count)*(Sum3/Sum2_Count))/(Sum2/Sum2_Count))

Bfeature=[(x-y) for x,y in zip(book_price,MidPrice)]
df2['bfeature']=Bfeature

alpha=[(x*y) for x,y in zip(Bfeature,MidPrice)]
df2['alpha']=alpha

df2=df2[['timestamp','quantity','price','midprice','bfeature','alpha','side']]
df2.head(20)


# In[32]:


df2.tail(20)


# In[ ]:




