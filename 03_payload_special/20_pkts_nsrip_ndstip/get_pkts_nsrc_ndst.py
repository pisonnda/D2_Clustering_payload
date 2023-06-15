#!/usr/bin/python3
import pandas
import mysql.connector
import sqlalchemy
import sys
from tqdm import tqdm
import pandas as pd

from sqlalchemy import create_engine

#engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/as63199?charset=utf8')
engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/as63199_new?charset=utf8')

#query = 'SELECT DISTINCT vhash FROM db_20170906 WHERE NOT (vhash = "NULL")'
query = 'SELECT DISTINCT packet_size, vhash FROM db_20170901'

df = pd.read_sql(query, engine)
print(df)
vhash_list = list(df["vhash"][:1000])
print("Payloads: ", len(vhash_list))
bar = tqdm(total = len(vhash_list))

n_src = []
n_dst = []

for i in range(0, len(df)):
    bar.update(1)
    vhash       = df['vhash'][i]
    pkt_size    = df['packet_size'][i]
    query1 = 'SELECT srcip, dstip FROM db_20170901 WHERE vhash = ' + '"' + vhash + '"'
    df1 = pd.read_sql(query1, engine)
    n_src.append((len(df1['srcip'].unique())))
    n_dst.append((len(df1['dstip'].unique())))

#Add Number of Source IPs/Destination IPs
df['n_src'] = n_src
df['n_dst'] = n_dst
df.set_index("vhash", inplace=True)
df.to_csv("as63199_pkts_nsrc_ndst_0901.csv")
#df.to_csv("as63199_pkts_nsrc_ndst_02.csv")
