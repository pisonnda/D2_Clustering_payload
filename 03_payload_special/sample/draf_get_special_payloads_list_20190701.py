import csv
import mysql.connector
import numpy
import pandas as pd
import pickle
import sqlalchemy
import sys

from tqdm import tqdm
from sqlalchemy import create_engine



#Write and Read data to (from) binary file
def write_list(pay_list):
    with open("special_list_63199_0902.dump", "wb") as fp:
        pickle.dump(pay_list, fp)
        print("Done writing list into a binary file")

def read_list():
    with open("special_list_63199_0902.dump", "rb") as fp:
        pay_list = pickle.load(fp)
        return pay_list


def main():
    #Read 2017 September's Special payloads list
    ifile = open("./63199/63199_special_payloads_September.lst", "r")
    #print("Read special_payloads.lst: OK!")
    dat = ifile.read()
    september_payloads = dat.split("\n")
    ifile.close

    #Read payloads in 2017/09/01
    #fields_name = ["as_num", "vhash"]
    #df1 = pd.read_csv("42570_0907.csv", names = fields_name)
    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/as63199?charset=utf8')
    query = 'SELECT DISTINCT vhash FROM db_20170902 WHERE NOT (vhash = "NULL")'
    df = pd.read_sql(query, engine)
    payloads = list(df["vhash"])

    #Get list special payloads in 2017/09/01 (Matching up)
    #print("Running")
    leng = len(september_payloads)
    #print("Payload in 0902: {}".format(leng))
    bar = tqdm(total = leng)
    special_payload_0902 = []

    for ipay in september_payloads:
        bar.update(1)
        if ipay in payloads:
            special_payload_0902.append(ipay)
        else: continue

    bar = tqdm(total = len(special_payload_0902))
    for vhash in special_payload_0902:
        bar.update(1)
        query1 = 'SELECT DISTINCT srcip FROM db_20170902 WHERE vhash = ' + '"' + vhash + '"'
        df1 = pd.read_sql(query1, engine)
        query2 = 'SELECT DISTINCT dstip FROM db_20170902 WHERE vhash = ' + '"' + vhash + '"'
        df2 = pd.read_sql(query2, engine)
        print("{},{},{}".format(vhash, len(df1), len(df2)))

    #write_list(special_payload_0902)
if __name__ == '__main__':
    main()
