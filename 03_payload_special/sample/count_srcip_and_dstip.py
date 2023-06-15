#!/usr/bin/python3
import pandas
import mysql.connector
import sqlalchemy
import sys
import pandas as pd

from sqlalchemy import create_engine
from tqdm import tqdm

engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/as42570?charset=utf8')
#query = 'SELECT DISTINCT vhash FROM db_20170907 WHERE NOT (vhash = "NULL")'
#df = pd.read_sql(query, engine)
#ifile = open("63199/63199_special_payloads_September.lst", "r")

ifile = open("/data/pison/D2/03_payload_special/sample/42570/42570_0907_special.lst", "r")
#print("Loaded Special Payloads File!!")
dat = ifile.read()
special_payloads = dat.split("\n")
bar = tqdm(total = len(special_payloads))
#vhash_list = list(df["vhash"])

for vhash in special_payloads:
    bar.update(1)
    query1 = 'SELECT DISTINCT srcip FROM db_20170907 WHERE vhash = ' + '"' + vhash + '"'
    df1 = pd.read_sql(query1, engine)
    #if len(df1) < 2:
    #    continue
    query2 = 'SELECT DISTINCT dstip FROM db_20170907 WHERE vhash = ' + '"' + vhash + '"'
    df2 = pd.read_sql(query2, engine)
    print("{},{},{}".format(vhash, len(df1), len(df2)))
