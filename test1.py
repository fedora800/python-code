import csv
import json

# Specify the input file containing the data
input_file = "test.json"  # Replace with your actual file path

# Specify the output CSV file name
output_file = "output.csv"

# Open the input file in read mode
with open(input_file, "r") as file:
    # Read all the data as a single string
    data_string = file.read()

# Split the data string into individual JSON objects, handling potential trailing commas
json_data = [json.loads(item.strip()) for item in data_string.split("}") if item.strip()]

# Open the output CSV file in write mode
with open(output_file, "w", newline="") as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write the header row using keys from the first JSON object
    header = list(json_data[0].keys())
    csv_writer.writerow(header)

    # Write each row of data from the JSON objects
    for item in json_data:
        row = [item[key] for key in header]
        csv_writer.writerow(row)

print("Data converted to CSV successfully!")

