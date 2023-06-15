#!/usr/bin/bash

function count_a(){
    counter=$(ps -ef | grep make* | grep -v grep | wc -l)
    echo $counter
}

ls /data/darknet/2017/2017-09-1*.pcap.zst | while read pcap_file 
do
    n=`count_a`
    while [ $n -ge 5 ]
        do
            sleep 2m
            n=`count_a`
        done
    result=`basename $pcap_file .pcap.zst|sed 's/-//g'`
    db_name=`echo db_$result`
    ./make_payl_db.py $pcap_file $ASNUM $db_name &
    echo "./make_payl_db.py $pcap_file $ASNUM $db_name &"
done

#ASNUM=$1
#ls /data/darknet/2017/2017-09-1*.pcap.zst | while read pcap_file 
#do
#    result=`basename $pcap_file .pcap.zst|sed 's/-//g'`
#    db_name=`echo db_$result`
#    ./make_payl_db.py $pcap_file $ASNUM $db_name &
#    echo "./make_payl_db.py $pcap_file $ASNUM $db_name &"
#done



#./make_payl_db.py /data/darknet/2017/2017-09-06.pcap.zst $1  db_170906 &
#./make_payl_db.py /data/darknet/2017/2017-09-07.pcap.zst $1  db_170907 &
#./make_payl_db.py /data/darknet/2017/2017-09-08.pcap.zst $1  db_170908 &
#./make_payl_db.py /data/darknet/2017/2017-09-09.pcap.zst $1  db_170909 &
#./make_payl_db.py /data/darknet/2017/2017-09-10.pcap.zst $1  db_170910 &
#./make_payl_db.py /data/darknet/2017/2017-09-11.pcap.zst $1  db_170911 &
#./make_payl_db.py /data/darknet/2017/2017-09-12.pcap.zst $1  db_170912 &
#./make_payl_db.py /data/darknet/2017/2017-09-13.pcap.zst $1  db_170913 &
#./make_payl_db.py /data/darknet/2017/2017-09-14.pcap.zst $1  db_170914 &
#./make_payl_db.py /data/darknet/2017/2017-09-15.pcap.zst $1  db_170915 &
#./make_payl_db.py /data/darknet/2017/2017-09-16.pcap.zst $1  db_170916 &
#./make_payl_db.py /data/darknet/2017/2017-09-17.pcap.zst $1  db_170917 &
#./make_payl_db.py /data/darknet/2017/2017-09-18.pcap.zst $1  db_170918 &
#./make_payl_db.py /data/darknet/2017/2017-09-19.pcap.zst $1  db_170919 &

#./make_payl_db.py /data/darknet/2017/2017-09-20.pcap.zst $1  db_170920 &
#ps -ef | grep make* | awk '{print$2}' | while read pid; do kill $pid; done
