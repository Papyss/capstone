#!/usr/bin/env python
# coding: utf-8

# #package imports, global variables and functions

# In[1]:


import mysql.connector
import json
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [20, 15]

host = "localhost"
un = "root"
pw=""
db_name = "yelp"

def mysql_result_to_df(result, cursor):
    field_names = [i[0] for i in mycursor.description]
    return pd.DataFrame(myresult, columns=field_names)

def df_to_csv(df, fp, ext=".csv", na_rep=""):
    try:
        df.to_csv(fp + ext, encoding="utf-8", header = True,            doublequote = True, sep=",", index=False, na_rep=na_rep)
    except Exception as e:
        print("Error: {}".format(str(e)))

fp = "C:/Users/Tolis/Documents/Data Analytics Cource/CKME136 X10/Project/data/final/summary"


# #Connect to yelp db and load photo table

# In[2]:


mydb = mysql.connector.connect(
  host=host,
  user=un,
  passwd=pw,
  database=db_name
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM photo")

myresult = mycursor.fetchall()

photo_df = mysql_result_to_df(myresult, mycursor)

#Replace blank strings or objects {} to null
photo_df = photo_df.replace(r'^\s*$', np.nan, regex=True)
photo_df = photo_df.replace(r'^{}*$', np.nan, regex=True)

mycursor.close()
mydb.close()


# In[3]:


print(photo_df[0:10])


# #Replace blanks as null and transform list column

# #Qualitative summaries
# #This table does not have any number cols

# In[4]:


#Description for qualitative
df_description_cat = photo_df.describe(include=[np.object])
print(df_description_cat)


# In[5]:


#Row and col counts.
row_count = photo_df.shape[0]
col_count = photo_df.shape[1]
print(photo_df.shape)


# In[6]:


#Summary of NULLS
#Will need to drop fields that have a Null Percent > .5
#I will then fill the remaining null values with their field's average.
null_columns=photo_df.columns[photo_df.isnull().any()]
df_description_nulls=photo_df[null_columns].isnull().sum()
df_description_nulls = pd.DataFrame(df_description_nulls, columns=["Null Count"])
df_description_nulls["Null Percent"] = df_description_nulls["Null Count"].apply(lambda x: x/row_count)
print(df_description_nulls)


# #plots

# In[7]:


#Clean up and save description csv.
#The plots can be obtained via screenshot.

#To make sure field names make it in output csv
row_labels = df_description_nulls.index.values
df_description_nulls.insert (0, "Field", row_labels)
df_to_csv(df_description_nulls, fp + "/photo_desc_nulls", ext=".csv", na_rep="")


row_labels = df_description_cat.index.values
df_description_cat.insert (0, "Param", row_labels)
df_to_csv(df_description_cat, fp + "/photo_desc_cat", ext=".csv", na_rep="")


# In[8]:


photo_df = None
photo_df_cat = None


# In[ ]:




