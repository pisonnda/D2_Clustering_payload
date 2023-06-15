#!/usr/bin/python3
import mysql.connector
import sqlalchemy
import sys
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/Darknet17?charset=utf8')
table_list = ['db_20170928', 'db_20170929', 'db_20170930']

for i in table_list:
    ofile = "./csv/" + i[3:] + ".csv"
    query = 'SELECT as_num, vhash FROM ' + i +' WHERE NOT (vhash = "NULL")'
    df = pd.read_sql(query, engine)
    df.to_csv(ofile, header=False, index=False)
