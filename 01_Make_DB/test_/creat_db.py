#!/usr/bin/python3
#2023.04.12: 宛先ごとのパケット数・送信元数を求める。

import csv
import dpkt
import geoip2.database
import mysql.connector
import pandas as pd
import socket
import sys
import zstandard as zstd
from mysql.connector import Error


########################初期化###############################
if len(sys.argv) != 2: 
    print("Syntax Error")
    print("Syntax: make_data_dest.py <pcap_file.pcap.zst>")
    sys.exit()

pcap_file = sys.argv[1]
dst_dict = {}

########################DATABASE###############################
#データベースサーバーへ接続
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#データベースを作成
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

#データベース・へ接続
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#命令を送る
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

########################PCAP-FILE###############################
#Function1: Extract pcap file from .zst compress and read with dpkt --> all packet = packets
def extract_zst(zstfile):
	with open(zstfile, "rb") as f:
		data = f.read()

	dctx = zstd.ZstdDecompressor()
	decompressed = dctx.stream_reader(data)
	packets = dpkt.pcap.Reader(decompressed)
	print("------Extract .zst and read as Pcap Successfull------")
	return packets

#Read: .PCAP File
def read_pcap(pfile):
	fp = open(pfile, "rb")
	packets = dpkt.pcap.Reader(fp)
	return packets

#Make List of Data (Times, SrcIP, DestIP)
def make_data(pcr):
    data = []
    packet_count = 0
    #Read Pacapfile and Count packet of each Source IP
    for ts,buf in pcr:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            packet_count += 1
        except:
            print('Fail parse FrameNo:', packet_count, '. skipped.')
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

                src_ip = socket.inet_ntoa(ip.src)
                dst_ip = socket.inet_ntoa(ip.dst)
                ipid = ip.id
                ttl = ip.ttl

                sport = tcp.sport
                try:
                    dport = tcp.dport
                except: continue
                seq_num = tcp.seq
                winds = tcp.win

                phrase = []
                phrase = [ts, src_ip, dst_ip, ttl, ipid, sport, dport, seq_num, winds, isrcip, dstip]
                data.append(phrase)
    return data

def main():
    pcr = extract_zst(pcap_file)
    #pcr = read_pcap(pcap_file)
    dat_list = make_data(pcr)

    pw = 'Ramen!yokosuka2023'
    db = "Darknet17"
    connection = create_server_connection("localhost", "pison", pw)

    #データベースを作成する（一回のみ）
    create_database_cmd = "CREATE DATABASE " + db
    create_database(connection, create_database_cmd)

    #テーブルを作成
    create_table = """
        CREATE TABLE dat_170901 (
            TIME DOUBLE(16,4), 
            SRCIP VARCHAR(15),
            DSTIP VARCHAR(15),
            TTL INT, 
            IPID LONG, 
            SPORT INT, 
            DPORT INT,
            SEQ_NUM LONG, 
            WINDS LONG,
            I_SRCIP LONG, 
            I_DSTIP LONG
            );
    """
    connection = create_db_connection("localhost", "pison", pw, db)
    execute_query(connection, create_table)

    connection = create_db_connection("localhost", "pison", pw, db)
    mkdat_query = \
                "INSERT INTO dat_170901 \
                (TIME, SRCIP, DSTIP, TTL, IPID, SPORT, DPORT, SEQ_NUM, WINDS, I_SRCIP, I_DSTIP) VALUES \
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    cursor.executemany(mkdat_query, dat_list)
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    main()
