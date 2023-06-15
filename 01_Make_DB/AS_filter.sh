#!/usr/bin/bash

AS_NUM=$1
function count_a(){
    counter=$(ps -ef | grep make | grep -v grep | wc -l)
    echo $counter
}

ls /data/darknet/2017/2017-09-1[2,3,4,5,6]*.pcap.zst | while read pcap_file 
do
    echo $pcap_file
    n=`count_a`
    echo $n
    while [ $n -ge 5 ]
        do
            echo "Waiting for next Thread"
            echo `date`
            sleep 2m
            n=`count_a`
        done
    result=`basename $pcap_file .pcap.zst|sed 's/-//g'`
    table_name=`echo db_$result`
    ./make_db_AS_filter.py $pcap_file $AS_NUM $table_name &
    echo "./make_db_AS_filter.py $pcap_file $AS_NUM $table_name"
done
