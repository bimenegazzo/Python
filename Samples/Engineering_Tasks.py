#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import mysql.connector


# In[2]:


json = requests.get('https://volleypal.39-data.ru/get_objects/').json()
data = pd.json_normalize(json,"data")
data.head(1)


# In[3]:


#establishing the connection
mydb = mysql.connector.connect(
   user='test_user', password='test_user', host='68.198.26.23', port='3306', database='test_schema'
)
mycursor = mydb.cursor()


# In[4]:


#check connection
if (mydb.is_connected()):
    print("Connected")
else:
    print("Not connected")


# In[5]:


#delete table
drop = "DROP TABLE test_table"
mycursor.execute(drop)


# In[6]:


mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)


# In[7]:


#create table
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE test_table( shape VARCHAR(256), color VARCHAR(256), area NUMERIC )")


# In[8]:


mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)


# In[9]:


# creating column list for insertion
cols = "`,`".join([str(i) for i in data.columns.tolist()])

# Insert DataFrame recrds one by one.
for i, row in data.iterrows():
    sql = "INSERT INTO `test_table` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    mycursor.execute(sql, tuple(row))


# In[10]:


#delete table
drop = "DROP TABLE test_table"
mycursor.execute(drop)