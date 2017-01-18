#!/usr/bin/python
# -*- coding: latin-1 -*-

# merge different log files
# USAGE: python merge_markerlists list1 list2 sort_by
# sort_by can be 'time' or 'synctime'

import sys, time, re
from operator import itemgetter

infilename1 = sys.argv[1]
infilename2 = sys.argv[2]
master_list = []
synctime1 = '00:00:00'
synctime2 = '00:00:00'

fin1 = open(infilename1, 'r')
fin2 = open(infilename2, 'r')

def parse_infile(f):
    global master_list
    entries = -1
    for line in f:
        r = re.search(r'\bSynctime is \b', line)
        if r is not None:
            synctime = line[r.end():-1]
        e = re.search(r'\bTime\t\tSynctime\tSignificance\tComment\b', line)
        if entries > -1:
            master_list.append(line.split('\t'))
            entries += 1
        if e is not None:
            entries = 0
    return synctime

synctime1 = parse_infile(fin1)
synctime2 = parse_infile(fin2)
print synctime1, synctime2

sort_by = sys.argv[3]
if sort_by == 'time': sort_code = 0
if sort_by == 'synctime': sort_code = 1
master_list_sorted = sorted(master_list, key=itemgetter(sort_code))

outfilename = infilename1[:-4]+'_merged.txt'
f = open(outfilename, 'w')
f.write('Marker file for Crossadaptive project\n')
f.write('{} markers\n\n'.format(len(master_list_sorted)))
f.write('Merged from {} and {}\n'.format(infilename1, infilename2))
f.write('Synctime is {} and {} respectively \n\n'.format(synctime1,synctime2))
f.write('Time\t\tSynctime\tSignificance\tComment\n')
for item in master_list_sorted:
    print item
    s = item[0] + '\t' + item[1] + '\t' + item[2] + '\t\t' +  item[4]
    f.write(s)
    print(s)
f.close()
print('done')