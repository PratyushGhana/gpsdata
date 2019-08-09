#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import datetime


# In[2]:


with open("/home/pratyush/Downloads/4de9d124e5f43a61be9cb2aee09c9e08-7e9c9d22789f883807b4f5f82d1f620b59ea0cee/garmin.gpx") as fp:
    soup = BeautifulSoup(fp,"html.parser")


# In[3]:


points=soup.find_all("trkpt")
points[0]


# In[4]:


len(points)


# In[5]:



[item.get_text() for item in points[0].findChildren()]


# In[6]:


elevs=[float(x.get_text())for x in soup.find_all("ele")]
time=[x.get_text()for x in soup.find_all("time")][1:]


# In[7]:


pairs=zip(elevs,time)


# In[8]:


df1=pd.DataFrame.from_records(pairs)
df1.columns = ['elev', 'time']

df1.head()


# In[9]:


df1.describe()


# In[10]:


df1['elev_feet']=df1['elev'].map(lambda x: x*3.28)


# In[11]:


df1.head()


# In[12]:


from dateutil import parser
parser.parse(df1.iloc[10]['time'])
df1['time_time']=df1['time'].map(lambda time_str:parser.parse(time_str))
df1.head()


# In[25]:


df1['prior_time']=df1['time_time'].shift(1)
df1['time_since_prior']=df1['time_time']-df1['prior_time']
df1.head()


# In[14]:


import googlemaps
maps_key="use_your_api_key"
df1['time_since_prior'].value_counts()
gmaps = googlemaps.Client(key=maps_key)


# In[18]:


gmaps.distance_matrix((38.85687575675547122955322265625, -104.9322570674121379852294921875),
(38.85704356245696544647216796875, -104.9336370639503002166748046875))['rows'][0]['elements'][0]['duration']['text']


# In[32]:


df1['prior_elev']=df1['elev_feet'].shift(1)
df1['elev_gained_since_prior']=df1['elev_feet']-df1['prior_elev']
df1.head()


# In[21]:


from matplotlib import pyplot as plt


# In[35]:


fig = plt.figure()

ax= fig.add_subplot(111)
ax2 = ax.twinx()

df1.elev_feet.plot(kind='line',color='red',ax=ax)
df1.elev_gained_since_prior.plot(kind='line',color='blue',ax=ax2)

ax.set_ylabel('Feet')
ax2.set_ylabel('Meters')

plt.show()


# In[ ]:




