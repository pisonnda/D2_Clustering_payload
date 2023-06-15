#!/usr/bin/python3
import pandas
import mysql.connector
import sqlalchemy
import sys
import pandas as pd

from tqdm import tqdm
from sqlalchemy import create_engine


def append2_sql(df, table_name):
        engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/experiment?charset=utf8')
        connection = engine.connect()
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        connection.close()
        print("Appended Data " + str(table_name) + " to MySQL server")

def count_payload(as_num):
    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/new_dark17?charset=utf8')
    query = 'SELECT COUNT(DISTINCT vhash) FROM db_20170910 WHERE as_num = ' + str(as_num)
    df = pd.read_sql(query, engine)
    return df['COUNT(DISTINCT vhash)'][0]
    #append2_sql(df, str(as_num) + "_0910")

def get_as_list():
    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/new_dark17?charset=utf8')
    query = 'SELECT DISTINCT as_num FROM db_20170910 LIMIT 60'
    df = pd.read_sql(query, engine)
    as_list = list(df['as_num'])[:]
    return as_list


as_list = get_as_list()
bar = tqdm(total = len(as_list))
for as_num in as_list:
    bar.update(1)
    payload_counter = count_payload(as_num)
    print("{}:\t{}".format(as_num, payload_counter))
