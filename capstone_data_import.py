#!/usr/bin/env python
# coding: utf-8

# #package imports, global variables and functions

# In[2]:


import pymysql
import json
import csv
import pandas as pd

def yelp_json_reformat(fp, fn):
    result_coll = []
    headers = ""
    raw_file =  open(fp + "/" + fn, "r", encoding="utf8")
    counter = 0
    
    for line in raw_file:
        json_line = json.loads(line)
        
        if counter == 0:
            headers = list(json_line.keys())
            counter += 1
        
        row = list(json_line.values())
       
        for i,t in enumerate(row):
            if(type(t) is dict):
                row[i] = json.dumps(t)
        
        result_coll.append(tuple(row))
    
    raw_file.close()
    
    return headers, result_coll

def df_to_csv(df, fp, ext=".csv", na_rep=""):
    try:
        df.to_csv(fp + ext, encoding="utf-8", header = True,            doublequote = True, sep=",", index=False, na_rep=na_rep)
    except Exception as e:
        print("Error: {}".format(str(e)))
    

def execute_mysql(q, host, user, password):
    """
    This function load a csv file to MySQL table according to
    the load_sql statement.
    """
    try:
        con = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                autocommit=True,
                                local_infile=1)
        
        print("Connected to DB: {}".format(host))
        # Create cursor and execute Load SQL
        cursor = con.cursor()
        cursor.execute(q)
        print("Succuessfully loaded the table from csv.")
        
       
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        con.close()
        
def import_csv_to_sql(db_name, tbl_name, host, un, pw=""):
    tbl_name_w_db = db_name + "." + tbl_name
    
    q = "LOAD DATA LOCAL INFILE " + "'"         + fp + "/fixed/"+tbl_name+".csv' INTO TABLE " + tbl_name_w_db         + " FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    print(q)
    execute_mysql(q, host, un, pw)
    

fp = "C:/Users/Tolis/Documents/Data Analytics Cource/CKME136 X10/Project/data/final"


# #export yelp data to csv for easier and faster sql import.

# In[3]:


tbl_name = "business"
headers, data = yelp_json_reformat(fp, tbl_name+".json")

df = pd.DataFrame(data, columns=headers)
df[df["attributes"]==""] = None

df_to_csv(df,fp + "/fixed/" + tbl_name, ".csv", "{}")
#yelp_df_to_csv
#list_to_csv(data, headers, fp + "/fixed/" + tbl_name)
print(len(data),"rows written for", tbl_name + ".csv")
data = None
df = None


# In[4]:


tbl_name = "user"
headers, data = yelp_json_reformat(fp, tbl_name+".json")

df = pd.DataFrame(data, columns=headers)
df = df.drop(["friends"], axis=1)
df_to_csv(df,fp + "/fixed/" + tbl_name)
#yelp_df_to_csv
#list_to_csv(data, headers, fp + "/fixed/" + tbl_name)
print(len(data),"rows written for", tbl_name + ".csv")
data = None
df = None


# In[ ]:


tbl_name = "review"
headers, data = yelp_json_reformat(fp, tbl_name+".json")

df = pd.DataFrame(data, columns=headers)
df = df.drop(["text"], axis=1)


df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year 
 
df_2018 = df.loc[df["year"] == 2018]


df_2018 = df_2018.drop(["year"], axis=1)
df_to_csv(df_2018,fp + "/fixed/" + tbl_name)
#yelp_df_to_csv
#list_to_csv(data, headers, fp + "/fixed/" + tbl_name)
print(len(df_2018),"rows written for", tbl_name + ".csv")
data = None
df = None
df_2018 = None


# In[ ]:


tbl_name = "checkin"
headers, data = yelp_json_reformat(fp, tbl_name+".json")

df = pd.DataFrame(data, columns=headers)

def get_checkin_count(val):
    result = val.split(", ")
    return len(result)
    

df["date_count"] = df['date'].apply(get_checkin_count) 
df = df.drop(["date"], axis=1)
df_to_csv(df,fp + "/fixed/" + tbl_name)
#yelp_df_to_csv
#list_to_csv(data, headers, fp + "/fixed/" + tbl_name)
print(len(df),"rows written for", tbl_name + ".csv")
data = None
df = None


# In[ ]:


tbl_name = "tip"
headers, data = yelp_json_reformat(fp, tbl_name+".json")

df = pd.DataFrame(data, columns=headers)

df = df.drop(["text"], axis=1)
df_to_csv(df,fp + "/fixed/" + tbl_name)
#yelp_df_to_csv
#list_to_csv(data, headers, fp + "/fixed/" + tbl_name)
print(len(df),"rows written for", tbl_name + ".csv")
data = None
df = None


# In[ ]:


tbl_name = "photo"
headers, data = yelp_json_reformat(fp, tbl_name+".json")

df = pd.DataFrame(data, columns=headers)

df_to_csv(df,fp + "/fixed/" + tbl_name)
#yelp_df_to_csv
#list_to_csv(data, headers, fp + "/fixed/" + tbl_name)
print(len(df),"rows written for", tbl_name + ".csv")
data = None
df = None


# #import csv files directly to mysql

# In[ ]:


import_csv_to_sql("yelp", "business", "localhost", "root")


# In[ ]:


import_csv_to_sql("yelp", "user", "localhost", "root")


# In[ ]:


import_csv_to_sql("yelp", "review", "localhost", "root")


# In[ ]:


import_csv_to_sql("yelp", "checkin", "localhost", "root")


# In[ ]:


import_csv_to_sql("yelp", "tip", "localhost", "root")


# In[ ]:


import_csv_to_sql("yelp", "photo", "localhost", "root")


# #Add fk constraints to review table.
# #This is done after row inserts to prevent performance issues while the data is being imported.
# #Warning: This script may take awhile to execute.

# In[ ]:


try:
    con = pymysql.connect(host="localhost",
                            user="root",
                            password="",
                            database="yelp"
                            autocommit-True)

  
    cursor = con.cursor()

    q = """
    ALTER TABLE review
    ADD CONSTRAINT review_fk_business_id
    FOREIGN KEY (business_id) REFERENCES business(business_id);
    """
    cursor.execute(q)
    
    q = """
    ALTER TABLE review
    ADD CONSTRAINT review_fk_user_id
    FOREIGN KEY (user_id) REFERENCES user(user_id);
    """
    cursor.execute(q)
    
    q = """
    ALTER TABLE checkin
    ADD CONSTRAINT checkin_fk_business_id
    FOREIGN KEY (business_id) REFERENCES business(business_id);
    """
    cursor.execute(q)
    
    q = """
    ALTER TABLE photo
    ADD CONSTRAINT photo_fk_business_id
    FOREIGN KEY (business_id) REFERENCES business(business_id);
    """
    cursor.execute(q)
    
    q = """
    ALTER TABLE tip
    ADD CONSTRAINT tip_fk_business_id
    FOREIGN KEY (business_id) REFERENCES business(business_id);
    """
    cursor.execute(q)
    
    q = """
    ALTER TABLE tip
    ADD CONSTRAINT tip_fk_user_id
    FOREIGN KEY (user_id) REFERENCES user(user_id);
    """
    cursor.execute(q)
    
    print("Foreign Keys have been added to yelp db.")


except Exception as e:
    print("Error: {}".format(str(e)))
finally:
    con.close()

