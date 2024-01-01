import pandas as pd
import json
# json to csv - using pandas

# this worked, but i need to put a [ right at top and close with ] at the end of the file

#input_file = "input_file.json"
input_file = "test.json"

# pandas read JSON File
df = pd.read_json(input_file)
df.to_csv('output.csv')

