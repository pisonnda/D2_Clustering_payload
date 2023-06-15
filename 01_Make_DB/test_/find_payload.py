#!/usr/bin/python3
#Version1: get payload packet's header information -> .csv file
import csv
import dpkt 
import hashlib
import os 
import matplotlib.pyplot as plt
import sys
import seaborn as sns 
import pandas as pd
import zstandard as zstd

def extract_zst(pcap_file):
	with open(pcap_file, "rb") as f:
		data = f.read()
	dctx = zstd.ZstdDecompressor()
	decompressed = dctx.stream_reader(data)
	packets = dpkt.pcap.Reader(decompressed)
	return packets


if len(sys.argv) < 3: 
    print("Syntax Error")
    print("find_payload.py hash_value list_file")
    sys.exit()

find_hash = sys.argv[1]
ofile = str(find_hash) + ".csv"
pcap_files = sys.argv[2:]
metaif = ["IPID", "TTL","SRCIP", "DSTIP", "SPORT", "DPORT", "TSEQ", "WINDS"]
datalist = []


for pcap_file in pcap_files:
    if pcap_file.endswith(".pcap"):
        f = open(pcap_file, "rb")
        packets = dpkt.pcap.Reader(f)
    if pcap_file.endswith(".pcap.zst"):
        packets = extract_zst(pcap_file)
    for ts, buf in packets:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            continue
        if type(eth.data) == dpkt.ip.IP:
            ip = eth.data
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data
                try:
                    tdport = tcp.dport
                    payload = tcp.data
                    if len(payload) == 0 : continue
                    vhash =  hashlib.md5(payload).hexdigest()
                    if vhash == find_hash:
                        ipid  = ip.id
                        ipttl = ip.ttl
                        srcip = int.from_bytes(ip.src, "big")
                        dstip = int.from_bytes(ip.dst, "big")
                        tsport = tcp.sport
                        tseq   = tcp.seq
                        twin   = tcp.win
                        phrase = [ipid, ipttl, srcip, dstip , tsport, tdport, tseq, twin]
                    datalist.append(phrase)
                except:
                    continue

df = pd.DataFrame(datalist, columns=metaif)
df.to_csv(ofile, encoding='utf-8')
