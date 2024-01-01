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

# Specify the input text file name
input_file_name = "input.txt"

# Read data from the input text file
with open(input_file_name, 'r') as input_file:
    data = json.load(input_file)

# Specify the CSV file name
csv_file_name = "output.csv"

# Write data to CSV file
with open(csv_file_name, 'w', newline='') as csvfile:
    fieldnames = data[0].keys()
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    csvwriter.writeheader()

    # Write data
    csvwriter.writerows(data)

print(f"Data from {input_file_name} has been successfully written to {csv_file_name}")

