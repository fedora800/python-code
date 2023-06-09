import csv
from datetime import datetime
from pytz import timezone

#INPUT_FILE='C:\\mytmp\\test-date-epoch-times.csv'
INPUT_FILE='C:\\mytmp\\\\redline_swiss\DUFN.S'
#output_file='C:\\mytmp\\test-date-epoch-times-converted.csv'
output_file=INPUT_FILE + '_out.csv'
o_file=open(output_file, encoding='utf8', mode='w')

fmt = "%Y-%m-%dT%H:%M:%S.%f"


#millseconds = 1646627400000.228000
#millseconds = 984567.224325
#millseconds = 1646627400.224325     # works
#millseconds = 1646627400000228000
#millseconds = 1646627400.228000 # works
#datetime_x = datetime.fromtimestamp(millseconds)
#print(datetime_x)
#print(type(datetime_x))




with open(INPUT_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # This skips the first row of the CSV file.
    next(csv_reader)
    for row in csv_reader:
        #print(row)
        symbol=row[0]
        orig_exchange_time=row[3]
        # using the exchange_time as they provided does not work when trying to get the milliseconds
        # need to do the below by extracting 1st 10 chars for the datetime and skip next 3 chars and then the milliseconds component
        #exchange_time=int(row[3][0:13])
        # so 1646627400000228000 becomes 1646627400.228000
        exchange_time=float(row[3][0:10] + '.' + row[3][13:])
        #print(exchange_time)
        #dt = datetime.fromtimestamp(exchange_time / 1000)
        dt = datetime.fromtimestamp(exchange_time)
        best_bid_price=row[4]
        best_ask_price=row[6]
        print(symbol, exchange_time, best_bid_price, best_ask_price, dt)
        o_file.write(symbol + ',' + orig_exchange_time + ',' + best_bid_price + ',' + best_ask_price + ',' + dt.strftime("%Y-%m-%d_%H:%M:%S.%f") + '\n')
        #o_file.write(symbol  + '\n')


"""
1646627400000 228000
1524349374099

mills = 1524349374099
dt3 = datetime.datetime.fromtimestamp(mills / 1000)
5
6print(dt3)
7>> 2018-04-22 07:22:54.099000

"""

