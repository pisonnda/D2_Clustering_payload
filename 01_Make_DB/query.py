#!/usr/bin/python3
import mysql.connector
import sqlalchemy
import sys
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/as63199?charset=utf8')


query = 'SHOW TABLES'
df = pd.read_sql(query, engine)
table_list = df["Tables_in_as63199"].values.tolist()

for i in table_list:
    query = 'SELECT DISTINCT srcip FROM ' + str(i) + ' ORDER BY srcip'
    name = "./srcip_63199/" + i[3:] + ".txt"
    df1 = pd.read_sql(query, engine)
    df1.to_csv(name, header=False, index=False)

    #query = 'SELECT DISTINCT vhash FROM ' + i
    #df2 = pd.read_sql(query, engine)
    #print(df2)
