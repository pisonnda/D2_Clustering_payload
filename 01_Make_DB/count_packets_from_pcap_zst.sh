ls /data/darknet/2017/2017-09-*.pcap.zst | while read pcap_file 
do
    echo -n "$pcap_file:" >> count_packets.md
    zstd -dc $pcap_file |capinfos - | grep "Number of packets =*" | awk '{print $5}' >> count_packets.md
done
