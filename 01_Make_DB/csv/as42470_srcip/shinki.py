#!/usr/bin/python3

import glob
import time

def main():
    path_list = sorted(glob.glob('*.csv'))
    newlist = {}
    for csv_file in path_list:
        #20170910.csv
        print(csv_file[:8], end='\t')
        new_count  = 0
        uniq_count = 0
        with open(csv_file, "r") as fp:
            buf = fp.readlines()
            for line in buf:
                uniq_count += 1 
                line = line.rstrip()
                if(line not in newlist):
                    newlist[line] = 1
                    new_count +=1
                else:
                    newlist[line] +=1;
        print(uniq_count, end='\t')
        print(new_count)
    print("Total: ", len(newlist))

if __name__ == '__main__':
    main()
