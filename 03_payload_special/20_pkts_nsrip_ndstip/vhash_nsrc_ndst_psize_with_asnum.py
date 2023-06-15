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

    connector = mysql.connector.connect(host='localhost', user='pison', password='Ramen!yokosuka2023', database='experiment')
    cursor = connector.cursor()
    query_index = 'ALTER TABLE ' + table_name + ' ADD INDEX vhash_index(vhash(64))'
    cursor.execute(query_index)
    print("Create Index Successfull")
    
def make_db_as(as_num):
    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/new_dark17?charset=utf8')
    query = 'SELECT * FROM db_20170910 WHERE as_num = ' + str(as_num)
    df = pd.read_sql(query, engine)
    #print("Leng of Dataframe:\t", len(df))
    append2_sql(df, str(as_num) + "_0910")

def get_out_pay_feature(ofile, table_name):
    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/experiment?charset=utf8')
    query = 'SELECT DISTINCT vhash, dport, packet_size FROM ' + str(table_name)
    df = pd.read_sql(query, engine)
    vhash_list = list(df["vhash"])
    #print("Payloads: ", len(vhash_list))
    bar = tqdm(total = len(vhash_list))
    n_src = []
    n_dst = []
    for i in range(0, len(df)):
        bar.update(1)
        vhash       = df['vhash'][i]
        query1 = 'SELECT srcip, dstip FROM ' + str(table_name) + ' WHERE vhash = ' + '"' + vhash + '"'
        df1 = pd.read_sql(query1, engine)
        n_src.append((len(df1['srcip'].unique())))
        n_dst.append((len(df1['dstip'].unique())))

    df['n_src'] = n_src
    df['n_dst'] = n_dst
    df.set_index("vhash", inplace=True)
    df.to_csv(ofile)

as_num = input("Type AS Number: ")
make_db_as(as_num)
get_out_pay_feature(str(as_num) + "_0910.csv", str(as_num) + "_0910")
