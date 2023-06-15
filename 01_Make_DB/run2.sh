#!/usr/bin/bash

ASNUM=$1
./make_payl_db.py /data/darknet/2017/2018-09-06.pcap.zst $ASNUM $db_name &

ls /data/darknet/2017/2017-09-0[7,8,9,10].pcap.zst | while read pcap_file 
do
    while :
        do
            count=`ps -ef | grep make* | grep -v "grep" | wc -l`
            if [ $count -lt 5 ]; then
                result=`basename $pcap_file .pcap.zst|sed 's/-//g'`
                db_name=`echo db_$result`
                ./make_payl_db.py $pcap_file $ASNUM $db_name &
                echo "./make_payl_db.py $pcap_file $ASNUM $db_name &"
                continue
            elif [ $count -eq 0 ]; then
               exit 0 
            else
                echo "Waiting for next thread"
                sleep 2m
            fi
        done
done
