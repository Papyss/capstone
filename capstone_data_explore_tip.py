#!/usr/bin/env python
# coding: utf-8

# #package imports, global variables and functions

# In[15]:


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


# #Connect to yelp db and load user table

# In[16]:


mydb = mysql.connector.connect(
  host=host,
  user=un,
  passwd=pw,
  database=db_name
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM tip")

myresult = mycursor.fetchall()

tip_df = mysql_result_to_df(myresult, mycursor)

mycursor.close()
mydb.close()


# In[17]:


print(tip_df[0:10])


# In[18]:


#Replace empty strings and json objects to null
tip_df = tip_df.replace(r'^\s*$', np.nan, regex=True)
tip_df = tip_df.replace(r'^{}*$', np.nan, regex=True)


# #Numeric summaries

# In[19]:


#Description of quantitative fields.
df_description_number = tip_df.describe(include=[np.number])
print(df_description_number)


# In[20]:


#Description for qualitative
df_description_cat = tip_df.describe(include=[np.object])
print(df_description_cat)


# In[21]:


#Row and col counts.
row_count = tip_df.shape[0]
col_count = tip_df.shape[1]
print(tip_df.shape)


# In[22]:


#Summary of NULLS
#Doesn't seem to be any nulls
null_columns=tip_df.columns[tip_df.isnull().any()]
df_description_nulls=tip_df[null_columns].isnull().sum()
df_description_nulls = pd.DataFrame(df_description_nulls, columns=["Null Count"])
df_description_nulls["Null Percent"] = df_description_nulls["Null Count"].apply(lambda x: x/row_count)
print(df_description_nulls)


# #plots

# In[23]:


#Visualize correlations between quantitative vars
#variables that are strongly correleated will be removed during the feature selection process.
corr = tip_df.corr()
sns.heatmap(corr, cmap="Blues", 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)


# In[24]:


tip_df_num = tip_df.select_dtypes(include=np.number)


hist = tip_df_num.hist()
#Histograms don't really show much here because a lot of the fields are very close together with little spread.
#In addition, most values for these fields seem to be close to 0.
#However, it seems stars has a skewed to the left distribution (due to the peak at 5.0.


# In[25]:


#Scale and center data to compare variance in side-by-side boxplots, and to easily spot outliers.
df_center = (tip_df_num - tip_df_num.mean())
df_scale = (df_center - df_center.mean())/df_center.std()
df_scale.plot.box()
#A lot of outlier and extremes. These will have to be treated prior to analysis.
#Stars seems to have low spread with no outliers, most likely because there is a max set by yelp.


# In[26]:


#Clean up and save description csv.
#The plots can be obtained via screenshot.

#To make sure field names make it in output csv
row_labels = df_description_nulls.index.values
df_description_nulls.insert (0, "Field", row_labels)
df_to_csv(df_description_nulls, fp + "/tip_desc_nulls", ext=".csv", na_rep="")

row_labels = df_description_number.index.values
df_description_number.insert (0, "Param", row_labels)
df_to_csv(df_description_number, fp + "/tip_desc_number", ext=".csv", na_rep="")

row_labels = df_description_cat.index.values
df_description_cat.insert (0, "Param", row_labels)
df_to_csv(df_description_cat, fp + "/tip_desc_cat", ext=".csv", na_rep="")
tip_df = None
tip_df_num = None
tip_df_cat = None


# In[ ]:




