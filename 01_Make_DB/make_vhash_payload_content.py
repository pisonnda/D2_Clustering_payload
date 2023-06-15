#!/usr/bin/python3
import csv
import dpkt
import hashlib
import mysql.connector
import pandas as pd
import sys
import zstandard as zstd

from mysql.connector import Error
from sqlalchemy import create_engine
from tqdm import tqdm

vhash_dict = {}
content_list = []
type_list = []

def remove_column(dict_a, n):
    result = []
    for k,v in dict_a.items():
        result.append(v[n])
    return result

def read_pcap(pfile):
    fp = open(pfile, "rb")
    packets = dpkt.pcap.Reader(fp)
    return packets

def read_pcap_zst(zstfile):
    with open(zstfile, "rb") as f:
        data = f.read()
    dctx = zstd.ZstdDecompressor()
    decompressed = dctx.stream_reader(data)
    packets = dpkt.pcap.Reader(decompressed)
    return packets

def main():
    if len(sys.argv) != 4:
        print("Syntax Error: make_vhash_content_type.py pcap_file table_name packet_counter")

    pfile = sys.argv[1]
    table_name = sys.argv[2]
    max_packets = int(sys.argv[3])
    count = 0
    bar = tqdm(total = max_packets)

    if pfile.endswith('.pcap'): packets = read_pcap(pfile)
    if pfile.endswith('.pcap.zst'): packets = read_pcap_zst(pfile)

    for ts, buf in packets:
        bar.update(1)
        try: 
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            print("Faile parse Frame")

        if type(eth.data) == dpkt.ip.IP:
            ip = eth.data
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data
                try:
                    dstport = tcp.dport
                    payload = tcp.data 
                    if len(payload) > 0:
                        vhash = hashlib.md5(payload).hexdigest()
                        if vhash not in vhash_dict:
                            vhash_dict[vhash] = ''
                        else: continue

                        try:
                            #p = payload.decode('utf-8').rstrip()
                            p = payload.decode('utf-8')
                            pay_type = "text"
                        except:
                            pay_type = "binary"

                        vhash_dict[vhash] = [payload.hex()]
                        vhash_dict[vhash].append(pay_type)
                except:
                    continue

    data = []
    df = pd.DataFrame(vhash_dict.values(), columns = ["payload_content", "payload_type"])
    df["vhash"] = vhash_dict.keys()
    columns = ["vhash", "payload_type", "payload_content"]
    df = df[columns]

    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/vhash_content?charset=utf8')
    connection = engine.connect()
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    connection.close()
    print("Appended Data", table_name, "to MySQL server")

    connector = mysql.connector.connect(host='localhost', user='pison', password='Ramen!yokosuka2023', database='vhash_content')
    cursor = connector.cursor()
    query_index = 'ALTER TABLE ' + table_name +' ADD INDEX vhash_index(vhash(64))'
    cursor.execute(query_index)
    print("Create Index Successfull")
                    
if __name__ == "__main__":
    main()

#content_list.append(payload.decode('utf-8', errors='ignore'))
#columns = ["vhash", "content", "payload_type"]
