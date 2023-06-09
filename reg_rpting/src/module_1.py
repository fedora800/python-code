'''
Created on 17 Jul 2019

@author: sshinde
'''
import csv
from builtins import zip

INPUT_FILE="Z:\downloads\equity_completeness_file_November_2019_test.csv"
output_file="Z:\downloads\equity_completeness_file_November_2019_converted.csv"

print("starting ....")

o_fd = open(output_file, 'w+')
#print reader.next()
dict1 = {}

with open(INPUT_FILE) as input_fd:
    reader = csv.reader(input_fd, delimiter=',')
    headers = next(reader)[1:]
    print('headers=',headers)
    line_count = 0
    for row in reader:
        line_count=line_count+1
        
        print('line=', line_count, 'row=',row)
        #print('row0=', row[0])
        print('row1:=', row[1:])
        isin=row[0]
        for key, value in zip(headers, row[1:]):   # this will do a 1 to 1 tuple pair and return an iterator. so (date1, '') (date2, '') ... (dateN, 'CHECK') ...
            #print('==key==', key, '==value==', value)
            if value == 'CHECK':
            #if value == 'N':
                write_file = '%s, %s, %s,\n' % (isin, key, value)
                o_fd.write(write_file)
o_fd.close()
print("completed ....")



#1 import os, sys
