import json
import csv

'''
format needs to be like below with those 2 additional [ ] brackets - 

[
    {"ticker": "00XJ1d_EQ", "type": "ETF", ... },
    {"ticker": "00XK1d_EQ", "type": "ETF", ... },
    ...
]
'''

# Specify the input and output file
input_file_name = "input.txt"
# Specify the CSV file name
csv_file_name = input_file_name + "-processed.csv"

# Read data from the input text file
with open(input_file_name, 'r') as input_file:
    data = json.load(input_file)


# Write data to CSV file
with open(csv_file_name, 'w', newline='') as csvfile:
    fieldnames = data[0].keys()
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    csvwriter.writeheader()

    # Write data
    csvwriter.writerows(data)

print(f"Data from {input_file_name} has been successfully written to {csv_file_name}")


#  19 \copy tbl_instrument (symbol, name, industry, exchange_code, asset_type) FROM '~/git-projects/python-code/timescaledb/data/tbl_instrument_data.csv' DELIMITER ',' CSV HE

# egrep "type.*ETF.*currency.*:.*GBP.*shortName" input.txt  | sed -e 's/.*,"shortName"://' -e 's/countryOfOrigin.*subclasses//' | sed 's/,.*fullName":/,/' | awk -F',' 'BEGIN {OFS=","} {print $1, $3, $4}' | sed -e 's/"description":"//' -e 's/"":\["//' -e 's/"]}//' -e 's/"//g' -e 's/$/,UNKNOWN,ETF/' > file.csv

# dbs_invest=# \copy tbl_instrument (symbol, name, note_1, exchange_code, asset_type) FROM '/tmp/file.csv' DELIMITER ',' CSV;

 
