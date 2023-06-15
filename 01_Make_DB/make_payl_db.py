#!/usr/bin/python3
###################################################################################################################
#                                     Program Read Pcap file and output to MySQL                                  #   
# Version1: 2023.05.18                                                                                            #
#["TIME", "ASN", "SRCIP", "DSTIP", "TTL", "IPID", "SPORT", "DPORT", "SEQ_N", "WINDS", "ISRCIP", "IDSTIP", "VHASH"]#
###################################################################################################################

import csv
import dpkt
import geoip2.database
import hashlib
import mysql.connector
import pandas as pd
import socket
import sys
import zstandard as zstd
from mysql.connector import Error
from sqlalchemy import create_engine


#初期化
if len(sys.argv) != 4: 
    print("Syntax Error")
    print("Syntax: make_payl_db.py <pcap_file.pcap.zst> db_name table_name")
    sys.exit()

pcap_file = sys.argv[1]
db_name = sys.argv[2]
table_name = sys.argv[3]
dst_dict = {}
reader = geoip2.database.Reader('/home/pison/geo_asn/GeoLite2-ASN.mmdb')
label = ["ts", "as_num", "srcip", "dstip", "ttl", "ipid", "sport", "dport", "seq_n", "winds", "isrcip", "idstip", "vhash"]

#Read-Pcap-file
#Function1: Extract pcap file from .zst compress and read with dpkt --> all packet = packets
def read_pcap(pcap_file):
    fp = open(pcap_file, "rb")
    packets = dpkt.pcap.Reader(fp)
    return packets

def read_pcap_zst(zstfile):
    with open(zstfile, "rb") as f:
        data = f.read()
    dctx = zstd.ZstdDecompressor()
    decompressed = dctx.stream_reader(data)
    packets = dpkt.pcap.Reader(decompressed)
    return packets

#Make List of Data
def make_data(packets):
    data = []
    packet_counter = 0
    #Read Pcap_file and Count packet of each Source IP
    for ts,buf in packets:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            packet_counter += 1
        except:
            print('Fail parse FrameNo:', packet_counter, '. skipped.')
            continue

        if type(eth.data) == dpkt.ip.IP:
            ip = eth.data
            isrcip = int.from_bytes(ip.src, "big")
            dstip = int.from_bytes(ip.dst, "big")
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data
                #防大の送信元を無視する
                if (isrcip & 0xFFFFF000) == 0xCA195000: continue
                #防大の宛先意外を無視する
                if (dstip & 0xFFFFF000) != 0xCA195000: continue
                #SINET
                if  isrcip == 0x9663C7E1 or \
                    isrcip == 0x9663C7E2 or \
                    dstip == 0x9663C7E2:
                        continue
                #HONEYPORT
                if dstip == 0xCA19550A or \
                dstip == 0xCA195510:
                    continue

                ipid = ip.id
                ttl = ip.ttl
                src_ip = socket.inet_ntoa(ip.src)
                dst_ip = socket.inet_ntoa(ip.dst)
                #Get AS-Number
                try:
                    response = reader.asn(src_ip)
                except:
                    asn = -1
                    continue
                asn = response.autonomous_system_number

                try:
                    sport = tcp.sport
                except: 
                    print("Error at packets: %s\t%s", ts, packet_counter)
                    continue

                try:
                    dport = tcp.dport
                except: 
                    print("Error at packets: %s\t%s", ts, packet_counter)
                    continue
                seq_num = tcp.seq
                winds = tcp.win
                payload = tcp.data
                vhash = hashlib.md5(payload).hexdigest()

                phrase = []
                phrase = [ts, asn, src_ip, dst_ip, ttl, ipid, sport, dport, seq_num, winds, isrcip, dstip, vhash]
                data.append(phrase)
    return pd.DataFrame(data, columns=label)

def main():
    if pcap_file.endswith('.pcap'): packets = read_pcap(pcap_file)
    if pcap_file.endswith('.pcap.zst'): packets = read_pcap_zst(pcap_file)

    df = make_data(packets)
    engine = create_engine('mysql+pymysql://pison:Ramen!yokosuka2023@localhost/' + db_name + '?charset=utf8')
    connection = engine.connect()
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    connection.close()

if __name__ == "__main__":
    main()
