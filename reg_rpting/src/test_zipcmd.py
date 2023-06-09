import csv

# this script will convert that big csv with lots of columns to a simplified 3 column output
# input file needs to be in CSV format
# Country,MIC,ISIN,CFI,TRDNG_START_DATE,TRDNG_TERMINATION_DATE,OK,CHECK,INCONSISTENT,2020-10-01, .......

# output will give ISIN, REPORT_DATE, VALUE

input_file="IE_LEUF_QUANTCOMPLETENESS_2022-02-09.csv"
output_file="IE_LEUF_QUANTCOMPLETENESS_2022-02-09_converted.csv"


o_fd = open(output_file, 'w+')
#print reader.next()
dict1 = {}

with open(input_file) as input_fd:
    reader = csv.reader(input_fd, delimiter=',')
    headers = next(reader)[1:]   # create a list of all the date columns from the header record
    line_count = 0
    for row in reader:
        isin = row[2]
        for key, value in zip(headers, row[1:]):
            if value == 'CHECK':
                write_file = '%s, %s, %s\n' % (isin, key, value)
                o_fd.write(write_file)

o_fd.close()

