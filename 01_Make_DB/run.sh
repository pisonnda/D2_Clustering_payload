#!/usr/bin/bash

DB_NAME=$1
function count_a(){
    counter=$(ps -ef | grep make | grep -v grep | wc -l)
    echo $counter
}

ls /data/darknet/2017/2017-09-*.pcap.zst | while read pcap_file 
do
    echo $pcap_file
    n=`count_a`
    #echo $n
    while [ $n -ge 5 ]
        do
            #echo "Waiting for next Thread"
            #echo `date`
            sleep 2m
            n=`count_a`
        done
    result=`basename $pcap_file .pcap.zst|sed 's/-//g'`
    table_name=`echo db_$result`
    packets_counter=`zstd -dc $pcap_file |capinfos - | grep "Number of packets =*" | awk '{print $5}'`

    #echo "$pcap_file $packets_counter"
    ./make_data.py $pcap_file $packets_counter $DB_NAME $table_name &
done
