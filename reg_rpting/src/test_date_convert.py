import csv
from datetime import datetime
from pytz import timezone

INPUT_FILE='C:\\mytmp\\test-dates.csv'
output_file='C:\\mytmp\\test-dates-converted.csv'
o_file=open(output_file, encoding='utf8', mode='w')

fmt = "%Y-%m-%dT%H:%M:%S.%f"

with open(INPUT_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        input_date_str_uktime = row[0] + 'T' + row[1]
#        print(input_date_str_uktime)
        input_date_str_with_tz = datetime.strptime(input_date_str_uktime, fmt).astimezone(timezone('Europe/London'))
        input_date_str_utc=input_date_str_with_tz.astimezone(timezone('UTC'))
        print('input date uk time=', input_date_str_with_tz, '\tconverted to UTC=', input_date_str_utc)
        o_file.write(input_date_str_with_tz.strftime(fmt) +  ',' +  input_date_str_utc.strftime(fmt) + '\n')
