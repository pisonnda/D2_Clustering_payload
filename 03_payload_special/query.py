#!/usr/bin/python3
import pandas
import mysql.connector
import sqlalchemy
import sys
from sqlalchemy import create_engine
import pandas as pd

#engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/Darknet17?charset=utf8')
vhash = sys.argv[1]

engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/vhash_content?charset=utf8')
query = 'SELECT payload_type, payload_content FROM db_20170910 WHERE vhash ="' + vhash + '"'
df = pd.read_sql(query, engine)

content = list(df['payload_content'])
ptype   = list(df['payload_type'])

for i in range(0, len(content)):
    p = content[i]
    try:
        payload = bytes.fromhex(p).decode('utf-8')
    except:
        payload = bytes.fromhex(p)

    #print("{}:\t{}\n{}".format(vhash, ptype[i], payload))
    print("{}:\t{}".format(vhash, payload))


#===================
# Get list Srcip - Dstip with key = vhash
#
#ofile = "63199_list_src-dst.csv"
#query = 'SELECT DISTINCT isrcip, idstip FROM db_20170901 WHERE vhash = "a668727d917520a1bd87a15c1380cec2"'
#df = pd.read_sql(query, engine)
#df.to_csv(ofile, header=False, index=False)
#===================

# Get as_num and vhash list
#
#table  =    input("Input Table's name:")
#as_num =    input("Input as_num:")
#
#query = 'SELECT as_num, vhash FROM ' + table +' WHERE NOT (vhash = "NULL") AND as_num=' + as_num
#query = 'SELECT DISTINCT vhash FROM db_20170901 WHERE NOT (vhash = "NULL")'
#df = pd.read_sql(query, engine)
#vhash_list = list(df["vhash"])
#print(len(vhash_list))
#
#for vhash in vhash_list:
#    query1 = 'SELECT DISTINCT srcip FROM db_20170901 WHERE vhash = ' + '"' + vhash + '"'
#    df1 = pd.read_sql(query1, engine)
#    query2 = 'SELECT DISTINCT dstip FROM db_20170901 WHERE vhash = ' + '"' + vhash + '"'
#    df2 = pd.read_sql(query2, engine)
#    print("{},{},{}".format(vhash, len(df1), len(df2)))
#

###############
#table_list = ['db_20170928', 'db_20170929', 'db_20170930']
#for i in table_list:
#    ofile = "./10_csv/" + i[3:] + ".csv"
#    query = 'SELECT as_num, vhash FROM ' + i +' WHERE NOT (vhash = "NULL")'
#    df = pd.read_sql(query, engine)
#    df.to_csv(ofile, header=False, index=False)
###############

#query = 'SHOW TABLES'
#df = pd.read_sql(query, engine)
#table_list = df["Tables_in_Darknet17"].values.tolist()

###############

#    #query = 'SELECT DISTINCT vhash FROM ' + i
#    #df2 = pd.read_sql(query, engine)
#    #print(df2)

###############
#query = 'SHOW DATABASES'
#query = 'SELECT as_num, vhash FROM db_20170901 WHERE NOT (vhash = "NULL")'
#df = pd.read_sql(query, engine)
#df.to_csv('./20170901.csv')

#query = 'SELECT as_num, vhash FROM db_20170901 WHERE NOT (vhash = "NULL") INTO OUTFILE "/data/pison/D2/03_payload_special/db_20170901.csv" FIELDS TERMINATED BY "," OPTIONALLY ENCLOSED BY "'"'

