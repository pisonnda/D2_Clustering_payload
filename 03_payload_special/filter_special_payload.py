#!/usr/bin/python3
import csv 
import sys
from tqdm import tqdm

# Get List of day_n.csv
payload_dict = {}
bar = tqdm(total = 1738084320)
file_list = sorted(sys.argv[1:])
#print(file_list)

# Get Special Payload with Filtering
for ifile in file_list:
    with open(ifile, "r") as fp:
        buf = fp.readlines()
    for line in buf:
        bar.update(1)
        line = line.rstrip()
        as_num, vhash = line.split(",")
        if vhash not in payload_dict:
            payload_dict[vhash] = as_num;
        elif as_num != payload_dict[vhash]:
            payload_dict[vhash] = "null"
        else:
            continue

# Output vhash, as_num of Special Payload
for k in payload_dict.keys():
    if payload_dict[k] != "null":
        print("{},{}".format(k, payload_dict[k]))
