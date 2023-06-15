#!/usr/bin/python3
#2022.12.01: Program Get Top Source IP Address on Specific Port
#2023.01.13: Convernt to: Time,AS,Destination
#2023.03.01: Get IP of AS42570 Network Scanning, Destination IP, Port

import csv
import dpkt
import geoip2.database
import socket
import sys
import zstandard as zstd

if len(sys.argv) != 3: 
    print("Syntax Error")
    print("Syntax: asn_dest.py <pcap_file.pcap.zst> AS_number")
    sys.exit()

# Read Data Base of ASN
reader = geoip2.database.Reader('./geo_asn/GeoLite2-ASN.mmdb')

print("----------Information----------")
pcap_file = sys.argv[1]
print("pcap_file: ", pcap_file)
AS_num = sys.argv[2]
print("AS_num: ", AS_num)

#Function1: Extract pcap file from .zst compress and read with dpkt --> all packet = packets
def extract_zst(zstfile):
	with open(zstfile, "rb") as f:
		data = f.read()

	dctx = zstd.ZstdDecompressor()
	decompressed = dctx.stream_reader(data)
	packets = dpkt.pcap.Reader(decompressed)
	print("------Extract .zst and read as Pcap Successfull------")
	return packets

pcr = extract_zst(pcap_file)

#Read Pacapfile and Count packet of each Source IP
for ts,buf in pcr:
    try:
        eth = dpkt.ethernet.Ethernet(buf)
    except:
        print('Fail parse FrameNo:', packet_count, '. skipped.')
        continue
    if type(eth.data) == dpkt.ip.IP:
        ip = eth.data
        isrcip = int.from_bytes(ip.src, "big")
        dstip = int.from_bytes(ip.dst, "big")

        #防大の送信元を無視する
        if (isrcip & 0xFFFFF000) == 0xCA195000: continue
        #SINET
        if  isrcip == 0x9663C7E1 or \
            isrcip == 0x9663C7E2 or \
            dstip == 0x9663C7E2:
                continue
        #HONEYPORT
        if dstip == 0xCA19550A or \
        dstip == 0xCA195510:
            continue

        #Get destination port
        if ip.p == dpkt.ip.IP_PROTO_TCP:
            TCP = ip.data
            try: 
                dest_port = TCP.dport
            except:
                continue
        else: continue

        dport = int(dest_port)
        #Shiraishi moto no co-do
        src_ip = socket.inet_ntoa(ip.src)
        #dest_ip = socket.inet_ntoa(ip.dst)
        try:
            response = reader.asn(src_ip)
        except:
            asn = -1
            continue
        asn = response.autonomous_system_number
        #if asn == 42570:
        if asn == AS_num:
            print("{},{},{}".format(ts, isrcip, dstip))
        else:
            continue

        #data.append("{},{},{}".format(asn, src_ip, dest_ip))
#with open(ofile, "w") as fp:
#    fp.write('\n'.join(data))
#fp.close()
