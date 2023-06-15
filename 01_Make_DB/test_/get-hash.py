#!/usr/bin/python3
import dpkt
import hashlib
import sys
import zstandard as zstd

payloads = {}
listpay = []

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


def main(pfile):
    count = 0
    if pfile.endswith('.pcap'): packets = read_pcap(pfile)
    if pfile.endswith('.pcap.zst'): packets = read_pcap_zst(pfile)

    for ts, buf in packets:
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
                        print(vhash, end = '\t')
                        print(payload.decode('utf-8', errors='ignore'))
                except:
                    continue
                    
if __name__ == "__main__":
    main(sys.argv[1])
