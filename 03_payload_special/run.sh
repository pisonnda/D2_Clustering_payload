#!/usr/bin/bash

# Filter special payload
#python filter_special_payload.py 10_csv/*.csv > result_special_payload_September_2017.csv

#
#cut -d, -f2 *Sep* | sort | uniq -c | sort -nr >  result_count_special_payloads_from_as.csv


IFILE=$1
cut -d, -f1 $IFILE | while read vhash; 
do 
    ./query.py $vhash
done
